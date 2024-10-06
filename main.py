from npc import NPC
from biome import Biome
from town_state import TownState
from town import Town


def parse_csv(npc_path: str, biome_path: str = None) -> dict[str, NPC]:
    with open(npc_path, 'r') as file:
        npc_lines = file.readlines()

    # Parse the header
    affiliated_npcs = npc_lines[0].strip().split(',')
    affiliated_npcs.pop(0)  # Remove the "NPCs" header

    # Parse the data rows
    npc_dict = {}
    for line in npc_lines[1:]:
        data = line.strip().split(',')
        npc_name = data[0]

        # Ensure that only one instance of each NPC is created
        if npc_name not in npc_dict:
            npc_dict[npc_name] = NPC(npc_name)

        for i, affiliate_npc in enumerate(affiliated_npcs):
            i += 1
            
            if affiliate_npc not in npc_dict:
                npc_dict[affiliate_npc] = NPC(affiliate_npc)

            npc_dict[npc_name].add_preference(data[i].capitalize(), npc_dict[affiliate_npc])

    # Parse the biomes
    if biome_path:
        with open(biome_path, 'r') as file:
            biome_lines = file.readlines()

        # Parse the header
        biomes = biome_lines[0].strip().split(',')
        biomes.pop(0) # Remove the "Biomes" header

        # Parse the data rows
        for line in biome_lines[1:]:
            data = line.strip().split(',')
            for i, biome in enumerate(biomes):
                i += 1
                npc_dict[data[0]].add_preference(data[i].capitalize(), Biome(biome))
    else:
        print("No biome data provided!")

    return npc_dict


def check_data(npc_list: dict[str, NPC]) -> None:
    # Data integrity checks!
    overall_pass = True
    for npc in npc_list:
        npc_opinions = npc_list[npc].get_opinions()
        if not npc_opinions["Loves"] and npc_opinions["Likes"].keys() == ["Princess"] and not npc_opinions["Dislikes"] and not npc_opinions["Hates"]:
            overall_pass = False
            print(f"NPC {npc} has missing opinions!")

        opinion_objects = []
        for opinion in npc_opinions:
            opinion_objects.extend(npc_opinions[opinion].values())

        no_biomes = True
        for opinion_object in opinion_objects:
            if isinstance(opinion_object, Biome) or npc == "Princess":
                no_biomes = False
                break

        if no_biomes:
            overall_pass = False
            print(f"NPC {npc} has no biome preferences!")
        
    if overall_pass:
        print("All data checks passed!")


def main():
    # npc_dict_no_biomes = parse_csv("data/npc_relationships.csv")
    npc_dict_with_biomes = parse_csv("data/npc_relationships.csv", "data/npc_biomes.csv")
    # check_data(npc_dict_no_biomes)
    check_data(npc_dict_with_biomes)
    # print(npc_dict_with_biomes)

    # Random testing
    town = Town()
    town.add_resident(npc_dict_with_biomes["Guide"])
    town.add_resident(npc_dict_with_biomes["Merchant"])
    town.add_resident(npc_dict_with_biomes["Nurse"])

    print(town.avg_multiplier)
    print(town.state)


if __name__ == "__main__":
    main()
