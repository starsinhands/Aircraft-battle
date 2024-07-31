package com.tedu.element;

import java.awt.Color;
import java.awt.Graphics;

import javax.swing.ImageIcon;

import com.tedu.manager.GameLoad;

public class Boss extends ElementObj{
	private String fx = "right";
	private String img = "boss";
	private int x;
	int back = (int) (Math.random() * 200);

	public ElementObj createElement(String str) {
		
		String[] split = str.split(",");
		this.setX(Integer.parseInt(split[0]));
		this.setY(Integer.parseInt(split[1]));
		ImageIcon icon2 = GameLoad.imgMap.get(split[2]);
		this.setW(icon2.getIconWidth());
		this.setH(icon2.getIconHeight());
		this.setIcon(icon2);
		this.setHp(100);
		return this;
	}
	
	@Override
	public void showElement(Graphics g) {
		g.drawImage(this.getIcon().getImage(), 
				this.getX(), this.getY(), 
				this.getW(), this.getH(), null);
		g.setColor(Color.RED);
		g.drawRect(106, 16, 408, 28);
		g.fillRect(110, 20, 4*this.getHp(), 20);
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
	protected void updateImage() {
		this.setIcon(GameLoad.imgMap.get(img+this.getGq()));
	}

}
