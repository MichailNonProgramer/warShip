from random import randrange
import Ship


class User:
    fleet_user = []
    fleet_user_array = []
    fleet = [1,1,1,1,2,2,2,3,3]
    count_ships = 0
    user_shoot = []

    def __init__(self, offset_x_user, offset_y_user, prefix, max_ships, map_size):
        self.offset_x_user = offset_x_user
        self.offset_y_user = offset_y_user
        self.prefix = prefix
        self.max_ships = max_ships
        self.size = map_size

    def generateRandomShips(self, prefix="my"):
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