from functools import partial, singledispatch
from numbers import Complex, Number, Real
from typing import Any, Dict, List, Optional, Tuple, Union

import jax.numpy as jnp
import numpy as np
import yapf
from jax.interpreters.xla import DeviceArray
from jax.tree_util import tree_flatten, tree_map, tree_reduce

from .annotations import Array, PyTree
from .dtypes import default_atol, default_rtol

__all__ = ['assert_tree_allclose', 'tree_allclose', 'get_test_string', 'get_relative_test_string']


def assert_tree_allclose(actual: PyTree,
                         desired: PyTree,
                         original_name: Optional[str] = None,
                         original_value: Optional[PyTree] = None,
                         *,
                         column_limit: int = 100,
                         rtol: Optional[float] = None,
                         atol: Optional[float] = None) -> None:
    """
    Asserts that every tensor in an actual pytree matches the corresponding tensor in a desired
    pytree.  If the assertion fails, a passing test string is printed::

    ```python
    from tjax import assert_tree_allclose, dataclass, RealNumeric

    @dataclass
    class A:
        x: RealNumeric
        y: RealNumeric

    @dataclass
    class B:
        z: A

    original = B(A(1.2, 3.4))
    desired = B(A(3.0, 4.0))
    actual = B(A(1.2, 5.2))

    assert_tree_allclose(actual, desired)
    ```
    This prints::
    ```
    JAX trees don't match with rtol=0.0001 and atol=1e-06.
    Mismatched elements: 2 / 2 (100%)
    Maximum absolute difference: 1.8
    Maximum relative difference: 0.6
    Actual: B
        z=A
            x=1.2
            y=5.2

    Desired: B
        z=A
            x=3.0
            y=4.0

    Test string:
    actual = B(z=A(x=1.2, y=5.2))
    ```
    The test string can then be pasted.

    Args:
        actual: The actual value.
        desired: The desired value.
        original_name: The variable name that contains the original value.
        original_value: The original value.  This is usually a pytree like a dataclass that has the
            same type as actual and desired, but contains different values.
        rtol: The relative tolerance of the comparisons in the assertion.
        atol: The absolute tolerance of the comparisons in the assertion.
    """
    if rtol is None:
        rtol = default_rtol()
    if atol is None:
        atol = default_atol()

    flattened_actual, structure_actual = tree_flatten(actual)
    flattened_desired, structure_desired = tree_flatten(desired)
    if structure_actual != structure_desired:
        raise AssertionError(f"\nTree structure mismatch.\nActual: {actual}\nDesired: {desired}\n")

    for i, (actual_, desired_) in enumerate(zip(flattened_actual, flattened_desired)):
        try:
            np.testing.assert_allclose(actual_, desired_, rtol=rtol, atol=atol)
        except AssertionError as exception:
            old_message = exception.args[0].split('\n')
            best_part_of_old_message = "\n".join(old_message[3:6]).replace("Max ", "Maximum ")
            test_string = (get_relative_test_string(actual, original_name, original_value, rtol,
                                                    atol)
                           if original_name is not None and original_value is not None
                           else get_test_string(actual, rtol, atol))
            style_config = yapf.style.CreatePEP8Style()
            style_config['COLUMN_LIMIT'] = column_limit
            test_string = yapf.yapf_api.FormatCode("desired = " + test_string,
                                                   style_config=style_config)[0]
            message = (
                f"\nTree leafs don't match at position {i} with rtol={rtol} and atol={atol}.\n"
                f"{best_part_of_old_message}\n\n"
                f"Actual: {actual}\nDesired: {desired}\n"
                f"Test string:\n{test_string}")
            raise AssertionError(message) from None


def tree_allclose(actual: PyTree,
                  desired: PyTree,
                  rtol: Optional[float] = None,
                  atol: Optional[float] = None) -> bool:
    """
    Args:
        actual: The actual value.
        desired: The desired value.
        rtol: The relative tolerance of the comparisons in the comparison.
        atol: The absolute tolerance of the comparisons in the comparison.
    """
    if rtol is None:
        rtol = default_rtol()
    if atol is None:
        atol = default_atol()

    return tree_reduce(jnp.logical_and,
                       tree_map(partial(np.allclose, rtol=rtol, atol=atol), actual, desired),
                       True)


# get test string ----------------------------------------------------------------------------------
# Redefinition typing errors in this file are due to https://github.com/python/mypy/issues/2904.
@singledispatch
def get_test_string(actual: Any, rtol: float, atol: float) -> str:
    """
    Args:
        actual: The actual value that was produced, and that should be the desired value.
        rtol: The relative tolerance of the comparisons in the assertion.
        atol: The absolute tolerance of the comparisons in the assertion.
    Returns:
        A string of Python code that produces the desired value.
    """
    return str(actual)


