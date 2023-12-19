# defining array of tokens
tokens = []

# defining index which iterates the indexes of tokens
index = 0

class tokenSet:
    def _init_(self):
        self.classPart = "",
        self.valuePart = "",
        self.lineNumber = 0

# taking input the file of words.txt 
def TokenInput():
    file = open("words.txt", "r")
    TokenLines = file.readlines()

    for token in TokenLines:
        indivToken = token.strip().split(', ')
        # initializing object
        tokenObj = tokenSet()
        tokenObj.classPart = indivToken[0]
        tokenObj.valuePart = indivToken[1]
        tokenObj.lineNumber = indivToken[2]

        tokens.append(tokenObj)

TokenInput()

# Semantic initializations

stack = []
scope = 0
stack.append(scope)
CurrentClass = ""

# tables initialization

function_table = [["Name", "Type", "Scope"]]
main_table = [["Name", "Type", "Category", "Parent", "Link"]]

data_member_tables = {}
member_table = [["Name", "Type", "Access Modifier", "Type Modifier"]]

def insert_function_table(Name, Type, Scope):

    # check redeclaration
    check = 0
    function_table.append([Name, Type, Scope])

    for i in range(len(function_table)):

        if function_table[i][0]=="Name":
            continue

        if Name==function_table[i][0] and Scope==function_table[i][2]:
            check += 1
            if check == 1:
                continue
            function_table.pop() 
            return False

    return True

def insert_function_table_func(Name, Type, Scope):

    # check redeclaration
    check = 0
    function_table.append([Name, Type, Scope])

    for i in range(len(function_table)):

        if function_table[i][0]=="Name":
            continue

        if Name==function_table[i][0] and Type.split(' -> ')[0] == function_table[i][1].split(' -> ')[0] and Scope==function_table[i][2]:
            check += 1
            #print(Type.split('->')[0] , "   " , function_table[i][1].split('->')[0])
            if check == 1:
                continue
            function_table.pop()
            return False

    return True

def insert_main_table(Name, Type, Category, Parent, Link):

    # check redeclaration
    Link = Name + Type
    check = 0
    main_table.append([Name, Type, Category, Parent, Link])


    for i in range(len(main_table)):

        if main_table[i][0]=="Name":
            continue

        if Name==main_table[i][0]:
            check += 1
            if check == 1:
                continue
            main_table.pop()
            return False

    data_member_tables[Link] = member_table
    return True

def lookup_function_table( Name, Scope ):
  for i in range(len(function_table)):

        if function_table[i][0]=="Name":
            continue

        if Name==function_table[i][0] and Scope==function_table[i][2]:
          return function_table[i][1]
  return False

def mainSyntaxAnalyzer():
    global index
    if(structure()):
        if(tokens[index].classPart == "$"):
            print("No syntax error")
    
    else:
        print("SYNTAX ERROR!")
        print({tokens[index].classPart}, {tokens[index].valuePart}, {tokens[index].lineNumber})

def structure(): # follow included
    global index
    print('structure is calling')
    if(SST()):
        if(structure()):
            return True
    elif(Class()):
        if(structure()):
            return True
    elif(Abstract_class()):
        if(structure()):
            return True
    elif(tokens[index].classPart == "$"): 
        return True
    
    return False

def SST():
    global index
    print("SST is calling")
    if(Expression()):
        return True
    elif(Declaration()):
        print('reading dec')
        return True
    elif(if_else()):
        return True
    elif(during()):
        return True
    elif(run_st()):
        return True
    elif(break_st()):
        return True
    elif(Continue()):
        return True
    elif(return_st()):
        return True
    elif(func_dec()):
        return True
    elif(Tuple()):
        return True
    elif(try_except()):
        return True
    elif(tokens[index].classPart == "Id"):
        index += 1  
        if(SST1()):
            return True
   
    return False

def SST1(): # follow included
    print("reading DT of sst1")
    if(Array_def()):
        return True
    elif(object_call()):
        return True 
    elif(inc_dec()):
        return True 
    elif(Arr_func()):
        return True  
    elif(func_call()):
        return True 
    elif(tokens[index].classPart == "DT"):
        return True   
    elif(tokens[index].classPart == "return"):
        return True   
    elif(tokens[index].classPart == "if"):
        return True   
    elif(tokens[index].classPart == "during"):
        return True   
    elif(tokens[index].classPart == "run"):
        return True   
    elif(tokens[index].valuePart == "break"):
        return True   
    elif(tokens[index].valuePart == "continue"):
        return True   
    elif(tokens[index].classPart == "def"):
        return True   
    elif(tokens[index].valuePart == "tup"):
        return True   
    elif(tokens[index].classPart == "try"):
        return True   
    elif(tokens[index].classPart == "Id"):
        return True   
    elif(tokens[index].classPart == "except"):
        return True   
    elif(tokens[index].classPart == "else"):
        return True   
    elif(tokens[index].valuePart == "}"):
        return True   
    
    return False

