import pygame
from enum import Enum

import pygame.sprite

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
        # Меняем значение поля direction
        self.direction = direction
        # Поворачиваем наш тайл (без изменения оригинала)
        self.image = pygame.transform.rotate(
            self.original_image, 
            self.direction.value
        )
        # Обновляем маску (т.к. поменялось положение пикселей)
        self.mask = pygame.mask.from_surface(self.image)


class PlayerTank(Tank):
    def update(self):
        global world
        global x_shift, y_shift

        WORLD_H = world_height * TILE_SIZE
        WORLD_W = world_width * TILE_SIZE

        if not self.on_move:
            return
        
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


tank = PlayerTank('tank-1.png', 3, 3)
enemy = EnemyTank('tank-2-enemy.png', 21, 21)

world_height = 25
world_width = 25

ground = pygame.sprite.Group()

for i in range(world_height):
    for j in range(world_width):
        tile = Tile(default_tile, i, j)
        ground.add(tile)

world = pygame.sprite.Group()

# world = []
# for i in range(world_height):
#     row = []
#     for j in range(world_width):
#         row.append(None)
#     world.append(row)

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
    global world, world_height, world_width

    file = open('map.txt', 'r')

    world_info = next(file)
    world_size = world_info.strip().split()
    world_width = int(world_size[0])
    world_height = int(world_size[1])
    
    world = pygame.sprite.Group()
    # world = []
    # for i in range(world_height):
    #     row = []
    #     for j in range(world_width):
    #         row.append(None)
    #     world.append(row)

    for line in file:
        line = line.strip()
        i, j, tile = line.split()

        i = int(i)
        j = int(j)
        image = name_to_tile[tile]
        
        world.add(Tile(image, i, j))
        
    file.close()


load_world()


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
            
        if event.type == pygame.KEYDOWN:
            if event.key in ARROWS:
                tank.on_move = True
        
        if event.type == pygame.KEYUP:
            if event.key in ARROWS:
                tank.on_move = False
    
    ground.update()
    world.update()
    tank.update()
    enemy.update()
    
    screen.fill(BLACK)
    
    # for i in range(world_height):
    #     for j in range(world_width):
    #         x = j * TILE_SIZE - x_shift
    #         y = i * TILE_SIZE - y_shift
    #         
    #         screen.blit(default_tile, (x, y))
    # 
    #         cell = world[i][j]
    #         if cell is not None:
    #             screen.blit(cell, (x, y))

    ground.draw(screen)
    world.draw(screen)

    screen.blit(tank.image, tank.rect)
    screen.blit(enemy.image, enemy.rect)
    
    pygame.time.delay(25)
    pygame.display.update()
pygame.quit()
