package com.tedu.controller;

import java.util.List;
import java.util.Map;

import javax.swing.ImageIcon;

import com.tedu.element.ElementObj;
import com.tedu.element.Enemy;
import com.tedu.element.Play;
import com.tedu.manager.ElementManager;
import com.tedu.manager.GameElement;
import com.tedu.manager.GameLoad;

/**
 * @说明 游戏的主线程，用于控制游戏加载，游戏关卡，游戏运行时自动化
 * 		游戏判定；游戏地图切换 资源释放和重新读取。。。
 * @author renjj
 * @继承 使用继承的方式实现多线程(一般建议使用接口实现)
 */
public class GameThread extends Thread{
	private ElementManager em;
	
//  	表示第几关
	private static int flag = 1;
	
	public static int getFlag() {
		return flag;
	}
	
	public GameThread() {
		em=ElementManager.getManager();
	}
	
	@Override
	public void run() {//游戏的run方法  主线程
		
//		设置一共5个关卡
		while(flag < 6) { //扩展,可以讲true变为一个变量用于控制结束
//		游戏开始前   读进度条，加载游戏资源(场景资源)
			gameLoad();
//		游戏进行时   游戏过程中
			gameRun();
//		游戏场景结束  游戏资源回收(场景资源)
			gameOver();
			try {
				sleep(50);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	/**
	 * 游戏的加载
	 */
	private void gameLoad() {

		GameLoad.loadImg(flag); //加载图片
		GameLoad.loadBackground(flag);

//		GameLoad.MapLoad(5);//可以变为 变量，每一关重新加载  加载地图
//		加载主角
		GameLoad.loadPlay(flag);//也可以带参数，单机还是2人
//		加载敌人NPC等
		
		GameLoad.loadEnemy(flag);
//		全部加载完成，游戏启动
		
		
		
		
		
	}
	/**
	 * @说明  游戏进行时
	 * @任务说明  游戏过程中需要做的事情：1.自动化玩家的移动，碰撞，死亡
	 *                                 2.新元素的增加(NPC死亡后出现道具)
	 *                                 3.暂停等等。。。。。
	 * 先实现主角的移动
	 * */
	private long gameTime = System.currentTimeMillis();
	boolean r = false;
	private final Object lock = new Object();
	private void gameRun() {
//		long gameTime=System.currentTimeMillis();//给int类型就可以啦
		while(true) {// 预留扩展   true可以变为变量，用于控制管关卡结束等
			// 暂停
			while(Play.getPauseGame()) {
				try {
					Thread.sleep(1);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
			
			Map<GameElement, List<ElementObj>> all = em.getGameElements();
			List<ElementObj> enemys = em.getElementsByKey(GameElement.ENEMY);
			List<ElementObj> files = em.getElementsByKey(GameElement.PLAYFILE);
			List<ElementObj> maps = em.getElementsByKey(GameElement.MAPS);
			List<ElementObj> boss = em.getElementsByKey(GameElement.BOSS);
			List<ElementObj> tool = em.getElementsByKey(GameElement.TOOL);
			List<ElementObj> play = em.getElementsByKey(GameElement.PLAY);
			moveAndUpdate(all,gameTime);//	游戏元素自动化方法
			ElementPK(boss, files);
			ElementPK(enemys,files);
			ElementPK(files,maps);

			ElementGetTool(play,tool);
			gameTime++;//唯一的时间控制
			try {
				sleep(10);//默认理解为 1秒刷新100次 
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			// 小飞机打完喽，来boss喽！！
			if(em.getElementsByKey(GameElement.ENEMY).size()==0 && !r) {
				GameLoad.loadBoss(flag);
				r = true;
			}
			// boss死亡，胜利
			if(em.getElementsByKey(GameElement.BOSS).size() == 0 && r) {
				r=false;
				return;
			}
		}
	}
	
	public void ElementPK(List<ElementObj> listA,List<ElementObj>listB) {
//		请大家在这里使用循环，做一对一判定，如果为真，就设置2个对象的死亡状态
		for(int i=0;i<listA.size();i++) {
			ElementObj enemy=listA.get(i);
			for(int j=0;j<listB.size();j++) {
				ElementObj file=listB.get(j);
				if(enemy.pk(file)) {
//					问题： 如果是boos，那么也一枪一个吗？？？？
//					将 setLive(false) 变为一个受攻击方法，还可以传入另外一个对象的攻击力
//					当收攻击方法里执行时，如果血量减为0 再进行设置生存为 false
//					扩展 留给大家
//					System.out.println(listB);
					enemy.setHp(enemy.getHp()-10);
					if(enemy.getHp()<0) {
						enemy.setLive(false);
					}
					
					file.setLive(false);
					break;
				}
			}
		}
	}
	public void ElementGetTool(List<ElementObj> listA,List<ElementObj>listB) {
//		请大家在这里使用循环，做一对一判定，如果为真，就设置2个对象的死亡状态
		for(int i=0;i<listA.size();i++) {
			ElementObj play=listA.get(i);
			for(int j=0;j<listB.size();j++) {
				ElementObj tool=listB.get(j);
				if(play.pk(tool)) {
//					问题： 如果是boos，那么也一枪一个吗？？？？
//					将 setLive(false) 变为一个受攻击方法，还可以传入另外一个对象的攻击力
//					当收攻击方法里执行时，如果血量减为0 再进行设置生存为 false
//					扩展 留给大家
					System.out.println(listB);
					tool.setLive(false);
					if(tool.getHp()==0){
						List<ElementObj> playlist = ElementManager.getManager().getElementsByKey(GameElement.PLAY);
						for(int k = 0 ;k<playlist.size();k++) {
							ElementObj player = playlist.get(k);
							player.setSd(player.getSd()*2);
//							System.out.println(player.getSd());
						}
					}
					if(tool.getHp()==2){
						List<ElementObj> bosslist = ElementManager.getManager().getElementsByKey(GameElement.BOSS);
						for(int k = 0 ;k<bosslist.size();k++) {
							ElementObj boss = bosslist.get(k);
							boss.setHp(boss.getHp()/2);
						}
					}
					if(tool.getHp()==1){
						List<ElementObj> playlist = ElementManager.getManager().getElementsByKey(GameElement.PLAY);
						for(int k = 0 ;k<playlist.size();k++) {
							ElementObj player = playlist.get(k);
							player.setHp(player.getHp()+10);
						}
					}
					break;
				}
			}
		}
	}
	
	
//	游戏元素自动化方法
	public void moveAndUpdate(Map<GameElement, List<ElementObj>> all, long g) {
		//GameElement.values();  隐藏方法，返回一个数组，顺序是定义枚举的顺序
		for(GameElement ge: GameElement.values()) {
			List<ElementObj> list = all.get(ge);
			for(int i = 0; i < list.size(); i++) {
				ElementObj obj = list.get(i);
				if(!obj.isLive()) {
					obj.die();
					list.remove(i--);
					continue;
				}

					obj.model(g);			
			}
		}
		gameTime=System.currentTimeMillis();		
	}
	
	
	/**游戏切换关卡*/
	private void gameOver() {
//		System.out.println(flag);
		try {
			sleep(3000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		if(flag > 4) {
			System.exit(0);
		}
		flag++;
		System.out.println(flag);
		GameLoad.clear();
	}
	

	
}





