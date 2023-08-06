import xlwings as wings

class simpleCalculator:
    def __init__(self, bookName, sheetName, inputCell, outputCell):
        self.bookName = bookName
        self.sheetName = sheetName
        self.inputCell = inputCell
        self.outputCell = outputCell
        try:
            book = wings.Book(self.bookName)
        except OSError:
            bookName = bookName.split('\\', -1)[-1]
            book = wings.Book(bookName)   
        sheet = book.sheets[self.sheetName]
        self.book = book
        self.sheet = sheet
        
    def calculate(self, input):
        self.__writeData(input)
        output = self.__readData()
        return output
    
    def __writeData(self, input):
        for n in range(len(input)):
            self.sheet.range(self.inputCell[n]).value = input[n]
        
    def __readData(self):
        data = self.sheet.range(self.outputCell).value
        return data

class advancedCalculator:  
    def __init__(self, inputBookName, inputSheetName, inputCell, outputBookName, outputSheetName, outputCell):
        self.inputBookName = inputBookName
        self.inputSheetName = inputSheetName
        self.inputCell = inputCell
        self.outputBookName = outputBookName
        self.outputSheetName = outputSheetName
        self.outputCell = outputCell
        try:
            inputBook = wings.Book(self.inputBookName)
        except OSError:
            inputBookName = inputBookName.split('\\', -1)[-1]
            inputBook = wings.Book(inputBookName)   
        inputSheet = inputBook.sheets[self.inputSheetName]
        self.inputBook = inputBook
        self.inputSheet = inputSheet
        try:
            outputBook = wings.Book(self.outputBookName)
        except OSError:
            outputBookName = outputBookName.split('\\', -1)[-1]
            outputBook = wings.Book(outputBookName)   
        outputSheet = outputBook.sheets[self.outputSheetName]
        self.outputBook = outputBook
        self.outputSheet = outputSheet
        
    def calculate(self, input):
        self.__writeData(input)
        output = self.__readData()
        return output
        
    def __writeData(self, input):
        for n in range(len(input)):
            self.inputSheet.range(self.inputCell[n]).value = input[n]
        
    def __readData(self):
        data = self.outputSheet.range(self.outputCell).value
        return data