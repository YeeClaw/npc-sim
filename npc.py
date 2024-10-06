from biome import Biome
import copy

class NPC:

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def biome_preferences(self) -> dict[str, dict[str, object]]:
        """
        {opinion: {biome_name: biome_object}}
        """
        return self._biome_preferences
    
    @property
    def relationship_preferences(self) -> dict[str, dict[str, object]]:
        """
        {opinion: {npc_name: npc_object}}
        """
        return self._relationship_preferences

    def __init__(self, name: str):
        self._name = name

        self._base_preferences = {
            "Loves": {},
            "Likes": {},
            "Dislikes": {},
            "Hates": {}
        }
        self._biome_preferences = copy.deepcopy(self._base_preferences)
        self._relationship_preferences = copy.deepcopy(self._base_preferences)

    def add_preference(self, opinion: str, preferred_thing: object) -> None:
        if opinion == "Neutral":
            return

        if isinstance(preferred_thing, Biome):
            self._biome_preferences[opinion][preferred_thing.name] = preferred_thing
        elif isinstance(preferred_thing, NPC):
            self._relationship_preferences[opinion][preferred_thing.name] = preferred_thing
        else:
            raise TypeError(f"Unsupported type: {type(preferred_thing)}")
        
    def get_opinions(self) -> list[str]:
        opinions = {}
        for preference_type in self._base_preferences:
            opinions[preference_type] = self._biome_preferences[preference_type] | self._relationship_preferences[preference_type]

        return opinions
