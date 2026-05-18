import pygame
import math
from cv2.typing import MatLike

from utils import SpriteHandler, GameProperties
from entities.entity import BaseEntity
from entities.entity_master import EntityMaster


class Knight(BaseEntity):
    """Knight is a controllable player character."""

    facing_right: bool = True
    max_hp: int

    def __init__(self, init_pos: tuple[int]) -> None:
        # Initialize sprite
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize handler and properties
        self.sprite_handler = SpriteHandler(char_sprite="Knight")
        self.game_props = GameProperties("Knight")

        # Load game properties
        self.max_hp = self.game_props.char_properties["HP"]
        attack = self.game_props.char_properties["Attack"]
        speed = self.game_props.char_properties["Speed"]
        self._controls = self.game_props.controls
        self._animation = self.sprite_handler.animation

        # Temporary dummy hitbox for parent init
        dummy_hitbox = pygame.Rect(0, 0, 32, 32)

        # Initialize BaseEntity
        BaseEntity.__init__(self, hp=self.max_hp, attack=attack, speed=speed, hitbox=dummy_hitbox)

        # Animation setup
        self.direction = "down"
        self.frame_index = 0
        self.animation_speed = 0.4

        self.image = self._get_current_frame()
        self.rect = self.image.get_rect(center=init_pos)

        # Hitbox setup
        self.hitbox_margin = 42
        self.update_hitbox()

        self.shoot_cooldown = 200  # milliseconds between shots
        self.last_shot_time = 0

        self.heal_cooldown = 5000
        self.last_time_healed = 0

        EntityMaster.add_player(self)
        EntityMaster.player_pos = (self.rect.x, self.rect.y)

    def _get_current_frame(self, action: str = "Walk") -> pygame.Surface:
        """Return current pygame Surface for the knight’s facing direction."""
        frames = self._animation[action][self.direction]
        frame: MatLike = frames[int(self.frame_index) % len(frames)]
        return pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGBA")

    def update_hitbox(self) -> None:
        """Recalculate hitbox position and size."""
        self._hitbox = pygame.Rect(
            self.rect.x + self.hitbox_margin,
            self.rect.y + self.hitbox_margin,
            self.rect.width - self.hitbox_margin * 2,
            self.rect.height - self.hitbox_margin * 2
        )

    def shoot(self) -> None:
        """Func for handling player's shooting."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            bullet = Bullet(direction=self.direction)
            bullet.rect.center = self.rect.center
            self.last_shot_time = current_time

    def dash(self) -> None:
        """Dashes the player forward"""
        if self.direction == "up":
            self.rect.y -= 20
        if self.direction == "down":
            self.rect.y += 20

        if self.direction == "right":
            self.rect.x += 20
        if self.direction == "left":
            self.rect.x -= 20

    def heal(self) -> None:
        """Player heals itself"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time_healed >= self.heal_cooldown:
            self.hp = min(self.hp + 20, self.max_hp) # So it won't be greater than max hp
            self.last_time_healed = current_time

    def handle_input(self, keys) -> None:
        """Handle keyboard input for movement and animation."""
        if self.hp <= 0:
            self.kill()

        moving = False
        dx, dy = 0, 0

        if keys[self._controls["Walk_left"]]:
            dx -= 1
            self.direction = "left"
            moving = True
        if keys[self._controls["Walk_right"]]:
            dx += 1
            self.direction = "right"
            moving = True
        if keys[self._controls["Walk_up"]]:
            dy -= 1
            self.direction = "up"
            moving = True
        if keys[self._controls["Walk_down"]]:
            dy += 1
            self.direction = "down"
            moving = True
        if keys[self._controls["Shoot"]]:
            self.shoot()
        if keys[self._controls["Dash"]] and moving:
            self.dash()
        if keys[self._controls["Heal"]]:
            self.heal()

        # Normalize diagonal movement
        if dx != 0 or dy != 0:
            magnitude = math.sqrt(dx ** 2 + dy ** 2)
            dx /= magnitude
            dy /= magnitude

            self.rect.x += dx * self._speed
            self.rect.y += dy * self._speed

        current_action = "Walk" if moving else "Idle"
        self.frame_index += self.animation_speed if moving else 0.2

        # Reset frame index when looping animation
        if self.frame_index >= len(self._animation[current_action][self.direction]):
            self.frame_index = 0

        # Update image and hitbox
        self.image = self._get_current_frame(action=current_action)
        EntityMaster.player_pos = (self.rect.x, self.rect.y)
        self.update_hitbox()

    def on_collision(self, other: BaseEntity) -> None:
        self.hp -= other.attack


class Bullet(BaseEntity):
    _hp = 1
    _attack: int
    _speed: int = 25
    SIZE = (5, 5)  # small square bullet
    direction: str

    def __init__(self, direction: str):
        game_props = GameProperties("Knight")
        pygame.sprite.Sprite.__init__(self)
        
        self._attack = game_props.char_properties["Attack"]
        dummy_hitbox = pygame.Rect(0, 0, *self.SIZE)

        BaseEntity.__init__(self, hp=self._hp, attack=self._attack, speed=self._speed, hitbox=dummy_hitbox)

        # Make the bullet appear as a small pink-red square
        self.image = pygame.Surface(self.SIZE)
        self.image.fill((255, 100, 120))  # light pink-red color

        # Define its position and collision rectangle
        self.rect = self.image.get_rect()
        self.rect.topleft = (40, 40)
        EntityMaster.add_bullet(self)
        self.direction = direction

    def update(self):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

        if (self.rect.x < 0 or self.rect.x > 1000 or 
            self.rect.y < 0 or self.rect.y > 1000):
            self.kill()

        if self._hp <= 0:
            self.kill()

    def on_collision(self, other: BaseEntity) -> None:
        self.hp -= other.attack
        other.hp -= self._attack
        self.kill()