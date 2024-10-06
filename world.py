from town import Town
from npc import NPC
import inspect

class World:
    
    @property
    def towns(self) -> list[Town]:
        return self._towns
    
    @property
    def npcs(self) -> list[NPC]:
        return self._npcs
    
    def __init__(self, npcs: list[NPC]):
        self._towns = []
        self._npcs = npcs

    def __init__(self, npcs: list[NPC], towns: list[Town]):
        self._towns = towns
        self._npcs = npcs

    def add_town(self, town: Town) -> None:
        self.towns.append(town)

    def settle_npcs(self, unsorted_npcs=None) -> None:
        """
        This method will sort and settle npcs into ideal housing situations as to maximize
        their happiness and the happiness of the town.
        """
        if unsorted_npcs is None:
            unsorted_npcs = self.npcs

        # Check recursion depth
        def get_recursion_depth():
            frame = inspect.currentframe()
            depth = 0
            while frame:
                frame = frame.f_back
                depth += 1
            initial_depth = 3
            return depth - initial_depth

        # Phase 1 initial sort
        for npc in unsorted_npcs:
            town_happiness_delta = {}

            for town in self.towns:
                town_happ_with_npc, _residents_effects = town.calc_avg_multiplier(npc)
                town_happiness_delta[town] = town.avg_multiplier - town_happ_with_npc

            best_town = max(town_happiness_delta, key=town_happiness_delta.get)

            best_town.add_resident(npc)

        print(f"Sort {get_recursion_depth()}:")
        print(self)
        
        # Phase 2 check and re-sort
        if get_recursion_depth() < 10:  # Maybe make this dynamic with "tries"
            reevaluations = []
            for town in self.towns:
                for resident in town.residents:
                    if resident.happiness > 1:
                        town.remove_resident(resident)
                        reevaluations.append(resident)

            if reevaluations:
                self.settle_npcs(reevaluations)

    def __str__(self) -> str:
        final_str = ""
        for town in self.towns:
            final_str += f"{town.location.name}: {town.state}\n"
            for resident in town.residents:
                final_str += f"\t{resident.name}: {resident.happiness}\n"

        return final_str
