## Super/parent class that prints in nice required format and also checks for dups and calculates the age of book
class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"

    def __eq__(self, other):
        return self.title == other.title and self.author == other.author

    def age(self, current_year):
        return current_year - self.year

## below sub/child class Ebook for super class Book which has additional attribute size_mb to calculate download time in seconds
class EBook(Book):
    def __init__(self, title, author, year, size_mb):
        super().__init__(title, author, year)
        self.size_mb = size_mb

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year}) [{self.size_mb} MB]"

    def download_seconds(self, mbit_per_s):
        return round((self.size_mb * 8) / mbit_per_s, 1)

## this stores the books list, add books, find author , no.of books, oldest book
class Library:
    def __init__(self):
        self.books = []

    def add(self, book):
        if book in self.books:
            print(f"Duplicate book ignored: {book}")
            return
        else:
            self.books.append(book)
        print(f"Book added: {book}")

    def find_by_author(self, author):
        return [book for book in self.books if book.author == author]
    
    def oldest(self):
        oldest_book = self.books[0]

        for book in self.books:
            if book.year < oldest_book.year:
                oldest_book = book

        return oldest_book

    def __len__(self):
        return len(self.books)


from datetime import datetime

print("Demo.... ")

print("\nAdding books......... ")

b1 = Book("1984", "George Orwell", 1949)
b2 = Book("Core Python Programming", "R. Nageswara Rao", 2007)
b3 = Book("Robotics, Vision and Control", "Peter Corke", 2011)
b4 = Book("Coming Up for Air", "George Orwell", 1939)
e1 = EBook("Python Basics", "John Smith", 2020, 25)
e2 = EBook("Data Science", "Jane Doe", 2022, 40)

duplicate = Book("1984", "George Orwell", 1950)

lib = Library()

lib.add(b1)
lib.add(b2)
lib.add(b3)
lib.add(b4)
lib.add(e1)
lib.add(e2)
lib.add(duplicate)  # ignored

print("\nTesting......... ")

print(f"\nAge of {b1} : ", b1.age(datetime.now().year)) ## to get current year I used datetime.now() or we can hardcode as 2026

print(f"\nDownload time of {e1} : ", e1.download_seconds(20), "seconds")

print("\nBooks by George Orwell:")
for book in lib.find_by_author("George Orwell"):
    print(book)

print("\nOldest book : " ,lib.oldest())

print("\nNumber of books in library : ", len(lib))

print("\nAll books in library :")
for book in lib.books:
    print(book)