def const():
    global index
    print("const is calling")
    print(index)
    print(tokens[index].valuePart)
    if(tokens[index].classPart == "String Constant"):
        index += 1
        return True
    elif(tokens[index].classPart == "Boolean Constant"):
        index += 1
        return True
    elif(tokens[index].classPart == "Character Constant"):
        index += 1
        return True
    elif(tokens[index].classPart == "Float Constant"):
        index += 1
        return True
    elif(tokens[index].classPart == "Integer Constant"):
        index += 1
        return True
    
    return False

def Declaration():
    global index, scope
    print("Declaration is calling")

    if(tokens[index].classPart == "DT"):
        T = tokens[index].valuePart # saving type of variable by its valuepart
        index += 1
        if(tokens[index].classPart == "Id"):
            N = tokens[index].valuePart # saving a value of Id by its valuepart
            if(not insert_function_table(N, T, scope)):
                print("............................REDECLARATION ERROR ................................!")
                return 
            index += 1
            if(init()):
                if(List(T)):
                    return True
    
    return False

def init(): # follow included
    global index
    print("init is calling")
    if(tokens[index].valuePart == "="):
        index += 1
        if(Expression()):
            return True
    elif(tokens[index].valuePart == ";"):
        return True
    elif(tokens[index].valuePart == ","):
        return True
    
    return False

def List(T):
    global index, scope
    if(tokens[index].valuePart == ";"):
        index += 1
        return True
    elif(tokens[index].valuePart == ","):
        index += 1
        if(tokens[index].classPart == "Id"):
            N = tokens[index].valuePart
            if(not insert_function_table(N, T, scope)):
                print("............................REDECLARATION ERROR ................................!")
                return
            index += 1
            if(init()):
                if(List(T)):
                    return True
    
    return False

def return_st():
    global index
    print("return_st is calling")
    if(tokens[index].classPart == "return"):
        index += 1
        if(return1()):
            return True
    
    return False

def return1():
    global index
    print("return1 is calling")

    if(Expression()):
        if(tokens[index].valuePart == ";"):
            index += 1
            return True
    elif(tokens[index].valuePart == ";"):
        index += 1
        return True
    
    return False

def break_st():
    global index
    if(tokens[index].classPart == "break"):
        index += 1
        return True
    
    return False

def Continue():
    global index
    if(tokens[index].classPart == "continue"):
        index += 1
        return True
    
    return False

def inc_dec():
    if(inc_dec_opt()):
        return True
    
    return False

def inc_dec_opt():
    global index
    if(tokens[index].classPart == "++"):
        index += 1
        return True
    elif(tokens[index].classPart == "--"):
        index += 1
        return True
    
    return False

def if_else():
    global index
    print("if_else is calling")
    if(tokens[index].classPart == "if"):
        index += 1
        if(tokens[index].valuePart == "("):
            index += 1
            if(Expression()):
                if(tokens[index].valuePart == ")"):
                    index += 1
                    if(body()):
                        if(Else()):
                            return True
    
    return False

def body(): # follow set included
    global index
    print("reading DT of body")
    if(SST()):
        return True
    elif(tokens[index].valuePart == "{"):
        index += 1
        if(MST()):
            if(tokens[index].valuePart == "}"):
                index += 1
                return True
    elif(tokens[index].valuePart == ";"):
        index += 1
        return True
    elif(tokens[index].classPart == "DT"):
        return True   
    elif(tokens[index].classPart == "return"):
        return True   
    elif(tokens[index].classPart == "if"):
        return True   
    elif(tokens[index].classPart == "during"):
        return True   
    elif(tokens[index].classPart == "run"):
        return True   
    elif(tokens[index].classPart == "break"):
        return True   
    elif(tokens[index].classPart == "continue"):
        return True   
    elif(tokens[index].classPart == "def"):
        return True   
    elif(tokens[index].classPart == "tup"):
        return True   
    elif(tokens[index].classPart == "try"):
        return True   
    elif(tokens[index].classPart == "Id"):
        return True   
    elif(tokens[index].classPart == "except"):
        return True   
    elif(tokens[index].classPart == "else"):
        return True   
    elif(tokens[index].valuePart == "}"):
        return True   
    
    return False

def MST(): # follow set included
    print("MST func is calling")
    print(tokens[index].valuePart)
    if(SST()):
        if(MST()):
            return True
    elif(tokens[index].valuePart == "}"):
        return True   
    
    return False

