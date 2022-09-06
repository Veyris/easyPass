from zxcvbn import zxcvbn
import hashlib
import requests
from pyfiglet import figlet_format
from termcolor import colored
import re

def feedback(score, guesses, guesses_log10, time_to_crack, feedback, symbols, capital_letters, small_letters, numbers, used_classes_count, password):
    color = "red"
    """
        Method prints feedback to console
        @params:
            score           - Required  : Integer
            guesses         - Required  : Double
            guesses_log10   - Required  : Double
            time_to_crack   - Required  : List
            feedback        - Required  : List
            password        - Required  : String
        """

    print("-"*36 + "PASSWORT-STATISTICS" + "-"*36)

    print(f"Number of Guesses needed: {guesses} \n          - Should be at least 10^6 for Online Passwords, 10^10 for Offline Passwords")
    print(f"Number of Guesses in Log10: 10^{guesses_log10} \n          - Should be at least 6 for Online Passwords, 10 for Offline Passwords")
    
    offline_fast = time_to_crack["offline_fast_hashing_1e10_per_second"]
    offline_slow = time_to_crack["offline_slow_hashing_1e4_per_second"]
    online_throttled = time_to_crack["online_throttling_100_per_hour"]
    online_no_throttle = time_to_crack["online_no_throttling_10_per_second"]
    
    print(f"Crack Time needed:")

    print(f"          - Online no throttling (10 Hashes per second): {online_no_throttle}")
    print(f"          - Online with throttling (100 Hashes per hour): {online_throttled}")
    print(f"          - Offline Fast Hashing (10000000000 Hashes per second): {offline_fast}")
    print(f"          - Offline Slow Hashing (10000 Hashes per second): {offline_slow}")

    print(f"You used {used_classes_count} different Classes (Captial Letters, Small Letters, Numbers or Symbols in your Password.")

    printLine()
    if score < 3:
        color = "red"
        print(colored(f"You can use this as online- password, but you could improve it!  Your password: \"{password}\"  -  Score should be at least 3 out of 4, your Score: {score}", "red"))
        print(colored(f"You could improve your password:","red"))
        
        if symbols == 1 or capital_letters == 1 or numbers == 1:
            print(colored(f"          - inserting uppercase letters, symbols or digits in the middle (Attackers know people often put Digits, Symbols and Uppercase Letters at beginning or end of the password.", "red" ))
        
        print(colored(f"          - Make a sentence that no one has ever said before like \"alienslikeracoonsanddrinkchewinggum\".", "red" ))
        print(colored(f"          - Avoid using passwords with personal information like names, birthdays, pets etc.", "red" ))
    
    elif score == 3:
        color = "yellow"
        print(colored(f"This password is safe for online usage.  Your password: \"{password}\"  -   Score: {score} out of 4.", "yellow"))
        print(colored(f"You could improve your password:","yellow"))
        
        if symbols == 1 or capital_letters == 1 or numbers == 1:
            print(colored(f"          - inserting uppercase letters, symbols or digits in the middle (Attackers know people often put Digits, Symbols and Uppercase Letters at beginning or end of the password.", "yellow" ))
        
        print(colored(f"          - Make a sentence that no one has ever said before like \"alienslikeracoonsanddrinkchewinggum\".", "yellow" ))
        print(colored(f"          - Avoid using passwords with personal information like names, birthdays, pets etc.", "red" ))
    
    else:
        color = "green"
        print(colored(f"Awesome password! Your password: \"{password}\"  -  Score 4/4.", "green"))
    
    suggestion_length = len(feedback["suggestions"])
    
    if (suggestion_length != 0):
            
        for item in feedback["suggestions"]:
            print(colored(f"          - "+ item, color))
    
def printLine():
    print("-" * 100)

