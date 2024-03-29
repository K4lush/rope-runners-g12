import pygame


class AnimatedSprite:
    
    def __init__(self, images, frame_rate, initially_flipped=False, lava=None):
        self.original_images = images
        self.images = images[:]
        self.frame_rate = frame_rate
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.flipped = initially_flipped
        self.lava = lava    
        self.lava = lava    
        self.died_state_started = False  # Initialize the 'died' state tracker
        self.animation_completed = False
        self.completed_once = False
        self.flagDone = False

        if self.flipped:
            self.flip_images()

    
    def update(self, action=None):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            
            if action == 'died':
                   
                    if self.died_state_started and not self.completed_once:
                        self.animation_completed = True
                        self.completed_once = True
                       
            if action == 'gotten':
                if self.current_frame == len(self.images):
                    self.flagDone = True

   
    def draw(self, surface, position, offset_x=0, offset_y=0):
        
       
        offset_position = (position[0] - offset_x, position[1] - offset_y)
        # Draw the current frame of the animation on the given surface.
        frame = self.images[self.current_frame]
        surface.blit(frame, offset_position)
    def flip_images(self, force_flip=False):
        if self.flipped != True or force_flip:
            self.images = [pygame.transform.flip(img, True, False) for img in self.original_images]
            self.flipped = not self.flipped
        else:
            self.images = self.original_images[:]
            self.flipped = False

    def set_flipped(self, flipped):
        if self.flipped != flipped:
            self.flip_images()