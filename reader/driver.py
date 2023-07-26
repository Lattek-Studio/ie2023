from player import Perseus

player = Perseus()

data = open("./reader/test.txt", "r")

player.addReading(data)

print(player.health)
