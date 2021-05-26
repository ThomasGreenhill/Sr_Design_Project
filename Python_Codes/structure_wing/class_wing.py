"""
Includes the classes used in wing modeling and load calculations


Note:
      ****Unfinished****

History:
    05.25.2021, Created, XT.
"""

import types


class Load:

    def __init__(self, load_arr):
        if type(load_arr) is not list and type(load_arr) is not tuple:
            self.load_arr = [load_arr]
        else:
            self.load_arr = load_arr

        self.check_load_types()

    def check_load_types(self):

        total_load_classes = ["PointLoad", "UniformLoad", "DistributedLoad"]

        for element in self.load_arr:
            if not (type(element).__name__ in total_load_classes):
                raise Exception("One or more of the load elements are not identified in class_wing.py\n")


class PointLoad:

    def __init__(self, magnitude, location):
        self.magnitude = magnitude
        self.location = location


class UniformLoad:

    def __init__(self, magnitude, start_location, end_location):
        self.magnitude = magnitude
        self.start = start_location
        self.end = end_location


class DistributedLoad:

    def __int__(self, magnitude_func, start_location, end_location):
        self.start = start_location
        self.end = end_location
        if isinstance(magnitude_func, types.FunctionType):
            self.magnitude_func = magnitude_func
        else:
            raise Exception("Error: first input has to be a load function for a given location\n")

    def get_load_at(self, target_location):
        if target_location < self.start or target_location > self.end:
            raise Exception("Error: specified location has to be within {:.2f} and {:.2f} m\n".format(self.start,
                                                                                                      self.end))

        return self.magnitude_func(target_location)


if __name__ == '__main__':
    a = PointLoad(23, 1)
    b = type(a).__name__
    print(type(b))

    c = [1, 2, 3]
    d = 4
    print(d in c)
