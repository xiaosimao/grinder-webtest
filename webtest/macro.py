# macro.py

"""This module defines macro functions that can be invoked from a webtest.
Macros provide a way of programmatically generating things like timestamps,
random strings or numbers, or other strings that cannot be hard-coded.

Macro functions are defined as methods within the `Macro` class. Any methods
defined in this module are built-in, so you can invoke them from any evaluated
expression in a ``.webtest`` file.

All macro functions are invoked using a ``lower_case`` name followed by
parentheses. If the macro accepts arguments, they are passed as a literal
string, separated by commas. For example::

    <FormPostParameter Name="INVOICE_DATE" Value="{today(%y%m%d)}"/>
    <FormPostParameter Name="DUE_DATE" Value="{today_plus(7, %y%m%d)}"/>

You can also assign the return value of a macro to a variable, for later use::

    <FormPostParameter Name="INVOICE_DATE" Value="{TODAY = today(%y%m%d)}"/>
    <FormPostParameter Name="DUE_DATE" Value="{NEXT_WEEK= today_plus(7, %y%m%d)}"/>

If you want to define your own custom macros, first create a derived class::

    from webtest.macro import Macro

    class MyMacro (Macro):
        def square(self, num):
            return str(num * num)

        def cube(self, num):
            return str(num * num * num)

Then, tell your test runner to use your macro class::

    TestRunner = get_test_runner( ... , macro_class=MyMacro)

Any ``.webtest`` files that are executed by this TestRunner will be able to call
your custom macro methods::

    <FormPostParameter Name="NUM1" Value="{square(5)}" />
    <FormPostParameter Name="NUM2" Value="{CUBE_VAR = cube(5)}" />

Macro functions each accept a string argument, and return a string. If a macro
needs to accept several arguments, they are packed into a string and separated
with commas.
"""

import random
import datetime
import time

def _sample(choices, how_many):
    """Return `how_many` randomly-chosen items from `choices`.
    """
    return [random.choice(choices) for x in range(how_many)]

class Macro:
    """Functions that can be invoked from a webtest.
    """
    def __init__(self):
        pass

    def invoke(self, macro_name, args):
        """Invoke ``macro_name``, passing ``args``, and return the result.
        """
        try:
            func = getattr(self, macro_name)
        except AttributeError:
            raise ValueError("Macro function '%s' is undefined")
        else:
            return str(func(args))

    def random_digits(self, length):
        """Generate a random string of digits of the given length.
        """
        return ''.join(_sample('0123456789', int(length)))

    def random_letters(self, length):
        """Generate a random string of letters of the given length.
        """
        return ''.join(_sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', int(length)))

    def random_alphanumeric(self, length):
        """Generate a random alphanumeric string of the given length.
        """
        return ''.join(_sample('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', int(length)))

    def today(self, format):
        """Return today's date in the given format. For example, ``%m%d%y`` for
        ``MMDDYY`` format. See the datetime_ module documentation for allowed
        format strings.

        .. _datetime: http://docs.python.org/library/datetime.html
        """
        return datetime.date.today().strftime(format)

    def today_plus(self, days_and_format):
        """Return today plus some number of days, in the given format.
        """
        days, format = [arg.strip() for arg in days_and_format.split(',')]
        return (datetime.date.today() + datetime.timedelta(int(days))).strftime(format)

    def timestamp(self, arg):
        """Return a timestamp (number of seconds since the epoch).
        """
        return str(int(time.time()))


