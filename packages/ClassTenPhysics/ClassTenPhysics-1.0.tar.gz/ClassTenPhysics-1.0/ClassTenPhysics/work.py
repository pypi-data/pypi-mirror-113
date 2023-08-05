""" This module calculates many functions about work,energy and power and related topics about these subjects."""


def work(f='x', s='x', m='x', a='x', p='x', t='x'):
    """
    Calculate and return the value of work/transformation of energy using given values of the params

    How to Use:
        Give arguments for f and s params,
        or, give arguments for m,a and s params,
        or, give arguments for p and t params
    *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
    IT'LL BE HARD TO UNDERSTAND AND USE.'

    Parameters:
        f (int):force in Newton
        s (int):distance in meter
        m (int):mass in kg
        a (int):acceleration in m/s2
        p (int):power in Watt
        t (int):time in second


    Returns:
        int: the value of work in Joule
    """
    if (f != 'x') and (s != 'x'):
        w = f * s
        return w
    elif (m != 'x') and (a != 'x') and (s != 'x'):
        w = m * a * s
        return w
    elif (p != 'x') and (t != 'x'):
        w = p * t
        return w


def force(w, s):
    """
    Calculate and return the value of force using given values of the params

    How to Use:
        Give arguments for w and s params
    *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
    IT'LL BE HARD TO UNDERSTAND AND USE.'

    Parameters:
        s (int):distance in meter
        w (int):work in Joule

    Returns:
        int: the value of force in Newton
        """
    f = w / s
    return f


def distance(w='x', f='x', m='x', a='x'):
    """
    Calculate and return the value of distance using given values of the params

    How to Use:
        Give arguments for f and w params,
        or, give arguments for w,m and a params,
    *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
    IT'LL BE HARD TO UNDERSTAND AND USE.'

    Parameters:
        w (int):work/transformation of energy
        f (int):force in Newton
        m (int):mass in kg
        a (int):acceleration in m/s2


    Returns:
         int: the value of distance in meter
        """
    if (w != 'x') and (m != 'x') and (a != 'x'):
        s = w / (m * a)
        return s
    elif (f != 'x') and (w != 'x'):
        s = w / f
        return s


def mass(w='x', a='x', s='x', ek='x', v='x', ep='x', h='x'):
    """
    Calculate and return the value of mass using given values of the params

    How to Use:
        Give arguments for ep and h params,
        or, give arguments for w,a and s params,
        or, give arguments for ek and v params
    *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
    IT'LL BE HARD TO UNDERSTAND AND USE.'

    Parameters:
        w (int):work in Joule
        a (int):acceleration in m/s2
        s (int):distance in meter
        ek (int):kinetic energy in Joule
        v (int):velocity in m/s
        ep (int):potential energy in Joule
        h (int):height in meter


    Returns:
        int: the value of mass in kg
        """
    if (w != 'x') and (a != 'x') and (s != 'x'):
        m = w / (a * s)
        return m
    elif (ek != 'x') and (v != 'x'):
        m = (2 * ek) / v ** 2
        return m
    elif (ep != "x") and (h != 'x'):
        g = 9.8
        m = ep / (g * h)
        return m


def n_mass(e):
    """
    Calculate and return the value of mass using given value of the energy of nuclear reaction

    How to Use:
        Give arguments for e parameter,
    *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
    IT'LL BE HARD TO UNDERSTAND AND USE.'

    Parameters:
        e (int):nuclear energy in Joule

    Returns:
        int: the value of mass in kg

    """
    c = 3 * 10 ** 8
    m = e / c ** 2
    return m


def acceleration(w, m, s):
    """
    Calculate and return the value of acceleration using given values of the params

    How to Use:
        Give arguments for w,m and s params
    *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
    IT'LL BE HARD TO UNDERSTAND AND USE.'

    Parameters:
        w (int):work/transformation of energy
        m (int):mass in kg
        s (int):distance in meter

    Returns:
        int: the value of acceleration in m/s2
    """
    a = w / (m * s)
    return a


def velocity(ek, m):
    """
    Calculate and return the value of velocity using given values of the params

    How to Use:
        Give arguments for ek and m params,
    *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
    IT'LL BE HARD TO UNDERSTAND AND USE.'

    Parameters:
        ek (int): kinetic energy in Joule
        m (int):mass in kg


    Returns:
         int: the value of velocity in m/s
    """
    import math
    v = math.sqrt((2 * ek) / m)
    return v


def kinetic_energy(m, v):
    """
        Calculate and return the value of kinetic energy using given values of the params

        How to Use:
            Give arguments for m and v params
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            m (int):distance in meter
            v (int):work in joule

        Returns:
            int: the value of kinetic energy in Joule
            """
    ek = 0.5 * m * v ** 2
    return ek


def potential_energy(m, h):
    """
        Calculate and return the value of potential energy using given values of the params

        How to Use:
            Give arguments for m and h params
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            m (int):mass in kg
            h (int):height in meter

        Returns:
            int: the value of potential energy in Joule
            """
    g = 9.8
    ep = m * g * h
    return ep


def height(ep, m):
    """
        Calculate and return the value of height using given values of the params

        How to Use:
            Give arguments for ep and m params
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            ep (int):potential energy in Joule
            m (int):mass in kg

        Returns:
            int: the value of height in meter
            """
    g = 9.8
    h = ep / (m * g)
    return h


