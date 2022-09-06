import helperFunctions as helper

checkExit = False
helper.welcome()

while(checkExit is False):

    option = helper.init_password_opt()

    password_bool = False

    while password_bool is False:

        helper.print_requirements(option)
        password = helper.getPassword()
        strengthResults = helper.checkStrength(password)

        password_bool = False
        lengthBool = False
        strengthBool = False
        pwnedBool = True

        
        if option == 1:
            if len(password) > 9: 
                lengthBool = True
                print(f"{len(password)}")
                print("Your Password met the length check!")
            else: 
                lengthBool = False
                print("Your Password doesnt met the length check!")
            if strengthResults[2] >= 6: 
                strengthBool = True
                print("Your password met the strength check!")
            
            if lengthBool is True and strengthBool is True:
                    password_bool = True
            else: 
                print("Password Requirements not met! Reapeat....")
                continue

        elif option == 2: 
            if len(password) > 7: 
               lengthBool = True
               print("Your Password met the length check!")
            else:
                lengthBool = False
                print("Your Password doesnt met the length check!")
            pwnedBool = helper.check_pwned_databaseAPI(password)
            if pwnedBool is False: print("Your Password wasnt found in haveibeenpwned databse!")
            if lengthBool is True and pwnedBool is False: password_bool = True
            else: 
                print("Password Requirements not met! Reapeat....")
                continue
        
        if (password_bool is True):
            print("Password Requirements met!")
            classCheck = helper.classCheck(password)
            helper.feedback(strengthResults[0], strengthResults[1], strengthResults[2], strengthResults[3], strengthResults[4], 
            classCheck[0], classCheck[1], classCheck[2], classCheck[3], classCheck[4], password)
            checkExit = helper.leave_or_stay()






