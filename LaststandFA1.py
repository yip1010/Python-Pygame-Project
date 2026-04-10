import pygame  # Pygame is a library for creating games with graphics and sound
import sys     # Sys module provides access to system-specific parameters and functions
import random  # Random module is used to generate random numbers and selections
import pickle  # Pickle module is used to serialize and deserialize Python objects


# Initialize Pygame and the mixer for sound
pygame.init()
pygame.mixer.init()

# Create a clock object to manage the frame rate
clock = pygame.time.Clock()
fps = 60

# Define screen dimensions, create the game window, and window title
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Last Stand')

# Load background image and title image for the main menu
background_img = pygame.image.load('Gamephoto/bg/FABG.jpg').convert_alpha()
title_img = pygame.image.load('Gamephoto/bg/laststand.png').convert_alpha()

# Load background music and set it to loop indefinitely
pygame.mixer.music.load('bgsound.mp3')
pygame.mixer.music.play(-1)

# Define colors used in the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define fonts for rendering text in the game
font = pygame.font.SysFont('Helvetica', 24)
title_font = pygame.font.SysFont('Helvetica', 48)


# Button class for creating clickable buttons
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        """
        Initialize the button with position, size, text, and optional action.
        :param x: X-coordinate of the button
        :param y: Y-coordinate of the button
        :param width: Width of the button
        :param height: Height of the button
        :param text: Text to display on the button
        :param action: Optional function to call when button is clicked
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action

    def draw(self):
        """Draw the button on the screen with the specified text."""
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))  # Draw button rectangle
        text_surface = font.render(self.text, True, BLACK)  # Render the button text

        # Center the text on the button and paste to screen
        screen.blit(text_surface, (self.x + self.width / 2 - text_surface.get_width() / 2,
                                   self.y + self.height / 2 - text_surface.get_height() / 2))

    def is_clicked(self, event):
        """
        Check if the button is clicked based on mouse events.
        :param event: The event to check
        :return: True if the button is clicked, otherwise False
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is within the button's rectangle
            if self.x < event.pos[0] < self.x + self.width and self.y < event.pos[1] < self.y + self.height:
                return True
        return False


