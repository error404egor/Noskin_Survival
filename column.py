class Column:
    def __init__(self) -> None:
        self.__array = []
        self.__index_now = 0

    def append(self, object_to_append) -> None:
        self.__array.append(object_to_append)

    def up(self, n=1) -> None:
        self.__index_now += n if self.__index_now + n < len(self.__array) else 0

    def down(self, n=1) -> None:
        self.__index_now -= n if self.__index_now >= n else 0

    def get(self):
        try:
            return self.__array[self.__index_now]
        except IndexError:
            raise Exception("There are 0 objects in column.")
