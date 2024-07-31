import pygame
from pygame.sprite import Sprite
class Ship(Sprite):#管理飞船的类
    def __init__(self,ai_game):
        super().__init__()
        # 初始化飞船并设置其初始位置
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect=ai_game.screen.get_rect()

        #加载飞船图像并获取其外接矩形
        self.image=pygame.image.load('images/ship.bmp')
        self.rect=self.image.get_rect()

        #对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom=self.screen_rect.midbottom

        #在飞船的属性x中存储小数值
        self.x=float(self.rect.x)

        #移动标志
        self.moving_right=False
        self.moving_left=False

    def update(self):#根据移动标志调整飞船的位置
        #更新飞船而不是rect对象的x值
        if self.moving_right and self.rect.right<self.screen_rect.right:#self.rect.right返回飞船外接矩形右边缘的x坐标，如果这个值小于self.screen_rect.right的值，就说明飞船未触及屏幕右边缘
            self.x+=self.settings.ship_speed#向右移动飞船
        if self.moving_left and self.rect.left>0:#左边缘的情况类似：如果rect左边缘的x坐标大于0，就说明飞船未触及屏幕左边缘
            self.x-=self.settings.ship_speed#如果玩家同时按下了左右箭头键，将先增加再减少飞船的rect.x值，即飞船的位置保持不变

        #根据self.x更新rect对象
        self.rect.x=self.x #self.rect.x只存储self.x的整数部分，但对显示飞船而言，问题不大

    def blitme(self):
        #在底部位置绘制飞船
        self.screen.blit(self.image,self.rect)

    def center_ship(self):#让飞船在屏幕底端居中
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)