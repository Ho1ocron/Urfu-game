import pygame
from cv2.typing import MatLike

from utils import SpriteHandler, GameProperties
from entities.entity import BaseEntity
from entities.entity_master import EntityMaster


class Dragon(BaseEntity):
    """Generic enemy class."""
    _id: int

    def __init__(self, init_pos: tuple[int], sprite_name: str = "Dragon", _id: str = "enemy1"):
        pygame.sprite.Sprite.__init__(self)
        
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

        self._id = _id

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
        # Reset frame index when looping animation
        if self.frame_index >= len(self._animation["Idle"][self.direction]):
            self.frame_index = 0

        # Update image and hitbox
        self.frame_index += 0.2
        self.image = self._get_current_frame(action="Idle")
        if self.hp <= 0:
            EntityMaster.remove_enemy_pos(self._id)
            self.kill()