import math
from PIL import Image, ImageTk
from gameObject import GameObject

class HealthBar(GameObject):
    """
    health bar game object inheritiing from game object class

    Attributes:
        max_health (int): Maximum health value.
        current_health (int): Current health value.
    """
    def __init__(self, canvas,x,y, maxhealth):
        """
        Initialises the health bar

        Parameters:
            canvas: cavas that bullet is drawn onto
            x (float): starting x coord for bullet
            y (float): starting y coord for bullet
            max_health (int): max health
        
        """
        self.max_health = maxhealth
        self.currenthealth = maxhealth
        super().__init__(canvas,x,y,'healthBar.gif')
        self.gameObject = self.draw(0,0)

    def draw(self, offsetX=0, offsetY=0):
        """
        draws health bar onto screen

        parameters: None

        Returns:
            int: canvas object
        """
        image=Image.open('healthBar.gif')
        image.seek((math.floor((-6)*(self.currenthealth/self.max_health))+6)
                   if self.currenthealth>0 else 6)
        self.image = ImageTk.PhotoImage(image)
        return self.canvas.create_image(self.x+offsetX, self.y+offsetY,
                                        anchor='nw', image=self.image)
