import pygame
from pygame.sprite import Sprite, Group

from utils.sprite_handler import SpriteHandler


class BaseEntity:
    _hp: int
    _attack: int
    _hitbox: list
    _sprite: Sprite

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


class Knight(Sprite):
    _hp: int
    _attack: int
    _hitbox: list
    _sprite: Sprite
    _speed: int
    facing_right: bool = True

    def __init__(self, hp: int, attack: int, hitbox, group: Group, speed: int):
        super().__init__(group)
        self._hp = hp
        self._attack = attack
        self._hitbox = hitbox
        self._speed = speed

        sprite_handler = SpriteHandler("./assets/knight.png")
        try:
            sprite = pygame.image.frombuffer(sprite_handler.sprite.tobytes(), sprite_handler.sprite.shape[1::-1], "RGB")
        except:
            print(f"{sprite_handler.sprite.shape=}")
            return
        
        self.image = sprite
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (200, 200)
        # self.image = Surface((50, 50))
        # self.image.fill((255, 0, 0))  # bright red square
        # self.rect = self.image.get_rect(center=(320, 240))

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self._speed
            if self.facing_right:  # only flip if currently facing right
                self.image = pygame.transform.flip(self.original_image, True, False)
                self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += self._speed
            if not self.facing_right:  # only flip if currently facing left
                self.image = pygame.transform.flip(self.original_image, False, False)
                self.facing_right = True
        if keys[pygame.K_UP]:
            self.rect.y -= self._speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self._speed


