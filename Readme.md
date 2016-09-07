# SimpleSuper [![Build Status](https://travis-ci.org/dwt/simplesuper.svg?branch=master)](https://travis-ci.org/dwt/simplesuper)

License: ISC - See LICENSE.txt file

This is a simple piece of code born out of our frustration with the 
repetitiveness of calling overridden methods in python.
having to write

    super(TheCurrentClassThatImIn, self).the_method_that_im_currently_in(all, the, arguments, again)

every time you want to do that is just not DRY and makes refactoring
that much more tedious.

Wouldn't it be much cooler if you could just write self.super() instead? 
Yeah, we thought so, too.

In the class where you want to use this (or any superclass),
you need to make the SuperProxy available like this:

    class SuperClass(object):
        super = SuperProxy()

Afterwards you can just use it in three forms in any method:
  - Auto-pick-up all available arguments and call the super method of the current method
    
    self.super()
    
  - Call super method of current method but with explicit arguments
    
    self.super(some_arguments)
    
  - Get a proxy for the superclass and call a specific method with specific arguments
    
    self.super.whatever_method(whatever, arguments)
    
    (self.super is the same as super(CurrentClass, self) but more DRY)

## Known Bugs:

  - Works only for object subclasses (new style classes)
  - Doesn't find super-methods of decorated methods as the code 
    of the current method can't be found in the class object under 
    the name of the method.

## TODO:

  - Find a way so you can do something like from simple_super import 
    use_in_object to get every object enhanced by its niceness.

## Changelog:

1.0.5 and 1.0.6, 1.0.7, 1.0.8, 1.0.9 (2016-09-07)

  - package for pypi to have an easy dependency
  - small cleanups to make it easier to step over this code in the debugger

1.0.4 (2010-06-06)

  - Add heuristic to move arguments to kwargs if lower method has more named
    arguments than the upper method

1.0.3 (2010-05-31)

  - Added compatibility for Python 3
  - Moved stand-alone functions into nice classes

1.0.2 (2010-03-27)

  - Simplistic heuristic detection if self.super() or 
    self.super(*args, **kwargs) was called so we can pass the right parameters
  - Made simple_super compatible with Python 2.3 and old-style classes

1.0.1

  - do not add arguments if subclass uses self.super() and super class does 
    not get any arguments besides self.

1.0

  - initial release