def Else(): # follow set included
    global index
    print("Else func is calling")
    print("reading DT of else")
    print(tokens[index].valuePart)

    if(tokens[index].classPart == "else"):
        index += 1
        if(body()):
            return True
    elif(tokens[index].classPart == "DT"):
        return True   
    elif(tokens[index].classPart == "return"):
        return True   
    elif(tokens[index].classPart == "if"):
        return True   
    elif(tokens[index].classPart == "during"):
        return True   
    elif(tokens[index].classPart == "run"):
        return True   
    elif(tokens[index].classPart == "break"):
        return True   
    elif(tokens[index].classPart == "continue"):
        return True   
    elif(tokens[index].classPart == "def"):
        return True   
    elif(tokens[index].classPart == "tup"):
        return True   
    elif(tokens[index].classPart == "try"):
        return True   
    elif(tokens[index].classPart == "Id"):
        return True   
    elif(tokens[index].classPart == "except"):
        return True   
    elif(tokens[index].classPart == "else"):
        return True   
    elif(tokens[index].valuePart == "}"):
        return True   
    
    return False

def during():
    global index
    print("during func is calling")

    print(tokens[index].valuePart)

    if(tokens[index].classPart == "during"):
        index += 1
        if(tokens[index].valuePart == "("):
            index += 1
            if(Expression()):
                if(tokens[index].valuePart == ")"):
                    index += 1
                    if(while_body()):
                        return True

    return False

def while_body():
    global index
    print("while_body func is calling")
    print(tokens[index].valuePart)

    if(tokens[index].valuePart == ":"):
        index += 1
        return True
    elif(SST()):
        return True
    elif(tokens[index].valuePart == "{"):
        index += 1
        if(MST()):
            if(tokens[index].valuePart == "}"):
                index += 1
                return True
            
    return False

def  run_st():
    global index
    print("run_st func is calling")
    print(tokens[index].valuePart)

    if(tokens[index].classPart == "run"):
        index += 1
        if(tokens[index].valuePart == "("):
            index += 1
            if(Declaration()):
                # if(tokens[index].valuePart == ";"):
                #     index += 1
                    if(Expression()):
                        if(tokens[index].valuePart == ";"):
                            index += 1
                            if(Expression()):
                                if(tokens[index].valuePart == ")"):
                                    index += 1
                                    if(for_body()):
                                        return True
    
    return False


def for_body():
    global index
    print("for_body func is calling")
    print(tokens[index].valuePart)

    if(tokens[index].valuePart == ";"):
        index += 1
        return True
    elif(SST()):
        return True
    elif(tokens[index].valuePart == "{"):
        index += 1
        if(MST()):
            if(tokens[index].valuePart == "}"):
                index += 1
                return True
            
    return False

def try_except():
    global index
    print("try_except func is calling")
    print(tokens[index].valuePart)

    if(tokens[index].classPart == "try"):
        index += 1
        if(try_body()):
            if(Except()):
                return True
    
    return False

def try_body():
    global index
    print("try_body func is calling")
    print(tokens[index].valuePart)

    if(SST()):
        return True
    elif(tokens[index].valuePart == "{"):
        index += 1
        if(MST()):
            if(tokens[index].valuePart == "}"):
                index += 1
                return True

    return False

def Except():
    global index
    print("Except func is calling")
    print(tokens[index].valuePart)

    if(tokens[index].classPart == "except"):
        index += 1
        if(tokens[index].classPart == "Id"):
            index += 1
            if(except_body()):
                return True
    
    return False

def except_body():
    global index
    print("except_body func is calling")
    print(tokens[index].valuePart)

    if(SST()):
        return True
    elif(tokens[index].valuePart == "{"):
        index += 1
        if(MST()):
            if(tokens[index].valuePart == "}"):
                index += 1
                return True

    return False


def func_dec():
    global index
    print("function declaration is calling")
    print(tokens[index].valuePart)

    if(tokens[index].classPart == "def"):
        print("valuepart = ", tokens[index].classPart)
        index += 1
        if(tokens[index].classPart == "Id"):
            print("valuepart = ", tokens[index].valuePart)
            index += 1
            if(tokens[index].valuePart == "("):
                print("valuepart = ", tokens[index].valuePart)
                index+=1
                if(param_list()):
                    if(tokens[index].valuePart == ")"):
                        index+=1
                        if(func_body()):
                            return True
    
    return False

def param_list(): # follow set included
    global index

    if(Type()):
        if(tokens[index].classPart == "Id"):
            index += 1
            if(pl2()):
                return True
    elif(tokens[index].valuePart == ")"):
        return True

    return False

def Type():
    global index
    print("Type is calling")

    if(tokens[index].classPart == "Id"):
        index += 1
        return True
    elif(tokens[index].classPart == "DT"):
        index += 1
        return True

    return False

def pl2():
    global index
    print("pl2 is calling")

    if(tokens[index].valuePart == ","):
        index += 1
        if(Type()):
            if(tokens[index].classPart == "Id"):
                index += 1
                if(pl2()):
                    return True
    elif(tokens[index].valuePart == ")"):
        return True

    return False

def func_body():
    global index
    print("func_body is calling")
    print(tokens[index].valuePart)

    if(tokens[index].valuePart == "{"):
        index += 1
        if(remaining_body()):
            return True
        
    return False
        
