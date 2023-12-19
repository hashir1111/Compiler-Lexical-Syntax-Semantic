import re

file = open('./input.txt', "r+", encoding="utf-8") 
inputData = file.read()
file.close()

re_int = r"^[+-]?\d+$"
re_flt = r'\d+\.\d*|\.\d+'  
re_string = r'".*?"'  
re_char = r"'.*?'"
re_bool = r"^(true|false)$"  

re_ID = "^[_A-Za-z]+[_A-Za-z0-9$]*$"
re_comment = "^[#][A-Za-z0-9]*|[#][!][A-Za-z0-9]*[!][#]$"

arithmetic_operator = ["+","-","/","%","*","**"]
assignment_operator = ["="]
relational_operator = ["==","!=","<",">","!",">=","<="]
compound_assignment = ["+=","-=","*=","/=","%="]
inc_dec = ["++" , "--"]
logical_operator = ["and", "or", "not"]
punctuator = [";",":","@","(",")","{","}",".",",","[","]"]
dataType = ["whole" , "dec" , "truth_value" , "string" , "char"]
if_class = ["if"]
def_class = ["def"]
this_class = ["this"]
abstract_class = ["Abstract"]
else_class = ["else"]
return_class = ["return"]
access_modifiers = ["public" , "private"]
new_class = ["new"]
class_c = ["Class"]
inherit_class = ["inherit"]
run_class = ["run"]
during_class = ["during"]
try_class = ["try"]
catch_class = ["catch"]
except_class= ["except"]

line = 1

words = []
def breakWords(data, line):
    iter = 0
    temp = ""
    
    while iter < len(data):
        check = data[iter]

        if check == '#':

            temp = ""
            temp += data[iter]
            iter += 1
            check = data[iter]
            if check == "!":
                while True:
                    temp += data[iter]
                    iter += 1
                    check = data[iter]

                    if check == '!':
                        temp += data[iter]
                        iter += 1
                        check = data[iter]

                        if check == "#":
                            temp += data[iter]

                            temp = ""
                            break
            else:
                while True:
                    temp += data[iter]
                    iter += 1
                    check = data[iter]

                    if check == '\n':
                        temp += data[iter]

                        temp = ""
                        break

        elif check == '"':
            while True:
                temp += data[iter]
                iter += 1
                check = data[iter]

                if check == '"':
                    temp += data[iter]
                    words.append(["", temp, line])
                    temp = ""
                    break

        elif check == "'":
            while True:
                temp += data[iter]
                iter += 1
                check = data[iter]

                if check == "'":
                    temp += data[iter]
                    words.append(["", temp, line])
                    temp = ""
                    break

        elif re.match(r"^[-+]?\d*\.\d+|\d+", data[iter:]):
            match_flt = re.match(r"^\d*\.\d+|\d+", data[iter:])
            if match_flt:
                temp_flt = match_flt.group()
                words.append(["Float Constant", temp_flt, line])
                iter += len(temp_flt) - 1

        elif check == "+":
            
            if data[iter + 1] == "+":
                words.append(["", "++", line])
                iter += 1
            elif data[iter + 1] == "=":
                words.append(["", "+=", line])
                iter += 1
            else:
                
                while True:
                    temp += data[iter]
                    iter += 1
                    check = data[iter]

                    if check not in arithmetic_operator:
                        words.append(["", temp, line])
                        temp = ""
                        break

        elif check == "-":
            
            if data[iter + 1] == "-":
                words.append(["", "--", line])
                iter += 1 
            elif data[iter + 1] == "=":
                words.append(["", "-=", line])
                iter += 1
            else:
                
                while True:
                    temp += data[iter]
                    iter += 1
                    check = data[iter]

                    if check not in arithmetic_operator:
                        words.append(["", temp, line])
                        temp = ""
                        break
  
                    if check not in assignment_operator:
                        words.append(["", temp, line])
                        temp = ""
                        break
        elif check in relational_operator:
            while True:
                temp += data[iter]
                iter += 1
                check = data[iter]
  
                if check not in relational_operator:
                    words.append(["", temp, line])
                    temp = ""
                    break
        elif check in compound_assignment:
            while True:
                temp += data[iter]
                iter += 1
                check = data[iter]
  
                if check not in compound_assignment:
                    words.append(["", temp, line])
                    temp = ""
                    break
        elif check in logical_operator:
            while True:
                temp += data[iter]
                iter += 1
                check = data[iter]
  
                if check not in logical_operator:
                    words.append(["", temp, line])
                    temp = ""
                    break
        elif check in inc_dec:
            while True:
                temp += data[iter]
                iter += 1
                check = data[iter]
  
                if check not in inc_dec:
                    words.append(["", temp, line])
                    temp = ""
                    break

        elif check in punctuator:
            words.append(["", temp, line])
            temp = ""

            temp += data[iter]
            words.append(["", temp, line])
            temp = ""

        elif check == "\n":
            
            if temp:
                words.append(["", temp, line])
                temp = ""
            line += 1
            iter += 1  
            continue  

        elif check != " ":
            temp += data[iter]

        else:
            if temp:
                words.append(["", temp, line])
                temp = ""
        
        iter += 1

    if temp:
        words.append(["", temp, line])
    return iter


