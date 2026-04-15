# LIBRARY MANAGEMENT SYSTEM


class LibraryItem:

    def __init__(self,title,author,availability=True):
        self.title = title
        self.author = author
        self.availability = availability


    #Checking item availability
    def item_available(self):
        if(self.availability==True):
            return "Item is available"
        else:
            return "Item is not available"


    def __str__(self):
        return f"Book {self.title} written by {self.author}"
    
# Function to validate titles and authors
def validate_titles_or_authors(word):
    if word == "":
        return "Title/Author name can't be empty"
    return None


 
#Creating Book class which inherits the LibraryItem class
class Book(LibraryItem):
    def __init__(self,title, author, ISBN):
        super().__init__(title, author)
        self.ISBN=ISBN

    # Print the ISBN number
    def __str__(self):
        return f"{super().__str__()} \nISBN number of the book is {self.ISBN}"



    #Function to allow user to borrow book
    def borrow_book(self):
        if(self.availability==True):
            self.availability=False
            return f"Book borrowed successfully"
        else:
            return f"Book is not available"
       


    #Function to allow user to return book
    def return_book(self):
        if(self.availability==False):
            self.availability=True
            return f"Book returned successfully"
        else:
            return f"Book is already in the library"
    

# Function to check validation of 10-digit ISBN
def is_valid_ISBN_10(ISBN :str):
    if len(ISBN)!=10:
        return False
    

    total=0
    for i in range(9):
        if not ISBN[i].isdigit():
            return False
        total+=(i+1)*int(ISBN[i])

    if ISBN[9]=="X":
        total+=10*10
    elif ISBN[9].isdigit():
        total+=10*int(ISBN[9])
    else:
        return False
    
    return total%11==0


# Function to check validation of 13-digit ISBN
def is_valid_ISBN_13(ISBN:str):
    if len(ISBN)!=13 or not ISBN.isdigit():
        return False
    total=0
    for i in range(12):
        digit=int(ISBN[i])
        if i%2==0:
            total+=digit
        else:
            total+=3*digit

    check_digit=(10-(total%10))%10
    return check_digit==int(ISBN[12])



# Function to format ISBN and check validity
def validate_ISBN(ISBN:str):
    isbn=ISBN.replace("-","").replace(" ","")
    if len(isbn)==10:
        return "Valid ISBN-10" if is_valid_ISBN_10(isbn) else "Invalid ISBN-10"
    elif len(isbn)==13:
        return "Valid ISBN-13" if is_valid_ISBN_13(isbn) else "Invalid ISBN-13"
    else:
        return "Invalid ISBN format"
    


class User:

    def __init__(self,name,user_id,borrowed_books=None):        
        self.name=name
        self.user_id=user_id
        self.borrowed_books=borrowed_books if borrowed_books is not None else []         


    #Function to add borrowed book in the user borrowed book list
    def add_borrowed_book(self, book):
        if not book in self.borrowed_books:
            self.borrowed_books.append(book)
            return "Book borrowed successfully"
        else:
            return "Book is already borrowed"

    #Function to remove borrowed book from the user borrowed book list
    def remove_borrowed_book(self, book):
       self.borrowed_books.remove(book)
       return "Book removed successfully"

    #Function to display all borrowed books by the user
    def display_borrowed_books(self):
        if len(self.borrowed_books)==0:
            return f"{self.name} has not borrowed any of the books"
        else:
           book_info ="\n".join(str(book) for book in self.borrowed_books)
           return f"Books borrowed by {self.name}:\n{book_info}"


    #Function to allow user to borrow book
    def borrow_book(self, book):
        if book.availability:
            book.availability = False
            self.add_borrowed_book(book)
            return f"{self.name} borrowed {book.title}"
        else:
            return f"{book.title} is not available"


    #Function to allow user to return book
    def return_book(self, book):
        if book in self.borrowed_books:
            book.availability = True
            self.remove_borrowed_book(book)
            return f"{self.name} returned {book.title}"
        else:
            return f"{self.name} did not borrow {book.title}"



#Creating book list present in the library
book_list=[]
def add_book(book):
    book_list.append(book)
    return "Book added successfully"



#Creating user list
user_list=[]
def add_user(user):
    user_list.append(user)
    return "User added successfully"




# Function to search book by title
def search_books_by_title(title):
    for book in book_list:
        if book.title.lower()==title.lower():
            return book
    return None



