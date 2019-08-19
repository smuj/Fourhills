"""Simple enumeration from each pane handling a tab control"""

from enum import Enum


class TabResult(Enum):
    TabConsumed = 1  # Tab has been fully handled
    TabRemaining = 2  # Tab has not been handled and must be passed on
