import pygame, pygameMenu
import os, json
from player import Player
import options_menu


class Clueless:
    def __init__(self):
        # Initialize the pygame module
        pygame.init()

        # Set the title of the screen
        pygame.display.set_caption("The Game of Clue-Less")

        # Create the actual screen
        self.screen = pygame.display.set_mode((2560, 1440), pygame.RESIZABLE)

        # Create the options menu
        self.options = options_menu.Options()
        self.options.init_accusation_menu(self.screen)
        self.options.init_move_menu(self.screen, ["NONE"])

        # Load Images
        self.logo_image = pygame.image.load('images\logo2.png')
        self.house_image = pygame.image.load('images\house.jpg')
        self.start_image = pygame.image.load('images\start.png').convert_alpha()
        self.map_image = pygame.image.load('images\map2.png')

        # Color variables
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        
        # Variables
        self.SCREEN_WIDTH = 2560
        self.SCREEN_HEIGHT = 1440
        self.ROOM_DIMENSIONS = 200
        self.MAP_WIDTH = self.ROOM_DIMENSIONS * 5
        self.MAP_HEIGHT = self.ROOM_DIMENSIONS * 5
        self.SCREEN_DIVIDER_START = self.ROOM_DIMENSIONS + self.MAP_WIDTH + self.ROOM_DIMENSIONS
        self.OPTIONS_WIDTH = self.SCREEN_WIDTH - self.SCREEN_DIVIDER_START
        self.MAP_SIZE = self.map_image.get_size()
        self.MAP_X = (self.SCREEN_DIVIDER_START - self.MAP_SIZE[0]) / 3
        self.MAP_Y = (self.SCREEN_HEIGHT - self.MAP_SIZE[1]) / 3
        self.screen_opacity = 0
        self.start_opacity = 150

        self.MAP_LOCATIONS = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        self.MAP_DICT = None

        # Initialize the map dict
        self.init_map_dict()

        # Update the map locations
        self.update_map_locations()

        # Initialize clock and timer
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 100)

        # Load the players
        cwd = os.getcwd()
        self.player_list = []
        self.player_list.append(Player(cwd + "\\images\\players\\big_demon",     "H1",  1, "Miss Scarlet", "Red Demon"))
        self.player_list.append(Player(cwd + "\\images\\players\\big_zombie",    "H2",  2, "Prof. Plumb", "Big Zombie"))
        self.player_list.append(Player(cwd + "\\images\\players\\green_girl",    "H4",  3, "Col. Mustard", "Female Elf"))
        self.player_list.append(Player(cwd + "\\images\\players\\green_guy",     "H7",  4, "Mrs. Peacock", "Male Elf"))
        self.player_list.append(Player(cwd + "\\images\\players\\knight_orange", "H10", 5, "Mr. Green", "Male Knight"))
        self.player_list.append(Player(cwd + "\\images\\players\\knight_pink",   "H11", 6, "Mrs. White", "Female Knight"))

        # Update the images
        self.update_images()

        # Update player locations
        for player in self.player_list:
            player.set_location(self.MAP_DICT[player.sprite_room]["LOCATION"])

        self.current_player = self.player_list[1]
        self.current_player.bool_is_active = True
        self.options.update_player_info(
            self.current_player.player_number,
            self.current_player.player_name,
            self.current_player.character,
            "Col. Mustard",
            "Rope",
            "Sutdy"
        )

        # Screen fade parameters
        self.fade = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.fade.fill(self.BLACK)

        # State enums
        self.program_state = "GAME"
        self.menu_state = "INIT"
        self.game_state = "WAITING"
        self.opacity_direction = "UP"

    def init_map_dict(self):
        with open("map_dict.json", "r") as map_dict_file:
            self.MAP_DICT = json.load(map_dict_file)

    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)

    def update_map_locations(self):
        divisor = self.MAP_SIZE[0] / 10
        row = divisor
        col = divisor
        for i in range(0, 5):
            for j in range(0, 5):
                self.MAP_LOCATIONS[i][j] = [int(row + self.MAP_Y), int(col + self.MAP_X)]
                if i == 0 and j == 0:
                    self.MAP_DICT["STUDY"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 1 and j == 0:
                    self.MAP_DICT["H0"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 2 and j == 0:
                    self.MAP_DICT["HALL"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 3 and j == 0:
                    self.MAP_DICT["H1"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 4 and j == 0:
                    self.MAP_DICT["LOUNGE"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 0 and j == 1:
                    self.MAP_DICT["H2"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 2 and j == 1:
                    self.MAP_DICT["H3"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 4 and j == 1:
                    self.MAP_DICT["H4"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 0 and j == 2:
                    self.MAP_DICT["LIBRARY"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 1 and j == 2:
                    self.MAP_DICT["H5"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 2 and j == 2:
                    self.MAP_DICT["BILLIARD_ROOM"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 3 and j == 2:
                    self.MAP_DICT["H6"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 4 and j == 2:
                    self.MAP_DICT["DINING_ROOM"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 0 and j == 3:
                    self.MAP_DICT["H7"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 2 and j == 3:
                    self.MAP_DICT["H8"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 4 and j == 3:
                    self.MAP_DICT["H9"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 0 and j == 4:
                    self.MAP_DICT["CONSERVATORY"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 1 and j == 4:
                    self.MAP_DICT["H10"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 2 and j == 4:
                    self.MAP_DICT["BALLROOM"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 3 and j == 4:
                    self.MAP_DICT["H11"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                elif i == 4 and j == 4:
                    self.MAP_DICT["KITCHEN"]["LOCATION"] = self.MAP_LOCATIONS[i][j]
                col = col + 2 * divisor
            col = divisor
            row = row + 2 * divisor

    def update_images(self):
        ## Transform images ##
        # Logo image
        width = int(self.SCREEN_WIDTH * .6)
        height = int(width / 7)
        self.logo_image = pygame.transform.scale(self.logo_image, (width, height))

        # House image
        self.house_image = pygame.transform.scale(self.house_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Start image
        width = int(self.SCREEN_WIDTH / 12)
        height = int(width / 4)
        self.start_image = pygame.transform.scale(self.start_image, (width, height))

        # Map image
        width = int(self.SCREEN_WIDTH * 1 / 2)
        height = int(width)
        self.map_image = pygame.transform.scale(self.map_image, (width, height))

        # Sprites
        for player in self.player_list:
            player.transform_sprites(self.SCREEN_WIDTH)

        # Title screen
        #width = int(self.SCREEN_WIDTH - self.ROOM_DIMENSIONS + self.MAP_WIDTH + self.ROOM_DIMENSIONS)
        #height = int(width / 5)
        #self.title_screen = pygame.transform.scale(self.title_screen, (width, height))

        ## UPdate image locations ##
        # Logo location parameters
        self.LOGO_SIZE = self.logo_image.get_size()
        self.LOGO_X = (self.SCREEN_WIDTH - self.LOGO_SIZE[0]) / 2
        self.LOGO_Y = (self.SCREEN_HEIGHT - self.LOGO_SIZE[1]) / 2

        # Start location parameters
        self.START_SIZE = self.start_image.get_size()
        self.START_X = (self.SCREEN_WIDTH - self.START_SIZE[0]) / 2
        self.START_Y = (self.SCREEN_HEIGHT - self.START_SIZE[1] - 100)

        # Map location parameters
        self.MAP_SIZE = self.map_image.get_size()
        self.SCREEN_DIVIDER_START = self.ROOM_DIMENSIONS + self.MAP_WIDTH + self.ROOM_DIMENSIONS
        self.OPTIONS_WIDTH = self.SCREEN_WIDTH - self.SCREEN_DIVIDER_START
        self.MAP_X = (self.SCREEN_DIVIDER_START - self.MAP_SIZE[0]) / 3
        self.MAP_Y = (self.SCREEN_HEIGHT - self.MAP_SIZE[1]) / 3

        ## Options Menu ##
        self.update_options_menu()

    def update_options_menu(self):
        # Options player info
        width = int(self.OPTIONS_WIDTH / 3)
        height = int(width * self.options.PLAYER_INFO_SURFACE_RATIO)
        self.options.update_scaled_values(width, height)
        self.options.player_info_surface = pygame.transform.scale(self.options.player_info_surface, (width, height))

        # Option menu updates
        self.options.init_accusation_menu(self.screen)

    def main_loop(self):
        # Mutable variables
        running = True

        while running:
            # Boolean Variables
            bool_update_opacity = False
            bool_animate = False

            # State Variables
            move_direction = "NONE"



            # event handler
            events = pygame.event.get()
            for event in events:
                # Timer events
                if event.type == pygame.USEREVENT:
                    bool_update_opacity = True
                    bool_animate = True
                # Resize the window in case of a resize event
                if event.type == pygame.VIDEORESIZE:
                    self.SCREEN_WIDTH = event.w
                    self.SCREEN_HEIGHT = event.h
                    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)

                    # Update the images
                    self.update_images()

                    # Update the map locations
                    self.update_map_locations()
                    for player in self.player_list:
                        player.set_location(self.MAP_DICT[player.sprite_room]["LOCATION"])

                    if self.program_state == "GAME":
                        # Draw the map
                        self.draw_map()

                # Mouse click events
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    response = self.options.check_button_clicked(pos, (self.SCREEN_DIVIDER_START + 10,
                                                            self.options.title_surface.get_size()[1]))
                    if response == "Move":
                        self.options.init_move_menu(self.screen,
                                                   self.MAP_DICT[self.current_player.sprite_room]["DIRECTIONS"])
                        self.options.move_menu.enable()
                    elif response == "Accuse / Suspect":
                        self.options.accusation_menu.enable()
                # Quit game in the case of a quit event
                if event.type == pygame.QUIT:
                    # Exit the main loop
                    running = False

            if self.program_state == "MENU":
                self.menu_loop(bool_update_opacity)
            elif self.program_state == "GAME":
                self.game_loop(bool_animate, move_direction)

            self.options.accusation_menu.mainloop(events)
            self.options.move_menu.mainloop(events)

            pygame.display.update()

    def update_opacity(self, bool_update_opacity):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.START_X < mouse[0] < self.START_X + self.START_SIZE[0] and self.START_Y < mouse[1] < self.START_Y + self.START_SIZE[1]:
            self.start_opacity = 255

            # Check if the button is clicked
            if click[0] == 1:
                self.screen_opacity = 0
                self.menu_state = "START"

        elif bool_update_opacity:
            if self.opacity_direction == "UP":
                self.start_opacity = self.start_opacity + 5
                if self.start_opacity > 200:
                    self.opacity_direction = "DOWN"
            else:
                self.start_opacity = self.start_opacity - 5
                if self.start_opacity < 100:
                    self.opacity_direction = "UP"

    def fade_screen(self, opacity):
        fade = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        fade.fill(self.BLACK)
        fade.set_alpha(opacity)
        self.screen.blit(fade, (0, 0))
        #pygame.display.update()


    def menu_loop(self, bool_update_opacity):

        # Initialize values
        if self.menu_state == "INIT":
            self.screen_opacity = 255
            self.menu_state = "OPENING"

        # Fade into the opening
        if self.menu_state == "OPENING":
            self.screen_opacity = self.screen_opacity - 5
            self.screen.blit(self.house_image, (0, 0))
            self.fade_screen(self.screen_opacity)
            if self.screen_opacity < 0:
                self.screen_opacity = 0
                self.menu_state = "WAITING"

        # Wait for the start button to be pressed
        elif self.menu_state == "WAITING":
            # Draw the background
            self.screen.blit(self.house_image, (0,0))
            # Draw the logo
            self.screen.blit(self.logo_image, [self.LOGO_X, 20])
            # Draw the start button
            self.update_opacity(bool_update_opacity)
            self.blit_alpha(self.screen, self.start_image, [self.START_X, self.START_Y], self.start_opacity)

        # Fade out to start the game
        elif self.menu_state == "START":
            self.screen_opacity = self.screen_opacity + 5
            self.screen.blit(self.house_image, (0, 0))
            self.fade_screen(self.screen_opacity)
            if self.screen_opacity == 255:
                self.screen_opacity = 255
                self.program_state = "GAME"



    def game_loop(self, bool_animate, move_direction):
        if self.game_state == "INIT":
            self.screen_opacity = 255
            self.game_state = "FADE_IN"
        elif self.game_state == "FADE_IN":
            self.screen_opacity = self.screen_opacity - 2
            self.draw_map()
            self.fade_screen(self.screen_opacity)
            if self.screen_opacity < 0:
                self.game_state = "WAITING"
        elif self.game_state == "WAITING":
            # Drwaw the map
            self.draw_map()

            # Draw the players
            for player in self.player_list:
                if not player == self.current_player:
                    player.animate(bool_animate, self.screen)
            self.current_player.animate(bool_animate, self.screen)

            # Check for a movement action
            move_direction = "NONE"
            if self.options.move_chosen:
                move_direction = self.options.move_direction
                self.options.move_chosen = False

            if move_direction == "RIGHT":
                direction_index = self.MAP_DICT[self.current_player.sprite_room]["DIRECTIONS"].index(move_direction)
                new_room = self.MAP_DICT[self.current_player.sprite_room]["ROOMS"][direction_index]
                self.current_player.move("RIGHT", self.MAP_DICT[new_room]["LOCATION"], new_room)
                self.game_state = "MOVE_PLAYER"
            elif move_direction == "LEFT":
                direction_index = self.MAP_DICT[self.current_player.sprite_room]["DIRECTIONS"].index(move_direction)
                new_room = self.MAP_DICT[self.current_player.sprite_room]["ROOMS"][direction_index]
                self.current_player.move("LEFT", self.MAP_DICT[new_room]["LOCATION"], new_room)
                self.game_state = "MOVE_PLAYER"
            elif move_direction == "DOWN":
                direction_index = self.MAP_DICT[self.current_player.sprite_room]["DIRECTIONS"].index(move_direction)
                new_room = self.MAP_DICT[self.current_player.sprite_room]["ROOMS"][direction_index]
                self.current_player.move("DOWN", self.MAP_DICT[new_room]["LOCATION"], new_room)
                self.game_state = "MOVE_PLAYER"
            elif move_direction == "UP":
                direction_index = self.MAP_DICT[self.current_player.sprite_room]["DIRECTIONS"].index(move_direction)
                new_room = self.MAP_DICT[self.current_player.sprite_room]["ROOMS"][direction_index]
                self.current_player.move("UP", self.MAP_DICT[new_room]["LOCATION"], new_room)
                self.game_state = "MOVE_PLAYER"
        elif self.game_state == "MOVE_PLAYER":
            self.draw_map()
            for player in self.player_list:
                player.animate(bool_animate, self.screen)
            if self.current_player.sprite_state == "WAIT":
                self.game_state = "CHANGE_PLAYER"
        elif self.game_state == "CHANGE_PLAYER":
            self.current_player.bool_is_active = False
            player_number = self.current_player.player_number
            if player_number == 6:
                player_number = 1
            else:
                player_number = player_number + 1
            self.current_player = self.player_list[player_number - 1]
            self.current_player.bool_is_active = True
            self.options.update_player_info(
                self.current_player.player_number,
                self.current_player.player_name,
                self.current_player.character,
                "Col. Mustard",
                "Rope",
                "Sutdy"
            )
            self.game_state = "WAITING"
            self.update_options_menu()


    def draw_map(self):
        # Clear the screen
        self.screen.fill(self.BLACK)

        # Draw the map
        self.screen.blit(self.map_image, (self.MAP_Y, self.MAP_X))

        # Draw the options screen
        text_rect = self.options.title_surface.get_rect(center=(self.SCREEN_DIVIDER_START + self.OPTIONS_WIDTH / 2, self.options.title_surface.get_size()[1] / 2))
        self.screen.blit(self.options.title_surface, text_rect)

        options_row = self.options.title_surface.get_size()[1]
        self.screen.blit(self.options.player_info_surface, (self.SCREEN_DIVIDER_START + 10, options_row))

        # Print screen separator
        line_start = (self.ROOM_DIMENSIONS + self.MAP_WIDTH + self.ROOM_DIMENSIONS, 0)
        line_end = (self.ROOM_DIMENSIONS + self.MAP_WIDTH + self.ROOM_DIMENSIONS, self.SCREEN_HEIGHT)
        pygame.draw.line(self.screen, self.WHITE, line_start, line_end, 5)


game = Clueless()
game.main_loop()