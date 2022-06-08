# "Общий Tkinter
from tkinter import *

# Для использования Radiobutton
from tkinter import ttk

# Для использования окон-сообщений
from tkinter import messagebox

# Рандомчик
from random import randint

# Бипер (пищалка), простейший генератор звука
from winsound import Beep

from time import sleep

# ========================== МЕТОДЫ И ФУНКЦИИ =================================

# Обновляет надписи
def refreshText():
    textSteps["text"] = f"Сделано ходов: {steps[diffCombobox.current()]}"
    textRecord["text"] = f"Рекорд ходов: {record[diffCombobox.current()]}"

# Сохранение рекордов
def saveRecords():
    global record
    try:
        f = open("steps.dat", "w", encoding="utf-8")
        for i in range(len(steps)):
            # Проверяем: чтобы побить рекорд, количества шагов
            # для каждого уровня должно быть больше ноля, но
            # меньше предыдущего рекорда
            if (steps[i] > 0 and steps[i] < record[i]):
                record[i] = steps[i]
            f.write(str(record[i]) + "\n")
        f.close()
    # В случае ошибки создания и записи
    except:
        messagebox.showinfo("Ошибка",
                            "Возникла проблема с файлом при сохранении очков")
        

# Возвращает рекорды ходов
def getRecordSteps():
    m = []
    try:
        f = open("steps.dat", "r", encoding="utf-8")
        for line in f.readlines():
            m.append(int(line))
        f.close()
    except:
        m = []

    if (len(m) != 6):
        for i in range(6):
            m.append(1000 + 1000 * i)
    return m

# Кнопка просмотра отпущена
def seeEnd(event):
    global dataImage
    Beep(1082, 25)
    for i in range(n):
        for j in range(m):
            dataImage[i][j] = copyData[i][j]

    updatePictures()
    

# Кнопка просмотра собранного нажата
def seeStart(event):
    global copyData, dataImage
    Beep(1632, 25)
    for i in range(n):
        for j in range(m):
            copyData[i][j] = dataImage[i][j]

            # Формируем собранное поле, от 0 до 15
            dataImage[i][j] = i * n + j

    # Обязательно обновляем содержимое окна
    updatePictures()

# Выбор изображения
def isCheckImage():
    global imageBackground
    # Если в переменной image содержится True...
    if (image.get()):
        # ... то ставим imageBackground01
        imageBackground = imageBackground01
        Beep(1000, 25)
    else:
        imageBackground = imageBackground02
        Beep(1300, 25)
    updatePictures()

# Обновление всех изображений
def updatePictures():
    # С помощью цикла проходим все labelImage[][] устанавливая в них
    # необходимые изображения
    for i in range(n):
        for j in range(m):
            labelImage[i][j]["image"] = \
                                      imageBackground[dataImage[i][j]]

    # Обязательно обновляем экран
    root.update()

# Сброс игрового поля
def resetPictures():
    global dataImage, steps, playGame
    steps[diffCombobox.current()] = 0
    playGame = False
    
    # Настраиваем состояние виджетов
    startButton["state"] = NORMAL
    resetButton["state"] = DISABLED
    diffCombobox["state"] = "readonly"
    radio01["state"] = NORMAL
    radio02["state"] = NORMAL

    # Заполняем dataImage[][] первоначальными значениями (последовательность от 0 до 15)
    for i in range(n):
        for j in range(m):
            dataImage[i][j] = i * n + j

    # Задаем пустое поле
    dataImage[n - 1][m - 1] = blackImg

    # Звуки
    Beep(800, 50)
    Beep(810, 35)

    # Перерисовываем экран
    updatePictures()

    # Обновить текстовые метки
    refreshText()

# Обмен изображений
def exchangeImage(x1, y1, x2, y2):
    global dataImage, labelImage
    dataImage[x1][y1], dataImage[x2][y2] = \
                       dataImage[x2][y2], dataImage[x1][y1]

    # Получаем изображение по номеру из dataImage
    # и устанавливаем его в labelImage
    labelImage[x1][y1]["image"] = imageBackground[dataImage[x1][y1]]
    labelImage[x2][y2]["image"] = imageBackground[dataImage[x2][y2]]

    # Перерисовка окна
    root.update()

    sleep(0.01)
