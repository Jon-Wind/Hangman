import google.generativeai as genai #Imports Gemini API
genai.configure(api_key="AIzaSyBEsUqLeqWNuVNEjD0H8r47sjKLK7d8PAE")  #A API key that lets me actually use the AI
model = genai.GenerativeModel("gemini-1.5-flash")  # THe version  for the AI
import os #Used to clear screen
import time #Used mostly for waitings
import sys
import random

game_on = True
answer_word = 'testing' #A testing variable
answer_letters = 0
hint_number = 3 #How many attempts lost till you get a hint
guess_letters = [] #Stores all the guessed letters
success = False
score = 100 #Moves up and down whether or not he player guesses something right or not
l_guesses = 0 #The amount of letter guesses the player has made.

gamemodes_management = {
    "easy": { #Easily adjustable gamemodes and can add more
        "bonus": 25,
        "attempts": 12,
        "display": 'Easy',
        "input": 'e'
    },
    "medium": {
        "bonus": 50,
        "attempts": 8,
        "display": 'Medium',
        "input": 'm'
    },
    "hard": {
        "bonus": 100,
        "attempts": 6,
        "display": 'Hard',
        "input": 'h'
    },
    "outrageous": {
        "bonus": 400,
        "attempts": 3,
        "display": 'Outrageous',
        "input": 'o'
    }
}

win_bonus = '' #A setting that gives you bonus points for winning on harder difficulties
difficulty_setting = '' #Selected from gamemodes_management

def print_slow(str): #Slow types to make parts of the game more dramatic
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.05)

def clear_screen(): #Prevents clogging of terminal.
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear') #works for apple computers

def answer_generator():
    while True:
        answer_letters = input("Input the amount of letters you want roughly (AI isn't always accurate) in your word: ") #Dictates answer length.
        try:
            if int(answer_letters) < 3: #Has to be a letter greater than 3
                print('Input a number greater than 3')
                continue
            else:
                ai_prompt = f'''Generate a {answer_letters} long word
                            thats one word long, all in lower case with no additional spaces. 
                            The word also MUST {answer_letters} long and can't be any longer or shorter.
                            If the word is longer than {answer_letters} DO NOT USE IT!''' #Very strict prompt to generate words
                ai_word = model.generate_content(ai_prompt) #Generates a word for the game
                #print(ai_word.text) #Debugging line
                return str(ai_word.text.strip()) #Strips all the fluff from the AI response and gives the word itself.
        except:
            print('Input a number')

def game_mode():  # Can easily change the difficulty numbers in the function.
    while True:
        global gamemodes_management
        print("\nThese are the available gamemodes:")

        # Display all game modes and corresponding inputs
        for mode in gamemodes_management.values():
            print(f'{mode["display"]} (Input: {mode["input"]})')

        question = input("\nWhat difficulty do you want to play? ").lower()

        global win_bonus
        global answer_letters  # Allows code to access the answer_letters variable
        global difficulty_setting

        # Search for the input dynamically
        for key, mode in gamemodes_management.items():
            if question == mode["input"]:  # Match the user input with the "input" field
                difficulty_setting = mode
                print(f'You picked {difficulty_setting["display"]} mode')

                # Set answer_letters based on difficulty
                answer_letters = {"easy": 5, "medium": 9, "hard": 12}.get(key, 5) #placeholders changed in answer generation

                win_bonus = difficulty_setting["bonus"]
                print(f'You have {difficulty_setting["attempts"]} attempts')
                return difficulty_setting["attempts"]

        # If input is not valid
        print("Wrong input, try again.")

def attempt_manager(remaining):  # Manages the number of attempts the user gets and the word hints
    remaining -= 1
    if remaining == 0:
        print('You lose')
    else:
        print('This is how many attempts you have left:', str(remaining))
    return remaining

