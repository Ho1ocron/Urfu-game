import pygame


class EntityMaster:
    """Centralized manager for all sprite groups."""
    player_group = pygame.sprite.Group()
    player_pos: tuple[int]

    enemy_group = pygame.sprite.Group()
    enemy_poses: dict[str, tuple[int]] = {}
    enemy_collision_radius: int = 100

    bullet_group = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group() 

    @classmethod
    def add_player(cls, player: pygame.sprite.Sprite) -> None:
        cls.player_group.add(player)
        cls.all_sprites.add(player)

    @classmethod
    def add_enemy(cls, enemy: pygame.sprite.Sprite) -> None:
        cls.enemy_group.add(enemy)
        cls.all_sprites.add(enemy)

    @classmethod
    def add_enemy_pos(cls, pos: dict[str, tuple[int]]) -> None:
        cls.enemy_poses.update(pos)

    @classmethod
    def remove_enemy_pos(cls, _id: str):
        cls.enemy_poses.pop(_id)

    @classmethod
    def is_position_free(cls, new_pos: tuple[int, int]) -> bool:
        for pos in cls.enemy_poses.values():
            dx = pos[0] - new_pos[0]
            dy = pos[1] - new_pos[1]
            distance_sq = dx * dx + dy * dy
            if distance_sq < cls.enemy_collision_radius ** 2:
                return False
            
        dx = cls.player_pos[0] - new_pos[0]
        dy = cls.player_pos[1] - new_pos[1]
        distance_sq = dx * dx + dy * dy 
        
        if distance_sq < cls.enemy_collision_radius ** 2:
                return False
        return True

    @classmethod
    def add_bullet(cls, bullet: pygame.sprite.Sprite) -> None:
        cls.bullet_group.add(bullet)
        cls.all_sprites.add(bullet)

    @classmethod
    def clear_all(cls) -> None:
        """Clear all sprite groups."""
        cls.player_group.empty()
        cls.enemy_group.empty()
        cls.all_sprites.empty()

    @classmethod
    def check_collisions(cls) -> None:
        """Detect and handle collisions between player and enemies."""
        for bullet in cls.bullet_group:
            collided_enemies = pygame.sprite.spritecollide(
                bullet, cls.enemy_group, False, pygame.sprite.collide_mask
            )
            for enemy in collided_enemies:
                bullet.on_collision(enemy)
