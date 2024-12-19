from gameObject import GameObject

class Bullet(GameObject):
    """
    Is the bullet from the player, inherits from the GameObject class

    Attributes:
        x_offset (float): x offset for bullet
        y_offset (float): y offset for bullet
    """
    def __init__(self, canvas,x,y):
        """
        Initialises the bullet

        Parameters:
            canvas: cavas that bullet is drawn onto
            x (float): starting x coord for bullet
            y (float): starting y coord for bullet
        
        """
        super().__init__(canvas,x,y,'bulletImage.png')
        self.x_offset=0
        self.y_offset=0