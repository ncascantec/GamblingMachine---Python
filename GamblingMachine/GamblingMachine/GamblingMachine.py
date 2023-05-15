import random

MAX_LINES = 3 #Constant value for maximun of lines to bet on
MAX_BET = 100 #Constant value for maximun bet amount allowed
MIN_BET = 1 #Constant value for minimun bet amount allowed
ROWS = 3 #Constant value for rows in the machine
COLS = 3 #Constant value for columns in the machine

symbol_count = {           #Dictionary for the gambling machine
    "A": 3,
    "X": 5,
    "Y": 6,
    "Z": 8
    }

symbol_value = {           #Dictionary for the values on the gambling machine
    "A": 5,
    "X": 4,
    "Y": 3,
    "Z": 2
    }

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line] #We look at the first column because that's where the first symbols are always going to be for each row and then get whatever line were on
        for column in columns:
            symbol_to_check = column[line] #We are checking the first symbol in the column
            if symbol != symbol_to_check:
                break                      #If we found one of the symbols is not equal to the previous symbol or equal to all of the symbols that should be in this row, then we break out of the fault 
        else:                              #If symbols are the same then we don't break 
            winnings += values[symbol] * bet #If we get to the end of the for loop and we've not broke out (means all of the symbols are the same), the user won. The user won wahtever the multiplier is for that symbol times their bet
            winning_lines.append(line + 1) #We are returning to values, the total amount the user won as well as what lines they won on.
    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols): #Parameters are passed to this function to code the machine spin slots
    all_symbols = []  #Symbols are going to be added into this symbol list
    for symbol, symbol_count in symbols.items():   #We are iterating through the dictionary to pick random values for the machine
        for _ in range(symbol_count): #To loop trough the symbol count and avoid unused variables
            all_symbols.append(symbol)

    columns = []   #Loop to select what values are going to go in every column, each of these nested lists are going to represent the values
    for _ in range(cols):  #For each of the columns we have, we need to generate the values inside of the colums
        column = []          #For every column we need to generate a certain number of symbols
        current_symbols = all_symbols[:]  #We are going to use a copy of the list to remove values from the list so we can't choose that value again
        for _ in range(rows):  #We loop through the number of values that we need to generate, wich is equal to the number of rows that we have
            value = random.choice(current_symbols) #Value is going to be choosed randomly from the list
            current_symbols.remove(value) #It's going to find the first instance of this value in the list and remove it
            column.append(value)  #We are going to add the value to the column
    
        columns.append(column) #We add our column to our columns list

    return columns #We return our columns

def print_slot_machine(columns): #Funtion to print and test the slots machine
    for row in range(len(columns[0])):  #We are going to be transposing the matrix, the number of rows we have is the number of elements in each of our columns
       for i,column in enumerate(columns):  #Loop through all of the columns and only print the first value in it, whatever the index of my current row is
           if i != len(columns) - 1: #For every column we only print the current row that we're on
               print(column[row], end=" | ") #Im going to print the value that's at the first row of the column
           else:
               print(column[row], end="")
     
       print()

def deposit():
    while True: #Because whe need to constantly ask the cx to enter a deposit amount until a valid amount is entered
        amount = input("What would you like to deposit? $")
        if amount.isdigit(): #Check that the amount entered is actually a number
            amount = int(amount) #Because the variable is a string by default, so we need to set it as int
            if amount > 0: #Check if the number is greater than zero
                break # If it is greater than zero break here
            else: #If is not greater than zero else
                print("Amount must be grater than 0.")
        else:
            print("Please enter a number.") #If the amount is not a digit 
                
    return amount #The valid amount is returned

def get_numer_of_lines(): #To ask the cx how many lines they are gonna bet on
    while True: 
        lines = input("Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? ") #Constant max lines is converted to string to avoid exeptions on the program
        if lines.isdigit():
            lines = int(lines) 
            if 1 <= lines <= MAX_LINES: #Check if the value lines is in between the max of lines to bet on
                break 
            else: 
                print("Enter a valid number of lines")
        else:
                print("Please enter a number.") 
                
    return lines

def get_bet(): #To ask the cx how muchs they are gonna bet on
    while True: 
        amount = input("How much would you like to bet on each line? $") #Constant max lines
        if amount.isdigit():
            amount = int(amount) 
            if MIN_BET <= amount <= MAX_BET: #Check if the value is in between the max and min amount to bet on
                break 
            else: 
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.") #Constants are converted to string 
        else:
                print("Please enter a number.") 
                
    return amount

def spin(balance):
    lines = get_numer_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"Your current balance of: ${balance} is not enough for this bet")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.") 
    print(f"You won on lines:", *winning_lines) #We call the splat operator or the unpack operator, it's going to pass every single line from the winning lines list to the priont function
    return winnings - total_bet

def main(): 
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)

    print(f"You left with ${balance}")
main()