# InputBox class for creating text input fields
class InputBox:
    def __init__(self, x, y, width, height, text=''):
        """
        Initialize the input box with position, size, and optional initial text.
        :param x: X-coordinate of the input box
        :param y: Y-coordinate of the input box
        :param width: Width of the input box
        :param height: Height of the input box
        :param text: Initial text to display in the input box
        """
        self.rect = pygame.Rect(x, y, width, height)  # Create a rectangle for the input box
        self.color = WHITE
        self.text = text
        self.txt_surface = font.render(text, True, BLACK)  # Render the initial text
        self.active = False

    def handle_event(self, event):
        """
        Handle events for the input box such as mouse clicks and key presses.
        :param event: The event to handle
        :return: The current text if Enter is pressed, otherwise None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active  # Toggle active state when clicked
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text  # Return the text when Enter is pressed
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Remove last character on Backspace
                elif len(self.text) < 10 and (event.unicode.isalpha() or event.unicode.isdigit()):
                    self.text += event.unicode  # Add new character to text
                self.txt_surface = font.render(self.text, True, BLACK)  # Update text surface

    def draw(self):
        """Draw the input box on the screen with the current text."""
        pygame.draw.rect(screen, self.color, self.rect)  # Draw the input box rectangle
        pygame.draw.rect(screen, self.color, self.rect, 2)  # Draw the border
        # Center the text within the input box
        text_width = self.txt_surface.get_width()
        text_height = self.txt_surface.get_height()
        text_x = self.rect.x + (self.rect.width - text_width) / 2
        text_y = self.rect.y + (self.rect.height - text_height) / 2
        screen.blit(self.txt_surface, (text_x, text_y))


# Function to display the main menu
def main_menu():
    run = True

    # Create buttons for the main menu
    new_game_button = Button(center_x - button_width / 2, center_y - button_height - button_gap, button_width, button_height, 'New Game')
    continue_button = Button(center_x - button_width / 2, center_y, button_width, button_height, 'Continue')
    exit_button = Button(center_x - button_width / 2, center_y + button_height + button_gap, button_width, button_height, 'Exit')

    # Function to load the game state from a saved file
    def load_game():
        try:
            with open('saved_game.pkl', 'rb') as file:
                game_state = pickle.load(file)
                return game_state['players'], game_state['ai_players'], game_state['battle_log']
        except (FileNotFoundError, EOFError):
            return None, None, None

    while run:
        clock.tick(fps)  # Control the frame rate
        screen.blit(background_img, (0, 0))  # Draw the background image
        screen.blit(title_img, (center_x - title_img.get_width() / 2, center_y - button_height - button_gap - title_img.get_height() * 1.3))  # Draw the title image

        # Draw the buttons
        new_game_button.draw()
        continue_button.draw()
        exit_button.draw()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Exit the loop if the window is closed
            if new_game_button.is_clicked(event):
                team_creation()  # Start a new game
            elif continue_button.is_clicked(event):
                # Attempt to load a saved game
                loaded_players, loaded_ai_players, loaded_battle_log = load_game()
                if loaded_players and loaded_ai_players:
                    battle_scene(loaded_players)  # Continue with the loaded game
                else:
                    show_popup_message("No saved game found!")
            elif exit_button.is_clicked(event):
                run = False  # Exit the loop if the exit button is clicked

        pygame.display.update()  # Update the display


# Function to create a player team by taking input from the user
def team_creation():
    # Render the text for team name input
    team_name_text = font.render('Enter Team Name', True, WHITE)
    # Create an input box for team name
    team_name_input = InputBox(center_x - 150, center_y - 120, 300, 50)

    # Render the text for number of players input
    num_players_text = font.render('Number of Players (1-5)', True, WHITE)
    # Create an input box for the number of players
    num_players_input = InputBox(center_x - 150, center_y - 20, 300, 50)

    # Create a submit button
    submit_button = Button(center_x - 50, center_y + 50, 100, 50, 'Submit')

    while True:
        # Limit the frame rate
        clock.tick(fps)

        # Clear the screen and redraw background image
        screen.blit(background_img, (0, 0))

        # Draw the team name prompt and input box
        screen.blit(team_name_text, (center_x - team_name_text.get_width() / 2, center_y - 150))
        team_name_input.draw()

        # Draw the number of players prompt and input box
        screen.blit(num_players_text, (center_x - num_players_text.get_width() / 2, center_y - 50))
        num_players_input.draw()

        # Draw the submit button
        submit_button.draw()

        # Process events in the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the game if the quit event is triggered
                pygame.quit()
                sys.exit()

            # Handle events for the team name input box
            team_name_input.handle_event(event)
            # Handle events for the number of players input box
            num_players_input.handle_event(event)

            # Check if the submit button is clicked
            if submit_button.is_clicked(event):
                # Retrieve the team name from the input box
                team_name = team_name_input.text
                try:
                    # Attempt to convert the number of players input to an integer
                    num_players = int(num_players_input.text)
                    # Validate the number of players (should be between 1 and 5)
                    if 1 <= num_players <= 5:
                        # Call the function to create the player team
                        player_creation(team_name, num_players)
                    else:
                        # If number of players is not valid, set a default value
                        num_players_input.text = '3'
                except ValueError:
                    # If conversion fails, set a default value
                    num_players_input.text = '3'

        # Update the display with the new frame
        pygame.display.update()


# Function for displaying a popup message
def show_popup_message(message, duration=2000):
    """
    Displays a popup message with a black background for a specified duration in milliseconds.

    Parameters:
    message (str): The message to be displayed in the popup.
    duration (int): Duration for which the popup message will be displayed (in milliseconds).
    """
    # Create a black overlay covering the entire screen
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.fill(BLACK)  # Fill the overlay with black color
    overlay.set_alpha(200)  # Set the transparency level (200 out of 255 for less transparency)
    screen.blit(overlay, (0, 0))  # Blit the overlay on the screen to create a dark background

    # Create the popup message surface
    popup_font = pygame.font.SysFont('Helvetica', 32)  # Define font and size for the popup message
    popup_surface = pygame.Surface((500, 100))  # Create a surface for the popup message with specified width and height
    popup_surface.fill(WHITE)  # Fill the popup surface with white color

    # Render the text onto the popup surface
    text_surface = popup_font.render(message, True, BLACK)  # Render the message text with black color
    popup_surface.blit(text_surface, (popup_surface.get_width() / 2 - text_surface.get_width() / 2,
                                      popup_surface.get_height() / 2 - text_surface.get_height() / 2))
    # Center the text on the popup surface

    # Calculate the position to center the popup on the screen
    popup_x = screen_width / 2 - popup_surface.get_width() / 2
    popup_y = screen_height / 2 - popup_surface.get_height() / 2

    # Display the popup message
    screen.blit(popup_surface, (popup_x, popup_y))  # Blit the popup surface on the screen at the calculated position
    pygame.display.update()  # Update the display to show the popup
    pygame.time.delay(duration)  # Pause execution for the specified duration to keep the popup visible


# Function to create input boxes for each player's name and type
def player_creation(team_name, num_players):
    # Create input boxes for player names, positioned vertically
    player_name_inputs = [InputBox(center_x - 250, center_y + i * 100 - (num_players * 100) / 2, 240, 50) for i in
                          range(num_players)]

    # Create input boxes for player types, positioned vertically beside the name input boxes
    player_type_inputs = [InputBox(center_x + 50, center_y + i * 100 - (num_players * 100) / 2, 240, 50) for i in
                          range(num_players)]

    # Create a submit button for finalizing player input
    submit_button = Button(center_x - 125, screen_height - 100, 300, 50, 'Submit')

    # Create a back button to return to the previous screen
    back_button = Button(20, 20, 100, 50, 'Back')

    # Create text labels for player name inputs
    player_names_text = [font.render(f'Player {i + 1} Name', True, WHITE) for i in range(num_players)]

    # Create text labels for player type inputs, instructing users to choose 'Warrior' or 'Tanker'
    player_types_text = [font.render(f'{i + 1}. Warrior/Tanker only ', True, WHITE) for i in range(num_players)]

    while True:
        # Limit frame rate to the defined FPS
        clock.tick(fps)

        # Draw background image
        screen.blit(background_img, (0, 0))

        # Create a semi-transparent overlay to darken the background
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        # Draw input labels and input boxes for each player
        for i in range(num_players):
            # Draw player name labels above the name input boxes
            screen.blit(player_names_text[i], (
                player_name_inputs[i].rect.x + player_name_inputs[i].rect.width / 2 - player_names_text[
                    i].get_width() / 2,
                player_name_inputs[i].rect.y - 30))

            # Draw player type labels above the type input boxes
            screen.blit(player_types_text[i], (
                player_type_inputs[i].rect.x + player_type_inputs[i].rect.width / 2 - player_types_text[
                    i].get_width() / 2,
                player_type_inputs[i].rect.y - 30))

            # Draw the input boxes for player names and types
            player_name_inputs[i].draw()
            player_type_inputs[i].draw()

        # Draw the submit and back buttons
        submit_button.draw()
        back_button.draw()

        # Handle events such as button clicks and input updates
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the game if the quit event is triggered
                pygame.quit()
                sys.exit()

            # Handle events for each input box (name and type)
            for i in range(num_players):
                player_name_inputs[i].handle_event(event)
                player_type_inputs[i].handle_event(event)

            # Handle submit button click
            if submit_button.is_clicked(event):
                players = []
                for i in range(num_players):
                    player_name = player_name_inputs[i].text
                    player_type = player_type_inputs[i].text

                    # Create player data dictionary with random attributes based on type
                    player_data = {
                        'name': player_name,
                        'type': player_type,
                        'HP': 100,
                        'Attack': random.randint(5, 20) if player_type == 'Warrior' else random.randint(1, 10),
                        'Defense': random.randint(1, 10) if player_type == 'Warrior' else random.randint(5, 15),
                        'EXP': 0,
                        'Rank': 1,
                        'coins': 0  # Initialize coins for each player
                    }
                    players.append(player_data)

                # Print player team details for debugging
                print(f'Team "{team_name}" created with {num_players} players: {players}')

                # Show a popup message indicating successful team creation
                show_popup_message("Team successfully created")

                # Proceed to the battle scene with the created players
                battle_scene(players)

            # Handle back button click to return to the team creation screen
            if back_button.is_clicked(event):
                team_creation()

        # Update the display to show the latest changes
        pygame.display.update()


# Function for battle scene
def battle_scene(players):
    # Define a Button class to handle button creation and interaction
    class Button:
        def __init__(self, x, y, width, height, text, color=(255, 255, 255), text_color=(0, 0, 0), font_size=19):
            # Initialize the button with position, size, text, and colors
            self.rect = pygame.Rect(x, y, width, height)  # Button's rectangular area
            self.text = text  # Button's text
            self.color = color  # Button's fill color
            self.text_color = text_color  # Text color
            self.font_size = font_size  # Font size for text

        # Draw the button on the screen
        def draw(self):
            pygame.draw.rect(screen, self.color, self.rect)  # Draw the button's background
            font = pygame.font.SysFont('Helvetica', self.font_size)  # Create font object
            text_surface = font.render(self.text, True, self.text_color)  # Render text
            text_rect = text_surface.get_rect(center=self.rect.center)  # Center text in the button
            screen.blit(text_surface, text_rect)  # Draw text on the screen

        # Check if the button was clicked
        def is_clicked(self, event):
            return self.rect.collidepoint(event.pos)  # Return True if click is within the button's area

    # Define a Dropdown class to handle dropdown menu creation and interaction
    class Dropdown:
        def __init__(self, x, y, width, height, options):
            # Initialize the dropdown menu with position, size, and options
            self.rect = pygame.Rect(x, y, width, height)  # Dropdown's rectangular area
            self.options = options  # List of options for the dropdown
            self.selected_option = options[0]  # Default selected option
            self.dropdown_open = False  # Track whether the dropdown is open
            self.font = pygame.font.SysFont('Helvetica', 24)  # Font for option text
            self.option_rects = []  # List to store rectangles for each option
            self.option_height = 30  # Height of each option in the dropdown

        # Draw the dropdown on the screen
        def draw(self):
            pygame.draw.rect(screen, WHITE, self.rect)  # Draw the background of the selected option
            pygame.draw.rect(screen, BLACK, self.rect, 2)  # Draw border around the dropdown
            text_surface = self.font.render(self.selected_option, True, BLACK)  # Render selected option text
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))  # Draw selected text

            # Draw the dropdown list if it's open
            if self.dropdown_open:
                for i, option in enumerate(self.options):
                    # Create a rectangle for each dropdown option
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.option_height, self.rect.width,
                                              self.option_height)
                    self.option_rects.append(option_rect)  # Store the rectangle
                    pygame.draw.rect(screen, WHITE, option_rect)  # Draw the option's background
                    pygame.draw.rect(screen, BLACK, option_rect, 2)  # Draw border around the option
                    option_text_surface = self.font.render(option, True, BLACK)  # Render option text
                    screen.blit(option_text_surface, (option_rect.x + 5, option_rect.y + 5))  # Draw option text
                self.option_rects.append(self.rect)  # Add main dropdown rectangle to the list

        # Handle events for the dropdown
        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle dropdown visibility when the main rectangle is clicked
                if self.rect.collidepoint(event.pos):
                    self.dropdown_open = not self.dropdown_open
                else:
                    # If dropdown is open, check if an option is selected
                    if self.dropdown_open:
                        for i, rect in enumerate(self.option_rects):
                            if rect.collidepoint(event.pos):
                                self.selected_option = self.options[i]  # Update selected option
                                self.dropdown_open = False  # Close the dropdown
                                return


    battle_log_width = 280 # Width of the battle log panel on the left side
    battle_scene_width = 1000 # Width of the main battle scene area
    max_log_messages = 25 # Maximum number of messages to display in the battle log
    background_img = pygame.image.load('Gamephoto/bg/fightbg.jpg').convert_alpha()  # Load and convert the background image for the battle scene

    def load_image(image_path):
        """
        Load and convert an image to be used in the game.

        Args:
            image_path (str): The file path of the image to load.

        Returns:
            pygame.Surface: The loaded image surface, or None if there was an error.
        """
        try:
            # Attempt to load and convert the image
            image = pygame.image.load(image_path).convert_alpha()
            return image
        except pygame.error as e:
            # Print an error message if image loading fails
            print(f"Error loading image {image_path}: {e}")
            return None

    # Load images for player and AI characters
    player_warrior_img = load_image('Gamephoto/Idle/2.png')
    player_tanker_img = load_image('Gamephoto/Idle/1-01.png')
    ai_warrior_img = load_image('Gamephoto/Idle/3.png')
    ai_tanker_img = load_image('Gamephoto/Idle/4.png')

    # Font settings for displaying battle log messages
    battle_log_font = pygame.font.SysFont('Helvetica', 24)

    # Initialize the battle log as an empty list
    battle_log = []

    # Create buttons for saving, restarting, and exiting the game
    save_button = Button(15, screen_height - 100, 70, 40, 'Save', font_size=16)
    restart_button = Button(100, screen_height - 100, 70, 40, 'Restart', font_size=16)
    exit_button = Button(190, screen_height - 100, 70, 40, 'Exit', font_size=16)

    # Initialize AI players with random types and default attributes
    num_players = len(players)
    ai_players = [{'type': random.choice(['Warrior', 'Tanker']), 'HP': 100, 'coins': 0} for _ in range(num_players)]

    def save_game(players, ai_players, battle_log):
        """
        Save the current game state to a file.

        Args:
            players (list): The list of player characters.
            ai_players (list): The list of AI characters.
            battle_log (list): The list of battle log messages.
        """
        # Create a dictionary to store the game state
        game_state = {
            'players': players,
            'ai_players': ai_players,
            'battle_log': battle_log
        }
        # Write the game state to a file using pickle
        with open('saved_game.pkl', 'wb') as file:
            pickle.dump(game_state, file)
        # Display a message indicating the game has been saved
        show_popup_message("Game Saved!")

    # Function for simulate an attack from a player on an AI character.
    def attack(player, ai_player):
        """
        Args:
            player (dict): The player character attacking.
            ai_player (dict): The AI character being attacked.

        Returns:
            int: The amount of damage dealt.
        """
        # Determine random damage value between 10 and 20
        damage = random.randint(10, 20)
        # Apply damage to the AI character
        ai_player['HP'] -= damage
        if ai_player['HP'] < 0:
            ai_player['HP'] = 0
        # Calculate coins earned based on damage dealt
        coins_earned = damage
        player['coins'] = player.get('coins', 0) + coins_earned
        return damage

    # Function for simulate an attack from an AI character on a player character.
    def ai_attack(ai_player, player):
        """
        Args:
            ai_player (dict): The AI character attacking.
            player (dict): The player character being attacked.

        Returns:
            int: The amount of damage dealt.
        """
        # Determine random damage value between 5 and 15
        damage = random.randint(5, 15)
        # Apply damage to the player character
        player['HP'] -= damage
        if player['HP'] < 0:
            player['HP'] = 0
        # Calculate coins earned based on damage dealt
        coins_earned = damage
        ai_player['coins'] = ai_player.get('coins', 0) + coins_earned
        return damage

    # Draw the background image onto the screen.
    def draw_bg():
        screen.blit(background_img, (battle_log_width, 0))

    def draw_battle_log():
        # Load and scale the background image for the battle log area
        battle_log_img = pygame.image.load('Gamephoto/bg/battlelog.jpg').convert_alpha()
        battle_log_img = pygame.transform.scale(battle_log_img, (280, 720))

        # Load and scale the coin image to represent the player's coins
        coin_img = pygame.image.load('Gamephoto/Idle/battlecoin.png').convert_alpha()
        coin_img = pygame.transform.scale(coin_img, (35, 35))

        # Draw the battle log background image at the top left corner of the screen
        screen.blit(battle_log_img, (0, 0))

        # Calculate the total number of coins across all players
        total_coins = sum(player.get('coins', 0) for player in players)

        # Draw the coin image and total coin count on the screen
        screen.blit(coin_img, (10, 10))
        total_coins_surface = font.render(f"x {total_coins}", True, (0, 0, 0))  # Render total coins as text
        screen.blit(total_coins_surface, (60, 20))

        # Set up the font for rendering the battle log text
        battle_log_font = pygame.font.SysFont('Helvetica', 17)

        # Helper function to wrap text within a specified width
        def wrap_text(text, font, max_width):
            words = text.split(' ')  # Split text into individual words
            lines = []
            current_line = ''

            # Loop through each word to create lines that fit within max_width
            for word in words:
                test_line = f'{current_line} {word}'.strip()
                # If the line fits within the max width, continue building it
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    # Otherwise, add the current line to the list of lines and start a new line
                    lines.append(current_line)
                    current_line = word

            # Append the last line to the list of lines
            if current_line:
                lines.append(current_line)

            return lines

        # Set the maximum width for the text and initialize y_offset for drawing text
        max_width = 280 - 10  # Account for padding on the sides
        y_offset = 60  # Start position for the text after the coin display
        max_log_height = screen_height - 150  # Maximum height for the log before truncating

        # Render and display each log message on the screen, wrapping long messages
        for log in battle_log:
            wrapped_lines = wrap_text(log, battle_log_font, max_width)
            for line in wrapped_lines:
                log_surface = battle_log_font.render(line, True, (0, 0, 0))  # Render each line as a surface
                # If there is enough space, draw the text and increment y_offset
                if y_offset + log_surface.get_height() <= max_log_height:
                    screen.blit(log_surface, (5, y_offset))
                    y_offset += log_surface.get_height() + 2  # Add spacing between lines
                else:
                    break  # Stop rendering if there's no more space for text

    # Create a list of AI names for the dropdown menu, based on the number of AI players
    ai_names = [f"AI {i + 1}" for i in range(len(ai_players))]

    # Create a dropdown menu for AI selection, positioned to the right of the battle log
    ai_dropdown = Dropdown(battle_log_width + 430, screen_height - 670, 120, 30, ai_names)

    # Function to draw a health bar representing the current and maximum HP
    def draw_hp_bar(x, y, current_hp, max_hp):
        hp_bar_width = 100  # Set the width of the health bar
        hp_bar_height = 10  # Set the height of the health bar
        fill_percentage = current_hp / max_hp  # Calculate the percentage of HP remaining
        fill_width = int(hp_bar_width * fill_percentage)  # Determine the width of the filled portion

        # Draw the red background (empty part of the HP bar)
        pygame.draw.rect(screen, (255, 0, 0), (x, y, hp_bar_width, hp_bar_height))

        # Draw the green foreground (filled part of the HP bar)
        pygame.draw.rect(screen, (0, 255, 0), (x, y, fill_width, hp_bar_height))

    # Function to draw the player and AI characters on the screen
    def draw_players_and_ai():
        player_y_start = 100  # Y-coordinate where the first player's image will be drawn
        player_spacing = 110  # Vertical spacing between each player/AI character
        button_width = 60  # Width of the attack and heal buttons
        button_height = 25  # Height of the attack and heal buttons

        # Loop through all players and draw their image, health bar, and action buttons
        for i, player in enumerate(players):
            y_pos = player_y_start + i * player_spacing  # Calculate vertical position for each player

            # Only draw players that are still alive (HP > 0)
            if player['HP'] > 0:
                # Display the player's image based on their type (Warrior or Tanker)
                if player['type'].lower() == 'warrior':
                    screen.blit(player_warrior_img, (battle_log_width + 90, y_pos))
                else:
                    screen.blit(player_tanker_img, (battle_log_width + 90, y_pos))

                # Draw the player's health bar above their image
                draw_hp_bar(battle_log_width + 90, y_pos - 20, player['HP'], 100)

                # Create attack and heal buttons next to the player's image
                attack_button = Button(battle_log_width + 90 + player_warrior_img.get_width() + 10, y_pos,
                                       button_width, button_height, 'Attack', color=(191, 2, 2),
                                       text_color=(255, 255, 255), font_size=12)
                heal_button = Button(battle_log_width + 90 + player_warrior_img.get_width() + 10,
                                     y_pos + button_height + 5, button_width, button_height, 'Heal',
                                     color=(0, 191, 2), text_color=(255, 255, 255), font_size=12)

                # If the player is dead (HP <= 0), disable the buttons by coloring them gray
                if player['HP'] <= 0:
                    attack_button.color = (100, 100, 100)
                    heal_button.color = (100, 100, 100)

                # Draw the attack and heal buttons on the screen
                attack_button.draw()
                heal_button.draw()

                # Handle events, such as mouse clicks on the buttons
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Handle attack button click
                        if attack_button.is_clicked(event) and player['HP'] > 0:
                            # Get the target AI based on the dropdown selection and deal damage
                            target_ai_index = ai_names.index(ai_dropdown.selected_option)
                            target_ai = ai_players[target_ai_index]
                            damage = attack(player, target_ai)

                            # Log the attack in the battle log
                            battle_log.append(
                                f"{player['name']} attacked {ai_dropdown.selected_option} for {damage} damage!")

                            # Ensure the log does not exceed the maximum number of messages
                            if len(battle_log) > max_log_messages:
                                battle_log.pop(0)

                            # AI counter-attacks a random player
                            ai_target = random.choice(players)
                            ai_damage = ai_attack(random.choice(ai_players), ai_target)
                            battle_log.append(
                                f"{ai_dropdown.selected_option} attacked {ai_target['name']} for {ai_damage} damage!")

                            # Ensure the log does not exceed the maximum number of messages
                            if len(battle_log) > max_log_messages:
                                battle_log.pop(0)

                        # Handle heal button click
                        elif heal_button.is_clicked(event) and player['HP'] > 0:
                            # Heal the player and cap HP at 100
                            player['HP'] += 20
                            if player['HP'] > 100:
                                player['HP'] = 100

                            # Log the heal action in the battle log
                            battle_log.append(f"{player['name']} healed for 20 HP!")

                            # Ensure the log does not exceed the maximum number of messages
                            if len(battle_log) > max_log_messages:
                                battle_log.pop(0)

        # Loop through AI players and draw their images and health bars
        for i, ai_player in enumerate(ai_players):
            y_pos = player_y_start + i * player_spacing  # Calculate vertical position for each AI

            # Only draw AI that are still alive (HP > 0)
            if ai_player['HP'] > 0:
                # Display the AI's image based on their type (Warrior or Tanker)
                if ai_player['type'] == 'Warrior':
                    screen.blit(ai_warrior_img, (battle_log_width + battle_scene_width - 180, y_pos))
                else:
                    screen.blit(ai_tanker_img, (battle_log_width + battle_scene_width - 180, y_pos))

                # Draw the AI's health bar above their image
                draw_hp_bar(battle_log_width + battle_scene_width - 180, y_pos - 20, ai_player['HP'], 100)

    # Main game loop
    run = True  # Set the loop control variable to True
    while run:
        clock.tick(fps)  # Control the frame rate of the game to match the fps
        draw_bg()  # Draw the background image
        draw_players_and_ai()  # Draw the player and AI characters along with their health bars and action buttons
        draw_battle_log()  # Display the battle log on the screen
        save_button.draw()  # Draw the save button
        restart_button.draw()  # Draw the restart button
        exit_button.draw()  # Draw the exit button
        ai_dropdown.draw()  # Draw the AI dropdown menu for selecting AI targets

        # Event handling
        for event in pygame.event.get():
            # Handle the quit event (e.g., closing the game window)
            if event.type == pygame.QUIT:
                pygame.quit()  # Close Pygame
                sys.exit()  # Exit the program

            # Handle mouse button down event (e.g., clicking buttons)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the save button is clicked, save the current game state
                if save_button.is_clicked(event):
                    save_game(players, ai_players, battle_log)

                # If the restart button is clicked, reset the game state to its initial configuration
                elif restart_button.is_clicked(event):
                    players = [{'name': player['name'], 'type': player['type'], 'HP': 100, 'Attack': player['Attack'],
                                'Defense': player['Defense'], 'EXP': 0, 'Rank': 1, 'coins': 0} for player in players]
                    ai_players = [{'type': random.choice(['Warrior', 'Tanker']), 'HP': 100, 'coins': 0} for _ in
                                  range(len(players))]
                    battle_log = []  # Clear the battle log

                # If the exit button is clicked, quit the game
                elif exit_button.is_clicked(event):
                    pygame.quit()  # Close Pygame
                    sys.exit()  # Exit the program

                # Handle AI dropdown menu selection events
                ai_dropdown.handle_event(event)

        pygame.display.flip()  # Update the display with the latest drawing actions



# Main loop parameters
button_width = 200  # Width of the buttons in the main menu
button_height = 50  # Height of the buttons in the main menu
button_gap = 20  # Gap between buttons in the main menu
center_x = screen_width / 2  # Horizontal center of the screen (used to align buttons)
center_y = screen_height / 2  # Vertical center of the screen (used to align buttons)

main_menu()  # Call the main menu function to start the game
