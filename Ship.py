class Ship():
    # свойства объектов, описанные в классе
    # длина
    length = 1
    # массив со статусами точек корабля
    status_map = []
    # массив с координатами точек корабля
    coord_map = []
    # точки вокруг корабля
    around_map = []
    # статус гибели корабля
    death = 0
    # префикс тега
    prefix = ""
    # свойство: корабль был создан и не выходит за рамки поля
    ship_correct = 1
    # таг, отвечающий за верхний левый угол
    key_point = ""
    # ориентация
    orient = -1

    # метод-конструктор
    def __init__(self, length, size, rasp, keypoint):
        self.status_map = []
        self.around_map = []
        self.coord_map = []
        self.death = 0
        self.ship_correct = 1
        self.length = length
        self.key_point = keypoint
        self.orient = rasp
        self.size = size
        # переопределить переменную self.prefix
        self.prefix = keypoint.split("_")[0]
        # создать массивы status_map и coord_map (в зависимости от направления)
        line = int(keypoint.split("_")[1])
        column = int(keypoint.split("_")[2])
        for i in range(length):
            self.status_map.append(0)
            # в зависимости от направления генерировать новые точки корабля
            # 0 - горизонт (увеличивать столбец), 1 - вертикаль (увеличивать строку)
            if column + i * (1 - self.orient) > (self.size - 1) or line + i * self.orient > (self.size - 1) or column < 0 or line < 0:
                self.ship_correct = 0
            if rasp == 0:
                self.coord_map.append(self.prefix + "_" + str(line) + "_" + str(column + i))
            else:
                self.coord_map.append(self.prefix + "_" + str(line + i) + "_" + str(column))
        for point in self.coord_map:
            ti = int(point.split("_")[1])
            tj = int(point.split("_")[2])
            for ri in range(ti - 1, ti + 2):
                for rj in range(tj - 1, tj + 2):
                    if ri >= 0 and ri <= (self.size - 1) and rj >= 0 and rj <= (self.size - 1):
                        if not (self.prefix + "_" + str(ri) + "_" + str(rj) in self.around_map) and not (
                                self.prefix + "_" + str(ri) + "_" + str(rj) in self.coord_map):
                            self.around_map.append(self.prefix + "_" + str(ri) + "_" + str(rj))

    # выстрел
    def shoot(self, shootpoint):
        # определить номер точки и изменить её статус
        status = 0
        for point in range(len(self.coord_map)):
            if self.coord_map[point] == shootpoint:
                self.status_map[point] = 1
                status = 1
                break
        if not (0 in self.status_map):
            status = 2
            self.death = 1
        return status

    # подвинуть корабль
    def move(self, dx, dy):
        arr = self.key_point.split("_")
        new_ship = Ship(self.length, self.size, self.orient, arr[0] + "_" + str(int(arr[1]) + dx) + "_" + str(int(arr[2]) + dy))
        if new_ship.ship_correct:
            self = new_ship
        return self

    # повернуть корабль
    def rotate(self):
        new_ship = Ship(self.length, self.size,  1 - self.orient, self.key_point)
        if new_ship.ship_correct:
            self = new_ship
        return self