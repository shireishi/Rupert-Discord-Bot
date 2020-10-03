import ast

def write():
    tempDict = {}
    with open('Untitled.txt', 'r') as file:
        dict = ast.literal_eval(file.read())
        for Id in dict:
            tempDict[Id] = dict[Id]
            
    with open('reputation.log', 'w') as file:
        file.write(str(tempDict))

write()