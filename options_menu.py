import pygame, pygameMenu
import copy
import clue_tracker


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
        self.CLUETRACKER_WIDTH = 0
        self.CLUETRACKER_HEIGHT = 0
        self.CLUETRACTER_SURFACE_RATIO = 0
        self.SCALED_WIDTH = 0
        self.SCALED_HEIGHT = 0
        self.TRACKER_SCALED_WIDTH = 180
        self.TRACKER_SCALED_HEIGHT = 180
        self.button_starts = [0,0,0]
        self.card_given = False
        self.passed = False
        self.card_to_give = None

        # Move parameters
        self.move_direction = None
        self.move_chosen = False

        # Accusation variables
        self.who_accusation = None
        self.what_accusation = None
        self.where_accusation = None
        self.bool_accuse = False
        self.accuse_chosen = False

        self.error_messages = [
            "Illegal move, cannot move to a hallway with someone already present",
            "You can only suspect the room you are currently in",
            "You must be in a room before you can suspect anyone",
            "The card you are trying to give is not one of the suspected cards",
            "Your hand contains one of the cards in the inquiry, you must give a card"
        ]

        self.general_messages = [
            "The card given was: ",
            "CONGRATULATIONS YOU WIN!!!!",
            "Sorry, you lose and are out of the game",
            "Everyone has been eliminated. No one has won the game"
        ]

        # Fonts
        self.title_font = pygame.font.SysFont('goudy', 100)
        self.category_font = pygame.font.SysFont('stencil', 80)
        self.text_font = pygame.font.SysFont('stencil', 60)

        self.player_info_surface = None
        self.player_info = []
        self.clue_tracker_surface = None

        # Menus
        self.accusation_menu = None
        self.move_menu = None
        self.illegal_move_menu = None
        self.suspect_menu = None
        self.illegal_suspection_menu = None
        self.general_message_menu = None

        # Create Clue tracker
        self.clue_tracker = clue_tracker.ClueTracker()
        self.update_clue_tracker()

        # Update title surface
        self.title_surface = self.title_font.render('THE CLUE-LESS GAME', False, (255, 255, 255))
        self.TITLE_WIDTH, self.TITLE_HEIGHT = self.title_surface.get_size()

        # Create the buttons
        self.buttons = []
        self.buttons.append(Button((0, 255, 0), "Move"))
        self.buttons.append(Button((255, 0, 0), "Accuse / Suspect"))
        self.buttons.append(Button((0, 0, 255), "Pass"))

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

    def update_clue_tracker(self):
        box_size = self.clue_tracker.BOX_SIZE
        row_count = self.clue_tracker.ROW_SIZE
        col_count = self.clue_tracker.COL_SIZE

        self.clue_tracker.draw()
        self.CLUETRACKER_WIDTH = box_size * col_count + 200
        self.CLUETRACKER_HEIGHT = box_size * row_count
        self.CLUETRACTER_SURFACE_RATIO = self.CLUETRACKER_WIDTH/ self.CLUETRACKER_HEIGHT
        self.clue_tracker_surface = pygame.Surface((self.CLUETRACKER_WIDTH, self.CLUETRACKER_HEIGHT))
        self.clue_tracker_surface.blit(self.clue_tracker.clue_tracker_surface, [0,0])



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
        if suspects:
            self.player_info.append(self.text_font.render('          Suspects:    ' + suspects[0], False, (255, 255, 255)))
            for i in range(1, len(suspects)):
                self.player_info.append(
                    self.text_font.render('                                   ' + suspects[i], False, (255, 255, 255)))
        if weapons:
            self.player_info.append(self.text_font.render('          Weapons:     ' + weapons[0], False, (255, 255, 255)))
            for i in range(1, len(weapons)):
                self.player_info.append(
                    self.text_font.render('                                   ' + weapons[i], False, (255, 255, 255)))
        if rooms:
            self.player_info.append(self.text_font.render('          Rooms:          ' + rooms[0], False, (255, 255, 255)))
            for i in range(1, len(rooms)):
                self.player_info.append(
                    self.text_font.render('                                   ' + rooms[i], False, (255, 255, 255)))
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

    def update_tracker_scaled_values(self, width, height):
        self.TRACKER_SCALED_WIDTH = width
        self.TRACKER_SCALED_HEIGHT = height

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

        offset2 = [offset[0] + self.SCALED_WIDTH + 40, offset[1]]
        self.clue_tracker.clicked(position, offset2, self.TRACKER_SCALED_HEIGHT, self.TRACKER_SCALED_WIDTH)
        self.update_clue_tracker()

        return "None"

    def init_suspect_menu(self, screen, initiator, responder, cards):
        screen_width, screen_height = screen.get_size()
        text_menu = pygameMenu.TextMenu(screen,
                                        dopause=False,
                                        font=pygameMenu.fonts.FONT_FRANCHISE,
                                        menu_color=(30, 50, 107),  # Background color
                                        menu_color_title=(120, 45, 30),
                                        menu_width=600,
                                        menu_height=300,
                                        onclose=pygameMenu.locals.PYGAME_MENU_CLOSE,  # Pressing ESC button does nothing
                                        title='Suspection',
                                        window_height=screen_height,
                                        window_width=screen_width
                                        )
        text_menu.add_line(responder.upper())
        line_1 = "The player " + initiator.upper() + " has accused " + self.who_accusation.upper() + " of the"
        line_2 = "murder in the " + self.where_accusation.upper() + " with the " + self.what_accusation.upper()
        text_menu.add_line(line_1)
        text_menu.add_line(line_2)
        text_menu.add_option('Back', pygameMenu.locals.PYGAME_MENU_BACK)

        self.suspect_menu = pygameMenu.Menu(screen,
                                               dopause=False,
                                               enabled=False,
                                               font=pygameMenu.fonts.FONT_NEVIS,
                                               menu_alpha=85,
                                               menu_color=(0, 0, 0),  # Background color
                                               menu_color_title=(255, 0, 0),
                                               menu_height=400,
                                               menu_width=1200,
                                               onclose=pygameMenu.locals.PYGAME_MENU_CLOSE,
                                               # If this menu closes (press ESC) back to main
                                               title=responder.upper() + ': Suspection',
                                               title_offsety=5,  # Adds 5px to title vertical position
                                               window_height=screen_height,
                                               window_width=screen_width
                                               )
        self.suspect_menu.add_option('View Suspection', text_menu)
        self.suspect_menu.add_selector('Give card?',
                               cards,
                               onchange=self.update_card_given,
                               onreturn=self.update_card_given,
                               default=1
                               )
        self.suspect_menu.add_option('Give', self.give_card)
        self.suspect_menu.add_option('Pass', self.pass_turn)

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
                                          onchange=self.update_where_accusation,
                                          onreturn=self.update_where_accusation,
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
        self.accusation_menu.add_option('Done', self.done_accusing)
        self.accusation_menu.add_option('Cancel', pygameMenu.locals.PYGAME_MENU_CLOSE)

    def init_illegal_move_menu(self, screen, message_number):
        screen_width, screen_height = screen.get_size()
        self.illegal_move_menu = pygameMenu.TextMenu(screen,
                                dopause=False,
                                font=pygameMenu.fonts.FONT_FRANCHISE,
                                menu_color=(30, 50, 107),  # Background color
                                menu_color_title=(120, 45, 30),
                                menu_width=600,
                                menu_height=200,
                                onclose=pygameMenu.locals.PYGAME_MENU_CLOSE,  # Pressing ESC button does nothing
                                title='Illegal Move',
                                window_height=screen_height,
                                window_width=screen_width
                                )
        self.illegal_move_menu.add_line(self.error_messages[message_number])

    def init_general_message_menu(self, screen, message_number):
        message = self.general_messages[message_number]
        if message_number == 0:
            message = message + self.card_to_give
        screen_width, screen_height = screen.get_size()
        self.general_message_menu = pygameMenu.TextMenu(screen,
                                dopause=False,
                                font=pygameMenu.fonts.FONT_FRANCHISE,
                                menu_color=(30, 50, 107),  # Background color
                                menu_color_title=(120, 45, 30),
                                menu_width=600,
                                menu_height=200,
                                onclose=pygameMenu.locals.PYGAME_MENU_CLOSE,  # Pressing ESC button does nothing
                                title='General Message',
                                window_height=screen_height,
                                window_width=screen_width
                                )
        self.general_message_menu.add_line(message)

    def update_move_direction(self, c, **kwargs):
        self.move_direction = c

    def update_who_accusation(self, c, **kwargs):
        self.who_accusation = c

    def update_what_accusation(self, c, **kwargs):
        self.what_accusation = c

    def update_where_accusation(self, c, **kwargs):
        self.where_accusation = c

    def update_card_given(self, c, **kwargs):
        self.card_to_give = c

    def give_card(self):
        self.card_given = True

    def pass_turn(self):
        self.passed = True

    def accuse_supect(self, c, **kwargs):
        if c == "Accuse":
            self.bool_accuse = True
        else:
            self.bool_accuse = False

    def done_accusing(self):
        self.accuse_chosen = True

    def movement_chosen(self):
        self.move_chosen = True


