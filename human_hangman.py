### Epitech Pre_Pool Day 7
# Project Title: "First Program"
# Project Goal: Hangman Game!

import random
import time
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument("--ap", type=int, help= "Allowed Penalties")
parser.add_argument("--ts", type=int, help= "Time Limit (in seconds)")
parser.add_argument("--wl", type=int, help="Word Length")
parser.add_argument("--f", type=str, help="File Name - including extension")

args = parser.parse_args()

if args.ap:
    if args.ap < 1:
        print("You have entered an invalid Allowed Penalites. Reassigned to 12.")
        args.ap = 12
if args.ts: 
    if args.ts < 0:
        print("You have entered an invalid time. Reassigned to 30 seconds.")
        args.ts = 30

if args.f:
    if not os.path.exists("./"+args.f) and not os.path.exists("./"+args.f+".txt"):
        print("Your file does not exist. Reverting to Random.")
        args.f = "random"

if args.wl:
    if args.wl < 3:
        print("You have entered an invalid word length. Reassigned to 7.")
        args.wl = 7

#  history.append({
#         "game_id": game_id,
#         "word": word,
#         "won": False,
#         "penalties": penalties,
#     })

def get_best_score(history):
    attempts = 1000
    word = ""
    for game in history:
        if game["attempts"] < attempts:
            attempts = game["attempts"]
            word = game["word"]
        else:
            continue
    return attempts, word

def get_current_time():
    timestamp = time.time()
    local_time = time.localtime(timestamp)
    formatted_date = time.strftime("%Y-%m-%d", local_time)
    hour = time.strftime("%H", local_time)
    minute = time.strftime("%M", local_time)

    return ' '.join([formatted_date, hour, minute])

def update_best_score(score, score_time):
    with open("high_scores.txt", "a") as f:
        f.write(" ".join([str(score), score_time, "\n"]))
        f.close()
    return

def set_high_scores(history):
    high_scores = []
    best_score_in_current_history, word = get_best_score(history)
    current_time = get_current_time()
    with open("high_scores.txt", "r") as f:
        for line in f:
            high_scores.append([line])
        f.close()

    best_score_in_file = high_scores[0]
    for highscore in high_scores:
        scoring = highscore[0].split(" ")
        print(scoring)
        if int(scoring[0]) < int(best_score_in_file[0].split(" ")[0]):
            best_score_in_file = highscore
        else:
            continue
    if best_score_in_current_history < int(best_score_in_file[0].split(" ")[0]):
        update_best_score(best_score_in_current_history, current_time)
        print(f"Best ever! You guessed {word} in {best_score_in_current_history} attempts!")
    else:
        print(f"You guessed {word} in {best_score_in_current_history} attempts, but the record from {" ".join(best_score_in_file[0].split(" ")[1:-3])} is {int(best_score_in_file[0].split(" ")[0])} attempts.")
    return


def win_rate(history):
    wins = 0
    for game in history:
        if game["won"] == True:
            wins += 1
        else:
            continue
    return (wins/len(history)) * 100


def average_penalties(history):
    penalties = 0
    games_won = 0
    for game in history:
        if game["won"] == True:
            penalties += game["penalties"]
            games_won += 1
        else:
            continue

    if games_won == 0:
        return None
    return penalties/games_won

def longest_word(history):
    longest_word = ""
    for game in history:
        if game["won"] == True:
            if len(game["word"]) > len(longest_word):
                longest_word = game["word"]
            else:
                continue
        else:
            continue
    if longest_word == "":
        return None
    return longest_word


def get_games_continue():
    valid_choice = False
    games_continue = False
    while not valid_choice:
        try:
            continue_choice = str(input("Would you like to keep playing? (Y/N) ")).lower()
            if continue_choice == "y":
                games_continue = True
                valid_choice = True      
            elif continue_choice =="n":
                games_continue = False
                valid_choice = True
            else:
                print("Enter a valid option please.")
                valid_choice = False
        except:
            print("Enter a valid option please.")
            continue
    return games_continue

def give_hint(word, pairs, penalties, guesses_letters):
    penalties += 2
    print(f"Your hint has been applied. 2 penalties have been applied. Your total penalty is {penalties}")
    user_guess = random.choice([char for char in word if char not in pairs])
    print(user_guess)

    return pairs, penalties, guesses_letters, user_guess

### Returns a random word from 'file_name'.txt
def get_word_from_file(file_name, length):
    words = []

    with open(file_name, "r") as f:
        for line in f:
            for w in line.split():
                words.append(w)
    word = ""
    while word == "":

        candidates = [word for word in list(words) if len(word) == length]
        if candidates:
            word = random.choice(candidates)
        else:
            try:
                length = int(input("You have chosen an invalid length. Please enter a new length: "))
            except:
                print("You have entered a non-integer. Please enter a valid length.")
    
    return word
    
