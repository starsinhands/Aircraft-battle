package com.tedu.element;

import java.awt.Graphics;
import java.util.List;
import java.util.Random;

import javax.swing.ImageIcon;

import com.tedu.manager.ElementManager;
import com.tedu.manager.GameElement;
import com.tedu.manager.GameLoad;

public class Tool extends ElementObj{
	private boolean dir=false;
	@Override
	public void showElement(Graphics g) {
		g.drawImage(this.getIcon().getImage(), 
				this.getX(), this.getY(), 
				this.getW(), this.getH(), null);
	}
	@Override
	public ElementObj createElement(String str) {
//		String[] split = str.split(",");
//		this.setX(Integer.parseInt(split[0]));
//		this.setY(Integer.parseInt(split[1]));
//		ImageIcon icon2 = GameLoad.imgMap.get(split[2]);
//		this.setW(50);
//		this.setH(50);
//		this.setIcon(icon2);
//		this.setHp(50);
////		split[2]是flag的值，代表关卡
//		return this;
		String[] split = str.split(",");
		for(String str1 : split) {//X:3
			String[] split2 = str1.split(":");// 0下标 是 x,y,f   1下标是值
			switch(split2[0]) {
			case "x": this.setX(Integer.parseInt(split2[1])+10);break;
			case "y":this.setY(Integer.parseInt(split2[1])+10);break;
			case "hp":this.setHp(Integer.parseInt(split2[1]));break;
			}
		}
		this.setW(30);
		this.setH(30);
		this.setIcon(new ImageIcon("image/prop/"+this.getHp()+".png"));
		return this;
	}
	public void changefx() {
		if(dir) {
			dir=false;
		}else {
			dir=true;
		}
	}
	@Override
	public void move() {
		if(this.getX()<20||this.getX()>600||this.getX()==200||this.getX()==400) {
			changefx();
		}
		if(dir) {
			this.setX(this.getX()+1);
			this.setY(this.getY()+1);
		}else {
			this.setX(this.getX()-1);
			this.setY(this.getY()+1);
		}
		if(this.getY()>500||this.getX()>800||this.getX()<0) {
			this.setLive(false);
		}
	}
}
