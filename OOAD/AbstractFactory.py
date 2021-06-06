from OOAD.GuiControllerDevelopment import GuiControllerDevelopment
from OOAD.GuiControllerProduction import GuiControllerProduction

class AbstractFactory:
    
    def development_mode(self):
        development_instance = GuiControllerDevelopment()
        return development_instance

    def production_mode(self):
        production_instance = GuiControllerProduction()
        return production_instance

    def start(self):
        pass



   