def remaining_body():
    global index
    print("remaining_body is calling")

    if(MST()):
        if(tokens[index].valuePart == "}"):
            index += 1
            if(tokens[index].valuePart == ";"):
                index += 1
                return True

    return False

def Tuple():
    global index
    if(tokens[index].classPart == "tup"):
        index += 1
        if(tokens[index].classPart == "Id"):
            index += 1
            if(tokens[index].classPart == "="):
                index += 1
                if(tuple_body()):
                    if(tokens[index].classPart == ":"):
                        index += 1
                        return True
    
    return False

def tuple_body():
    global index
    if(tokens[index].valuePart == "("):
        index += 1
        if(inside_tup_body()):
            if(tokens[index].valuePart == ")"):
                index += 1
                return True
            
    return False

def inside_tup_body():
    if(Expression()):
        if(rpt()):
            return True
        
    return False

def rpt(): # follow set included
    global index
    if(tokens[index].valuePart == ","):
        index += 1
        if(inside_tup_body()):
            return True         
    elif(tokens[index].valuePart == ")"):
        return True
     
    return False

def Array_def():
    global index
    if(tokens[index].valuePart == "="):
        index += 1
        if(body_Arr()):
            return True
    
    return False    

def body_Arr():
    global index
    if(tokens[index].valuePart == "["):
        index += 1
        if(inside_Arr_body()):
            if(tokens[index].valuePart == "]"):
                index += 1
                return True

    return False

def inside_Arr_body():
    if(Expression()):
        if(rpt2()):
            return True
    elif(body_Arr()):
        if(rpt2()):
            return True
    
    return False

def rpt2():
    global index
    if(tokens[index].valuePart == ","):
        index += 1
        if(inside_Arr_body()):
            return True
    elif(tokens[index].valuePart == "]"):
        return True
        
    return False


def Arr_func():
    global index
    if(tokens[index].valuePart == "."):
        index += 1
        if(Array_call_func()):
            return True

    return False

def Array_call_func():
    global index
    if(tokens[index].classPart == "append"):
        index += 1
        if(tokens[index].valuePart == "("):
            index += 1
            if(append_value()):
                if(tokens[index].valuePart == ")"):
                    index += 1
                    return True
    elif(tokens[index].classPart == "pop"):
        index += 1
        if(tokens[index].valuePart == "("):
            index += 1
            if(tokens[index].valuePart == ")"):
                index += 1
                return True
            
    return False

def append_value():
    global index
    if(tokens[index].classPart == "Id"):
        index += 1
        return True
    elif(const()):
        return True
    elif(body_Arr()):
        return True
    
    return False
                
def Array_call():
    global index
    if(tokens[index].valuePart == "["):
        index += 1
        if(Expression()):
            if(tokens[index].valuePart == "]"):
                index += 1
                if(tokens[index].valuePart == ":"):
                    index += 1

def func_call(): 
    global index
    print("func_call is calling")

    if(tokens[index].valuePart == "("):
        index += 1
        if(func_call_value()):
            if(tokens[index].valuePart == ")"):
                index += 1
                if(tokens[index].valuePart == ":"):
                    index += 1
                    return True
                
    return False

def func_call_value():
    if(Expression()):
        if(rpt3()):
            return True
        
    return False

def rpt3(): # follow set included
    global index
    if(tokens[index].valuePart == ","):
        index += 1
        if(func_call_value()):
            return True
    elif(tokens[index].valuePart == ")"):
        return True
    
    return False

def object_call(): 
    print("object_call is calling")
    if(call()):
        return True
    
    return False

def call():
    global index
    print("call is calling")

    if(tokens[index].valuePart == "."):
        index += 1
        if(tokens[index].classPart == "Id"):
            index += 1
            if(recall()):
                return True
    elif(tokens[index].valuePart == "++"): 
        return True
    
    print("returning false from function call")
    return False

def recall():
    if(call()):
        return True
    elif(func_call()):
        if(call()):
            return True
    elif(Array_call()):
        if(call()):
            return True
        
    return False

def Class():
    global index
    print("Class is calling")

    print(tokens[index].valuePart)

    if(Access_modifier()):
        if(tokens[index].classPart == "Class"):
            print(tokens[index].valuePart)
            index += 1
            if(tokens[index].classPart == "Id"):
                print(tokens[index].valuePart)
                index += 1
                if(Inheritance()):
                    if(class_body()):
                        return True
    
    return False

def Access_modifier(): # follow set included
    global index
    print("Access modifier is calling")
    print(tokens[index].valuePart)

    if(tokens[index].classPart == "AM"):
        index += 1
        return True
    elif(tokens[index].classPart == "Class"):
        return True
    elif(tokens[index].classPart == "DT"):
        return True
    elif(tokens[index].classPart == "def"): 
        return True
    elif(tokens[index].classPart == "Abstract"): # not defined in lexical
        return True
    
    return False

