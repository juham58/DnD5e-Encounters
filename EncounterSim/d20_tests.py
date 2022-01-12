import re
import d20
from d20.dice import CritType

print(re.findall(r"\d?\d?\d?\d(?=d)", "12d8+2d4+4"))
print([(m.start(0), m.end(0)) for m in re.finditer(r"\d?\d?\d?\d(?=d)", "12d8+2d4+4")])
print("12d8+2d4+4"[0:2])

dice_input = "12d8+2d4+4"
for n, i in enumerate(str(2*int('12'))):
    dice_input[n] = i
print(dice_input)
