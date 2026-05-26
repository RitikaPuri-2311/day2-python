from packages.module1 import add, divide, factorial
from packages.module2 import reverse_string, count_vowels
from packages.module3 import write_file, read_file
from packages.config import APP_NAME


print("Application Name:", APP_NAME)

print(add(10, 20))

print(divide(10, 2))

print(factorial(5))

print(reverse_string("Python"))

print(count_vowels("Programming"))

print(write_file("test.txt", "Hello Python"))

print(read_file("test.txt"))