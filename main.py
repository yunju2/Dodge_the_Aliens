import pygame as pg
import random

pg.init()

# Screen setting
size = x_val, y_val = 1280, 720
screen = pg.display.set_mode(size)
player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
pg.display.set_caption('Dodged the Aliens')

# BackGround image
background = pg.image.load('space2.png')
background = pg.transform.scale(background, size)

spacefighter_image = pg.image.load('spaceShip.png')
spacefighter_image = pg.transform.scale(spacefighter_image, (80, 40))

alien_image = pg.image.load('alien.png')
alien_image = pg.transform.scale(alien_image, (30, 50))
alien_respawn_time = pg.time.get_ticks()

start_time = pg.time.get_ticks()
clock = pg.time.Clock()

# 초기값 설정
aliens_per_gust = 2  # 초기 외계인 수
elapesed_time = 0  # 게임 시작 시간
aliens = pg.sprite.Group()


# 플레이어(우주선) 클래스
class Escape(pg.sprite.Sprite):
    image = spacefighter_image
    dt = 3

    def __init__(self):
        super(Escape, self).__init__()
        self.rect = self.image.get_rect()
        self.rect.x = player_pos.x
        self.rect.y = player_pos.y

    # 외계인과 충돌하면 true 리턴
    def collide(self, sprites):
        for sprite in sprites:
            if pg.sprite.collide_rect(self, sprite):
                return True
        return False

    # 화면에 우주선 그리기
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


# 외계인 클래스
class Alien(pg.sprite.Sprite):
    image = alien_image

    def __init__(self, xpos, ypos, hspeed, wspeed):
        super(Alien, self).__init__()
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.hspeed = hspeed
        self.wspeed = wspeed

        self.set_direction()

    # 위치 업데이트
    def update(self):
        self.rect.y += self.wspeed
        self.rect.x += self.hspeed

        # 화면 밖에 벗어나면 없어짐
        if self.rect.x > x_val or self.rect.x < 0 - self.rect.width or self.rect.y > y_val or self.rect.y < 0 - self.rect.height:
            self.kill()

    # 외계인 회전시키기
    def set_direction(self):
        if self.hspeed > 0:
            self.image = pg.transform.rotate(self.image, 180)
        elif self.hspeed < 0:
            self.image = pg.transform.rotate(self.image, 90)
        elif self.wspeed > 0:
            self.image = pg.transform.rotate(self.image, 180)


spacefighter = Escape()


# 외계인 랜덤하게 호출하기
def random_alien(speed):
    random_or = random.randint(1, 4)
    if random_or == 1:  # 위 -> 아래
        return Alien(random.randint(0, x_val), 0, 0, speed)
    if random_or == 2:  # 오른쪽 -> 왼쪽
        return Alien(x_val, random.randint(0, y_val), -speed, 0)
    if random_or == 3:  # 아래 -> 위
        return Alien(random.randint(0, x_val), y_val, 0, -speed)
    if random_or == 4:  # 왼쪽 -> 오른쪽
        return Alien(0, random.randint(0, y_val), speed, 0)


# 화면에 외계인 그리기
def draw_alien():
    global aliens_per_gust
    global alien_respawn_time
    min_speed = 2
    max_speed = 5

    # 1초 마다 외계인 그리도록 제안
    if pg.time.get_ticks() - alien_respawn_time < 1000:
        return

    if elapesed_time > 180:  # 게임시작 시간 180초 이후
        aliens_per_gust = 13
        max_speed = 80
        min_speed = 60
    elif elapesed_time > 100:  # 게임시작 시간 100초 이후
        aliens_per_gust = 10
        min_speed = 6
        max_speed = 9
    elif elapesed_time > 50:  # 게임시작 시간 50초 이후
        aliens_per_gust = 8
        min_speed = 5
        max_speed = 8
    elif elapesed_time > 30:  # 게임시작 시간 30초 이후
        aliens_per_gust = 6
        min_speed = 4
        max_speed = 7
    elif elapesed_time > 10:  # 게임시작 시간 10초 이후
        aliens_per_gust = 4
        min_speed = 3
        max_speed = 6

    for i in range(aliens_per_gust):
        aliens.add(random_alien(random.randint(min_speed, max_speed)))

    alien_respawn_time = pg.time.get_ticks()


# 화면에 타이머 그리기
def draw_timer():
    global elapesed_time
    elapesed_time = (pg.time.get_ticks() - start_time) / 1000
    font = pg.font.SysFont('Helvetica', 30, True, False)
    text_score = font.render("Time : " + str(elapesed_time), True, "WHITE")
    screen.blit(text_score, [10, 50])


# 화면에 그리는 함수들 호출
def draw_screen():
    screen.blit(background, (0, 0))
    spacefighter.draw()
    draw_timer()
    draw_alien()
    pg.display.update()


