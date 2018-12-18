# Nick Purington's Quiz 

# A list of numbered prompts to be passed in to the play game function
numbered_prompts = ["__1__", "__2__", "__3__", "__4__", "__5__", "__6__", "__7__", "__8__"]

# Strings to pass in to the playing_level function  
easy = "One way to __1__ someone's retention of __2__ is to test their knowledge using a __3__.  Also known as a __4__, this term is used in Britan to refer to an eccentric person."
medium = "Mars is the __1__ planet from the __2__ and the __3__ smallest planet in the solar system, after __4__.  Named after the Roman god of war, it is ofter referred to as the __5__ planet."
hard = "The DeLorean DMC-12 is a __1__ car manufactured by __2__ Motor Company from __3__ to __4__.  The car featured __5__ wing doors, a __6__ body, and brushed __7__ __8__ body panels."

# Answers to numbered prompts
easy_answers = ["gauge", "information", "test", "quiz"]
medium_answers = ["fourth", "sun", "second", "mercury", "red"]
hard_answers = ["sports", "DeLorean", "1981", "1983", "gull", "fiberglass", "stainless", "steel"]

answer_list = []

guesses = 0

game_over_count = 0
                                
def answer_string(number, numbered_prompts):
    """ Loop for prompting the "blanks" """
    for pos in numbered_prompts:
        if pos in number:
            return pos
    return None

def playing_level():
    """ Determines which playing level will run """ 
    user_input_1 = raw_input("Hello, welcome to Nick's quiz.  Please select a level of difficulty - Easy, Medium, Hard" + " ")
    while user_input_1 not in ["easy", "medium", "hard"]:
        print "Sorry, this is not an available level."
        user_input_1 = raw_input("Hello, welcome to Nick's quiz.  Please select a level of difficulty - Easy, Medium, Hard" + " ")
    if user_input_1.lower() == "easy":
        print easy
        print " "
        return easy
    elif user_input_1.lower() == "medium":
        print medium
        print " "
        return medium
    elif user_input_1.lower() == "hard":
        print hard
        print " "
        return hard

# Checks if answers are correct
def level_evaluation():
    """ Checks to see if answers are correct, and loops back incorect answers until correct """
    global user_input_2
    user_input_2 = raw_input("Please enter an answer for:" + replacement + " ")
    while user_input_2 not in (easy_answers + medium_answers + hard_answers):
        global guesses
        guesses = guesses + 1
        if guesses == 4:
            global game_over_count
            game_over_count = game_over_count + 1
            print "Sorry, out of tries.  Game over."
            return " "
            break
        return incorrect_answer()
    if user_input_2 in (easy_answers + medium_answers + hard_answers):
        guesses = 0
        return correct_answer()
        answer_list.remove(user_input_2)
    
def correct_answer():
    """ Called by the level_evaluation function when answers are correct """ 
    index_1 = len(level) - len(replaced) - 1
    answer_list.append(user_input_2)
    print " "
    print "Correct!"
    print " "
    print " ".join(replaced + answer_list + level[-index_1:])
    return " " 
       
def incorrect_answer():
    """ Called by the level_evaluation function when answers are incorrect """
    index_2 = len(level) - len(replaced)
    global user_input_2
    print " "
    print "Incorrect Answer - Please Try Again"
    print " "
    print " ".join(replaced + level[-index_2:])
    print " "
    return level_evaluation()
    
def game_start():
    """ Plays the game by receiving the inputs and producing the final correct answers """
    global replaced
    global number
    global level
    replaced = []
    level = playing_level().split()
    for number in level:
        global replacement
        replacement = answer_string(number, numbered_prompts)
        if replacement != None:
            print level_evaluation()
            if game_over_count != 0:
                return " "
            number = number.replace(replacement, user_input_2)
            replaced.append(number)
        else:
            replaced.append(number)
    replaced = " ".join(replaced)
    return "You completed the quiz - Great job!!"

print game_start()
