f = open("./reader/test.txt", "r")

file = f.read().split("\n")

f.close()

size = file[0]

xSize = int(size.split(" ")[0])
ySize = int(size.split(" ")[1])

print(xSize, xSize)

map = ''
for i in range(1, ySize):
    map += file[i]

print(map)

coords = file[ySize + 1]

xCoord = int(coords.split(" ")[0])
yCoord = int(coords.split(" ")[1])

print(xCoord, yCoord)

abilities = file[ySize + 2]

health = int(abilities.split(" ")[0])
dig = int(abilities.split(" ")[1])
attack = int(abilities.split(" ")[2])
move = int(abilities.split(" ")[3])
vision = int(abilities.split(" ")[4])
scan = int(abilities.split(" ")[5])
battery = int(abilities.split(" ")[6])

print(health, dig, attack, move, vision, scan, battery)

resources = file[ySize + 3]

cobblestone = int(resources.split(" ")[0])
iron = int(resources.split(" ")[1])
osmium = int(resources.split(" ")[2])

print(cobblestone, iron, osmium)
