import re
import yaml
from typing import List, Tuple, Optional
from fourhills import Setting
from fourhills.exceptions import FhParseError
from fourhills.text_utils import display_panes, title


class Scene:
    """Represents a particular location in the world."""

    def __init__(
        self,
        monster_names_quantities: List[Tuple[str, int]],
        npc_names: List[str],
        setting: Optional[Setting] = None,
    ):
        """Initialise the object.

        Parameters
        ----------
        monster_names_quantities: list of tuples of str, int
            A list of the monster names (as strings) and the quantity of each.
        npc_names: list of str
            A list of the NPC names (as strings).
        setting : Setting or None
            The setting the scene belongs to. If None, one will be generated.
        """
        self.monster_names_quantities = monster_names_quantities
        self.npc_names = npc_names
        self.setting = setting or Setting()

    @classmethod
    def from_file(cls, filename: str, setting: Optional[Setting] = None):
        """Load scene info from a file and return a Scene instance.

        Parameters
        ----------
        filename : str
            Filename of the YAML file to load scene info from.
        setting : Setting or None
            The setting the scene belongs to. If None, one will be generated.

        Raises
        ------
        FhParseError
            If there is an error parsing the file.
        """
        with open(filename) as f:
            try:
                scene_info = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise FhParseError(f"Error parsing YAML for scene: {str(exc)}")

            # Stores the list of monster names and numbers
            monster_info = []

            # If there was a monsters section, load the monsters
            if "monsters" in scene_info:
                for monster_name_number in scene_info["monsters"]:
                    # See if it matches the expected format, extracting name and number
                    match = re.match(r"^(\w*)(?: ?x?(\d+))?$", monster_name_number)
                    if not match:
                        raise FhParseError(
                            f'Error parsing "{monster_name_number}": could not split '
                            "into a monster name and (optional) quantity."
                        )
                    # Get the name of the monster and how many there are. If there
                    # wasn't a number, assume 1 monster.
                    name = match[1]
                    number = match[2] or "1"
                    # Convert to int
                    try:
                        number = int(number)
                    except ValueError as exc:
                        raise FhParseError(
                            f'Error parsing quantity "{number}" of monster "{name}" '
                            'into an integer.'
                        ) from exc
                    # Add to the list
                    monster_info.append((name, number))

            # Stores the list of NPC names
            npc_info = scene_info["npcs"] if "npcs" in scene_info else []

            return cls(monster_info, npc_info, setting)

    def display_battle(self):
        """Display statistsics for battle."""
        panes = list()

        for monster_name, quantity in self.monster_names_quantities:
            monster = self.setting.monsters[monster_name]
            panes.append(
                monster.summary_info(self.setting.pane_width, quantity)
                + monster.battle_info(self.setting.pane_width)
            )

        for npc_name in self.npc_names:
            npc = self.setting.npcs[npc_name]
            panes.append(
                npc.summary_info(self.setting.pane_width)
                + npc.battle_info(self.setting.pane_width)
            )

        display_panes(panes, self.setting.panes, self.setting.pane_width)

    def display_npcs(self):
        """Display information about NPCs."""
        panes = list()

        for npc_name in self.npc_names:
            npc = self.setting.npcs[npc_name]
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
                (self.setting.monsters[monster_name], quantity)
                for monster_name, quantity in self.monster_names_quantities
            ]
            if self.monster_names_quantities
            else []
        )

        # List of all of the NPCs at the location
        npcs = (
            [self.setting.npcs[npc_name] for npc_name in self.npc_names]
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
