import math
import pygame
import cv2
from cv2.typing import MatLike
from random import randint

from utils import SpriteHandler, GameProperties
from entities.entity import BaseEntity
from entities.entity_master import EntityMaster


class Doppelganger(BaseEntity):
    """Generic enemy class."""
    _id: int

    def __init__(self, init_pos: tuple[int] = (0, 0), sprite_name: str = "Knight", _id: str = "enemy1"):
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


class Dragon(BaseEntity):
    """The main boss of the game that player should kill."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        sprite_name = "Dragon"
        self.sprite_handler = SpriteHandler(char_sprite=sprite_name)
        self.game_props = GameProperties(sprite_name)

        # Load stats from GameProperties
        hp = self.game_props.char_properties["HP"]
        attack = self.game_props.char_properties["Attack"]
        speed = self.game_props.char_properties.get("Speed", 0)  # Default to 0 if not defined

        # Place at center-top of screen
        screen_w, screen_h = 620, 750
        center_x = screen_w // 2
        center_y = 100  # Slightly below the top edge
        dummy_hitbox = pygame.Rect(0, 0, 128, 128)
        BaseEntity.__init__(self, hp=hp, attack=attack, speed=speed, hitbox=dummy_hitbox)

        # Animation setup
        self._animation = self.sprite_handler.animation
        self.direction = "down"
        self.frame_index = 0
        self.image = self._get_current_frame("Idle")
        self.rect = self.image.get_rect(center=(center_x, center_y))

        # Shooting setup
        self.shoot_cooldown = randint(3000, 7000)  # 3–7 seconds between volleys
        self.last_shot_time = pygame.time.get_ticks() - randint(0, self.shoot_cooldown)

        # Register in EntityMaster
        EntityMaster.add_enemy(self)
        EntityMaster.add_enemy_pos({"Dragon": (self.rect.x, self.rect.y)})

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

    def shoot(self) -> None:
        """Shoots a burst of bullets in multiple directions."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            directions = ["down", "left", "right"]
            for direction in directions:
                bullet = Fbullet(direction=direction)
                bullet.rect.center = self.rect.center

            # Randomize next cooldown between 3–7 seconds
            self.shoot_cooldown = randint(1000, 5000)
            self.last_shot_time = current_time

    def update(self) -> None:
        """Dragon only shoots and animates."""
        self.shoot()

        # Update animation
        self.frame_index += 0.1
        if self.frame_index >= len(self._animation["Idle"][self.direction]):
            self.frame_index = 0
        self.image = self._get_current_frame("Idle")

        if self.hp <= 0:
            EntityMaster.remove_enemy_pos("Dragon")
            self.kill()


