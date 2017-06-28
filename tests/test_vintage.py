import functools
import sys
import warnings
from contextlib import contextmanager

import pytest
import vintage

# pylint: disable=redefined-outer-name
_EXPECTED_VALUE = 6


def test_vintage(deprecated, expected_message):
    lineno = _get_lineno() + 2
    with _assert_single_deprecation() as rp:
        deprecated()
    assert rp.warning_message == expected_message
    if not hasattr(sys, 'pypy_version_info'):
        # on pypy, functools is implemented in Python so the frame would be wrong
        assert rp.filename == __file__
        assert rp.lineno == lineno


def test_deprecated_frame_correction():
    message = 'Some message'
    def some_function():
        @vintage.deprecated(message=message, frame_correction=1)
        def other_function():
            pass
        other_function()
    lineno = _get_lineno() + 2
    with _assert_single_deprecation() as rp:
        some_function()
    assert rp.warning_message == 'tests.test_vintage.other_function is deprecated. {}'.format(message)
    if not hasattr(sys, 'pypy_version_info'):
        # on pypy, functools is implemented in Python so the frame would be wrong
        assert rp.filename == __file__
        assert rp.lineno == lineno


def test_get_no_deprecations_context_for_decorator(deprecated, expected_message):
    with _assert_no_deprecation():
        with vintage.get_no_deprecations_context():
            deprecated()
    with _assert_single_deprecation() as rp:
        deprecated()
    assert rp.warning_message == expected_message


def test_get_no_deprecations_context_for_messages():
    msg = 'Hello'
    with _assert_no_deprecation():
        with vintage.get_no_deprecations_context():
            vintage.warn_deprecation(msg)
    with _assert_single_deprecation() as rp:
        vintage.warn_deprecation(msg)
    assert rp.warning_message == msg


def test_deprecated_property(message):

    class Sample(object):

        @property
        @vintage.deprecated(message=message)
        def prop(self):
            return _EXPECTED_VALUE

    with _assert_single_deprecation():
        assert Sample().prop == _EXPECTED_VALUE


def test_deprecated_doc(deprecated, since, message):
    expected_since = '.. deprecated:: {}'.format(since) if since else '.. deprecated'
    doc_lines = [l.strip() for l in deprecated.func.__doc__.splitlines()]
    assert expected_since in doc_lines
    if message is not None:
        assert message in doc_lines


def test_warn_deprecation():
    message = 'this is a message'
    lineno = _get_lineno() + 2
    with _assert_single_deprecation() as rp:
        vintage.warn_deprecation(message)

    assert rp.lineno == lineno
    assert rp.warning_message == message


##########################################################################

@pytest.fixture
def expected_message(deprecated, message, deprecated_type, what):
    if what:
        name = what
    else:
        if deprecated_type == 'method':
            func = deprecated.func._func  # pylint: disable=protected-access
            name = 'Sample.func'
        else:
            func = deprecated.func
            name = '{}.func'.format(__name__)
        assert func.__name__ == 'func'
    returned = '{} is deprecated'.format(name)
    if message:
        returned += '. {}'.format(message)
    return returned


def _get_lineno():
    return sys._getframe(1).f_lineno  # pylint: disable=protected-access


@pytest.fixture(params=['method', 'function'])
def deprecated_type(request):
    return request.param


@pytest.fixture
def deprecated(deprecated_type, message, since, what):
    if deprecated_type == 'method':
        class Sample(object):

            @_deprecate(message=message, since=since, what=what)
            def func(self, a, b, c):
                "docstring"
                return a + b + c

        returned = Sample().func
    elif deprecated_type == 'function':
        @_deprecate(message=message, since=since, what=what)
        def func(a, b, c):
            "docstring"
            return a + b + c
        returned = func

    else:
        raise NotImplementedError()  # pragma: no cover

    return functools.partial(returned, 1, 2, _EXPECTED_VALUE - 1 - 2)

def _deprecate(**kwargs):
    """Helper to sometimes simulate calling ``deprecated`` with parameters and sometimes plainly without any arguments
    """
    def decorator(func):
        if kwargs and set(kwargs.values()) != set([None]):
            return vintage.deprecated(**kwargs)(func)
        return vintage.deprecated(func)
    return decorator


@pytest.fixture(params=[None, 'message here'])
def message(request):
    return request.param


@pytest.fixture(params=[None, '3.2.1'])
def since(request):
    return request.param


@pytest.fixture(params=[None, 'my.special_function'])
def what(request):
    return request.param


@contextmanager
def _assert_single_deprecation():
    warnings.simplefilter('always')
    with warnings.catch_warnings(record=True) as recorded:
        yield _RecordProxy(recorded)
    assert len(recorded) == 1, 'No single warning captured'
    assert recorded[0].category == DeprecationWarning


@contextmanager
def _assert_no_deprecation():
    warnings.simplefilter('always')
    with warnings.catch_warnings(record=True) as recorded:
        yield _RecordProxy(recorded)
    assert len(recorded) == 0, 'Deprecation warning were captured'  # pylint: disable=len-as-condition


class _RecordProxy(object):

    def __init__(self, record):
        self._record = record

    def __getattr__(self, attr):
        # record.message is actually our warning
        return getattr(self._record[0], attr)

    @property
    def warning_obj(self):
        # warnings quirk - the message that is captured is actually the warning
        # object
        return self._record[0].message

    @property
    def warning_message(self):
        return self.warning_obj.args[0]
