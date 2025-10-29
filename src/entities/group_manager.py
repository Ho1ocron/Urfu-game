import pygame


class GroupManager:
    """Centralized manager for all sprite groups."""
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()  # optional convenience group

    @classmethod
    def add_player(cls, player: pygame.sprite.Sprite) -> None:
        cls.player_group.add(player)
        cls.all_sprites.add(player)

    @classmethod
    def add_enemy(cls, enemy: pygame.sprite.Sprite) -> None:
        cls.enemy_group.add(enemy)
        cls.all_sprites.add(enemy)

    @classmethod
    def clear_all(cls) -> None:
        """Clear all sprite groups."""
        cls.player_group.empty()
        cls.enemy_group.empty()
        cls.all_sprites.empty()

    @classmethod
    def check_collisions(cls):
        """Detect and handle collisions between player and enemies."""
        for player in cls.player_group:
            # Detect collisions between this player and all enemies
            collided_enemies = pygame.sprite.spritecollide(
                player, cls.enemy_group, False, pygame.sprite.collide_mask
            )

            for enemy in collided_enemies:
                if player != enemy:
                    player.on_collision(enemy)
                    enemy.on_collision(player)