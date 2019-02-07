import pygame

class Clueless:
    def __init__(self):
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

        # Menu location parameters
        self.LOGO_X = (self.SCREEN_WIDTH - 1650) / 2
        self.LOGO_Y = (self.SCREEN_HEIGHT - 1275) / 2

        # State enums
        self.game_state = "MENU"
        self.menu_state = "OPENING"

        # Load Images
        self.logo_image = pygame.image.load('images\logo2.png')
        self.house_image = pygame.image.load('images\house.jpg')
        self.house_image = pygame.transform.scale(self.house_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Initialize the pygame module
        pygame.init()

        # Set the title of the screen
        pygame.display.set_caption("The Game of Clue-Less")

        # Create the actual screen
        self.screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

        # Draw the map
        # self.draw_map()
        
    def main_loop(self):

        # Variable to show if game is still running
        running = True

        while running:
            if self.game_state == "MENU":
                self.menu_loop()
            elif self.game_state == "GAME":
                self.game_loop()

            # event handler
            for event in pygame.event.get():
                # Resize the window in case of a resize event
                if event.type == pygame.VIDEORESIZE:
                    self.SCREEN_WIDTH = event.w
                    self.SCREEN_HEIGHT = event.h
                    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)

                    # Update the logo location
                    self.LOGO_X = (self.SCREEN_WIDTH - 1650) / 2

                    # Update house image size
                    self.house_image = pygame.transform.scale(self.house_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

                    if self.game_state == "GAME":
                        # Draw the map
                        self.draw_map()

                # Quit game in the case of a quit event
                if event.type == pygame.QUIT:
                    # Exit the main loop
                    running = False

            pygame.display.update()

    def menu_loop(self):

        # Draw the background
        self.screen.blit(self.house_image, (0,0))
        # Draw the logo
        self.screen.blit(self.logo_image, [self.LOGO_X, 20])

    def draw_map(self):
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