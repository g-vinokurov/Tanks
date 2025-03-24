import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (25, 25, 25)
LIGHT_GRAY = (50, 50, 50)

TILE_SIZE = 32

visible_world_width = 15
visible_world_height = 15

SCREEN_H = TILE_SIZE * visible_world_height
SCREEN_W = SCREEN_H * 2
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

grass = pygame.image.load('tiles/grass.png')
stone = pygame.image.load('tiles/stone.png')
water = pygame.image.load('tiles/water.png')

grass = pygame.transform.scale(grass, (TILE_SIZE, TILE_SIZE))
stone = pygame.transform.scale(stone, (TILE_SIZE, TILE_SIZE))
water = pygame.transform.scale(water, (TILE_SIZE, TILE_SIZE))

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

class Button:
    def __init__(self, tile, text):
        font = pygame.font.Font("USSR-STENCIL.ttf", 30)

        self.tile = tile
        self.tile_rect : pygame.Rect = self.tile.get_rect()

        self.text = font.render(text, True, WHITE)
        self.text_rect = self.text.get_rect()
        
        self.w = self.text_rect.width + TILE_SIZE + 50
        self.h = max(TILE_SIZE, self.text_rect.height) + 20
        self.rect = pygame.Rect(0, 0, self.w, self.h)

        self.is_hovered = False
        self.is_active = False
    
    def check_collision(self, pos):
        self.is_hovered = False
        if self.rect.collidepoint(pos):
            self.is_hovered = True
        return self.is_hovered
    
    def render(self, screen):
        if self.is_hovered:
            pygame.draw.rect(screen, GRAY, self.rect)
        if self.is_active:
            pygame.draw.rect(screen, LIGHT_GRAY, self.rect)
        screen.blit(self.text, self.text_rect)
        screen.blit(self.tile, self.tile_rect)


grass_btn = Button(grass, 'Grass')
stone_btn = Button(stone, 'Stone')
water_btn = Button(water, 'Water')

grass_btn.rect.left = TILE_SIZE * visible_world_width + 25
grass_btn.rect.top = TILE_SIZE // 2
grass_btn.tile_rect.left = grass_btn.rect.left + 20
grass_btn.tile_rect.centery = grass_btn.rect.centery
grass_btn.text_rect.left = grass_btn.tile_rect.right + 10
grass_btn.text_rect.centery = grass_btn.tile_rect.centery

stone_btn.rect.left = TILE_SIZE * visible_world_width + 25
stone_btn.rect.top = grass_btn.rect.bottom + 10
stone_btn.tile_rect.left = stone_btn.rect.left + 20
stone_btn.tile_rect.centery = stone_btn.rect.centery
stone_btn.text_rect.left = stone_btn.tile_rect.right + 10
stone_btn.text_rect.centery = stone_btn.tile_rect.centery

water_btn.rect.left = TILE_SIZE * visible_world_width + 25
water_btn.rect.top = stone_btn.rect.bottom + 10
water_btn.tile_rect.left = water_btn.rect.left + 20
water_btn.tile_rect.centery = water_btn.rect.centery
water_btn.text_rect.left = water_btn.tile_rect.right + 10
water_btn.text_rect.centery = water_btn.tile_rect.centery

tiles_buttons = [grass_btn, stone_btn, water_btn]

selected_tile = None

tile_names = {
    grass: 'grass',
    stone: 'stone',
    water: 'water'
}


name_to_tile = {
    'grass': grass,
    'stone': stone,
    'water': water
}


def load_world():
    global world, world_height, world_width
    # Откроем фал map.txt в папке с программой на чтение
    # Если файла нет, будет ошибка!
    # Кодировка файла - UTF-8 (по умолчанию)
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
        # Уберем вокруг нашей строки все пробельные символы
        # Т.е. пробелы, табуляции и переводы строк
        line = line.strip()
        
        # Строчки имеют вид: <строка> <столбец> <имя-тайла>
        # Метод split() разделит их по пробелам на список строк
        # Т.е. если строка есть: 1 2 grass
        # То мы получим список строк: ['1', '2', 'grass']
        # Каждое значение по порядку присвоится переменным:
        # i = '1'
        # j = '2'
        # tile = 'grass'
        i, j, tile = line.split()
        
        # Приведем строки i и j к целым числам
        i = int(i)
        j = int(j)
        
        # По названию тайла получим картинку
        tile = name_to_tile[tile]
        
        # Поместим тайл в наш мир
        world[i][j] = tile
    
    # Закроем файл
    file.close()


