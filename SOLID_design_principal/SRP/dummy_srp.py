from __future__ import annotations
from dataclasses import dataclass
from os import name
from  typing import  List, Self



@dataclass
class product:
    name:str
    price:int

class shoppingcart :
    def __init__(self)->None:
        self.product = List[product]=[]
        
    def add_product(self,item:product)->None:
        self.product.append(item)
        
    def get_product(self)->List[product]:
        return List[product](Self.product)
    
    def cal_total(self)->float:
        total = sum(p.price for p in product)
        return total
    
class shoopping_Database:
    def __init__(self,cart:shoppingcart) -> None:
        self.cart = cart
    
    def save_cart_(self)->None:
        self.save_cart_
        print("Saving shopping cart to database...")
    
class cart_print:
    def __init__(self,cart:shoppingcart) -> None:
        self.cart = cart
    
    def print_invoice (self)->None:
        for p in self.cart.get_product():
            print(f"product->{p.name}->price:{p.price}")
        print(f"Total: Rs {self._cart.calculate_total()}")
        
def main()-> None:
    product1 = product("Laptop",50000)
    product2 = product("Mobile",41520)
    product3 = product("Mobile_iphone",51520)
    
    cart = shoppingcart()
    cart.add_product(product1)
    cart.add_product(product2)
    cart.add_product(product3)
    print = cart_print(cart)
    save_to_db = shoopping_Database(cart)
    
    
    cart.cal_total()
    print.print_invoice()
    save_to_db.save_cart_()
    
    
    if __name__  == "__main__":
        main()
    
    




























    
    
    