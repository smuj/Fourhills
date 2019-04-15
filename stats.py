import math
from dataclasses import dataclass
from typing import Optional
import yaml


class StatsException(RuntimeError):
    pass


class StatsLoadException(StatsException):
    pass


@dataclass
class StatBlock:
    """The stat block for a monster or character."""

    name: str
    size: str
    creature_type: str
    alignment: str
    ac: int
    hp: str
    speed: str
    challenge: int
    ability: dict
    passive_perception: int
    actions: list
    saving_throws: Optional[list] = None
    skills: Optional[dict] = None
    vulnerabilities: Optional[list] = None
    resistances: Optional[list] = None
    immunities: Optional[list] = None
    proficiencies: Optional[list] = None
    languages: Optional[list] = None
    special_traits: Optional[dict] = None
    reactions: Optional[list] = None

    def __str__(self):
        return self.formatted_string(line_width=80)

    @staticmethod
    def calculate_ability_modifier(ability_score: int) -> int:
        """Calculate the ability modifier from an ability score.

        Parameters
        ----------
        ability_score : int
            The ability score to calculate the modifier for.
        
        Returns
        -------
        int
            The ability modifier.
        """
        return math.floor((ability_score - 10) / 2)

    def formatted_string(self, line_width: int = 80) -> str:
        """Return a string representation of the stat block.

        Parameters
        ----------
        line_width : int
            The width of the output, in characters.
        
        Returns
        -------
        str
            A string representation of the stat block.
        """
        # Each formatted ability stat needs 2 characters for the score, 3 for the
        # modifier (including sign), 2 for the brackets around the modifier, and
        # 2 for the minimum number of spaces on either side. There are 6 ability
        # stats, so if each needs 9 characters in total, there must be an allowed
        # width of at least 56.
        if line_width < 56:
            raise ValueError(
                "Width must be at least 56 in order for there to be room for all scores."
            )

        # Function to pad a string with spaces, centre-aligned
        def centre_pad(s, width=line_width):
            return "{:^{width}}".format(s, width=width)

        # List to hold the lines of the output
        lines = list()

        # Header
        lines.append(centre_pad(self.name.capitalize()))
        lines.append("=" * line_width)

        # Description
        lines.append(f"{self.size.capitalize()} {self.creature_type}, {self.alignment}")

        # AC, HP, speed and challenge
        lines.append(f"AC {self.ac}")
        lines.append(f"HP {self.hp}")
        lines.append(f"Speed {self.speed}")
        lines.append(f"Challenge {self.challenge}")

        # Separator
        lines.append("-" * line_width)

        # Abilities
        ability_width = math.floor(line_width / len(self.ability))
        # Lists to hold the name and score strings for the abilities
        ability_name_strings = list()
        ability_score_strings = list()
        # Go through the abilities, generating padded strings for the name and score
        for ability, score in self.ability.items():
            # Add the name to the list of names
            ability_name_strings.append(centre_pad(ability, ability_width))
            # Calculate the ability modifier
            modifier = self.calculate_ability_modifier(score)
            # Add the score and modifier to the list of scores
            ability_score_strings.append(
                centre_pad(f"{score:d}({modifier:+d})", ability_width)
            )
        # Join the names and scores into one line each, and centre and pad for the whole
        # line width, before appending to the list
        lines.append(centre_pad("".join(ability_name_strings)))
        lines.append(centre_pad("".join(ability_score_strings)))

        # Separator
        lines.append("-" * line_width)

        return "\n".join(lines)

    @classmethod
    def from_file(cls, filename):
        """Create a StatBlock from a YAML file.

        Parameters
        ----------
        filename: str
            Path to the YAML file
        """
        with open(filename) as f:
            try:
                stat_dict = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise StatsLoadException(f"Error loading from {filename}.") from exc

            stats = StatBlock(**stat_dict)
            print(stats.formatted_string(56))


s = StatBlock.from_file("Monsters/lion.yaml")

