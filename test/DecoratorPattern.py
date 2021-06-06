from abc import ABC, abstractmethod


class Ironman(ABC):

    @abstractmethod
    def attach(self):
        pass


class TonyStark(Ironman):
    def attach(self):
        print('In ironman : TonyStark')


class IronmanDecorator(Ironman):

    def __init__(self, person):
        self.person = person

    def attach(self):
        self.person.attach()


class Armor(IronmanDecorator):
    def __init__(self,person):
        super().__init__(person)

    def attach(self):
        self.person.attach()
        self.__setup_armor(self.person)

    def __setup_armor(self,person):
        print('Armor installed')

class Wing(IronmanDecorator):
    def __init__(self,person):
        super().__init__(person)

    def attach(self):
        self.person.attach()
        self.__setup_wing(self.person)

    def __setup_wing(self,person):
        print('Wing installed')

if __name__ == '__main__':
    ironman = TonyStark()
    ironman = Armor(ironman)
    ironman.attach()
