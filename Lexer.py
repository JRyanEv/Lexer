# CS 4337.502
# Project Part 1
# Python Lexer

# James Ryan Evans
# JRE170001@utdallas.edu

import codecs
import sys
import re

lineNumber = 1; #Keep track of Line Number for Input
errorID = 9 #Identify Error

allOperations = ['=', '>', '<', '!', ';', '+', '-', '*', '/'] #All operations available
allLexemes = ["for", "get", "printf", "if", "else"] #All Lexmes available

def slashBackslash(inSlash): #Works with backshlash inputs for strings 
    string_elem = inSlash.group(0)
    return string_elem.replace("\\", "")

def stringLexer(inString): #Handles Strings inputs
    i = 0
    while i < len(inString):
        i += 1
        if inString[i] == "\"":
            if inString[i-1] == "\\":
                continue
            else: 
                break
        elif inString[i] == ";":
            return [[errorID, " Invalid String Format. " + "Found on Line: " + str(lineNumber)], inString]
        
    workString = u"".join(inString[1:i])
    workString = workString.replace(u"\n", "\n")
    workString = workString.replace(u"\t", "\t")
    workString = workString.replace(u"\"", "\"")
    workString = workString.replace(u"\\", "\\")
    workString = re.sub(u"\\[^\s]", slashBackslash, workString)
    
    return [[ workString], input[i+1:]]

def checkLexerID(lex): #token ID and Lexer
    patternID = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*")

    if patternID.fullmatch(lex):
        return [lex]
    else: 
        print(lex)
        return [errorID, " Invalid ID Format. " + "Found on Line: " + str(lineNumber)]

def find(lex): #find the function
   
    if lex in allLexemes:
        return [lex]
    else:
        return checkLexerID(lex) #return to token ID and Lexer
    
def checkCharacter(check): #token ID
    return check.isdigit() or check.isalpha() or check == "_"
       
def lexerInteger(inInt, symbol): #Integer Values
    i = 0
    while not inInt[i].isspace() and i < len(inInt):
        if inInt[i].isdigit():
            i += 1
        elif inInt[i] in allOperations:
            break
        else:
            return[[errorID, " Invalid Integer Format. " + "Found on Line: " + str(lineNumber)], inInt]
    return [[symbol*int("".join(inInt[0:i]))], inInt[i:]]

def keyLexerID(inLex, onlyId = False): #token ID and string parser for lexemes
    i = 0
    while i < len(inLex) and checkCharacter(inLex[i]):
        i += 1
    if onlyId:
        return [checkLexerID("".join(inLex[0:i])), inLex[i:]]
    return [find("".join(inLex[0:i])), inLex[i:]] 

def lexer(inAll): #Lexer Function
    global lineNumber 
    i = 0
    while inAll[i].isspace() and i < len(inAll): #whitespaces
        if inAll[i] == "\n":
            lineNumber = lineNumber + 1
        i += 1
        
    if i >= len(inAll): #End of File Check
        return [[5, ""], inAll]
    
    inAll = inAll[i:] #whitespaces

    #parsing:[=, ;, !, >, <, int, (, ), _, \, ,, /, -, *, +, whitespace, exceptions]
    if inAll[0] == "=": 
        if inAll[1] == "=" and len(inAll) > 1:
            return [["=="], inAll[2:]]
        else:
            return [["="], inAll[1:]]

    elif inAll[0] == ";":
        return [[";"], inAll[1:]]
    
    elif inAll[0] == "!": 
        if len(inAll) > 1 and inAll[1] == "=":
            return [["!="], inAll[2:]]
        else:
            return [[errorID, " Invalid '!' Format, '!' is expected before '='. " + "Found on Line: " + str(lineNumber)], inAll]  

    elif inAll[0] == ">":
        if len(inAll) > 1 and inAll[1] == "=":
            return [[">="], inAll[2:]]
        else:
            return [[">"], inAll[1:]]
  
    elif inAll[0] == "<":
        if len(inAll) > 1 and inAll[1] == "=":
            return [["<="], inAll[2:]]
        else:
            return [["<"], inAll[1:]]
   
    elif inAll[0].isdigit():
        return lexerInteger(inAll, 1)
    
    elif inAll[0] == "(" or inAll[0] == ")":
        return [[inAll[0]], inAll[1:]]  
    
    elif inAll[0] == "_" or inAll[0].isalpha():
        return keyLexerID(inAll)
    
    elif inAll[0] == "\"":
        return stringLexer(inAll)
    
    elif inAll[0] == ",":
        return [[","], inAll[1:]]
    
    elif inAll[0] == "/":
        return [["/"], inAll[1:]]
    
    elif inAll[0] == "-":
        if inAll[1].isdigit():
            return lexerInteger(inAll[1:], -1)
        else:
            return [["-"], inAll[1:]]
        
    elif inAll[0] == "*":
        return [["*"], inAll[1:]]
    
    elif inAll[0] == "+":
        return [["+"], inAll[1:]]
      
    elif inAll[0].isspace():
        pass

    else: 
        return[[errorID, " Invalid or Indeterminable Character used. " + "Found on Line: " + str(lineNumber)], inAll]

# Calls the Lexer Functions, reading File Inputs
print("Please Enter Test File. For example, enter \"test1.txt\" ") 
file = input()
fileIN = open(file, "r")
fileRead = list(fileIN.read())

[next, fileRead] = lexer(fileRead)

while next[0] != errorID and next[0] != 5:
    print(next)
    [next, fileRead] = lexer(fileRead)

if next[0] == errorID:
    print("ERROR: " + next[1])

fileIN.close()