from random import randint

noDirection = 0

        # Повторение перемешиваний
for i in range(100):
            # Задаём заведомо истинную комбинацию для while
    direction = noDirection

            # Получаем число ТОЧНО не повторяющее предыдущее
    while (direction == noDirection):
        direction = randint(0, 3)
    print(direction)      
