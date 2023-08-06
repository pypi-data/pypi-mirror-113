"""mkdocs plugin for documentation generation

See https://www.mkdocs.org/user-guide/plugins/ for plugin API documentation
"""

from collections import defaultdict
import re
from experimaestro.mkdocs.annotations import shoulddocument
import requests
from urllib.parse import urljoin
from experimaestro.core.types import ObjectType, Type
import mkdocs
from pathlib import Path
from typing import List, Optional, Tuple, Type as TypingType
import importlib
import logging
import inspect
import mkdocs.config.config_options as config_options
from mkdocs.structure.pages import Page as MkdocPage
from experimaestro.core.objects import Config
import json
from docstring_parser.parser import parse as docstringparse

MODULEPATH = Path(__file__).parent


def md_protect(s):
    return re.sub(r"""([*`_{}[\]])""", r"""\\\1""", s)


class Configurations:
    def __init__(self):
        self.tasks = set()
        self.configs = set()


def relativepath(source: str, target: str):
    """Computes a relative path from source to target"""
    if source == target:
        return ""

    if source[-1] == "/":
        source = source[:-1]

    if target[-1] == "/":
        target = target[:-1]

    source_seq = source.split("/")
    target_seq = target.split("/")
    maxlen = min(len(source_seq), len(target_seq))

    i = 0
    while i < maxlen and target_seq[i] == source_seq[i]:
        i += 1

    path = [".."] * (len(source_seq) - i) + target_seq[i:]

    return "/".join(path)


