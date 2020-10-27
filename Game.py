from arguments_parcer import parse_arguments
from random import randrange
from time import sleep
from tkinter import *
from tkinter.messagebox import *
import Ship
import sys
import User
import Bot

class Application(Frame):

   # Cделать пвп
    # ширина рабочего поля
    width = 800
    # высота рабочего поля
    height = 400
    # цвет фона холста
    bg = "lightcyan"
    # отступ между ячейками
    indent = 1
    # смещение по y (отступ сверху)
    offset_y = 40
    # смещение по x пользовательского поля
    offset_x_user1 = 30
    # смещение по x поля компьютера
    offset_x_user2 = 430
    # компьютерный флот
    fleet_user2 = []
    # наш флот
    fleet_user = []
    # использованные клетки
    fleet_user_array = []
    lengths = []
    # массив точек, в которые стрелял компьютер
    user2_shot = []
    # массив точек, в которые попал компьютер, но ещё не убил
    comp_hit = []
    cur_ship = None
    first_player_turn = TRUE
    # добавление холста на окно
    def createCanvas(self):
        self.canv = Canvas(self)
        self.canv["height"] = self.height
        self.canv["width"] = self.width
        self.canv["bg"] = self.bg
        self.canv.pack()
        self.canv.focus_set()
        # установка кораблей юзера
        self.canv.bind("<Return>", self.creatingUserFleetEnter)
        self.canv.bind("<Key>", self.creatingUserFleetSpace)
        self.canv.bind("<Down>", self.creatingUserFleetDown)
        self.canv.bind("<Right>", self.creatingUserFleetRight)
        self.canv.bind("<Left>", self.creatingUserFleetLeft)
        self.canv.bind("<Up>", self.creatingUserFleetUp)
        self.canv.bind("<Shift-Up>", self.skipingShips)
        # клик по холсту вызывает функцию play
        self.canv.bind("<Button-1>", self.userPlay)

    def updateFleets(self):
        self.lengths = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]

    def createFieldUser(self, offset_x, color, tag):
        for i in range(self.size):
            # перебор столбцов
            for j in range(self.size):
                xn = j * self.gauge + (j + 1) * self.indent + offset_x
                xk = xn + self.gauge
                yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                yk = yn + self.gauge
                # добавление прямоугольника на холст с тегом в формате:
                # префикс_строка_столбец
                self.canv.create_rectangle(xn, yn, xk, yk, tag=tag + str(i) + "_" + str(j), fill=color)

    def add_numbers(self, offset_x):
        for i in reversed(range(self.size)):
            # цифры 1 игрока
            xc = offset_x - 15
            yc = i * self.gauge + (i + 1) * self.indent + self.offset_y + round(self.gauge / 2)
            self.canv.create_text(xc, yc, text=str(i + 1))

    def add_letters(self, offset_x):
        symbols = "АБВГДЕЖЗИКЛМНОПРСТУФ"
        for i in range(size):
            xc = i * self.gauge + (i + 1) * self.indent + offset_x + round(self.gauge / 2)
            yc = self.offset_y - 15
            self.canv.create_text(xc, yc, text=symbols[i])

    def new_game(self):
        self.fleet_user = []
        self.fleet_user_array = []
        self.canv.delete('all')
        self.updateFleets()
        # добавление игровых полей пользователя и компьютера
        # создание поля для пользователя
        # перебор строк
        self.createFieldUser(self.offset_x_user1, None, "my_")
        self.createFieldUser(self.offset_x_user2, "gray", "nmy_")
        self.add_numbers(self.offset_x_user1)
        self.add_numbers(self.offset_x_user2)
        # буквы
        self.add_letters(self.offset_x_user1)
        self.add_letters(self.offset_x_user2)
        # генерация кораблей противника
        if self.game_mode == "ON":
            self.createnmyships("nmy")
        self.cur_ship = Ship.Ship(self.lengths.pop(), self.size, 0, "my_0_0")
        self.paintUnreadyShip(self.cur_ship)

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
                    while 1:
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
        self.fleet_user2 = fleet_ships
    # юзер жмёт Enter
    def creatingUserFleetEnter(self, e):
        if len(self.fleet_user) < self.max_ships:
            # если корабль монжо поместить на это место, то помещаем туда и переходим к следующему
            intersect_array = list(set(self.fleet_user_array) & set(self.cur_ship.around_map + self.cur_ship.coord_map))
            if self.cur_ship.ship_correct == 1 and len(intersect_array) == 0:
                self.fleet_user_array += self.cur_ship.coord_map
                self.fleet_user.append(self.cur_ship)
                self.paintReadyShip(self.cur_ship, "blue")
                self.count_shops = self.count_shops - 1
                if len(self.lengths) and self.count_shops > 0:
                    self.cur_ship = Ship.Ship(self.lengths.pop(), self.size, 0, "my_0_0")
                    self.paintUnreadyShip(self.cur_ship)
               # if self.count_shops == 0 and self.game_mode == "ON" and self.player2.count_ships < self.max_ships:
                  #  self.actual_player = self.player2


    def skipingShips(self, e):
        if len(self.lengths):
            self.paintReadyShip(self.cur_ship, "lightcyan")
            if len(self.lengths) == 1:
                self.updateFleets()
            self.cur_ship = Ship.Ship(self.lengths.pop(), self.size, 0, "my_0_0")
            self.paintUnreadyShip(self.cur_ship)


    def creatingUserFleetDown(self, e):
        if len(self.fleet_user) < self.max_ships:
            self.fillRedInLightCyan(self.cur_ship)
            self.cur_ship = self.cur_ship.move(1, 0)
            self.paintUnreadyShip(self.cur_ship)

    def creatingUserFleetUp(self, e):
        if len(self.fleet_user) < self.max_ships:
            self.fillRedInLightCyan(self.cur_ship)
            self.cur_ship = self.cur_ship.move(-1, 0)
            self.paintUnreadyShip(self.cur_ship)

    def creatingUserFleetLeft(self, e):
        if len(self.fleet_user) < self.max_ships:
            self.fillRedInLightCyan(self.cur_ship)
            self.cur_ship = self.cur_ship.move(0, -1)
            self.paintUnreadyShip(self.cur_ship)

    def creatingUserFleetRight(self, e):
        if len(self.fleet_user) < self.max_ships:
            self.fillRedInLightCyan(self.cur_ship)
            self.cur_ship = self.cur_ship.move(0, 1)
            self.paintUnreadyShip(self.cur_ship)

    def creatingUserFleetSpace(self, e):
        if len(self.fleet_user) < self.max_ships and e.char == ' ':
            self.fillRedInLightCyan(self.cur_ship)
            self.cur_ship = self.cur_ship.rotate()
            self.paintUnreadyShip(self.cur_ship)

    def fillRedInLightCyan(self, ship):
        for point in ship.coord_map:
            self.canv.itemconfig(point, fill="lightcyan")
        for ship in self.fleet_user:
            for point in ship.coord_map:
                self.canv.itemconfig(point, fill="blue")

    def paintUnreadyShip(self, ship):
        for point in ship.coord_map:
            self.canv.itemconfig(point, fill="red")

    # метод для отрисовки корабля
    def paintReadyShip(self, ship, color):
        # отрисовка корабля
        for point in ship.coord_map:
            self.canv.itemconfig(point, fill=color)

    # метод рисования в ячейке креста на белом фоне
    def paintCross(self, xn, yn, tag):
        xk = xn + self.gauge
        yk = yn + self.gauge
        self.canv.itemconfig(tag, fill="white")
        self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, width="3")
        self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, width="3")

    # метод рисования промаха
    def paintMiss(self, point):
        # найти координаты
        line = int(point.split("_")[1])
        collumn = int(point.split("_")[2])
        if point.split("_")[0] == "nmy":
            xn = collumn * self.gauge + (collumn + 1) * self.indent + self.offset_x_user2 + self.gauge / 20 * self.size - round(self.size / 4)
        else:
            xn = collumn * self.gauge + (collumn + 1) * self.indent + self.offset_x_user1 + self.gauge / 20 * self.size - round(self.size / 4)
        yn = line * self.gauge + (line + 1) * self.indent + self.offset_y + self.gauge /20 * self.size - round(self.size / 4)
        # добавить прямоугольник
        # покрасить в белый
        self.canv.itemconfig(point, fill="red")
        self.canv.create_oval(xn, yn, xn, yn, fill="gray")

    # метод проверки финиша
    def checkFinish(self, type):
        '''type - указание, от чьего имени идёт обращение'''
        status = 0
        if type == "user":
            for ship in self.fleet_user2:
                status += ship.death
        else:
            for ship in self.fleet_user:
                status += ship.death
        return status

    # метод игры компьютера

    def AiPlayHard(self):
        if self.checkFinish("user") < self.max_ships and self.checkFinish("comp") < self.max_ships:
            sleep(1)
            # если нет точек, в которые попал, но не убил то генерировать случайные точки
            if len(self.comp_hit) == 0:
                # генерировать случайные точки, пока не будет найдена пара, которой не было в списке выстрелов
                while 1:
                    i = randrange(self.size)
                    j = randrange(self.size)
                    if not ("my_" + str(i) + "_" + str(j) in self.user2_shot):
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
                                ti == i and tj == j) and not ("my_" + str(ti) + "_" + str(tj) in self.user2_shot):
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
                        if not arr in self.user2_shot:
                            points_to_strike.append(arr)
                    # справа
                    if self.comp_hit[-1][5] != str(self.size - 1):
                        arr = self.comp_hit[-1].split('_')
                        arr[2] = str(int(arr[2]) + 1)
                        arr = arr[0] + '_' + arr[1] + '_' + arr[2]
                        if not arr in self.user2_shot:
                            points_to_strike.append(arr)
                else:
                    # сверху
                    if self.comp_hit[0][3] != '0':
                        arr = self.comp_hit[0].split('_')
                        arr[1] = str(int(arr[1]) - 1)
                        arr = arr[0] + '_' + arr[1] + '_' + arr[2]
                        if not arr in self.user2_shot:
                            points_to_strike.append(arr)
                    # снизу
                    if self.comp_hit[-1][3] != str(self.size - 1):
                        arr = self.comp_hit[-1].split('_')
                        arr[1] = str(int(arr[1]) + 1)
                        arr = arr[0] + '_' + arr[1] + '_' + arr[2]
                        if not arr in self.user2_shot:
                            points_to_strike.append(arr)
                # случайная точка (не больше двух)
                selected = points_to_strike[randrange(len(points_to_strike))]
                i = int(selected.split('_')[1])
                j = int(selected.split('_')[2])
            xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_user1
            yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
            hit_status = 0
            for obj in self.fleet_user:
                # если координаты точки совпадают с координатой корабля, то вызвать метод выстрела
                if "my_" + str(i) + "_" + str(j) in obj.coord_map:
                    hit_status = 2
                    # изменить статус попадания
                    self.comp_hit.append("my_" + str(i) + "_" + str(j))
                    # мы попали, поэтому надо нарисовать крест
                    self.paintCross(xn, yn, "my_" + str(i) + "_" + str(j))
                    # добавить точку в список выстрелов компьютера
                    self.user2_shot.append("my_" + str(i) + "_" + str(j))
                    # если метод вернул двойку, значит, корабль убит
                    if obj.shoot("my_" + str(i) + "_" + str(j)) == 2:
                        # изменить статус корабля
                        obj.death = 1
                        # все точки вокруг корабля сделать точками, в которые мы уже стреляли
                        for point in obj.around_map:
                            # нарисовать промахи
                            self.paintMiss(point)
                            # добавить точки вокруг корабля в список выстрелов компьютера
                            self.user2_shot.append(point)
                        showinfo("", "Убил!")
                        self.comp_hit.clear()
                    else:
                        showinfo("", "Попал!")
                    break
            # если статус попадания остался равным нулю - значит, мы промахнулись, передать управление компьютеру
            # иначе дать пользователю стрелять
            if hit_status == 0:
                # добавить точку в список выстрелов
                self.user2_shot.append("my_" + str(i) + "_" + str(j))
                self.paintMiss("my_" + str(i) + "_" + str(j))
                showinfo("", "Ха, лох, не попал!")
            else:
                # проверить выигрыш, если его нет - передать управление компьютеру
                if self.checkFinish("comp") < self.max_ships:

                    if self.bot_lvl == 1:
                        self.AiPlayEasy()
                    else:
                        self.AiPlayHard()
                else:
                    showinfo("", "Как ты слил компу?!")

    def AiPlayEasy(self):
        while 1:
            i = randrange(self.size)
            j = randrange(self.size)
            if not ("my_" + str(i) + "_" + str(j) in self.user2_shot):
                break
        xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_user1
        yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
        hit_status = 0
        for obj in self.fleet_user:
            # если координаты точки совпадают с координатой корабля, то вызвать метод выстрела
            if "my_" + str(i) + "_" + str(j) in obj.coord_map:
                hit_status = 2
                # изменить статус попадания
                self.comp_hit.append("my_" + str(i) + "_" + str(j))
                # мы попали, поэтому надо нарисовать крест
                self.paintCross(xn, yn, "my_" + str(i) + "_" + str(j))
                # добавить точку в список выстрелов компьютера
                self.user2_shot.append("my_" + str(i) + "_" + str(j))
                # если метод вернул двойку, значит, корабль убит
                if obj.shoot("my_" + str(i) + "_" + str(j)) == 2:
                    # изменить статус корабля
                    obj.death = 1
                    # все точки вокруг корабля сделать точками, в которые мы уже стреляли
                    for point in obj.around_map:
                        # нарисовать промахи
                        self.paintMiss(point)
                        # добавить точки вокруг корабля в список выстрелов компьютера
                        self.user2_shot.append(point)
                    showinfo("", "Убил!")
                    self.comp_hit.clear()
                else:
                    showinfo("", "Попал!")
                break
        # если статус попадания остался равным нулю - значит, мы промахнулись, передать управление компьютеру
        # иначе дать пользователю стрелять
        if hit_status == 0:
            # добавить точку в список выстрелов
            self.user2_shot.append("my_" + str(i) + "_" + str(j))
            self.paintMiss("my_" + str(i) + "_" + str(j))
            showinfo("", "Ха, лох, не попал!")
        else:
            # проверить выигрыш, если его нет - передать управление компьютеру
            if self.checkFinish("comp") < self.max_ships:
                if self.bot_lvl == 1:
                    self.AiPlayEasy()
                else:
                    self.AiPlayHard()
            else:
                showinfo("", "Как ты слил компу?!")

    # метод для игры пользователя
    def userPlay(self, e):
        if len(self.fleet_user) == self.max_ships and self.checkFinish("user") < self.max_ships and self.checkFinish("comp") < self.max_ships:
            for i in range(self.size):
                for j in range(self.size):
                    xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_user2
                    yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                    xk = xn + self.gauge
                    yk = yn + self.gauge
                    if e.x >= xn and e.x <= xk and e.y >= yn and e.y <= yk:
                        # проверить попали ли мы в корабль
                        hit_status = 0
                        for obj in self.fleet_user2:
                            # если координаты точки совпадают с координатой корабля, то вызвать метод выстрела
                            if "nmy_" + str(i) + "_" + str(j) in obj.coord_map:
                                # изменить статус попадания
                                hit_status = 1
                                # мы попали, поэтому надо нарисовать крест
                                self.paintCross(xn, yn, "nmy_" + str(i) + "_" + str(j))
                                # если метод вернул двойку, значит, корабль убит
                                if obj.shoot("nmy_" + str(i) + "_" + str(j)) == 2:
                                    # изменить статус корабля
                                    obj.death = 1
                                    # все точки вокруг корабля сделать точками, в которые мы уже стреляли
                                    for point in obj.around_map:
                                        # нарисовать промахи
                                        self.paintMiss(point)
                                    showinfo("", "Вы потопили корабль!")
                                else:
                                    showinfo("", "Вы попали!")
                                break
                        # если статус попадания остался равным нулю - значит, мы промахнулись, передать управление компьютеру
                        # иначе дать пользователю стрелять
                        if hit_status == 0:
                            self.paintMiss("nmy_" + str(i) + "_" + str(j))
                            showinfo("", "Вы промахнулись!")
                            # проверить выигрыш, если его нет - передать управление компьютеру
                            if self.checkFinish("user") < self.max_ships:
                                if self.bot_lvl == 1:
                                    self.AiPlayEasy()
                                else:
                                    self.AiPlayHard()
                            else:
                                showinfo("Морской бой", "Победил игрок!")
                        elif self.checkFinish("user") == self.max_ships:
                            showinfo("Морской бой", "Победил игрок!")
                        break

    def quit_game(self):
        root.destroy()

    def __init__(self, size, bot_lvl,game_mode, max_ships, rndShips, master=None):
        self.size = size
        self.bot_lvl = bot_lvl
        self.game_mode = game_mode
        self.max_ships = max_ships
        self.count_shops = max_ships
        self.rndFLeet = rndShips
        # размер одной из сторон квадратной ячейки
        self.gauge = 32 * 10/self.size
        self.player1 = User.User(self.offset_x_user1, self.offset_y, "my", self.max_ships, self.size)
        self.actual_player = self.player1
        if self.game_mode == "OFF":
            self.player2 = User.User(self.offset_x_user2, self.offset_y, "nmy", self.max_ships, self.size)
        else:
            self.player2 = Bot.Bot(self.max_ships, self.size, self.user2_shot, self.comp_hit, self.gauge, self.offset_x_user2, self.indent,
                               self.offset_y, self.fleet_user, self.paintCross, self.checkFinish, self.paintMiss, self.bot_lvl)
        Frame.__init__(self, master)
        self.pack()
        # инициализация меню
        self.m = Menu(master)
        master.config(menu=self.m)
        self.m_play = Menu(self.m)
        self.createCanvas()
        self.m.add_command(label="Новая игра", command=self.new_game)
        self.m.add_command(label="Выход", command=self.quit_game)

        root.protocol("WM_DELETE_WINDOW", self.quit_game)
        root.mainloop()


if __name__ == '__main__':
    args = parse_arguments()
    size = 10
    AI_Lvl = 2
    game_mode = "OFF"
    max_ships = 10
    rnd_Ships = "OFF"
    try:
        size = int(args.size_place)
        max_ships = args.count_ships
        if max_ships > 10 or max_ships < 1:
            max_ships = 10
        if size > 20 or size < 10:
            size = 10
        if args.game_mode == "ON":
            game_mode = "ON"
        if args.LVL_AI == 1:
            AI_Lvl = 1
        if args.random_ships == "ON":
            rnd_Ships = "ON"
    except PermissionError:
        sys.exit(11)
# инициализация окна
    root = Tk()
    root.title('WarShips')
    root.geometry("800x400+100+100")

# инициализация приложения
    app = Application(size,AI_Lvl,game_mode, max_ships,rnd_Ships,  root)
    app.mainloop()

    def checkFinish(self, type):
        '''type - указание, от чьего имени идёт обращение'''
        status = 0
        if type == "user":
            for ship in self.fleet_user2:
                status += ship.death
        else:
            for ship in self.fleet_user:
                status += ship.death
        return status