def Inheritance(): # follow set included
    global index
    print("Inheritance is calling")
    print(tokens[index].valuePart)

    if(tokens[index].classPart == "inherit"):
        index += 1
        if(tokens[index].classPart == "Id"):
            index += 1
            return True
    elif(tokens[index].valuePart == "{"):
        return True
    
    return False

def class_body():
    global index
    print("class_body is calling")
    print(tokens[index].valuePart)

    if(tokens[index].valuePart == "{"):
        index += 1
        if(CMST()):
            if(tokens[index].valuePart == "}"):
                index += 1
                return True
            
    return False
def CMST():  # follow included 
    global index
    print("CMST is calling")
    print(tokens[index].valuePart)

    if(class_Dec()):
        if(CMST()):
            return True
    elif(class_method()):
        if(CMST()):
            return True
    elif(constructor()):
        if(CMST()):
            return True
    elif(tokens[index].valuePart == "}"):
        return True
        
    return False
def class_Dec():
    print("class_dec is calling")
    print(tokens[index].valuePart)

    if(Access_modifier()):
        if(Declaration()):
            return True
    return False
        
def class_method():
    global index
    print("class_method is calling")
    print(tokens[index].valuePart)

    if(Access_modifier()):
        if(tokens[index].classPart == "def"):
            index += 1
            if(tokens[index].classPart == "Id"):
                index += 1
                if(tokens[index].valuePart == "("):
                    index += 1
                    if(param_list()):
                        if(tokens[index].valuePart == ")"):
                            index += 1
                            if(c_method_body()):
                                return True
    return False
def c_method_body():
    global index
    print("c_method_body is calling")
    print(tokens[index].valuePart)

    if(tokens[index].valuePart == "{"):
        index += 1
        if(CSST()):
            if(tokens[index].valuePart == "}"):
                index += 1
                return True
    return False

def CSST():
    global index
    print("CSSt is calling")
    print(tokens[index].valuePart)

    if(MST()):
        return True
    return False

def constructor():
    global index
    print("constructor is calling")
    print(tokens[index].valuePart)

    if(tokens[index].classPart == "Id"):
        index += 1
        if(tokens[index].valuePart == "("):
            index += 1
            if(param_list()):
                if(tokens[index].valuePart == ")"):
                    index += 1
                    if(constructor_body()):
                        return True
    return False

def constructor_body():
    global index
    print("constructor_body is calling")
    print(tokens[index].valuePart)
    
    if(tokens[index].valuePart == "{"):
        index += 1
        if(constructor_MST()):
            if(tokens[index].valuePart == "}"):
                index += 1
                return True

    return False

def constructor_MST(): # follow set included
    global index
    print("constructor_MST is calling")
    print(tokens[index].valuePart)

    if(tokens[index].classPart == "this"):
        index += 1
        if(tokens[index].valuePart == "."):
            index += 1
            if(Declaration()):
                if(constructor_MST()):
                    return True
    elif(CSST()):
        if(constructor_MST()):
            return True
    elif(tokens[index].valuePart == "}"):
        return True
    
    return False

def Abstract_class():
    global index
    print("Abstract_class is calling")
    print(tokens[index].valuePart)

    if(Access_modifier()):
        if(tokens[index].classPart == "Abstract"):
            index += 1
            if(tokens[index].classPart == "Class"):
                index += 1
                if(tokens[index].classPart == "Id"):
                    index += 1
                    if(Abstract_body()):
                        return True
    
    return False

def Abstract_body():
    global index
    print("Abstract_body is calling")
    print(tokens[index].valuePart)

    if(tokens[index].valuePart == "{"):
        index += 1
        if(Abstract_inside()):
            if(tokens[index].valuePart == "}"):
                index += 1
                return True
            
    return False

def Abstract_inside():
    print("Abstract_inside is calling")
    print(tokens[index].valuePart)

    if(class_Dec()):
        return True
    elif(Abstract_func_types()):
        return True
    
    return False
            
def Abstract_func_types():
    print("Abstract_func_types is calling")
    print(tokens[index].valuePart)

    if(Abstract_method()):
        return True
    elif(class_method()):
        return True
    
    return False

def Abstract_method():
    global index
    print("Abstract_method is calling")
    print(tokens[index].valuePart)

    if(tokens[index].valuePart == "def"):
        index += 1
        if(tokens[index].classPart == "Id"):
            index += 1
            if(tokens[index].valuePart == "("):
                index += 1
                if(param_list()):
                    if(tokens[index].valuePart == ")"):
                        index += 1
                        if(tokens[index].valuePart == ";"):
                            index += 1
                            return True
                        
    return False

