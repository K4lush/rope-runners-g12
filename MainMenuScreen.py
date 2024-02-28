from Button import Button
# from Game import GameState

import pygame

from text_input import TextInput
from Button import Button


class MainMenuScreen:
    def __init__(self, client_script):
        # Default Character if no character is chosen
        self.client = client_script
        self.character = 'NinjaFrog'

        self.switch_state = False
        self.screen = None
        self.character_sprites = self.load_characters_sprites()
        self.last_hovered_character = None
        self.current_state = "MAIN"
        self.ninja_button = Button(60, 150, 300, 60, color=(207, 185, 151),
                              highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=24,
                              text='Ninja Frog',
                              font='2d-game/assets/fonts/SC.ttf')  # Set up button parameters
        self.mask_button = Button(60, 225, 300, 60, color=(207, 185, 151),
                             highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=24,
                             text='Mask Dude',
                             font='2d-game/assets/fonts/SC.ttf')

        self.pink_button = Button(60, 300, 300, 60, color=(207, 185, 151),
                             highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=24,
                             text='Pink Man',
                             font='2d-game/assets/fonts/SC.ttf')  # Set up button parameters
        self.virtual_button = Button(60, 375, 300, 60, color=(207, 185, 151),
                                highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=24,
                                text='Virtual Guy',
                                font='2d-game/assets/fonts/SC.ttf')

        self.return_button = Button(450, 375, 300, 60, color=(207, 185, 151),
                               highlight_color=(207, 185, 151), font_color=(255, 255, 0), font_size=30,
                               text='Return',
                               font='2d-game/assets/fonts/SC.ttf')
        self.start_button = Button(250, 225, 300, 60, color=(207, 185, 151),
                              highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=24,
                              text='Start Game',
                             font='2d-game/assets/fonts/SC.ttf')

        self.select_character_button = Button(250, 300, 300, 60, color=(207, 185, 151),
                                         highlight_color=(207, 185, 151), font_color=(255, 255, 255), font_size=24,
                                         text='Select Character',
                                        font='2d-game/assets/fonts/SC.ttf')

        self.play_game_sprite = pygame.image.load('2d-game/assets/menu/Buttons/Play.png').convert_alpha()
        self.settings_sprite = pygame.image.load('2d-game/assets/menu/Buttons/Settings.png').convert_alpha()

        button_height = self.start_button.rect.height  # Assuming both buttons have the same height

        self.play_game_sprite = pygame.transform.scale(
            self.play_game_sprite,
            (button_height, button_height)  # New width and height
        )
        self.settings_sprite = pygame.transform.scale(
            self.settings_sprite,
            (button_height, button_height)  # New width and height
        )

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("THIS IS EVENT", event)

                if self.start_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.switch_state = True

                if self.ninja_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.character = 'NinjaFrog'

                if self.select_character_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.current_state = "SHOW CHARACTER"

                if self.return_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.current_state = "MAIN"

                if self.mask_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.character = 'MaskDude'

                if self.pink_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.character = 'PinkMan'

                if self.virtual_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.character = 'VirtualGuy'




    def update(self):
        print("UPDATE: ", self.switch_state)

        if self.switch_state:
            return "PLAYING"

        # In your select_character method's loop
        self.ninja_button.update(pygame.mouse.get_pos())
        self.mask_button.update(pygame.mouse.get_pos())
        self.pink_button.update(pygame.mouse.get_pos())
        self.virtual_button.update(pygame.mouse.get_pos())
        self.return_button.update(pygame.mouse.get_pos())

        # Update the last hovered character based on button highlights
        if self.ninja_button.highlighted:
            self.last_hovered_character = 'NinjaFrog'
        elif self.mask_button.highlighted:
            self.last_hovered_character = 'MaskDude'
        elif self.pink_button.highlighted:
            self.last_hovered_character = 'PinkMan'
        elif self.virtual_button.highlighted:
            self.last_hovered_character = 'VirtualGuy'

    def render(self, screen):
        if not self.screen:
            self.screen = screen

        if self.current_state == "MAIN":
            self.start_button.draw(screen)
            self.select_character_button.draw(screen)

            # Position for the Play sprite (beside the Start Game button)
            play_sprite_x = self.start_button.rect.right + 10  # 10 pixels to the right
            play_sprite_y = self.start_button.rect.y
            screen.blit(self.play_game_sprite, (play_sprite_x, play_sprite_y))

            # Position for the Settings sprite (beside the Select Character button)
            settings_sprite_x = self.select_character_button.rect.right + 10  # 10 pixels to the right
            settings_sprite_y = self.select_character_button.rect.y
            screen.blit(self.settings_sprite, (settings_sprite_x, settings_sprite_y))

        elif self.current_state == "SHOW CHARACTER":
            self.ninja_button.draw(screen)
            self.mask_button.draw(screen)
            self.pink_button.draw(screen)
            self.virtual_button.draw(screen)
            self.virtual_button.draw(screen)
            self.return_button.draw(screen)

        # Render the run animation if a character is hovered
        if self.last_hovered_character and self.current_state == 'SHOW CHARACTER':
            self.display_run_animation(self.last_hovered_character, screen)

    def display_run_animation(self, character, screen, scale_factor=3):  # Added scale_factor argument
            frames = self.character_sprites[character]['idle']
            current_time = pygame.time.get_ticks()
            frame_index = (current_time // 50) % len(frames)
            current_frame = frames[frame_index]

            # Scale the current frame
            scaled_frame = pygame.transform.scale(current_frame, (
            current_frame.get_width() * scale_factor, current_frame.get_height() * scale_factor))

            animation_pos = (500, 150)  # Adjust as necessary
            screen.blit(scaled_frame, animation_pos)

    def load_characters_sprites(self):
        characters = {
            'NinjaFrog': {
                'idle': self.load_animation_frames('NinjaFrog', 'idle', 11),
                'run': self.load_animation_frames('NinjaFrog', 'run', 12),
                'died': self.load_animation_frames('NinjaFrog', 'died', 7),
                # Add more animations for NinjaFrog as needed
            },
            'MaskDude': {
                'idle': self.load_animation_frames('MaskDude', 'idle', 11),
                'run': self.load_animation_frames('MaskDude', 'run', 12),
                'died': self.load_animation_frames('MaskDude', 'died', 7),
                # Add more animations for MaskDude as needed
            },
            'PinkMan': {
                'idle': self.load_animation_frames('PinkMan', 'idle', 11),
                'run': self.load_animation_frames('PinkMan', 'run', 12),
                # 'died': self.load_animation_frames('PinkMan', 'died', 7),
                # Add more animations for NinjaFrog as needed
            },
            'VirtualGuy': {
                'idle': self.load_animation_frames('VirtualGuy', 'idle', 11),
                'run': self.load_animation_frames('VirtualGuy', 'run', 12),
                # 'died': self.load_animation_frames('VirtualGuy', 'died', 7),
                # Add more animations for MaskDude as needed
            }
            # Add more characters as needed
        }
        return characters

    def load_animation_frames(self, character_folder, action, num_frames,
                              scale_factor=2):  # Added scale_factor argument
        path = f'2d-game/assets/MainCharacters/{character_folder}/{action}.png'
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()

        frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (
                frame_width * scale_factor, frame_height * scale_factor))  # Scale frame
            frames.append(scaled_frame)

        return frames



