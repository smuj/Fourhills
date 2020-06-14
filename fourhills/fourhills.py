import sys
import re
import yaml
from typing import List, Tuple
from fourhills import Setting, StatBlock, Npc
from fourhills.exceptions import FourhillsFileLoadError
from fourhills.text_utils import display_panes, title

SCENE_FILENAME = "scene.yaml"


class Scene:
    """Represents a particular location in the world."""

    def __init__(
        self, monster_names_quantities: List[Tuple[str, int]], npc_names: List[str]
    ):
        """Initialise the object."""
        self.monster_names_quantities = monster_names_quantities
        self.npc_names = npc_names
        self.setting = Setting()

    @classmethod
    def from_file(cls, filename: str):
        """Load scene info from a file and return a Scene instance.

        Parameters
        ----------
        filename : str
            Filename of the YAML file to load scene info from.
        """
        with open(filename) as f:
            try:
                scene_info = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise FourhillsFileLoadError(f"Error loading from {filename}.") from exc

            # Stores the list of monster names and numbers
            monster_info = []

            # If there was a monsters section, load the monsters
            if "monsters" in scene_info:
                for monster_name_number in scene_info["monsters"]:
                    # See if it matches the expected format, extracting name and number
                    match = re.match(r"^(\w*)(?: ?x?(\d+))?$", monster_name_number)
                    if not match:
                        raise FourhillsFileLoadError(
                            "Error parsing monster in scene file"
                        )
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
            npc_info = scene_info["npcs"] if "npcs" in scene_info else []

            return cls(monster_info, npc_info)

    def display_battle(self):
        """Display statistsics for battle."""
        panes = list()

        for monster_name, quantity in self.monster_names_quantities:
            monster = StatBlock.from_name(monster_name, self.setting)
            panes.append(
                monster.summary_info(self.setting.pane_width, quantity)
                + monster.battle_info(self.setting.pane_width)
            )

        for npc_name in self.npc_names:
            npc = Npc.from_name(npc_name, self.setting)
            panes.append(
                npc.summary_info(self.setting.pane_width)
                + npc.battle_info(self.setting.pane_width)
            )

        display_panes(panes, self.setting.panes, self.setting.pane_width)

    def display_npcs(self):
        """Display information about NPCs."""
        panes = list()

        for npc_name in self.npc_names:
            npc = Npc.from_name(npc_name, self.setting)
            panes.append(
                npc.summary_info(self.setting.pane_width)
                + npc.character_info(self.setting.pane_width)
            )

        display_panes(panes, self.setting.panes, self.setting.pane_width)

    def display_scene(self):
        """Display information about location."""
        panes = list()

        # List of all of the monsters at the location, and the quantities of each
        monsters_quantities = (
            [
                (StatBlock.from_name(monster_name, self.setting), quantity)
                for monster_name, quantity in self.monster_names_quantities
            ]
            if self.monster_names_quantities
            else []
        )

        # List of all of the NPCs at the location
        npcs = (
            [Npc.from_name(npc_name, self.setting) for npc_name in self.npc_names]
            if self.npc_names
            else []
        )

        # If there are monsters, create a pane of text displaying them
        if monsters_quantities:
            monster_lines = title("Monsters", self.setting.pane_width)
            for monster, quantity in monsters_quantities:
                monster_lines.append(
                    f"{monster.name} x{quantity}" if quantity != 1 else monster.name
                )
            panes.append(monster_lines)

        # If there are NPCs, create a pane of text displaying them
        if npcs:
            npc_lines = title("NPCs", self.setting.pane_width)
            for npc in npcs:
                npc_lines.append(npc.name)
            panes.append(npc_lines)

        # Calculate the total monster and NPC XP
        monster_xp = sum(
            quantity * monster.xp for monster, quantity in monsters_quantities
        )
        npc_xp = sum(npc.stats.xp if npc.stats else 0 for npc in npcs)

        xp_lines = title("XP", self.setting.pane_width)
        xp_lines.append("Total monster XP = " + str(monster_xp))
        xp_lines.append("Total NPC XP = " + str(npc_xp))
        xp_lines.append("Total XP = " + str(monster_xp + npc_xp))
        panes.append(xp_lines)

        display_panes(panes, self.setting.panes, self.setting.pane_width)


def print_usage():
    raise NotImplementedError


def main():
    try:
        scene = Scene.from_file(SCENE_FILENAME)
    except FileNotFoundError:
        print("No scene file at this location")
        sys.exit()
    if len(sys.argv) > 1:
        if sys.argv[1] in ["b", "battle"]:
            scene.display_battle()
        elif sys.argv[1] in ["n", "npc", "npcs"]:
            scene.display_npcs()
        elif sys.argv[1] in ["s", "scene"]:
            scene.display_scene()
        else:
            print_usage()
    else:
        scene.display_scene()


if __name__ == "__main__":
    main()
