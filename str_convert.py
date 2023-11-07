import math
import operator



'''
This script substitute eval() to calculate an equation from a string.

Inputs: 
        expression = the string containing an algebraic equation (must be in proper format and only contain the available operations)
        parameter(optional) = if there are any parameter in the expression, enter a list of parameter with its corresponding value
                            = [(parameter_name1, value1), (parameter_name2, value2), ....]
        available operations = +, -, *, /, **, //, %, sqrt, sin, cos, tan, asin, acos, atan 
                (to add more operation, change self.ops)

Output: using the method "return_value()", we can get a float number containing the calculated value of the expression
(only when proper expression and parameters are given)

'''



class Str_Conv():

    def __init__(self, expression, parameters=[]):

        # set input and output
        self.str = expression.replace(" ", "")
        self.parameters = parameters
        self.value = 0
        self.test = 1

        # available operators, following the normal precendence (math_ops functions accept one input, arith_ops two)
        self.math_ops = ["sqrt", "sin", "cos", "tan", "asin", "acos", "atan"]
        self.arith_ops = ["+", "-", "*", "/", "//", "**", "%"]
        self.op = { 
                "+": operator.add,
                "-": operator.sub,
                "*": operator.mul,
                "/": operator.truediv,
                "**": operator.pow,
                "%": operator.mod,
                "//": operator.floordiv,
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "asin": math.asin,
                "acos": math.acos,
                "atan": math.atan}   

        # load methods
        self.insert_parameters() 
        self.check_parenthesis()
        self.str = self.get_value(self.str)


    
    def insert_parameters(self):
        ''' 
        This function substitute the value of all listed parameters into the string.

        Process: Use for loop to goes through each parameter and subtitute the value in every presence of the parameter.
        '''
        parameters = self.parameters
        self.parameters = []

        for parameter in parameters:
            if self.parameters == []:
                self.parameters.append(parameter)
            else:
                i = 0
                while i < len(self.parameters) and len(parameter[0]) < len(self.parameters[i][0]):    i += 1
                self.parameters.insert(i, parameter)

        for parameter in self.parameters:
            if self.str.find(parameter[0]) != -1:
                # substitue parameter with its value
                self.str = self.str.replace(parameter[0], str(parameter[1]))
        
        self.str = self.str.replace("pi", "3.1415")



    def check_parenthesis(self):
        ''' 
        This function check if there are proper numbers of parenthesis in expressions.

        Process: Check for number of parenthesis and add ")" at the end, "(" at the front as need.
        '''
        i = self.str.count("(")
        j = self.str.count(")")

        if i == j:
            pass
        elif i == j + 1:
            self.str = self.str + ")"
        elif j == i + 1:
            self.str = "(" + self.str
        else: 
            print("ERROR: parenthesis not corresponding!")
            


    def get_value(self, string): 
        '''
        This function return the final value of the calculation.

        Input: a string with only numbers and operators(include parenthesis)
        
        Process: This funtion work recrusively to get the smallest parenthesis that needs to be calculate first 
        and call "calculate" method to get the value inside the parenthesis. Repeat the process until no more parenthesis present
        and then calculate the whole expression to get a value.
        '''
        # look for contents within parenthesis
        start = string.find("(") 
        if start != -1:
            i = start + 1
            while i < len(string):
            #for i in range(start+1, len(self.str)):
                # call itself if another parenthesis exist in the current parenthesis
                if string[i] == "(": 
                    temp = self.get_value(string[i:])
                    string = string.replace(string[i:], temp)
                # calculate the value inside parenthesis
                elif string[i] == ")":
                    temp = self.calculate(string[start:i+1])
                    string = string.replace(string[start:i+1], temp)
                    if string.find("(") == -1:
                        break
                i += 1

        # calculate the final value without parenthesis
        if string.find("(") == -1 and string.find(")") == -1:
            string = self.calculate(string)
            
        return string



    def calculate(self, string):
        '''
        This function calculate the value of expression from a string (don't include parenthesis).

        Input: a string with only numbers and operators(exclude parenthesis)
        
        Process: Split the string into numeric value and operators; then, do the calculation for each operator in precendence order.
        '''
        # remove parenthesis
        string = string.replace("(", "").replace(")","")

        # if no calculation required, return the value
        if string.replace(".","").isnumeric():
            return string
        
        # split the string into list
        list = self.partition_operators(string)

        # substitute for math operations first
        i = 0
        while i < len(list):
            if list[i] in self.math_ops: 
                list[i] = self.op[list[i]](float(list[i+1]))
                list.pop(i+1)
            elif str(list[i])[0] == "-" and str(list[i])[1:] in self.math_ops:
                temp = str(list[i])[1:]
                list[i] = -self.op[temp](float(list[i+1]))
                list.pop(i+1)
            i += 1
        
        # substitute for arithmatic operations in order
        list = self.call_ops(list, ["**"])
        list = self.call_ops(list, ["*", "//", "/", "%"])
        list = self.call_ops(list, ["+", "-"])

        # check if the result is a number
        if len(list) != 1:
            print(list)
            print(f"ERROR: Improper format for {string}!")
        else:
            return str(list[0])
    


    def call_ops(self, list, arith_ops):
        '''
        This function calculate results of certain arithmetic operations.

        Input: list = a list of strings with number and operators separated
               arith_ops = a list of arithmetic opertions we deal with (must be within self.arith_ops)

        Process: goes through the list to check for operators in arith_ops and perform the corresponding operation in the list.
        '''
        i = 0
        # goes through the list
        while i < len(list):
            if list[i] in arith_ops:
                # call the function stored in dictionary self.ops
                list[i-1] = self.op[list[i]](float(list[i-1]), float(list[i+1]))
                list.pop(i)
                list.pop(i)
            else:
                i += 1
        
        return list



    def partition_operators (self, string):
        '''
        This function split a string expression into a list of separated numbers and operators

        Input: a string expression

        Process: Goes through each character in the string, split the string where ever it changes between three types of characters (digit, letter, operators)
        '''
        list = []
        last_i = 0

        # define the type of previous character: 1 = num, 2 = alpha, 3 = operators
        if string[0].isdigit(): 
            prev = 1
        elif string[0].isalpha(): 
            prev = 2
        else: 
            prev = 3

        # iterate through all characters to split the string
        for i, char in enumerate(string):
            if (char.isdecimal() or char == ".") and prev != 1:
                list.append(string[last_i:i])
                last_i = i
                prev = 1
            elif char.isalpha() and prev != 2 :
                list.append(string[last_i:i])
                last_i = i
                prev = 2
            elif not (char.isdecimal() or char == "." or char.isalpha()) and prev != 3:
                list.append(string[last_i:i])
                last_i = i
                prev = 3

            if i == len(string)-1:
                list.append(string[last_i:i+1])
            
        if list[0] == "-":
            list.pop(0)
            list[0] = "-" + list[0]
            
        return list



    def return_value (self):
        '''
        This function return the final calculated value of the string.
        '''

        try:
            self.value = float(self.str)
            return self.value
        except ValueError or TypeError:
            print("ERROR: Can't find proper final value!")
            print(f"The final result: {self.str}")

            

if __name__ == "__main__":
    string = "(-atan(T2/T1)*180/pi"
    parameter = [('PD', '2.375'), ('L1', '6'), ('L2', '1'), ('W1', '5'), ('W2', '4'), ('W3', '1.5'), ('W4', '1'), ('H1', '4'), 
                 ('H2', '0.6'), ('TH1', '0.5'), ('TH2', '0.5'), ('TH3', '0.3'), ('TH4', '0.2'), ('BD', '0.3125'), ('BHD1', '0.67'), 
                 ('BHD2', '0.728'), ('BTH', '0.25'), ('T1', 4.1403022731818435), ('T2', 0.25), ('T3', 4.1478431640208795)]
    a = Str_Conv(string, parameter)
    b = a.return_value()
    print(b)



