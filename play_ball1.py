from tkinter import *
import random
import time


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.score = 0
        # print(self.canvas.winfo_height())
        # self.canvas_height = self.canvas.winfo_height()

    def draw(self):
        # 移动球为ID，速度方向为x,y
        self.canvas.move(self.id, self.x, self.y)
        # 获取球的坐标，pos为四个数[左上x，左上y，右下x，右下y]
        self.pos = self.canvas.coords(self.id)
        # print(self.pos)
        # 一下两行为控制上下边沿，左右边沿
        if self.pos[1] <= 0:
            self.y = 1

        if self.pos[3] >= self.canvas.winfo_reqheight():
            # print(self.canvas.winfo_reqheight())
            self.y = 0
            self.x = 0
            time.sleep(0.5)
            self.canvas.create_text(100, 100, text='Game Over', fill='red')
        if self.front_hit_paddle(self.pos) == True:
            self.score = self.score + 1
            self.y = -3
        if self.back_hit_paddle(self.pos) == True:
            self.y = 3

        if self.pos[0] <= 0:
            self.x = 1
        if self.pos[2] >= self.canvas.winfo_width():
            self.x = -1

    def front_hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
            return False

    def back_hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[1] <= paddle_pos[3] and pos[1] >= paddle_pos[1]:
                return True
            return False


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= self.canvas.winfo_width():
            self.x = 0

    def turn_left(self, evt):
        self.x = -2

    def turn_right(self, evt):
        self.x = 2
if __name__=="__main__":
    tk = Tk()  # 实例化窗口
    tk.title("Game")  # 定义窗口名称
    tk.resizable(0, 0)  # 不可变化窗口大小
    tk.wm_attributes("-topmost", 1)  # 窗口置顶
    # 实例化画板
    canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()

    paddle = Paddle(canvas, 'blue')
    ball = Ball(canvas, paddle, 'red')  # 实例化球

    # tk.update()
    i = 1
    j = canvas.create_text(50, 10, text='SCORE:%d' % i)
    while 1:
        i = i + 1
        canvas.itemconfig(j, text='SCORE:%d' % ball.score)
        ball.draw()  #
        paddle.draw()
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)
