import turtle,time,random,snake
size= 10
actions = (0,2,1,3,0,3,1)
fpos = [(5,5),(6,6),(5,6),(6,7),(0,0)]
segs = []
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("blue")
# the width and height can be put as user's choice
wn.setup(width=size*20, height=size*20)
wn.tracer(0)
head = turtle.Turtle()
head.shape("square")
head.color("white")
head.penup()
headx,heady = size//2 + 1,size//2 +1
head.goto(0,0)
food = turtle.Turtle()
colors = random.choice(['red', 'green', 'black'])
shapes = 'square'
food.speed(0)
food.shape(shapes)
food.color(colors)
food.penup()
fx,fy=fpos[0][0],fpos[0][1]
food.goto(fx*20,fy*20)
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.hideturtle()
pen.goto(0, 250)
pen.write("Score : 0  High Score : {}".format(len(actions)), align="center",
        font=("candara", 24, "bold"))
pen.penup()
while True:
    wn.update()
    for i in range(len(actions)):
        dd=actions[i]
        print(dd)
        if dd==0:
            dirx=1
            diry=0
        elif dd==1:
            dirx=-1
            diry=0
        elif dd==2:
            dirx=0
            diry=1
        elif dd==3:
            dirx=0
            diry=-1
        headx-=(dirx*20)
        heady-=(diry*20)
        head.goto(headx,heady)
        if headx>=fpos[0][0]-30 or headx<=fpos[0][0]+30:
            if heady>=fpos[0][1]-30 or heady<=fpos[0][1]+30:
                quit()
        time.sleep(0.5)
    break
turtle.mainloop()