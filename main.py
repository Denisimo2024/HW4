
from abc import ABC, abstractmethod

class Weapon(ABC):
    @abstractmethod
    def attack(self):
        pass

class Sword(Weapon):
    def attack(self):
        return "удар коротким мечом"

class Axe(Weapon):
    def attack(self):
        return "удар быстрым топором"

class Bow(Weapon):
    def attack(self):
        return "выстрел из среднего лука"

class MagicWand(Weapon):
    def attack(self):
        return "магическая атака абра катабра"



class Fighter:
    def __init__(self, name):
        self.name = name
        self.weapon = None  # Изначально оружие не выбрано

    def change_weapon(self, weapon: Weapon):
        self.weapon = weapon
        print(f"{self.name} выбирает {self.weapon.attack()}.")

    def attack(self):
        if not self.weapon:
            print(f"{self.name} не может атаковать без оружия!")
        else:
            print(f"{self.name} наносит {self.weapon.attack()}.")



class Monster:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} побежден!")
        else:
            print(f"{self.name} имеет {self.health} здоровья.")



def fight(fighter: Fighter, monster: Monster, weapon: Weapon):
    fighter.change_weapon(weapon)
    print(f"{fighter.name} атакует {monster.name}.")
    fighter.attack()
    monster.take_damage(10)


# Создаем бойца и монстра
fighter = Fighter(name="Герой")
monster = Monster(name="Дракон", health=40)

# Создаем оружие
sword = Sword()
bow = Bow()
magic_wand = MagicWand()
axe = Axe()

# Демонстрируем бой с использованием разных видов оружия
fight(fighter, monster, sword)
fight(fighter, monster, bow)
fight(fighter, monster, magic_wand)
fight(fighter, monster, axe)