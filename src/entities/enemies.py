import pygame
import math
from cv2.typing import MatLike

from entities.player import Knight
from utils import SpriteHandler, GameProperties
from entities.entity import BaseEntity
from entities.group_manager import GroupManager


class EnemyKnight(BaseEntity):
    """Generic enemy class."""

    def __init__(self, init_pos: tuple[int], sprite_name: str = "Knight"):
        pygame.sprite.Sprite.__init__(self)
        GroupManager.add_enemy(self)
        self.sprite_handler = SpriteHandler(char_sprite=sprite_name)
        self.game_props = GameProperties(sprite_name)

        hp = self.game_props.char_properties["HP"]
        attack = self.game_props.char_properties["Attack"]
        speed = self.game_props.char_properties["Speed"]

        dummy_hitbox = pygame.Rect(0, 0, 128, 128)
        BaseEntity.__init__(self, hp=hp, attack=attack, speed=speed, hitbox=dummy_hitbox)

        self._animation = self.sprite_handler.animation
        self.direction = "down"
        self.frame_index = 0
        self.image = self._get_current_frame("Idle")
        self.rect = self.image.get_rect(center=init_pos)
        self.update_hitbox()

    def _get_current_frame(self, action: str = "Idle") -> pygame.Surface:
        frames = self._animation[action][self.direction]
        frame = frames[int(self.frame_index) % len(frames)]
        return pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGBA")

    def update_hitbox(self):
        self.hitbox = pygame.Rect(
            self.rect.x + 42, self.rect.y + 42,
            self.rect.width - 84, self.rect.height - 84
        )

    def on_collision(self, other: BaseEntity) -> None:
        if isinstance(other, Knight):
            print("EnemyKnight collided with player — could counterattack here!")