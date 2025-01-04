from decimal import Decimal as Dec


class TemperatureError(Exception):
    pass


class NotSupportUnit(TemperatureError):
    pass


class Temperature:
    __units = {'k', 'f', 'c'}

    @classmethod
    def units(cls):
        return cls.__units

    func_key = {
        'k2f': lambda k: Dec(str(k)) * Dec('1.8') - Dec('459.67'),
        'f2k': lambda f: (Dec(str(f)) + Dec('459.67')) / Dec('1.8'),
        'k2c': lambda k: Dec(k) - Dec('273.15'),
        'c2k': lambda c: Dec(c) + Dec('273.15'),
        'f2c': lambda f: (Dec(str(f)) - Dec('32')) / Dec('1.8'),
        'c2f': lambda c: Dec(str(c)) * Dec('1.8') + Dec('32')
    }

    @classmethod
    def exists_unit(cls, *unit, raise_exception: bool = True) -> bool:
        result: bool = True
        for i in unit:
            if i.lower() not in cls.__units:
                result = False
                break
        if raise_exception and not result:
            raise NotSupportUnit
        return result

    @staticmethod
    def decorator_convert(fn):
        def wrapper(*args, **kwargs):
            with open('convert.log', 'a+') as log:
                for i in args:
                    log.write(f'{i}\n')
                for i in kwargsargs:
                    log.write(f'{i}\n')
            return method_name(*args, **kwargs)

        return wrapper

    @classmethod
    def convert(cls, value, source_unit: str, dest_unit: str):
        result = None
        if source_unit.lower() != dest_unit.lower():
            Temperature.exists_unit(source_unit, dest_unit)
            func_key = f'{source_unit.lower()}2{dest_unit.lower()}'
            result = cls.func_key[func_key](value)  #search function converting and run
        else:
            result = value
        return result

    def __init__(self, value: Dec, unit: str):
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
    def unit(self, unit: str) -> None:
        if self.__unit.lower() != unit.lower():
            self.__value = Temperature.convert(
                value=self.__value,
                source_unit=self.__unit,
                dest_unit=unit
            )
            self.__unit = unit.lower()

    def __str__(self):
        return f'temperature={self.__value} unit={self.__unit}'