def object_class():
    global index
    print("object_class is calling")
    print(tokens[index].valuePart)
    
    if(tokens[index].classPart == "Id"):
        index += 1
        if(tokens[index].classPart == "Id"):
            index += 1
            if(tokens[index].valuePart == "="):
                index += 1
                if(tokens[index].classPart == "new"):
                    index += 1
                    if(tokens[index].classPart == "Id"):
                        index += 1
                        if(tokens[index].valuePart == "("):
                            index += 1
                            if(Expression()):
                                if(tokens[index].valuePart == ")"):
                                    index += 1
                                    if(tokens[index].valuePart == ";"):
                                        index += 1
                                        return True
                                    
    return False


def Expression():
    print("Expression is calling...")
    print(tokens[index].valuePart)

    if(compound_Ass()):
        if(Expression1()):
            return True
    elif(tokens[index].valuePart == ")"):
        return True
    
    return False

def Expression1(): # follow set included
    global index
    if(tokens[index].classPart == "compound_Assignment"):
        index += 1
        if(compound_Ass()):
            if(Expression1()):
                return True
    elif(tokens[index].valuePart == ")"):
        return True
    elif(tokens[index].valuePart == "]"):
        return True
    elif(tokens[index].valuePart == ","):
        return True
    elif(tokens[index].valuePart == ";"):
        return True
    elif(tokens[index].valuePart == "!"):
        return True
    elif(tokens[index].valuePart == "("):
        return True
    elif(tokens[index].classPart == "Id"):
        return True
    elif(tokens[index].classPart == "String Constant"):
        return True
    elif(tokens[index].classPart == "Boolean Constant"):
        return True
    elif(tokens[index].classPart == "Character Constant"):
        return True
    elif(tokens[index].classPart == "Float Constant"):
        return True
    elif(tokens[index].classPart == "Integer Constant"):
        return True
    elif(tokens[index].valuePart == "."):
        return True
    
    return False

def compound_Ass():
    print("Compound assignment is calling")
    if(Assignment_opt()):
        if(compound_Ass1()):
            return True
        
    return False

def follow_oe():



    if tokens[index].valuePart == "!":
        return True
    elif tokens[index].valuePart == "]":
        return True
    elif tokens[index].valuePart == ",":
        return True
    elif tokens[index].valuePart == ";":
        return True
    elif tokens[index].valuePart == "}":
        return True
    elif tokens[index].valuePart == ")":
        # self.current_index += 1
        # self.current_token = self.lexer[self.current_index]
        return True
    elif tokens[index].valuePart == "(":
        return True
    elif tokens[index].classPart == "Id":
        return True
    elif(tokens[index].classPart == "String Constant"):
        return True
    elif(tokens[index].classPart == "Boolean Constant"):
        return True
    elif(tokens[index].classPart == "Character Constant"):
        return True
    elif(tokens[index].classPart == "Float Constant"):
        return True
    elif(tokens[index].classPart == "Integer Constant"):
        return True
    elif tokens[index].valuePart == ".":
        return True
    elif(tokens[index].classPart == "String Constant"):
        return True
    elif(tokens[index].classPart == "Boolean Constant"):
        return True
    elif(tokens[index].classPart == "Character Constant"):
        return True
    elif(tokens[index].classPart == "Float Constant"):
        return True
    elif(tokens[index].classPart == "Integer Constant"):
        return True
    return False


def compound_Ass1():
    global index
    if(tokens[index].classPart == "assignment_operator"):
        index += 1
        if(Assignment_opt()):
            if(compound_Ass1()):
                return True
    elif(tokens[index].classPart == "compound_Assignment"):
        return True
    elif(tokens[index].valuePart == ")"):
        return True
    elif(tokens[index].valuePart == ","):
        return True
    elif(tokens[index].valuePart == "]"):
        return True
    elif(tokens[index].valuePart == ";"):
        return True
    elif(follow_oe()):
        return True

    return False

def Assignment_opt():
    print("assignment operator is calling")
    if(NOT()):
        if(Assignment_opt1()):
            return True
    return False

def Assignment_opt1(): # follow set included
    global index
    if(tokens[index].valuePart == "not"):
        index += 1
        if(NOT()):
            if(Assignment_opt1()):
                return True
    elif(tokens[index].classPart == "assignment_operator"):
        return True
    elif(tokens[index].classPart == "compound_Assignment"):
        return True
    elif(tokens[index].valuePart == ")"):
        return True
    elif(tokens[index].valuePart == ","):
        return True
    elif(tokens[index].valuePart == "]"):
        return True
    elif(tokens[index].valuePart == ";"):
        return True
    elif(follow_oe()):
        return True
    
    return False

def NOT():
    print("NOT is calling")
    if(OR()):
        if(NOT1()):
            return True
    return False

