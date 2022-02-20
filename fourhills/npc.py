import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Dict
from fourhills.exceptions import FhParseError
from fourhills.text_utils import wrap_lines_paragraph, title


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
        return self.summary_info(line_width=80)

    def summary_info(self, line_width: int = 80) -> List[str]:
        """Return a list of lines summarising the NPC.

        Parameters
        ----------
        line_width : int
            The width of the output, in characters.

        Returns
        -------
        list of str
            A summary of the NPC block as a list of lines.
        """
        lines = title(
            f"{self.name} (deceased)" if self.deceased else self.name, line_width
        )

        if self.stats:
            # Size, type and alignment
            lines.append(
                f"{self.stats.alignment.capitalize()} {self.stats.name} "
                f"({self.stats.size.capitalize()} {self.stats.creature_type})"
            )

        return wrap_lines_paragraph(lines, line_width)

    def battle_info(self, line_width: int = 80) -> List[str]:
        """Return a list of lines detailing the NPC's stats.

        Parameters
        ----------
        line_width : int
            The width of the output, in characters.

        Returns
        -------
        list of str
            A representation of the NPC's stats as a list of lines.
        """
        if self.stats:
            return self.stats.battle_info(line_width)
        else:
            return ["This NPC has no stats defined"]

    def character_info(self, line_width: int = 80) -> List[str]:
        """Return a list of lines describing the NPC.

        Parameters
        ----------
        line_width : int
            The width of the output, in characters.

        Returns
        -------
        list of str
            A representation of the NPC as a list of lines.
        """
        lines = []
        lines.append(f"Appearance: {self.appearance}")
        if self.accent:
            lines.append(f"Accent: {self.accent}")

        if self.temperament or self.background:
            lines.append(" ".join([self.temperament or "", self.background or ""]))

        if self.phrases:
            lines.append("")
            lines.append("Phrases:")
            for phrase in self.phrases:
                lines.append(f"- {phrase}")

        return wrap_lines_paragraph(lines, line_width)

    @classmethod
    def from_file(cls, filepath: Path, setting):
        """Create a Npc from a YAML file.

        Parameters
        ----------
        filename: Path
            Path to the YAML file
        setting: Setting
            The Setting object; this is used to find any stats as defined by the
            stats_base key

        Raises
        ------
        FhParseError
            If there is an error parsing the file.
        """
        with open(filepath) as f:
            try:
                npc_dict = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise FhParseError(
                    f'Error parsing YAML in NPC "{filepath.stem}": {str(exc)}'
                )

            if "stats_base" in npc_dict:
                stats = setting.monsters[npc_dict["stats_base"]]
            else:
                stats = None

            if "stats" in npc_dict:
                raise NotImplementedError

            npc = cls(
                **{
                    key: value
                    for key, value in npc_dict.items()
                    if key not in ["stats_base", "stats"]
                }
            )
            npc.stats = stats

            return npc
