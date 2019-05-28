import yaml
from dataclasses import dataclass
from typing import Optional, List, Dict
from setting import Setting
from stats import StatBlock
from text_utils import centre_pad
from fourhills_exceptions import FourhillsFileLoadError, FourhillsSettingStructureError


@dataclass
class Npc:
    """Represents a non-player character."""

    name: str
    appearance: str
    temperament: Optional[str] = None
    accent: Optional[str] = None
    phrases: Optional[List[str]] = None
    background: Optional[str] = None
    deceased: Optional[bool] = False
    stats: Optional[Dict] = None

    def __str__(self):
        return self.formatted_string(line_width=80)

    def formatted_string(self, line_width: int = 80) -> str:
        """Return a string representation of the NPC.

        Parameters
        ----------
        line_width : int
            The width of the output, in characters.

        Returns
        -------
        str
            A string representation of the NPC.
        """
        raise NotImplementedError

    def formatted_stats_string(self, line_width: int = 80) -> str:
        """Return a string representation of the NPC's stats.

        Parameters
        ----------
        line_width : int
            The width of the output, in characters.

        Returns
        -------
        str
            A string representation of the NPC's stats.
        """
        lines = []
        lines.append(centre_pad(self.name.capitalize(), line_width))
        lines.append("=" * line_width)
        if self.stats:
            lines.append(self.stats.formatted_string(line_width, include_header=False))
        else:
            lines.append("This NPC has no stats defined")
        return "\n".join(lines)

    @classmethod
    def from_name(cls, name: str, setting: Setting):
        """Create an Npc by looking it up in the setting.

        Parameters
        ----------
        name: str
            The name of the NPC. Must exactly match a filename in the setting's
            `npcs` folder, excluding the extension.
        setting: Setting
            The Setting object; this is used to find the setting root and
            subdirectories.
        """
        # Suspected path of the NPC file
        npc_file = setting.npcs_dir / (name + ".yaml")
        if not npc_file.is_file():
            raise FourhillsSettingStructureError(f"NPC file {npc_file} does not exist.")
        with open(npc_file) as f:
            try:
                npc_dict = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise FourhillsFileLoadError(f"Error loading from {npc_file}.") from exc

            if "stats_base" in npc_dict:
                stats = StatBlock.from_name(npc_dict["stats_base"], setting)

            if "stats" in npc_dict:
                pass
                #raise NotImplementedError

            npc = cls(
                **{
                    key: value
                    for key, value in npc_dict.items()
                    if key not in ["stats_base", "stats"]
                }
            )
            npc.stats = stats

            return npc
