from tkinter import Tk, Canvas, Label, PhotoImage, Button
import random
import math
import time

from tank import Tank
from scrollingBackground import BackgroundTile
from food import Food
from bullet import Bullet
from healthBar import HealthBar
from startScreen import StartScreen


#cheats are: points,bullet,fast

#----------------FUNCTIONS-----------------#


def set_up_window():
    """
    
    Configures the main games window settings

    Parameters:
        None

    Returns:
        None

    """
    window.geometry("800x600")
    window.configure(background="#D5D5D5")
    window.title("Deep.io")
    window.resizable(False, False)
    #window.iconbitmap('@icon.xbm')
 

def calculate_mouse_angle():
    """
    
    Calculates mouse angle relative the the middle of the screen

    Parameters:
        None

    Returns:
        float: angle in radians between mouse and middle of the screen

    """
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    angle = math.atan2(mouse_y-300, mouse_x-400)
    return angle


def mouse_position():
    """
    
    Calculates the mouse position on the screen relative to the canvas

    Parameters:
        None

    Returns:
        tuple: Holds the mouses X and Y position

    """
    mouse_x=canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y=canvas.winfo_pointery() - canvas.winfo_rooty()
    return (mouse_x,mouse_y)


def distance_from_mouse():
    """
    
    Calculates the distance the mouse is from the middle of the screen

    Parameters:
        None

    Returns:
        float: distance from mouse to centre of screen

    """
    distance_x = canvas.winfo_pointerx() - canvas.winfo_rootx()-400
    distance_y=canvas.winfo_pointery() - canvas.winfo_rooty()-300
    return math.sqrt(math.pow(distance_x, 2)+math.pow(distance_y, 2))


def calculate_change_in_position(position,mouse_position, max_boundry, 
    scroll_speed, angle, is_x):
    """
    
    If the mouse points away from the border, then the player can start moving
    The new position is also calculated by the angle the mouse makes with the tank

    Parameters:
        position (float): current X or Y position of the player
        mouse_position (float): current X or Y position of the mouse
        max_boundary (float): Bound for the players position
        scroll_speed (float): Speed of movement
        angle (float): Angle of mouse relative to tank
        is_x (bool): Decides if positions are X or Y

    Returns:
        float: distance from mouse to centre of screen

    """
    if position > max_boundry:
        change = 0
        if mouse_position > max_boundry:
            if is_x:
                change = scroll_speed * -math.cos(angle)
            else: change = scroll_speed * -math.sin(angle)
    elif position < -max_boundry:
        change = 0
        if mouse_position < max_boundry:
            if is_x:
                change = scroll_speed * -math.cos(angle)
            else: change = scroll_speed * -math.sin(angle)
    else:
            if is_x:
                change = scroll_speed * -math.cos(angle)
            else: change = scroll_speed * -math.sin(angle)
    return change


