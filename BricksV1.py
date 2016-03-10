# -*- coding: cp936 -*-
#引入pygame库
import pygame
import sys

#设定屏幕大小
screenSize   = 600,600
#设定砖块大小
brickWidth  = 60
brickHeight  = 15
#设定挡板大小
baffleWidth  = 60
baffleHeight = 12
#设定小球大小
diameter = 16
radius   = diameter / 2

MAX_PADDLE_X = screenSize[0] - baffleWidth
MAX_BALL_X   = screenSize[0] - diameter
MAX_BALL_Y   = screenSize[1] - diameter

# Paddle Y coordinate
PADDLE_Y = screenSize[1] - baffleHeight - 10

# Color constants
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
BRICK_COLOR = (184,134,11)

#定义状态常量 提升可读性
State_stopping = 0
State_playing = 1
State_win = 2
State_gameover = 3

#程序的封装
class Brick:
    def __init__(self):
        #初始化pygame模块
        pygame.init()
        #初始化混音器
        pygame.mixer.init()
        pygame.time.delay(1000)
        #创建游戏窗口
        self.screen = pygame.display.set_mode((600,600),0)
#无边框版self.screen = pygame.display.set_mode((600,600),pygame.NOFRAME)

        #设置窗口标题
        pygame.display.set_caption("Bricks py")

        #将图像数据都转化为Surface对象
        self.background=pygame.image.load("bgpicture.png").convert()

        #载入背景音乐
        self.soundwav=pygame.mixer.Sound("bgmusic.wav")
        self.clock = pygame.time.Clock()

        #设置字体大小
        if pygame.font:
            self.font = pygame.font.Font(None,30)
      #  else:
      #      self.font = None

        self.init_game()

        
    def init_game(self):
        #初始化生命得分和状态
        self.lives = 3
        self.score = 0
        self.state = State_stopping
        #创建平台和小球
        self.paddle   = pygame.Rect(300,PADDLE_Y,baffleWidth,baffleHeight)
        self.ball     = pygame.Rect(300,PADDLE_Y - diameter,diameter,diameter)
        #初始化小球速度
        self.ball_vel = (5,-5)
        #创建砖块
        self.create_bricks()
        
    #生成砖块位置
    def create_bricks(self):
        y_ofs = 35
        self.bricks = []
        for i in range(7):
            x_ofs = 35
            for j in range(8):
                self.bricks.append(pygame.Rect(x_ofs,y_ofs,brickWidth,brickHeight))
                x_ofs += brickWidth+ 10
            y_ofs += brickHeight + 5
    #画出砖块
    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, BRICK_COLOR, brick)

    #侦测键盘输入控制平台位置    
    def keyInput(self):
        keys = pygame.key.get_pressed()
        #
        if keys[pygame.K_LEFT]:
            self.paddle.left -= 5
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            self.paddle.left += 5
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if keys[pygame.K_SPACE] and self.state == State_stopping:
            self.ball_vel = [5,-5]
            self.state = State_playing
        elif keys[pygame.K_RETURN] and (self.state == State_gameover or self.state == State_win):
            self.init_game()

    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top  += self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]
        
        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= MAX_BALL_Y:            
            self.ball.top = MAX_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]
    #碰撞处理
    def collision(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 3
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break

        if len(self.bricks) == 0:
            self.state = State_win
            
        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - diameter
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = State_stopping
            else:
                self.state = State_gameover
    #显示生命状态
    def show_stats(self):
       # if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), False, WHITE)
            self.screen.blit(font_surface, (205,5))
             #获取程序Fps
            self.fps=int(self.clock.get_fps())
            myfps=self.font.render("FPS: " + str(self.fps) , False, WHITE)
            self.screen.blit(myfps, (5,5))

    #显示信息模块
    def show_message(self,message):
            size = self.font.size(message)
            font_surface = self.font.render(message,False, WHITE)
            x = (screenSize[0] - size[0]) / 2
            y = (screenSize[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))
            
        
            
    def run(self):
        #播放背景音乐（-1表示循环)
        self.soundwav.play(-1)

        while True:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit

            #控制帧数
            self.clock.tick(100)
            #生成背景
            self.screen.blit(self.background, (0,0))
             #self.screen.fill((0,0,0))#黑屏版
             #self.screen.fill((255,255,255))#白屏版

            #执行按键侦测
            self.keyInput()

            #判断游戏所处在的状态并给出相应反馈
            if self.state == State_playing:
                self.move_ball()
                self.collision()
            elif self.state == State_stopping:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top  = self.paddle.top - self.ball.height
                self.show_message("Press SPACE to Launch the Ball")
            elif self.state == State_gameover:
                self.show_message("What a pity! Press Enter to play again")
            elif self.state == State_win:
                self.show_message("Congratulations! Press Enter to play again")
                
            self.draw_bricks()

            # Draw paddle
            pygame.draw.rect(self.screen, BLUE, self.paddle)

            # Draw ball
            pygame.draw.circle(self.screen, WHITE, (self.ball.left + radius, self.ball.top + radius), radius)

            self.show_stats()

            pygame.display.flip()

myMasterpiece=Brick()
myMasterpiece.run()
