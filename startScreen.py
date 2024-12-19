from tkinter import PhotoImage, Button, Entry
from settingsScreen import SettingsScreen

class StartScreen:
    """
    
    Represetns the start screen of the game

    Attributes:
        root: main window application
        canvas: cavnas where lements are drawn
        start_function: function at the start of game
    
    """
    def __init__(self, root, canvas,start_function):
        """
    
        initialises the start screen of the game

        Attributes:
            root: main window application
            canvas: cavnas where lements are drawn
            start_function: function at the start of game
        
        """
        self.root=root
        self.canvas=canvas
        self.start_function=start_function

        # loads the start menu image and puts it on the screen
        self.start_screen_image=PhotoImage(file='startMenu.png')
        self.start_screen=self.canvas.create_image(
            0, 0, anchor='nw', image=self.start_screen_image)

        # Creates the text box where the player types there name
        self.entry=Entry(self.root,width=50,bd=4,fg='#7a7a7a')
        self.entry.insert(0,'This is the tale of...')
        # determines what happens if the player clickes on the text box
        self.entry.bind('<FocusIn>', lambda event: self.hover_in_entry_box())
        self.entry.place(x=200,y=300)

        self.name=''

        # Adds a start button
        self.start_button=Button(root)
        self.start_button_config()
        self.start_button.place(x=360,y=400)

        # Adds a load button
        self.load_button=Button(root)
        self.load_button_config()
        self.load_button.place(x=360,y=440)

        # Adds a settings button
        self.setting_image=PhotoImage(file='settingButton.png')
        self.setting_button=Button(
            root,image=self.setting_image,command=self.open_settings)
        self.setting_button.place(x=10,y=10)


    # Function used to determine what happens when the start button is pressed
    # Sets the name from the entry box to self.name
    # Deletes the content of the canvas and other widgets
    # Starts the game
    def start_game(self):
        """
        Function used to determine what happens when the start button is pressed
        Sets the name from the entry box to self.name
        Deletes the content of the canvas and other widgets
        Starts the game

        Parameters: None

        Returns: None
        
        """
        if self.entry.get() == 'This is the tale of...':
            self.name='Tank'
        else:
            self.name=self.entry.get()
        self.canvas.delete(self.start_screen) # remove elements from the canvas
        self.start_button.destroy() # remove elements from the screen/root
        self.setting_button.destroy()
        self.entry.destroy()
        self.load_button.destroy()
        #initializeGame(self.name)
        self.start_function(self.name)

    def load_game(self):
        """
        Loads game by using player name, clearing canvas

        Parameters: None

        Returns: None
        
        """
        if self.entry.get() == 'This is the tale of...':
            self.name='Tank'
        else:
            self.name=self.entry.get()
        self.canvas.delete(self.start_screen) # remove elements from the canvas
        self.start_button.destroy() # remove elements from the screen/root
        self.setting_button.destroy()
        self.entry.destroy()
        self.load_button.destroy()
        #initializeGame(self.name)
        self.start_function(self.name, True)


    def hover_in_entry_box(self):
        """
        Function use to determin what happens when to mouse clicks the Entry Box
        Text is deleted and the text colour changes to black

        Parameters: None

        Return: None
        
        """
        self.entry.delete(0,'end')
        self.entry.config(fg='#000000')

    def start_button_config(self):
        """
        Sets up the properties of the start button
        
        paramters: None

        Return: None
        
        """
        self.start_button.config(text='Play!')
        self.start_button.config(command=self.start_game)
        self.start_button.config(width=10)
        self.start_button.config(bg='#26d45d')
        self.start_button.config(activebackground='#29c259')
        self.start_button.config(bd=3)

    def load_button_config(self):
        """
        sets up properites for load button

        parameters: None
        
        returns : None
        
        """
        self.load_button.config(text='Load!')
        self.load_button.config(command=self.load_game)
        self.load_button.config(width=10)
        self.load_button.config(bg='#268cd4')
        self.load_button.config(activebackground='#2982c2')
        self.load_button.config(bd=3)


    def open_settings(self):
        """
        Opens a settings menu and clears screen

        parameters: None

        returns: None
        
        """

        self.canvas.delete(self.start_screen) # remove elements from the canvas
        self.start_button.destroy() # remove elements from the screen/root
        self.setting_button.destroy()
        self.entry.destroy()
        self.load_button.destroy()
        settingsMenu=SettingsScreen(self.root,self.canvas, self.start_function)
