import math
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, List
from fourhills.text_utils import (
    format_indented_paragraph,
    format_list,
    centre_pad,
    title,
)
from fourhills.exceptions import FhParseError, FhConfigError


@dataclass
class StatBlock:
    """The stat block for a monster or character."""

    # Each formatted ability stat needs 2 characters for the score, 3 for the modifier
    # (including sign), 2 for the brackets around the modifier, and 2 for the minimum
    # number of spaces on either side. There are 6 ability stats, so if each needs 9
    # characters in total, there must be an allowed width of at least 56.
    MINIMUM_TERMINAL_WIDTH = 56

    name: str
    size: str
    creature_type: str
    alignment: str
    ac: str
    hp: str
    speed: str
    ability: Dict[str, int]
    challenge: float
    passive_perception: int
    saving_throws: Optional[Dict[str, str]] = None
    skills: Optional[Dict[str, str]] = None
    damage_vulnerabilities: Optional[List[str]] = None
    damage_resistances: Optional[List[str]] = None
    damage_immunities: Optional[List[str]] = None
    condition_immunities: Optional[List[str]] = None
    special_senses: Optional[Dict[str, str]] = None
    languages: Optional[List[str]] = None
    special_traits: Optional[Dict[str, str]] = None
    melee_attacks: Optional[Dict[str, Dict[str, str]]] = None
    ranged_attacks: Optional[Dict[str, Dict[str, str]]] = None
    multiattack: Optional[str] = None
    other_actions: Optional[Dict[str, str]] = None
    description: Optional[str] = None

    def __str__(self):
        return self.summary_info(line_width=80)

    @property
    def xp(self):
        """The experience points of the monster.

        Returns
        -------
        int
            The number of XP.

        Raises
        ------
        FhParseError
            If the challenge rating is invalid.
        """
        xp_table = {
            0: 0,
            0.125: 25,
            0.25: 50,
            0.5: 100,
            1: 200,
            2: 450,
            3: 700,
            4: 1100,
            5: 1800,
            6: 2300,
            7: 2900,
            8: 3900,
            9: 5000,
            10: 5900,
            11: 7200,
            12: 8400,
            13: 10000,
            14: 11500,
            15: 13000,
            16: 15000,
            17: 18000,
            18: 20000,
            19: 22000,
            20: 25000,
            21: 33000,
            22: 41000,
            23: 50000,
            24: 62000,
            25: 75000,
            26: 90000,
            27: 105000,
            28: 120000,
            29: 135000,
            30: 155000,
        }
        try:
            return xp_table[self.challenge]
        except KeyError:
            raise FhParseError(
                f'StatBlock "{self.name}" has invalid challenge rating '
                f'"{self.challenge}". Challenge rating must be either 0.125, 0.25 or '
                "0.5, or an integer between 0 and 30."
            )

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

    def summary_info(
        self, line_width: int = 80, quantity: Optional[int] = None
    ) -> List[str]:
        """Return a list of lines summarising the stat block.

        Parameters
        ----------
        line_width : int
            The width of the output, in characters.
        quantity : int or None
            If an int, it will be shown as in the header as a quantity e.g. "Lion x3".
            If None, just the name will be shown e.g. "Lion".

        Returns
        -------
        list of str
            A summary of the stat block as a list of lines.
        """
        lines = title(
            f"{self.name} x{quantity:d}" if quantity else self.name, line_width
        )

        # Size, type and alignment
        lines.append(f"{self.size.capitalize()} {self.creature_type}, {self.alignment}")

        return lines

    def battle_info(self, line_width: int = 80) -> List[str]:
        """Return the battle info for the stat block as a list of lines.

        Parameters
        ----------
        line_width : int
            The width of the output, in characters.

        Returns
        -------
        list of str
            A representation of the stat block as a list of lines.

        Raises
        ------
        FhConfigError
            If there isn't enough room to display the info.
        """

        if line_width < self.MINIMUM_TERMINAL_WIDTH:
            raise FhConfigError(
                f"Pane width must be at least {self.MINIMUM_TERMINAL_WIDTH} for there "
                "to be room for all scores."
            )

        # List to hold the lines of the output.
        lines = list()

        # AC, HP, speed
        lines.append(f"AC {self.ac}")
        lines.append(f"HP {self.hp}")
        lines.append(f"Speed {self.speed}")

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
        lines.append(centre_pad("".join(ability_name_strings), line_width))
        lines.append(centre_pad("".join(ability_score_strings), line_width))

        # Separator
        lines.append("-" * line_width)

        # Saving throws
        if self.saving_throws:
            throws = [f"{throw} {value}" for throw, value in self.saving_throws.items()]
            lines.extend(format_list("Saving throws", throws, line_width))
        # Skills
        if self.skills:
            skill_list = [f"{skill} {value}" for skill, value in self.skills.items()]
            lines.extend(format_list("Skills", skill_list, line_width))
        # Vulnerabilities
        if self.damage_vulnerabilities:
            lines.extend(
                format_list(
                    "Damage vulnerabilities", self.damage_vulnerabilities, line_width
                )
            )
        # Resistances
        if self.damage_resistances:
            lines.extend(
                format_list("Damage resistances", self.damage_resistances, line_width)
            )
        # Immunities
        if self.damage_immunities:
            lines.extend(
                format_list("Damage immunities", self.damage_immunities, line_width)
            )
        if self.condition_immunities:
            lines.extend(
                format_list(
                    "Condition immunities", self.condition_immunities, line_width
                )
            )
        # Passive perception
        lines.append(f"Passive perception: {self.passive_perception}")
        # Senses
        if self.special_senses:
            senses = [
                f"{sense} {value}" for sense, value in self.special_senses.items()
            ]
            lines.extend(format_list("Senses", senses, line_width))
        # Languages
        lines.extend(format_list("Languages", self.languages or ["none"], line_width))

        # Challenge rating
        lines.append(f"Challenge: {self.challenge} ({self.xp} XP)")

        # Separator
        lines.append("")
        lines.append(centre_pad("Special traits", line_width))
        lines.append("-" * line_width)

        if self.special_traits:
            for name, text in self.special_traits.items():
                lines.extend(
                    format_indented_paragraph(
                        f"{name.capitalize()}: {text}", line_width
                    )
                )

        # Separator and title
        lines.append("")
        lines.append(centre_pad("Actions", line_width))
        lines.append("-" * line_width)

        # Melee attacks
        if self.melee_attacks:
            for name, details in self.melee_attacks.items():
                details_formatted = (
                    f"{name.capitalize()}: melee weapon attack, "
                    f"{details['hit']} to hit, reach {details['reach']}, "
                    f"{details['targets']}. "
                    f"Hit damage: {details['damage']}."
                )
                if "info" in details:
                    details_formatted += f" {details['info']}."
                lines.extend(format_indented_paragraph(details_formatted, line_width))

        # Ranged attacks
        if self.ranged_attacks:
            for name, details in self.ranged_attacks.items():
                details_formatted = (
                    f"{name.capitalize()}: ranged weapon attack, "
                    f"{details['hit']} to hit, range {details['range']},"
                    f"{details['targets']}. "
                    f"Hit damage: {details['damage']}."
                )
                if "info" in details:
                    details_formatted += f" {details['info']}."
                lines.extend(format_indented_paragraph(details_formatted, line_width))

        if self.multiattack:
            lines.extend(
                format_indented_paragraph(
                    f"Multiattack: {self.multiattack}", line_width
                )
            )

        # Other actions
        if self.other_actions:
            for name, text in self.other_actions.items():
                action_formatted = f"{name.capitalize()}: {text}"
                lines.extend(format_indented_paragraph(action_formatted, line_width))

        lines.append("")

        if self.description:
            lines.extend(format_indented_paragraph(self.description, line_width))

        return lines

    @classmethod
    def from_file(cls, filepath: Path):
        """Create a StatBlock from a YAML file.

        Parameters
        ----------
        filename: Path
            Path to the YAML file

        Raises
        ------
        FhParseError
            If there is an error parsing the file.
        """
        with open(filepath) as f:
            try:
                stat_dict = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise FhParseError(
                    f'Error parsing YAML for stat block "{filepath.stem}": {str(exc)}'
                )

            return cls(**stat_dict)
