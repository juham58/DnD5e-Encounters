from CR_Finder import CR_Finder


class PlayersTools(CR_Finder):
    def __init__(self):
        self.avg_dice_list = []
        self.dmg = 0
        self.adjusted_dmg = 0

    def avg_dice_collector(self):
        if len(self.avg_dice_list) == 0:
            self.dmg = 0
            return self.dmg
        self.dmg = round(sum(self.avg_dice_list))
        print("Players' average damage per round with 100% hit rate:", self.dmg)

    def avg_dice(self, x, y, z):
        return self.avg_dice_list.append(x*((y+1)/2)+z)

    def avg_hit_chance(self, monster_ac, avg_hit_mod):
        avg_hit_percentage = 1 - (monster_ac - avg_hit_mod)*(5/100)
        self.adjusted_dmg = avg_hit_percentage*self.dmg
        print("Players' average damage per round with target AC of {} and avergage hit modifier of {}:".format(monster_ac, avg_hit_mod), self.adjusted_dmg)

avg_calc = PlayersTools()
avg_calc.avg_dice(8, 6, 0)
avg_calc.avg_dice_collector()
print(avg_calc.dmg)
