import functools
from contextlib import contextmanager

import pytest

import vintage

_EXPECTED_VALUE = 6


def test_vintage(deprecated, expected_message):
    with _assert_single_deprecation() as w:
        deprecated()
    assert w.message == expected_message


##########################################################################

@pytest.fixture
def expected_message(deprecated, message, deprecated_type):
    if deprecated_type == 'method':
        func = deprecated.func._func  # pylint: disable=protected-access
        name = 'Sample.func'
    else:
        func = deprecated.func
        name = '{}.func'.format(__name__)
    assert func.__name__ == 'func'
    returned = '{} is deprecated.'.format(name)
    if message:
        returned += ' {}'.format(message)
    return returned


@pytest.fixture(params=['method', 'function'])
def deprecated_type(request):
    return request.param


@pytest.fixture
def deprecated(deprecated_type, message):
    if deprecated_type == 'method':
        class Sample(object):

            @_deprecate(message)
            def func(self, a, b, c):
                return a + b + c
        returned = Sample().func
    elif deprecated_type == 'function':
        @_deprecate(message)
        def func(a, b, c):
            return a + b + c
        returned = func

    else:
        raise NotImplementedError()  # pragma: no cover

    return functools.partial(returned, 1, 2, _EXPECTED_VALUE - 1 - 2)


def _deprecate(message):
    """Helper to sometimes simulate calling ``deprecated`` with parameters and sometimes plainly without any arguments
    """
    def decorator(func):
        if message:
            return vintage.deprecated(message=message)(func)
        return vintage.deprecated(func)
    return decorator


@pytest.fixture(params=[None, 'message here'])
def message(request):
    return request.param


@contextmanager
def _assert_single_deprecation():
    with pytest.deprecated_call() as w:
        yield _RecordProxy(w)


class _RecordProxy(object):

    def __init__(self, record):
        self._record = record

    def __getattr__(self, attr):
        # record.message is actually our warning
        w = self._record[0].message
        if attr == 'message':
            assert len(w.args) == 1
            return w.args[0]
        return getattr(w, attr)