@get_test_string.register(np.ndarray)
@get_test_string.register(DeviceArray)
def _(actual: Union[Array, DeviceArray], rtol: float, atol: float) -> str:
    def fts(x: Complex) -> str:
        return _float_to_string(x, rtol, atol)
    with np.printoptions(formatter={'float_kind': fts,
                                    'complex_kind': fts}):
        return "np." + repr(np.asarray(actual)).replace(' ]', ']').replace(' ,', ',').replace(
            '  ', ' ')


@get_test_string.register  # type: ignore
def _(actual: Complex, rtol: float, atol: float) -> str:
    x = float(actual) if isinstance(actual, Real) else complex(actual)
    return _float_to_string(x, rtol, atol)


@get_test_string.register  # type: ignore
def _(actual: Number, rtol: float, atol: float) -> str:
    return str(actual)


@get_test_string.register(list)  # type: ignore
@get_test_string.register(tuple)
def _(actual: Union[List[Any], Tuple[Any]], rtol: float, atol: float) -> str:
    is_list = isinstance(actual, list)
    return (("[" if is_list else "(")
            + ", ".join(get_test_string(sub_actual, rtol, atol)
                        for i, sub_actual in enumerate(actual))
            + ("]" if is_list else ")"))


@get_test_string.register(dict)  # type: ignore
def _(actual: Dict[Any, Any], rtol: float, atol: float) -> str:
    return '{' + ",\n".join(repr(key) + ': ' + get_test_string(sub_actual, rtol, atol)
                            for key, sub_actual in actual.items()) + '}'


# get relative test string -------------------------------------------------------------------------
@singledispatch
def get_relative_test_string(actual: Any,
                             original_name: str,
                             original: Any,
                             rtol: float,
                             atol: float) -> str:
    """
    Args:
        original_name: The name of the variable containing an original value.
        actual: The actual value that was produced, and that should be the desired value.
        original: The original value.
        rtol: The relative tolerance of the comparisons in the assertion.
        atol: The absolute tolerance of the comparisons in the assertion.
    Returns:
        A string of Python code that produces the desired value from an "original value" (could be
        zeroed-out, for example).
    """
    return str(actual)


@get_relative_test_string.register(np.ndarray)  # type: ignore
@get_relative_test_string.register(DeviceArray)
def _(actual: Union[Array, DeviceArray], original_name: str, original: Any, rtol: float,
      atol: float) -> str:
    def fts(x: Complex) -> str:
        return _float_to_string(x, rtol, atol)
    with np.printoptions(formatter={'float_kind': fts,
                                    'complex_kind': fts}):
        return "np." + repr(np.asarray(actual)).replace(' ]', ']').replace(' ,', ',').replace(
            '  ', ' ')


@get_relative_test_string.register  # type: ignore
def _(actual: Complex, original_name: str, original: Any, rtol: float, atol: float) -> str:
    return _float_to_string(actual, rtol, atol)


@get_relative_test_string.register  # type: ignore
def _(actual: Number, original_name: str, original: Any, rtol: float, atol: float) -> str:
    return str(actual)


@get_relative_test_string.register(list)  # type: ignore
@get_relative_test_string.register(tuple)
def _(actual: Union[List[Any], Tuple[Any]], original_name: str, original: Any, rtol: float,
      atol: float) -> str:
    is_list = isinstance(actual, list)
    return (("[" if is_list else "(")
            + ", ".join(get_relative_test_string(f"{original_name}[{i}]",
                                                 sub_actual, sub_original,
                                                 rtol, atol)
                        for i, (sub_actual, sub_original) in enumerate(zip(actual, original)))
            + ("]" if is_list else ")"))


@get_relative_test_string.register(dict)  # type: ignore
def _(actual: Dict[Any, Any], original_name: str, original: Any, rtol: float, atol: float) -> str:
    if not isinstance(original, dict):
        raise TypeError

    def relative_string(key, sub_actual):
        return get_relative_test_string(
            f"{original_name}[{key}]", sub_actual, original[key], rtol, atol)

    return '{' + ",\n".join(repr(key) + ': ' + relative_string(key, sub_actual)
                            for key, sub_actual in actual.items()) + '}'


# Private functions --------------------------------------------------------------------------------
def _float_to_string_with_precision(x: Union[float, complex], precision: int) -> str:
    with np.printoptions(precision=precision, floatmode='maxprec'):
        return repr(np.array(x))[6:-1]


def _float_to_string(x: complex, rtol: float, atol: float) -> str:
    y: Union[float, complex]
    if isinstance(x, Real):
        y = float(x)
    elif isinstance(x, Complex):
        y = complex(x)
    else:
        raise TypeError
    for i in range(20):
        retval = _float_to_string_with_precision(y, i)
        if np.allclose(complex(retval), x, rtol=rtol, atol=atol):
            break
    return retval
