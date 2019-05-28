import sys
import re
import yaml
import click
from typing import Optional, List, Tuple
from setting import Setting
from stats import StatBlock
from npc import Npc
from fourhills_exceptions import FourhillsFileLoadError, FourhillsSettingStructureError

BATTLE_FILENAME = "battle.yaml"


def load_battle_info(filename: str) -> Tuple[List[Tuple[str, int]], List[str]]:
    """Load info about a battle from a file and return the details.

    Parameters
    ----------
    filename : str
        Filename of the YAML file to load battle info from.

    Returns
    -------
    list of (str, int)
        List of monster names and the number of each
    """
    with open(filename) as f:
        try:
            battle_info = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            raise FourhillsFileLoadError(f"Error loading from {filename}.") from exc

        # Stores the list of monster names and numbers
        monster_info = []

        # If there was a monsters section, load the monsters
        if "monsters" in battle_info:
            for monster_name_number in battle_info["monsters"]:
                # See if it matches the expected format, extracting name and number
                match = re.match(r"^(\w*)(?: ?x?(\d+))?$", monster_name_number)
                if not match:
                    raise FourhillsFileLoadError("Error parsing monster in battle file")
                # Get the name of the monster and how many there are. If there
                # wasn't a number, assume 1 monster.
                name = match[1]
                number = match[2] or "1"
                # Convert to int
                try:
                    number = int(number)
                except ValueError as exc:
                    raise FourhillsFileLoadError(
                        f"Error parsing number for monster {name}"
                    ) from exc
                # Add to the list
                monster_info.append((name, number))

        # Stores the list of NPC names
        npc_info = battle_info["npcs"] or []

        return monster_info, npc_info


def battle():

    setting = Setting()

    try:
        monster_info, npc_info = load_battle_info(BATTLE_FILENAME)
    except FileNotFoundError:
        raise FourhillsSettingStructureError(
            f"No '{BATTLE_FILENAME}' battle file found."
        )

    stat_strings = [
        StatBlock.from_name(monster_name, setting).formatted_string(
            line_width=56, quantity=quantity
        )
        for monster_name, quantity in monster_info
    ]
    stat_strings.extend(
        [
            Npc.from_name(npc_name, setting).formatted_stats_string(line_width=56)
            for npc_name in npc_info
        ]
    )
    click.echo_via_pager("\n".join(stat_strings))


def print_usage():
    raise NotImplementedError


def print_location():
    raise NotImplementedError


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ["b", "battle"]:
            battle()
        else:
            print_usage()
    else:
        print_location()


if __name__ == "__main__":
    main()
