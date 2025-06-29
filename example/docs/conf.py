import os
import sys
sys.path.insert(0, os.path.abspath('../src'))
sys.path.insert(0, os.path.abspath('../../src'))

extensions = ['sphinx.ext.autodoc', 'stoplightio_schema_sphinx']

json_schema_dir = os.path.abspath('../schemas')

autodoc_default_options = {
    'members': True,
}
