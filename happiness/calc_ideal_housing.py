from npc import NPC

def parse_csv(file_path: str) -> list[NPC]:
    with open(file_path, 'r') as file:
        all_npcs = file.readline().strip().split(',')
        all_npcs.pop(0)  # Remove header
        all_npcs = [NPC(name) for name in all_npcs]  # Cast to NPC

        rows = file.readlines()
        rows = [row.split(',') for row in rows]

        print(rows)
        for i, npc in enumerate(all_npcs):
            if rows[i][i + 1] == "Neutral":
                continue
            elif rows[i][i + 1] == "Love":
                npc.loves.append(NPC(rows[i][0]))
            elif rows[i][i + 1] == "Like":
                npc.likes.append(NPC(rows[i][0]))
            elif rows[i][i + 1] == "Dislike":
                npc.dislikes.append(NPC(rows[i][0]))
            elif rows[i][i + 1] == "Hate":
                npc.hates.append(NPC(rows[i][0]))

    return all_npcs