def collision_between(object1, object2, collision_distance=30):
    """
    
    determines if the distance between two objects 
    is less than the collision distance

    Parameters:
        object1: A game object
        object2: A game object
        collision_distance (float): Max distance to be a collision

    Returns:
        bool: if objects collide then return True, else False

    """
    object_centre_1 = (object1.x, object1.y)
    object_centre_2 = (
        object2.x+object1.image.width()//2,
        object2.y+object1.image.height()//2)
    distance_x=object_centre_1[0]-object_centre_2[0]
    distance_y=object_centre_1[1]-object_centre_2[1]
    distance=math.sqrt(math.pow(distance_x, 2)+math.pow(distance_y, 2))
    return distance < collision_distance


def create_custom_text(text_to_display,x,y,text_font,colour,
    border_width,text_size=40, tag=None):
    """
    
    creates a text widget with a transparent background and a border

    Parameters:
        text_to_display (str): The text to display on the canvas.
        x (int): X position of text.
        y (int): Y position of text.
        text_font (str): font for the text
        colour (str): colour for the text
        border_width (int): width of the text border
        text_size (int): size of the font
        tag (str): tag for the text

    Returns:
        None

    """
    canvas.create_text(x+border_width, y, text=text_to_display,
        font=(text_font, text_size, "bold"), fill='black', tag=tag)
    canvas.create_text(x-border_width, y, text=text_to_display,
        font=(text_font, text_size, "bold"), fill='black', tag=tag)
    canvas.create_text(x, y+border_width, text=text_to_display,
        font=(text_font, text_size, "bold"), fill='black', tag=tag)
    canvas.create_text(x, y-border_width, text=text_to_display,
        font=(text_font, text_size, "bold"), fill='black', tag=tag)

    canvas.create_text(x+border_width, y-border_width, text=text_to_display,
        font=(text_font, text_size, "bold"), fill='black', tag=tag)
    canvas.create_text(x-border_width, y+border_width, text=text_to_display,
        font=(text_font, text_size, "bold"), fill='black', tag=tag)
    canvas.create_text(x+border_width, y+border_width, text=text_to_display,
        font=(text_font, text_size, "bold"), fill='black', tag=tag)
    canvas.create_text(x-border_width, y-border_width, text=text_to_display,
        font=(text_font, text_size, "bold"), fill='black', tag=tag)

    canvas.create_text(x, y, text=text_to_display, font=(
        text_font, text_size, "bold"), fill=colour, tag=tag)


def boss_key(image):
    """
    
    Switches window to a work related window

    Parameters:
        image: the image used as work related window

    Returns:
        None

    """
    global BOSS_WINDOW_OPEN, BOSS_WINDOW
    if BOSS_WINDOW_OPEN is False:
        BOSS_WINDOW=Label(window,image=image)
        BOSS_WINDOW.place(x=0,y=0)
        BOSS_WINDOW_OPEN=True
    elif BOSS_WINDOW_OPEN is True:
        BOSS_WINDOW.place_forget()
        BOSS_WINDOW_OPEN=False


def load_settings():
    """
    
    loads the values from the settings.txt file and returns them as a list

    Parameters:
        None

    Returns:
        list: list of settings from file

    """
    save_settings_file = open('savedSettings.txt', 'r')
    save_settings_values=save_settings_file.read().splitlines()
    save_settings_file.close()
    return save_settings_values


def cheat_settings():
    """
    
    Changes the attributes of the tanks objects to give it more bullets per second and max bullets

    Parameters:
        None

    Returns:
        None

    """
    if load_settings()[2]=='bullet':
        tank.bullet_cool_down=50
        tank.max_bullets=50


def pause():
    """
    
    toggles on and off the paused variable, and when toggled back on, it restarts the update loops
    this function activates whenever the p button is pressed

    Parameters:
        None

    Returns:
        None

    """

    global pause_on
    pause_on = not pause_on
    tank.pauseOn = not pause_on
    if pause_on is False or tank.pauseOn is False:
        update()
        tank.update()


def exit_game():
    """
    
    Exits the game and goes the start menu

    Parameters:
        None

    Returns:
        None

    """
    pauseOn = True
    pause()
    canvas.delete('all')
    save_game()
    startScreen = StartScreen(window, canvas, initiialise_game)


def save_game():
    """
    
    Saves the current state of the game, like the global position

    Parameters:
        None

    Returns:
        None

    """

    save_game_file = open('savedGame.txt', 'w')
    save_game_file.write(str(tank.points)+'\n')
    save_game_file.write(str(x_position)+'\n')
    save_game_file.write(str(y_position)+'\n')
    save_game_file.write(str(change_in_x)+'\n')
    save_game_file.write(str(change_in_y)+'\n')
    save_game_file.write(str(tank.health_bar.currenthealth)+'\n')
    save_game_file.close()


def load_game():
    """
    load game

    param:None
    return: points
    
    """
    save_game_file = open('savedGame.txt', 'r')
    points = save_game_file.read().split()
    save_game_file.close()
    return points


def update_high_score(score, user_name):
    """

    updates the high score list
    converts the list of data, to a tuple, 
    then sorts each tuple by the first element 
    and adds the new score to the list of sorted tuples

    userName (string): name of the player

    Returns: None

    """

    high_scores_file = open('highscores.txt', 'r')
    high_scores = list(high_scores_file.read().split())

    list_of_tuples=[]
    for highscore in high_scores:
        parts_of_score = highscore.split(',')
        score_number = int(parts_of_score[0])
        score_name = parts_of_score[1]
        list_of_tuples.append((score_number,score_name))

    list_of_tuples.append((int(score), user_name))

    list_of_tuples=sorted(list_of_tuples, key=lambda x:x[0], reverse=True)

    upadted_high_score=[f'{highscore},{user}' for highscore,
        user in list_of_tuples]
    upadted_high_score=upadted_high_score[:5]

    high_scores_file.close()
    high_scores_file = open('highscores.txt', 'w')

    for highscore in upadted_high_score:
        high_scores_file.write(f'{highscore}\n')

    high_scores_file.close()


def display_leaderboard():
    """
    
    displays the top 5 high scores in the game

    Parameters:
        None

    Returns:
        None

    """
    high_score_file = open('highscores.txt', 'r')
    high_scores = list(high_score_file.read().split())
    create_custom_text('Leaderboard:',700,20,'calibri','white',2,12)
    create_custom_text(str(high_scores[0]),700,50,'calibri','white',2,12)
    create_custom_text(str(high_scores[1]),700,70,'calibri','white',2,12)
    create_custom_text(str(high_scores[2]),700,90,'calibri','white',2,12)
    create_custom_text(str(high_scores[3]),700,110,'calibri','white',2,12)
    create_custom_text(str(high_scores[4]),700,130,'calibri','white',2,12)
    high_score_file.close()


def spawn_crasher(canvas, speed):
    """
    
    spawns crahsers from a random position on the border, 
    then gives it an initial offset towards the player

    Parameters:
        canvas: the canvas object
        speed (float): speed crasher moves at

    Returns:
        crasher Object

    """
    side = random.choice(['up', 'down', 'left', 'right'])
    if side=='up':
        x=random.randint(0, 800)
        y=-50
    elif side=='down':
        x=random.randint(0, 800)
        y=650
    elif side=='left':
        x=-50
        y=random.randint(0, 600)
    elif side=='right':
        x=850
        y=random.randint(0, 600)

    crasher = Food(canvas, x, y, 'crasher')
    vector_x=400-x
    vector_y=300-y
    current_length = math.sqrt(vector_x**2 + vector_y**2)
    crasher.offsetX=(vector_x/current_length)*speed
    crasher.offsetY=(vector_y/current_length)*speed
    crasher.currentSpawnTime=time.time()
    return crasher


#------------Global Varaibles--------------#

# Sets up the window and canvas
window = Tk()
set_up_window()
canvas = Canvas(window, width=800, height=600, background="#D3D3D3")
canvas.pack(side="bottom")

# sets up the images used for buttons and boss key
boss_window_image=PhotoImage(file='workImage.png')
exit_button_image=PhotoImage(file='exitButton.png')
BOSS_WINDOW_OPEN=False
BOSS_WINDOW=None

# player name
PLAYER_USER_NAME=None



def initiialise_game(player_name, load_game_saved_state=False):
    """
    Code ran when the start button is pressed
    This initializes the game, so creates all the variables and objects
    Then calls the update funciton to start the main game loop
    
    Parameters:
        playerName (string): name of the player
        loadGameSavedState (bool): if game is loaded

    Returns: None
    
    """

    # variables that will be used in the main game loop,
    # made global so update function can access them
    global tank, foods, game_objects, x_position, y_position, \
        change_in_x, change_in_y, pause_on, PLAYER_USER_NAME, cheat_code, crashers

    PLAYER_USER_NAME = player_name
    cheat_code = load_settings()[2]

    # Adds a settings button which executes the openStartScreen function
    exit_button=Button(window,image=exit_button_image, command=exit_game)
    exit_button.place(x=10,y=10)

    # bind the set key binds to shoot and boss key functions
    window.bind(f'<{load_settings()[1]}>',
        lambda event: tank.shoot(400,300,14))
    window.bind(f'<{load_settings()[0]}>',
        lambda event: boss_key(boss_window_image))

    pause_on = False
    window.bind('p', lambda event: pause())


    # resets variables
    x_position,y_position=0,0
    change_in_x,change_in_y=0,0
    scrollSpeed = 5

    # Creates 4 tiles for sccrolling background
    bg1 = BackgroundTile(canvas, 0,-100)
    bg2 = BackgroundTile(canvas, 400,-100)
    bg3 = BackgroundTile(canvas, 0,300)
    bg4 = BackgroundTile(canvas, 400,300)
    game_objects = [bg1,bg2,bg3,bg4]

    # Creates the player/tank
    tank = Tank(canvas,400, 300)

    # Creates a list of food objects
    foods = [Food(canvas, random.randint(0,800),
        random.randint(0,600), 'square') for i in range(10)]
    crashers = []

    # If the load button is pressed, then this code is ran,
    # loads saved variables into game like health and position of objects
    if load_game_saved_state:
        tank.points=int(load_game()[0])
        tank.health_bar.currenthealth=int(load_game()[5])
        x_position,y_position=float(load_game()[1]),float(load_game()[2])
        change_in_x,change_in_y=float(load_game()[3]),float(load_game()[4])
        for game_object in game_objects:
            game_object.updatePosition(x_position+change_in_x,y_position+change_in_y)
        for food in foods:
            # updates the position of the food object along with its health bar
            food.updatePosition(x_position+change_in_x+food.offsetX,
                y_position+change_in_y+food.offsetY)
            food.healthBar.updatePosition(x_position+change_in_x+food.offsetX,
                y_position+change_in_y+food.offsetY)


    # Creates the text at the bottom of the screen with the players name
    create_custom_text(player_name,400,565,'calibri','white',3,30)
    create_custom_text(tank.points,400,590,'calibri','white',2,15, 'points')

    # displays the leaderboard
    display_leaderboard()

    update()


#-------------------Main-------------------#

def update():
    """
    Main game loop for the game holding game logic such as:
    collisions, movement, scoring
    
    Parameters: None

    Returns: None
    
    """

    global x_position,y_position,change_in_x,change_in_y, crashers

    # clock holding game time
    game_current_time=time.time()

    # if the pause variable is on, then breaks out of the update loop
    if pause_on:
        return

    # every frame, chance of penatgons or squares to spawn in
    # to spawn in the quadrant the player is in
    random_number_for_pentagons=random.randint(1,1500)
    if random_number_for_pentagons == 1:
        foods.append(
            Food(canvas,
                random.randint(int(x_position)
                    if x_position>=0 else int(x_position)+400,
                int(x_position+400)
                    if x_position>=0 else int(x_position)+800),
                random.randint(int(y_position)
                    if y_position>=0 else int(y_position)+300,
                int(y_position+300)
                    if y_position>=0 else int(y_position)+600),
                'pentagon'))
    random_number_for_squares=random.randint(1,1500)
    if random_number_for_squares == 1:
        foods.append(
            Food(canvas,
                random.randint(int(x_position)
                    if x_position>=0 else int(x_position)+400,
                int(x_position+400)
                    if x_position>=0 else int(x_position)+800),
                random.randint(int(y_position)
                    if y_position>=0 else int(y_position)+300,
                int(y_position+300)
                    if y_position>=0 else int(y_position)+600),
                'square'))

    # chance for crasers to spawn on the border, there speed is based on
    # how many points the player has
    if tank.points > 3 and tank.points < 5:
        random_number_for_crashers = random.randint(1, 15)
        if random_number_for_crashers == 1:
            crashers.append(spawn_crasher(canvas,10))
    elif tank.points >=5:
        random_number_for_crashers = random.randint(1, 10)
        if random_number_for_crashers == 1:
            crashers.append(spawn_crasher(canvas,15))
    else:
        random_number_for_crashers = random.randint(1, 25)
        if random_number_for_crashers == 1:
            crashers.append(spawn_crasher(canvas,5))

    # if the player press the a button, then cheat settings load up
    window.bind('a', lambda event: cheat_settings())

    # scroll speed depends on distance from tank/player/centre of the screen
    if distance_from_mouse() > 100:
        if cheat_code=='fast':
            scroll_speed = 30
        else:
            scroll_speed = 10
    else:
        scroll_speed = distance_from_mouse() * 0.1

    angle = calculate_mouse_angle()

    # Changes the changeInX variable depending on the angle the mouse is from the tank
    # And also if the tank is touching a border, then it wont be able to moving towards it
    change_in_x = calculate_change_in_position(x_position,mouse_position()[0],
        400,scroll_speed,angle,True)
    change_in_y = calculate_change_in_position(y_position,mouse_position()[1],
        400,scroll_speed,angle,False)

    # Moves the tiles in order to create the scrolling background effect
    for game_object in game_objects:
        game_object.updatePosition(change_in_x,change_in_y)

    # move the bullets based to create scrolling background effect
    for bullet in tank.bullets:
        bullet.updatePosition(change_in_x+bullet.xOffset,
            change_in_y+bullet.yOffset)

    # move the crashers based to create scrolling background effect
    for crasher in crashers:
        crasher.updatePosition(change_in_x+crasher.offsetX,
            change_in_y+crasher.offsetY)

        # deletes the crashers after 2 seconds
        if game_current_time-crasher.currentSpawnTime>2:
            canvas.delete(crasher.gameObject)
            crashers.remove(crasher)

        # logic for collisions between crashers and objects
        if collision_between(tank, crasher, crasher.size):

            # cooldown hit timer
            current_time = int(time.time() * 1000)
            if current_time-tank.last_hit_time>tank.damage_cool_down:

                # deletes crasher
                canvas.delete(crasher.gameObject)
                crashers.remove(crasher)

                # reduces the tanks health bar and redraws it
                tank.health_bar.currenthealth-=1
                tank.health_bar.gameObject=tank.health_bar.draw(0,0)
                tank.last_hit_time=current_time

    for food in foods:

        # updates the position of the food object along with its health bar
        food.updatePosition(change_in_x+food.offsetX,change_in_y+food.offsetY)
        food.healthBar.updatePosition(change_in_x+food.offsetX, 
            change_in_y+food.offsetY)

        # reduces the foods offset, this gives the effect of the food
        # slowly coming to a stop
        if food.offsetX != 0:
            food.offsetX*=0.98
        if food.offsetY != 0:
            food.offsetY*=0.98

        # =======HIT======= #
        if collision_between(tank, food, food.size):

            # cooldown hit timer
            current_time = int(time.time() * 1000)
            if current_time-tank.last_hit_time>tank.damage_cool_down:

                # pushes the food in the direction of the tank
                food.offsetX=math.cos(tank.angle)*0.5
                food.offsetY=math.sin(tank.angle)*0.5

                # reduces the tanks health bar and redraws it
                tank.health_bar.currenthealth-=1
                tank.health_bar.gameObject=tank.health_bar.draw(0,0)
                tank.last_hit_time=current_time


        # for each food, detect if each bullet is in the
        # hit radius to registor as a hit
        for bullet in tank.bullets:
            if collision_between(bullet,food, food.size):
                # =======HIT======= #
                # deletes the bullet, reduces health bar,
                # redraws the health bar
                tank.removeBullet(-1)
                food.healthBar.currenthealth -=1
                food.healthBar.gameObject=food.healthBar.draw(change_in_x,
                    change_in_y)

                # pushes the food in the direction of the tank
                food.offsetX=math.cos(tank.angle)*0.5
                food.offsetY=math.sin(tank.angle)*0.5

                # If food DEAD
                if food.healthBar.currenthealth<=0:
                    #delete food item along with its health bar
                    canvas.delete(food.gameObject)
                    canvas.delete(food.healthBar.gameObject)
                    foods.remove(food)

                    # Increase the tanks points and redraws the
                    # points text widget
                    if cheat_code=='points':
                        tank.points+=10
                    else:
                        tank.points+=1
                    canvas.delete('points')
                    create_custom_text(tank.points,400,590,'calibri',
                        'white',2,15, 'points')
                    break

    # Updates the xPosition and yPosition
    x_position+=change_in_x
    y_position+=change_in_y

    # If player DEAD, then breaks out of updates loop,
    # then creates a new update loop and reinitializes the game
    if tank.health_bar.currenthealth <= 0:
        update_high_score(tank.points, PLAYER_USER_NAME)
        canvas.delete('all')
        initiialise_game(PLAYER_USER_NAME)
        return

    # After 10ms, updates the canvas and calls the function update again
    canvas.after(20, update)

start_screen = StartScreen(window, canvas, initiialise_game)

window.mainloop()
