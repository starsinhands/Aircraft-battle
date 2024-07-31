class Settings:#存储游戏《外星人入侵》中所有设置的类
    def __init__(self):#初始化游戏的设置
        #屏幕设置
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(230,230,230)#设置背景色

        self.ship_speed=1.5#飞船设置

        #子弹设置：创建宽3像素、高15像素的深灰色子弹。子弹的速度比飞船稍低
        self.bullet_speed=1.5#提高子弹的速度
        self.ship_limit=3#飞船设置
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(60,60,60)
        self.bullets_allowed=3#存储最大子弹数

        # 外星人设置
        self.alien_speed=1.0
        self.fleet_drop_speed=10
        self.fleet_direction=1#fleet_direction为1表示向右移，为-1表示向左移

        #加快游戏节奏的速度
        self.speedup_scale=1.1#控制游戏节奏的加快速度：游戏节奏始终不变，设置为1.1能够将游戏节奏提高到足够块，让游戏既有难度又并非不可完成
        self.score_scale=1.5#外星人分数的提高速度：玩家每提高一个等级，游戏的节奏就翻一倍

        self.initialize_dynamic_settings()#初始化随游戏进行而变化的属性

    def initialize_dynamic_settings(self):#初始化随游戏进行而变化的设置
        self.ship_speed=1.5
        self.bullet_speed=3.0
        self.alien_speed=1.0

        self.fleet_direction=1#为1表示向右，为-1表示向左

        self.alien_points=50#记分

    def increase_speed(self):#提高速度设置和外星人分数
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.speedup_scale

        self.alien_points=int(self.alien_points*self.score_scale)
        print(self.alien_points)