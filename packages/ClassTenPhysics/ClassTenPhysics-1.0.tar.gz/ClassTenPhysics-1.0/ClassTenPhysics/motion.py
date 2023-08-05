""" This module calculates many functions about motion and related topics about the subject."""


def terminal_velocity(u='x', a='x', t='x', s='x'):
    """
        Calculate and return the value of terminal velocity using given values of the params

        How to Use:
            Give arguments for any three params
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            u (int):initial velocity in m/s
            a (int):acceleration in m/s2
            t (int):time in second
            s (int):distance in meter

        Returns:
            int: the value of terminal velocity in m/s
            """
    if s == 'x':
        v = u + a * t
        return v
    elif a == 'x':
        v = ((2 * s) / t) - u
        return v
    elif t == 'x':
        import math
        v = math.sqrt(u ** 2 + (2 * a * s))
        return v
    elif u == 'x':
        u = (s / t) - (0.5 * a * t)
        v = u + a * t
        return v


def distance(u='x', v='x', a='x', t='x'):
    """
        Calculate and return the value of distance using given values of the params

        How to Use:
            Give arguments for any three params
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            u (int):initial velocity in m/s
            v (int):terminal velocity in m/s
            a (int):acceleration in m/s2
            t (int):time in second


        Returns:
            int: the value of distance in meter
            """

    if v == 'x':
        s = u * t + (0.5 * a * t ** 2)
        return s
    elif a == 'x':
        s = (u + v) * (t / 2)
        return s

    elif t == 'x':
        s = (v ** 2 - u ** 2) / 2 * a
        return s
    elif u == 'x':
        u = v - a * t
        s = u * t + (0.5 * a * t ** 2)
        return s


def acceleration(u='x', v='x', t='x', s='x'):
    """
        Calculate and return the value of acceleration using given values of the params

        How to Use:
            Give arguments for any three params
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            u (int):initial velocity in m/s
            v (int): terminal velocity in m/s
            t (int):time in second
            s (int):distance in meter

        Returns:
            int: the value of acceleration in m/s2
            """

    if s == 'x':
        a = (v - u) / t
        return a
    elif v == 'x':
        a = (2 * s / t ** 2) - (2 * u / t)
        return a
    elif t == 'x':
        a = (v ** 2 - u ** 2) / 2 * s
        return a
    elif u == 'x':
        a = (2 * v / t) - (2 * s / t ** 2)
        return a


def time(u='x', v='x', a='x', s='x'):
    """
        Calculate and return the value of time using given values of the params

        How to Use:
            Give arguments for any three params
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            u (int):initial velocity in m/s
            v (int):terminal velocity in m/s
            a (int):acceleration in m/s2
            s (int):distance in meter

        Returns:
            int: the value of time in second
            """

    if s == 'x':
        t = (v - u) / a
        return t
    elif v == 'x':
        import math
        v = math.sqrt(u ** 2 + 2 * a * s)
        t = (2 * s) / (u + v)
        return t
    elif a == 'x':
        t = (2 * s) / (u + v)
        return t
    elif u == 'x':
        import math
        u = math.sqrt(v ** 2 - 2 * a * s)
        t = (v - u) / a
        return t


def initial_velocity(v='x', a='x', t='x', s='x'):
    """
        Calculate and return the value of initial velocity using given values of the params

        How to Use:
            Give arguments for any three params
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            v (int):terminal velocity in m/s
            a (int):acceleration in m/s2
            t (int):time in second
            s (int):distance in meter

        Returns:
            int: the value of initial velocity in m/s
            """

    if s == 'x':
        u = v - a * t
        return u
    elif v == 'x':
        u = (s / t) - (0.5 * a * t)
        return u
    elif t == 'x':
        import math
        u = math.sqrt(v ** 2 - 2 * a * s)
        return u
    elif a == 'x':
        a = (2 * v / t) - (2 * s / t ** 2)
        u = v - a * t
        return u
