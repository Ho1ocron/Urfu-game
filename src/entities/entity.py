from pygame.sprite import Sprite, Group


class BaseEntity:
    _hp: int
    _attack: int
    _hitbox: list
    _sprite: str

    def __init__(self, hp: int, attack: int, hitbox: list, sprite: Sprite) -> None:
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


class Knight(BaseEntity, Sprite):
    def __init__(self, hp, attack, hitbox, sprite):
        super().__init__(hp, attack, hitbox, sprite)
        
        self._sprite = sprite

