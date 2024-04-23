"""
Module responsible for creating the game graph
And finding all possible ways of winning

To display graph run the file algorithm.py or
run get_next_positions and than print connections
"""

from constants import CHARACTERS_NUMBER, SIDES, STARTING_SIDE, RAFT_CAPACITY
from pprint import pprint

losing = []
connections = {}

# creating the basic settings such as starting position, winning position and losing conditions
if STARTING_SIDE == "<":
    starting = "c"*CHARACTERS_NUMBER+"m"*CHARACTERS_NUMBER+"<"
    winning = ">"+"c"*CHARACTERS_NUMBER+"m"*CHARACTERS_NUMBER
else:
    starting = ">"+"c"*CHARACTERS_NUMBER+"m"*CHARACTERS_NUMBER
    winning = "c"*CHARACTERS_NUMBER+"m"*CHARACTERS_NUMBER+"<"

for i in range(2, CHARACTERS_NUMBER+1):
    for j in range(1, i):
        for k in range(2):
            losing.append("c"*i+"m"*j+SIDES[k]+"c"*(CHARACTERS_NUMBER-i)+"m"*(CHARACTERS_NUMBER-j))
            losing.append("c"*(CHARACTERS_NUMBER-i)+"m"*(CHARACTERS_NUMBER-j)+SIDES[k]+"c"*i+"m"*j)


def get_possible_raft(position: str) -> list:
    """
    Creates list of every possible combination of raft crew depening on side
    """
    possibilities = []
    side = split_position(position)[0]
    ms, cs = side.count("m"), side.count("c")

    for i in range(1, min(ms, RAFT_CAPACITY)+1):
        possibilities.append(i*"m")
    for i in range(1, min(cs, RAFT_CAPACITY)+1):
        possibilities.append(i*"c")
    for i in range(1, min(cs, RAFT_CAPACITY)+1):
        for j in range(1, min(ms, RAFT_CAPACITY)-i+1):
            possibilities.append("c"*i+"m"*j)

    return possibilities


def split_position(position: str) -> (str, str, str):
    """
    Divides position into three sections depending on current side of the river
    """
    if position.count("<"):
        side, opposite, sign = position.split("<") + ["<"]
    else:
        opposite, side, sign = position.split(">") + [">"]
    return side, opposite, sign


def get_resulting_position(position: str, raft: str) -> str:
    """
    Get position string after making a move (transfering raft to the other side)
    """
    side, opposite, sign = split_position(position)
    sidem = side.count("m") - raft.count("m")
    sidec = side.count("c") - raft.count("c")
    oppositem = opposite.count("m") + raft.count("m")
    oppositec = opposite.count("c") + raft.count("c")
    if sign == "<":
        return sidec*"c"+sidem*"m"+">"+oppositec*"c"+oppositem*"m"
    else:
        return oppositec*"c"+oppositem*"m"+"<"+sidec*"c"+sidem*"m"


def get_next_positions(position: str):
    """
    Creates game grap (connection graph) using recursive algorithm
    Global variable connections used to save memory usage
    """
    for raft in get_possible_raft(position):
        new_position = get_resulting_position(position, raft)
        if connections.get(position):
            if new_position in connections[position]:
                continue
            else:
                connections[position].append(new_position)
        else:
            connections[position] = [new_position]

        # end condition
        if new_position not in losing:
            get_next_positions(new_position)


def find_path(position: str, path: list, winning: str) -> list:
    """
    Returns a list of all possible paths leading to a victory
    """
    winning_paths = []
    for new_pos in connections[position]:
        if new_pos in losing or new_pos in path:
            continue
        if new_pos == winning:
            return [path+[new_pos]]
        winning_paths += find_path(new_pos, path+[new_pos], winning)
    return winning_paths


get_next_positions(starting)
if __name__ == "__main__":
    pprint(connections, indent=4)
    pprint(find_path(starting, [starting], winning), compact=True)
