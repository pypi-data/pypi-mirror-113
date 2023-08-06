import os.path
with open((os.path.join(os.path.dirname(__file__), ".version")), "r") as f:
    __version__ = f.readline().strip()

import logging
import types

from .Buffers import *
from .Patterns import *
from .TimeVar import *
from .Constants import *
from .Root import Root
from .Scale import Scale, Tuning, get_freq_and_midi

# Define any custom functions

@PatternMethod
def __getitem__(self, key):
    """ Overrides the Pattern.__getitem__ to allow indexing
        by TimeVar and PlayerKey instances. """
    if isinstance(key, TimeVar):
        # Create a TimeVar of a PGroup that can then be indexed by the key
        item = TimeVar(tuple(self.data))
        item.dependency = key
        item.evaluate = fetch(Get)
        return item
    else:
        return self.getitem(key)

def player_method(f):
    """ Decorator for assigning functions as Player methods.

    >>> @player_method
    ... def test(self):
    ...    print(self.degree)

    >>> p1.test()
    """
    setattr(Player, f.__name__, f)
    return getattr(Player, f.__name__)

PlayerMethod = player_method # Temporary alias

def _futureBarDecorator(n, multiplier=1):
    if callable(n):
        def switch(*args, **kwargs):
            Clock.now_flag = True
            output = n()
            Clock.now_flag = False
            return output
        Clock.schedule(switch, Clock.next_bar())
        return switch
    def wrapper(f):
        Clock.schedule(f, Clock.next_bar() + (n * multiplier))
        return f
    return wrapper

def next_bar(n=0):
    ''' Schedule functions when you define them with @nextBar
    Functions will run n beats into the next bar.

    >>> nextBar(v1.solo)
    or
    >>> @nextBar
    ... def dostuff():
    ...     v1.solo()
    '''
    return _futureBarDecorator(n)

nextBar = next_bar # temporary alias

def futureBar(n=0):
    ''' Schedule functions when you define them with @futureBar
    Functions will run n bars in the future (0 is the next bar)

    >>> futureBar(v1.solo)
    or
    >>> @futureBar(4)
    ... def dostuff():
    ...     v1.solo()
    '''
    return _futureBarDecorator(n, Clock.bar_length())

def Ramp(t=32, ramp_time=4):
    """ Returns a `linvar` that goes from 0 to 1 over the course of the last
        `ramp_time` bars of every `t` length cycle. """
    return linvar([0,0,1,0],[t-ramp_time, ramp_time, 0, 0])

def functions(module):
    """ Returns a list of function names defined in module """
    return [name for name, data in vars(module).items() if type(data) == types.FunctionType]

logging.basicConfig(level=logging.ERROR)

PatternMethods = Pattern.get_methods()
PatternTypes = functions(Sequences)