import os
import json
from sphinx.application import Sphinx
from stoplightio_schema_sphinx import schema_to_rst


def test_schema_to_rst(tmp_path):
    schema_path = tmp_path / "func.schema.json"
    schema = {"type": "object"}
    schema_path.write_text(json.dumps(schema))
    rst = schema_to_rst(schema)
    assert ".. code-block:: json" in "\n".join(rst)


def test_sphinx_build(tmp_path):
    srcdir = tmp_path / "src"
    os.makedirs(srcdir)
    (srcdir / "conf.py").write_text(
        "import os, sys\n"
        "sys.path.insert(0, os.path.abspath('.'))\n"
        "extensions=['sphinx.ext.autodoc','stoplightio_schema_sphinx']\n"
        "json_schema_dir=os.path.abspath('.')\n")
    (srcdir / "index.rst").write_text(".. autofunction:: module.func\n")
    (srcdir / "module.py").write_text("def func():\n    \"\"\"Do things.\"\"\"\n")
    schema = {'type': 'object'}
    (srcdir / "func.schema.json").write_text(json.dumps(schema))
    app = Sphinx(str(srcdir), str(srcdir), str(tmp_path/'out'), str(tmp_path/'doctrees'), "html")
    app.build()
    html = (tmp_path / 'out' / 'index.html').read_text()
    assert 'JSON Schema' in html
