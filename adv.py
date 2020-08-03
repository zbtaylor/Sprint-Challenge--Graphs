from room import Room
from player import Player
from world import World
from stack import Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


# while visited does not equal num rooms in graph
# if current room hasn't been visited
# get all of current room's exits
# check if any have not been visited
# if so, go to a random, not visited room
# otherwise, backtrack to a room connected to unvisited exits


def traverse():
    path = []
    visited = {}

    # start with '?' for each exit so we know we haven't used it yet
    visited[player.current_room.id] = {
        dir: '?' for dir in player.currentRoom.getExits()}

    # while we haven't visited every room
    while len(visited) != len(world.rooms):
        current_room = player.current_room
        current_room_id = current_room.id
        exits = player.current_room.get_exits()

        not_visited = []

        # for each available exit in the current room
        for dir in visited[current_room_id]:
            # if we haven't used an exit yet, add it to our list
            if visited[current_room_id][dir] == "?":
                not_visited.append(dir)

        # if there are exits we haven't used yet
        if len(not_visited) > 0:
            # randomly choose a direction, add it to path, and travel that way
            next_dir = not_visited[random.randint(0, len(not_visited) - 1)]
            path.append(next_dir)
            player.travel(next_dir)
            next_room_id = player.current_room.id
            visited[current_room_id][next_dir] = next_room_id

            # mark the next room as visited if we haven't been there
            if next_room_id not in visited:
                next_room_exits = player.current_room.get_exits()
                visited[next_room_id] = {dir: '?' for dir in next_room_exits}

            # figure out the direction to the previous room
            prev_room_dir = None
            if next_dir == 'n':
                prev_room_dir = 's'
            if next_dir == 's':
                prev_room_dir = 'n'
            if next_dir == 'e':
                prev_room_dir = 'w'
            if next_dir == 'w':
                prev_room_dir = 'e'

            # fill in the id of the previous room for the directions
            # of the room we just traveled to
            visited[next_room_id][prev_room_dir] = current_room_id

        # we've used every available exit in this room already
        else:
            # backtrack
            print("hey")


traverse()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
