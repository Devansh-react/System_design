from __future__ import annotations

from math import prod
from os import name
from pickle import LIST, NONE
from sys import implementation
from typing import List
from dataclasses import dataclass
from abc import ABC,abstractmethod


@dataclass
class product:
    name:str
    price:int


class shoppingCart:
    def __init__(self,Product: product) -> None:
        self.product  = List[Product] = []
        
    def addprodct(self,Product: product)->None:
        self.product.append(Product);

    def get_products(self) -> List[product]:
        return list(self._products)

    def calculate_total(self) -> float:
        return sum(p.price for p in self._products)


class ShoppingCartPrinter:
    def __init__(self, cart: shoppingCart) -> None:
        self._cart = cart

    def print_invoice(self) -> None:
        print("Shopping Cart Invoice:")
        for p in self._cart.get_products():
            print(f"{p.name} - Rs {p.price}")
        print(f"Total: Rs {self._cart.calculate_total()}")

class presistace_DB(ABC):
    @abstractmethod
    def save(self,cart: shoppingCart)->None:
        raise NotImplementedError
    
class save_to_MongoDB(presistace_DB):
    def save(self,cart: shoppingCart,)->None:
        print(f"save to mongodb")
           
class save_to_postgress(presistace_DB):
    def save(self,cart: shoppingCart)->None:
        print(f"save to postgress")

class save_to_file(presistace_DB):
    def save(self,cart: shoppingCart)->None:
        print(f"save to file")

def main()->None:
    
    product1 = product("item1",789)
    product2= product("item2",456)
    cart.addprodct(product1)
    cart.addprodct(product2)
    cart = shoppingCart(product)
    
    cart.calculate_total()
    save = save_to_MongoDB()
    save.save()
    save2 = save_to_file
    save2.save



if __name__ == "__main__":    
    main()




















