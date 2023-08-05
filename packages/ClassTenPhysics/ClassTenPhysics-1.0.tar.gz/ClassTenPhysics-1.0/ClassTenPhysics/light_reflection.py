""" This module calculates many functions about light reflection and related topics about the subject."""


class PlaneMirror:
    """Calculate functions about plane mirror and also has an attribute about description of its image"""

    def __init__(self, u='x', v='x', l='x', li='x'):
        """Calculates various attributes of plane mirror using given params

        How to use:
        Give arguments for the parameters to get the value of necessary attribute
        for example: to get length of image,
        give argument for l parameter
        *GIVE NECESSARY ARGUMENTS TO GET CERTAIN ATTRIBUTES, OTHERWISE
        IT'LL RAISE AN ERROR
        USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE

        parameters:
        u (int):distance of object from mirror
        v (int):distance of image from mirror
        l (int):length of object
        li (int):length of image


        Get attribute:
        *AFTER MAKING AN OBJECT AS AN INSTANCE OF THE CLASS, GIVE KEYWORD ARGUMENTS ON THE BRACKET OF THE CLASS
        THEN TYPE THE OBJECT NAME THEN PRESS '.' THEN SELECT THE NECESSARY ATTRIBUTE AND PRINT THAT
        MAGNIFICATION ATTRIBUTE ARE ALWAYS 1 AND FOCUS IS ALWAYS INFINITE, SO IT DOESN'T NEED TO GIVE ANY ARGUMENT TO GET THAT

        Get description of image:
        *AFTER MAKING AN OBJECT AS AN INSTANCE OF THE CLASS, THEN TYPE THE OBJECT NAME AND THEN PRESS '.' THEN SIMPLY TYPE
        description of image AND THEN PRINT THAT. TO GET SPECIFIC DESCRIPTION, AFTER TYPING description of image PUT [] AND
        INSIDE OF IT PUT '' AND INSIDE IT WRITE THE SPECIFIC ATTRIBUTE(position/size/state/presence) AND PRINT THAT
        """

        if u != 'x':
            self.distance_of_image = -u
        elif v != 'x':
            self.distance_of_object = -v
        elif l != 'x':
            self.length_of_image = l
        elif li != 'x':
            self.length_of_object = li
        self.magnification = 1
        self.focus = "infinite"

    description_of_image = {"position": "on the opposite side of the mirror "
                                        "but same distance as the object's distance from mirror.",
                            "size": "same size as object",
                            "state": "straight",
                            "presence": "unreal"
                            }


class ConvexMirror:
    """Calculate functions about convex mirror and also has an attribute about description of its image"""
    def __init__(self, u='x', v='x', l='x', li='x', f='x', m='x', r='x'):
        """Calculates various attributes of convex mirror using given params

        How to use:
        Give arguments for the parameters to get the value of necessary attribute
        for example: to get focus attribute,
        give arguments for r parameter
        or, give arguments for u and v parameters
        *GIVE NECESSARY ARGUMENTS TO GET CERTAIN ATTRIBUTES, OTHERWISE
        IT'LL RAISE AN ERROR
        USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE

        parameters:
        u (int):distance of object from mirror
        v (int):distance of image from mirror
        f (int):focus distance
        l (int):length of object
        li (int):length of image
        m (int):magnification
        r (int):radius/ double focus distance

        Get attribute:
        *AFTER MAKING AN OBJECT AS AN INSTANCE OF THE CLASS, GIVE KEYWORD ARGUMENTS ON THE BRACKET OF THE CLASS
        THEN TYPE THE OBJECT NAME THEN PRESS '.' THEN SELECT THE NECESSARY ATTRIBUTE AND PRINT THAT

        Get description of image:
        *AFTER MAKING AN OBJECT AS AN INSTANCE OF THE CLASS, THEN TYPE THE OBJECT NAME AND THEN PRESS '.' THEN SIMPLY TYPE
        description of image AND THEN PRINT THAT. TO GET SPECIFIC DESCRIPTION, AFTER TYPING description of image PUT [] AND
        INSIDE OF IT PUT '' AND INSIDE IT WRITE THE SPECIFIC ATTRIBUTE(position/size/state/presence) AND PRINT THAT
        """

        if r != 'x':
            self.focus = r / 2
        elif (u != 'x') and (v != 'x'):
            self.focus = (u * v) / (u + v)
            self.magnification = -v / u
        elif (l != 'x') and (li != 'x'):
            self.magnification = l / li
        elif (f != 'x') and (u != 'x'):
            self.distance_of_image = (f * u) / (u - f)
        elif (f != 'x') and (v != 'x'):
            self.distance_of_object = (f * v) / (v - f)
        elif (m != 'x') and (li != 'x'):
            self.length_of_object = m * li
        elif (m != 'x') and (l != 'x'):
            self.length_of_image = l / m
        elif (m != 'x') and (u != 'x'):
            self.distance_of_image = - (m * u)
        elif (m != 'x') and (v != 'x'):
            self.distance_of_object = - (v / m)

    description_of_image = {
        "position": " on the opposite side of the mirror and more distance than the object's distance from mirror.",
        "size": "magnified",
        "state": "straight",
        "presence": "unreal"}


