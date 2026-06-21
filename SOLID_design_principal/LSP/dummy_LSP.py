from __future__ import annotations

from abc import ABC, abstractmethod
from logging import raiseExceptions
from nt import error
from typing import List, Self

# parent_class
class non_withdraw_account(ABC):
    @abstractmethod
    def deposit(self,amount:int)->None:
        pass
# child class
class withdraw_account(non_withdraw_account,ABC):
    @abstractmethod
    def withdraw(self,ammount:int)->None:
        pass
        
        
    
    
class Savings_account(withdraw_account):
    def __init__(self,balance) -> None:
        self.balance = balance
    
    def deposit(self,amount:int)->None:
        self.balance += amount 
    def withdraw(self,amount:int)->None:
        if(self.balance>=amount):
            self.balance -= amount
            print(f"withdraw the amount {amount} , balance left{self.balance}")
        else:
            raise error("Insufficient_funds")
    
class Current_account(withdraw_account):
    def __init__(self,balance) -> None:
        self.balance = balance
    
    def deposit(self,amount:int)->None:
        self.balance += amount 
    def withdraw(self,amount:int)->None:
        if(self.balance>=amount):
            self.balance -= amount
            print(f"withdraw the amount {amount} , balance left{self.balance}")
        else:
            raise error("Insufficient_funds")

class FD_account(non_withdraw_account):
    def __init__(self,balance) -> None:
        self.balance = balance
    
    def deposit(self,amount:int)->None:
        self.balance += amount 
        print(f"{amount} is deposited in the FD")



class bank():
    def __init__(self,withdrawable: List[withdraw_account],non_withdrawable: List[non_withdraw_account]) -> None:
        self.withdrawable_account = withdrawable
        self.non_withdrawable_accounts = non_withdrawable
        
    #  a function that deposit and witdraw 1000 and 500 respectively from respective account 
    def transaction_procress(self,account_list1:withdraw_account,account_list2:non_withdraw_account)->None:
        for acc in account_list1:
            acc.deposit(1000)
            acc.withdraw(500)
            
        for acc in account_list2:
            acc.deposit(1000)
        


            
            
def main()->None:
    withdraw_acc_List = List[withdraw_account]=[Savings_account(),Current_account()]
    non_withdraw_acc_List = List[non_withdraw_account] = [FD_account()]
    
    back_sys = bank(withdraw_acc_List,non_withdraw_acc_List)
    back_sys.transaction_procress()
    
    











