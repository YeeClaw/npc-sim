def optimize_housing(npc_list: list[NPC], biomes: list[str]) -> dict:
    # NOTE: Princess HATES being lonely!
    optimal_housing = {"Not sorted": []}
    for npc in npc_list:
        loved_biomes = npc.get_loved_biomes(biomes)
        liked_biomes = npc.get_liked_biomes(biomes)

        if loved_biomes:
            for biome in loved_biomes:
                if not optimal_housing.get(biome):
                    optimal_housing[biome] = [npc.name]
                elif ((npc.dislikes + npc.hates) not in optimal_housing.get(biome)):
                    optimal_housing.get(biome).append(npc.name)
                else:
                    optimal_housing["Not sorted"].append(npc.name)
            
            continue
        
        if liked_biomes:
            for biome in liked_biomes:
                if not optimal_housing.get(biome):
                    optimal_housing[biome] = [npc.name]
                elif ((npc.dislikes + npc.hates) not in optimal_housing.get(biome)):
                    optimal_housing.get(biome).append(npc.name)
                else:
                    optimal_housing["Not sorted"].append(npc.name)

            continue
        
        optimal_housing["Not sorted"].append(npc.name)

    for housing in optimal_housing:
        if housing == "Not sorted":
            continue

        cluster = optimal_housing[housing]
        for str_npc in cluster:
            # Match the NPC to the object
            obj_npc = [npc for npc in npc_list if npc.name == str_npc][0]
            # Check to see if the NPC has any dislikes or hates in the cluster and how many
            bad_vibes = obj_npc.get_disliked_npcs(cluster) + obj_npc.get_hated_npcs(cluster)
            if len(bad_vibes) >= 1:
                optimal_housing["Not sorted"].append(str_npc)
                cluster.remove(str_npc)
                print(f"{obj_npc.name} has bad vibes with {bad_vibes} in {cluster}")

    return optimal_housing