class ConcaveMirror:
    """Calculate functions about concave mirror"""
    def __init__(self, u='x', v='x', l='x', li='x', f='x', m='x', r='x'):
        """Calculates various attributes of concave mirror using given params

        How to use:
        Give arguments for the parameters to get the value of necessary attribute
        for example: to get focus attribute,
        give arguments for r parameter
        or, give arguments for u and v parameters
        *GIVE NECESSARY ARGUMENTS TO GET CERTAIN ATTRIBUTES, OTHERWISE
        IT'LL RAISE AN ERROR
        USE KEYWORD ARGUMENTS FOR EASY USE, OTHERWISE
        IT'LL BE HARD TO UNDERSTAND AND USE

        parameters:
        u (int):distance of object from mirror
        v (int):distance of image from mirror
        f (int):focus distance
        l (int):length of object
        li (int):length of image
        m (int):magnification
        r (int):radius/ double focus distance

        Get attribute:
        *AFTER MAKING AN OBJECT AS AN INSTANCE OF THE CLASS, GIVE KEYWORD ARGUMENTS ON THE BRACKET OF THE CLASS
        THEN TYPE THE OBJECT NAME THEN PRESS '.' THEN SELECT THE NECESSARY ATTRIBUTE AND PRINT THAT
        """
        if r != 'x':
            self.focus = r / 2
        elif (u != 'x') and (v != 'x'):
            self.focus = (u * v) / (u + v)
            self.magnification = -v / u
        elif (l != 'x') and (li != 'x'):
            self.magnification = l / li
        elif (f != 'x') and (u != 'x'):
            self.distance_of_image = (f * u) / (u - f)
        elif (f != 'x') and (v != 'x'):
            self.distance_of_object = (f * v) / (v - f)
        elif (m != 'x') and (li != 'x'):
            self.length_of_object = m * li
        elif (m != 'x') and (l != 'x'):
            self.length_of_image = l / m
        elif (m != 'x') and (u != 'x'):
            self.distance_of_image = - (m * u)
        elif (m != 'x') and (v != 'x'):
            self.distance_of_object = - (v / m)

    @staticmethod
    def image(focus, distance_of_object):
        """Calculates and returns description of image using given values of focus and distance of object

         How to use:
         Give arguments for focus and distance of object (from mirror)

         parameters:
         focus: focus distance
         distance of object: distance of object from mirror

         returns:
         dict: description of image

         Get specific description of image:
        *AFTER MAKING AN OBJECT AS AN INSTANCE OF THE CLASS PUT '.' AFTER CALLING THE CLASS THEN CALL THIS image() FUNCTION AND
        GIVE KEYWORD ARGUMENTS INSIDE THE BRACKET OF THIS image() FUNCTION. NEXT LINE TYPE THE OBJECT'S NAME THEN
         PUT [] AND INSIDE OF IT PUT '' AND INSIDE IT WRITE THE SPECIFIC ATTRIBUTE(position/size/state/presence) AND PRINT THAT
         """
        if focus > distance_of_object:
            description_of_image = {
                "position": " on the opposite side of the mirror and "
                            "more distance than the object's distance from mirror.",
                "size": "magnified",
                "state": "straight",
                "presence": "unreal"}
            return description_of_image
        elif focus == distance_of_object:
            description_of_image = {
                "position": "no position",
                "size": "no size",
                "state": "it doesn't exists!",
                "presence": "no presence"
            }
            return description_of_image
        elif focus < distance_of_object < focus * 2:
            description_of_image = {
                "position": " on the same side of the mirror and "
                            "more distance than the object's distance from mirror"
                            "(outside of the double focus distance).",
                "size": "magnified",
                "state": "reversed",
                "presence": "real"}
            return description_of_image
        elif distance_of_object == 2 * focus:
            description_of_image = {
                "position": " on the same side of the mirror and "
                            "below the object",
                "size": "same as object",
                "state": "reversed",
                "presence": "real"}
            return description_of_image
        elif distance_of_object > 2 * focus:
            description_of_image = {
                "position": " on the same side of the mirror and "
                            "less distance than the object's distance from mirror"
                            "(outside of the focus distance"
                            "but inside of the double focus distance).",
                "size": "smaller than object",
                "state": "reversed",
                "presence": "real"}
            return description_of_image
