import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("공 튕기기 게임")

# 색상 정의 (배경, 공, 막대 색상 변경)
WHITE = (255, 255, 255)     # 하얀색
RED = (255, 0, 0)           # 빨간색
BLUE = (0, 0, 255)          # 파란색 (막대 색상 변경)
BLACK = (0, 0, 0)           # 검은색 (글자 색상)
YELLOW = (255, 255, 0)      # 노란색

# 공 설정
ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5
ball_dy = 5

# 막대 설정
paddle_width = 100
paddle_height = 10
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 50
paddle_speed = 10

# 게임 상태
game_over = False
game_started = False
start_time = 0
elapsed_time = 0

# 폰트 설정 (영어로 텍스트를 출력)
try:
    font = pygame.font.Font("NanumGothic.ttf", 55)  # 한글을 지원하는 폰트 파일을 로드
    time_font = pygame.font.Font("NanumGothic.ttf", 35)
    countdown_font = pygame.font.Font("NanumGothic.ttf", 100)
except IOError:
    font = pygame.font.SysFont(None, 55)
    time_font = pygame.font.SysFont(None, 35)
    countdown_font = pygame.font.SysFont(None, 100)

# 게임 루프
clock = pygame.time.Clock()

# 키보드 입력 처리
keys = pygame.key.get_pressed()

# 게임 시작 화면 표시 (카운트다운)
def show_start_screen():
    countdown_numbers = [3, 2, 1]
    
    for i, number in enumerate(countdown_numbers):
        screen.fill(WHITE)  # 이전 숫자 지우기 위해 화면을 하얀색으로 지운다
        
        # 카운트다운을 화면에 표시
        countdown_text = countdown_font.render(str(number), True, BLACK)  # 글자 색상을 검은색으로 변경
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 3))
        
        pygame.display.flip()
        pygame.time.delay(1000)  # 1초 대기

    pygame.time.delay(500)  # 카운트다운 후 잠시 멈추고 게임 시작

# 게임 루프
while True:
    # 게임 시작 화면 표시
    if not game_started:
        show_start_screen()
        game_started = True
        start_time = pygame.time.get_ticks()  # 게임 시작 시간 기록

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 게임 오버 상태에서 더 이상 진행되지 않도록
    if game_over:
        # "Game Over" 텍스트 출력
        game_over_text = font.render("Game Over", True, BLACK)  # 글자 색상을 검은색으로 변경
        screen.fill(WHITE)  # 배경을 하얀색으로 설정
        screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 3))

        # 경과 시간 계산 (초 단위)
        elapsed_time_text = time_font.render(f"Time: {elapsed_time // 1000} seconds", True, BLACK)  # 글자 색상을 검은색으로 변경
        screen.blit(elapsed_time_text, (WIDTH // 3, HEIGHT // 2 + 50))

        pygame.display.flip()
        continue  # 게임 오버 상태에서는 게임 진행을 멈춤

    # 키보드 입력 처리: 막대 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    # 공 위치 업데이트
    ball_x += ball_dx
    ball_y += ball_dy

    # 벽에 부딪히면 반사
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_dx = -ball_dx
    if ball_y - ball_radius <= 0:
        ball_dy = -ball_dy

    # 막대와 공 충돌 처리
    if (paddle_x <= ball_x <= paddle_x + paddle_width) and (ball_y + ball_radius >= paddle_y):
        ball_dy = -ball_dy  # 공이 막대에 닿으면 위로 튕기기

    # 공이 바닥에 떨어지면 게임 오버 처리
    if ball_y + ball_radius >= HEIGHT:
        game_over = True
        elapsed_time = pygame.time.get_ticks() - start_time  # 게임 시작 시간에서 끝난 시간을 빼서 경과 시간 기록

    # 화면 배경 채우기
    screen.fill(WHITE)  # 배경을 하얀색으로 설정

    # 공 그리기 (빨간색)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

    # 막대 그리기 (파란색)
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))

    # 화면 업데이트
    pygame.display.flip()

    # 프레임 속도 설정
    clock.tick(60)
