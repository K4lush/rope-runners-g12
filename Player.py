import pygame
import time
import pygame.mixer

class Player:
    
    def __init__(self, id, character, action, direction, x, y, width, height, colour, speed=5, collision=False):
        self.id = id
        self.character = character
        self.action = action
        self.direction = direction
        self.x = x
        self.y = y
        self.highest_y = self.y
        self.horizontalCollision = False
        self.VerticalCollision = False

        pygame.mixer.init()
        self.jump_sound = pygame.mixer.Sound('assets/SoundEffects/JumpSound.mp3')
        
        self.width = width
        self.height = height
        self.colour = colour
        self.speed = speed
        self.collision = collision
        self.collision = collision
        self.rect = pygame.Rect(x, y, width, height)
        self.is_jumping = False
        self.on_ground = False  # Initialize the on_ground flag
        self.jump_velocity = 0  # Initialize jump velocity
        self.gravity = 0.9  # Adjust this for desired gravity strength
        self.flagCollision = False

        self.last_jump_time = 0  # Timestamp of last jump
        self.jump_cooldown = 0.4  # Cooldown in seconds
        

        self.score = 0
        self.twoPlayers = False
       

        print("Player Width:", self.rect.width)
        print("Player Height:", self.rect.height)    

    def check_collision(self, sprite_mask, rect):
        block_mask = pygame.mask.from_surface(pygame.Surface((rect.width, rect.height)))
       

    # Offset the rectangle mask to match the position of the rectangle
        offset = (rect.left, rect.top)
        
        # Check for overlap
        overlap = sprite_mask.overlap(block_mask, offset)
        
        return overlap is not None
    def updateScore(self):

        if self.y < self.highest_y:
            self.highest_y = self.y
            self.score += 1
        

    def setAction(self, action):
            self.current_action = action
            self.current_frame = 0   

    # In your Player class
    def apply_gravity(self):
        """Makes the player fall downwards if they're not on the ground."""
        if not self.on_ground:
            self.jump_velocity += self.gravity  # Gravity pulls down
            self.y += self.jump_velocity
            self.update_rect()  # Update rect after changing y-position

    def to_json(self):
        return {
            'id': self.id,
            'character': self.character,
            'action': self.action,
            'direction': self.direction,
            'x': self.x,
            'y': self.y,
            'rect_centerx': self.rect.centerx,  # Add rect.centerx
            'rect_centery': self.rect.centery,  # Add rect.centery
            'collision':self.collision,
            'score':self.score,
            'twoPlayers':self.twoPlayers
            # ... other necessary attributes ...
        }

    def jump(self):
        current_time = time.time()

        """Starts a jump if the player is standing on the ground."""
        
        if self.on_ground and current_time - self.last_jump_time > self.jump_cooldown:
            self.jump_velocity = -15  # Negative velocity means upwards jump
            self.is_jumping = True
            self.on_ground = False
            self.last_jump_time = current_time  # Update last jump time
            self.update_rect()  # Update rect after changing y-position
            self.jump_sound.play()

    def handle_collisions(self, platforms):
        self.on_ground = False
        self.VerticalCollision = False
        self.horizontalCollision = False

        for platform in platforms:
            if self.rect.colliderect(platform):
                collision_side = self.get_collision_side(platform)
               

                if collision_side == "bottom":
                    self.VerticalCollision = True
                    self.y = platform.top - self.height
                    self.on_ground = True
                    self.jump_velocity = 0

                elif collision_side == "top":
                    self.y = platform.bottom
                    self.VerticalCollision = True
                    self.jump_velocity = 0

                elif collision_side == "left":
                    self.x = platform.right
                    self.horizontalCollision = True

                elif collision_side == "right":
                    self.x = platform.left - self.width
                    self.horizontalCollision = True

            self.update_rect()

    def hanldeFlagCollision(self, flags):
        for flag in flags:
            if self.rect.colliderect(flag.rect):
                flag.action = 'gotten'
                if flag.collision is False:
                    self.score += 100
                    flag.collision = True
                #self.flagCollision = True
            
            


    def get_collision_side(self, platform):
        # Calculate the sides of the player and the platform
        player_bottom = self.rect.bottom
        player_top = self.rect.top
        player_left = self.rect.left
        player_right = self.rect.right

        platform_bottom = platform.bottom
        platform_top = platform.top
        platform_left = platform.left
        platform_right = platform.right

        # Calculate the difference between each side
        bottom_diff = abs(player_bottom - platform_top)
        top_diff = abs(player_top - platform_bottom)
        left_diff = abs(player_left - platform_right)
        right_diff = abs(player_right - platform_left)

        # Find the minimum difference to determine the collision side
        min_diff = min(bottom_diff, top_diff, left_diff, right_diff)

        if min_diff == bottom_diff:
            return 'bottom'
        elif min_diff == top_diff:
            return 'top'
        elif min_diff == left_diff:
            return 'left'
        elif min_diff == right_diff:
            return 'right'

    def update_position_from_rect(self):
        # Update the player's position based on the rect
        self.x = self.rect.x
        self.y = self.rect.y
    def handleLavaCollisions(self,lavaBLocks):
        if self.y + self.height >= lavaBLocks[0].y:
            self.collision = True

    def move_left(self):
        self.x -= self.speed
        self.update_rect()

    def move_right(self):
        self.x += self.speed
        self.update_rect()

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y



