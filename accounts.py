# COMP 517 Continuos Assessment 2
# Name : Kevin John Mathew
# Student ID : 201591357

import random
import datetime

# The purpose of this class is to conduct all user operations related to a Basic Account
# This class stores a list of card numbers to help with generating unique card numbers along with card deatils,
# account number, account holders name and available balance
# This class provides services such as depositing and withdrawing money, issuing new card details,
# printing balance and closing the account 

class BasicAccount :
    acNum = 0
    cardsList = []
    def __init__(self, name, openingBalance):
        self.name = name
        self.balance = openingBalance
        BasicAccount.acNum += 1
        self.acNum = BasicAccount.acNum
    
    def __str__(self):
        return f'Account owner name is {self.name} and account number is {self.acNum} and balance is {self.balance}'


    # deposits money into the user account
    def deposit(self, amount):
        self.amount = amount
        if self.amount > 0 :
            self.balance = self.balance + self.amount
        else :
            print("Please enter an amount greater than 0")

        # check overdraft state if premium account after deposit is made
        if type(self) == PremiumAccount:
            if self.balance < 0:
                self.overdraft = True
            else:
                self.overdraft = False


    # withdraws money from the user account if all conditions are satisfied
    def withdraw(self, amount):
        self.amount = amount
        if type(self) == BasicAccount:
            if self.amount > self.balance:
                print("Can not withdraw £{}".format(self.amount))
            else: 
                self.balance = self.balance - self.amount
                print("{} has withdrawn £{}. New balance is £{}".format(self.name, self.amount, self.balance))
        else:
            self.overallBalance = self.balance + self.overdraftLimit
            if self.amount > self.overallBalance:
                print("Can not withdraw £{}".format(self.amount))
            else:
                self.balance -= self.amount
                if self.balance < 0:
                    self.overdraft = True
                else :
                    self.overdraft = False   
                print("{} has withdrawn £{}. New balance is £{}".format(self.name, self.amount, self.balance))


    # issues new card details including new card number and card expiry date 
    def issueNewCard(self):
        while True:
            randomCardNum = ' '.join([str(random.randint(0, 9999)).zfill(4) for _ in range(4)])
            self.cardNum = str(randomCardNum.replace(" ",""))
            if self.cardNum not in BasicAccount.cardsList:
                BasicAccount.cardsList.append(self.cardNum)
                break
        # expiry month will be same as current month    
        expiryMonth = datetime.datetime.now().month
        expiryDate =  datetime.datetime.now() + datetime.timedelta(days=1095)
        expiryYear = int(expiryDate.strftime("%y"))
        self.cardExp = (expiryMonth, expiryYear)
        print('Card Number : {}'.format(self.cardNum))
        print('Card Expiry : {}'.format(self.cardExp))


    # returns available balance in user account
    def getAvailableBalance(self):
        return float(self.balance)


    # returns balance in user account
    def getBalance(self):
        return float(self.balance)


    # prints balance in user account
    def printBalance(self):
        print('Your current account balance is : £{}'.format(self.balance))


    # returns account holders name
    def getName(self):
        return str(self.name)


    # returns account number
    def getAcNum(self):
        return str(self.acNum)


    # closes the account of the user after conditions are checked
    def closeAccount(self):
            if(self.balance < 0):
                print("Can not close account due to customer being overdrawn by £{}".format(abs(self.balance)))
                return False
            else:
                self.withdraw(self.balance)
                return True



# The purpose of this class is to conduct all user operations related to a Premium Account
# This class stores the overdraft limit of the account and the state of the overdraft
# This class provides services such as setting a new overdraft limit, depositing and withdrawing money,
# issuing new card details, printing the account balance and closing the account

class PremiumAccount(BasicAccount):

    def __init__(self, name, openingBalance, initialOverdraft):
        BasicAccount.__init__(self,name,openingBalance)
        self.overdraftLimit = initialOverdraft
        self.overdraft = False

    def __str__(self):
        return f'Account owner name is {self.name} and has overdraft limit of £{self.overdraftLimit} and the account balance is £{self.balance}'


    # sets the new overdraft limit for the user
    def setOverdraftLimit(self, newLimit):      
        self.overdraftLimit = newLimit
       

    # returns the available balance
    def getAvailableBalance(self):
        return float(self.balance + self.overdraftLimit)


    # prints the account balance   
    def printBalance(self):
        if(self.overdraft == True):
            print("Your current account balance is £{} \n Overdraft can be taken upto £{} and your overdraft balance is £{}".format(self.balance,self.overdraftLimit, self.balance + self.overdraftLimit)) 
        else:
            print("Your current account balance is £{} \n Your overdraft balance and limit is {}".format(self.balance, self.overdraftLimit))


    # closes the account after checking if the user has any current overdraft
    def closeAccount(self):
            if(self.overdraft == True):
                print("Can not close account due to customer being overdrawn by £{}".format(abs(self.balance)))
                return False
            else:
                self.withdraw(self.balance)
                return True
