import pygame
from cv2.typing import MatLike

from utils.sprite_handler import SpriteHandler


class BaseEntity:
    _hp: int
    _attack: int
    _hitbox: list
    _sprite: pygame.sprite.Sprite

    def __init__(self, hp: int, attack: int, hitbox: list) -> None:
        self._hp = hp
        self._attack = attack
        self._hitbox = hitbox
    
    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, action: int) -> None:
        if not isinstance(action, int):
            raise ValueError("Action should be integer!")
            return
        
        self._hp = action


class Knight(pygame.sprite.Sprite):
    """Knight is a class for the player"""
    _hp: int
    _attack: int
    _sprite: pygame.sprite.Sprite
    _speed: int
    _init_pos: tuple[int]
    facing_right: bool = True

    def __init__(self, hp: int, attack: int, group: pygame.sprite.Group, speed: int, init_pos: tuple[int]) -> None:
        super().__init__(group)
        self._hp = hp
        self._attack = attack
        self._speed = speed

        self.sprite_handler = SpriteHandler(
            char_sprite="Knight",
            walk_sheet_path_up = "./assets/Adventure/Walk/walk_up.png", 
            walk_sheet_path_down = "./assets/Adventure/Walk/walk_down.png",
            walk_sheet_path_left = "./assets/Adventure/Walk/walk_left_down.png",
            walk_sheet_path_right = "./assets/Adventure/Walk/walk_right_down.png"
        )

        self.direction = "down"
        self.frame_index = 0
        self.animation_speed = 0.4

        # try:
        #     sprite = pygame.image.frombuffer(sprite_handler.sprite.tobytes(), sprite_handler.sprite.shape[1::-1], "RGB")
        # except:
        #     print(f"{sprite_handler.sprite.shape=}")
        #     return
        self.image = self._get_current_frame()
        self.rect = self.image.get_rect(center=init_pos)

        self.hitbox_margin = 8
        self.hitbox = pygame.Rect(
            self.rect.x + self.hitbox_margin,
            self.rect.y + self.hitbox_margin,
            self.rect.width - self.hitbox_margin*2,
            self.rect.height - self.hitbox_margin*2
        )
        # self.image = Surface((50, 50))
        # self.image.fill((255, 0, 0))  # bright red square
        # self.rect = self.image.get_rect(center=(320, 240))
    def _get_current_frame(self) -> pygame.Surface:
        """Return current pygame Surface for the knight’s facing direction."""
        frames = self.sprite_handler.animation[self.direction]
        frame: MatLike = frames[int(self.frame_index) % len(frames)]

        return pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
    
    def handle_input(self, keys) -> None:
        moving = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= self._speed
            self.direction = "left"
            moving = True
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self._speed
            self.direction = "right"
            moving = True
        elif keys[pygame.K_UP]:
            self.rect.y -= self._speed
            self.direction = "up"
            moving = True
        elif keys[pygame.K_DOWN]:
            self.rect.y += self._speed
            self.direction = "down"
            moving = True
        if moving:
            self.frame_index += self.animation_speed
        else:
            self.frame_index = 0  # reset to idle

        # Cycle frames
        if self.frame_index >= len(self.sprite_handler.animation[self.direction]):
            self.frame_index = 0

        # Update sprite image
        self.image = self._get_current_frame()

        # Update hitbox position
        self.hitbox.topleft = (
            self.rect.x + self.hitbox_margin,
            self.rect.y + self.hitbox_margin
        )