def hint_manager(hint_limit):  # Calculates how many turns until the next hint is available
    hint_limit -= 1
    hint_type = random.randint(1, 2)  # Randomly chooses between two hints
    if hint_limit == 0:
        if hint_type == 1:  # AI hint
            ai_prompt = f'Create a hint for the word {answer_word} without using the word itself' #Hint relates to word without the word
        if hint_type == 2:
            ai_prompt = f'Generate a hint for the word {answer_word} by giving a singular letter that is not in {guess_letters}' #Picks a letter in the word and gives it
        ai_response = model.generate_content(ai_prompt)
        print(ai_response.text) #Strips fluff from the AI response and gives the hint itself.
        hint_limit = 3
    else:
        print('This is how many losses till you get a hint:', str(hint_limit))
    return hint_limit

def check_guess(answer, guess):
    return guess in answer

def input_guess(a):  # Allows the user to make a guess
    while True:
        guess_type = input(
            '''\n Input what type of guess you want to make, letter (l) or word (w} or look at your current gamestate (g). ''')
        try:  # Checks if input is a number. A number just loops back and no turn is lost.
            guess_type.isalpha()
            if guess_type.lower() == 'w':  # Guessing a word
                word_guess = input('Input your word: ').lower()
                if word_guess == a:
                    print('You win.')
                    return 'Win'
                else:
                    print('You got it wrong.')
                    return 'Wrong'
            elif guess_type.lower() == 'l':  # Guessing a letter
                guess_input = input('Input your letter: ')
                letter_guess = str(guess_input.lower())
                letter_count = len(letter_guess)

                if letter_count == 1:
                    if letter_guess in guess_letters:
                        print('You already guessed that.\n')
                        return 'Same'
                    elif letter_guess in answer_word:
                        guess_letters.append(letter_guess)
                        print('You got a letter right! \n')
                        global l_guesses 
                        l_guesses += 1
                        return 'Successful'
                    else:
                        guess_letters.append(letter_guess)
                        return 'Wrong'
                else:
                    print('One letter only.')
            elif guess_type == 'g':
                global attempts
                global score
                print_slow('These are your stats')
                print(f'\n Your attempts {attempts}, Your current score {score}.')
        except:
            print('No numbers allowed, try again.')         

def display_word(word, guessed_letters):  # Displays the word with guessed letters
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])

def input_continue(): #Allows user to input to continue to slow the program
    e = input('[Input to continue] ')
    return e

while game_on == True: # Main game loop
    print_slow('\n --------- Welcome ---------')
    time.sleep(1)
    attempts = game_mode()
    answer_word = answer_generator()


    while attempts != 0:  # If attempts are not zero, keep going
        clear_screen()
        success = input_guess(answer_word)
        if success == 'Win':
            if l_guesses > 0:
                score += 100 - l_guesses*10 #100 points added to total score if you guess the word with 10 points deducted for every CORRECT letter guess
                print(f'Your score: {score}')
                break
        elif success == 'Successful':
            success = True
            score += 10
            display_score = str(score) #Keeps a constant string of score
            print('Your current score is ', {display_score})
        elif success == 'Same':
            display_score = str(score) #Keeps a constant string of score
            print('Your current score is ', {display_score})
        else:
            success = False
            print('You got nothing! \n')
            if score != 0: #Can't go below zero.
                score -= 10
            display_score = str(score) #Keeps a constant string of score
            print('Your current score is ', {display_score})
            hint_number = hint_manager(hint_number)
            attempts = attempt_manager(attempts)
        
        print(display_word(answer_word, guess_letters))
        if "_" not in display_word(answer_word, guess_letters):  # If there are no "_", the game is over and you win
            print(f"Congratulations! You guessed the word: {answer_word}")
            print(f'Since you played on {difficulty_setting} you get {win_bonus} extra points')
            score += win_bonus
            print(f'Your score is {score}')
            break
        elif attempts == 0:
            print(f'The answer was {answer_word}')
            score = 0
            display_score = str(score)
            print('Final score is ', {display_score})
        input_continue()

    continue_game = input(f'Do you wish to continue? Your score {score} will be set to zero if you lose. Input N to quit ')
    if continue_game.lower() == 'n':
        score = 0
        game_on == False #Game ends here.
        quit()
    else:
        if score == 0:
            score = 50 #Gives player pity score if he plays again.

