import glob
import pygame
import copy

class Player:

    def __init__(self, sprite_file, sprite_location):
        ## Variables ##
        self.current_sprite = 0
        self.sprites = []
        self.sprite_state = "WAIT"
        self.sprite_direction = "RIGHT"
        self.sprite_location = sprite_location
        self.final_location = sprite_location

        # Load sprites
        location_list = glob.glob(sprite_file + "\\*")

        for location in location_list:
            self.sprites.append(pygame.image.load(location))

    def stop(self):
        self.current_sprite = 0
        self.sprite_state = "WAIT"

    def move(self, direction, final_location):
        self.current_sprite = 0
        self.sprite_state = "MOVE"
        self.sprite_direction = direction
        self.final_location = final_location

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return copy.copy(self.sprite_location)

    def animate(self, bool_animate, screen):
        if bool_animate:
            if self.sprite_state == "WAIT":
                self.current_sprite = self.current_sprite + 1
                if self.current_sprite > 1:
                    self.current_sprite = 0
            if self.sprite_state == "MOVE":
                if self.sprite_direction == "RIGHT":
                    self.current_sprite = self.current_sprite + 1
                    if self.current_sprite > 3:
                        self.current_sprite = 0

                    self.sprite_location[0] = self.sprite_location[0] + 1

                if self.sprite_direction == "DOWN":
                    self.current_sprite = self.current_sprite + 1
                    if self.current_sprite > 1:
                        self.current_sprite = 0

                    self.sprite_location[1] = self.sprite_location[1] + 1

                if self.sprite_location == self.final_location:
                    self.current_sprite = 0
                    self.sprite_state = "WAIT"


        screen.blit(self.sprites[self.current_sprite], self.sprite_location)