def save_world(world):
    # Откроем фал map.txt в папке с программой на перезапись
    # Если файла нет, он создастся автоматически
    # Кодировка файла - UTF-8
    file = open('map.txt', 'w', encoding='utf-8')

    world_record = ''
    # Ширина мира
    world_record += str(len(world[0]))
    world_record += ' '
    # Высота мира
    world_record += str(len(world))
    world_record += '\n'
    file.write(world_record)

    for i in range(len(world)):
        for j in range(len(world[i])):
            if world[i][j] is None:
                continue
            # Сохраним запись о тайле в формате:
            # <строка> <столбец> <имя-тайла>

            # Эквивалентная запись:
            # record = ''
            # record += str(i)
            # record += ' '
            # record += str(j)
            # record += ' '
            # cell = world[i][j]
            # tile = tile_names[cell]
            # record += tile
            # record += '\n'
            # file.write(record)

            file.write(f'{i} {j} {tile_names[world[i][j]]}\n')
    
    # Закроем файл
    file.close()


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        # Если нажали стрелку вверх 
        # и если мы не в самом верху, то смещаемся на 1 вверх
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and y_shift > 0:
                y_shift -= 1
        # Если нажали стрелку вниз 
        # и если мы не в самом низу, то смещаемся на 1 вниз
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                # проверяем, что не вышли за границы списка (мира)
                if y_shift < world_height - visible_world_height:
                    y_shift += 1
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if x_shift > 0:
                x_shift -= 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if x_shift < world_width - visible_world_width:
                x_shift += 1
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_world(world)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                load_world()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            w = TILE_SIZE * visible_world_width
            h = TILE_SIZE * visible_world_height
            if x < w and y < h:
                tile_x = x // TILE_SIZE + x_shift
                tile_y = y // TILE_SIZE + y_shift
                world[tile_y][tile_x] = selected_tile
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверяем, что хотя бы одна кнопка нажата
            # Устанавливаем переменную-флаг в значение False
            any_button_pressed = False
            for button in tiles_buttons:
                if button.check_collision(event.pos):
                    # Как только нашли нажатую кнопку
                    # Ставим флаг в True и прекращаем поиск
                    any_button_pressed = True
                    break
            
            # Если ни одна кнопка не была нажата,
            # Переходим на следующую итерацию цикла событий
            if not any_button_pressed:
                continue
            
            # Иначе для нажатой кнопки меняем состояние на противопложное
            # А для других кнопок ставим его в False
            for button in tiles_buttons:
                if button.check_collision(event.pos):
                    button.is_active = not button.is_active
                else:
                    button.is_active = False
    
    
    mouse_pos = pygame.mouse.get_pos()

    grass_btn.check_collision(mouse_pos)
    stone_btn.check_collision(mouse_pos)
    water_btn.check_collision(mouse_pos)
    
    # Устанавливаем текущий выбранный тайл
    # Если какая-то кнопка активна, берём её тайл
    selected_tile = None
    for button in tiles_buttons:
        if button.is_active:
            selected_tile = button.tile

    screen.fill(BLACK)
    
    # Отрисовываем только 10x10 элементов мира (видимый участок)
    for i in range(visible_world_height):
        for j in range(visible_world_width):
            x = j * TILE_SIZE
            y = i * TILE_SIZE
            # Хотим получить элемент мира с учетом смещения
            cell = world[i + y_shift][j + x_shift]
            if cell is not None:
                screen.blit(cell, (x, y))
            else:
                w = TILE_SIZE
                h = TILE_SIZE
                pygame.draw.rect(screen, WHITE, (x, y, w, h), 1)
    
    grass_btn.render(screen)
    stone_btn.render(screen)
    water_btn.render(screen)
    
    pygame.time.delay(50)
    pygame.display.update()
pygame.quit()