# Перемешиваем
def shufflePictures(x, y):
    if (diffCombobox.current() < 5):
        # Количества перемещений в зависимости от уровня сложности
        count = int(((2 + diffCombobox.current()) ** 4) * 1.25)

        # Запрет направления
        noDirection = 0

        # Повторение перемешиваний
        for i in range(count):
            # Задаём заведомо истинную комбинацию для while
            direction = noDirection

            # Получаем число ТОЧНО не повторяющее предыдущее
            while (direction == noDirection):
                direction = randint(0, 3)

            # Вниз
            if (direction == 0 and x + 1 < n):
                # Обмениваем текущую и спрайт ниже
                exchangeImage(x, y, x + 1, y)

                # Увеличиваем х, т.к. пустое место переместилось в
                # новую позицию х + 1
                x += 1

                # Запрещаем направление. Следующее direction не должно
                # равняться 1, т.е обмену с верхней плиткой
                noDirection = 1

            # Вверх
            elif (direction == 1 and x - 1 >= 0):
                exchangeImage(x, y, x - 1, y)
                x -= 1
                noDirection = 0
            # Вправо
            elif (direction == 2 and y + 1 < m):
                exchangeImage(x, y, x, y + 1)
                y += 1
                noDirection = 3
            # Влево
            elif (direction == 3 and y - 1 >= 0):
                exchangeImage(x, y, x, y - 1)
                y -= 1
                noDirection = 2

    else:
        exchangeImage(n - 1, m - 3, n - 1, m - 2)
        
    Beep(1750, 50)

    resetButton["state"] = NORMAL

# СТАРТ
def startNewRound():
    global steps, playGame
    # Игра началась
    playGame = True

    # Обнуляем количество шагов для текущего уровня
    steps[diffCombobox.current()] = 0
   
    # Сбрасываем состояние кнопок и переключателей
    diffCombobox["state"] = DISABLED
    startButton["state"] = DISABLED
    radio01["state"] = DISABLED
    radio02["state"] = DISABLED

    Beep(100, 300)
    Beep(300, 300)

    # Находим пустую ячейку перебором списка dataImage[][]
    x = n - 1
    y = m - 1
    

    # Запускаем метод и перемешиваем
    shufflePictures(x, y)

    # Обновляем текстовые метки
    refreshText()
         

def go(x, y):
    global steps, playGame
    
    if (x + 1 < n and dataImage[x + 1][y] == blackImg):
        exchangeImage(x, y, x + 1, y)
    elif (x - 1 >= 0 and dataImage[x - 1][y] == blackImg):
        exchangeImage(x, y, x - 1, y)
    elif (y + 1 < m and dataImage[x][y + 1] == blackImg):
        exchangeImage(x, y, x, y + 1)
    elif (y - 1 >= 0 and dataImage[x][y - 1] == blackImg):
        exchangeImage(x, y, x, y - 1)
    else:
        Beep(500, 100)
        return 0
    Beep(1400, 5)
    # Если игра идёт и метод продолжается (т.е. не сработала строка return 0)
    # то мы добавляем +1 ход
    if (playGame):
        steps[diffCombobox.current()] += 1
        refreshText()

        # Заранее предпологаем, что пользователь выиграл
        # Задача алгоритма - доказать, что это не так.
        win = True

        # В циклах обходим весь цикл dataImage
        for i in range(n):
            for j in range(m):
                # Контролируем, если правая нижняя клетка
                # то сравниваем с blackImg
                if (i == n - 1 and j == m - 1):

                    # Если хотя бы одно из выражений - False
                    # то переменная win принимает значение False
                    win = win and dataImage[i][j] == blackImg

                    # ... иначе сравниваем с числовым рядом
                    # 0..14 включительно
                else:
                    win = win and dataImage[i][j] == i * n + j
        
        if (win):
             # Устанавливаем вместо свободного поля спрайт
             # правого нижнего угла для целостности изображения
             dataImage[n - 1][m - 1] = blackImg - 1
             # Обновляем содержимое Label
             updatePictures()

             # Выводим окно сообщение
             messagebox.showinfo("Браво!", "Вы одолели эту непосильную игру! Будте здоровы и счастливы!")

             # Проигрываем победную музыку
             music()
 
             # Сохраняем рекорды. Метод сам посчитает
             # поставил ли новый рекорд игрок
             saveRecords()
             # Игра окончена
             playGame = False
             # Обновляем текст
             refreshText()                           

def music():
    Beep(100, 100)
    Beep(200, 200)
    Beep(300, 250)

                
# ========================== НАЧАЛО ПРОГРАММЫ =================================
# Создание окна
root = Tk()
root.resizable(False, False)
root.title("Головоломка для самых умных")

# Иконка. Изготовленна на сайте https://www.favicon.by/
root.iconbitmap("icon/icon.ico")

# ЦВЕТА
black = "#373737"
fore = "#AFAFAF"

# Настройка геометрии окна
WIDTH = 422
HEIGHT = 730
POS_X = root.winfo_screenwidth() // 2 - WIDTH // 2
POS_Y = root.winfo_screenheight() // 2 - HEIGHT // 2
root.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")

# Устанавливаем фоновый цвет
root["bg"] = black

