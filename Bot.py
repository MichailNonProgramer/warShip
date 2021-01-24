from time import sleep

import Ship
from random import randrange
from tkinter import *
from tkinter.messagebox import *
from User import User

class Bot(User):

    def __init__(self, max_ships, size, gauge, offset_x_user, indent, offset_y_user, paintCross, checkFinish, paintMiss,
                 bot_lvl, prefix, map_size, type, paintReadyShip, post_in_VK, vk_post, start_x, start_y):

        super().__init__(offset_x_user, offset_y_user, prefix, max_ships, map_size, type, paintReadyShip, start_x,
                         start_y)
        self.fleet_user = []
        self.comp_shoot = []
        self.comp_hit = []
        self.max_ships = max_ships
        self.size = size
        self.gauge = gauge
        self.offset_x_user = offset_x_user
        self.offset_y = offset_y_user
        self.indent = indent
        self.bot_lvl = bot_lvl
        self.paintCross = paintCross
        self.checkFinish = checkFinish
        self.paintMiss = paintMiss
        self.createnmyships()
        self.prefix = "nmy"
        self.post_in_VK = post_in_VK
        self.vk_post = vk_post

    def AiPlayHard(self, player):
        if self.checkFinish("user1") < self.max_ships and self.checkFinish("bot") < self.max_ships:
            # если нет точек, в которые попал, но не убил то генерировать случайные точки
            if len(self.comp_hit) == 0:
                # генерировать случайные точки, пока не будет найдена пара, которой не было в списке выстрелов
                while TRUE:
                    i = randrange(self.size)
                    j = randrange(self.size)
                    if not ("my_" + str(i) + "_" + str(j) in self.comp_shoot):
                        break
            # если есть одна такая точка
            elif len(self.comp_hit) == 1:
                # массив точек вокруг
                points_around = []
                i = int(self.comp_hit[0].split("_")[1])
                j = int(self.comp_hit[0].split("_")[2])
                for ti in range(i - 1, i + 2):
                    for tj in range(j - 1, j + 2):
                        if ti >= 0 and ti <= (self.size - 1) and tj >= 0 and tj <= (self.size - 1) and (ti == i or tj == j) and not (
                                ti == i and tj == j) and not ("my_" + str(ti) + "_" + str(tj) in self.comp_shoot):
                            points_around.append([ti, tj])
                # cлучайная точка из массива
                select = randrange(len(points_around))
                i = points_around[select][0]
                j = points_around[select][1]
            else:
                # если есть больше одной такой точки
                points_to_strike = []
                self.comp_hit.sort()
                # если у таких точек сопадает первая координата
                if self.comp_hit[0][3] == self.comp_hit[1][3]:
                    # проверяем точку слева от найденных
                    if self.comp_hit[0][5] != '0':
                        arr = self.comp_hit[0].split('_')
                        arr[2] = str(int(arr[2]) - 1)
                        arr = arr[0] + '_' + arr[1] + '_' + arr[2]
                        if not arr in self.comp_shoot:
                            points_to_strike.append(arr)
                    # справа
                    if self.comp_hit[-1][5] != str(self.size - 1):
                        arr = self.comp_hit[-1].split('_')
                        arr[2] = str(int(arr[2]) + 1)
                        arr = arr[0] + '_' + arr[1] + '_' + arr[2]
                        if not arr in self.comp_shoot:
                            points_to_strike.append(arr)
                else:
                    # сверху
                    if self.comp_hit[0][3] != '0':
                        arr = self.comp_hit[0].split('_')
                        arr[1] = str(int(arr[1]) - 1)
                        arr = arr[0] + '_' + arr[1] + '_' + arr[2]
                        if not arr in self.comp_shoot:
                            points_to_strike.append(arr)
                    # снизу
                    if self.comp_hit[-1][3] != str(self.size - 1):
                        arr = self.comp_hit[-1].split('_')
                        arr[1] = str(int(arr[1]) + 1)
                        arr = arr[0] + '_' + arr[1] + '_' + arr[2]
                        if not arr in self.comp_shoot:
                            points_to_strike.append(arr)
                # случайная точка (не больше двух)
                selected = points_to_strike[randrange(len(points_to_strike))]
                i = int(selected.split('_')[1])
                j = int(selected.split('_')[2])
            xn = j * self.gauge + (j + 1) * self.indent + player.offset_x_user
            yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
            hit_status = 0
            for obj in player.fleet_user:
                # если координаты точки совпадают с координатой корабля, то вызвать метод выстрела
                if "my_" + str(i) + "_" + str(j) in obj.coord_map:
                    hit_status = 2
                    # изменить статус попадания
                    self.comp_hit.append("my_" + str(i) + "_" + str(j))
                    self.user_hit.append("my_" + str(i) + "_" + str(j))
                    # мы попали, поэтому надо нарисовать крест
                    self.paintCross(xn, yn, "my_" + str(i) + "_" + str(j))
                    # добавить точку в список выстрелов компьютера
                    self.comp_shoot.append("my_" + str(i) + "_" + str(j))
                    # если метод вернул двойку, значит, корабль убит
                    if obj.shoot("my_" + str(i) + "_" + str(j)) == 2:
                        # изменить статус корабля
                        obj.death = 1
                        # все точки вокруг корабля сделать точками, в которые мы уже стреляли
                        for point in obj.around_map:
                            # нарисовать промахи
                            self.paintMiss(point)
                            self.user_missing.append(point)
                            # добавить точки вокруг корабля в список выстрелов компьютера
                            self.comp_shoot.append(point)
                        self.comp_hit.clear()
                    break
            # если статус попадания остался равным нулю - значит, мы промахнулись, передать управление компьютеру
            # иначе дать пользователю стрелять
            if hit_status == 0:
                # добавить точку в список выстрелов
                self.comp_shoot.append("my_" + str(i) + "_" + str(j))
                self.paintMiss("my_" + str(i) + "_" + str(j))
                self.user_missing.append("my_" + str(i) + "_" + str(j))
            else:
                # проверить выигрыш, если его нет - передать управление компьютеру
                if self.checkFinish("user2") < self.max_ships:

                    if self.bot_lvl == 1:
                        self.AiPlayEasy(player)
                    else:
                        self.AiPlayHard(player)
                else:
                    showinfo("", "Как ты слил компу?!")
                    if self.vk_post == "ON":
                        self.post_in_VK(FALSE)

    def AiPlayEasy(self, player):
        while TRUE:
            i = randrange(self.size)
            j = randrange(self.size)
            if not ("my_" + str(i) + "_" + str(j) in self.comp_shoot):
                break
        xn = j * self.gauge + (j + 1) * self.indent + player.offset_x_user
        yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
        hit_status = 0
        for obj in player.fleet_user:
            # если координаты точки совпадают с координатой корабля, то вызвать метод выстрела
            if "my_" + str(i) + "_" + str(j) in obj.coord_map:
                hit_status = 2
                # изменить статус попадания
                self.comp_hit.append("my_" + str(i) + "_" + str(j))
                # мы попали, поэтому надо нарисовать крест
                self.paintCross(xn, yn, "my_" + str(i) + "_" + str(j))
                self.user_hit.append("my_" + str(i) + "_" + str(j))
                # добавить точку в список выстрелов компьютера
                self.comp_shoot.append("my_" + str(i) + "_" + str(j))
                # если метод вернул двойку, значит, корабль убит
                if obj.shoot("my_" + str(i) + "_" + str(j)) == 2:
                    # изменить статус корабля
                    obj.death = 1
                    # все точки вокруг корабля сделать точками, в которые мы уже стреляли
                    for point in obj.around_map:
                        # нарисовать промахи
                        self.paintMiss(point)
                        self.user_missing(point)
                        # добавить точки вокруг корабля в список выстрелов компьютера
                        self.comp_shoot.append(point)
                    self.comp_hit.clear()
                break
        # если статус попадания остался равным нулю - значит, мы промахнулись, передать управление компьютеру
        # иначе дать пользователю стрелять
        if hit_status == 0:
            # добавить точку в список выстрелов
            self.comp_shoot.append("my_" + str(i) + "_" + str(j))
            self.paintMiss("my_" + str(i) + "_" + str(j))
            self.user_missing.append("my_" + str(i) + "_" + str(j))
        else:
            # проверить выигрыш, если его нет - передать управление компьютеру
            if self.checkFinish("user2") < self.max_ships:
                if self.bot_lvl == 1:
                    self.AiPlayEasy(player)
                else:
                    self.AiPlayHard(player)
            else:
                showinfo("", "Как ты слил компу?!")
                if self.vk_post == "ON":
                    self.post_in_VK(FALSE)

    def createnmyships(self, prefix="nmy"):
        # функция генерации кораблей на поле
        # количество сгенерированных кораблей
        global fleet_ships
        count_ships = 0
        while count_ships < self.max_ships:
            # массив занятых кораблями точек
            fleet_array = []
            # обнулить количество кораблей
            count_ships = 0
            # массив с флотом
            fleet_ships = []
            # генерация кораблей (length - палубность корабля)
            for length in reversed(range(1, 5)):
                # генерация необходимого количества кораблей необходимой длины
                for i in range(5 - length):
                    # генерация точки со случайными координатами, пока туда не установится корабль
                    while TRUE:
                        # генерация точки со случайными координатами
                        ship_point = prefix + "_" + str(randrange(self.size)) + "_" + str(randrange(self.size))
                        # случайное расположение корабля (либо горизонтальное, либо вертикальное)
                        orientation = randrange(2)
                        # создать экземпляр класса Ship
                        new_ship = Ship.Ship(length, self.size, orientation, ship_point)
                        # если корабль может быть поставлен корректно и его точки не пересекаются с уже занятыми точками поля
                        # пересечение множества занятых точек поля и точек корабля:
                        intersect_array = list(set(fleet_array) & set(new_ship.around_map + new_ship.coord_map))
                        if new_ship.ship_correct == 1 and len(intersect_array) == 0:
                            # добавить в массив со всеми занятыми точками точки вокруг корабля и точки самого корабля
                            fleet_array += new_ship.coord_map
                            fleet_ships.append(new_ship)
                            count_ships += 1
                            break
        self.fleet_user = fleet_ships