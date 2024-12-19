from tkinter import Canvas, PhotoImage
import math
import time
from PIL import ImageTk, Image
from bullet import Bullet
from healthBar import HealthBar


class Tank:
    """
    Tank object

    Attributes:
        canvas: canvas where tank is drawn onto
        size (int): size of the tank
        colour (str): colour of the tank
        x (float): x coord
        y (float): y coord
        speed (int): speed of tank
        angle (float): angle of tank
        bullets (list): bullets of tank fired
        max bullets (int): max bullets
        bullet cooldown (int): cooldown
        last shot fired (int): time when last shot fired
        health bar: health bar of tank
        last hit time (int): time between last hits
        damage cooldown (int): cooldown between hits
        points (int): score
        pause on (bool): pause on flag
        """
    def __init__(self,canvas,start_pos_x,start_pos_y,size=40,colour="blue",max_bullets=20):
        """
        
        initiliases tank instance

        parameters:
        canvas: canvas where tank is drawn onto
        size (int): size of the tank
        colour (str): colour of the tank
        
        """
        self.canvas=canvas
        self.size=size
        self.colour=colour
        self.x=start_pos_x
        self.y=start_pos_y
        self.speed=1
        self.angle=0

        self.original_image = Image.open(
            "tankImage.png").resize((self.size, self.size), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.original_image)

        self.body=self.create_tank()

        # Bullet attributes with fire rate
        self.bullets = [] # List containing bullet objects on the current canvas
        self.max_bullets = max_bullets # Max amount of bullets that can appear on the canvas
        self.bullet_cool_down=300 # Cooldown per bullet fired
        self.last_shot_fired=0 # Timer between bullets fired

        # Health,collision rate with food and points attributes
        self.health_bar = HealthBar(self.canvas, self.x-15, self.y+20, 10)
        self.last_hit_time = 0
        self.damage_cool_down = 250
        self.points=0

        self.pause_on = True

        self.update()


    def create_tank(self):
        """
        creates a tank image on the canvas

        Parameters: None

        Returns:
            int:
        
        """
        return self.canvas.create_image(self.x,self.y,image=self.image)


    def rotate_tank(self):
        """
        rotates the tank towards the mouse
        Uses the pillow(PIL) library for rotation, 
        then converts to TK image, then updates the canvas

        Parameters: None

        reutnes: None
        
        """
        rotated_image=self.original_image.rotate(-math.degrees(self.angle))
        self.image=ImageTk.PhotoImage(rotated_image)
        self.canvas.itemconfig(self.body, image=self.image)
        self.canvas.coords(self.body, self.x, self.y)


    def update_angle(self):
        """
        changes the angle of the tank to face the mouse pointer
        
        Parameters: None

        Returns: None
        
        """
        mouse_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        mouse_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        self.angle = math.atan2(mouse_y-self.y, mouse_x-self.x)



    def distance_from_mouse(self):
        """
        returns distance tank is from the mouse
        
        parameters: None

        Returns: float, disantce
        
        """
        mouse_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        mouse_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        return math.sqrt((mouse_x-self.x)**2 + (mouse_y-self.y)**2)


    def shoot(self,x,y, bullet_speed):
        """
        Creates a bullet object
        If the time between bullet shots is bigger than the cooldown then
        A bullet object is created and added to the bullets array
        And lowered in the canvas so it is behind the tank
        And given an inital direction with the offsets being the tanks direction
        
        paramertes: x,y,bulletSpeed
        returns:None

        """
        current_time=int(round(time.time()*1000)) # Gets the current time in ms
        if current_time-self.last_shot_fired>=self.bullet_cool_down:
            if len(self.bullets)>self.max_bullets:
                self.removeBullet(0)
            self.bullets.append(Bullet(self.canvas,x,y))
            self.bullets[-1].yOffset = math.sin(self.angle) * bullet_speed
            self.bullets[-1].xOffset = math.cos(self.angle) * bullet_speed
            self.canvas.tag_lower(self.bullets[-1].gameObject, self.body)
            self.last_shot_fired = current_time


    def removeBullet(self,index):
        """
        remove bullets

        Parameters: index
        returns: None
        
        """
        removed_bullet = self.bullets.pop(index)
        self.canvas.delete(removed_bullet.gameObject)


    def update(self):
        """
        updates the position of the tank every 10ms
        parameters: None
        returns: None
        
        """

        if not self.pause_on:
            return

        self.update_angle()
        self.rotate_tank()

        self.canvas.after(10, self.update)