def init_password_opt():

    """
        Method gives the user to choose one of two password policies to use or gives information about the different policies.
        
        @returns:
            pass_option: Integer : 1 or 2, 1 for min-strength + min-length Policie, 2 for blocklist + min-length policie
        """
    pass_option = 0
    check = 1
    
    while (check == 1):
        
        try:
            printLine()
            option_inp = int(input("With which password policies do you want to create the password?\n"
            "     Type \"1\" for minimum- strength + minimum length (recommended, only for online passwords!)\n"
            "     Type \"2\" for using blocklist + minimum length (only for online passwords!)\n"
            "     Type \"3\" for information what all these words mean\n"
            "     Your input:"))

            if(option_inp == 1 or option_inp == 2):
                check = 2
                pass_option = option_inp
            elif(option_inp == 3):
                check = 1
                printLine()
                print("Explanation: \n"
                "     \nMinimum Strength: a minimum guess number estimated for the password to be cracked.\n"
                "     \nMinimum Length: a minimum length the password must have.\n"
                "     \nBlocklists: These are wordlists, like Xato- wordlist or HaveIBeenPowned- API. If your password\n"
                "            matches one of the passwords in the list or is very similar to it the password\n"
                "            will be denied by the program.")
            else:
                check = 1
                print("WARNING: Only Integers 1, 2 and 3 are allowed.")
        
        except:
            print("WARNING: Only Integers 1, 2 and 3 are allowed.")

    respond_option = ""
    
    if (pass_option == 1): 
        respond_option = "minimum- strength + minimum length (recommended)"
        print(f"\n\nYou chose option [{pass_option}] {respond_option}")

    elif (pass_option == 2): 
        respond_option = "blocklist + minimum length (Recommandation: only for online passwords)"
        print(f"\n\nYou chose option [{pass_option}] {respond_option}")
    
    return pass_option

def print_requirements(option):
    """
        Method prints requirements before user inputs his password.
        @params:
            option      - Required: INT (1 or 2): if 1 min-strength mod requirements will be displayed, if 2 blocklist requirements will be displayed
        """
    
    print("-"*36 + "PASSWORD-REQUIREMENTS" + "-"*36)

    if option == 1:
        print(f"Your Online- Password should have a minimum-strength of: 10^6")
        print(f"Your Online- Password should have a minimum-length of: 10")

    if option == 2:
        print(f"Your Online- Password shouldnt appear in the Pwned Wordlist.")
    
        print(f"Your Online- Password should have a minimum-length of: 8")

def getPassword():
    """
        Method asks the user for a password input.
        @params:
            -
        @returns:
            password : String : The String with the password user chose.
        """
    pass_check = 1
    while (pass_check == 1):
            try:
                password_input = input("\nPlease type in your Password you want to check: ")
                printLine() 
                pass_check = 2      
            except:
                print("Something went wrong with typing in your Password.... Reapeating")


    return password_input

def checkStrength(password):

    """
        Method checks the password strength of it with zxcvbn library.
        @params:
            password  : str,required (Password to check with zxcvbn (String))
        @returns:
            list with 5 values. 
            - [0] is Score reaching from 0-4. 0 -> risky password (< 10^3), 1 -> very guessable (< 10^6), 2 -> guessable (< 10^8)
            3 -> safely unguessable (< 10^10), 4 -> very unguessable (> 10^10)
            - [1] is number of guesses neccessary to crack the password
            - [2] is Guesses Log10
            - [3] is time needed to crack the password (gives 4 Values)
            - [4] is feedback/suggestions to improve Password- Strength
        """

    result = zxcvbn(password)
    score = result["score"]
    number_of_guesses = result["guesses"]
    suggestion = result["feedback"]
    
    guess_log10 = result["guesses_log10"]
    crack_time = result["crack_times_display"]
    results = score, number_of_guesses, guess_log10, crack_time, suggestion
    return results

