import importlib.util
import os


def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_basic_example():
    # Construct absolute path to your example script
    here = os.path.dirname(__file__)
    example_path = os.path.abspath(os.path.join(here,
                                                "../../examples/basic/run.py"))

    # Load the module dynamically
    example_module = load_module_from_path("run_example_module", example_path)

    # Call the function inside the loaded module
    result = example_module.run_example()

    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0].__class__.__name__ == "TitleHandler"
    assert "TITLE: Lorem Ipsum" in str(result[0])
    assert len(result[0]._contents) == 3
