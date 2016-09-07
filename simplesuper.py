#!/usr/bin/env python
# encoding: utf-8

__all__ = ['SuperProxy']

import inspect
import re
import sys
import traceback

try:
    reversed
except NameError:
    def reversed(an_iterable):
        copied_iterable = list(an_iterable)
        copied_iterable.reverse()
        return copied_iterable


class SmartMethodCall(object):
    def __init__(self, method, *vargs, **kwargs):
        self._method = method
        self._vargs, self._kwargs = self._arguments_for_call(vargs, kwargs)
    
    # --- find correct arguments -----------------------------------------------
    def call_with_correct_parameters(self):
        return self._method(*self._vargs, **self._kwargs)
    
    def _arguments_for_call(self, vargs, kwargs):
        # always prefer explicit arguments
        if self._did_specify_arguments_explicitely(vargs, kwargs):
            return (vargs, kwargs)
        return self._arguments_for_super_method()

    def _did_specify_arguments_explicitely(self, vargs, kwargs):
        if vargs or kwargs:
            return True
        
        # yes, this is extremly ugly - however in Python 2.x there is no other
        # way to differentiate between self.super(*[], **{}) and self.super()
        caller_source_lines = inspect.getframeinfo(sys._getframe(4))[3]
        caller_source_code = caller_source_lines[0]
        match = re.search('self.super\((.*?)\)', caller_source_code)
        assert match is not None, repr(caller_source_code)
        if re.search('\S', match.group(1)):
            return True
        return False

    def _arguments_for_super_method(self):
        if not inspect.isroutine(self._method):
            # special treatment of object's __init__
            return ([], {})
        (args, varargs, varkw, defaults) = inspect.getargspec(self._method)
        if len(args) == 1 and varargs is None:  # just self
            return ([], {})
        return self._find_arguments_for_called_method()

    def _find_arguments_for_called_method(self):
        caller_frame = sys._getframe(3 + 2)
        caller_arg_names, caller_varg_name, caller_kwarg_name, caller_arg_values = inspect.getargvalues(caller_frame)
        (callee_arg_names, callee_varargs, callee_kwarg_name, callee_defaults) = inspect.getargspec(self._method)
        
        vargs = []
        kwargs = {}
        
        if len(caller_arg_names) > len(callee_arg_names):
            for name in caller_arg_names[len(callee_arg_names):]:
                kwargs[name] = caller_arg_values[name]
        # [1:..] because we don't need self
        for name in caller_arg_names[1:len(callee_arg_names)]:
            vargs.append(caller_arg_values[name])
        
        if caller_varg_name:
            vargs.extend(caller_arg_values[caller_varg_name])
        if caller_kwarg_name:
            kwargs.update(caller_arg_values[caller_kwarg_name])
        
        return vargs, kwargs
    

class SuperFinder(object):

    # --- find correct super method --------------------------------------------
    def super_method(self, method_name=None):
        caller_self = self._find_caller_self()
        code = sys._getframe(2).f_code
        if method_name is None:
            method_name = code.co_name
        super_class = self._find_class(caller_self, code)
        return getattr(super(super_class, caller_self), method_name)

    def _find_caller_self(self):
        arg_names, varg_name, kwarg_name, arg_values = inspect.getargvalues(sys._getframe(3))
        return arg_values[arg_names[0]]
    
    def _points_to_this_function(self, code, func):
        is_python2x = (2 == sys.version_info[0])
        if is_python2x:
            return self._points_to_this_function_py2x(code, func)
        return self._points_to_this_function_py3k(code, func)
    
    def _points_to_this_function_py2x(self, code, func):
        # Objects special methods like __init__ are c-stuff that is only
        # available to python as <slot_wrapper> which don't have im_func
        # members, so I can't get the code object to find the actual
        # implementation.
        # However this is not neccessary, as I only want to find methods defined
        # in python (the caller) so I  can just skip all <slot_wrappers>
        if hasattr(func, 'im_func'):
            other_code = func.im_func.func_code
            if id(code) == id(other_code):
                return True
        return False
    
    def _points_to_this_function_py3k(self, code, func):
        other_code = inspect.getmembers(func)[4][1]
        return id(code) == id(other_code)

    # We cannot just use self.__class__, because we need the class where the
    # method is defined, not where it is called on.
    def _find_class(self, instance, code):
        method_name = code.co_name
        for klass in reversed(inspect.getmro(instance.__class__)):
            if hasattr(klass, method_name):
                func = getattr(klass, method_name)
                if self._points_to_this_function(code, func):
                    return klass


class SuperProxy(object):
    "This has as few methods as possible, to serve as an ideal proxy."
    
    def __call__(self, *vargs, **kwargs):
        method = SuperFinder().super_method()
        call = SmartMethodCall(method, *vargs, **kwargs)
        return call.call_with_correct_parameters()
    
    def __getattr__(self, method_name):
        return SuperFinder().super_method(method_name=method_name)


