def isValid(title, author, year, pages, state):
    if(not isinstance(title, str)):
        raise ValueError("Title has to be a string")
    if(title == ""):
        raise ValueError("Book needs to have a title")
    if(not isinstance(author, str)):
        raise ValueError("Author has to be a string")
    if(author == ""):
        raise ValueError("Book needs to have an author")
    if(not isinstance(year, int) or year < 0):
        raise ValueError("Year has to be a positive integer")
    if(not isinstance(pages, int) or pages < 0):
        raise ValueError("Pages has to be a positive integer")
    if(not isinstance(state, str) and (state != "AVAILABLE" or state != "BORROWED")):
        raise ValueError("State has to be AVAILABLE OR BORROWED")
    return True
    
class Book():
    
    def __init__(self, title, author, year, pages, state) -> None:
        if(isValid(title, author, year, pages, state)):
            self.__title = title
            self.__author = author
            self.__year = year
            self.__pages = pages
            self.__state = state
            
    def prestar(self):
        if(self.__state == "BORROWED"):
            raise ValueError("Book is already borrowed")
        self.__state = "BORROWED"
        
    def devolver(self):
        if(self.__state == "AVAILABLE"):
            raise ValueError("Book is already available")
        self.__state = "AVAILABLE"
        
    def info(self):
        print("Título:", self.__title, ", autor:", self.__author, ", año:", self.__year, " , numero de paginas:", self.__pages, " , estado:", self.__state)
        
    def toLine(self):
        return "{},{},{},{},{}\n".format(self.__title, self.__author, self.__year, self.__pages, self.__state)
    
    def getPages(self):
        return self.__pages
    
    def getTitle(self):
        return self.__title
    
    def getAuthor(self):
        return self.__author
    
    def getYear(self):
        return self.__year
        
class Library():
    def __init__(self, books) -> None:
        self.__books = books
        
    def writeToFile(self, path_to_file):
        file = open(path_to_file, "a+")
        
        for book in self.__books:
            file.write(book.toLine())
        
        file.close()
        
    def addBook(self, book):
        self.__books.append(book)
        
    def findBooksByTitle(self, title):
        if(title == ""):
            raise ValueError("Book needs to have a title")
        if(not isinstance(title, str)):
            raise ValueError("Title has to be a string")
        return list(filter(lambda x : x.getTitle() == title, self.__books))
        
    def findBooksByAuthor(self, author):
        if(not isinstance(author, str)):
            raise ValueError("Author has to be a string")
        if(author == ""):
            raise ValueError("Book needs to have an author")
        return list(filter(lambda x : x.getAuthor() == author, self.__books))
    
    def totalPages(self):
        return sum([x.getPages() for x in self.__books])
    
    def average(self):
        if self.totalPages() == 0:
            return 0
        return self.totalPages() / len(self.__books)
    
    def numberOfBooksByYear(self, year):
        if(not isinstance(year, int) or year < 0):
            raise ValueError("Year has to be a positive integer")
        return len(list(filter(lambda x : x.getYear() == year, self.__books)))
    
    def show_books(self):
        print("----------------------------------------------\n")
        for book in self.__books:
            book.info()
            print("----------------------------------------------\n")
            
def buildBookFromLine(line):
    elements = line.split(",")
    return Book(elements[0], elements[1], int(elements[2]), int(elements[3]), elements[4])
    
library = Library([])

entrada = input("Elija si desea añadir un libro(ADD), cargar libros desde un fichero(LOAD), escribir los libros en un fichero(WRITE), listar los libros(SHOW) o si prefiere salir(EXIT). Tambien puede usar Media, Pages, Books in year, Search: ")

while(entrada != "EXIT"):
    
    match entrada:
        case "ADD":
            book_name = input("Introduzca el nombre del libro: ")
            book_author = input("Introduzca el autor del libro: ")
            book_year = int(input("Introduzca el año de publicación del libro: "))
            book_pages = int(input("Introduzca el número de páginas del libro: "))
            book_state = input("Introduzca el estado del libro(AVAILABLE, BORROWED): ")
            try:
                
                library.addBook(Book(book_name, book_author, book_year, book_pages, book_state))
                
            except Exception as e:
                print(e)
                
        case "LOAD":
            path_to_file = input("Introduzca ruta al archivo: ")
            try:
                file = open(path_to_file)
                
                lines = file.readlines()
                
                for line in lines:
                    if line != "\n":
                        library.addBook(buildBookFromLine(line))
                        
                file.close()
                    
            except FileNotFoundError as e:
                print(e)
            except Exception as e:
                print("Something went wrong while loading books from file")
                print(e)
            else:
                print("Library loaded")
        case "WRITE":
            path_to_file = input("Introduzca ruta al archivo: ")
            
            try:
                
                library.writeToFile(path_to_file)
            
            except FileNotFoundError as e:
                print(e)
            except Exception as e:
                print("Something went wrong while writing library")
                print(e)
            else:
                print("Library was written to file")
                
        case "SHOW":
            library.show_books()
            
        case "Media":
            print("Media de paginas entre los libros de la biblioteca: ", library.average())
            
        case "Pages":
            print("Total de páginas en los libros de la biblioteca: ", library.totalPages())
            
        case "Books in year":
            year = int(input("Introduzca el año en el que quiere saber cuantos libros se han publicado: "))
            print("Numero de libros publicados en el año ", year, ": ", library.numberOfBooksByYear(year))
            
        case "Search":
            option = input("Quieres buscar libros por titulo(TITULO) o por autor(AUTOR): ")
            if option == "TITULO":
                title = input("Titulo de los libros: ")
                books = library.findBooksByTitle(title)
                for book in books:
                    book.info()
                
            if option == "AUTOR":
                autor = input("Autor de los libros: ")
                books = library.findBooksByAuthor(autor)
                for book in books:
                    book.info()
                            
    entrada = input("Elija si desea añadir un libro(ADD), cargar libros desde un fichero(LOAD), escribir los libros en un fichero(WRITE), listar los libros(SHOW) o si prefiere salir(EXIT). Tambien puede usar Media, Pages, Books in year, Search: ")
    