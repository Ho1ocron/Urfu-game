import pygame
from cv2.typing import MatLike
from random import randint

from utils import SpriteHandler, GameProperties
from entities.entity import BaseEntity
from entities.entity_master import EntityMaster


class Doppelganger(BaseEntity):
    """Generic enemy class."""
    _id: int

    def __init__(self, init_pos: tuple[int] = (0, 0), sprite_name: str = "Dragon", _id: str = "enemy1"):
        pygame.sprite.Sprite.__init__(self)
        
        self.sprite_handler = SpriteHandler(char_sprite=sprite_name)
        self.game_props = GameProperties(sprite_name)

        hp = self.game_props.char_properties["HP"]
        attack = self.game_props.char_properties["Attack"]
        speed = self.game_props.char_properties["Speed"]

        dummy_hitbox = pygame.Rect(0, 0, 128, 128)
        BaseEntity.__init__(self, hp=hp, attack=attack, speed=speed, hitbox=dummy_hitbox)

        init_pos = (randint(50, 570), randint(50, 700))

        self._animation = self.sprite_handler.animation
        self.direction = "down"
        self.frame_index = 0
        self.image = self._get_current_frame("Idle")
        self.rect = self.image.get_rect(center=init_pos)

        self._id = _id
        self.shoot_cooldown = randint(3000, 10000)
        self.last_shot_time = pygame.time.get_ticks() - randint(0, self.shoot_cooldown)

        self.teleport_cooldown = randint(7000, 10000)
        self.last_teleport_time = pygame.time.get_ticks() - randint(0, self.teleport_cooldown)

        EntityMaster.add_enemy(self)
        EntityMaster.add_enemy_pos({self._id: (self.rect.x, self.rect.y)})

        self.update_hitbox()

    def _get_current_frame(self, action: str = "Idle") -> pygame.Surface:
        frames = self._animation[action][self.direction]
        frame: MatLike = frames[int(self.frame_index) % len(frames)]
        return pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGBA")

    def update_hitbox(self) -> None:
        self.hitbox = pygame.Rect(
            self.rect.x + 42, self.rect.y + 42,
            self.rect.width - 84, self.rect.height - 84
        )

    def on_collision(self, other: BaseEntity) -> None:
        self.hp -= other.attack

    def shoot(self) -> None:
        """Foes' attack: they shoot bullets (Fbullet) at the player"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown + randint(-500, 1000):
            bullet = Fbullet(direction=self.direction)
            bullet.rect.center = self.rect.center
            self.shoot_cooldown = randint(3000, 4000)
            self.last_shot_time = current_time

    
    def update(self) -> None:
        """This func will be called each frame by EntityMaster group in the main.py"""
        self.shoot()
        dx = EntityMaster.player_pos[0] - (self.rect.x + 20)
        dy = EntityMaster.player_pos[1] - (self.rect.y + 20)

        # Decide which axis is more dominant (abs distance)
        if abs(dx) > abs(dy):
            if dx > 0:
                self.direction = "right"
            else:
                self.direction = "left"
        else:
            if dy > 0:
                self.direction = "down"
            else:
                self.direction = "up"

        current_time = pygame.time.get_ticks()
        if current_time - self.last_teleport_time >= self.teleport_cooldown + randint(-500, 5000):
            new_pos = (randint(50, 520), randint(50, 650))
            if EntityMaster.is_position_free(new_pos) and new_pos != EntityMaster.player_pos:
                self.rect.x, self.rect.y = new_pos
                EntityMaster.add_enemy_pos({self._id: (self.rect.x, self.rect.y)})
                self.teleport_cooldown = randint(5000, 10000)
                self.last_teleport_time = current_time
            else:
                self.teleport_cooldown = randint(5000, 10000)

        # Reset frame index when looping animation
        if self.frame_index >= len(self._animation["Idle"][self.direction]):
            self.frame_index = 0

        # Update image and hitbox
        self.frame_index += 0.2
        self.image = self._get_current_frame(action="Idle")
        if self.hp <= 0:
            EntityMaster.remove_enemy_pos(self._id)
            self.kill()


class Fbullet(BaseEntity):
    """Fbullet is a bullet for foes that they can strike player with."""
    _hp = 1
    _attack: int
    _speed: int = 15
    SIZE = (7, 7)  # small square bullet
    direction: str

    def __init__(self, direction: str):
        game_props = GameProperties("Dragon")
        pygame.sprite.Sprite.__init__(self)
        
        self._attack = game_props.char_properties["Attack"]
        dummy_hitbox = pygame.Rect(0, 0, *self.SIZE)

        BaseEntity.__init__(self, hp=self._hp, attack=self._attack, speed=self._speed, hitbox=dummy_hitbox)

        # Make the bullet appear as a small pink-red square
        self.image = pygame.Surface(self.SIZE)
        self.image.fill((255, 100, 120))  # light pink-red color

        # Define its position and collision rectangle
        self.rect = self.image.get_rect()
        self.rect.topleft = (30, 30)
        EntityMaster.add_fbullet(self)
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

        if (self.rect.x < 0 or self.rect.x > 800 or 
            self.rect.y < 0 or self.rect.y > 600):
            self.kill()

        if self._hp <= 0:
            self.kill()

    def on_collision(self, other: BaseEntity) -> None:
        self.hp -= other.attack
        other.hp -= self._attack
        self.kill()