# Function to find books by a particular author and store them in the list
def find_books_by_author(author):
    books_by_author=[]
    for book in book_list:
        if book.author==author:
            books_by_author.append(book)
    return books_by_author


# Function to find user by ID
def search_user_by_id(user_id):
    for user in user_list:
        if user.user_id==user_id:
            return user
    return None



# Function to get all available books, not borrowed
def get_available_books():
    available_books = []
    for book in book_list:
        if book.availability == True:
            available_books.append(book)
    return available_books



# Function to count total number of books and available books
def count_books():
    total=len(book_list)
    available=len(get_available_books())
    print(f"Total number of books: {total}")
    print(f"Number of available books: {available}")


# Function to display all books in the library
def display_all_books():
    if len(book_list)==0:
        print("No books in the library")        #not using return because in the else block, loop is there 
    else:
        for book in book_list:
            print(f"Book Title: {book.title}, Author: {book.author}, Available: {book.availability} \n")


# Function to display user  and their borrowed books
def display_users_and_books():
    if len(user_list)==0:
        return "No users in the library"
    else:
        for user in user_list:
            print(f"User Name: {user.name}, User ID: {user.user_id}")
            user.display_borrowed_books()


# Function to save books to a file
def save_books_to_file(filename):
    try:
        with open(filename, "w") as file:
            for book in book_list:
                file.write(f"{book.title}|{book.author}|{book.isbn}|{book.availability}\n")
        return "Books saved successfully"
    except OSError as e:
        return f"Error saving books: {e}"

# Function to load books from file
def load_books_from_file(filename):
    try:
        with open(filename, "r") as file:
            for line in file:
                title, author, isbn, availability = line.strip().split("|")
                book = Book(title, author, isbn)
                book.availability = availability == "True"
                book_list.append(book)
        return "Books loaded successfully"
    except FileNotFoundError:
        return "File not found"
    except ValueError:
        return "Error in file format"




# Function to provide the options to the user
if __name__=="__main__":
    def Menu_display():
        print("\n=== Library Menu ===")
        print("1. Add  a new Book")
        print("2. View all  Books")
        print("3. Search for a  Book  by title")
        print("4. Add a new user ")
        print("5. View all users")
        print("6. Allow user to borrow a book")
        print("7. Allow user to return a book")
        print("8. Save data to file")
        print("9. Load data from file")
        print("10. Count total books")
        print("11. Search for a book by author")
        print("12. Exit")


    while True:
        Menu_display()
        choice=int(input("Enter your choice: "))
        try:
            if choice==1:
                # Add a new book
                title=input("Enter book title: ")
                author=input("Enter book author: ")
                ISBN=input("Enter book ISBN: ")
                book=Book(title,author,ISBN)
                add_book(book)
                print("Book added successfully!")


            elif choice==2:
                #View all books
                display_all_books()


            elif choice==3:
                #Search for a book by title
                title=input("Enter book title to search: ")
                book=search_books_by_title(title)
                if book:
                    print(f"Found: {book}")
                    print(f"Availability: {book.item_available()}")
                else:
                    print("Book not found.")


            elif choice==4:
                # Add new user
                name=input("Enter user name: ")
                user_ID=input("Enter user ID: ")
                user=User(name,user_ID)
                add_user(user)
                print("User added successfully!")


            elif choice==5:
                #View all users
                display_users_and_books()


            elif choice==6:   
                #Allow user to borrow a book
                user_id=input("Enter user ID: ")
                book_title=input("Enter book title: ")
                user=search_user_by_id(user_id)
                book=search_books_by_title(book_title)
                if user and book:
                    print(user.borrow_book(book))
                    
                else:
                    print("User or Book not found.")



            elif choice==7:    
                #Allow user to return a book
                user_id=input("Enter user ID: ")
                book_title=input("Enter book title: ")
                user=search_user_by_id(user_id)
                book=search_books_by_title(book_title)
                if user and book:
                    print(user.return_book(book))
                    
                else:
                    print("User or Book not found.")


            elif choice==8:
                #Save data to file
                filename=input("Enter filename to save data: ")
                save_books_to_file(filename)


            elif choice==9:
                #Load data from file
                filename=input("Enter filename to load data: ")
                load_books_from_file(filename)


            elif choice==10:
                #Count total books
                count_books()




            elif choice==11:
                #Search for books by author nae
                author=input("Enter author name to search: ")
                books=find_books_by_author(author)
                print(books)

            elif choice==12:
                print("Exiting...")
                break


            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print("An error occurred:", e)

            