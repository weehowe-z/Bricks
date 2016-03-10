# -*- coding: cp936 -*-
#����pygame��
import pygame
import sys

#�趨��Ļ��С
screenSize = 600,600
#�趨ש���С
brickWidth = 60
brickHeight = 15
#�趨�����С
baffleWidth = 80
baffleHeight = 12
#�趨С���С
radius = 8
diameter = 2*radius
#�趨�����ƶ��ٶ�
baffleVelocity = 5
#�趨С���ƶ��ٶ�
ballVelocity = 5,5
#�趨����ƶ���Χ
minXpos = 0
minBallXpos = 0
minBallYpos = 0
maxXpos = screenSize[0] - baffleWidth
maxBallXpos = screenSize[0] - diameter
maxBallYpos = screenSize[1] - diameter - 10
#�趨����λ��(�������ϽǼƣ�
baffleXpos = (screenSize[0] - baffleWidth)/2
baffleYpos = screenSize[1] - baffleHeight -10
#�趨С��λ��
ballXpos = screenSize[0]/2 - radius
ballYpos = baffleYpos -diameter 
#������ɫ
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
brickColor = (184,134,11)

#����״̬����
State_restarting = 0
State_playing = 1
State_win = 2
State_gameover = 3

#����ķ�װ
class Brick:
    def __init__(self):
        #��ʼ��pygameģ��
        pygame.init()

        #��ʼ��������
        pygame.mixer.init()
        pygame.time.delay(1000)

        #������Ϸ����
        self.screen = pygame.display.set_mode(screenSize,0)
