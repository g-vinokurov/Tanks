import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (25, 25, 25)
LIGHT_GRAY = (50, 50, 50)

TILE_SIZE = 30

visible_world_width = 31
visible_world_height = 15

SCREEN_W = TILE_SIZE * visible_world_width
SCREEN_H = TILE_SIZE * visible_world_height
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

grass = pygame.image.load('tiles/grass.jpg')
ground = pygame.image.load('tiles/ground.jpg')
stone = pygame.image.load('tiles/stone.png')
water = pygame.image.load('tiles/water.jpg')
lava = pygame.image.load('tiles/lava.jpg')

tank = pygame.image.load('tiles/tank.png')

grass = pygame.transform.scale(grass, (TILE_SIZE, TILE_SIZE))
ground = pygame.transform.scale(ground, (TILE_SIZE, TILE_SIZE))
stone = pygame.transform.scale(stone, (TILE_SIZE, TILE_SIZE))
water = pygame.transform.scale(water, (TILE_SIZE, TILE_SIZE))
lava = pygame.transform.scale(lava, (TILE_SIZE, TILE_SIZE))

tank_original = pygame.transform.scale(tank, (TILE_SIZE, TILE_SIZE))
tank = pygame.transform.rotate(tank_original, 270)

tank_x = visible_world_width // 2
tank_y = visible_world_height // 2

world_height = 25
world_width = 25

world = []
for i in range(world_height):
    row = []
    for j in range(world_width):
        row.append(None)
    world.append(row)

x_shift = 0
y_shift = 0

name_to_tile = {
    'grass': grass,
    'ground': ground,
    'lava': lava,
    'stone': stone,
    'water': water
}


def load_world():
    global world, world_height, world_width

    file = open('map.txt', 'r')

    world_info = next(file)
    world_size = world_info.strip().split()
    world_width = int(world_size[0])
    world_height = int(world_size[1])

    world = []
    for i in range(world_height):
        row = []
        for j in range(world_width):
            row.append(None)
        world.append(row)

    for line in file:
        line = line.strip()
        i, j, tile = line.split()

        i = int(i)
        j = int(j)
        tile = name_to_tile[tile]
        
        world[i][j] = tile
        
    file.close()


load_world()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and y_shift > 0:
                y_shift -= 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if y_shift < world_height - visible_world_height:
                    y_shift += 1
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if x_shift > 0:
                    x_shift -= 1
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if x_shift < world_width - visible_world_width:
                    x_shift += 1
    
    screen.fill(BLACK)
    
    for i in range(visible_world_height):
        for j in range(visible_world_width):
            x = j * TILE_SIZE
            y = i * TILE_SIZE

            cell = world[i + y_shift][j + x_shift]
            if cell is not None:
                screen.blit(cell, (x, y))
            else:
                screen.blit(grass, (x, y))
    
    screen.blit(tank, (tank_x * TILE_SIZE, tank_y * TILE_SIZE))

    
    pygame.time.delay(50)
    pygame.display.update()
pygame.quit()