### Check User Attempts. If attempts >= 12 (by default), they lose. Otherwise, they continue.
def check_attempts(atmpt, allowed = 12):
    if atmpt >= allowed: 
        print("You Lose!")
        return False
    else: 
        return True

### Gets the Number of Allowed Penalties from the User
def get_allowed_penalties():
    allowed = 12
    while True:
        user_choice = input("Would you like to change the number of penalties allowed? (Y/N): ").lower()
        if user_choice == "quit":
            quit()
        if user_choice == "y":
            while True:
                try:
                    allowed = int(input("Enter the number of penalties you would like: "))
                    break
                except:
                    print("You have entered an invalid number. Enter an integer.")
            return allowed

        elif user_choice == "n":
            return allowed
        else:
            print(f"{user_choice} is an invalid option. Try again.")

### Gets the time limits
def get_time_limit():
    time_limit_bool = False
    time_limit_s = 0
    while True:
        user_choice = input("Would you like to add a time limit? (Y/N): ").lower()
        if user_choice == "quit":
            quit()
        if user_choice == "y":
            while True:
                try:
                    time_limit_s = int(input("Enter the number of seconds you would like: "))
                    time_limit_bool = True
                    break
                except:
                    print("You have entered an invalid number. Enter an integer.")
            return time_limit_bool, time_limit_s

        elif user_choice == "n":
            return time_limit_bool, time_limit_s
        else:
            print(f"{user_choice} is an invalid option. Try again.")
    return
### Generates the '_ ' pairs to initialize the 'empty' word for the user to see
def generate_pairs(string):
    pairs = ""
    for i in range(len(string)):
        pairs += "_ "
    return pairs

### gets a random (lower-case) english word of length (chosen by user)
def get_random_word(length):
    options = ["random", "ocean", "plants", "space", "travel", "vehicles", "custom"]
    while True:
        user_input = ""
        try:
            user_input = args.f if args.f else input("Do you have a theme (Random, Plants, Space, Travel, Vehicles, Custom) in mind? ").lower()
            user_input = user_input.replace(".txt", "")
            if user_input in options:
                if user_input == "random":
                    from english_words import get_english_words_set
                    return random.choice([words for words in list(get_english_words_set(['web2'],lower=True)) if len(words) == length])
                elif user_input != "random" and user_input != "custom":
                    return get_word_from_file(user_input + ".txt", length)
                elif user_input == "custom":
                    user_input = input("Enter your file name (.txt only): ")
                    return get_word_from_file(user_input + ".txt", length)

            else:
                print(f"You have entered {user_input} which is an invalid option. Try again.")
                continue
        except Exception as e:
            print(f"An Error has occurred: {e}")

### updates the '_ ' paris according to the user guess.
def update_pairs(pairs, user_guess, word):
    for i in range(len(word)):
        if user_guess == word[i]:
            pairs = pairs[:2*i] + user_guess + pairs[2*i+1:]
        else:
            continue
    return pairs

### Checks if the user has won by compairing the pairs (stripped) to the word
def check_win(pairs, word):
    stripped = pairs.replace(" ", "")
    if stripped == word:
        return True
    else:
        return False

### Gets the desired word length from the user.
def get_word_length():
    while True:
        try:
            length = int(input("Enter the length of the word you would like: "))
            break
        except:
            print("You have entered an invalid option. Please enter an integer.")
    return length

### Implements the word guess interaction.
def word_guess_interaction(guesses_words, word, penalties):
    game_finished = False
    game_won = False
    print(f"You have guessed: {guesses_words} so far.")
    user_guess = input("Your (word) guess: ").lower()
    guesses_words.add(user_guess)
    if user_guess == word:
        print(f"Congratulations! Your guess is correct!! You won!!!")
        game_won = True
        game_finished = True
    else:
        penalties += 5
        print(f"Your guess of '{user_guess}' is incorrect. 5 penalties have been applied. Your total penalty is {penalties}")

    return guesses_words, penalties, game_finished, game_won