def check_pwned_databaseAPI(password):
    """
        Method checks if a given password is leaked on pwned database
        @params:
            password   - Required  : Password to check with pwned-API call (String)
        @returns:
            Boolean if password is in wordlist(True) or not(False)
        """
    get_hash = hashlib.sha1()
    get_hash.update(password.encode())
    sha1_password = get_hash.hexdigest()

    # calls haveibeenpwned API with the first 5 Bytes of Hash for range check
    pwned_API_results = requests.get("https://api.pwnedpasswords.com/range/" + sha1_password[:5])

    # gets last 35 chars of Hash for comparison with results of API- Call 
    comparison_hash = sha1_password[-35:].upper()
    result_hashes = pwned_API_results.text.split()

    password_in_pwned = False

    # compares every result hash from 
    for get_hash in result_hashes:
        if get_hash[:35]==comparison_hash:
            password_in_pwned = True
            print(f"Password Match found for Password {password} in Pwned Wordlist! Continue...")

    return password_in_pwned

def classCheck(check_pass):
    """
        Method calls checkClasses.py to check how many classes are in the password.
        @params:
            check_pass   - Required  : Password
        @returns:
            class_Check_array : List : with 5 values
                - [0]: Score from 0 - 3 for check_symbols (0: no symbols, 1: 1 symbol at start or end, 2: 1 symbol anywhere except start or end, 3: more than 1 symbols)
                - [1]: Score from 0 - 3 for check_capital_letters (0: no cap, 1: 1 cap at start or end, 2: 1 cap anywhere except start or end, 3: more than 1 cap)
                - [2]: Score from 0 - 3 for check_small_letters (0: no small, 1: 1 small at start or end, 2: 1 small anywhere except start or end, 3: more than 1 small)
                - [3]: Score from 0 - 3 for check_numbers (0: no numbers, 1: 1 number at start or end, 2: 1 number anywhere except start or end, 3: more numbers) 
                - [4]: Count of different Classes used in the password
        """
    classCheck_array = [check_symbols(check_pass), check_capital_letters(check_pass),
    check_small_letters(check_pass), check_numbers(check_pass), 0]

    classCounter = 0
    
    for item in classCheck_array:
        if item > 0: 
            classCounter += 1
        else:
            continue

    classCheck_array[4] = classCounter
    return classCheck_array

def check_symbols(testpass):
    """
        call Function to check whether
            - if there is a symbol used in the password
            - if its at beginning / or end of the password
            - if there are more than one symbol included in the password  
        @params:
            testpass     - Required  : String
        
        @returns:
            Returns Status Codes 0, 1, 2, 3
            - 0: No symbols used in the password.
            - 1: 1 symbol used, but at beginning or end of password
            - 2: 1 symbol used, not at beginning or end of password
            - 3: more than one symbol used in the password
        """
    regPattern_symbols = re.compile(r'[-!$%^&*()_+|#~=`{}@\[\]:"§;\'<>?,.\/]')
    matches_symbols = regPattern_symbols.findall(testpass)
    statusCode_symbols = 0

    if len(matches_symbols) > 1:
        statusCode_symbols = 3
    
    elif len(matches_symbols) == 1:
        
        if matches_symbols[0] == testpass[0] or matches_symbols[0] == testpass[len(testpass)-1]:
            statusCode_symbols = 1
        else:
            statusCode_symbols = 2    
    else:
        statusCode_symbols = 0
    print(f"{testpass} has checked Symbols score: {statusCode_symbols}")
    return statusCode_symbols

def check_capital_letters(testpass):
    """
        call Function to check whether
            - if there is a Capital Letter used in the password 
            - if its at beginning / or end of the password 
            - if there are more than one Capital Letter included in the password  
        @params:
            testpass     - Required  : String
        
        @returns:
            Returns Status Codes 0, 1, 2, 3
            - 0: No Capital Letters used in the password.  
            - 1: 1 Capital Letter used, but at beginning or end of password  
            - 2: 1 Capital Letter used, not at beginning or end of password
            - 3: more than one Capital Letter used in the password
        """
    
    regPattern_capital_letters = re.compile(r'[A-Z]')
    matches_capital_letters = regPattern_capital_letters.findall(testpass)
    statusCode_capital_letters = 0

    if len(matches_capital_letters) > 1:
        statusCode_capital_letters = 3
    
    elif len(matches_capital_letters) == 1:
        
        if matches_capital_letters[0] == testpass[0] or matches_capital_letters[0] == testpass[len(testpass)-1]:
            statusCode_capital_letters = 1
        else:
            statusCode_capital_letters = 2    
    else:
        statusCode_capital_letters = 0
    print(f"{testpass} has checked Capital letters score: {statusCode_capital_letters}")
    return statusCode_capital_letters

