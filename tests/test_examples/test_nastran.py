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
    result = example_module.run_example()

    assert isinstance(result, list)
    assert len(result) == 4
    assert result[0].__class__.__name__ == "FallbackHandler"
    assert result[1].__class__.__name__ == "SolHandler"
    assert result[2].__class__.__name__ == "ExecControlHandler"
    assert result[3].__class__.__name__ == "BulkHandler"

    bulk = result[3]._contents
    assert len(bulk) == 32
    assert bulk[0].__class__.__name__ == "String"
    assert bulk[1].__class__.__name__ == "CommentHandler"
    assert bulk[2].__class__.__name__ == "CardHandler"
    assert bulk[3].__class__.__name__ == "CardHandler"
    assert bulk[4].__class__.__name__ == "CardHandler"
    assert bulk[5].__class__.__name__ == "CardHandler"
    assert bulk[6].__class__.__name__ == "CardHandler"
    assert bulk[7].__class__.__name__ == "FallbackHandler"
    assert bulk[8].__class__.__name__ == "CommentHandler"
    assert bulk[9].__class__.__name__ == "CardHandler"
    assert bulk[10].__class__.__name__ == "FallbackHandler"
    assert bulk[11].__class__.__name__ == "CommentHandler"
    assert bulk[12].__class__.__name__ == "CardHandler"  # PSHELL
    assert len(bulk[12]._contents) == 2
    assert bulk[13].__class__.__name__ == "FallbackHandler"
    assert bulk[14].__class__.__name__ == "CommentHandler"
    assert bulk[15].__class__.__name__ == "CardHandler"
    assert bulk[16].__class__.__name__ == "CardHandler"
    assert bulk[17].__class__.__name__ == "CardHandler"
    assert bulk[18].__class__.__name__ == "CardHandler"
    assert bulk[19].__class__.__name__ == "FallbackHandler"
    assert bulk[20].__class__.__name__ == "CommentHandler"
    assert bulk[21].__class__.__name__ == "CardHandler"  # MPC
    assert len(bulk[21]._contents) == 2
    assert bulk[22].__class__.__name__ == "FallbackHandler"
    assert bulk[23].__class__.__name__ == "CommentHandler"
    assert bulk[24].__class__.__name__ == "CardHandler"
    assert bulk[25].__class__.__name__ == "FallbackHandler"
    assert bulk[26].__class__.__name__ == "CommentHandler"
    assert bulk[27].__class__.__name__ == "CardHandler"
    assert bulk[28].__class__.__name__ == "CardHandler"
    assert bulk[29].__class__.__name__ == "FallbackHandler"
    assert bulk[30].__class__.__name__ == "CommentHandler"
    assert bulk[31].__class__.__name__ == "String"

    pprint(result)
