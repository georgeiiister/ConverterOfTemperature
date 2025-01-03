from decimal import Decimal as Dec

class TemperatureError(Exception):
    pass

class NotSupportUnit(TemperatureError):
    pass

class Temperature:
    units = {'k', 'f', 'c'}

    func_key = {
                  'k2f': lambda k: Dec(str(k)) * Dec('1.8')- Dec('459.67'),
                  'f2k': lambda f: (Dec(str(f)) + Dec('459.67')) / Dec('1.8'),
                  'k2c': lambda k: k - Dec('273.15'),
                  'c2k': lambda c: c + Dec('273.15'),
                  'f2c': lambda f: (Dec(str(f)) - Dec('32')) / Dec('1.8'),
                  'c2f': lambda c: Dec(str(c)) * Dec('1.8') + Dec('32')
               }

    @classmethod
    def exists_unit(cls, *unit, raise_exception:bool=True)->bool:
        result: bool = True
        for i in unit:
             if i.lower() not in cls.units:
                result = False
                break
        if raise_exception and not result:
            raise NotSupportUnit
        return result

    @classmethod
    def convert(cls, value, source_unit:str, dest_unit:str):
        Temperature.exists_unit(source_unit, dest_unit)
        func_key = f'{source_unit.lower()}2{dest_unit.lower()}'
        return cls.func_key[func_key](value) #search function converting and run

    def __init__(self, value:Dec, unit:str):
        Temperature.exists_unit(unit)
        self.__value = Dec(str(value))
        self.__unit = unit.lower()

    @property
    def value(self):
        return self.__value

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, unit:str)->None:
        if self.__unit.lower()!=unit.lower():
            self.__value = Temperature.convert(
                                                value = self.__value,
                                                source_unit = self.__unit,
                                                dest_unit = unit
                                               )
            self.__unit = unit.lower()

    def __str__(self):
        return f'temperature={self.__value} unit={self.__unit}'