def NOT1(): # follow set included
    global index
    if(tokens[index].valuePart == "or"):
        index += 1
        if(OR()):
            if(NOT1()):
                return True
    elif(tokens[index].valuePart == "not"):
        return True
    elif(tokens[index].classPart == "assignment_operator"):
        return True
    elif(tokens[index].classPart == "compound_Assignment"):
        return True
    elif(tokens[index].valuePart == ")"):
        return True
    elif(tokens[index].valuePart == ","):
        return True
    elif(tokens[index].valuePart == "]"):
        return True
    elif(tokens[index].valuePart == ";"):
        return True
    elif(follow_oe()):
        return True
    
    return False

def OR():
    print("OR is calling")
    if(AND()):
        if(OR1()):
            return True
        
    return False

def OR1(): # follow set included
    global index
    if(tokens[index].valuePart == "and"):
        index += 1
        if(AND()):
            if(OR1()):
                return True
    elif(tokens[index].valuePart == "or"):
        return True
    elif(tokens[index].valuePart == "not"):
        return True
    elif(tokens[index].classPart == "assignment_operator"):
        return True
    elif(tokens[index].classPart == "compound_Assignment"):
        return True
    elif(tokens[index].valuePart == ")"):
        return True
    elif(tokens[index].valuePart == ","):
        return True
    elif(tokens[index].valuePart == "]"):
        return True
    elif(tokens[index].valuePart == ";"):
        return True
    elif(follow_oe()):
        return True
    
    return False

def AND():
    print("AND is calling")
    if(ROP()):
        if(AND1()):
            return True
    return False

def AND1(): # follow set included
    global index
    if(tokens[index].classPart == "relational_operator"):
        index += 1
        if(ROP()):
            if(AND1()):
                return True
    elif(tokens[index].valuePart == "and"):
        return True
    elif(tokens[index].valuePart == "or"):
        return True
    elif(tokens[index].valuePart == "not"):
        return True
    elif(tokens[index].classPart == "assignment_operator"):
        return True
    elif(tokens[index].classPart == "compound_Assignment"):
        return True
    elif(tokens[index].valuePart == ")"):
        return True
    elif(tokens[index].valuePart == ","):
        return True
    elif(tokens[index].valuePart == "]"):
        return True
    elif(tokens[index].valuePart == ";"):
        return True
    elif(follow_oe()):
        return True
    
    return False

def ROP():
    print("ROP is calling")
    if(PM()):
        if(ROP1()):
            return True
        
    return False

def ROP1(): # follow set included
    global index
    if(tokens[index].classPart == "arithmetic_operator"):
        index += 1
        if(PM()):
            if(ROP1()):
                return True
            
    elif(tokens[index].classPart == "relational_operator"):
        return True
    elif(tokens[index].valuePart == "and"):
        return True
    elif(tokens[index].valuePart == "or"):
        return True
    elif(tokens[index].valuePart == "not"):
        return True
    elif(tokens[index].classPart == "assignment_operator"):
        return True
    elif(tokens[index].classPart == "compound_Assignment"):
        return True
    elif(tokens[index].valuePart == ")"):
        return True
    elif(tokens[index].valuePart == ","):
        return True
    elif(tokens[index].valuePart == "]"):
        return True
    elif(tokens[index].valuePart == ";"):
        return True
    elif(follow_oe()):
        return True
    
    return False

def PM():
    print("PM is calling")
    if(MDM()):
        if(PM1):
            return True
        
    return False

def PM1(): # follow set included
    global index
    if(tokens[index].classPart == "arithmetic_operator"):
        index += 1
        if(MDM()):
            if(PM1()):
                return True
    elif(tokens[index].valuePart == "+" or tokens[index].valuePart == "-"):
        return True
    elif(tokens[index].classPart == "relational_operator"):
        return True
    elif(tokens[index].valuePart == "and"):
        return True
    elif(tokens[index].valuePart == "or"):
        return True
    elif(tokens[index].valuePart == "not"):
        return True
    elif(tokens[index].classPart == "assignment_operator"):
        return True
    elif(tokens[index].classPart == "compound_Assignment"):
        return True
    elif(tokens[index].valuePart == ")"):
        return True
    elif(tokens[index].valuePart == ","):
        return True
    elif(tokens[index].valuePart == "]"):
        return True
    elif(tokens[index].valuePart == ";"):
        return True
    elif(follow_oe()):
        return True
    
    
    return False

def MDM():
    print("MDM is calling")
    if(P()):
        if(MDM1()):
            return True

    return False

def MDM1(): # follow set included
    global index
    if(tokens[index].classPart == "P"):
        index += 1
        if(P()):
            if(MDM1()):
                return True
            
    elif(tokens[index].valuePart == "*" or tokens[index].valuePart == "/" or tokens[index].valuePart == "%"):
        return True
    elif(tokens[index].valuePart == "+" or tokens[index].valuePart == "-"):
        return True
    elif(tokens[index].classPart == "relational_operator"):
        return True
    elif(tokens[index].valuePart == "and"):
        return True
    elif(tokens[index].valuePart == "or"):
        return True
    elif(tokens[index].valuePart == "not"):
        return True
    elif(tokens[index].classPart == "assignment_operator"):
        return True
    elif(tokens[index].classPart == "compound_Assignment"):
        return True
    elif(tokens[index].valuePart == ")"):
        return True
    elif(tokens[index].valuePart == ","):
        return True
    elif(tokens[index].valuePart == "]"):
        return True
    elif(tokens[index].valuePart == ";"):
        return True
    elif(follow_oe()):
        return True

    return False