#�ޱ߿��self.screen = pygame.display.set_mode(screenSize,pygame.NOFRAME)

        #���ô��ڱ���
        pygame.display.set_caption("Bricks by zwh")

        #��ͼ�����ݶ�ת��ΪSurface����
        self.background=pygame.image.load("bg.png").convert()

        #���뱳������
        self.soundwav=pygame.mixer.Sound("bgmusic.wav")
        #�趨ʱ��
        self.clock = pygame.time.Clock()

        #��������
        self.font = pygame.font.Font("Lancy.ttf",23)
        self.font2 = pygame.font.Font("Kevin.ttf",20)

        self.init_game()

    #��Ϸ���ݣ��仯�ģ���ʼ��    
    def init_game(self):

        #��ʼ�������÷ֺ�״̬
        self.lives = 3
        self.score = 0
        self.state = State_restarting

        #���������С��ľ��η�Χ
        self.baffle = pygame.Rect(baffleXpos,baffleYpos,baffleWidth,baffleHeight)
        self.ball   = pygame.Rect(ballXpos,ballYpos,diameter,diameter)

        #��ʼ��С���ٶ�
        self.ballVelocity = ballVelocity

        #ִ�д���ש��
        self.create_bricks()
        
    #����ש����η�Χ
    def create_bricks(self):
        ypos= 30
        self.bricks = []
        for i in range(7):
            xpos = 25
            for j in range(8):
                self.bricks.append(pygame.Rect(xpos,ypos,brickWidth,brickHeight))
                xpos += brickWidth+ 10
            ypos += brickHeight + 5

    #����ש��
    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, brickColor, brick)
            #pygame.draw.ellipse(self.screen, brickColor, brick) ��Բ�� 

    #�������������ƽ̨λ��    
    def keyInput(self):
        keys = pygame.key.get_pressed()

        #�������
        if keys[pygame.K_LEFT]:
            self.baffle.left -= baffleVelocity
            if self.baffle.left <= minXpos:
                self.baffle.left = minXpos

        #�Ҽ�����
        if keys[pygame.K_RIGHT]:
            self.baffle.left += baffleVelocity
            if self.baffle.left >= maxXpos:
                self.baffle.left = maxXpos
                
        #           ̫�հ�
        ##�ϼ�����
        #if keys[pygame.K_UP]:
        #    self.baffle.top -= baffleVelocity
        ##�¼�����
        #if keys[pygame.K_DOWN]:
        #    self.baffle.top += baffleVelocity
        
        #Space����
        if keys[pygame.K_SPACE] and self.state == State_restarting:
            self.ballVelocity = [5,-5]
            self.state = State_playing

        #ʤ����ʧ��ʱ����������
        elif keys[pygame.K_RETURN] and (self.state == State_gameover or self.state == State_win):
            self.init_game()

    def move_ball(self):

        #�ƶ����� �ٶ�V*��t(��֡����أ� �����Ͻ�Ϊ��׼
        self.ball.left += self.ballVelocity[0]
        self.ball.top  += self.ballVelocity[1]

        #���ڷ���
        if self.ball.left <= minBallXpos:
            self.ball.left = minBallXpos
            self.ballVelocity[0] *= -1
        elif self.ball.left >= maxBallXpos:
            self.ball.left = maxBallXpos
            self.ballVelocity[0] *= -1
        elif self.ball.top <= minBallYpos:
            self.ball.top = minBallYpos 
            self.ballVelocity[1] *= -1
        #���׾�ֹ
        elif self.ball.top >= maxBallYpos:            
            self.ball.top = maxBallYpos

    #��ײ����
    def collision(self):

        #����ÿһ��ש������ж� �ӷ� �ٶȷ��� ש������
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 10
                self.ballVelocity[1] *= -1
                self.bricks.remove(brick)
                break

        if self.bricks == []:
            self.state = State_win

        if self.ball.colliderect(self.baffle):
            self.ball.top = self.baffle.top - diameter
            self.ballVelocity[1] *= -1
        elif self.ball.top == maxBallYpos:
            self.lives -= 1
            if self.lives > 0:
                pygame.time.wait(200)
                self.state = State_restarting
            else:
                self.state = State_gameover
    #��ʾ����״̬
    def show_stats(self):
        myScore = self.font2.render("SCORE: " + str(self.score), True, WHITE)
        myLife = self.font2.render("LIVES: " + str(self.lives), True, WHITE)
        self.screen.blit(myScore, (400,5))
        self.screen.blit(myLife, (500,5))
        #��ȡ����Fps
        self.fps=int(self.clock.get_fps())  #Ϊ��ȥ��ĩβ��С��
        myfps=self.font2.render("FPS: " + str(self.fps) , True, WHITE)
        self.screen.blit(myfps, (5,5))

    #��ʾ��Ϣģ��
    def show_message(self,message):
            #��ȡ�����Сʹ������ʾ������
            size = self.font.size(message)
            font_surface = self.font.render(message,True, WHITE)
            x = (screenSize[0] - size[0]) / 2
            y = (screenSize[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))
            
        
    #���й���      
    def run(self):
        #���ű������֣�-1��ʾѭ��)
        self.soundwav.play(-1)

        while True:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #����֡��
            self.clock.tick(100)
            #���ɱ���
            self.screen.blit(self.background, (0,0))
             #self.screen.fill((0,0,0))#������
             #self.screen.fill((255,255,255))#������

            #ִ�а������
            self.keyInput()

            #�ж���Ϸ�����ڵ�״̬��������Ӧ����
            if self.state == State_playing:   #ֻ���ڸ�״̬�²Żᴥ���ƶ�����ײ
                self.move_ball()
                self.collision()
            elif self.state == State_restarting:
                self.ball.left = self.baffle.left + self.baffle.width / 2 - radius
                self.ball.top  = self.baffle.top - self.ball.height
                self.show_message("Press SPACE to Launch the Ball")
            elif self.state == State_gameover:
                self.show_message("What a pity! Press ENTER to retry")
            elif self.state == State_win:
                self.show_message("Congratulations! Press ENTER to play again")
                
            self.draw_bricks()
            self.show_stats()

            #��������
            pygame.draw.rect(self.screen, BLUE, self.baffle)
            #����С��
            pygame.draw.circle(self.screen, WHITE, (self.ball.left + radius, self.ball.top + radius), radius)


            pygame.display.flip()

myMasterpiece=Brick()
myMasterpiece.run()
