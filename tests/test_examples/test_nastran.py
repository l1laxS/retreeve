import importlib.util
import os
from pprint import pprint


def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_basic_example():
    # Construct absolute path to your example script
    here = os.path.dirname(__file__)
    example_path = os.path.abspath(os.path.join(
        here, "../../examples/nastran/run.py"))

    # Load the module dynamically
    example_module = load_module_from_path("run_example_module", example_path)

    # Call the function inside the loaded module
    pprint(example_module.run_example())