iter = breakWords(inputData, line)

words2 = []
for i in range(len(words)):
    if words[i][1] != "" and words[i][1] != "\n" and words[i][1] != " ":
        words2.append(words[i])

# for the last line for $ 
last_line = words2[-1][2]

for i in range(len(words2)):
    if words2[i][1] == "=":
        words2[i][0] = "assignment_operator"
    elif words2[i][1] in arithmetic_operator:
        words2[i][0] = "arithmetic_operator"
    elif words2[i][1] in relational_operator:
        words2[i][0] = "relational_operator"
    elif words2[i][1] in compound_assignment:
        words2[i][0] = "compound_Assignment"
    elif words2[i][1] in logical_operator:
        words2[i][0] = "logical_operator"
    elif words2[i][1] in dataType:
        words2[i][0] = "DT"
    elif words2[i][1] in def_class:
        words2[i][0] = "def"
    elif words2[i][1] in this_class:
        words2[i][0] = "this"
    elif words2[i][1] in abstract_class:
        words2[i][0] = "Abstract"
    elif words2[i][1] in if_class:
        words2[i][0] = "if"
    elif words2[i][1] in else_class:
        words2[i][0] = "else"
    elif words2[i][1] in return_class:
        words2[i][0] = "return"
    elif words2[i][1] in access_modifiers:
        words2[i][0] = "AM"
    elif words2[i][1] in new_class:
        words2[i][0] = "new"
    elif words2[i][1] in class_c:
        words2[i][0] = "Class"
    elif words2[i][1] in inherit_class:
        words2[i][0] = "inherit"
    elif words2[i][1] in run_class:
        words2[i][0] = "run"
    elif words2[i][1] in during_class:
        words2[i][0] = "during"
    elif words2[i][1] in try_class:
        words2[i][0] = "try"
    elif words2[i][1] in catch_class:
        words2[i][0] = "catch"
    elif words2[i][1] in except_class:
        words2[i][0] = "except"
    elif words2[i][1] in punctuator:
        words2[i][0] = "punctuator"
    elif words2[i][1] in inc_dec:
        words2[i][0] = "inc_dec"
    else:
        if bool(re.match(re_string, words2[i][1])):
            words2[i][0] = "String Constant"
            words2[i][1] = words2[i][1][1:-1]
        elif bool(re.match(re_bool, words2[i][1])):
            words2[i][0] = "Boolean Constant"
        elif bool(re.match(re_char, words2[i][1])):
            words2[i][0] = "Character Constant"
            words2[i][1] = words2[i][1][1:-1]
        elif bool(re.match(re_flt, words2[i][1])):
            words2[i][0] = "Float Constant"
        elif bool(re.match(re_int, words2[i][1])):
            words2[i][0] = "Integer Constant"
        elif bool(re.match(re_ID, words2[i][1])):
            words2[i][0] = "Id"
        elif bool(re.match(re_comment, words2[i][1])):
            words2[i][0] = "Comment"
        else:
            words2[i][0] = "Error"

wordsFile = open("./words.txt", "w", encoding="utf-8")
for i in words2:
    wordsFile.write(f"{i[0]}, {i[1]}, {i[2]}\n")
wordsFile.write(f"$, , {last_line + 1}")
wordsFile.close()




# print("gfujskd\"hfkk")