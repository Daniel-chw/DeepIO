from tkinter import PhotoImage, Button, Entry, OptionMenu, StringVar

class SettingsScreen:
    """
    
    Represetns the settings screen of the game

    Attributes:
        root: main window application
        canvas: cavnas where lements are drawn
        start_function: function at the start of game
    
    """
    def __init__(self,root,canvas, start_function):
        """
        creates an instance of setting sscreen

        Parameters:
            root: main window application
            canvas:  cavnas where lements are drawn
            start_function: function at the start of game
        """
        self.root=root
        self.canvas=canvas
        self.start_function=start_function

        # Create the background image
        self.settings_menu_screen_image=PhotoImage(file='settingMenu.png')
        self.setting_menu_screen=self.canvas.create_image(
            0, 0, anchor='nw',image=self.settings_menu_screen_image)
        self.canvas.image = self.settings_menu_screen_image

        # Adds a settings button which executes the openStartScreen function
        self.exit_button_image=PhotoImage(file='exitButton.png')
        self.exit_button=Button(
            root,image=self.exit_button_image,command=self.open_start_screen)
        self.exit_button.place(x=10,y=10)

        # Creates a text box for the boss key
        self.create_text('Boss Key: ',100,200,'calibri','white',2,20)
        # Creates a drop down menu to change the boss key
        # current setting for boss key is loaded from the settings.txt file

        self.boss_entry_key=Entry(self.root,width=20,bd=4,fg='#000000')
        self.boss_entry_key.insert(0,self.load_settings()[0])
        self.boss_entry_key.place(x=160, y=183)
        self.boss_entry_key.bind('<KeyPress>',self.capture_key_bindings)

        # Creates a text box for the shoot key
        self.create_text('Shoot Button: ',123,240,'calibri','white',2,20)
        # Creates a drop down menu to change the shoot key
        # current setting for shoot key is loaded from the settings.txt file
        self.selected_option_shoot_key = StringVar()
        self.selected_option_shoot_key.set(self.load_settings()[1])
        self.remap_keys_menu_shoot_key = OptionMenu(
            self.root, self.selected_option_shoot_key, 'space', 'Button-1')
        self.remap_keys_menu_shoot_key.place(x=203, y=223)

        # Creates a text box for the cheat key
        self.create_text('Cheat key: A',112,280,'calibri','white',2,20)

        # Creates a text box for the pause key
        self.create_text('Pause key: P',112,320,'calibri','white',2,20)

        # Creates a text box and entry box for the cheat codes
        self.create_text('Cheat Code:',108,360,'calibri','white',2,20)
        self.entry=Entry(self.root,width=20,bd=4,fg='#000000')
        self.entry.place(x=180,y=345)


    def open_start_screen(self):

        """
        function used when the button is pressed
        creates an instance of the start screen
        saves the current values in the drop down menu in the settings file

        Parameters:None

        returns:None

        """

        self.save_settings()
        from startScreen import StartScreen
        self.canvas.delete('all') # remove elements from the canvas
        self.exit_button.destroy() # remove elements from the screen/root
        self.remap_keys_menu_shoot_key.destroy() # removes the drop down menu
        self.canvas.update()
        self.boss_entry_key.destroy() # removes the drop down menu
        self.entry.destroy()
        startScreen = StartScreen(self.root,self.canvas, self.start_function)


    def create_text(self,text_to_display,x,y,text_font,colour,border_width,text_size=40, tag=None):

        """
        creates a text widget with a transparent background and a border

        Parameters:
            textToDisplay
            x
            y
            textFont
            colour
            borderWidth
            textSize

        Returns:None
        
        """

        #border
        self.canvas.create_text(
            x+border_width, y, text=text_to_display, 
            font=(text_font, text_size, "bold"), fill='black', tag=tag)
        self.canvas.create_text(
            x-border_width, y, text=text_to_display, 
            font=(text_font, text_size, "bold"), fill='black', tag=tag)
        self.canvas.create_text(
            x, y+border_width, text=text_to_display, 
            font=(text_font, text_size, "bold"), fill='black', tag=tag)
        self.canvas.create_text(
            x, y-border_width, text=text_to_display, 
            font=(text_font, text_size, "bold"), fill='black', tag=tag)

        #diagonal border
        self.canvas.create_text(
            x+border_width, y-border_width, text=text_to_display, 
            font=(text_font, text_size, "bold"), fill='black', tag=tag)
        self.canvas.create_text(
            x-border_width, y+border_width, text=text_to_display, 
            font=(text_font, text_size, "bold"), fill='black', tag=tag)
        self.canvas.create_text(
            x+border_width, y+border_width, text=text_to_display, 
            font=(text_font, text_size, "bold"), fill='black', tag=tag)
        self.canvas.create_text(
            x-border_width, y-border_width, text=text_to_display, 
            font=(text_font, text_size, "bold"), fill='black', tag=tag)

        #main text
        self.canvas.create_text(
            x, y, text=text_to_display, 
            font=(text_font, text_size, "bold"), fill=colour, tag=tag)


    def save_settings(self):
        """
        saves the current values from the drop down menus into the settings file

        Parameters: None

        Returns: None
        
        """
        save_settings_file = open('savedSettings.txt', 'w')
        save_settings_file.write(self.boss_entry_key.get()+'\n')
        save_settings_file.write(self.selected_option_shoot_key.get()+'\n')
        save_settings_file.write(self.entry.get()+'\n')
        save_settings_file.close()


    def load_settings(self):
        """
        
        loads the values from the settings.txt file and returns them as a list

        Parameters: None

        Returns: None
        
        """
        save_settings_file = open('savedSettings.txt', 'r')
        save_settings_value=save_settings_file.read().splitlines()
        save_settings_file.close()
        return save_settings_value

    def capture_key_bindings(self, event):
        """
        
        Captues what key the user presses and converts it to rext

        Paramenters: event

        returns: break, to stop fuurter event going on
        
        """
        key_pressed = event.keysym
        self.boss_entry_key.delete(0, 'end')
        self.boss_entry_key.insert(0, key_pressed)
        return 'break'
