"""Sphinx extension for embedding JSON schemas in autodoc documentation."""
import json
import os
from typing import List, Dict, Any, Optional

SCHEMA_LINES_HEADER = ["", "**JSON Schema**", "", ".. code-block:: json", ""]


def schema_to_rst(schema: Dict[str, Any]) -> List[str]:
    """Convert JSON schema dict to rst lines."""
    return SCHEMA_LINES_HEADER + ["   " + line for line in json.dumps(schema, indent=2).splitlines()] + [""]


def load_schema(schema_dir: str, *, class_name: Optional[str], func_name: str) -> Optional[List[str]]:
    """Load schema file based on class/func names and return rst lines."""
    if class_name:
        filename = f"{class_name}.{func_name}.schema.json"
    else:
        filename = f"{func_name}.schema.json"
    path = os.path.join(schema_dir, filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    return schema_to_rst(schema)


def process_docstring(app, what, name, obj, options, lines) -> None:
    schema_dir = app.config.json_schema_dir
    if not schema_dir:
        return
    if what not in {"function", "method"}:
        return
    class_name = None
    func_name = name.split(".")[-1]
    if what == "method":
        parts = name.split(".")
        if len(parts) >= 2:
            class_name = parts[-2]
    rst_lines = load_schema(schema_dir, class_name=class_name, func_name=func_name)
    if rst_lines:
        lines.extend(rst_lines)


def setup(app):
    app.add_config_value("json_schema_dir", default=None, rebuild="html")
    app.connect("autodoc-process-docstring", process_docstring)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
