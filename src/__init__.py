"""Package entry for src converters.

Avoid importing converter modules at package import time because some
modules may perform interactive prompts or side-effects when imported.

Provide a small helper to lazily load a converter by name.
"""
from importlib import import_module
from types import ModuleType
from typing import Callable


def get_converter(input_fmt: str, output_fmt: str) -> Callable[[str, str, str], None]:
	"""Return the convert(file_name, input_path, output_path) callable for the
	given input/output formats.

	Raises ImportError or AttributeError if the module or function is missing.
	"""
	module_name = f"src.{input_fmt}_{output_fmt}"
	mod: ModuleType = import_module(module_name)
	# converters should expose a function named `convert`
	return getattr(mod, "convert")


__all__ = ["get_converter"]