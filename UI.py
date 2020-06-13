from CR_Finder import CR_Finder
from EncounterBuilder import EncounterBuilder
from PlayersTools import PlayersTools


def find_cr_atk_bonus(ac=10, hp=10, atk_bonus=3, tier=1, resistances=False, immunities=False):
    finder = CR_Finder()
    finder.avg_dice(2, 6, 5)
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
    finder.avg_dice(3, 6, 5)
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
players_dmg.avg_dice_collector()
players_dmg.avg_hit_chance(17, 5)

test.add_party(2, 6)

#  test.add_monster(find_cr_save_dc(ac=18, hp=300, save_dc=18, tier=3, immunities=True))
#  test.add_monster(find_cr_atk_bonus(ac=17, hp=100, atk_bonus=7))
test.add_monsters_group(1/8, 4)
test.add_monster(3)
test.get_difficulty()
