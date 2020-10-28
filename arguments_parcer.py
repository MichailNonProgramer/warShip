import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', type=int, dest='size_place', default=10,
                        help='Field size. Max 20x20')
    parser.add_argument('-AI', type=str, dest='game_mode',
                        default="ON",
                        help='PVP ON (OFF/ON)')
    parser.add_argument('-AILvl', type=int, dest='LVL_AI',
                        default=2,
                        help='LVL AI 1 or 2, default = 2')
    parser.add_argument('-cs', type=int, dest='count_ships', default=10,
                        help='Count ships 1-10. Max 10')
    parser.add_argument('-rndShips', type=str, dest='random_ships',
                        default="OFF",
                        help='Generate randoms ships, (OFF/ON), default OFF')
    parser.add_argument('-VK', type=str, dest='vk_post', default="OFF",
                        help='VK post result and INPUT LOGIN AND PASSWORD!, (OFF/ON), default OFF')
    parser.add_argument('-VKLogin', type=str, dest='vk_log', default="",
                        help='Input VK login')
    parser.add_argument('-VKPassword', type=str, dest='vk_pass', default="",
                        help='Input VK password')

    return parser.parse_args()