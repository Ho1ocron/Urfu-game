class BaseEntity:
    _hp: int
    _attack: int
    _hitbox: list

    def __init__(self, hp: int, attack: int, hitbox: list) -> None:
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


class Knight(BaseEntity):
    def __init__(self, hp, attack, hitbox):
        super().__init__(hp, attack, hitbox)