class Documentation(mkdocs.plugins.BasePlugin):
    RE_SHOWCLASS = re.compile(r"::xpm::([^ \n]+)")

    config_scheme = (
        ("name", config_options.Type(str, default="Tasks and configurations")),
        ("modules", config_options.Type(list)),
        ("external", config_options.Type(list)),
        ("init", config_options.Type(list)),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # path to sets of XPM types
        self.configurations = defaultdict(lambda: Configurations())

        # Maps XPM types to markdown paths
        self.type2path = {}

    def on_config(self, config, **kwargs):
        # Import modules in init
        for module_name in self.config.get("init") or []:
            importlib.import_module(module_name)

        # Include documentation pages in config
        self.parsed = {}
        self.external = {}
        self.baseurl = config["site_url"]

        for item in self.config.get("external") or []:
            module_name, url = next(iter(item.items()))
            logging.info("Loading external mappings from %s", url)
            baseurl = str(urljoin(url, "."))
            mappings = requests.get(url).json()
            for module, path in mappings.items():
                self.external[module] = f"{baseurl}{path}"

        for name_packagename in self.config["modules"]:
            module_name, md_path = next(iter(name_packagename.items()))
            path_cfgs = self.configurations[md_path]
            if md_path.endswith(".md"):
                md_path = md_path[:-3]

            package = importlib.import_module(module_name)
            basepath = Path(package.__path__[0])

            for path in basepath.rglob("*.py"):
                parts = list(path.relative_to(basepath).parts)
                if parts[-1] == "__init__.py":
                    parts = parts[:-1]
                elif parts[-1].endswith(".py"):
                    parts[-1] = parts[-1][:-3]

                fullname = (
                    f"""{module_name}.{".".join(parts)}""" if parts else module_name
                )

                # Avoid to re-parse
                if fullname in self.parsed:
                    continue
                self.parsed[fullname] = f"{md_path}.html"

                try:
                    module = importlib.import_module(fullname)
                    for _, member in inspect.getmembers(
                        module, lambda t: inspect.isclass(t) and issubclass(t, Config)
                    ):
                        # Only include members of the module
                        if member.__module__ != fullname:
                            continue

                        d = (
                            path_cfgs.tasks
                            if getattr(member.__getxpmtype__(), "task", None)
                            is not None
                            else path_cfgs.configs
                        )

                        self.type2path[
                            f"{member.__module__}.{member.__qualname__}"
                        ] = f"{md_path}.html"

                        member.__xpmtype__.__initialize__()
                        d.add(member.__xpmtype__)
                except Exception as e:
                    logging.error(
                        "Error while reading definitions file %s: %s", path, e
                    )
        return config

    def on_post_build(self, config):
        mapping_path = Path(config["site_dir"]) / "experimaestro-mapping.json"
        logging.info("Writing mapping file %s", mapping_path)
        with mapping_path.open("wt") as fp:
            json.dump(self.parsed, fp)

    def showclass(self, location, m: re.Match):
        return self.getlink(location, m.group(1).strip())

    def _getlink(self, url, qualname: str) -> Tuple[str, Optional[str]]:
        """Get a link given a qualified name"""

        # Use an internal reference
        md_path = self.type2path.get(qualname, None)
        if md_path:
            return qualname, f"{relativepath(url, md_path)}#{qualname}"

        # Try to get an external reference
        module_name = qualname[: qualname.rfind(".")]
        baseurl = self.external.get(module_name, None)

        return qualname, f"{baseurl}#{qualname}" if baseurl else None

    def getlink(self, url, qualname: str):
        """Get a link given a qualified name"""
        qualname, href = self._getlink(url, qualname)
        if href:
            return f"[{qualname}]({href})"
        return qualname

    def getConfigLink(self, pageURL: str, config: TypingType):
        return self._getlink(pageURL, f"{config.__module__}.{config.__qualname__}")

    def build_doc(self, page: MkdocPage, lines: List[str], configs: List[ObjectType]):
        """Build the documentation for a list of configurations"""
        configs = sorted(configs, key=lambda x: str(x.identifier))
        for xpminfo in configs:
            fullqname = (
                f"{xpminfo.objecttype.__module__}.{xpminfo.objecttype.__qualname__}"
            )
            lines.extend(
                (
                    f"""### {xpminfo.title} <span id="{fullqname}"> </span>\n\n""",
                    f"""`from {xpminfo.objecttype.__module__} import {xpminfo.objecttype.__name__}`\n\n""",
                )
            )

            if xpminfo.description:
                lines.extend((xpminfo.description, "\n\n"))

            # Add parents
            parents = list(xpminfo.parents())
            if parents:
                lines.append("*Parents*: ")
                lines.append(
                    ", ".join(
                        self.getlink(page.url, parent.fullyqualifiedname())
                        for parent in parents
                    )
                )
                lines.append("\n\n")

            for name, argument in xpminfo.arguments.items():

                if isinstance(argument.type, ObjectType):
                    basetype = argument.type.basetype
                    typestr = self.getlink(
                        page.url, f"{basetype.__module__}.{basetype.__qualname__}"
                    )
                else:
                    typestr = argument.type.name()

                lines.append("- ")
                if argument.generator:
                    lines.append(" [*generated*] ")
                elif argument.constant:
                    lines.append(" [*constant*] ")
                lines.append(f"**{name}** ({typestr})")
                if argument.help:
                    lines.append(f"\n  {argument.help}")
                lines.append("\n\n")

            methods = [
                member
                for key, member in inspect.getmembers(
                    xpminfo.objecttype,
                    predicate=lambda member: inspect.isfunction(member)
                    and shoulddocument(member),
                )
            ]

            if methods:
                lines.append("**Methods**\n\n")
                for method in methods:
                    parseddoc = docstringparse(method.__doc__)
                    lines.append(
                        f"""- {md_protect(method.__name__)}() *{parseddoc.short_description}*\n"""
                    )

    def on_page_markdown(self, markdown, page: MkdocPage, **kwargs):
        """Generate markdown pages"""
        path = page.file.src_path

        markdown = Documentation.RE_SHOWCLASS.sub(
            lambda c: self.showclass(page.url, c), markdown
        )

        cfgs = self.configurations.get(path, None)
        if cfgs is None:
            return markdown

        lines = [
            markdown,
            "<style>",
            (MODULEPATH / "style.css").read_text(),
            "</style>\n",
            "<div><hr></div>",
            "*Documentation generated by experimaestro*\n",
        ]

        if cfgs.configs:
            lines.extend(["## Configurations\n\n"])
            self.build_doc(page, lines, cfgs.configs)

        if cfgs.tasks:
            lines.extend(["## Tasks\n\n"])
            self.build_doc(page, lines, cfgs.tasks)

        return "".join(lines)
