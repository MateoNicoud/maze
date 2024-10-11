import random
import time 
import subprocess

def grid_init(width, height):
    grid = []

    for _ in range(height):
        row = ["□"] * width
        grid.append(row)

    grid[0][0] = "S"
    grid[0][1] = "■"
    grid[1][1] = "■"
    grid[2][1] = "■"
    grid[4][1] = "■"
    grid[5][1] = "■"
    grid[1][3] = "■"
    grid[2][3] = "■"
    grid[4][3] = "■"
    grid[1][4] = "■"
    grid[2][4] = "G"
    grid[3][4] = "■"
    grid[3][5] = "■"
    grid[5][5] = "■"
    grid[1][6] = "■" 

    return grid, [0, 0], [4, 2]

def grid_alea(width, height):
    grid = []

    for _ in range(height):
        row = ["□"] * width
        grid.append(row)

    ratio = 0.3
    start_x, start_y = random.randint(0, width-1), random.randint(0, height-1)
    grid[start_y][start_x] = "S"
    
    end_x, end_y = random.randint(0, width-1), random.randint(0, height-1)
    while (end_x, end_y) == (start_x, start_y):
        end_x, end_y = random.randint(0, width-1), random.randint(0, height-1)
    grid[end_y][end_x] = "G"

    for _ in range(int(width * height * ratio)):
        wall_x, wall_y = random.randint(0, width-1), random.randint(0, height-1)
        while grid[wall_y][wall_x] in ["S", "G", "■"]:
            wall_x, wall_y = random.randint(0, width-1), random.randint(0, height-1)
        grid[wall_y][wall_x] = "■"

    return grid, [start_x, start_y], [end_x, end_y]



def resolve_dfs(grid, start_pos, end_pos, nbr_action=0, action=None, real_start=None):
    if action is None:
        action = []
    player = "◆"
    p_x, p_y = start_pos
    if real_start is None:
        real_start= start_pos
    grid[p_y][p_x] = player

    directions = {
        "right": (1, 0),
        "down": (0, 1),
        "left": (-1, 0),
        "up": (0, -1)
    }

    def move(direction):
        nonlocal p_x, p_y
        dx, dy = directions[direction]
        grid[p_y][p_x] = "⧅"  # miette du petit poussé
        p_x += dx
        p_y += dy
        grid[p_y][p_x] = player
        action.append(direction)

    def backtrack():
        nonlocal p_x, p_y
        last_action = action.pop()
        dx, dy = directions[last_action]
        grid[p_y][p_x] = "⧅"
        p_x -= dx
        p_y -= dy
        grid[p_y][p_x] = player

    if p_x + 1 < len(grid[0]) and grid[p_y][p_x + 1] not in ["■", "⧅"]:
        move("right")
    elif p_y + 1 < len(grid) and grid[p_y + 1][p_x] not in ["■", "⧅"]:
        move("down")
    elif p_x - 1 >= 0 and grid[p_y][p_x - 1] not in ["■", "⧅"]:
        move("left")
    elif p_y - 1 >= 0 and grid[p_y - 1][p_x] not in ["■", "⧅"]:
        move("up")
    elif len(action) <= 0:
        print("No solution")
        return grid
    else:
        backtrack()

    nbr_action += 1
    for row in grid:
        print(" ".join(row))
    time.sleep(0.5)
    subprocess.run(["clear"])

    if [p_x, p_y] != end_pos:
        resolve_dfs(grid, [p_x, p_y], end_pos, nbr_action, action, real_start)
        return grid

    # Print the final path
    p_x, p_y = real_start
    for steps in action:
        dx, dy = directions[steps]
        grid[p_y][p_x] = {"right": "→", "down": "↓", "left": "←", "up": "↑"}[steps]
        p_x += dx
        p_y += dy
        for row in grid:
            print(" ".join(row))
        time.sleep(0.5)
        subprocess.run(["clear"])

    print("The maze has been solved in " + str(nbr_action) + " steps")
    print("The optimal path is " + str(len(action)) + " steps")
    return grid

def resolve_bfs(grid, start_pos, end_pos, speed = 0.1):
    player = "◆"

    start_pos.append([])
    players_pos = [
        start_pos
    ]
    grid[players_pos[0][1]][players_pos[0][0]] = player
    nbr_action = 0
    
    while not any([players[0], players[1]] == end_pos for players in players_pos):
        if not players_pos:
            print("No solution")
            return grid
        for players in players_pos:
            if [players[0], players[1]] == end_pos:
                grid[players[1]][players[0]] = player
                for step in players[2]:
                    p_y, p_x = step
                    grid[p_y][p_x] = "@"
                    for row in grid:
                        print(" ".join(row))
                    time.sleep(0.5)
                    subprocess.run(["clear"])
                print("The maze has been solved in " + str(nbr_action) + " steps")
                return grid
            else:
                grid[players[1]][players[0]] = "⧅"
            y = players[1]
            x = players[0]
            players.append([])
            possibilites = players[len(players) - 1]

            # Bas
            if y + 1 < len(grid) and grid[y + 1][x] != "■" and grid[y + 1][x] != "⧅":
                possibilites.append("down")
            # Droite
            if x + 1 < len(grid[0]) and grid[y][x + 1] != "■" and grid[y][x + 1] != "⧅":
                possibilites.append("right")

            # Gauche
            if x - 1 >= 0 and grid[y][x - 1] != "■" and grid[y][x - 1] != "⧅":
                possibilites.append("left")

            # Haut
            if y - 1 >= 0 and grid[y - 1][x] != "■" and grid[y - 1][x] != "⧅":
                possibilites.append("up")

            if len(possibilites) == 0:
                players_pos.remove(players)
                continue

            memory = players[2]
        
            if possibilites[0] == "down":
                memory.append([y,x])
                players[1] += 1
            elif possibilites[0] == "right":
                memory.append([y,x])
                players[0] += 1
            elif possibilites[0] == "left":
                memory.append([y,x])
                players[0] -= 1
            elif possibilites[0] == "up":
                memory.append([y,x])
                players[1] -= 1

            players[2] = memory  # Update the player's memory with the new path

            for row in grid:
                print(" ".join(row))
            time.sleep(0.5)
            subprocess.run(["clear"])

            nbr_action += 1
            if len(possibilites) > 1:
                for i in range(1, len(possibilites)):
                    new_memory = memory[:]
                    if possibilites[i] == "down":
                        new_memory.append([y,x])
                        players_pos.append([x, y + 1, new_memory])
                    elif possibilites[i] == "right":
                        new_memory.append([y,x])
                        players_pos.append([x + 1, y, new_memory])
                    elif possibilites[i] == "left":
                        new_memory.append([y,x])
                        players_pos.append([x - 1, y, new_memory])
                    elif possibilites[i] == "up":
                        new_memory.append([y,x])
                        players_pos.append([x, y - 1, new_memory])

            grid[players[1]][players[0]] = player
            if len(players) > 3:
                players.pop(len(players) - 1)

            for row in grid:
                print(" ".join(row))
            time.sleep(speed)
            subprocess.run(["clear"])


        
    # print("The maze has been solved in "+str(nbr_action)+" steps")
    # print("The optimal path is "+str(len(action))+" steps")
    # return grid


# -- Code ---------------------------------------------------------


# int width, int height
grid, start_pos, end_pos = grid_init(7, 6)
# grid, start_pos, end_pos = grid_alea(10, 10)


# resolve_dfs(grid, start_pos, end_pos)
resolve_bfs(grid, start_pos, end_pos, 0.01)

for row in grid:
    print(" ".join(row))
