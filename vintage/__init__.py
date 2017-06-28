from contextlib import contextmanager
import functools
import threading
import warnings

from six import string_types


class _Local(threading.local):
    enabled = True

_local = _Local()


@contextmanager
def get_no_deprecations_context():
    """Disables deprecation messages temporarily
    """
    prev_enabled = _local.enabled
    _local.enabled = False
    try:
        yield
    finally:
        _local.enabled = prev_enabled


def warn_deprecation(message, frame_correction=0):
    if _local.enabled:
        warnings.warn(message, DeprecationWarning, stacklevel=2+frame_correction)


class _DeprecatedFunction(object):

    def __init__(self, func, message, obj=None, objtype=None, since=None, what=None, frame_correction=None):
        super(_DeprecatedFunction, self).__init__()
        self._func = func
        self._message = message
        self._obj = obj
        self._objtype = objtype
        self._frame_correction = 0 if frame_correction is None else frame_correction
        self._what = what
        self._since = since

    def _get_underlying_func(self):
        returned = self._func
        if isinstance(returned, classmethod):
            if hasattr(returned, '__func__'):
                returned = returned.__func__
            else:
                returned = returned.__get__(self._objtype).__func__
        return returned

    def __call__(self, *args, **kwargs):
        func = self._get_underlying_func()
        warning = "{0} is deprecated".format(self._get_func_str())
        if self._message is not None:
            warning += ". {0}".format(self._message)
        warn_deprecation(warning, frame_correction=self._frame_correction+1)
        if self._obj is not None:
            return func(self._obj, *args, **kwargs)
        elif self._objtype is not None:
            return func(self._objtype, *args, **kwargs)
        return func(*args, **kwargs)

    def _get_func_str(self):
        if self._what:
            return self._what
        func = self._get_underlying_func()
        if self._objtype is not None:
            return '{0}.{1}'.format(self._objtype.__name__, func.__name__)
        return '{0}.{1}'.format(func.__module__, func.__name__)

    def __get__(self, obj, objtype):
        return self.bound_to(obj, objtype)

    def bound_to(self, obj, objtype):
        return _DeprecatedFunction(self._func, self._message, obj=obj, objtype=objtype, since=self._since,
                                   what=self._what, frame_correction=self._frame_correction)

    @property
    def __name__(self):
        return self._get_underlying_func().__name__

    @property
    def __doc__(self):
        returned = self._get_underlying_func().__doc__ or ''
        returned += "\n.. deprecated"
        if self._since:
            returned += ':: {}'.format(self._since)
        returned += "\n"
        if self._message:
            returned += "   {0}".format(self._message)
        return returned

    @__doc__.setter
    def __doc__(self, doc):
        self._get_underlying_func().__doc__ = doc


def deprecated(func=None, message=None, since=None, what=None, frame_correction=None):
    """Marks the specified function as deprecated, and emits a warning when
    it's called.

    >>> @deprecated(message='No longer supported')
    ... def deprecated_func():
    ...     pass

    This will cause a warning log to be emitted when the function gets called,
    with the correct filename/lineno.

    .. versionadded:: 0.12
    """
    if isinstance(func, string_types):
        assert message is None
        message = func
        func = None

    if func is None:
        return functools.partial(
            deprecated,
            message=message, since=since, what=what,
            frame_correction=frame_correction)

    return _DeprecatedFunction(func, message, since=since, what=what, frame_correction=frame_correction)