def mev_to_joule(mev):
    """
        Convert Mega electron Volt(mev) to Joule

        How to Use:
            Give arguments for mev parameter
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            mev (int): nuclear energy in Mega electron Volt

        Returns:
            int: the value of nuclear energy in Joule
            """
    joule = mev * (10 ** 6) * (1.6 * 10 ** -19)
    return joule


def joule_to_kwh(joule):
    """
        Convert joule to kilo Watt/hour

        How to Use:
            Give arguments for joule parameter
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            joule (int):energy in Joule

        Returns:
            int: the value of energy in kilo Watt/hour

            """
    kwh = joule / (3.6 ** 10 ** -19)
    return kwh


def power(w, t):
    """
        Calculate and return the value of power using given values of the params

        How to Use:
            Give arguments for w and t params
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            w (int):work in Joule
            t (int):time in second

        Returns:
            int: the value of power in Watt
            """
    p = w / t
    return p


def time(w, p):
    """
        Calculate and return the value of time using given values of the params

        How to Use:
            Give arguments for w and p params
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            w (int):work in joule
            p (int):power in Watt

        Returns:
            int: the value of time in second
            """
    t = w / p
    return t


def hp(p):
    """
    Converts Watt to horse power(hp)
    How to Use:
        Give arguments for p parameter
    *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
    IT'LL BE HARD TO UNDERSTAND AND USE.'

    Parameters:
        p (int): power in Watt

    Returns:
        int: the value of power in hp
        """
    horse_power = p / 746
    return horse_power


def hp_to_power(horse_power):
    """
        Converts horse power(hp) to Watt
        How to Use:
            Give arguments for hp parameter
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            horse_power (int): power in horse power

        Returns:
            int: the value of power in Watt
            """
    pw = horse_power * 746
    return pw


def efficiency(ef_energy='x', gv_energy='x', ef_power='x', gv_power='x'):
    """
        Calculate and return the value of efficiency using given values of the params

        How to Use:
            Give arguments for ef_energy and gv_energy parameters
            or,give arguments for ef_power and gv_power parameters
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            ef_energy (int):efficient energy in Joule
            gv_energy (int):given energy in Joule
            ef_power (int):efficient power in Watt
            gv_power (int):given power in Joule

        Returns:
            int: the value of efficiency
            """
    if ef_energy != 'x':
        n = ef_energy / gv_energy
        return n
    elif ef_power != 'x':
        n = ef_power / gv_power
        return n


def effective_energy(n, gv_energy):
    """
            Calculate and return the value of effective energy using given values of the params

            How to Use:
                Give arguments for n and gv_energy parameters
            *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
            IT'LL BE HARD TO UNDERSTAND AND USE.'

            Parameters:
                n (int): efficiency
                gv_energy (int):given energy in Joule


            Returns:
                int: the value of effective energy in Joule
                """
    ef_energy = n * gv_energy
    return ef_energy


def given_energy(n, ef_energy):
    """
            Calculate and return the value of given energy using given values of the params

            How to Use:
                Give arguments for ef_energy and n parameters
            *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
            IT'LL BE HARD TO UNDERSTAND AND USE.'

            Parameters:
                ef_energy (int):effective energy in Joule
                n (int): efficiency

            Returns:
                int: the value of given energy in Joule
                """
    gv_energy = ef_energy / n
    return gv_energy


def effective_power(n, gv_power):
    """
            Calculate and return the value of effective power using given values of the params

            How to Use:
                Give arguments for efficiency and gv_power parameters
            *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
            IT'LL BE HARD TO UNDERSTAND AND USE.'

            Parameters:
                gv_power (int):given power in Watt
                n (int):efficiency

            Returns:
                int: the value of effective power in Watt
                """
    ef_power = n * gv_power
    return ef_power


def given_power(n, ef_power):
    """
    Calculate and return the value of given power using given values of the params

    How to Use:
        Give arguments for efficiency and ef_power parameters
    *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
    IT'LL BE HARD TO UNDERSTAND AND USE.'

    Parameters:
        ef_power (int):effective power in Watt
        n (int):efficiency

    Returns:
        int: the value of given power in Watt
        """
    gv_power = ef_power / n
    return gv_power


def energy_loss(ef_energy='x', gv_energy='x', n='x'):
    """
    Calculate and return the value of energy loss using given values of the params

    How to Use:
        Give arguments for ef_energy and gv_energy parameters
        or,give arguments for efficiency and gv_energy parameters
    *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
    IT'LL BE HARD TO UNDERSTAND AND USE.'

    Parameters:
        ef_energy (int): effective energy in Joule
        gv_energy (int): given energy in Joule
        n (int): efficiency

    Returns:
        int: the value of energy loss in Joule
        """
    if n == 'x':
        en_loss = ef_energy - gv_energy
        return en_loss
    elif n != 'x':
        en_loss = (1 - n) * gv_energy
        return en_loss


def power_loss(ef_power='x', gv_power='x', n='x'):
    """
        Calculate and return the value of power loss using given values of the params

        How to Use:
            Give arguments for ef_power and gv_power parameters
            or,give arguments for efficiency and gv_power parameters
        *USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE.'

        Parameters:
            ef_power (int): effective power in Watt
            gv_power (int): given power in Watt
            n (int): efficiency

        Returns:
            int: the value of power loss in Watt
            """
    if n == 'x':
        pw_loss = ef_power - gv_power
        return pw_loss
    elif n != 'x':
        pw_loss = (1 - n) * gv_power
        return pw_loss
