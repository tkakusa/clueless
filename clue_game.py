import pygame

class Clueless:
    def __init__(self):
        # Initialize the pygame module
        pygame.init()

        # Set the title of the screen
        pygame.display.set_caption("The Game of Clue-Less")

        # Create the actual screen
        self.screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

        # Color variables
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        
        # Variables
        self.ROOM_DIMENSIONS = 200
        self.MAP_WIDTH = self.ROOM_DIMENSIONS * 5
        self.MAP_HEIGHT = self.ROOM_DIMENSIONS * 5
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080
        self.screen_opacity = 0
        self.start_opacity = 150

        self.ROW_0 = 200
        self.ROW_1 = self.ROW_0 + 1 * self.ROOM_DIMENSIONS
        self.ROW_2 = self.ROW_0 + 2 * self.ROOM_DIMENSIONS
        self.ROW_3 = self.ROW_0 + 3 * self.ROOM_DIMENSIONS
        self.ROW_4 = self.ROW_0 + 4 * self.ROOM_DIMENSIONS
        self.COL_0 = 200
        self.COL_1 = self.COL_0 + 1 * self.ROOM_DIMENSIONS
        self.COL_2 = self.COL_0 + 2 * self.ROOM_DIMENSIONS
        self.COL_3 = self.COL_0 + 3 * self.ROOM_DIMENSIONS
        self.COL_4 = self.COL_0 + 4 * self.ROOM_DIMENSIONS

        # Initialize clock and timer
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 100)

        # Load Images
        self.logo_image = pygame.image.load('images\logo2.png')
        self.house_image = pygame.image.load('images\house.jpg')
        self.start_image = pygame.image.load('images\start.png').convert_alpha()
        self.start_image.set_alpha(20)

        # Update the images
        self.update_images()

        # Screen fade parameters
        self.fade = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.fade.fill(self.BLACK)

        # State enums
        self.program_state = "MENU"
        self.menu_state = "INIT"
        self.game_state = "INIT"
        self.opacity_direction = "UP"

    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)

    def update_images(self):
        ## Transform images ##
        # Logo image
        logo_width = int(self.SCREEN_WIDTH * .6)
        logo_height = int(logo_width / 7)
        self.logo_image = pygame.transform.scale(self.logo_image, (logo_width, logo_height))

        # House image
        self.house_image = pygame.transform.scale(self.house_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Start image
        start_width = int(self.SCREEN_WIDTH / 12)
        start_height = int(start_width / 4)
        self.start_image =pygame.transform.scale(self.start_image, (start_width, start_height))

        ## UPdate image locations ##
        # Logo location parameters
        self.LOGO_SIZE = self.logo_image.get_size()
        self.LOGO_X = (self.SCREEN_WIDTH - self.LOGO_SIZE[0]) / 2
        self.LOGO_Y = (self.SCREEN_HEIGHT - self.LOGO_SIZE[1]) / 2

        # Start location parameters
        self.START_SIZE = self.start_image.get_size()
        self.START_X = (self.SCREEN_WIDTH - self.START_SIZE[0]) / 2
        self.START_Y = (self.SCREEN_HEIGHT - self.START_SIZE[1] - 100)


    def main_loop(self):
        # Variable to show if game is still running
        running = True

        while running:
            # Boolean Variables
            bool_update_opacity = False

            # event handler
            for event in pygame.event.get():
                # Timer events
                if event.type == pygame.USEREVENT:
                    bool_update_opacity = True
                # Resize the window in case of a resize event
                if event.type == pygame.VIDEORESIZE:
                    self.SCREEN_WIDTH = event.w
                    self.SCREEN_HEIGHT = event.h
                    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)

                    # Update the images
                    self.update_images()

                    if self.program_state == "GAME":
                        # Draw the map
                        self.draw_map()

                # Quit game in the case of a quit event
                if event.type == pygame.QUIT:
                    # Exit the main loop
                    running = False

            if self.program_state == "MENU":
                self.menu_loop(bool_update_opacity)
            elif self.program_state == "GAME":
                self.game_loop()

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
            self.screen_opacity = self.screen_opacity - 2
            self.screen.blit(self.house_image, (0, 0))
            self.fade_screen(self.screen_opacity)
            if self.screen_opacity < 0:
                self.menu_state = "WAITING"

        elif self.menu_state == "WAITING":
            # Draw the background
            self.screen.blit(self.house_image, (0,0))
            # Draw the logo
            self.screen.blit(self.logo_image, [self.LOGO_X, 20])
            # Draw the start button
            self.update_opacity(bool_update_opacity)
            self.blit_alpha(self.screen, self.start_image, [self.START_X, self.START_Y], self.start_opacity)

        elif self.menu_state == "START":
            self.screen_opacity = self.screen_opacity + 5
            self.screen.blit(self.house_image, (0, 0))
            self.fade_screen(self.screen_opacity)
            if self.screen_opacity == 255:
                self.program_state = "GAME"



    def game_loop(self):
        if self.game_state == "INIT":
            self.screen_opacity = 255
            self.game_state = "FADE_IN"
        elif self.game_state == "FADE_IN":
            self.screen_opacity = self.screen_opacity - 2
            self.draw_map()
            self.fade_screen(self.screen_opacity)
            if self.screen_opacity < 0:
                self.game_state = "WAITING"


    def draw_map(self):
        # Clear the screen
        self.screen.fill(self.BLACK)
        # Room variables
        room_study = pygame.Rect(self.COL_0, self.ROW_0, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS)
        room_hall = pygame.Rect(self.COL_0, self.ROW_2, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS)
        room_lounge = pygame.Rect(self.COL_0, self.ROW_4, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS)
        room_library = pygame.Rect(self.COL_2, self.ROW_0, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS)
        room_billiard = pygame.Rect(self.COL_2, self.ROW_2, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS)
        room_dining = pygame.Rect(self.COL_2, self.ROW_4, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS)
        room_conservatory = pygame.Rect(self.COL_4, self.ROW_0, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS)
        room_ballroom = pygame.Rect(self.COL_4, self.ROW_2, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS)
        room_kitchen = pygame.Rect(self.COL_4, self.ROW_4, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS)

        # Print rooms on screen
        pygame.draw.rect(self.screen, self.WHITE, room_study)
        pygame.draw.rect(self.screen, self.WHITE, room_hall)
        pygame.draw.rect(self.screen, self.WHITE, room_lounge)
        pygame.draw.rect(self.screen, self.WHITE, room_library)
        pygame.draw.rect(self.screen, self.WHITE, room_billiard)
        pygame.draw.rect(self.screen, self.WHITE, room_dining)
        pygame.draw.rect(self.screen, self.WHITE, room_conservatory)
        pygame.draw.rect(self.screen, self.WHITE, room_ballroom)
        pygame.draw.rect(self.screen, self.WHITE, room_kitchen)

        # Print hallways on screen
        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.COL_0 + self.ROOM_DIMENSIONS / 3, self.ROW_1, self.ROOM_DIMENSIONS / 3, self.ROOM_DIMENSIONS))
        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.COL_0 + self.ROOM_DIMENSIONS / 3, self.ROW_3, self.ROOM_DIMENSIONS / 3, self.ROOM_DIMENSIONS))
        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.COL_1, self.ROW_0 + self.ROOM_DIMENSIONS / 3, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS / 3))
        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.COL_1, self.ROW_2 + self.ROOM_DIMENSIONS / 3, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS / 3))
        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.COL_1, self.ROW_4 + self.ROOM_DIMENSIONS / 3, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS / 3))
        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.COL_2 + self.ROOM_DIMENSIONS / 3, self.ROW_1, self.ROOM_DIMENSIONS / 3, self.ROOM_DIMENSIONS))
        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.COL_2 + self.ROOM_DIMENSIONS / 3, self.ROW_3, self.ROOM_DIMENSIONS / 3, self.ROOM_DIMENSIONS))
        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.COL_3, self.ROW_0 + self.ROOM_DIMENSIONS / 3, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS / 3))
        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.COL_3, self.ROW_2 + self.ROOM_DIMENSIONS / 3, self.ROOM_DIMENSIONS, self.ROOM_DIMENSIONS / 3))
        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.COL_3, self.ROW_4 +self.ROOM_DIMENSIONS / 3,self.ROOM_DIMENSIONS,self.ROOM_DIMENSIONS / 3))
        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.COL_4 +self.ROOM_DIMENSIONS / 3, self.ROW_1,self.ROOM_DIMENSIONS / 3,self.ROOM_DIMENSIONS))
        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.COL_4 +self.ROOM_DIMENSIONS / 3, self.ROW_3,self.ROOM_DIMENSIONS / 3,self.ROOM_DIMENSIONS))

        # Print screen separator
        line_start = (self.ROOM_DIMENSIONS + self.MAP_WIDTH + self.ROOM_DIMENSIONS, 0)
        line_end = (self.ROOM_DIMENSIONS + self.MAP_WIDTH + self.ROOM_DIMENSIONS, self.SCREEN_HEIGHT)
        pygame.draw.line(self.screen, self.WHITE, line_start, line_end, 5)


game = Clueless()
game.main_loop()