import json
import os
from typing import List, Dict, Optional

class Book:
    """Class to represent a book in the library"""
    def __init__(self, title: str, author: str, year: int, genre: str, read: bool = False):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.read = read
    
    def to_dict(self) -> Dict:
        """Convert book object to dictionary"""
        return {
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'genre': self.genre,
            'read': self.read
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Book':
        """Create book object from dictionary"""
        return cls(
            title=data['title'],
            author=data['author'],
            year=data['year'],
            genre=data['genre'],
            read=data['read']
        )
    
    def __str__(self) -> str:
        read_status = "Read" if self.read else "Unread"
        return f"{self.title} by {self.author} ({self.year}) - {self.genre} - {read_status}"

class LibraryManager:
    """Class to manage the personal library"""
    def __init__(self, data_file: str = 'library_data.json'):
        self.books: List[Book] = []
        self.data_file = data_file
        self.load_library()
    
    def add_book(self, book: Book) -> None:
        """Add a book to the library"""
        self.books.append(book)
        self.save_library()
    
    def remove_book(self, title: str) -> bool:
        """Remove a book by title"""
        for i, book in enumerate(self.books):
            if book.title.lower() == title.lower():
                del self.books[i]
                self.save_library()
                return True
        return False
    
    def search_books(self, search_term: str, search_by: str = 'title') -> List[Book]:
        """Search books by title or author"""
        search_term = search_term.lower()
        if search_by == 'title':
            return [book for book in self.books if search_term in book.title.lower()]
        elif search_by == 'author':
            return [book for book in self.books if search_term in book.author.lower()]
        else:
            return []
    
    def get_all_books(self) -> List[Book]:
        """Get all books in the library"""
        return self.books
    
    def get_statistics(self) -> Dict[str, float]:
        """Get library statistics"""
        total_books = len(self.books)
        read_books = sum(1 for book in self.books if book.read)
        percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
        return {
            'total_books': total_books,
            'percentage_read': percentage_read
        }
    
    def save_library(self) -> None:
        """Save library data to file"""
        data = [book.to_dict() for book in self.books]
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_library(self) -> None:
        """Load library data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(book_data) for book_data in data]
            except (json.JSONDecodeError, FileNotFoundError):
                self.books = []
        else:
            self.books = []

def display_menu() -> None:
    """Display the command-line menu"""
    print("\nPersonal Library Manager")
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics")
    print("6. Exit")

def get_book_input() -> Book:
    """Get book details from user input"""
    title = input("Enter the book title: ").strip()
    author = input("Enter the author: ").strip()
    year = int(input("Enter the publication year: "))
    genre = input("Enter the genre: ").strip()
    read = input("Have you read this book? (yes/no): ").strip().lower() == 'yes'
    return Book(title, author, year, genre, read)

def command_line_interface() -> None:
    """Run the command-line interface"""
    manager = LibraryManager()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            # Add a book
            book = get_book_input()
            manager.add_book(book)
            print("Book added successfully!")
        
        elif choice == '2':
            # Remove a book
            title = input("Enter the title of the book to remove: ").strip()
            if manager.remove_book(title):
                print("Book removed successfully!")
            else:
                print("Book not found in the library.")
        
        elif choice == '3':
            # Search for a book
            print("Search by:")
            print("1. Title")
            print("2. Author")
            search_choice = input("Enter your choice (1-2): ").strip()
            
            if search_choice in ('1', '2'):
                search_by = 'title' if search_choice == '1' else 'author'
                search_term = input(f"Enter the {search_by} to search for: ").strip()
                results = manager.search_books(search_term, search_by)
                
                if results:
                    print("\nMatching Books:")
                    for i, book in enumerate(results, 1):
                        print(f"{i}. {book}")
                else:
                    print("No matching books found.")
            else:
                print("Invalid choice.")
        
        elif choice == '4':
            # Display all books
            books = manager.get_all_books()
            if books:
                print("\nYour Library:")
                for i, book in enumerate(books, 1):
                    print(f"{i}. {book}")
            else:
                print("Your library is empty.")
        
        elif choice == '5':
            # Display statistics
            stats = manager.get_statistics()
            print(f"\nTotal books: {stats['total_books']}")
            print(f"Percentage read: {stats['percentage_read']:.1f}%")
        
        elif choice == '6':
            # Exit
            print("Library saved to file. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    command_line_interface()