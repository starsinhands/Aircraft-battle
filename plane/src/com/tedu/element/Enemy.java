package com.tedu.element;

import java.awt.Graphics;
import java.util.List;
import java.util.Random;

import javax.swing.ImageIcon;

import com.tedu.manager.ElementManager;
import com.tedu.manager.GameElement;
import com.tedu.manager.GameLoad;

public class Enemy extends ElementObj{
	private String fx = "right";
	private int x;
	int back = (int) (Math.random() * 200);
	
	@Override
	public void showElement(Graphics g) {
		g.drawImage(this.getIcon().getImage(), 
				this.getX(), this.getY(), 
				this.getW(), this.getH(), null);
	}
	
	@Override
	public ElementObj createElement(String str) {
		Random ran=new Random();
		int x=ran.nextInt(600);
		int y=ran.nextInt(300);
		this.setX(x);
		this.setY(y);
		this.setW(50);
		this.setH(50);
		this.setHp(1);
		this.setIcon(new ImageIcon("image/enemy/"+str+".png"));
		return this;
	}
	
	@Override
	public void move() {
		if(fx.equals("right")) {
			if((this.getX() < 770 - this.getW()) && (this.getX() - x < back)) {
				this.setX(this.getX() + 1);
			}
			else {
				this.fx = "left";
				back = (int) (Math.random() * 400);
			}
		}
		if(fx.equals("left")) {
			if(this.getX() > 0 && (x - this.getX() < back)) {
				this.setX(this.getX() - 1);
			}
			else {
				this.fx = "right";
				back = (int) (Math.random() * 400);
			}
		}
	}
	@Override
	public void die() {
		ElementObj obj = GameLoad.getObj("tool");
		ElementObj tool = obj.createElement(this.toString());
		ElementManager.getManager().addElement(tool, GameElement.TOOL);
		
	}
	
	@Override
	public String toString() {
		int a = new Random().nextInt(3);
		int x = this.getX();
		int y = this.getY();
		return "x:"+x+",y:"+y+",hp:"+a;
	}
}
