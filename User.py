class User:
    fleet_user = []
    fleet_user_array = []
    fleet = [1,1,1,1,2,2,2,3,3]
    count_ships = 0

    def __init__(self, offset_x_user, offset_y_user, prefix):
        self.offset_x_user = offset_x_user
        self.offset_y_user = offset_y_user
        self.prefix = prefix

