import pygame
import random
import sys

#   set up pygame and window
pygame.init()
pygame.display.set_caption("Pong")

#   Set up screen
size = width, height = 600, 480
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)

#   set up the boards
board_size = 10, 50
board_speed = 5

player_board = pygame.Rect([0, height//2 - board_size[1]/2], board_size)
cpu_board = pygame.Rect([width - board_size[0], height//2 - board_size[1]/2], board_size)

#   Set up the ball
ball = pygame.Rect(width//2 - 5, height//2 - 5, 10, 10)
max_vertical_speed = board_speed + 1
max_horizontal_speed = 5

ball_speed = [random.randint(1, max_horizontal_speed), random.randint(1, max_vertical_speed)]

#   set up fonts
point_font = pygame.font.SysFont('arial.ttf', 20)
end_game_font = pygame.font.SysFont('arial.ttf', 50)

#   Set up points
player_point = 0
cpu_point = 0

player_point_display = point_font.render(str(player_point), True, white)
cpu_point_display = point_font.render(str(cpu_point), True, white)

player_point_rect = player_point_display.get_rect()
cpu_point_rect = cpu_point_display.get_rect()

player_point_rect.topleft = 10, 10
cpu_point_rect.topright = width-10, 10

#   Set up variables in game
move_up = False
move_down = False

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_up = True

            elif event.key == pygame.K_DOWN:
                move_down = True

            elif event.key == pygame.K_q:
                sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                move_up = False

            elif event.key == pygame.K_DOWN:
                move_down = False

    if move_up is True and player_board.top - board_speed >= 0:
        player_board = player_board.move(0, -board_speed)

    if move_down is True and player_board.bottom + board_speed <= height:
        player_board = player_board.move(0, board_speed)

#   Moving cpu
    if ball.center != cpu_board.center:
        if ball.center[1] > cpu_board.center[1] and cpu_board.bottom + board_speed <= height:
            if not (ball.center[1] < cpu_board.move(0, board_speed).center[1] and cpu_board.top - board_speed > 0):
                cpu_board = cpu_board.move(0, board_speed)

        elif ball.center[1] < cpu_board.center[1] and cpu_board.top - board_speed > 0:
            if not (ball.center[1] > cpu_board.move(0, -board_speed).center[1] and cpu_board.bottom + board_speed <= height):
                cpu_board = cpu_board.move(0, -board_speed)

#   Reflect ball when hit board
    if ball.left <= player_board.right < ball.move(-ball_speed[0], ball_speed[1]).left:
        if player_board.top < ball.bottom < player_board.bottom:
            ball_speed[0] = random.randint(1, max_horizontal_speed)

            x = ball.top - player_board.top

            if x < board_size[1] //2:
                ball_speed[1] = (board_size[1] // 2 - x) // (board_size[1] // (2*max_vertical_speed))
                ball_speed[1] = -abs(ball_speed[1])

            else:
                ball_speed[1] = (board_size[1] // 2 - x) // (board_size[1] // (2*max_vertical_speed))
                ball_speed[1] = abs(ball_speed[1])

    elif ball.move(-ball_speed[0], ball_speed[1]).right < cpu_board.left <= ball.right:
        if cpu_board.top < ball.bottom < cpu_board.bottom:
            ball_speed[0] = -random.randint(1, max_horizontal_speed)
            ball_speed[1] = random.randint(1, max_vertical_speed)

#   Handles ball out of screen
    if ball.left < -10:
        cpu_point += 1
        cpu_point_display = point_font.render(str(cpu_point), True, white)

        if cpu_point == 3:
            gameover_message = end_game_font.render("YOU LOSE", True, white)
            gameover_message_rect = gameover_message.get_rect()
            gameover_message_rect.center = screen.get_rect().center

            screen.blit(gameover_message, gameover_message_rect)

            break

        ball = pygame.Rect(width // 2 - 5, height // 2 - 5, 10, 10)
        ball_speed = [random.randint(1, max_horizontal_speed), random.randint(1, max_vertical_speed)]

    if ball.right > width + 10:
        player_point += 1
        player_point_display = point_font.render(str(player_point), True, white)

        if player_point == 3:
            gameover_message = end_game_font.render("YOU WIN", True, white)
            gameover_message_rect = gameover_message.get_rect()
            gameover_message_rect.center = screen.get_rect().center

            screen.blit(gameover_message, gameover_message_rect)

            break

        ball = pygame.Rect(width // 2 - 5, height // 2 - 5, 10, 10)
        ball_speed = [random.randint(1, max_horizontal_speed), random.randint(1, max_vertical_speed)]

#   Reflect ball when hits wall
    if ball.top <= 0:
        ball_speed[1] = abs(ball_speed[1])

    elif ball.bottom > height:
        ball_speed[1] = -abs(ball_speed[1])

#   Move ball
    ball = ball.move(*ball_speed)

#   Update the screen
    screen.fill(black)

    pygame.draw.rect(screen, (255, 255, 255), player_board)
    pygame.draw.rect(screen, (255, 255, 255), cpu_board)
    pygame.draw.rect(screen, white, ball)

    screen.blit(player_point_display, player_point_rect)
    screen.blit(cpu_point_display, cpu_point_rect)

    pygame.display.update()

    pygame.time.delay(10)

"""
    Make title page including
        Start
        How to play
        Difficulty setting
        Background, 2 cpu play against each other
    Make "game over" or "you win" when score goes above 3 (10 in actual games)
    
"""










