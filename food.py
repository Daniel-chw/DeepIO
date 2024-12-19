import random
from PIL import ImageTk, Image
from gameObject import GameObject
from healthBar import HealthBar


class Food(GameObject):
    """
    Represents the food object in the game with different variations
    inherits from game object

    Attributes:
        type_of_food (string): type of food
        imagePath (string): path to image file
        maxHealth (int): maximun health for food
        size (int): radius of hitbox for food
        x_offset (float): x offset for food
        y_offset (float): y offset for food
    
    """
    def __init__(self,canvas,x,y,type_of_food):
        """
        Initialises the food

        Parameters:
            canvas: cavas that bullet is drawn onto
            x (float): starting x coord for bullet
            y (float): starting y coord for bullet
            type_of_food (string): type of food
        
        """
        self.type_of_food=type_of_food

        #food properites based on there type
        if self.type_of_food == 'square':
            self.image_path = 'squareFoodImage.png'
            self.maxHealth = 10
            self.size=20
        elif self.type_of_food == 'crasher':
            self.image_path = 'crasherFoodImage.png'
            self.maxHealth = 40
            self.size=20
        elif self.type_of_food == 'pentagon':
            self.image_path = 'pentagonFoodImage.png'
            self.maxHealth = 40
            self.size=30
        else:
            self.image_path = 'squareFoodImage.png'
            self.maxHealth = 10
            self.size=30

        self.health = self.maxHealth

        super().__init__(canvas,x,y,self.image_path)

        self.offsetX=0
        self.offsetY=0

        # creates health bar if not a craser type
        if self.type_of_food != 'crasher':
            self.healthBar = HealthBar(self.canvas, 
                                       self.x-10+self.image.width()//2,
                                       self.y+self.image.height()+10,
                                       self.maxHealth)


    def draw(self):
        """
        Opens the image, converts to RGBA mode, then rotates 
        it to a random angle
        creates a transparent background then pastes image 
        ontop of it

        Parameters: None

        Returns: 
            PhotoImage: Image drawn onto the screen

        """
        original_image=Image.open(self.image_path).convert('RGBA')
        angle=random.randint(0,360)
        rotated_image=original_image.rotate(angle,expand=True)

        # creates transaparent background
        transparent_bg = Image.new("RGBA", rotated_image.size,
                                  (255, 255, 255, 0))
        transparent_bg.paste(rotated_image, (0,0), rotated_image.split()[3])

        self.image_path=ImageTk.PhotoImage(transparent_bg)
        return self.canvas.create_image(self.x, self.y, anchor='nw',
                                        image=self.image_path)