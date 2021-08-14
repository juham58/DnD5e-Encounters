// @ts-ignore
import DDBEntity from './ddbentity.spec.ts';

type Ability = 'str' | 'dex' | 'con' | 'int' | 'wis' | 'cha';

class Class extends DDBEntity {
    name: string;
    hit_points: string;
    proficiencies: string;
    equipment: string;
    table: ClassTable;
    // list of list of class features - e.g. levels[0] is a list of all granted class features at level 1
    levels: ClassFeature[][];
    subclasses: Subclass[];
}

class ClassTable {
    headers: string[];
    // for each level, the value under each header
    // e.g. levels[0][1] is the value of the 2nd header at 1st level
    levels: string[][];  // outer arr len = 20, inner arr len = len(headers)
}

class ClassFeature {
    name: string;
    text: string;  // Markdown-formatted
}

class Subclass extends DDBEntity {
    name: string;
    // list of list of class features - e.g. levels[0] is a list of all granted class features at level 1
    // for subclasses, there are likely a lot of empty levels
    levels: ClassFeature[][];
}

// examples:
/*
{
  "name": "Bard",
  "hit_die": "1d8",
  "saves": [
    "dex",
    "cha"
  ],
  "proficiencies": {
    "armor": [
      "light"
    ],
    "weapons": [
      "simple",
      "hand crossbows",
      "longswords",
      "rapiers",
      "shortswords"
    ],
    "tools": [
      "three musical instruments of your choice"
    ],
    "skills": ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"],
    "num_skills": 3
  },
  "equipment": "• (a) a rapier, (b) a longsword, or (c) any simple weapon\n• (a) a diplomat's pack or (b) an entertainer's pack\n• (a) a lute or (b) any other musical instrument\n• Leather armor, and a dagger",
  "table": {
    "headers": [
      "Cantrips Known",
      "Spells Known",
      "1st",
      "2nd",
      "3rd",
      "4th",
      "5th",
      "6th",
      "7th",
      "8th",
      "9th"
    ],
    "levels": [
      [
        "2",
        "4",
        "2",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0"
      ],
      [
        "2",
        "5",
        "3",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0"
      ],
      [
        "2",
        "6",
        "4",
        "2",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0"
      ],
      [
        "3",
        "7",
        "4",
        "3",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0"
      ],
      ...
    ]
  },
  "levels": [
    [
      {
        "name": "Bardic Inspiration",
        "text": "You can inspire others through stirring words or music. To do so, you use a bonus action on your turn to choose one creature other than yourself within 60 feet of you who can hear you. That creature gains one Bardic Inspiration die, a d6.\nOnce within the next 10 minutes, the creature can roll the die and add the number rolled to one ability check, attack roll, or saving throw it makes. The creature can wait until after it rolls the d20 before deciding to use the Bardic Inspiration die, but must decide before the DM says whether the roll succeeds or fails. Once the Bardic Inspiration die is rolled, it is lost. A creature can have only one Bardic Inspiration die at a time.\nYou can use this feature a number of times equal to your Charisma modifier (a minimum of once). You regain any expended uses when you finish a long rest.\nYour Bardic Inspiration die changes when you reach certain levels in this class. The die becomes a d8 at 5th level, a d10 at 10th level, and a d12 at 15th level."
      },
      {
        "name": "Spellcasting",
        "text": "You have learned to untangle and reshape the fabric of reality in harmony with your wishes and music. Your spells are part of your vast repertoire, magic that you can tune to different situations. See chapter 10 for the general rules of spellcasting and chapter 11 for the bard spell list.\n**Cantrips**: You know two cantrips of your choice from the bard spell list. You learn additional bard cantrips of your choice at higher levels, learning a 3rd cantrip at 4th level and a 4th at 10th level.\n**Spell Slots**: The Bard table shows how many spell slots you have to cast your bard spells of 1st level and higher. To cast one of these spells, you must expend a slot of the spell's level or higher. You regain all expended spell slots when you finish a long rest.\nFor example, if you know the 1st-level spell cure wounds and have a 1st-level and a 2nd-level spell slot available, you can cast cure wounds using either slot.\n**Spells Known of 1st Level and Higher**: You know four 1st-level spells of your choice from the bard spell list.\nYou learn an additional bard spell of your choice at each level except 12th, 16th, 19th, and 20th. Each of these spells must be of a level for which you have spell slots. For instance, when you reach 3rd level in this class, you can learn one new spell of 1st or 2nd level.\nAdditionally, when you gain a level in this class, you can choose one of the bard spells you know and replace it with another spell from the bard spell list, which also must be of a level for which you have spell slots.\n**Spellcasting Ability**: Charisma is your spellcasting ability for your bard spells. Your magic comes from the heart and soul you pour into the performance of your music or oration. You use your Charisma whenever a spell refers to your spellcasting ability. In addition, you use your Charisma modifier when setting the saving throw DC for a bard spell you cast and when making an attack roll with one.\n`Spell Save DC = 8 + Charisma modifier + Proficiency Bonus`\n`Spell Attack Bonus = Charisma modifier + Proficiency Bonus`\n**Ritual Casting**: You can cast any bard spell you know as a ritual if that spell has the ritual tag.\n**Spellcasting Focus**: You can use a musical instrument (found in chapter 5) as a spellcasting focus for your bard spells."
      },
      {
        "name": "Spellcasting: Cantrips",
        "text": "You know two cantrips of your choice from the bard spell list. You learn additional bard cantrips of your choice at higher levels, learning a 3rd cantrip at 4th level and a 4th at 10th level."
      },
      {
        "name": "Spellcasting: Spell Slots",
        "text": "The Bard table shows how many spell slots you have to cast your bard spells of 1st level and higher. To cast one of these spells, you must expend a slot of the spell's level or higher. You regain all expended spell slots when you finish a long rest.\nFor example, if you know the 1st-level spell cure wounds and have a 1st-level and a 2nd-level spell slot available, you can cast cure wounds using either slot."
      },
      {
        "name": "Spellcasting: Spells Known of 1st Level and Higher",
        "text": "You know four 1st-level spells of your choice from the bard spell list.\nYou learn an additional bard spell of your choice at each level except 12th, 16th, 19th, and 20th. Each of these spells must be of a level for which you have spell slots. For instance, when you reach 3rd level in this class, you can learn one new spell of 1st or 2nd level.\nAdditionally, when you gain a level in this class, you can choose one of the bard spells you know and replace it with another spell from the bard spell list, which also must be of a level for which you have spell slots."
      },
      {
        "name": "Spellcasting: Spellcasting Ability",
        "text": "Charisma is your spellcasting ability for your bard spells. Your magic comes from the heart and soul you pour into the performance of your music or oration. You use your Charisma whenever a spell refers to your spellcasting ability. In addition, you use your Charisma modifier when setting the saving throw DC for a bard spell you cast and when making an attack roll with one.\n`Spell Save DC = 8 + Charisma modifier + Proficiency Bonus`\n`Spell Attack Bonus = Charisma modifier + Proficiency Bonus`"
      },
      {
        "name": "Spellcasting: Ritual Casting",
        "text": "You can cast any bard spell you know as a ritual if that spell has the ritual tag."
      },
      {
        "name": "Spellcasting: Spellcasting Focus",
        "text": "You can use a musical instrument (found in chapter 5) as a spellcasting focus for your bard spells."
      }
    ],
    [
      {
        "name": "Jack of All Trades",
        "text": "Starting at 2nd level, you can add half your proficiency bonus, rounded down, to any ability check you make that doesn't already include your proficiency bonus."
      },
      {
        "name": "Song of Rest (d6)",
        "text": "Beginning at 2nd level, you can use soothing music or oration to help revitalize your wounded allies during a short rest. If you or any friendly creatures who can hear your performance regain hit points by spending Hit Dice at the end of the short rest, each of those creatures regains an extra 1d6 hit points.\nThe extra hit points increase when you reach certain levels in this class: to 1d8 at 9th level, to 1d10 at 13th level, and to 1d12 at 17th level."
      }
    ],
    [
      {
        "name": "Bard College",
        "text": "At 3rd level, you delve into the advanced techniques of a bard college of your choice from the list of available colleges. Your choice grants you features at 3rd level and again at 6th and 14th level."
      },
      {
        "name": "Expertise",
        "text": "At 3rd level, choose two of your skill proficiencies. Your proficiency bonus is doubled for any ability check you make that uses either of the chosen proficiencies.\nAt 10th level, you can choose another two skill proficiencies to gain this benefit."
      }
    ],
    [
      {
        "name": "Ability Score Improvement",
        "text": "When you reach 4th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1. As normal, you can't increase an ability score above 20 using this feature.\nIf your DM allows the use of feats, you may instead take a feat."
      }
    ],
    [
      {
        "name": "Bardic Inspiration (d8)",
        "text": "At 5th level, your Bardic Inspiration die changes to a d8."
      },
      {
        "name": "Font of Inspiration",
        "text": "Beginning when you reach 5th level, you regain all of your expended uses of Bardic Inspiration when you finish a short or long rest."
      }
    ],
    [
      {
        "name": "Countercharm",
        "text": "At 6th level, you gain the ability to use musical notes or words of power to disrupt mind-influencing effects. As an action, you can start a performance that lasts until the end of your next turn. During that time, you and any friendly creatures within 30 feet of you have advantage on saving throws against being frightened or charmed. A creature must be able to hear you to gain this benefit. The performance ends early if you are incapacitated or silenced or if you voluntarily end it (no action required)."
      },
      {
        "name": "Bard College feature",
        "text": "At 6th level, you gain a feature from your Bard College."
      }
    ],
    [],
    [
      {
        "name": "Ability Score Improvement",
        "text": "When you reach 8th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1. As normal, you can't increase an ability score above 20 using this feature.\nIf your DM allows the use of feats, you may instead take a feat."
      }
    ],
    [
      {
        "name": "Song of Rest (d8)",
        "text": "At 9th level, the extra hit points gained from Song of Rest increases to 1d8."
      }
    ],
    [
      {
        "name": "Bardic Inspiration (d10)",
        "text": "At 10th level, your Bardic Inspiration die changes to a d10."
      },
      {
        "name": "Expertise",
        "text": "At 10th level, you can choose another two skill proficiencies. Your proficiency bonus is doubled for any ability check you make that uses either of the chosen proficiencies."
      },
      {
        "name": "Magical Secrets",
        "text": "By 10th level, you have plundered magical knowledge from a wide spectrum of disciplines. Choose two spells from any classes, including this one. A spell you choose must be of a level you can cast, as shown on the Bard table, or a cantrip.\nThe chosen spells count as bard spells for you and are included in the number in the Spells Known column of the Bard table.\nYou learn two additional spells from any classes at 14th level and again at 18th level."
      }
    ],
    [],
    [
      {
        "name": "Ability Score Improvement",
        "text": "When you reach 12th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1. As normal, you can't increase an ability score above 20 using this feature.\nIf your DM allows the use of feats, you may instead take a feat."
      }
    ],
    [
      {
        "name": "Song of Rest (d10)",
        "text": "At 13th level, the extra hit points gained from Song of Rest increases to 1d10."
      }
    ],
    [
      {
        "name": "Magical Secrets",
        "text": "At 14th level, choose two additional spells from any classes, including this one. A spell you choose must be of a level you can cast, as shown on the Bard table, or a cantrip.\nThe chosen spells count as bard spells for you and are included in the number in the Spells Known column of the Bard table."
      },
      {
        "name": "Bard College feature",
        "text": "At 14th level, you gain a feature from your Bard College."
      }
    ],
    [
      {
        "name": "Bardic Inspiration (d12)",
        "text": "At 15th level, your Bardic Inspiration die changes to a d12."
      }
    ],
    [
      {
        "name": "Ability Score Improvement",
        "text": "When you reach 16th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1. As normal, you can't increase an ability score above 20 using this feature.\nIf your DM allows the use of feats, you may instead take a feat."
      }
    ],
    [
      {
        "name": "Song of Rest (d12)",
        "text": "At 17th level, the extra hit points gained from Song of Rest increases to 1d12."
      }
    ],
    [
      {
        "name": "Magical Secrets",
        "text": "At 18th level, choose two additional spells from any class, including this one. A spell you choose must be of a level you can cast, as shown on the Bard table, or a cantrip.\nThe chosen spells count as bard spells for you and are included in the number in the Spells Known column of the Bard table."
      }
    ],
    [
      {
        "name": "Ability Score Improvement",
        "text": "When you reach 19th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1. As normal, you can't increase an ability score above 20 using this feature.\nIf your DM allows the use of feats, you may instead take a feat."
      }
    ],
    [
      {
        "name": "Superior Inspiration",
        "text": "At 20th level, when you roll initiative and have no uses of Bardic Inspiration left, you regain one use."
      }
    ]
  ],
  "subclasses": [
    {
      "name": "College of Lore",
      "levels": [
        [],
        [],
        [
          {
            "name": "Bonus Proficiencies",
            "text": "When you join the College of Lore at 3rd level, you gain proficiency with three skills of your choice."
          },
          {
            "name": "Cutting Words",
            "text": "Also at 3rd level, you learn how to use your wit to distract, confuse, and otherwise sap the confidence and competence of others. When a creature that you can see within 60 feet of you makes an attack roll, an ability check, or a damage roll, you can use your reaction to expend one of your uses of Bardic Inspiration, rolling a Bardic Inspiration die and subtracting the number rolled from the creature's roll. You can choose to use this feature after the creature makes its roll, but before the DM determines whether the attack roll or ability check succeeds or fails, or before the creature deals its damage. The creature is immune if it can't hear you or if it's immune to being charmed."
          }
        ],
        [],
        [],
        [
          {
            "name": "Additional Magical Secrets",
            "text": "At 6th level, you learn two spells of your choice from any class. A spell you choose must be of a level you can cast, as shown on the Bard table, or a cantrip. The chosen spells count as bard spells for you but don't count against the number of bard spells you know."
          }
        ],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [
          {
            "name": "Peerless Skill",
            "text": "Starting at 14th level, when you make an ability check, you can expend one use of Bardic Inspiration. Roll a Bardic Inspiration die and add the number rolled to your ability check. You can choose to do so after you roll the die for the ability check, but before the DM tells you whether you succeed or fail."
          }
        ],
        [],
        [],
        [],
        [],
        [],
        []
      ],
      "source": "PHB",
      "page": ...,
      "entity_id": ...,
      "url": ...,
      "is_free": true
    },
    ...
  ],
  "source": "PHB",
  "page": ...,
  "entity_id": ...,
  "url": ...,
  "is_free": true
}
 */