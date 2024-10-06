from npc import NPC
from biome import Biome
from town_state import TownState

class Town:

    @property
    def residents(self) -> list[NPC]:
        return self._residents
    
    @property
    def location(self) -> Biome:
        return self._location
    
    @property
    def avg_multiplier(self) -> float:
        return self._avg_multiplier
    
    @avg_multiplier.setter
    def avg_multiplier(self, value: float) -> None:
        self._avg_multiplier = value

    @property
    def state(self) -> str:
        if self.avg_multiplier < 1:
            return TownState.HAPPY
        elif self.avg_multiplier == 1:
            return TownState.NEUTRAL
        else:
            return TownState.UNHAPPY
        

    def __init__(self, location: Biome):
        self._residents = []
        self._avg_multiplier = 1.0
        self._location = location


    def add_resident(self, resident: NPC) -> None:
        self.residents.append(resident)
        self.avg_multiplier, resident_happiness = self.calc_avg_multiplier()
        for npc, multiplier in resident_happiness.items():
            npc.happiness = multiplier

    
    def remove_resident(self, resident: NPC) -> None:
        self.residents.remove(resident)
        self.avg_multiplier, resident_happiness = self.calc_avg_multiplier()
        for npc, multiplier in resident_happiness.items():
            npc.happiness = multiplier


    def calc_avg_multiplier(self, potential_npc: NPC = None) -> float:
        # TODO: DRY violated. This smells!
        if potential_npc:
            calc_residents = self.residents + [potential_npc]
        else:
            calc_residents = self.residents

        if not calc_residents:
            return 1.0
        
        # Loves, Likes, Dislikes, Hates
        mood_multipliers = [0.88, 0.94, 1.06, 1.12]
        
        # Calculate the multiplier for each resident
        total_multiplier = 0.0
        individual_multipliers = {}

        for resident in calc_residents:
            resident_multiplier = 1.0
            # Find resident multiplier due to other residents
            for i, affinity in enumerate(resident.relationship_preferences):
                resident_multiplier *= self.calc_relation_multiplier(resident, affinity, mood_multipliers[i])

            # Find resident multiplier due to biome preferences
            for i, affinity in enumerate(resident.biome_preferences):
                resident_multiplier *= self.calc_biome_multiplier(resident, affinity, mood_multipliers[i])

            # Apply the crowding/solitude bonus
            if len(calc_residents) <= 3:
                resident_multiplier *= 0.95
            else:
                resident_multiplier *= 1.05

            # Clamp the multiplier to 0.75 as per the Terraria wiki
            if resident_multiplier < 0.75:
                resident_multiplier = 0.75

            resident_multiplier = round(resident_multiplier, 2)
            individual_multipliers[resident] = resident_multiplier
            total_multiplier += resident_multiplier

        final_avg = total_multiplier / len(calc_residents)
        return round(final_avg, 3), individual_multipliers  # Final multipliers are rounded to 2 decimal places


    def calc_relation_multiplier(self, resident: NPC, affinity: str, multiplier: float) -> float:
        final_multiplier = 1.0
        for related_npc in resident.relationship_preferences[affinity].values():
            if related_npc in self.residents:
                final_multiplier *= multiplier

        return final_multiplier
    

    def calc_biome_multiplier(self, resident: NPC, affinity: str, multiplier: float) -> float:
        final_multiplier = 1.0
        for related_biome in resident.biome_preferences[affinity].values():
            if related_biome == self.location:
                final_multiplier *= multiplier

        return final_multiplier
