from decimal import Decimal

class TemperatureError(Exception):
    pass

class NotSupportUnit(TemperatureError):
    pass

class Temperature:
    unit_list = {'k',
                 'f',
                 'c'}

    fk = {'k2f': lambda k: Decimal(str(k)) * Decimal('1.8')
                           - Decimal('459.67'),
          'f2k': lambda f: (Decimal(str(f)) + Decimal('459.67'))
                           / Decimal('1.8'),
          'k2c': lambda k: k - Decimal('273.15'),
          'c2k': lambda c: c + Decimal('273.15'),
          'f2c': lambda f: (Decimal(str(f)) - Decimal('32')) / Decimal('1.8'),
          'c2f': lambda c: Decimal(str(c))*Decimal('1.8') + Decimal('32')
    }

    @classmethod
    def exists_unit(cls, unit, raise_exception:bool=True)->bool:
        result:bool = unit.lower() in cls.unit_list
        if raise_exception and not result:
            raise NotSupportUnit
        return result

    @classmethod
    def convert(cls, value, source_unit:str, dest_unit:str):
        Temperature.exists_unit(unit=source_unit)
        Temperature.exists_unit(unit=dest_unit)
        return cls.fk[f'{source_unit.lower()}2{dest_unit.lower()}'](value)

    def __init__(self, value:Decimal, unit:str):
        Temperature.exists_unit(unit = unit)
        self.__value = Decimal(str(value))
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