# 게임 시작 전 화면
def draw_before_start_screen():
    start_screen = pg.display.set_mode((x_val, y_val))
    start_screen.fill((0, 0, 0))

    # 화면에 보여지는 글자 속성
    gameStartFont = pg.font.SysFont('arial', 120, True)
    gameSurf = gameStartFont.render('Game start ! ', True, 'white')
    gameRect = gameSurf.get_rect()
    gameRect.midtop = (start_screen.get_width() / 2, 80)

    gameStartFont2 = pg.font.SysFont('arial', 100, True)
    gameSurf2 = gameStartFont2.render(' >> Press D << ', True, 'orange')
    gameRect2 = gameSurf2.get_rect()
    gameRect2.midtop = (start_screen.get_width() / 2, 300)

    gameStartFont3 = pg.font.SysFont('arial', 40, True)
    gameSurf3 = gameStartFont3.render('To move the space ship, use the arrow keys on your keyboard ', True, 'white')
    gameRect3 = gameSurf3.get_rect()
    gameRect3.midtop = (start_screen.get_width() / 2, 500)

    start_screen.blit(gameSurf, gameRect)
    start_screen.blit(gameSurf2, gameRect2)
    start_screen.blit(gameSurf3, gameRect3)

    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    return 'play'


# 게임 시작 화면
def start_game():
    while True:
        pg.display.update()
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 'quit'

        keys = pg.key.get_pressed()

        original_x = spacefighter.rect.x
        original_y = spacefighter.rect.y

        if keys[pg.K_UP]:
            spacefighter.rect.y -= spacefighter.dt
        if keys[pg.K_DOWN]:
            spacefighter.rect.y += spacefighter.dt
        if keys[pg.K_RIGHT]:
            spacefighter.rect.x += spacefighter.dt
        if keys[pg.K_LEFT]:
            spacefighter.rect.x -= spacefighter.dt

        if is_position_x() or is_position_y():
            spacefighter.rect.x = original_x
            spacefighter.rect.y = original_y

        draw_screen()
        aliens.update()
        aliens.draw(screen)

        if spacefighter.collide(aliens):
            return 'game_over'


# 게임 종료 화면
def draw_game_over_screen():
    end_screen = pg.display.set_mode((x_val, y_val))
    end_screen.fill((0, 0, 0))

  # 화면에 보여지는 글자 속성
    gameOverFont = pg.font.SysFont('arial', 120, True)
    gameSurf = gameOverFont.render('Game Over', True, 'red')
    gameRect = gameSurf.get_rect()
    gameRect.midtop = (end_screen.get_width() / 2, 20)

    game_end_time = pg.font.SysFont('bahnschrift', 200, )
    timeSurf = game_end_time.render('time : ' + str(elapesed_time), True, 'white')
    timeRect = timeSurf.get_rect()
    timeRect.midtop = (end_screen.get_width() / 2, gameRect.height + 50)

    reGameFont = pg.font.SysFont('arial', 100)
    reGame = reGameFont.render('play again ?', True, 'purple')
    reGameRect = reGame.get_rect()
    reGameRect.midtop = (end_screen.get_width() / 2, timeRect.height + 300)

    reGameFont2 = pg.font.SysFont('arial', 70)
    reGame2 = reGameFont2.render('➡️ If you want , Press space bar ', True, 'pink')
    reGameRect2 = reGame2.get_rect()
    reGameRect2.midtop = (end_screen.get_width() / 2, timeRect.height + 450)

    end_screen.blit(gameSurf, gameRect)
    end_screen.blit(timeSurf, timeRect)
    end_screen.blit(reGame, reGameRect)
    end_screen.blit(reGame2, reGameRect2)
    pg.display.update()
    # pg.time.wait(50000)

    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    restart_game()
                    return 'play'


# 게임 재시작 화면
def restart_game():
    global start_time
    start_time = pg.time.get_ticks()
    spacefighter.rect.x = x_val / 2
    spacefighter.rect.y = y_val / 2
    aliens.empty()


# 플레이어(우주선)이 이동하다가 화면 밖으로 못 벗아나게 처리
def is_position_y():
    return spacefighter.rect.y - spacefighter.rect.h / 2 < 0 or spacefighter.rect.y + spacefighter.rect.h / 2 > y_val


def is_position_x():
    return spacefighter.rect.x - spacefighter.rect.w / 2 < 0 or spacefighter.rect.x + spacefighter.rect.w / 2 > x_val


def main_loop():
    action = 'start_screen'
    while action != 'quit':
        if action == 'start_screen':
            action = draw_before_start_screen()
        elif action == 'play':
            action = start_game()
        elif action == 'game_over':
            action = draw_game_over_screen()


main_loop()
