"""x = 0
y= 0
prx=0
pry=0
width = 4
coord_list = []
for i in range (5):
    x=0-width-abs(prx)
    coord_list.append((x,y))
    y=0+width+abs(pry)
    coord_list.append((x,y))
    x=abs(x)
    coord_list.append((x,y))
    y=0-y
    coord_list.append((x,y))
    prx=x
    pry=y"""

def get_spiral_traj(width,spirals,x,y):
    correction_x = x
    correction_y = y
    x = 0
    y= 0
    prx=0
    pry=0

    coord_list = []

    for i in range (spirals):
        x=0-width-abs(prx)
        coord_list.append((x+correction_x,y+correction_y))
        y=0+width+abs(pry)
        coord_list.append((x+correction_x,y+correction_y))
        x=abs(x)
        coord_list.append((x+correction_x,y+correction_y))
        y=0-y
        coord_list.append((x+correction_x,y+correction_y))
        prx=x
        pry=y

    return coord_list

print(get_spiral_traj(4,5,1,1))


