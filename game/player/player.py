from encodings import search_function


class Vector:
    def __init__(self, coordinates):
        self.__coordinates = list(coordinates)

    def __len__(self):
        return len(self.__coordinates)

    def __eq__(self, other):
        return self.__coordinates == other.__coordinates

    def __repr__(self):
        return str(self.__coordinates)

    def __add__(self, other):
        return Vector([i + j for i, j in zip(self.__coordinates, other.__coordinates)])

    def __mul__(self, other: int | float):
        return Vector([i*other for i in self.__coordinates])

    def __rmul__(self, other: int | float):
        return Vector([i*other for i in self.__coordinates])

    def __iter__(self):
        return iter(self.__coordinates)

    @property
    def length(self):
        return sum(i**2 for i in self.__coordinates) ** 0.5

    def norm(self, limit):
        length = self.length
        if length > 5:
            self.__coordinates = [x * (limit / length) for x in self.__coordinates]

    def to_list(self):
        return self.__coordinates


