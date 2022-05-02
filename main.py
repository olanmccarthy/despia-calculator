import sys
from calculator import Calculator

# Command Line error handling
if len(sys.argv) < 3:
    raise Exception("You have not provided enough arguments\nThis script should be run like: 'python3 deck.ydk 100'")
elif len(sys.argv) > 3:
    raise Exception("You have provided too many arguments\nThis script should be run like: 'python3 deck.ydk 100'")
elif sys.argv[1][-4:] != '.ydk':
    raise Exception("Provided decklist is not a .ydk file!")
elif not (isinstance(int(sys.argv[2]), int)):
    raise Exception("Loop amount is not a positive integer!")

calculator = Calculator(sys.argv[1], int(sys.argv[2]))
calculator.run()