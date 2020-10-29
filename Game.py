from time import sleep

import Ship
import vk_api
import User
import Bot
import pickle
from arguments_parcer import parse_arguments
from tkinter import *
from tkinter.messagebox import *

class Application(Frame):

   # Cделать пвп, сохраниние загрузка
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
    cur_ship = None
    change = TRUE
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
        if self.rnd_fLeet == "OFF":
            self.cur_ship = Ship.Ship(4, self.size, 0, "my_0_0")
            self.paintUnreadyShip(self.cur_ship)
        self.player1 = User.User(self.offset_x_user1, self.offset_y, "my", self.max_ships, self.size, "user1",
                                 self.paintReadyShip, "0", "0")
        self.actual_player = self.player1
        if self.rnd_fLeet == "ON":
            self.player1.generateRandomShips()
        if self.game_mode == "OFF":
            self.player2 = User.User(self.offset_x_user2, self.offset_y, "nmy", self.max_ships, self.size, "user2",
                                     self.paintReadyShip, str(self.offset_x_user2), "0")
            if self.rnd_fLeet == "ON":
                self.player2.generateRandomShips()
        else:
            self.player2 = Bot.Bot(self.max_ships, self.size, self.gauge, self.offset_x_user2, self.indent,
                                   self.offset_y, self.paintCross, self.checkFinish, self.paintMiss, self.bot_lvl,
                                   self.size, "nmy", "bot", self.paintReadyShip, self.post_in_VK, self.vk_post, 0, 0)
        self.wating_player = self.player2
        print(self.actual_player.prefix, self.wating_player.prefix)

    # юзер жмёт Enter
    def creatingUserFleetEnter(self, e):
        if len(self.actual_player.fleet_user) < self.max_ships:
            # если корабль монжо поместить на это место, то помещаем туда и переходим к следующему
            intersect_array = list(set(self.actual_player.fleet_user_array) & set(self.cur_ship.around_map + self.cur_ship.coord_map))
            if self.cur_ship.ship_correct == 1 and len(intersect_array) == 0:
                self.actual_player.fleet_user_array += self.cur_ship.coord_map
                self.actual_player.fleet_user.append(self.cur_ship)
                self.paintReadyShip(self.cur_ship, "blue")
                self.actual_player.count_ships = self.actual_player.count_ships - 1
                if len(self.actual_player.lengths) and self.actual_player.count_ships > 0:
                    self.cur_ship = Ship.Ship(self.actual_player.lengths.pop(), self.size, 0, self.actual_player.prefix + "_" + str(0)
                                              + "_" + str(0))
                    self.paintUnreadyShip(self.cur_ship)
                elif len(self.actual_player.fleet_user) == len(self.wating_player.fleet_user) == self.max_ships:
                    self.changePlayer(self.player1, self.player2)
                    showinfo("", "Ходит игрок 1")
                    sleep(1)
                if self.actual_player.count_ships == 0 and self.game_mode == "OFF" and self.change:
                    self.change = FALSE
                    self.changePlayer(self.player2, self.player1)
                    self.cur_ship = Ship.Ship(4, self.size, 0, "nmy_0_0")
                    self.paintUnreadyShip(self.cur_ship)
                    showinfo("", "2 игрок ставит кораблики")
                    sleep(1)

    def updateMapActual(self):
        for i in range(self.size):
            for j in range(self.size):
                xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_user1
                xk = xn + self.gauge
                yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                yk = yn + self.gauge
                self.canv.create_rectangle(xn, yn, xk, yk,
                                           tag=str(self.actual_player.prefix) + "_" + str(i) + "_" + str(j), fill="white")
                point = str(self.actual_player.prefix) + "_" + str(i) + "_" + str(j)
                if point in self.wating_player.user_hit:
                    self.paintCross(xn, yn, self.actual_player.prefix)
                if point in self.wating_player.user_missing:
                    self.paintMiss(point)

    def updateMapWating(self):
        for i in range(self.size):
            for j in range(self.size):
                xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_user2
                xk = xn + self.gauge
                yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                yk = yn + self.gauge
                self.canv.create_rectangle(xn, yn, xk, yk,
                                           tag=str(self.wating_player.prefix) + "_" + str(i) + "_" + str(j), fill="white")
                point = str(self.wating_player.prefix) + "_" + str(i) + "_" + str(j)
                if point in self.actual_player.user_hit:
                    self.paintCross(xn, yn, self.wating_player.prefix)
                if point in self.actual_player.user_missing:
                    self.paintMiss(point)

    def skipingShips(self, e):
        if len(self.actual_player.lengths) <= 1:
            self.actual_player.lengths = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        if len(self.actual_player.lengths):
            self.paintReadyShip(self.cur_ship, "lightcyan")
            self.cur_ship = Ship.Ship(self.actual_player.lengths.pop(), self.actual_player.size, 0, "my_0_0")
            self.paintUnreadyShip(self.cur_ship)
            print(self.actual_player.lengths)

    def creatingUserFleetDown(self, e):
        if len(self.actual_player.fleet_user) < self.actual_player.max_ships:
            self.fillRedInLightCyan(self.cur_ship)
            self.cur_ship = self.cur_ship.move(1, 0)
            self.paintUnreadyShip(self.cur_ship)

    def creatingUserFleetUp(self, e):
        if len(self.actual_player.fleet_user) < self.actual_player.max_ships:
            self.fillRedInLightCyan(self.cur_ship)
            self.cur_ship = self.cur_ship.move(-1, 0)
            self.paintUnreadyShip(self.cur_ship)

    def creatingUserFleetLeft(self, e):
        if len(self.actual_player.fleet_user) < self.actual_player.max_ships:
            self.fillRedInLightCyan(self.cur_ship)
            self.cur_ship = self.cur_ship.move(0, -1)
            self.paintUnreadyShip(self.cur_ship)

    def creatingUserFleetRight(self, e):
        if len(self.actual_player.fleet_user) < self.actual_player.max_ships:
            self.fillRedInLightCyan(self.cur_ship)
            self.cur_ship = self.cur_ship.move(0, 1)
            self.paintUnreadyShip(self.cur_ship)

    def creatingUserFleetSpace(self, e):
        if len(self.actual_player.fleet_user) < self.actual_player.max_ships and e.char == ' ':
            self.fillRedInLightCyan(self.cur_ship)
            self.cur_ship = self.cur_ship.rotate()
            self.paintUnreadyShip(self.cur_ship)

    def fillRedInLightCyan(self, ship):
        for point in ship.coord_map:
            self.canv.itemconfig(point, fill="lightcyan")
        for ship in self.actual_player.fleet_user:
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
            xn = collumn * self.gauge + (collumn + 1) * self.indent + self.wating_player.offset_x_user + self.gauge / 20 * self.size - round(self.size / 4)
        else:
            xn = collumn * self.gauge + (collumn + 1) * self.indent + self.actual_player.offset_x_user + self.gauge / 20 * self.size - round(self.size / 4)
        yn = line * self.gauge + (line + 1) * self.indent + self.offset_y + self.gauge /20 * self.size - round(self.size / 4)
        self.canv.itemconfig(point, fill="red")
        self.canv.create_oval(xn, yn, xn, yn, fill="gray")

    # метод проверки финиша
    def checkFinish(self, type):
        '''type - указание, от чьего имени идёт обращение'''
        status = 0
        if type == "user1":
            for ship in self.player2.fleet_user:
                status += ship.death
        else:
            for ship in self.player1.fleet_user:
                status += ship.death
        return status

    # метод для игры пользователя
    def userPlay(self, e):
        if len(self.actual_player.fleet_user) == self.actual_player.max_ships \
                and self.checkFinish(str(self.actual_player.type)) < self.actual_player.max_ships \
                and self.checkFinish(str(self.wating_player.type)) < self.actual_player.max_ships\
                and len(self.wating_player.fleet_user) == self.wating_player.max_ships:
            for i in range(self.size):
                for j in range(self.size):
                    xn = j * self.gauge + (j + 1) * self.indent + self.player2.offset_x_user
                    yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                    xk = xn + self.gauge
                    yk = yn + self.gauge
                    if e.x >= xn and e.x <= xk and e.y >= yn and e.y <= yk:
                        # проверить попали ли мы в корабль
                        hit_status = 0
                        for obj in self.wating_player.fleet_user:
                            # если координаты точки совпадают с координатой корабля, то вызвать метод выстрела
                            if str(self.wating_player.prefix) + "_" + str(i) + "_" + str(j) in obj.coord_map:
                                # изменить статус попадания
                                hit_status = 1
                                # мы попали, поэтому надо нарисовать крест
                                self.paintCross(xn, yn, str(self.wating_player.prefix) + "_" + str(i) + "_" + str(j))
                                self.actual_player.user_hit.append(str(self.wating_player.prefix) + "_" + str(i) + "_" + str(j))
                                # если метод вернул двойку, значит, корабль убит
                                if obj.shoot(str(self.wating_player.prefix) + "_" + str(i) + "_" + str(j)) == 2:
                                    # изменить статус корабля
                                    obj.death = 1
                                    # все точки вокруг корабля сделать точками, в которые мы уже стреляли
                                    for point in obj.around_map:
                                        # нарисовать промахи
                                        self.paintMiss(point)
                                        self.actual_player.user_missing.append(point)
                                break
                        # если статус попадания остался равным нулю - значит, мы промахнулись, передать управление компьютеру
                        # иначе дать пользователю стрелять
                        if hit_status == 0 and not ((str(self.wating_player.prefix) + "_" + str(i) + "_" + str(j)) in self.actual_player.user_missing):
                            point = str(self.wating_player.prefix) + "_" + str(i) + "_" + str(j)
                            self.paintMiss(point)
                            self.actual_player.user_missing.append(point)
                            # проверить выигрыш, если его нет - передать управление компьютеру // другому игроку
                            if self.checkFinish(str(self.actual_player.type)) < self.max_ships:
                                if self.game_mode == "ON":
                                    if self.bot_lvl == 1:
                                        self.player2.AiPlayEasy(self.actual_player)
                                    else:
                                        self.player2.AiPlayHard(self.actual_player)
                                else:
                                    if self.actual_player is self.player1:
                                        self.changePlayer(self.player2, self.player1)
                                        showinfo("", "Ходит игрок 2")
                                        sleep(1)
                                    else:
                                        self.changePlayer(self.player1, self.player2)
                                        showinfo("", "Ходит игрок 1")
                                        sleep(1)
                            else:
                                showinfo("Морской бой", "Победил игрок {}!".format(str(self.actual_player.type)))
                                if self.vk_post == "ON":
                                    self.post_in_VK(TRUE)
                        elif self.checkFinish(self.actual_player.type) == self.max_ships:
                            showinfo("Морской бой", "Победил игрок {}!".format(str(self.actual_player.type)))
                            if self.vk_post == "ON":
                                self.post_in_VK(TRUE)
                        break

    def post_in_VK(self, win):
        mes = "Я проиграл"
        if win:
            mes = "Я победил"
        try:
            vk_session = vk_api.VkApi(self.vk_log, self.vk_passw)
            vk_session.auth()
            vk = vk_session.get_api()
            print(vk.wall.post(message=mes + "в морском бое от @mcgernogorov"))
        except(vk_api.VkRequestsPoolException):
            showinfo("", "Введите правильный логин/пароль")

    def changePlayer(self, p1, p2):
        self.actual_player = p1
        self.wating_player = p2
        self.updateMapActual()
        self.updateMapWating()

    def quit_game(self):
        root.destroy()

    def save(self):
        with open("save_player1.pkl", "wb") as file:
            pickle.dump({"offset_x_user" : self.player1.offset_x_user, "offset_y_user" : self.player1.offset_y_user,
                         "user_missing" : self.player1.user_missing, "fleet_user" : self.player1.fleet_user,
                         "fleet_user_array" : self.player1.fleet_user_array, "prefix" : self.player1.prefix,
                         "lengths" : self.player1.lengths, "count_ships" : self.player1.count_ships, "max_ships" : self.player1.max_ships,
                         "size" : self.player1.size, "user_hit" : self.player1.user_hit }, file)
        with open("save_player2.pkl", "wb") as file:
            pickle.dump({"offset_x_user" : self.player2.offset_x_user, "offset_y_user" : self.player2.offset_y_user,
                         "user_missing" : self.player2.user_missing, "fleet_user" : self.player2.fleet_user,
                         "fleet_user_array" : self.player2.fleet_user_array, "prefix" : self.player2.prefix,
                         "lengths" : self.player2.lengths, "count_ships" : self.player2.count_ships, "max_ships" : self.player2.max_ships,
                         "size" : self.player2.size, "user_hit" : self.player2.user_hit}, file)

    def load(self):
        with open("save_player1.pkl", "rb") as file:
            player1 = pickle.load(file)
        with open("save_player2.pkl", "rb") as file:
            player2 = pickle.load(file)
        self.updatePlayers(player1, player2)
        self.updateMapActual()
        self.updateMapWating()

    def updatePlayers(self, p1, p2):
        self.actual_player.user_missing = p1["user_missing"]
        self.actual_player.fleet_user = p1["fleet_user"]
        self.actual_player.fleet_user_array = p1["fleet_user_array"]
        self.actual_player.lengths = p1["lengths"]
        self.actual_player.count_ships = p1["count_ships"]
        self.actual_player.size = p1["size"]
        self.actual_player.max_ships = p1["max_ships"]
        self.actual_player.prefix = p1["prefix"]
        self.actual_player.offset_x_user = p1["offset_x_user"]
        self.actual_player.offset_y_user = p1["offset_y_user"]
        self.actual_player.user_hit = p1["user_hit"]
        self.actual_player.max_ships = p1["max_ships"]
        self.actual_player.size = p1["size"]
        self.wating_player.user_missing = p2["user_missing"]
        self.wating_player.fleet_user = p2["fleet_user"]
        self.wating_player.fleet_user_array = p2["fleet_user_array"]
        self.wating_player.lengths = p2["lengths"]
        self.wating_player.count_ships = p2["count_ships"]
        self.wating_player.size = p2["size"]
        self.wating_player.max_ships = p2["max_ships"]
        self.wating_player.prefix = p2["prefix"]
        self.wating_player.offset_x_user = p2["offset_x_user"]
        self.wating_player.offset_y_user = p2["offset_y_user"]
        self.wating_player.user_hit = p2["user_hit"]
        self.wating_player.max_ships = p2["max_ships"]
        self.wating_player.size = p2["size"]
        self.size = p1["size"]
        self.max_ships = p1["max_ships"]

    def __init__(self, size, bot_lvl,game_mode, max_ships, rnd_ships, vk_post, vk_log, vk_passw, master=None):
        self.size = size
        self.bot_lvl = bot_lvl
        self.game_mode = game_mode
        self.max_ships = max_ships
        self.count_ships = max_ships
        self.rnd_fLeet = rnd_ships
        # размер одной из сторон квадратной ячейки
        self.gauge = 32 * 10/self.size
        self.vk_post=vk_post
        self.vk_passw = vk_passw
        self.vk_log = vk_log
        Frame.__init__(self, master)
        self.pack()
        # инициализация меню
        self.m = Menu(master)
        master.config(menu=self.m)
        self.m_play = Menu(self.m)
        self.createCanvas()
        self.m.add_command(label="Новая игра", command=self.new_game)
        self.m.add_command(label="Выход", command=self.quit_game)
        self.m.add_command(label="Сохранить", command=self.save)
        self.m.add_command(label="Загрузить", command=self.load)

        root.protocol("WM_DELETE_WINDOW", self.quit_game)
        root.mainloop()


if __name__ == '__main__':
    args = parse_arguments()
    size = 10
    AI_Lvl = 2
    game_mode = "ON"
    max_ships = 10
    rnd_ships = "OFF"
    vk_post = "OFF"
    vk_log = ""
    vk_passw = ""
    try:
        size = int(args.size_place)
        max_ships = args.count_ships
        if max_ships > 10 or max_ships < 1:
            max_ships = 10
        if size > 20 or size < 10:
            size = 10
        if args.game_mode == "OFF":
            game_mode = "OFF"
        if args.LVL_AI == 1:
            AI_Lvl = 1
        if args.random_ships == "ON":
            rnd_ships = "ON"
        if args.vk_post == "ON":
            vk_post = "ON"
        vk_log = args.vk_log
        vk_passw = args.vk_pass
    except PermissionError:
        sys.exit(11)
# инициализация окна
    root = Tk()
    root.title('WarShips')
    root.geometry("800x400+100+100")

# инициализация приложения
    app = Application(size,AI_Lvl,game_mode, max_ships, rnd_ships, vk_post, vk_log, vk_passw, root)
    app.mainloop()
