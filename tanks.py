import pygame
from enum import Enum

import pygame.sprite

from pygame.sprite import collide_mask
from pygame.sprite import spritecollideany

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TILE_SIZE = 36
TANK_SIZE = TILE_SIZE * 2

visible_world_width = 15
visible_world_height = 15

SCREEN_W = TILE_SIZE * visible_world_width
SCREEN_H = TILE_SIZE * visible_world_height
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

grass = pygame.image.load('tiles/grass.png')
stone = pygame.image.load('tiles/stone.png')
water = pygame.image.load('tiles/water.png')

grass = pygame.transform.scale(grass, (TILE_SIZE, TILE_SIZE))
stone = pygame.transform.scale(stone, (TILE_SIZE, TILE_SIZE))
water = pygame.transform.scale(water, (TILE_SIZE, TILE_SIZE))

default_tile = grass


class Direction(Enum):
    Up = 90
    Down = 270
    Left = 180
    Right = 0


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, i, j):
        super().__init__()
        self.image = image
        self.i = i
        self.j = j

        self.rect = image.get_rect()
        self.x = j * TILE_SIZE
        self.y = i * TILE_SIZE

        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        global x_shift, y_shift
        self.x = self.j * TILE_SIZE - x_shift
        self.y = self.i * TILE_SIZE - y_shift
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)


# Класс Tank унаследован от класса Sprite из модуля sprite библиотеки pygame
# То есть часть возможностей, которые имеет класс Sprite,
# становятся доступными для класса Tank
# Это позволит нам более качественно отслеживать столкновения
class Tank(pygame.sprite.Sprite):
    def __init__(self, tile, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Загрузили тайл как картинку
        self.tile = pygame.image.load(f'tiles/{tile}')
        # Установили размеры тайла
        self.w = TANK_SIZE
        self.h = TANK_SIZE
        self.size = (self.w, self.h)
        
        # Масштабировали наш тайл до нужного размера
        # И сохранили его оригинальный вариант
        self.original_image = pygame.transform.scale(
            self.tile, self.size
        )
        # Создали точно также копию тайла, 
        # которая будет меняться в процессе игры
        self.image = pygame.transform.scale(
            self.tile, self.size
        )
        # Для тайла сделали битовую маску
        # Т.е, прозрачные пиксели - это 0, непрозрачные - 1
        # 
        self.mask = pygame.mask.from_surface(self.image)
        
        # Для тайла получили Rect, который его "обрамляет"
        # Rect - прямоугольник, имеющий высоту и ширину тайла,
        # А также свои координаты, которые мы можем менять
        self.rect = self.image.get_rect()
        self.x = TILE_SIZE * x + TILE_SIZE // 2
        self.y = TILE_SIZE * y + TILE_SIZE // 2

        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)
        
        # Проинициализировали поле direction значением Right перечисления Direction
        self.direction = Direction.Right
        # Установили скорость, равную 1/6 размера тайла 
        # (чтобы не зависеть от масштаба экран)
        self.speed = TILE_SIZE / 6
        # Флаг on_move - есть True, когда танк едет, 
        # и False - когда стоит
        self.on_move = False
    
    def change_direction(self, direction: Direction):
        def try_change_direction(direction):
            self.direction = direction
            # Поворачиваем наш тайл (без изменения оригинала)
            self.image = pygame.transform.rotate(
                self.original_image, 
                self.direction.value
            )
            # Обновляем прямоугольник (он у нас повернулся)
            rect = self.image.get_rect()
            rect.centerx = self.rect.centerx
            rect.centery = self.rect.centery
            self.rect = rect
            # Обновляем маску (т.к. поменялось положение пикселей)
            self.mask = pygame.mask.from_surface(self.image)
        
        # Меняем значение поля direction
        old_direction = self.direction

        try_change_direction(direction)
        
        if spritecollideany(self, walls, collide_mask):
            try_change_direction(old_direction)


class PlayerTank(Tank):
    def update(self):
        global x_shift, y_shift

        if not self.on_move:
            return

        old_x = self.x
        old_y = self.y
        old_x_shift = x_shift
        old_y_shift = y_shift
        
        if self.direction == Direction.Up:
            if self.y <= SCREEN_H / 2 and y_shift - self.speed >= 0:
                y_shift -= self.speed
            else:
                self.y -= self.speed
        
        if self.direction == Direction.Down:
            if self.y >= SCREEN_H / 2 and y_shift + self.speed <= WORLD_H - SCREEN_H:
                y_shift += self.speed
            else:
                self.y += self.speed
        
        if self.direction == Direction.Left:
            if self.x <= SCREEN_W / 2 and x_shift - self.speed >= 0:
                x_shift -= self.speed
            else:
                self.x -= self.speed
        
        if self.direction == Direction.Right:
            if self.x >= SCREEN_W / 2 and x_shift + self.speed <= WORLD_W - SCREEN_W:
                x_shift += self.speed
            else:
                self.x += self.speed
        
        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)

        if spritecollideany(self, walls, collide_mask):
            self.x = old_x
            self.y = old_y
            x_shift = old_x_shift
            y_shift = old_y_shift
            self.rect.centerx = round(self.x)
            self.rect.centery = round(self.y)