### Implements the letter guess interaction.
def letter_guess_interaction(guesses_letters, word, penalties, pairs, allowed_penalties):
    user_guess = ""
    game_finished = False
    game_won = False
    while len(user_guess) != 1:
        user_guess_not_in_letters = False
        print(f"You have guessed {guesses_letters} so far.")
        while not user_guess_not_in_letters:
            user_guess = input("Your (letter) guess: ").lower()
            if user_guess in guesses_letters:
                print("You have chosen a repeated letter. Please try again. No penalty applied.")
            else:
                user_guess_not_in_letters = True

        if user_guess == "?":
            if (check_win(pairs,word)):
                print("The word is already full revealed.")
                continue

            if penalties + 2 >= allowed_penalties:
                print("Sorry, this option is unavailable to you. You have too many penalties.")
                continue
            else:
                pairs, penalties, guesses_letters, user_guess = give_hint(word, pairs, penalties, guesses_letters)

        if (len(user_guess) != 1):
            print(f"You entered: {user_guess} which is an invalid guess. Please try again.\n")
            continue

        guesses_letters.add(user_guess)
        if user_guess in word:
            pairs = update_pairs(pairs, user_guess, word)
            if check_win(pairs, word):
                print(f"Congratulations! Your guess is correct!! You won!!!")
                game_won = True
                game_finished = True
            else: 
                print("Congratulations! Your guess is correct!!")
        
        else:
            penalties += 1
            print(f"Your guess of '{user_guess}' is incorrect. 1 penalty has been applied. Your total penalty is {penalties}")
            
    return guesses_letters, penalties, game_finished, pairs, game_won

### Game Implementation

### Welcoming
print("Hello! Welcome to Hangman!")
print(f"The rules are as follows:\n - You may select the length of the word (int)\n - Each turn you may guess either a letter or a full word: \n   - if the letter exists, I will reveal all instances of that letter, but if it doesn't you are penalized 1 point.\n   - if the word exists, you win! If it doesn't, you are penalized 5 points. \n   - Once you are penalized {args.ap if args.ap else 12} times, you lose!\n")
history = []
games_continue = True

while games_continue:
    ### Initializations
    penalties = 0
    guess_count = 1
    game_finished = False
    guesses_letters = set()
    guesses_words = set()
    


    ### Initialize Word and Pairs

    word_length = args.wl if args.wl else get_word_length()
    word = get_random_word(word_length)
    pairs = generate_pairs(word)
    allowed_penalties = args.ap if args.ap else get_allowed_penalties()
    time_limit_bool, time_limit_s = (True, args.ts) if args.ts else get_time_limit()
    user_time = 0

    game_id = word + str(round(time.time(),0))
    history.append({
        "game_id": game_id,
        "word": word,
        "won": False,
        "penalties": penalties,
        "attempts": 0
    })
    

    print(f"Welcome! You have chosen a word with {word_length} letters. Good luck!!\n")
    if time_limit_bool:
        print("Your time starts now!!!")
        user_time = time.time()

    ### Game Play

    while not game_finished:
        if time_limit_bool and time.time() - user_time >= time_limit_s:
            print("Oh no! You have run out of time!!!")
            history[len(history)-1]["penalties"] = penalties
            history[len(history)-1]["won"] = False
            game_finished = True
            games_continue = get_games_continue()
            continue
        
        print(pairs)
        try:
            guess_type = input(f"Guess #{guess_count}\nWould you like to guess a word(w) or a letter (l)?\n")
            if guess_type.lower() == "quit":
                game_finished = True
                history[len(history)-1]["penalties"] = penalties
                history[len(history)-1]["won"] = False
                games_continue = False
                continue

            if guess_type.lower() == "w":
                guesses_words, penalties, game_finished, game_won = word_guess_interaction(guesses_words, word, penalties)
                history[len(history)-1]["attempts"] += 1
                if game_finished:
                    history[len(history)-1]["penalties"] = penalties
                    history[len(history)-1]["won"] = game_won
                    games_continue = get_games_continue()
                    continue
            elif guess_type.lower() == "l":
                guesses_letters, penalties, game_finished, pairs, game_won = letter_guess_interaction(guesses_letters, word, penalties, pairs, allowed_penalties)
                history[len(history)-1]["attempts"] += 1
                if game_finished: 
                    history[len(history)-1]["penalties"] = penalties
                    history[len(history)-1]["won"] = game_won
                    games_continue = get_games_continue()
                
                    continue
            else:
                print("You entered and invalid option - enter 'w' to guess a word or 'l' to guess a letter.")
                continue
            guess_count += 1

            if not check_attempts(penalties, allowed_penalties):
                game_finished = True
                history[len(history)-1]["penalties"] = penalties
                print(f"Your final result: {pairs}\nThe word: {word}.")
               
                games_continue = get_games_continue()
               
                continue
        except Exception as e:
            print(f"An error has occurred: {e}")

print(history)
print(longest_word(history))
print(average_penalties(history))
print(win_rate(history))
set_high_scores(history)




