import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:#管理游戏资源和行为的类
    def __init__(self):#初始化游戏并创建游戏资源
        pygame.init()#初始化背景设置
        self.settings=Settings()#导入Settings类，创建一个Settings实例赋给self.settings

        self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)#创建显示窗口，全屏
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats=GameStats(self)#创建一个用于存储游戏统计信息的实例
        self.sb=Scoreboard(self)#并创建记分牌

        self.ship=Ship(self)#创建Ship()实例，self指向的是当前AlienInvasion实例，这个参数让Ship能够访问游戏资源，如对象screen
        self.bullets=pygame.sprite.Group()#创建用于存储子弹的编组，其他都是同理
        self.aliens=pygame.sprite.Group()

        self._create_fleet()
        self.play_button=Button(self,"Play")#创建Play按钮

        self.bg_color=(230,230,230)#设置背景色

    def run_game(self):#开始游戏的主循环
        while True:
            #监视键盘和鼠标事件
            self._check_events()

            if self.stats.game_active:
                self.ship.update()#飞船的位置将在检测到键盘事件后（但在更新屏幕前）更新，这样玩家输入时飞船的位置将更新，从而确保使用更新后的位置将飞船绘制到屏幕上
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


    def _check_events(self):#响应按键和鼠标操作
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:#Pygame检测到一个MOUSEBUTTONDOWN事件
                mouse_pos=pygame.mouse.get_pos()#返回一个元组，包含玩家单击时鼠标的x坐标和y坐标，将值传递给方法_check_play_button()
                self._check_play_button(mouse_pos)
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self,mouse_pos):#在玩家单击Play按钮时开始新游戏
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()#重置游戏设置

            #重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active=True
            self.sb.prep_score()#开始新游戏时，重置游戏统计信息再调用prep_score()。此时生成的记分牌上显示的得分为零
            self.sb.prep_level()
            self.sb.prep_ships()

            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)#隐藏鼠标光标

    def _check_keydown_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_q:#按Q键可以结束游戏
            sys.exit()
        elif event.key==pygame.K_SPACE:#在玩家按空格键时调用_fire_bullet()
            self._fire_bullet()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):#创建一颗子弹，并将其加入编组bullets中
        if len(self.bullets) < self.settings.bullets_allowed:#创建新子弹前检查未消失的子弹数是否小于该设置
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):#更新子弹的位置并删除消失的子弹
        self.bullets.update()#更新子弹的位置

        #删除消失的子弹
        for bullet in self.bullets.copy():#copy()方法使得能在循环中修改bulltes
            if bullet.rect.bottom <= 0:#检查每颗子弹看看它是否从屏幕顶端消失
                self.bullets.remove(bullet)#如果是，将其从bullets中删除

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):#响应子弹和外星人碰撞
        #删除发生碰撞的子弹和外星人
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)

        #检查是否有子弹集中了外星人，如果是，就删除相应的子弹和外星人
        if collisions:
            for aliens in collisions.values():
                self.stats.score+=self.settings.alien_points*len(aliens)#将消灭的每个外星人都计入得分
            self.sb.prep_score()
            self.sb.check_high_score()#每当有外星人被消灭时，都需要在更新得分后调用check_high_score()

        if not self.aliens:#一群外星人被消灭后再显示另一群外星人
            #删除现有的子弹并新建另一群外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #提高等级
            self.stats.level+=1
            self.sb.prep_level()

    def _update_aliens(self):#检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship,self.aliens):#检测外星人和飞船之间的碰撞
            self._ship_hit()

        self._check_aliens_bottom()#检查是否有外星人到达了屏幕底端

    def _create_fleet(self):#创建外星人群
        #创建一个外星人并计算一行可以容纳多少个外星人
        #外星人的间距为外星人宽度
        alien=Alien(self)#创建一个外星人
        alien_width,alien_height=alien.rect.size#属性size是一个元组，包含rect对象的宽度和高度
        #屏幕宽度存储在settings.screen_width中，但需要在屏幕两边都留下一定的边距（将其设置为外形人的宽度）。因为有两个边距，所以可用于放置外星人的水平空间为屏幕宽度减去外星人宽度的两倍
        available_space_x=self.settings.screen_width-(2*alien_width)
        #还需要在外星人之间留一定空间（设为外星人宽度）。因此，显示一个外星人所需的水平空间为外星人宽度的两倍：一个宽度用于放置外星人，另一个宽度为外星人右边的空白区域。用空间除以外星人宽度的两倍得到一个表示外星人个数的整数
        number_aliens_x=available_space_x//(2*alien_width)

        ship_height=self.ship.rect.height
        """为计算可容纳的行数，要先计算可用的垂直空间：用屏幕高度减去第一行外星人的上边距（外星人高度）、飞船的高度以及外星人群最初与飞船之间的距离（外星人高度的两倍）。
        这样将在飞船的上方留下一定的空白区域，给玩家留出射杀外星人的时间"""
        available_space_y=(self.settings.screen_height-(3*alien_height)-ship_height)
        #每行下方都要留出一定的空白区域（设为外星人的高度）。为计算可容纳的行数，将可用的垂直空间除以外星人高度的两倍
        number_rows=available_space_y//(2*alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):#创建一行外星人
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):#创建一个外星人并将其放在当前行
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        alien.x=alien_width+2*alien_width*alien_number#将每个外星人都往右推一个外星人宽度，接下来将外星人宽度乘以2得到每个外星人占据的空间（其中包括右边的空白区域），再据此计算当前外星人在当前行的位置
        alien.rect.x=alien.x#使用外星人的属性x来设置其rect的位置
        #修改外星人的y坐标并在第一行外星人上方留出与外星人等高的空白区域。相邻外星人行的y坐标相差外星人高度的两倍，因此将外星人高度×2，再×行号。第一行的行号是0，因此第一行的垂直位置不变，而其他行都沿屏幕依次向下放置
        alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):#有外星人到达边缘时采取相应的措施
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):#将整群外星人下移，并改变他们的方向
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _update_screen(self):#更新屏幕上的图像，并切换到新屏幕
        #每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():#为在屏幕上绘制发射的所有子弹，遍历编组bullets中的精灵，并对每个精灵调用draw_bullet()
            bullet.draw_bullet()
        self.aliens.draw(self.screen)#draw()接受一个参数，这个参数指定了要将编组中的元素绘制到哪个surface上

        self.sb.show_score()#显示得分

        if not self.stats.game_active:#如果游戏处于非活动状态，就绘制Play按钮
            self.play_button.draw_button()

        #让最近绘制的屏幕可见
        pygame.display.flip()

    def _ship_hit(self):#响应飞船被外星人撞到
        if self.stats.ships_left>0:
            #将ships_left减1并更新记分牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人，并将飞船放到屏幕低端的中央
            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)#暂停
        else:
            self.stats.game_active=False#如果玩家没有了飞船，就将游戏状态设为False
            pygame.mouse.set_visible=True

    def _check_aliens_bottom(self):#检查是否有外星人到达了屏幕底端
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                self._ship_hit()#像飞船被撞到一样处理
                break


if __name__=='__main__':#创建游戏实例并运行游戏
    ai=AlienInvasion()
    ai.run_game()