# ------------------------------------------------------------------------------
# test cases

import unittest

class Super(object):
    super = SuperProxy()
    def __init__(self):
        self.did_call_super = False
    
    def method(self, *vargs, **kwargs):
        self.did_call_super = True
        return self
    
    def verify(self):
        assert self.did_call_super



class SuperTests(unittest.TestCase):
    
    def test_no_arguments(self):
        class Upper(Super):
            def method(self):
                return self.super()
        class Lower(Upper):
            def method(self):
                return self.super()
        
        Lower().method().verify()
    
    def test_positional_argument(self):
        class Upper(Super):
            def method(self, arg, *vargs):
                assert 'fnord' == arg
                assert (23, 42) == vargs
                return self.super()
        class Lower(Upper):
            def method(self, arg, *vargs):
                self.super(arg, *vargs)
                return self.super()
        
        Lower().method('fnord', 23, 42).verify()
    
    def test_test_keyword_argument(self):
        class Upper(Super):
            def method(self, arg1, arg2, **kwargs):
                assert 'fnord' == arg1
                assert 23 == arg2
                assert {'foo': 'bar'}
                return self.super()
        class Lower(Upper):
            def method(self, arg1, arg2, **kwargs):
                self.super(arg1=arg1, arg2=arg2, **kwargs)
                return self.super()
        
        Lower().method(arg1='fnord', arg2=23, foo='bar').verify()
    
    def test_positional_variable_and_keyword_arguments(self):
        class Upper(Super):
            def method(self, arg, *vargs, **kwargs):
                assert 'fnord' == arg
                assert (23, 42) == vargs
                assert {'foo': 'bar'} == kwargs
                return self.super()
        class Lower(Upper):
            def method(self, arg, *vargs, **kwargs):
                self.super(arg, *vargs, **kwargs)
                return self.super()
        
        Lower().method('fnord', 23, 42, foo='bar').verify()
    
    def test_default_arguments(self):
        class Upper(Super):
            def method(self, arg):
                assert 'fnord' == arg
                return self.super()
        class Lower(Upper):
            def method(self, arg='fnord'):
                self.super(arg)
                return self.super()
        
        Lower().method().verify()
    
    def test_can_change_arguments_to_super(self):
        class Upper(Super):
            def method(self, arg):
                assert 'fnord' == arg
                return self.super()
        class Lower(Upper):
            def method(self, arg):
                return self.super('fnord')
        
        Lower().method('foobar').verify()
    
    def test_super_has_fewer_arguments(self):
        class Upper(Super):
            def method(self, arg):
                assert 23 == arg
                return self.super()
        class Lower(Upper):
            def method(self, arg1, arg2):
                return self.super(arg1)
        
        Lower().method(23, 42).verify()
    
    def test_can_call_arbitrary_method_on_super(self):
        class Upper(Super):
            def foo(self):
                return self.super.method()
        class Lower(Upper):
            def bar(self):
                return self.super.foo()
        
        Lower().bar().verify()
    
    def test_can_use_super_in_init(self):
        # Objects special method like __init__ are special and can't be accessed like
        # normal methods. This test verifies that these methods can still be called.
        class Upper(object):
            super = SuperProxy()
            def __init__(self):
                self.super()
                self.did_call_super = True
        class Lower(Upper):
            def __init__(self):
                return self.super()
        
        self.assertEqual(True, Lower().did_call_super)
    
    def test_do_not_pass_arguments_by_default_if_lower_doesnt_have_any(self):
        # In order to have a nice API using self.super(), we need to be smart
        # so we can can detect the case where no arguments should be passed
        # as opposed to the case where all original arguments should be passed.
        class Upper(Super):
            def foo(self):
                return self.super.method()
        class Lower(Upper):
            def foo(self, default=None, *args, **kwargs):
                return self.super()
        
        Lower().foo().verify()
    
    def test_use_correct_default_arguments_for_super_method(self):
        class Upper(Super):
            def foo(self, important_key='fnord', *args, **kwargs):
                assert important_key == 'fnord', repr(important_key)
                return self.super.method()
        class Lower(Upper):
            def foo(self, some_paramter=None, *args, **kwargs):
                # Actually self.super.foo(*args, **kwargs) would work but it's
                # too easy to use the statement below so we have to support it.
                return self.super(*args, **kwargs)
        
        Lower().foo().verify()
    
    def test_add_arguments_to_kwargs_if_upper_has_less_named_arguments_than_lower(self):
        class Upper(Super):
            def foo(self, some_parameter, **kwargs):
                assert 'another_parameter' in kwargs
                assert kwargs['another_parameter'] == 'fnord'
                return self.super.method()
        class Lower(Upper):
            def foo(self, some_parameter, another_parameter='fnord', **kwargs):
                return self.super()
        Lower().foo(None).verify()
    
    def test_call_wrapped_super_method(self):
        pass  # TODO, FIXME


if __name__ == '__main__':
    unittest.main()

