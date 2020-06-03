from CR_Finder import CR_Finder


class PlayersTools(CR_Finder):
    def __init__(self):
        self.avg_dice_list = []
        self.dmg = 0

    def avg_dice_collector(self):
        if len(self.avg_dice_list) == 0:
            self.dmg = 0
            return self.dmg
        self.dmg = round(sum(self.avg_dice_list))
        print("Players' average damage per round:", self.dmg)

    def avg_dice(self, x, y, z):
        return self.avg_dice_list.append(x*((y+1)/2)+z)

players_dmg = PlayersTools()
players_dmg.avg_dice(1, 8, 3)
players_dmg.avg_dice(1, 6, 3)
players_dmg.avg_dice(1, 12, 0)
players_dmg.avg_dice(1, 10, 3)
players_dmg.avg_dice(1, 10, 3)
players_dmg.avg_dice(1, 6, 0)
players_dmg.avg_dice(1, 6, 0)
players_dmg.avg_dice_collector()
