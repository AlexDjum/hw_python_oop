from statistics import mean
from turtle import distance, speed




class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    

    def get_message(self) -> str:
        print(f'Тип тренировки: {self.training_type};'
        f'Длительность: {round(self.duration, 3)} ч.;'
        f'Дистанция: {round(self.distance, 3)} км.;'
        f'Ср. скорость: {round(self.speed, 3)} км/ч;'
        f'Потрачено ккал: {round(self.calories, 3)}'
        )
    

LEN_STEP = [0.65, 1.38]
M_IN_KM = 1000

class Training:
    """Базовый класс тренировки."""
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        # Дописать выбор длины шага в зависимости от тренировки
        distance = self.action * LEN_STEP / M_IN_KM
        return distance
        

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        # Доработать
        return print(f'Тренировка закончена')


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20
    LEN_STEP = LEN_STEP[0]

    def get_spent_calories(self) -> float:
        '''Расход калорий для бега.'''
        spent_calories = ((self.COEFF_CALORIE_1 * Training.get_mean_speed()
         - self.COEFF_CALORIE_2) * self.weight / M_IN_KM * self.duration
         )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_3 = 0.035,
    COEFF_CALORIE_4 = 0.029
    LEN_STEP = LEN_STEP[0]
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        '''Расход калорий для спортивной ходьбы.'''
        spent_calories = ((self.COEFF_CALORIE_3 * self.weight + 
        (Training.get_mean_speed()**2 // self.height) * 
        self.COEFF_CALORIE_4 * self.weight) * self.duration
        )
        return spent_calories


class Swimming(Training):
    COEFF_CALORIE_5 = 1.1
    COEFF_CALORIE_6 = 2
    LEN_STEP = LEN_STEP[1]
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        '''Расчёт израсходованных калорий при плавании.'''
        spent_calories = ((Swimming.get_mean_speed + self.COEFF_CALORIE_5) 
        * self.COEFF_CALORIE_6 * self.weight
        )
        return spent_calories
    
    def get_mean_speed(self) -> float:
        '''Расчёт средней скорости при плавании.'''
        mean_speed = (self.length_pool * self.count_pool 
        / M_IN_KM / self.duration
        )
        return mean_speed

    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training = {'SWM': Swimming, 
    'RUN': Running, 
    'WLK': SportsWalking
    }
    choose_training = dict_training[workout_type](*data)
    return choose_training
    


def main(training: Training) -> None:
    """Главная функция."""

    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
        

