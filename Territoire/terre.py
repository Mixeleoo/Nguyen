
from dataclasses import dataclass
from typing import Literal


@dataclass
class Terre:
    type: Literal["PLAIN", "MOUNTAIN", "LAKE", "FOREST"]
    nb_roturiers: int = 0