def check_small_letters(testpass):
    
    """
        call Function to check whether
            - if there is a small Letter used in the password
            - if its at beginning / or end of the password   
            - if there are more than one small Letter included in the password   
        @params:
            testpass     - Required  : String
        
        @returns:
            Returns Status Codes 0, 1, 2, 3
            - 0: No small Letters used in the password.   
            - 1: 1 small Letter used, but at beginning or end of password    
            - 2: 1 small Letter used, not at beginning or end of password
            - 3: more than one small Letter used in the password
        """
    
    regPattern_small_letters = re.compile(r'[a-z]')
    matches_small_letters = regPattern_small_letters.findall(testpass)
    statusCode_small_letters = 0

    if len(matches_small_letters) > 1:
        statusCode_small_letters = 3
    
    elif len(matches_small_letters) == 1:
        
        if matches_small_letters[0] == testpass[0] or matches_small_letters[0] == testpass[len(testpass)-1]:
            statusCode_small_letters = 1
        else:
            statusCode_small_letters = 2    
    else:
        statusCode_small_letters = 0
    print(f"{testpass} has checked Small letters score: {statusCode_small_letters}")
    return statusCode_small_letters

def check_numbers(testpass):
    """
        call Function to check whether
            - if there is a number used in the password 
            - if its at beginning / or end of the password  
            - if there are more than one number included in the password    
        @params:
            testpass     - Required  : String
        
        @returns:
            Returns Status Codes 0, 1, 2, 3
            - 0: No number used in the password.  
            - 1: 1 number used, but at beginning or end of password   
            - 2: 1 number used, not at beginning or end of password
            - 3: more than one number used in the password
        """
    
    
    regPattern_numbers = re.compile(r'[0-9]')
    matches_numbers = regPattern_numbers.findall(testpass)
    statusCode_numbers = 0

    if len(matches_numbers) > 1:
        statusCode_numbers = 3
    
    elif len(matches_numbers) == 1:
        
        if matches_numbers[0] == testpass[0] or matches_numbers[0] == testpass[len(testpass)-1]:
            statusCode_numbers = 1
        else:
            statusCode_numbers = 2    
    else:
        statusCode_numbers = 0
    print(f"{testpass} has checked Numbers score: {statusCode_numbers}")
    return statusCode_numbers

def leave_or_stay():
    """
        Asks the user if he wants to check another password or leave the program.
        @params:
            No params
        @returns:
            Boolean : True or False
        """ 
    check_leave = 1
    
    while (check_leave == 1):
        try:
            printLine()
            leave_inp = int(input("\n\nDo you want to create another Password or exit the program?\n     Type \"1\" for create another password\n     Type \"2\" for exit\n\n\nYour input:"))
            if(leave_inp == 1 or leave_inp == 2):
                check_leave = 2
                
            else:
                check_leave = 1
                print("WARNING: Only Integers 1 and 2 are allowed.")
        except:
            print("WARNING: Only Integers 1 and 2 are allowed.")

    respond_leave = ""
    if (leave_inp == 1): 
        respond_leave = "[1]: Create a new password."
    else: 
        respond_leave = "[2]: Program will be exited."
        print(figlet_format("EasyPass Alpha", font="slant"))
        print(figlet_format("     SAYS BYE", font="digital"))

    print(f"\n\nYou chose option {respond_leave}")
    printLine()
    


    if (leave_inp == 2): return True
    else: return False

def welcome():
    print(figlet_format("EasyPass Alpha", font="slant"))
    print(figlet_format("     Create safe and usable Passwords", font="digital"))