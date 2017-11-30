from tkinter import *
import time
import socket,threading

paddleup_pos=[1, 1, 1, 1]
paddledown_pos=[1, 1, 1, 1]
ball_pos=[1,2,3,4]

class online_client():
    def __init__(self):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1',9999))
        print(self.socket.recv(1024).decode('utf-8'))

    def run(self):
        global paddleup_pos,paddledown_pos,ball_pos

        while True:
            # data = self.socket.recv(1024)
            # message_data = data.decode('utf-8')
            self.socket.send((str(ball_pos)+','+str(paddleup_pos)).encode('utf-8'))
            paddledown_pos=eval(self.socket.recv(1024).decode('utf-8'))
            # print(message_data)
            # time.sleep(0.01)
            # if not data or data.decode('utf-8') == 'exit':
            #     break
        self.socket.close()


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
    def get_pos(self):
        return self.canvas.coords(self.id)
    def set_pos(self,position):
        self.canvas.coords(self.id,position)


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

    def get_pos(self):
        return self.canvas.coords(self.id)
    def set_pos(self,position):
        self.canvas.coords(self.id,position)



if __name__ == "__main__":

    tk = Tk()
    tk.title('Game_client')
    tk.wm_attributes("-topmost", 1)
    canvas = Canvas(tk, width=500, height=600)
    canvas.pack()

    score_text = canvas.create_text(100, 10, text='MYSCORE:%d ENEMYSCORE:%d'%(0,0))
    paddle_down = Paddle(canvas, 'blue', x_position=200, y_position=500,press_left='<KeyPress-A>',press_right='<KeyPress-D>')
    paddle_up = Paddle(canvas, 'red', x_position=200, y_position=100)

    ball = Ball(canvas, paddle_down, paddle_up,'red')
    paddleup_pos = paddle_up.get_pos()
    ball_pos = ball.get_pos()

    my_socket=online_client()
    my_threading=threading.Thread(target=my_socket.run,args=())
    my_threading.start()

    while 1:
        paddle_down.set_pos(paddledown_pos)
        paddle_up.set_pos(paddleup_pos)
        ball.set_pos(ball_pos)
        ball.move()
        paddle_down.move()
        paddle_up.move()
        canvas.itemconfig(score_text, text='MYSCORE:%d ENEMYSCORE:%d' %( ball.score_my,ball.score_enemy))

        ball_pos=ball.get_pos()
        paddleup_pos = paddle_up.get_pos()
        paddledown_pos=paddle_down.get_pos()

        tk.update_idletasks()
        tk.update()
        # print(paddle_pos)
        time.sleep(0.01)


    tk.mainloop()
