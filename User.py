import Ship
from random import randrange

class User:
    def __init__(self, offset_x_user, offset_y_user, prefix, max_ships, map_size, type, paintReadyShip, start_x, start_y):
        self.offset_x_user = offset_x_user
        self.offset_y_user = offset_y_user
        self.prefix = prefix
        self.max_ships = self.count_ships = max_ships
        self.size = map_size
        self.type = type
        self.paintReadyShip = paintReadyShip
        self.start_x = start_x
        self.start_y = start_y
        self.fleet_user = []
        # использованные клетки
        self.fleet_user_array = []
        self.lengths = [1, 1, 1, 1, 2, 2, 2, 3, 3]
        # стрелял в который
        # промахи
        self.user_missing = []
        # кресты
        self.user_hit = []

    def generateRandomShips(self):
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
                    while True:
                        # генерация точки со случайными координатами
                        ship_point = self.prefix + "_" + str(randrange(self.size)) + "_" + str(randrange(self.size))
                        # случайное расположение корабля (либо горизонтальное, либо вертикальное)
                        orientation = randrange(2)
                        # создать экземпляр класса Ship
                        new_ship = Ship.Ship(length, self.size, orientation, ship_point)
                        # если корабль может быть поставлен корректно и его точки не пересекаются с уже занятыми точками поля
                        # пересечение множества занятых точек поля и точек корабля:
                        intersect_array = list(set(self.fleet_user_array) & set(new_ship.around_map + new_ship.coord_map))
                        if new_ship.ship_correct == 1 and len(intersect_array) == 0:
                            # добавить в массив со всеми занятыми точками точки вокруг корабля и точки самого корабля
                            self.fleet_user_array += new_ship.coord_map
                            fleet_ships.append(new_ship)
                            self.paintReadyShip(new_ship, "blue")
                            count_ships += 1
                            break
        self.fleet_user = fleet_ships
