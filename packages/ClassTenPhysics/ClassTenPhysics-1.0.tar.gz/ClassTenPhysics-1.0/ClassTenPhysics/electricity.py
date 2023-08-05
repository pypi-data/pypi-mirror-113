""" This module calculates many functions about electricity and related topics about the subject."""
def electricity(q='x', t='x', v='x', r='x', pw='x'):
    """
    Calculate and return the value of electricity using given values of the params

    How to Use:
        Give arguments for q and t params,
        or, give arguments for v and r params,
        or, give arguments for pw and r params
    *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
    IT'LL BE HARD TO UNDERSTAND AND USE.'

    Parameters:
        q (int):charge in Coulomb
        t (int):time in second
        v (int):potential difference in volt
        r (int):resistance in ohm
        pw (int):power in Watt


    Returns:
        int: the value of electricity as Ammeter
    """

    if (q != 'x') and (t != 'x'):
        i = q / t
        return i
    elif (v != 'x') and (r != "x"):
        i = v / r
        return i
    elif (pw != 'x') and (r != 'x'):
        import math
        i = math.sqrt(pw / r)
        return i


def potential_difference(i='x', q='x', t='x', r='x', pw='x',w='x'):
    """
    Calculate and return the value of potential difference using given values of the params

    How to Use:
        Give arguments for i and r params,
        or, give arguments for w and q params,
        or, give arguments for pw,q and t params
        or, give arguments for pw and r params
    *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
    IT'LL BE HARD TO UNDERSTAND AND USE.'

    Parameters:
        i (int): electricity in Ammeter
        q (int):charge in Coulomb
        t (int):time in second
        r (int):resistance in ohm
        pw (int):power in Watt
        w (int): work in Joule


    Returns:
        int: the value of potential difference as Volt
    """

    if (i != 'x') and (r != "x"):
        v = i * r
        return v
    elif (w != 'x') and (q != 'x'):
        v = w / q
        return v
    elif (pw != 'x') and (q != 'x') and (t != 'x'):
        v = (pw * t) / q
        return v
    elif (pw != 'x') and (r != "x"):
        import math
        v = math.sqrt(pw * r)
        return v


def resistance(v='x', i='x', p='x', l='x', a='x', pw='x'):
    """
    Calculate and return the value of resistance using given values of the params

    How to Use:
        Give arguments for v and i params,
        or, give arguments for p,l and a params,
        or, give arguments for pw and i params
        or, give arguments for pw and v params
    *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
    IT'LL BE HARD TO UNDERSTAND AND USE.'

    Parameters:
        v (int);potential difference in Volt
        i (int) electricity in Ammeter
        p (int):relative resistance in ohm m
        l (int):length of conductor
        a (int):area of cross section
        pw (int):power in Watt

    Returns:
        int: the value of resistance in ohm
    """

    if (v != 'x') and (i != 'x'):
        r = v / i
        return r
    elif (p != 'x') and (l != 'x') and (a != 'x'):
        r = p * (l / a)
        return r
    elif (pw != 'x') and (i != 'x'):
        r = pw / (i ** 2)
        return r
    elif (pw != 'x') and (v != "x"):
        r = v ** 2 / pw
        return r


def relative_resistance(l='x', a='x', r='x', c='x'):
    """
     Calculate and return the value of relative resistance using given values of the params

     How to Use:
         Give arguments for c parameter,
         or, give arguments for r,l and a params,
     *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
     IT'LL BE HARD TO UNDERSTAND AND USE.'

     Parameters:
         c (int):conductivity in 1/(ohm m)
         r (int):resistance in ohm
         l (int):length of conductor
         a (int):area of cross section


     Returns:
         int: the value of relative resistance in ohm m
     """

    if c != 'x':
        p = 1 / c
        return p
    else:
        p = r * (a / l)
        return p


def conductivity(p):
    """
     Calculate and return the value of relative conductivity using given values of the params

     How to Use:
         Give arguments for p parameter
     *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
     IT'LL BE HARD TO UNDERSTAND AND USE.'

     Parameters:
         p (int):relative resistance in ohm m

     Returns:
         int: the value of relative conductivity in 1/(ohm m)
     """

    c = 1 / p
    return c


def emf(w, q):
    """
     Calculate and return the value of electromotive force using given values of the params

     How to Use:
         Give arguments for w and q params,
     *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
     IT'LL BE HARD TO UNDERSTAND AND USE.'

     Parameters:
         q (int):charge in Coulomb
         w (int): work in Joule

     Returns:
         int: the value of electromotive force as Volt
     """

    e = w / q
    return e


def electric_work(v='x', q='x', pw='x', t='x'):
    """
     Calculate and return the value of electric work using given values of the params

     How to Use:
         Give arguments for v and q params,
         or, give arguments for pw and t params
     *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
     IT'LL BE HARD TO UNDERSTAND AND USE.'

     Parameters:
         v (int):potential difference in Volt
         q (int):charge in Coulomb
         t (int):time in second
         pw (int):power in Watt


     Returns:
         int: the value of electric work as Joule
     """

    if (v != 'x') and (q != 'x'):
        w = v * q
        return w
    elif (pw != 'x') and (t != 'x'):
        w = p * t
        return w


def electric_power(w='x', t='x', v='x', q='x', i='x', r='x'):
    """
     Calculate and return the value of electric power using given values of the params

     How to Use:
         Give arguments for v and i params,
         or, give arguments for w and t params,
         or, give arguments for v,q and t params
         or, give arguments for i and r params
         or, give arguments for v and r params
     *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
     IT'LL BE HARD TO UNDERSTAND AND USE.'

     Parameters:
         i (int): electricity in Ammeter
         q (int):charge in Coulomb
         t (int):time in second
         r (int):resistance in ohm
         v (int):potential difference in Volt
         w (int): work in Joule


     Returns:
         int: the value of electric power as Watt
     """

    if (w != 'x') and (t != 'x'):
        pw = w / t
        return pw
    elif (v != 'x') and (q != 'x') and (t != 'x'):
        pw = (v * q) / t
        return pw
    elif (v != 'x') and (i != 'x'):
        pw = v * i
        return pw
    elif (i != 'x') and (r != "x"):
        pw = (i ** 2) * r
        return pw
    elif (v != 'x') and (r != "x"):
        pw = v ** 2 / r
        return pw


def equivalent_resistance_in_series(*resistances):
    """
     Calculate and return the value of equivalent resistance in series using given values of the resistances

     How to Use:
         Give a list of resistance which are placed in series,

     Parameters:
         resistances (list): resistances in series

     Returns:
         int: the value of equivalent resistance in series as Ohm
     """

    er = 0
    for r in resistances:
        er += r
    return er


def equivalent_resistance_in_parallel(*resistances):
    """
     Calculate and return the value of equivalent resistance in parallel using given values of the resistances

     How to Use:
         Give a list of resistance which are placed in parallel,

     Parameters:
         resistances (list): resistances in parallel

     Returns:
         int: the value of equivalent resistance in parallel as Ohm
     """

    pr = 0
    for r in resistances:
        pr += 1 / r
    er = 1 / pr
    return er


def unit(p, th):
    """
     Calculate and return the value of unit using given values of the parameters

     How to Use:
         Give arguments for p and th parameters
     *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
     IT'LL BE HARD TO UNDERSTAND AND USE

     Parameters:
         p (int):power in Watt
         t (int): time in hour
     *TIME SHOULD GIVE IN HOUR, OTHERWISE
     IT'LL BE MISCALCULATE THE FUNCTION

     Returns:
         int: the value of unit as unit
     """

    u = (p * th) / 1000
    return u
