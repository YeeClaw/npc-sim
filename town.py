from npc import NPC
from town_state import TownState

class Town:

    @property
    def residents(self) -> list[NPC]:
        return self._residents
    
    @property
    def avg_multiplier(self) -> float:
        return self._avg_multiplier

    @property
    def state(self) -> str:
        if self.avg_multiplier < 1:
            return TownState.HAPPY
        elif self.avg_multiplier == 1:
            return TownState.NEUTRAL
        else:
            return TownState.UNHAPPY
        
    def __init__(self):
        self._residents = []
        self._avg_multiplier = 1.0

    def add_resident(self, resident: NPC) -> None:
        self._residents.append(resident)
        self._avg_multiplier = self.calc_avg_multiplier()

    def calc_avg_multiplier(self) -> float:
        if not self.residents:
            return 1.0
        
                        # Loves, Likes, Dislikes, Hates
        mood_multipliers = [0.88, 0.94, 1.06, 1.12]
        
        # Calculate the multiplier for each resident
        total_multiplier = 0.0
        for resident in self.residents:
            # Calculate the multiplier for each individual resident
            resident_multiplier = 1.0
            for i, affinity in enumerate(resident.relationship_preferences):
                resident_multiplier *= self.calc_multiplier(resident, affinity, mood_multipliers[i])

            total_multiplier += resident_multiplier

        final_avg = total_multiplier / len(self.residents)
        return final_avg

    def calc_multiplier(self, resident: NPC, affinity: str, multiplier: float) -> float:
        final_multiplier = 1.0
        for related_npc in resident.relationship_preferences[affinity].values():
            if related_npc in self.residents:
                final_multiplier *= multiplier

        if final_multiplier < 0.75:
            final_multiplier = 0.75  # Clamp the multiplier to 0.75 as per the Terraria wiki

        return final_multiplier
