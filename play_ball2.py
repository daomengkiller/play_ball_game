from tkinter import *
import time


class Ball():
    def __init__(self, canvas, paddle_my,paddle_enemy, color):
        self.canvas = canvas
        self.paddle_my = paddle_my
        self.paddle_enemy=paddle_enemy
        self.score_my = 0
        self.score_enemy=0

        self.color = color
        self.id = self.canvas.create_oval(10, 10, 25, 25, fill=color)

        self.canvas.move(self.id, 245, 100)
        self.x = 1
        self.y = 1

    def move(self):
        self.canvas.move(self.id, self.x, self.y)
        self.pos = self.canvas.coords(self.id)
        if self.pos[1] <= 0:
            self.y = -self.y
        if self.pos[3] >= self.canvas.winfo_reqheight():
            self.y = 0
            self.x = 0
        if self.pos[0] <= 0:
            self.x = -self.x
        if self.pos[2] >= self.canvas.winfo_reqwidth():
            self.x = -self.x
        if self.hit_paddle(self.pos,self.paddle_my):
            self.y = -self.y
            self.score_my= self.score_my + 1
        if self.hit_paddle(self.pos,self.paddle_enemy):
            self.y = -self.y
            self.score_enemy= self.score_enemy + 1

    def hit_paddle(self, pos,paddle):
        paddle_pos = self.canvas.coords(paddle.id)

        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
                return True
        return False


class Paddle():
    def __init__(self, canvas, color,x_position=200,y_position=300,press_left='<KeyPress-Left>',press_right='<KeyPress-Right>'):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.color = color
        self.canvas.move(self.id, x_position,y_position)
        self.x = 0
        self.canvas.bind_all(press_left, self.turn_left)
        self.canvas.bind_all(press_right, self.turn_right)

    def turn_left(self, evt):
        self.x = -3

    def turn_right(self, evt):
        self.x = 3

    def move(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[2] >= self.canvas.winfo_width():
            self.x = 0
        if pos[0] <= 0:
            self.x = 0


if __name__ == "__main__":
    tk = Tk()
    tk.title('Game')
    tk.wm_attributes("-topmost", 1)
    canvas = Canvas(tk, width=500, height=600)
    canvas.pack()

    score_text = canvas.create_text(100, 10, text='MYSCORE:%d ENEMYSCORE:%d'%(0,0))

    paddle_down = Paddle(canvas, 'blue', x_position=200, y_position=500,press_left='<KeyPress-A>',press_right='<KeyPress-D>')
    paddle_up = Paddle(canvas, 'red', x_position=200, y_position=100)

    ball = Ball(canvas, paddle_down, paddle_up,'red')
    while 1:
        ball.move()
        paddle_down.move()
        paddle_up.move()
        canvas.itemconfig(score_text, text='MYSCORE:%d ENEMYSCORE:%d' %( ball.score_my,ball.score_enemy))
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)

    tk.mainloop()
