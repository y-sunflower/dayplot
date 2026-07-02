import base64
import tempfile
from typing import Any

import matplotlib
from bs4 import BeautifulSoup, Tag
from markdown import Markdown
from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
from mkdocs_matplotlib.plugin import (
    HIDECODE_SWITCH,
    HIDEOUTPUT_SWITCH,
    RENDER_SWITCH,
    _rendered_image_to_dir,
)


class MatplotlibRenderPostprocessor(Postprocessor):
    def run(self, text: str) -> str:
        soup = BeautifulSoup(text, features="html.parser")
        global_namespace: dict[str, Any] = {}
        local_namespace: dict[str, Any] = {}

        for code_tag in soup.find_all("code"):
            parent_code_tag = code_tag.parent
            if not isinstance(parent_code_tag, Tag) or parent_code_tag.name != "pre":
                continue

            raw_code = code_tag.text
            code_lines = raw_code.splitlines()
            if RENDER_SWITCH not in code_lines:
                continue

            is_hidecode = HIDECODE_SWITCH in code_lines
            is_hideoutput = HIDEOUTPUT_SWITCH in code_lines

            matplotlib.use("Agg", force=True)
            temp_file = tempfile.NamedTemporaryFile(suffix=".svg").name
            is_empty = _rendered_image_to_dir(
                temp_file, raw_code, global_namespace, local_namespace
            )

            if not is_hideoutput and not is_empty:
                with open(temp_file, "rb") as file:
                    encoded = base64.b64encode(file.read()).decode("ascii")
                img_tag = soup.new_tag(
                    "img",
                    src="data:image/svg+xml;base64," + encoded,
                )
                parent_code_tag.insert_after(img_tag)
                img_tag.wrap(soup.new_tag("center"))

            if is_hidecode:
                parent_code_tag.decompose()

        return str(soup)


class MatplotlibRenderExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.postprocessors.register(
            MatplotlibRenderPostprocessor(md), "matplotlib_render", 5
        )


def makeExtension(**kwargs: Any) -> MatplotlibRenderExtension:
    return MatplotlibRenderExtension(**kwargs)