class Rat(BaseEntity):
    """Simple chasing enemy that bites the player when close."""
    BITE_RANGE = 15
    BITE_COOLDOWN = 1000  # ms between bites
    HURT_DURATION = 200   # ms to show hurt (white) frame
    FRAME_W = 32
    FRAME_H = 32
    FRAME_COUNT = 6
    SCALE = 2.5

    def __init__(self, _id: str = "rat0"):
        pygame.sprite.Sprite.__init__(self)

        hp = 100
        attack = 10
        speed = 3

        dummy_hitbox = pygame.Rect(0, 0, self.FRAME_W * self.SCALE, self.FRAME_H * self.SCALE)
        BaseEntity.__init__(self, hp=hp, attack=attack, speed=speed, hitbox=dummy_hitbox)

        self._frames_run = self._load_sheet("./assets/Sprites/Rat/NoneOutlinedRat/rat-run.png")
        self._frames_idle = self._load_sheet("./assets/Sprites/Rat/NoneOutlinedRat/rat-idle.png")
        self._frame_hurt = self._load_single("./assets/Sprites/Rat/NoneOutlinedRat/rat-hurt.png")

        self.frame_index: float = 0.0
        self._moving = False
        self._flip = False
        self.image = self._frames_idle[0]

        init_pos = (randint(50, 570), randint(50, 700))
        self.rect = self.image.get_rect(center=init_pos)

        self._id = _id
        self._last_hp = hp
        self._hurt_timer = -self.HURT_DURATION
        self._bite_timer = pygame.time.get_ticks()

        EntityMaster.add_enemy(self)
        EntityMaster.add_enemy_pos({self._id: (self.rect.x, self.rect.y)})
        self.update_hitbox()

    def _load_sheet(self, path: str) -> list[pygame.Surface]:
        sheet = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        frames = []
        for i in range(self.FRAME_COUNT):
            frame = sheet[0:self.FRAME_H, i * self.FRAME_W:(i + 1) * self.FRAME_W]
            frame = cv2.resize(frame, (int(self.FRAME_W * self.SCALE), int(self.FRAME_H * self.SCALE)), interpolation=cv2.INTER_NEAREST)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA)
            surf = pygame.image.frombuffer(frame.tobytes(), (int(self.FRAME_W * self.SCALE), int(self.FRAME_H * self.SCALE)), "RGBA")
            frames.append(surf)
        return frames

    def _load_single(self, path: str) -> pygame.Surface:
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, (int(self.FRAME_W * self.SCALE), int(self.FRAME_H * self.SCALE)), interpolation=cv2.INTER_NEAREST)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        return pygame.image.frombuffer(img.tobytes(), (int(self.FRAME_W * self.SCALE), int(self.FRAME_H * self.SCALE)), "RGBA")

    def update_hitbox(self) -> None:
        self.hitbox = pygame.Rect(
            self.rect.x + 8, self.rect.y + 8,
            self.rect.width - 16, self.rect.height - 16
        )

    def on_collision(self, other: BaseEntity) -> None:
        self.hp -= other.attack

    def update(self) -> None:
        current_time = pygame.time.get_ticks()

        # Detect damage taken this frame
        if self.hp < self._last_hp:
            self._hurt_timer = current_time
        self._last_hp = self.hp

        # Chase or bite
        px, py = EntityMaster.player_pos
        dx = px - self.rect.centerx
        dy = py - self.rect.centery
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > self.BITE_RANGE:
            self._moving = True
            if dist > 0:
                self.rect.x += int(self.speed * dx / dist)
                self.rect.y += int(self.speed * dy / dist)
            self._flip = dx < 0
        else:
            self._moving = False
            if current_time - self._bite_timer >= self.BITE_COOLDOWN:
                for player in EntityMaster.player_group:
                    player.hp -= self.attack
                self._bite_timer = current_time

        # Separate from other rats so they don't stack
        separation = self.FRAME_W * self.SCALE
        for other in EntityMaster.enemy_group:
            if other is self or not isinstance(other, Rat):
                continue
            odx = self.rect.centerx - other.rect.centerx
            ody = self.rect.centery - other.rect.centery
            odist = math.sqrt(odx * odx + ody * ody)
            if 0 < odist < separation:
                push = (separation - odist) / odist
                self.rect.x += int(odx * push * 0.5)
                self.rect.y += int(ody * push * 0.5)

        EntityMaster.add_enemy_pos({self._id: (self.rect.x, self.rect.y)})
        self.update_hitbox()

        # Animate
        hurting = (current_time - self._hurt_timer) < self.HURT_DURATION
        if hurting:
            self.image = self._frame_hurt
        else:
            frames = self._frames_run if self._moving else self._frames_idle
            self.frame_index = (self.frame_index + 0.2) % len(frames)
            frame = frames[int(self.frame_index)]
            self.image = pygame.transform.flip(frame, self._flip, False)

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

        if (self.rect.x < 0 or self.rect.x > 1000 or 
            self.rect.y < 0 or self.rect.y > 1000):
            self.kill()

        if self._hp <= 0:
            self.kill()

    def on_collision(self, other: BaseEntity) -> None:
        self.hp -= other.attack
        other.hp -= self._attack
        self.kill()