# Кнопка ПОСМОТРЕТЬ СОБРАННОЕ
seeButton = Button(root, text="Посмотреть, как должно быть", width=56)
seeButton.place(x=10, y=620)
seeButton.bind("<Button-1>", seeStart)
seeButton.bind("<ButtonRelease>", seeEnd)

# Кнопка СТАРТ
startButton = Button(text="СТАРТ", width=56)
startButton.place(x=10, y=650)
startButton["command"] = startNewRound

# Кнопка СБРОС
resetButton = Button(root, text="Сброс", width=56)
resetButton.place(x=10, y=680)
resetButton["command"] = resetPictures

# Метка лдя вывода текста с количеством
# сделанных ходов и рекордом текущего уровня
textSteps = Label(root, bg = black, fg = fore)
textSteps.place(x=10, y=550)
textRecord = Label(root, bg = black, fg = fore)
textRecord.place(x=10, y = 570)

# Метка сложности
Label(root, bg=black, fg=fore, text="Сложность:").place(x=267, y=550)

# Названия степеней сложности перемешивания
itemDiff = ["Только начал", "Немного почитал", "Знаю print()", "Понял сортировку", "Изучил лабиртинт", "Задонатил!"]

# Выпадающий список
diffCombobox = ttk.Combobox(root, width=20, values=itemDiff, state="readonly")
diffCombobox.place(x=270, y=570)

# Пока коментируем, метода refershText() у нас нет
diffCombobox.bind("<<ComboboxSelected>>", lambda e: refreshText())

# Выбираем нулевой пункт: сложность "Только начал"
diffCombobox.current(0)

# Радиопереключатели
# Создаём переменную
image = BooleanVar()
# Устанавливаем значение
image.set(True)

# Создаём радио-кнопку и привязываем к ней переменную image
radio01 = Radiobutton(root, text="Космос", variable=image, value=True, activebackground=black, bg=black, fg=fore)
radio02 = Radiobutton(root, text="Прмрода", variable=image, value=False, activebackground=black, bg=black, fg=fore)

radio01["command"] = isCheckImage
radio02["command"] = isCheckImage
radio01.place(x=150, y=548)
radio02.place(x=150, y=568)

# ============================= ИЗОБРАЖЕНИЯ ====================================

# Размер поля
n = 4
m = 4

# Размер полного изображения
pictureWidth = 400
pictureHeight = 532

# Ширина и высота одного спрайта
widthPic = pictureWidth / n
heightPic = pictureHeight / m

# Список с именами файлов
fileName = ["img01.png", "img02.png", "img03.png", "img04.png", "img05.png", \
            "img06.png", "img07.png", "img08.png", "img09.png", "img10.png", \
            "img11.png", "img12.png", "img13.png", "img14.png", "img15.png", \
            "img16.png", "black.png"]

# Списки для хранения изображений
imageBackground = [] # АКТИВНОЕ ИЗОБРАЖЕНИЕ
imageBackground01 = [] # Космос
imageBackground02 = [] # Природа

# Добавляем в списки элементы и загружаем в них обьекты PhotoImage
for name in fileName:
    imageBackground01.append(PhotoImage(file="image01/" + name))
    imageBackground02.append(PhotoImage(file="image02/" + name))

# Номер изображения "пустого поля"
blackImg = 16

imageBackground = imageBackground01


# Метки Label
labelImage = []

# Математическая модель игрового поля
dataImage = []


# Для создания копии модели игрового поля при просмотре
# по кнопке "Посмотреть как должно быть"
copyData = []

for i in range(n):
    # Начинаем заполнять списки
    labelImage.append([])
    dataImage.append([])
    copyData.append([])

    for j in range(m):
        # Формула i * n + j сгенерирует ряд чисел 0, 1, 2, 3, 4 и так далее
        # это и есть номера "собранной" версии изображения
        dataImage[i].append(i * n + j)
        copyData[i].append(i * n + j)

        # Создаём и настраиваем Label, в который
        # будем выводить PhotoImage из imageBackground
        labelImage[i].append(Label(root, bg=black))
        labelImage[i][j]["bd"] = 1
        labelImage[i][j].place(x=10 + j * widthPic, y=10 + i * heightPic)

        # Что произойдет при нажатии на Label
        labelImage[i][j].bind("<Button-1>", lambda e, x=i, y=j: go(x, y))

        # Устанавливаем изображение
        # символ \ означает перенос строки
        # Свойство ["image"] отвечает за изображение, oбьект PhotoImage
        labelImage[i][j]["image"] = \
            imageBackground[dataImage[i][j]]

# =================== ХОДЫ
steps = [0, 0, 0, 0, 0, 0]

# Началась ли игра?
playGame = False

# Наименьшее кол-во шагов для сбора головоломки
record = getRecordSteps()

# Обновляем текст
refreshText()

# Обновляем изображение
resetPictures()
root.mainloop()




