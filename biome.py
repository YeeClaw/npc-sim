class Biome:

    @property
    def name(self) -> str:
        return self._name
    
    def __init__(self, name: str):
        self._name = name
