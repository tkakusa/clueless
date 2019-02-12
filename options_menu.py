import pygame, pygameMenu
import copy


class Button:
    def __init__(self, color, text):
        self.color = color
        self.font = pygame.font.SysFont('stencil', 60)
        self.text_value = text
        self.text = self.font.render(text, False, (255, 255, 255))
        self.rect = self.text.get_rect()

    def clicked(self):
        return self.text_value

class Options:
    def __init__(self):

        # Variables
        self.TITLE_HEIGHT = 0
        self.TITLE_WIDTH = 0
        self.PLAYER_INFO_HEIGHT = 0
        self.PLAYER_INFO_WIDTH = 0
        self.PLAYER_INFO_SURFACE_RATIO = 0
        self.SCALED_WIDTH = 0
        self.SCALED_HEIGHT = 0
        self.button_starts = [0,0]

        # Move parameters
        self.move_direction = None
        self.move_chosen = False

        # Accusation variables
        self.who_accusation = None
        self.what_accusation = None
        self.where_accusation = None
        self.bool_accuse = False
        self.accuse_chosen = False

        # Fonts
        self.title_font = pygame.font.SysFont('goudy', 100)
        self.category_font = pygame.font.SysFont('stencil', 80)
        self.text_font = pygame.font.SysFont('stencil', 60)

        self.player_info_surface = None
        self.player_info = []

        # Menus
        self.accusation_menu = None
        self.move_menu = None

        # Update title surface
        self.title_surface = self.title_font.render('THE CLUE-LESS GAME', False, (255, 255, 255))
        self.TITLE_WIDTH, self.TITLE_HEIGHT = self.title_surface.get_size()

        # Create the buttons
        self.buttons = []
        self.buttons.append(Button((0, 255, 0), "Move"))
        self.buttons.append(Button((255, 0, 0), "Accuse / Suspect"))

        # Update the player info screen
        self.update_player_info(1, "Miss Scarlet", "Red Demon", "Col. Mustard", "Rope", "Study")


    def draw_button(self, screen, button, location):
        button.rect.x, button.rect.y = location
        black_rect = copy.copy(button.rect)
        black_rect.x = button.rect.x + 20
        black_rect.y = button.rect.y + 20
        black_rect.w = button.rect.w - 40
        black_rect.h = button.rect.h - 40
        text_rect = button.text.get_rect(
            center=(button.rect.x + button.rect.w / 2, button.rect.y + button.rect.h / 2))
        pygame.draw.rect(screen, button.color, button.rect)
        pygame.draw.rect(screen, (0,0,0), black_rect)
        screen.blit(button.text, text_rect)


    def update_player_info(self, player_number, player_name, character, suspects, weapons, rooms):
        self.player_info = []
        self.player_info.append(self.category_font.render('PLAYER INFO', False, (255, 255, 255)))
        self.player_info.append(self.text_font.render(' ', False, (255, 255, 255)))
        self.player_info.append(self.text_font.render('Player Number: ' + str(player_number), False, (255, 255, 255)))
        self.player_info.append(self.text_font.render(' ', False, (255, 255, 255)))
        self.player_info.append(self.text_font.render('Player Name:       ' + player_name, False, (255, 255, 255)))
        self.player_info.append(self.text_font.render(' ', False, (255, 255, 255)))
        self.player_info.append(self.text_font.render('Character:          ' + character, False, (255, 255, 255)))
        self.player_info.append(self.text_font.render(' ', False, (255, 255, 255)))
        self.player_info.append(self.text_font.render('Starting Cards:', False, (255, 255, 255)))
        self.player_info.append(self.text_font.render(' ', False, (255, 255, 255)))
        self.player_info.append(self.text_font.render('          Suspects:    ' + suspects, False, (255, 255, 255)))
        self.player_info.append(self.text_font.render('          Weapons:     ' + weapons, False, (255, 255, 255)))
        self.player_info.append(self.text_font.render('          Rooms:          ' + rooms, False, (255, 255, 255)))
        self.player_info.append(self.text_font.render(' ', False, (255, 255, 255)))

        self.PLAYER_INFO_HEIGHT = 0
        self.PLAYER_INFO_WIDTH = 1000
        temp_surface = pygame.Surface((2560, 2560))
        for info in self.player_info:
            rect = info.get_size()
            temp_surface.blit(info, (0, self.PLAYER_INFO_HEIGHT))
            self.PLAYER_INFO_HEIGHT = self.PLAYER_INFO_HEIGHT + rect[1]

        count = 0
        for button in self.buttons:
            self.button_starts[count] = self.PLAYER_INFO_HEIGHT
            button.rect.w = self.PLAYER_INFO_WIDTH
            button.rect.h = button.text.get_rect().h * 4
            self.draw_button(temp_surface, button, (0, self.PLAYER_INFO_HEIGHT))
            self.PLAYER_INFO_HEIGHT = self.PLAYER_INFO_HEIGHT + button.rect.h + 40
            count = count + 1

        self.PLAYER_INFO_SURFACE_RATIO = self.PLAYER_INFO_HEIGHT / self.PLAYER_INFO_WIDTH
        self.player_info_surface = pygame.Surface((self.PLAYER_INFO_WIDTH, self.PLAYER_INFO_HEIGHT))
        self.player_info_surface.blit(temp_surface, (0, 0))

    def update_scaled_values(self, width, height):
        self.SCALED_WIDTH = width
        self.SCALED_HEIGHT = height

    def check_button_clicked(self, position, offset):
        count = 0
        scaled_ratio = self.SCALED_HEIGHT / self.PLAYER_INFO_HEIGHT
        for button in self.buttons:
            rect = button.text.get_rect()
            rect_x = rect.x + offset[0]
            rect_y = rect.y + offset[1] + int(self.button_starts[count] * scaled_ratio)
            rect_w = self.SCALED_WIDTH
            rect_h = int(rect.h * 4 * scaled_ratio)
            if rect_x + rect_w > position[0] > rect_x and rect_y + rect_h > position[1] > rect_y:
                return button.clicked()
            count = count + 1

        return "None"

    def init_move_menu(self, screen, directions):
        H_SIZE = 600
        W_SIZE = 600
        screen_width, screen_height = screen.get_size()
        formatted_directions = []
        for direction in directions:
            formatted_directions.append((direction, direction))

        self.move_menu = pygameMenu.Menu(screen,
                                         dopause=False,
                                         enabled=False,
                                         font=pygameMenu.fonts.FONT_NEVIS,
                                         menu_alpha=85,
                                         menu_color=(0, 0, 0),  # Background color
                                         menu_color_title=(0, 0, 255),
                                         menu_height=int(H_SIZE / 2),
                                         menu_width=W_SIZE,
                                         onclose=pygameMenu.locals.PYGAME_MENU_CLOSE,
                                         # If this menu closes (press ESC) back to main
                                         title='Move',
                                         title_offsety=10,  # Adds 5px to title vertical position
                                         window_height=screen_height,
                                         window_width=screen_width
                                         )

        self.move_menu.add_selector('Move to?',
                                    formatted_directions,
                                    onchange=self.update_move_direction,
                                    onreturn=self.update_move_direction,
                                    default=1
                                    )
        self.move_menu.add_option('Done', self.movement_chosen)
        self.move_menu.add_option('Cancel', pygameMenu.locals.PYGAME_MENU_CLOSE)

    def init_accusation_menu(self, screen):
        H_SIZE = 800
        W_SIZE = 800
        screen_width, screen_height = screen.get_size()
        self.accusation_menu = pygameMenu.Menu(screen,
                                               dopause=False,
                                               enabled=False,
                                               font=pygameMenu.fonts.FONT_NEVIS,
                                               menu_alpha=85,
                                               menu_color=(0, 0, 0),  # Background color
                                               menu_color_title=(255, 0, 0),
                                               menu_height=int(H_SIZE / 2),
                                               menu_width=W_SIZE,
                                               onclose=pygameMenu.locals.PYGAME_MENU_CLOSE,
                                               # If this menu closes (press ESC) back to main
                                               title='Suspect / Accuse',
                                               title_offsety=5,  # Adds 5px to title vertical position
                                               window_height=screen_height,
                                               window_width=screen_width
                                               )

        self.accusation_menu.add_selector('Who?',
                                          [('Miss Scarlet', 'Miss Scarlet'),
                                           ('Prof. Plum', 'Prof. Plum'),
                                           ('Col. Mustard', 'Col. Mustard'),
                                           ('Mrs. Peacock', 'Mrs. Peacock'),
                                           ('Mr. Green', 'Mr. Green'),
                                           ('Mrs. White', 'Mrs. White'),
                                           ],
                                          onchange=self.update_who_accusation,
                                          onreturn=self.update_who_accusation,
                                          default=1
                                          )

        self.accusation_menu.add_selector('What?',
                                          [('Candlestick', 'Candlestick'),
                                           ('Knife', 'Knife'),
                                           ('Lead Pipe', 'Lead Pipe'),
                                           ('Revolver', 'Revolver'),
                                           ('Rope', 'Rope'),
                                           ('Wrench', 'Wrench'),
                                           ],
                                          onchange=self.update_what_accusation,
                                          onreturn=self.update_what_accusation,
                                          default=1
                                          )

        self.accusation_menu.add_selector('Where?',
                                          [('Ballroom', 'Ballroom'),
                                           ('Billiard Room', 'Billiard Room'),
                                           ('Conservatory', 'Conservatory'),
                                           ('Dining Room', 'Dining Room'),
                                           ('Hall', 'Hall'),
                                           ('Kitchen', 'Kitchen'),
                                           ('Library', 'Library'),
                                           ('Lounge', 'Lounge'),
                                           ('Study', 'Study'),
                                           ],
                                          onchange=self.update_what_accusation,
                                          onreturn=self.update_what_accusation,
                                          default=1
                                          )
        self.accusation_menu.add_selector('Accuse?',
                                          [('Accuse', 'Accuse'),
                                           ('Suspect', 'Suspect'),
                                           ],
                                          onchange=self.accuse_supect,
                                          onreturn=self.accuse_supect,
                                          default=1
                                          )
        self.accusation_menu.add_option('Cancel', pygameMenu.locals.PYGAME_MENU_CLOSE)

    def update_move_direction(self, c, **kwargs):
        self.move_direction = c

    def update_who_accusation(self, c, **kwargs):
        self.who_accusation = c

    def update_what_accusation(self, c, **kwargs):
        self.what_accusation = c

    def update_where_accusation(self, c, **kwargs):
        self.where_accusation = c

    def accuse_supect(self, c, **kwargs):
        if c == "Accuse":
            self.bool_accuse = True
        else:
            self.bool_accuse = False

    def movement_chosen(self):
        self.move_menu.disable()
        self.move_chosen = True


