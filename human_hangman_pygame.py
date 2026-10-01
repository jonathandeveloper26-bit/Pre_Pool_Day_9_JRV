### Epitech Pre_Pool Day 9
# Project Title: "Pygame Hangman!"
# Project Goal: Hangman Game!

import random
import time
import argparse
import pygame
import string
from english_words import get_english_words_set

### gets a random (lower-case) english word of length (chosen by user)
def get_random_word():    
    return random.choice([words for words in list(get_english_words_set(['web2'],lower=True)) if len(words) == 7]).upper()

### Generate my empty pairs
def generate_pairs(string):
    pairs = ""
    for i in range(len(string)):
        pairs += "_ "
    return pairs  

### updates the '_ ' paris according to the user guess.
def update_pattern(pairs, user_guess, word):
    for i in range(len(word)):
        if user_guess == word[i]:
            pairs = pairs[:2*i] + user_guess + pairs[2*i+1:]
        else:
            continue
    return pairs

def draw_message(images):
    x = 640 - 150 * len(images) // 2
    for img in images:
        screen.blit(img, (x, 330))
        x += 150

def display_grid():
    x = 100
    y = 100
    count = 1

    for key in letters:
        letter = pygame.transform.scale(letters[key], (60,60))
        if used[key] == False:
            screen.blit(letter, (x, y))
        else:
            letter.set_alpha(80)
            screen.blit(letter,(x,y))

        if count % 5 == 0:
            x = 100
            y += 60
        else:
            x += 60
        count += 1

def display_pattern():
    x = 1000
    y = 500
    for char in pattern:
        letter = letters.get(char,"")
        if char == "_":
            letter = pygame.image.load("letters_3d/underscore.png").convert_alpha()
        if letter:
            letter = pygame.transform.scale(letter,(60,60))
        else:
            continue
        screen.blit(letter, (x-len(pattern)*25,y))
        x += 60

def menu_display(screen):
    menu_bg = pygame.image.load("playground.png")
    screen.blit(menu_bg,(0,0))
    play_img = pygame.image.load("play.png")
    play_img = pygame.transform.scale(play_img,(400,200))

    quit_img = pygame.image.load("quit.png")
    quit_img = pygame.transform.scale(quit_img,(400,200))

    leader_board_img = pygame.image.load("leaderboard.png")
    leader_board_img = pygame.transform.scale(leader_board_img, (400,200))
    screen.blit(play_img,menu_pg)
    screen.blit(quit_img,menu_qg)
    screen.blit(leader_board_img, menu_lb)
    return

def load_last_scores(count=5):
    try:
        with open("high_scores.txt", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        return []
 
    entries = []
    for line in lines:
        parts = line.split()
        if len(parts) != 4 or not parts[0].isdigit():
            continue
        attempts, date, hour, minute = parts
        entries.append((int(attempts), f"{date} {hour}:{minute}"))
 
    return entries[-count:]

def draw_scores(screen, font, entries, x, y, line_height=40, color=(255, 255, 255)):
    """Draw one line per entry, top to bottom, starting at (x, y)."""
    for i, (attempts, when) in enumerate(entries):
        text = f"{attempts:>2} attempts   {when}"
        surface = font.render(text, True, color)
        screen.blit(surface, (x, y + i * line_height))



pygame.init()
score_font = pygame.font.SysFont(None, 36)
scores = load_last_scores()


screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
bg_img = pygame.image.load("background_img.jpg")
stick_man = pygame.image.load("stickman.webp").convert_alpha()
stick_man = pygame.transform.scale(stick_man, (100,200))
stick_man_dead = pygame.image.load("dead_stickman.png").convert_alpha()
stick_man_dead = pygame.transform.scale(stick_man_dead, (300, 200))

letters = {
    ch: pygame.image.load(f"letters_3d/{ch}.png").convert_alpha()
    for ch in string.ascii_uppercase
}

you = [letters["Y"], letters["O"], letters["U"]]
won = [letters["W"], letters["O"], letters["N"]]
lost = [letters["L"], letters["O"], letters["S"], letters["T"]]

letter_rects = {}
x, y = 100, 100

for count, key in enumerate(letters, start= 1):
    letter_rects[key] = pygame.Rect(x, y, 60, 60)
    if count %5 == 0:
        x = 100
        y += 60
    else:
        x += 60

used = {
    ch: False
    for ch in string.ascii_uppercase
}

word = get_random_word()
pattern = generate_pairs(word)
penalties = 0
allowed_penalties = 12

running = True
state = "playing"


menu = pygame.Rect(0,0, 1280, 720)
menu_pg = pygame.Rect(440, 50, 400, 200)
menu_qg = pygame.Rect(440, 270, 400, 200)
menu_lb = pygame.Rect(440, 490, 400, 200)

display_menu = True
display_lb = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if state == "playing" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for key, rect in letter_rects.items():
                if rect.collidepoint(event.pos) and not used[key]:
                    used[key] = True
                    if key in word:
                        pattern = update_pattern(pattern, key, word)
                        if "_" not in pattern:
                            state = "won"
                    else:
                        penalties += 1
                        if penalties >= allowed_penalties:
                            state = "lost"
            if menu_qg.collidepoint(event.pos):
                pygame.quit()
            if menu_pg.collidepoint(event.pos):
                display_menu = False
            if menu_lb.collidepoint(event.pos):
                display_lb = True
                display_menu = False
        if state == "playing" and event.type == pygame.KEYDOWN and display_lb == True:
            display_lb = False
            display_menu = True

        if state == "playing" and event.type == pygame.KEYDOWN and display_lb == False and display_menu == False:
             key = event.unicode
             key = str(key).upper()
             if not used[key]:
                used[key] = True
                if key in word:
                    pattern = update_pattern(pattern, key, word)
                    if "_" not in pattern:
                        state = "won"
                else:
                    penalties += 1
                    if penalties >= allowed_penalties:
                        state = "lost"
             
                 
             
    if display_menu: 
        menu_display(screen)
        pygame.display.flip()
        clock.tick(60)
        continue

    if not display_menu and display_lb:
        draw_scores(screen, score_font, scores, x=450, y=250)
        pygame.display.flip()
        clock.tick(60)
        continue

        
    screen.blit(bg_img, (0,0))

    ### Stick Man (Alive, Dead, Free!)
    if state == "playing":
        screen.blit(stick_man, (900, 100))

    if state == "lost":
        screen.blit(stick_man_dead, (900,100))
    
    if state == "won":
        pass
    
    ### Displaying Grid
    display_grid()

    ### Displaying Pattern
    display_pattern()

    ### Win/Loss Messages
    if state == "won":
        draw_message(you + won)
        
    elif state == "lost":
        draw_message(you + lost)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()