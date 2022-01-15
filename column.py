class Column:
    def __init__(self) -> None:
        self.__array = []
        self.__index_now = 0

    def append(self, object_to_append) -> None:
        self.__array.append(object_to_append)

    def up(self, n=1) -> None:
        self.__index_now += n if self.__index_now + n < len(self.__array) else 0  # переход по текущему этажу на
        # n этажей вверх, если это возможно, иначе не изменение текущего этажа

    def down(self, n=1) -> None:
        self.__index_now -= n if self.__index_now >= n else 0  # переход по текущему этажу на
        # n этажей вниз, если это возможно, иначе не изменение текущего этажа

    def get(self):
        try:
            return self.__array[self.__index_now]  # возвращение всей информации текущего этажа
        except IndexError:
            raise Exception("There are 0 objects in column.")

    def __str__(self):
        return str(self.__array) + ", " + str(self.__index_now)

    def is_empty(self):
        return not bool(len(self.__array))
#  класс для создания списка этажей игры для переключения между ними(по сути обыкновенный переработанный
#  __list__ с изменениями функционала
