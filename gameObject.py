from tkinter import PhotoImage

class GameObject:
    """
    Represents the game object, has many child class inheriting these propeties

    Attributes:
        canvas: canvas where object is drawn
        x (float): x coorod of the object
        y (float): y coord of the object
        image (PhotoImage): image for object
        game_object: game ovject on canvas

    """

    def __init__(self,canvas,x,y,image):
        """
        initialises the game object

        Parameters:
            canvas: cavas that bullet is drawn onto
            x (float): starting x coord for bullet
            y (float): starting y coord for bullet
            image (string): image path
        """
        self.canvas=canvas
        self.x=x
        self.y=y
        self.image=PhotoImage(file=image)
        self.gameObject=self.draw()


    def draw(self):
        """
        draws game object onto screen

        parameters: None

        Returns:
            int: canvas object
        """
        return self.canvas.create_image(self.x, self.y, anchor='nw', image=self.image)

    def updatePosition(self,x,y):
        """
        updates position of gameobject on cavnas

        Parameters:
            x (float): change in x coord
            y (float): change in y coord
        """
        self.x += x
        self.y += y
        self.canvas.coords(self.gameObject, self.x, self.y)
