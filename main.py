import pygame as pg
from random import choice
from text import Text

# todo: Создание Окна игры
pg.init()

W, H = 1200, 800

window = pg.display.set_mode((W, H))
pg.display.set_caption("Pinc-Pong in TWO")
pg.display.set_icon(pg.image.load("ping-pong.png"))

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

FPS = 60
clock = pg.time.Clock()

# todo: Player
wplayer = 25
hplayer = 150
player1 = pg.rect.Rect(wplayer, H // 2 - hplayer // 2, wplayer, hplayer)
player2 = pg.rect.Rect(W - (wplayer*2), H // 2 - hplayer // 2, wplayer, hplayer)

# todo : Circle
x = 0
y = 0
radius_circle = 15
circle_rect = pg.Rect(W // 2 - radius_circle, H // 2 - radius_circle, radius_circle * 2, radius_circle * 2)


# todo : Счет
score_1 = 0
score_2 = 0

# todo: Текст
score1_txt = Text(f"{score_1}", "noteworthy", 50, WHITE)
score2_txt = Text(f"{score_2}", "noteworthy", 50, WHITE)
game_over = Text("Game Over", "noteworthy", 70, (0, 0, 0), RED)

game_over.rect_txt.center = (W // 2, H // 2 - 100)
score1_txt.rect_txt.topright = (W // 2  + radius_circle*-4, 0)
score2_txt.rect_txt.topleft = (W // 2 + (radius_circle*2), 0)

def update_txt():
    global score_1, score_2, score1_txt, score2_txt
    score1_txt = Text(f"{score_1}", "noteworthy", 50, WHITE)
    score2_txt = Text(f"{score_2}", "noteworthy", 50, WHITE)
    
    score1_txt.rect_txt.topright = (W // 2 + radius_circle*-2, 0)
    score2_txt.rect_txt.topleft = (W // 2 + radius_circle*2, 0)

# todo: Рандомное значение x и y
def x_y_rand():
    global x, y
    x = choice([-1, 1])
    y = choice([-1, 1])

# todo : Вывод окна
def window_update():
    window.fill('black')
    update_txt()
    window.blit(score1_txt.text, score1_txt.rect_txt)
    window.blit(score2_txt.text, score2_txt.rect_txt)
    pg.draw.aaline(window, WHITE, (W // 2, 0), (W // 2, H // 2 - radius_circle))
    pg.draw.aaline(window, WHITE, (W // 2, H), (W // 2, H // 2 + radius_circle))
    pg.draw.circle(window, WHITE, (W // 2, H // 2), 5)
    pg.draw.circle(window, WHITE, (W // 2, H // 2), radius_circle*2, 1)
    pg.draw.rect(window, BLUE, player1)
    pg.draw.rect(window, RED, player2)
    pg.draw.circle(window, GREEN, circle_rect.center, radius_circle)
    pg.display.flip()
    clock.tick(FPS)

# todo : Проверка на ВЫХОД
def quit_func():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
            

def new_score():
    global isgame
    isgame = False
    circle_rect.topleft = (W // 2 - radius_circle, H // 2 - radius_circle)
    player1.topleft = (wplayer, H // 2 - hplayer // 2)
    player2.topleft = (W - (wplayer*2), H // 2 - hplayer // 2)
    
# todo Основной цикл игры
isgame = False
while True:
    # todo : Начальная позиция ИЛИ ЖЕ если кто то кому то забил
    if not isgame:
        window_update()
        rr = True
        while rr:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        isgame = True
                        rr = False
                        FPS = 60
                        x_y_rand()
                    
    quit_func()
        
    # todo : Плитки для 1 Игрока 
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        player1.y -= 5
    elif keys[pg.K_s]:
        player1.y += 5
    
    # todo : Плитка для 2 игрока
    if keys[pg.K_UP]:
        player2.y -= 5
    elif keys[pg.K_DOWN]:
        player2.y += 5
    
    # todo : Передвижение Шарика
    circle_rect.x += x * 5
    circle_rect.y += y * 5
    
    # todo : Ударился ли он об игрока
    if circle_rect.colliderect(player1):
        x = 1
        FPS += 3
    elif circle_rect.colliderect(player2):
        x = -1
        FPS += 3
    
    # todo : Ударился ли он об Стенку
    if circle_rect.y == 0:
        y = 1
    elif circle_rect.y == H - radius_circle * 2:
        y = -1
        
    # todo : Вышел ли он за границы поля
    if circle_rect.x <= 0:
        score_2 += 1
        new_score()
    elif circle_rect.x >= W - radius_circle*2:
        score_1 += 1
        new_score()
        
        
    if score_1 == 3 or score_2 == 3:
        if score_1 > score_2:
            win_text = Text("СИНИЙ ИГРОК WIN!", "noteworthy", 40, (0, 0, 0), BLUE)
        else:
            win_text = Text("КРАСНЫЙ ИГРОК WIN!", "noteworthy", 40, (0, 0, 0), RED)
        
        win_text.rect_txt.center = (W // 2, H // 2 + 100)
        while True:
            quit_func()
            window.fill('black')
            window.blit(game_over.text, game_over.rect_txt)
            window.blit(win_text.text, win_text.rect_txt)
            pg.display.flip()
        
    # todo : ВЫВОД ВСЕГО НА ЭКРАН
    window_update()