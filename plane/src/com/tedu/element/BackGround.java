package com.tedu.element;

import java.awt.Graphics;

import javax.swing.ImageIcon;

import com.tedu.manager.GameLoad;

public class BackGround extends ElementObj{
	
	public ElementObj createElement(String str) {
		String[] split = str.split(",");
		this.setX(0);
		this.setY(0);
		ImageIcon icon2 = new ImageIcon("image/background/"+str+".png");
		this.setW(icon2.getIconWidth());
		this.setH(icon2.getIconHeight());
		this.setIcon(icon2);
		return this;
	}
	
	
	@Override
	public void showElement(Graphics g) {
		g.drawImage(this.getIcon().getImage(), 
				this.getX(), this.getY(), 
				this.getW(), this.getH(), null);
	}

}
