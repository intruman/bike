import bike


@bike.model()
class Character:
    name: str
    health: float = 1.0

    @bike.validator('name')
    def name_validator(cls, val):
        return str(val).title()

    @bike.validator('health')
    def health_validator(cls, val):
        if val < 0:
            return 0.0
        elif val > 1:
            return 1.0
        return val


c1 = Character(name='ninki walker', health=2.0)
print(c1.name)
print(c1.health)