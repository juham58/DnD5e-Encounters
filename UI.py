from CR_Finder import CR_Finder
from EncounterBuilder import EncounterBuilder
from PlayersTools import PlayersTools


def find_cr_atk_bonus(ac=10, hp=10, atk_bonus=3, tier=1, resistances=False, immunities=False):
    finder = CR_Finder()
    finder.avg_dice(1, 8, 3)
    finder.avg_dice(1, 6, 3)
    finder.avg_dice_collector()
    finder.set_tier(tier)
    finder.set_resistances(resistances)
    finder.set_immunities(immunities)
    finder.cr_from_hp(hp)
    finder.cr_from_ac(ac)
    finder.cr_from_dmg()
    finder.cr_from_atk_bonus(atk_bonus)
    return finder.get_final_cr()


def find_cr_save_dc(ac=10, hp=10, save_dc=10, tier=1, resistances=False, immunities=False):
    finder = CR_Finder()
    finder.avg_dice(1, 8, 3)
    finder.avg_dice(1, 6, 3)
    finder.avg_dice_collector()
    finder.set_tier(tier)
    finder.set_resistances(resistances)
    finder.set_immunities(immunities)
    finder.cr_from_hp(hp)
    finder.cr_from_ac(ac)
    finder.cr_from_dmg()
    finder.cr_from_atk_bonus(save_dc)
    return finder.get_final_cr()


test = EncounterBuilder()
players_dmg = PlayersTools()
players_dmg.avg_dice(1, 8, 3)
players_dmg.avg_dice(1, 6, 3)
players_dmg.avg_dice(3, 8, 0)
players_dmg.avg_dice(1, 10, 3)
players_dmg.avg_dice(1, 10, 3)
players_dmg.avg_dice(1, 6, 0)
players_dmg.avg_dice(1, 6, 0)
players_dmg.avg_dice(1, 4, 0)
players_dmg.avg_dice_collector()
players_dmg.dmg = 171
players_dmg.avg_hit_chance(17, 8)

test.add_party(6, 6)

#find_cr_atk_bonus(ac=17, hp=84, atk_bonus=8)

#  test.add_monster(find_cr_save_dc(ac=18, hp=300, save_dc=18, tier=3, immunities=True))
#  test.add_monster(find_cr_atk_bonus(ac=17, hp=100, atk_bonus=7))
#find_cr_atk_bonus(ac=16, hp=11, atk_bonus=3, )
test.add_monsters_group(11, 2)
#test.add_monster(find_cr_atk_bonus(ac=16, hp=150, atk_bonus=5))
test.get_difficulty()
