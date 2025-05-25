import time
import functools
from dataclasses import dataclass

def myDecorator(function):

    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)
        print("i am in the middle")
        return value

    return wrapper

@myDecorator
def hello_world(person):
    return "Hello, World!", person

hey = hello_world("mike")

## Example #1 Logging Decorator

def logging(function):
    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)
        with open("logfile.txt", "a+") as f:
            fname = function.__name__
            print(f"{fname} returned {value}")
            f.write(f"{fname} returned {value}\n")
        return value
    return wrapper

@logging
def add(x, y):
    return x + y

## Example #2 Timing

def timing(function):
    def wrapper(*args, **kwargs):
        start = time.time()
        value = function(*args, **kwargs)
        end = time.time()
        fname = function.__name__
        print(f"{fname} took {end - start} seconds to run")
        return value
    return wrapper

@timing
def check_numbers(x, y):
    for i in range(x - y, 1, 10):
        print(i)


## Useful Examples
# Property, to control the access to an attribute
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value >= 0:
            self._radius = value
        else:
            raise ValueError("Radius cannot be negative")
        
    @property
    def diameter(self):
        return self._radius * 2
    
    @radius.deleter
    def radius(self):
        del self._radius


# STATICMETHOD
class Math:
    @staticmethod
    def add(x, y):
        return x + y
    
    @staticmethod
    def multiply(x, y):
        return x * y

# CLASSMETHOD
class Person:
    species = "HOMO sapiens"

    @classmethod
    def get_species(cls):
        return cls.species
    
# functools-cache
@functools.cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# dataclass
@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0

    def total_cost(self):
        return self.price * self.quantity

ice = Product("ice cream", 12.00, 100)
print(ice.name)
print(ice.total_cost())