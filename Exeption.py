class BoardExeption(Exception):
    pass

class BoarOutException(BoardExeption):
    def __str__(self):
        return 'Вы выстрелили за пределы доски'

class BoardUsedException(BoardExeption):
    def __str__(self):
        return 'Вы уже стреляли в эту клетку'

class BoardWrongShipException(BoardExeption):
    pass