class EnemyTank(Tank):

    def update(self):
        self.rect.centerx = round(self.x - x_shift)
        self.rect.centery = round(self.y - y_shift)

        if not self.on_move:
            return
        
        if self.direction == Direction.Up:
            self.y -= self.speed
        if self.direction == Direction.Down:
            self.y += self.speed
        if self.direction == Direction.Left:
            self.x -= self.speed
        if self.direction == Direction.Right:
            self.x += self.speed
        
        self.rect.centerx = round(self.x - x_shift)
        self.rect.centery = round(self.y - y_shift)


class Fire(pygame.sprite.Sprite):
    def __init__(self, image, x, y, direction):
        super().__init__()
        self.image = pygame.image.load(f'tiles/{image}')
        self.w = TILE_SIZE
        self.h = TILE_SIZE
        self.size = (self.w, self.h)

        self.direction = direction  
        
        self.original_image = pygame.transform.scale(
            self.image, self.size
        )
        self.image = pygame.transform.scale(
            self.image, self.size
        )
        self.image = pygame.transform.rotate(
            self.image, self.direction.value
        )
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)

        self.speed = TILE_SIZE / 6 * 2
    
    def update(self):
        if self.direction == Direction.Up:
            self.y -= self.speed
        if self.direction == Direction.Down:
            self.y += self.speed
        if self.direction == Direction.Left:
            self.x -= self.speed
        if self.direction == Direction.Right:
            self.x += self.speed
        
        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)

        if self.x < 0 or self.y < 0 or self.x > WORLD_W or self.y > WORLD_H:
            # Удаляет спрайт огня из всех групп (группа fires)
            # Удаляет тогда, когда тайл вышел за границы поля
            self.kill()
        
        if spritecollideany(self, walls, collide_mask):
            self.kill()

x_shift = 0
y_shift = 0

name_to_tile = {
    'grass': grass,
    'stone': stone,
    'water': water
}

ARROWS = [
    pygame.K_UP, pygame.K_DOWN, 
    pygame.K_LEFT, pygame.K_RIGHT
]


def load_world():
    global world_height, world_width
    global WORLD_H, WORLD_W
    global walls, waters

    file = open('map.txt', 'r')

    world_info = next(file)
    world_size = world_info.strip().split()
    world_width = int(world_size[0])
    world_height = int(world_size[1])

    WORLD_H = world_height * TILE_SIZE
    WORLD_W = world_width * TILE_SIZE
    
    waters = pygame.sprite.Group()
    walls = pygame.sprite.Group()

    for line in file:
        line = line.strip()
        i, j, tile = line.split()

        i = int(i)
        j = int(j)
        image = name_to_tile[tile]
        
        tile = Tile(image, i, j)
        if image == water:
            waters.add(tile)
        if image == stone:
            walls.add(tile)
        
    file.close()


load_world()

ground = pygame.sprite.Group()

for i in range(world_height):
    for j in range(world_width):
        tile = Tile(default_tile, i, j)
        ground.add(tile)

tank = PlayerTank('tank-1.png', 3, 3)
enemy = EnemyTank('tank-2-enemy.png', 21, 21)

fires = pygame.sprite.Group()


sound_battle = pygame.mixer.Sound('audio/battle.mp3')
sound_shot = pygame.mixer.Sound('audio/shot.mp3')
sound_tank = pygame.mixer.Sound('audio/tank_move.mp3')

channel_0 = pygame.mixer.Channel(0)
channel_1 = pygame.mixer.Channel(1)
channel_2 = pygame.mixer.Channel(2)

channel_0.set_volume(0.2)  # У разных каналов своя громкость (от 0 до 1)
channel_1.set_volume(0.8)  # Чем меньше значение, тем меньше громкость
channel_2.set_volume(0.5)

channel_0.play(sound_battle, -1)  # -1 для бесконечного проигрывания

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                tank.change_direction(Direction.Up)
            if event.key == pygame.K_DOWN:
                tank.change_direction(Direction.Down)
            if event.key == pygame.K_LEFT:
                tank.change_direction(Direction.Left)
            if event.key == pygame.K_RIGHT:
                tank.change_direction(Direction.Right)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            fire = Fire('fire.png', tank.x, tank.y, tank.direction)
            fires.add(fire)
            channel_1.play(sound_shot, 0)
            
        if event.type == pygame.KEYDOWN:
            if event.key in ARROWS:
                tank.on_move = True
                channel_2.play(sound_tank, -1)
        
        if event.type == pygame.KEYUP:
            if event.key in ARROWS:
                tank.on_move = False
                channel_2.stop()
    
    ground.update()
    waters.update()
    walls.update()
    tank.update()
    enemy.update()
    fires.update()

    screen.fill(BLACK)

    ground.draw(screen)
    waters.draw(screen)
    walls.draw(screen)
    
    screen.blit(tank.image, tank.rect)
    screen.blit(enemy.image, enemy.rect)

    fires.draw(screen)
    
    pygame.time.delay(25)
    pygame.display.update()
pygame.quit()
