from typing import List, Dict, Optional


class Setup:
    def __init__(self, name: str, steps: List[str]):
        self.name = name
        self.steps = steps