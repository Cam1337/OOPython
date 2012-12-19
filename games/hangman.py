import random
import string
import sys

class Hangman(object):
    def __init__(self, wordlist, guesses=lambda word:len(word), converter=None):
        self.wordlist = wordlist
        
        self.guesses = guesses
        self.converter = converter
        
        self.guessed_letters = []
        self.all_guesses = []
        self.final_state = []
        self.current_state = []
        
        self.allowed = list(string.lowercase + string.uppercase + "-_'")
    
    def getPercentage(self):
        if self.guessed_letters == []: return 100
        return int(100 * (1 - len(self.guessed_letters)/self.guesses))
    
    def display(self):
        print "Health [{0}{1}%]".format("="*self.getPercentage(), self.getPercentage())
        print " ".join(self.current_state)

    def validateGuess(self, guess):
        if len(guess) > 1: return "Only enter one letter"
        if guess not in self.allowed: return "Only choose letters in {0}".format("".join(self.allowed))
        if guess in self.all_guesses: return "You have already guessed that letter"
        return True
    
    def makeGuess(self, validator, prompt="Please guess a letter"):
        validated = False
        while validated != True:
            if validated != False:
                print "Error: {0}".format(validated)
            _user_guess = raw_input("{0}: ".format(prompt))
            validated = validator(_user_guess)
        return _user_guess

    def initialize(self):
        wordlist = open(self.wordlist,"r")
        secret_word = random.choice(wordlist.readlines()).strip()
        if self.converter and callable(self.converter):
            secret_word = self.converter(secret_word)
        wordlist.close()
        
        self.final_state = list(secret_word)
        self.current_state = ["_" for r in secret_word]
        
        if callable(self.guesses):
            self.guesses = self.guesses(secret_word)
        self.guesses = self.guesses * 1.0

    def end(self):
        if self.final_state == self.current_state:
            sys.exit("You win!")
        if self.guesses == len(self.guessed_letters):
            sys.exit("You loose!")

    def play(self):
        self.initialize()
        print "Secret word == {0}".format("".join(self.final_state))
        while self.guesses - len(self.guessed_letters) > 0:
            self.display()
            user_guess = self.makeGuess(self.validateGuess)
            self.all_guesses.append(user_guess)
            if user_guess not in self.final_state:
                self.guessed_letters.append(user_guess)
                
            for i,v in enumerate(self.final_state):
                if v == user_guess:
                    self.current_state[i] = v
            
            if self.final_state == self.current_state:
                break
        self.end()

h = Hangman("/users/cam/desktop/wordlist.txt", converter = lambda s: s.lower())
h.play()
            