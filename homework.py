from dataclasses import dataclass, asdict
from typing import Any, ClassVar, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    OUTPUT_TEXT: ClassVar[str] = 'Тип тренировки: {training_type}; ' + \
                                 'Длительность: {duration:.3f} ч.; ' + \
                                 'Дистанция: {distance:.3f} км; ' + \
                                 'Ср. скорость: {speed:.3f} км/ч; ' + \
                                 'Потрачено ккал: {calories:.3f}.'

    def get_message(self) -> str:
        message = self.OUTPUT_TEXT.format(**asdict(self))
        return message


class UnknownWorkoutType(Exception):
    '''Класс для неизвестной тренировки'''
    print(Exception)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MINUTES_IN_HOURS: ClassVar[int] = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        return InfoMessage(training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_BURN: ClassVar[int] = 18
    COEFF_CALORIE_RECREATION: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        '''Расход калорий для бега.'''
        speed = self.get_mean_speed()
        spent_calories = ((self.COEFF_CALORIE_BURN * speed
                           - self.COEFF_CALORIE_RECREATION) * self.weight
                          / self.M_IN_KM * self.duration
                          * self.MINUTES_IN_HOURS
                          )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_SPEED: ClassVar[float] = 0.035
    COEFF_DURATION: ClassVar[float] = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        '''Расход калорий для спортивной ходьбы.'''
        spent_calories = ((self.COEFF_SPEED * self.weight
                           + (self.get_mean_speed()**2 // self.height)
                           * self.COEFF_DURATION * self.weight)
                          * self.duration * self.MINUTES_IN_HOURS
                          )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    COEFF_WATER_RESIST: ClassVar[float] = 1.1
    COEFF_ACTIVITY: ClassVar[int] = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        '''Расчёт израсходованных калорий при плавании.'''
        spent_calories = ((self.get_mean_speed() + self.COEFF_WATER_RESIST)
                          * self.COEFF_ACTIVITY * self.weight
                          )
        return spent_calories

    def get_mean_speed(self) -> float:
        '''Расчёт средней скорости при плавании.'''
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration
                      )
        return mean_speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_trainig: Dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in types_of_trainig.keys():
        raise UnknownWorkoutType('Неизвестный тип тренировки')
    choose_training = types_of_trainig[workout_type](*data)
    return choose_training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
