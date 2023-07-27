def get_spiral_traj(width, spirals, x, y, lim_x, lim_y):

    x=int(x)
    y=int(y)
    offset=int(1.3*width)
    # if x <= lim_x/2 and y <= lim_y/2:
    #     # 1
    #     x += lim_x//6
    #     y += lim_y//6

    # elif x < lim_x/2 and y >= lim_y/2:
    #     # 3
    #     x += lim_x//6
    #     y -= lim_y//6

    # elif x >= lim_x/2 and y < lim_y/2:
    #     # 2
    #     x -= lim_x//6
    #     y += lim_y//6

    # elif x > lim_x/2 and y > lim_y/2:
    #     # 4
    #     x -= lim_x//6
    #     y -= lim_y//6

    distance_closest_wall   = min(abs(x-0), abs(x-lim_x),abs(y-0), abs(y-lim_y))
    if abs(x-0) == distance_closest_wall:
        print("STANGA")
        x+=offset
    elif abs(x-lim_x) == distance_closest_wall:
        x-=offset
        print("DREAPTA")
    elif abs(y-0) == distance_closest_wall:
        y+=offset
        print("SUS")
    elif abs(y-lim_y) == distance_closest_wall:
        y-=offset
        print("JOS")

    correction_x = int(x)
    correction_y = int(y)
    x = 0
    y = 0
    prx = 0
    pry = 0

    coord_list = []

    for i in range(spirals):
        x = 0-width-abs(prx)
        print(prx, x)
        for j in reversed(range(x+1, prx)):
            coord_list.append((j+correction_x, y+correction_y))
        coord_list.append((x+correction_x, y+correction_y))

        y = 0+width+abs(pry)
        for j in range(pry+1, y):
            coord_list.append((x+correction_x, j+correction_y))
        coord_list.append((x+correction_x, y+correction_y))
        pry = y

        prx = x
        x = abs(x)
        for j in range(prx+1, x):
            coord_list.append((j+correction_x, y+correction_y))
        coord_list.append((x+correction_x, y+correction_y))

        y = 0-y
        for j in reversed(range(y+1, pry)):
            coord_list.append((x+correction_x, j+correction_y))
        coord_list.append((x+correction_x, y+correction_y))
        prx = x
        pry = y

    return coord_list


"""#spiral debug

import matplotlib.pyplot as plt

# List of coordinates
coordinates = get_spiral_traj(4,6,0,0,0,0)

# Separate the x and y coordinates into separate lists
x_values, y_values = zip(*coordinates)

# Create a scatter plot
plt.scatter(x_values, y_values, color='blue')

# Set plot title and labels
plt.title('Coordinates on a 2D Grid')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Set plot limits
plt.xlim(-35, 35)
plt.ylim(-35, 35)

# Show the plot
plt.grid(True)
plt.show()"""
