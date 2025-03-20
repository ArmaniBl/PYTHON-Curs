import pygame
import random
from sys import exit

pygame.init()
W = 800
L = 400
score, mistakes = 0, 0
top_score = 0
flag_letter, flag_word, flag_game_over, flag_first_game = False, False, True, True

counter, text = 1, '1'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
screen = pygame.display.set_mode((W, L))
test_font = pygame.font.Font(None, 50)
pygame.display.set_caption("Клавиатурный тренажёр")
clock = pygame.time.Clock()

fon_surface = pygame.image.load('graphics/fon.jpg').convert_alpha()
new_fon = pygame.transform.scale(fon_surface, (400, 200))
fon_rect = new_fon.get_rect(bottomright=(W, L))


def EndGame(score, mistakes, top_score):
    score_surface = test_font.render("Ваш счёт: " + str(score), True, 'Blue')
    screen.blit(score_surface, (300, 50))
    mistake_surf = test_font.render('Ошибок: ' + str(mistakes), True, 'Red')
    screen.blit(mistake_surf, (300, 100))
    top_score_surf = test_font.render("Рекорд: " + str(top_score), True, "Gold")
    screen.blit(top_score_surf, (600, 15))
    yes_surf = test_font.render("Повторить попытку", True, "Green")
    no_surf = test_font.render("Выйти", True, "Red")
    yes_rect = yes_surf.get_rect(midleft=(250, 200))
    screen.blit(yes_surf, yes_rect)
    no_rect = no_surf.get_rect(midright=(450, 300))
    screen.blit(no_surf, no_rect)
    if (yes_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed(3) == (True, False, False)) or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):  # Повторить попытку
        return True
    if no_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed(3) == (True, False, False):  # Выйти
        pygame.quit()
        exit()


def StartGame():
    text_surface = test_font.render("Играть", True, "White")
    text_rect = text_surface.get_rect(center=(W//2, L//2))
    screen.fill((23,4,32))  # Темно-фиолетовый цвет
    screen.blit(new_fon, fon_rect)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    if text_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed(3) == (True, False, False):
        return True


while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    while flag_game_over == False:
        if counter >= 0:  # Настраиваем счётчик
            text = str(counter).rjust(3)
            time_surf = test_font.render('Время: ' + str(counter), True, 'Pink')
        else:
            flag_game_over = True

        if flag_word == False:  # Читаем слово из файла, выводим его со счётом и ошибками на экран
            word = random.choice(open("russian.txt", encoding='utf-8').readlines())
            text_surface = test_font.render(word[:-1], True, 'White')
            screen.blit(text_surface, (275, 150))
            score_surf = test_font.render('Счёт: ' + str(score), False, 'Blue')
            mistake_surf = test_font.render('Ошибок: ' + str(mistakes), True, 'Red')
            flag_word = True
            i = 0

        if flag_letter == False:
            if (i == len(word[:-1])):  # Если слово кончилось
                flag_word = False
            if (flag_word):  # Берём букву из слова
                letter = word[i]
                flag_letter = True
                i += 1

        for event in pygame.event.get():  # Ввод с клавиатуры
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode == letter.lower():  # Буква совпала
                    score += 1
                    text_surface = test_font.render(word[i:-1], True, 'Green')
                    score_surf = test_font.render('Счёт: ' + str(score), True, 'Blue')
                    flag_letter = False
                else:  # Не совпала
                    score -= 1
                    mistakes += 1
                    text_surface = test_font.render(word[i:-1], True, 'Red')
                    score_surf = test_font.render('Счёт: ' + str(score), True, 'Blue')
                    mistake_surf = test_font.render('Ошибок: ' + str(mistakes), True, 'Red')
                    flag_letter = False
            if event.type == pygame.USEREVENT:
                counter -= 1

        if score > top_score:  # Подсчёт рекорда
            top_score = score

        screen.fill((18, 6, 31))  # Темно-фиолетовый цвет
        screen.blit(new_fon, fon_rect)
        screen.blit(text_surface, (275, 150))
        screen.blit(score_surf, (600, 15))
        screen.blit(mistake_surf, (600, 55))
        screen.blit(time_surf, (25, 25))
        pygame.display.flip()
        clock.tick(60)

    screen.fill((18, 6, 31))  # Темно-фиолетовый цвет
    screen.blit(new_fon, fon_rect)
    if flag_game_over and flag_first_game == False:  # Конечный экран
        if (EndGame(score, mistakes, top_score)):
            counter = 15
            score = 0
            mistakes = 0
            flag_letter = False
            flag_word = False
            flag_game_over = False

    if flag_game_over and flag_first_game:  # Начальный экран
        if (StartGame()):
            counter = 15
            flag_game_over = False
            flag_first_game = False

    pygame.display.update()
    clock.tick(60)