def P():
    print("P is calling")
    if(Dec()):
        if(P1()):
            return True

    return False

def P1(): # follow set included
    global index
    if(tokens[index].valuePart == "**"):
        index += 1
        if(Dec()):
            if(P1()):
                return True    
            
    elif(tokens[index].valuePart == "**"):
        return True
    elif(tokens[index].valuePart == "*" or tokens[index].valuePart == "/" or tokens[index].valuePart == "%"):
        return True
    elif(tokens[index].valuePart == "+" or tokens[index].valuePart == "-"):
        return True
    elif(tokens[index].classPart == "relational_operator"):
        return True
    elif(tokens[index].valuePart == "and"):
        return True
    elif(tokens[index].valuePart == "or"):
        return True
    elif(tokens[index].valuePart == "not"):
        return True
    elif(tokens[index].classPart == "assignment_operator"):
        return True
    elif(tokens[index].classPart == "compound_Assignment"):
        return True
    elif(tokens[index].valuePart == ")"):
        return True
    elif(tokens[index].valuePart == ","):
        return True
    elif(tokens[index].valuePart == "]"):
        return True
    elif(tokens[index].valuePart == ";"):
        return True
    elif(follow_oe()):
        return True
    
    return False

def Dec():
    print("Dec is calling")
    if(F()):
        if(Dec1()):
            return True
        
    return False

def Dec1(): # follow set included
    global index
    if(tokens[index].valuePart == "++"):
        index += 1
        if(F()):
            if(Dec1()):
                return True
    elif(tokens[index].valuePart == "--"):
        return True
    elif(tokens[index].valuePart == "**"):
        return True
    elif(tokens[index].valuePart == "*" or tokens[index].valuePart == "/" or tokens[index].valuePart == "%"):
        return True
    elif(tokens[index].valuePart == "+" or tokens[index].valuePart == "-"):
        return True
    elif(tokens[index].classPart == "relational_operator"):
        return True
    elif(tokens[index].valuePart == "and"):
        return True
    elif(tokens[index].valuePart == "or"):
        return True
    elif(tokens[index].valuePart == "not"):
        return True
    elif(tokens[index].classPart == "assignment_operator"):
        return True
    elif(tokens[index].classPart == "compound_Assignment"):
        return True
    elif(tokens[index].valuePart == ")"):
        return True
    elif(tokens[index].valuePart == ","):
        return True
    elif(tokens[index].valuePart == "]"):
        return True
    elif(tokens[index].valuePart == ";"):
        return True
    elif(follow_oe()):
        return True
    
    return False

def F():
    print("F is calling")
    global index
    if(const()):
        return True
    elif(tokens[index].valuePart == "("):
        index += 1
        if(Expression()):
            if(tokens[index].valuePart == ")"):
                index += 1
                return True
    elif(tokens[index].valuePart == "not"):
        index += 1
        if(F()):
            return True
    elif(tokens[index].classPart == "Id"):
        index += 1
        if(F2()):
            return True
        
    return False

def F2(): # follow set inculded
    if(object_call()):
        return True
    elif(inc_dec()):
        return True
    elif(Array_def()):
        return True
    elif(Arr_func()):
        return True
    elif(Array_call()):
        return True
    elif(func_call()):
        return True
    elif(tokens[index].classPart == "++"):
        return True
    elif(tokens[index].valuePart == "--"):
        return True
    elif(tokens[index].valuePart == "**"):
        return True
    elif(tokens[index].valuePart == "*" or tokens[index].valuePart == "/" or tokens[index].valuePart == "%"):
        return True
    elif(tokens[index].valuePart == "+" or tokens[index].valuePart == "-"):
        return True
    elif(tokens[index].classPart == "relational_operator"):
        return True
    elif(tokens[index].valuePart == "and"):
        return True
    elif(tokens[index].valuePart == "or"):
        return True
    elif(tokens[index].valuePart == "not"):
        return True
    elif(tokens[index].classPart == "assignment_operator"):
        return True
    elif(tokens[index].classPart == "compound_Assignment"):
        return True
    elif(tokens[index].valuePart == ")"):
        return True
    elif(tokens[index].valuePart == ","):
        return True
    elif(tokens[index].valuePart == "]"):
        return True
    elif(tokens[index].valuePart == ";"):
        return True
    
    return False


# main function call
mainSyntaxAnalyzer()

# printing data table

# print("Function table : \n", function_table)