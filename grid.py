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



def resolve_dfs(grid, start_pos, end_pos):
    player = "◆"
    p_x, p_y = start_pos
    grid[p_y][p_x] = player
    
    nbr_action = 0
    action = []


    while [p_x, p_y] != end_pos:

        # Droite
        if p_x + 1 < len(grid[0]) and grid[p_y][p_x+1] != "■" and grid[p_y][p_x+1] != "⧅":
            grid[p_y][p_x] = "⧅"  # miette du petit poussé
            p_x += 1  # déplacement à droite
            grid[p_y][p_x] = player  
            action.append("right")

        # Bas
        elif p_y + 1 < len(grid) and grid[p_y+1][p_x] != "■" and grid[p_y+1][p_x] != "⧅":
            grid[p_y][p_x] = "⧅"
            p_y += 1  
            grid[p_y][p_x] = player 
            action.append("down")

        # Gauche
        elif p_x - 1 >= 0 and grid[p_y][p_x-1] != "■" and grid[p_y][p_x-1] != "⧅":
            grid[p_y][p_x] = "⧅"  
            p_x -= 1  
            grid[p_y][p_x] = player 
            action.append("left")

        # Haut
        elif p_y - 1 >= 0 and grid[p_y-1][p_x] != "■" and grid[p_y-1][p_x] != "⧅":
            grid[p_y][p_x] = "⧅"
            p_y -= 1  
            grid[p_y][p_x] = player  
            action.append("up")
        
        elif len(action) <= 0:
            print("No solution")
            return grid

        # Retour en arrière
        else:
            grid[p_y][p_x] = "⧅"
            last_action = action.pop()
            match last_action:
                case "right":
                    p_x -= 1
                case "down":
                    p_y -= 1
                case "left":
                    p_x += 1
                case "up":
                    p_y += 1
            grid[p_y][p_x] = player

        nbr_action += 1
        for row in grid:
            print(" ".join(row))
        # print("--------------------------------------------")
        time.sleep(0.5)
        subprocess.run(["clear"])

    p_x, p_y = start_pos
    for steps in action:
        if steps == "right":
            grid[p_y][p_x] = "→"
            p_x += 1
        elif steps == "down":
            grid[p_y][p_x] = "↓"
            p_y += 1
        elif steps == "left":
            grid[p_y][p_x] = "←"
            p_x -= 1
        elif steps == "up":
            grid[p_y][p_x] = "↑"
            p_y -= 1
        
        for row in grid:
            print(" ".join(row))
        time.sleep(0.5)
        subprocess.run(["clear"])
    print("The maze has been solved in "+str(nbr_action)+" steps")
    print("The optimal path is "+str(len(action))+" steps")
    return grid

def resolve_bfs(grid, start_pos, end_pos, speed = 0.1):
    player = "◆"

    players_pos = [
        start_pos,
    ]
    grid[players_pos[0][1]][players_pos[0][0]] = player
    action = []
    nbr_action = 0
    
    while not any([players[0], players[1]] == end_pos for players in players_pos):
        if not players_pos:
            print("No solution")
            return grid
        for players in players_pos:
            if [players[0], players[1]] == end_pos:
                grid[players[1]][players[0]] = player
                print("The maze has been solved in "+str(nbr_action)+" steps")
                return grid
            else:
                grid[players[1]][players[0]] = "⧅"
            y = players[1]
            x = players[0]
            players.append([])
            possibilites = players[2]

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

            match possibilites[0]:
                case "down":
                    players[1] += 1
                case "right":
                    players[0] += 1
                case "left":
                    players[0] -= 1
                case "up":
                    players[1] -= 1
            for row in grid:
                print(" ".join(row))
            time.sleep(0.5)
            subprocess.run(["clear"])


            nbr_action += 1
            if len(possibilites) > 1:
                for i in range(1, len(possibilites)):
                    if possibilites[i] == "down":
                        players_pos.append([x, y + 1])
                        # for row in grid:
                        #     print(" ".join(row))
                        # time.sleep(speed)
                        # subprocess.run(["clear"])

                    elif possibilites[i] == "right":
                        players_pos.append([x + 1, y])
                        # for row in grid:
                        #     print(" ".join(row))
                        # time.sleep(speed)
                        # subprocess.run(["clear"])
                    elif possibilites[i] == "left":
                        players_pos.append([x - 1, y])
                        # for row in grid:
                        #     print(" ".join(row))
                        # time.sleep(speed)
                        # subprocess.run(["clear"])
                    elif possibilites[i] == "up":
                        players_pos.append([x, y - 1])
                        # for row in grid:
                        #     print(" ".join(row))
                        # time.sleep(speed)
                        # subprocess.run(["clear"])

            grid[players[1]][players[0]] = player
            players.pop(2)

            for row in grid:
                print(" ".join(row))
            time.sleep(speed)
            subprocess.run(["clear"])


        
    # print("The maze has been solved in "+str(nbr_action)+" steps")
    # print("The optimal path is "+str(len(action))+" steps")
    # return grid


# -- Code ---------------------------------------------------------


# int width, int height
# grid, start_pos, end_pos = grid_init(7, 6)
grid, start_pos, end_pos = grid_alea(20, 20)


resolve_dfs(grid, start_pos, end_pos)
# resolve_bfs(grid, start_pos, end_pos, 0.01)

for row in grid:
    print(" ".join(row))
