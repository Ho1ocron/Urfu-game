import sys
import os
import pytest
import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from entities.entity import BaseEntity
from entities.entity_master import EntityMaster


def _make_sprite(x: int, y: int, w: int, h: int, color=(255, 0, 0)) -> pygame.sprite.Sprite:
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.Surface((w, h))
    sprite.image.fill(color)
    sprite.rect = sprite.image.get_rect(topleft=(x, y))
    sprite.mask = pygame.mask.from_surface(sprite.image)
    return sprite


def _make_entity(x: int, y: int, w: int, h: int, hp: int = 100, attack: int = 10) -> BaseEntity:
    entity = BaseEntity.__new__(BaseEntity)
    pygame.sprite.Sprite.__init__(entity)
    entity.image = pygame.Surface((w, h))
    entity.image.fill((200, 200, 200))
    entity.rect = entity.image.get_rect(topleft=(x, y))
    entity.mask = pygame.mask.from_surface(entity.image)
    entity._hp = hp
    entity._attack = attack
    entity._speed = 5
    entity._hitbox = pygame.Rect(x, y, w, h)
    return entity


@pytest.fixture(autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture(autouse=True)
def clear_entity_master():
    EntityMaster.clear_all()
    yield
    EntityMaster.clear_all()


class TestIsPositionFree:

    def test_free_when_no_enemies(self):
        EntityMaster.player_pos = (0, 0)
        assert EntityMaster.is_position_free((500, 500)) is True

    def test_occupied_by_enemy(self):
        EntityMaster.player_pos = (0, 0)
        EntityMaster.enemy_poses["e1"] = (200, 200)
        assert EntityMaster.is_position_free((210, 210)) is False

    def test_free_far_from_enemy(self):
        EntityMaster.player_pos = (0, 0)
        EntityMaster.enemy_poses["e1"] = (200, 200)
        assert EntityMaster.is_position_free((400, 400)) is True

    def test_occupied_by_player(self):
        EntityMaster.player_pos = (300, 300)
        assert EntityMaster.is_position_free((310, 310)) is False

    def test_free_far_from_player(self):
        EntityMaster.player_pos = (0, 0)
        assert EntityMaster.is_position_free((500, 500)) is True

    def test_boundary_exactly_at_radius(self):
        EntityMaster.player_pos = (0, 0)
        r = EntityMaster.enemy_collision_radius  # 100
        assert EntityMaster.is_position_free((r, 0)) is True

    def test_multiple_enemies_all_far(self):
        EntityMaster.player_pos = (0, 0)
        EntityMaster.enemy_poses["e1"] = (500, 500)
        EntityMaster.enemy_poses["e2"] = (600, 600)
        assert EntityMaster.is_position_free((300, 300)) is True

    def test_multiple_enemies_one_close(self):
        EntityMaster.player_pos = (0, 0)
        EntityMaster.enemy_poses["e1"] = (500, 500)
        EntityMaster.enemy_poses["e2"] = (305, 305)
        assert EntityMaster.is_position_free((300, 300)) is False


class TestBaseEntityOnCollision:

    def test_base_on_collision_does_not_change_hp(self):
        target = _make_entity(0, 0, 32, 32, hp=100)
        attacker = _make_entity(0, 0, 32, 32, attack=25)
        target.on_collision(attacker)
        assert target.hp == 100

    def test_zero_attack_does_not_change_hp(self):
        target = _make_entity(0, 0, 32, 32, hp=80)
        attacker = _make_entity(0, 0, 32, 32, attack=0)
        target.on_collision(attacker)
        assert target.hp == 80

    def test_subclass_on_collision_reduces_hp(self):
        target = _make_entity(0, 0, 32, 32, hp=100)
        attacker = _make_entity(0, 0, 32, 32, attack=25)
        target.on_collision = lambda other: setattr(target, '_hp', target._hp - other._attack)
        target.on_collision(attacker)
        assert target.hp == 75

    def test_subclass_on_collision_hp_can_go_negative(self):
        target = _make_entity(0, 0, 32, 32, hp=10)
        attacker = _make_entity(0, 0, 32, 32, attack=50)
        target.on_collision = lambda other: setattr(target, '_hp', target._hp - other._attack)
        target.on_collision(attacker)
        assert target.hp == -40


class TestBulletVsEnemy:

    def _make_bullet(self, x, y, attack=10):
        bullet = _make_entity(x, y, 5, 5, hp=1, attack=attack)

        def on_collision(other):
            bullet._hp -= other._attack
            other._hp -= bullet._attack
            bullet.kill()

        bullet.on_collision = on_collision
        EntityMaster.add_bullet(bullet)
        return bullet

    def _make_enemy(self, x, y, hp=100, attack=10):
        enemy = _make_entity(x, y, 64, 64, hp=hp, attack=attack)
        EntityMaster.add_enemy(enemy)
        return enemy

    def test_bullet_hits_enemy_reduces_hp(self):
        bullet = self._make_bullet(10, 10, attack=15)
        enemy = self._make_enemy(10, 10, hp=100)

        EntityMaster.check_collisions()

        assert enemy._hp == 85
        assert not bullet.alive()

    def test_bullet_misses_enemy_no_damage(self):
        bullet = self._make_bullet(0, 0, attack=15)
        enemy = self._make_enemy(500, 500, hp=100)

        EntityMaster.check_collisions()

        assert enemy._hp == 100
        assert bullet.alive()

    def test_multiple_bullets_hit_enemy(self):
        b1 = self._make_bullet(10, 10, attack=10)
        b2 = self._make_bullet(10, 10, attack=20)
        enemy = self._make_enemy(10, 10, hp=100)

        EntityMaster.check_collisions()

        assert enemy._hp == 70
        assert not b1.alive()
        assert not b2.alive()

    def test_bullet_hits_correct_enemy(self):
        bullet = self._make_bullet(10, 10, attack=10)
        enemy_hit = self._make_enemy(10, 10, hp=100)
        enemy_miss = self._make_enemy(500, 500, hp=100)

        EntityMaster.check_collisions()

        assert enemy_hit._hp == 90
        assert enemy_miss._hp == 100


class TestFbulletVsPlayer:

    def _make_fbullet(self, x, y, attack=10):
        fbullet = _make_entity(x, y, 7, 7, hp=1, attack=attack)

        def on_collision(other):
            fbullet._hp -= other._attack
            other._hp -= fbullet._attack
            fbullet.kill()

        fbullet.on_collision = on_collision
        EntityMaster.add_fbullet(fbullet)
        return fbullet

    def _make_player(self, x, y, hp=100, attack=0):
        player = _make_entity(x, y, 64, 64, hp=hp, attack=attack)
        EntityMaster.add_player(player)
        EntityMaster.player_pos = (x, y)
        return player

    def test_fbullet_hits_player_reduces_hp(self):
        fbullet = self._make_fbullet(10, 10, attack=20)
        player = self._make_player(10, 10, hp=100)

        EntityMaster.check_collisions()

        assert player._hp == 80
        assert not fbullet.alive()

    def test_fbullet_misses_player_no_damage(self):
        fbullet = self._make_fbullet(0, 0, attack=20)
        player = self._make_player(500, 500, hp=100)

        EntityMaster.check_collisions()

        assert player._hp == 100
        assert fbullet.alive()

    def test_multiple_fbullets_hit_player(self):
        fb1 = self._make_fbullet(10, 10, attack=10)
        fb2 = self._make_fbullet(10, 10, attack=15)
        player = self._make_player(10, 10, hp=100)

        EntityMaster.check_collisions()

        assert player._hp == 75
        assert not fb1.alive()
        assert not fb2.alive()

    def test_fbullet_does_not_hit_enemy(self):
        fbullet = self._make_fbullet(10, 10, attack=10)
        enemy = _make_entity(10, 10, 64, 64, hp=100)
        EntityMaster.add_enemy(enemy)
        EntityMaster.check_collisions()

        assert enemy._hp == 100
        assert fbullet.alive()


class TestEnemyPosManagement:

    def test_add_and_remove_enemy_pos(self):
        EntityMaster.add_enemy_pos({"e1": (100, 200)})
        assert "e1" in EntityMaster.enemy_poses
        EntityMaster.remove_enemy_pos("e1")
        assert "e1" not in EntityMaster.enemy_poses

    def test_update_enemy_pos(self):
        EntityMaster.add_enemy_pos({"e1": (100, 100)})
        EntityMaster.add_enemy_pos({"e1": (200, 200)})
        assert EntityMaster.enemy_poses["e1"] == (200, 200)

    def test_clear_all_empties_groups(self):
        EntityMaster.add_enemy_pos({"e1": (10, 10)})
        s = _make_sprite(0, 0, 10, 10)
        EntityMaster.add_enemy(s)
        EntityMaster.clear_all()

        assert len(EntityMaster.enemy_group) == 0
        assert len(EntityMaster.all_sprites) == 0
        assert len(EntityMaster.enemy_poses) == 0
