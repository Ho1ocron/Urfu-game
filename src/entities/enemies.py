import pygame
from cv2.typing import MatLike
from random import randint

from utils import SpriteHandler, GameProperties
from entities.entity import BaseEntity
from entities.entity_master import EntityMaster


class Dragon(BaseEntity):
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

        self.teleport_cooldown = randint(7000, 10000)
        self.last_shot_time = 0

        EntityMaster.add_enemy(self)
        EntityMaster.add_enemy_pos({self._id: (self.rect.x, self.rect.y)})

        self.update_hitbox()

    def _get_current_frame(self, action: str = "Idle") -> pygame.Surface:
        frames = self._animation[action][self.direction]
        frame: MatLike = frames[int(self.frame_index) % len(frames)]
        return pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGBA")

    def update_hitbox(self):
        self.hitbox = pygame.Rect(
            self.rect.x + 42, self.rect.y + 42,
            self.rect.width - 84, self.rect.height - 84
        )

    def on_collision(self, other: BaseEntity) -> None:
        self.hp -= other.attack
    
    def update(self):
        if self.rect.x + 20 < EntityMaster.player_pos[0]:
            self.direction = "right"
        else:
            self.direction = "left"
        if self.rect.y + 20 > EntityMaster.player_pos[1]:
            self.direction = "up"
        else:
            self.direction = "down"

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.teleport_cooldown:
            new_pos = (randint(50, 520), randint(50, 650))
            if new_pos not in EntityMaster.enemy_poses.values() and new_pos != EntityMaster.player_pos:
                self.rect.x, self.rect.y = new_pos
                EntityMaster.add_enemy_pos({self._id: (self.rect.x, self.rect.y)})
                self.teleport_cooldown = randint(5000, 10000)
                self.last_shot_time = current_time
        # Reset frame index when looping animation
        if self.frame_index >= len(self._animation["Idle"][self.direction]):
            self.frame_index = 0

        # Update image and hitbox
        self.frame_index += 0.2
        self.image = self._get_current_frame(action="Idle")
        if self.hp <= 0:
            EntityMaster.remove_enemy_pos(self._id)
            self.kill()