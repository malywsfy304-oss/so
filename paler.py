import pygame
import sys
import random

# ---------------------------
# تهيئة pygame
# ---------------------------
pygame.init()

# ---------------------------
# إعدادات الشاشة
# ---------------------------
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏓 Big Pong - Simple Version 🏓")

# ---------------------------
# الألوان
# ---------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 60, 60)
BLUE  = (60, 120, 255)
YELLOW = (255, 255, 60)
GREEN = (60, 255, 120)

# ---------------------------
# إعدادات اللعبة
# ---------------------------
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 150
BALL_SIZE = 25
PADDLE_SPEED = 8
BALL_SPEED_X = 6
BALL_SPEED_Y = 6

# ---------------------------
# الخط
# ---------------------------
FONT = pygame.font.SysFont("Arial", 48)

# ---------------------------
# الكائنات
# ---------------------------
left_paddle = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

ball_dx = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
ball_dy = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

score_left = 0
score_right = 0

# ---------------------------
# رسم العناصر
# ---------------------------
def draw():
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, BLUE, left_paddle)
    pygame.draw.rect(WIN, RED, right_paddle)
    pygame.draw.ellipse(WIN, YELLOW, ball)
    pygame.draw.aaline(WIN, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    score_text = FONT.render(f"{score_left}   |   {score_right}", True, GREEN)
    WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
    pygame.display.flip()

# ---------------------------
# إعادة الكرة للمنتصف
# ---------------------------
def reset_ball():
    global ball_dx, ball_dy
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_dx = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
    ball_dy = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

# ---------------------------
# AI بسيط للمضرب الأيمن
# ---------------------------
def ai_move():
    if ball.centery > right_paddle.centery and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED - 2
    elif ball.centery < right_paddle.centery and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED - 2

# ---------------------------
# الحلقة الرئيسية
# ---------------------------
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # تحكم اللاعب الأيسر
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED

    # تحرك المضرب الأيمن (AI)
    ai_move()

    # حركة الكرة
    ball.x += ball_dx
    ball.y += ball_dy

    # اصطدام مع الحواف
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

    # اصطدام مع المضارب
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_dx *= -1

    # تسجيل النقاط
    if ball.left <= 0:
        score_right += 1
        reset_ball()
    if ball.right >= WIDTH:
        score_left += 1
        reset_ball()

    draw()
    clock.tick(60)
