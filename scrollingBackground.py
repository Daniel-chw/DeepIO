from gameObject import GameObject

class BackgroundTile(GameObject):
    """
    Represents background tile in the game,
    inherits from game object

    Attributes:
        canvas: canvas where tile is drawn onto
        x (float): x coord
        y (float): y coord
    
    """
    def __init__(self, canvas, x, y):
        """
        initiailises the background tile

        parameters:
            canvas: canvas where tile is drawn onto
            x (float): x coord
            y (float): y coord
        
        """
        super().__init__(canvas,x,y,'tileImage.png')
