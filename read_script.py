import math
import str_convert as sc
import load_autocad



'''
This script load the python code for Plant 3D cutom parts and load the corresponding shape on Plant 3D. 
Comparing to normal testing process that requires the restart of PLANT 3D, this script provide a faster way to test/debug the code. 

Input: 
        filename = the name of the file containing the python script (exclude extension ".py")
            (make sure the file is in the same file as current script, str_convert.py, and load_autocad.py)

Output: keep PLANT 3D runing when executing the code, the corresponding shape will load on the PLANT 3D interface. 

Restrictions on code format:        
    1. comments can't be on the same line as code (e.g. h1 = BOX(s, L, W, H) # this is a box)
    2. different shapes need to have different names 
    4. don't assign the same shape with different names (e.g. h2 = h1.translate((x,y,z)))
    5. don't support if-else statements or other condition logic
    6. only support the following comments: (the rest will be ignored)
    [BOX, CYLINDER, CONE, ARC3D, HALFSPHERE, TORUS, translate, rotate, subtractFrom, intersectWith, uniteWith]
'''


# Enter the filename over here:
FILENAME = "TEST"


class ReadScript ():
        
    def __init__ (self, filename):
    
        # open file
        self.f = open(filename + ".py", "r")

        # read file contents
        self.content = self.f.read()
        self.lines = self.content.split("\n")

        # define attributes
        self.parameters = []
        self.operations = []
        self.error = 0

        # load methods to process file content
        self.extract_file()
        self.get_parameters()
        self.process_operations()
        print(f"List of parameters:\n{self.parameters}\n---------------------------------------------------------------")
        print(f"List of operations with parameters:\n{self.operations}\n----------------------------------------------------------------")
        self.set_parameter_value()
        
        # print the list of operations for user to check before loading onto autocad
        if not self.error:
            x = input(f"Check the list of operation:\n{self.operations}\nProceed (y/n)?")
            if x == "y":
                load_autocad.Ac(self.operations)
        else:
            print("Oops! Something wrong with the code. Please check before proceed forward!")

        # close file
        self.f.close()



    def extract_file(self):
        '''
        This function process the file content and extract lines with command

        Process: goes through all the lines in file to get rid of the import section, parameters definitions, and comments 
        '''
        lines_temp = self.lines.copy()
        index = -1
        find_def = 0
        in_comment = 0 
        
        # iterate through self.lines
        for line in lines_temp:
            index += 1
            if line.find("def") != -1:
                find_def = 1
            # pop out the contents before function definitions
            elif find_def == 0: 
                self.lines.pop(index)
                index -= 1
            elif in_comment == 0:
                # get rid of comments and certain functions
                if line.find("#") != -1 or line.find("setPoint") != -1 or line.find("setLinearDimension") != -1: 
                    self.lines.pop(index)
                    index -= 1
                # find ''' and get rid of contents in between
                elif line.find("\'\'\'") != -1:
                    self.lines.pop(index)
                    index -= 1
                    in_comment = 1
                # get rid of lines without content
                elif line.isspace() or line == "\n" or line == "": 
                    self.lines.pop(index)
                    index -= 1
            else:
                if line.find("\'\'\'") != -1:
                    in_comment = 0
                self.lines.pop(index)
                index -= 1

        # error message if can't find the function definition
        if not find_def:
            print("ERROR: Can't find the function definition!\n")
            self.error = 1
        if in_comment:
            print("ERROR: Comment not closed!\n")
            self.error = 1
    

    def get_parameters(self):
        '''
        This function load the parameters pre-defined for the object

        Output: self.parameters = [(parameter_name, default_value), ....]

        Process: find the lines of PLANT3D function definition and load all parameters passed on to the arguments of the function
        '''
        # find all parameters enclosed by "()" and put them into paramters_str
        parameters_str = self.lines[0].split(",")
        parameters_str.pop(0)
        parameters_str.pop(-1)
        index = 0

        while self.lines[index].find(")") == -1:
            parameters_str.extend(self.lines[index+1].split(","))
            parameters_str.pop(-1)
            index += 1
        
        # pop the definition lines from self.lines
        for i in range(index+1):
            self.lines.pop(0)

        # change the formate of parameters_str and store it into self.parameters
        for parameter in parameters_str:
            parameter = parameter.replace(" ", "")
            temp = parameter.split("=")
            self.parameters.append ((temp[0], temp[1]))
    
        

    def process_operations(self):
        '''
        Ths function process all the command lines and store it in self.operations.

        Output: self.operations = [[operation_code, operation-specific content....], [], ....]
                    (operation_code: 0-20 = add_shape, 21 = translate, 22 = rotate, 23 = erase, 30-32 = edit shape)
        '''
        for operation in self.lines:
            operation = operation.replace(" ", "")
            if operation.find("=") != -1:
                self.operations.extend(self.add_shape(operation))
            elif operation.find("erase") != -1:
                self.operations.append(self.erase_shape(operation))
            elif operation.find("subtractFrom") == -1 or operation.find("uniteWith") == -1 or operation.find("intersectWith") == -1:
                self.operations.append(self.edit_shape(operation))
            else:
                print(f"ERROR: line \"{operation}\" don't correspond to any available commends!")
                self.error = 1
        


    def add_shape(self,operation):
        '''
        This function process the commands that defines a shape

        Output: rtn = [[operation_code = 0/1/2, object_name, dimensions = [....]], [operation_code = 21/22, object_name, other_elements]...]
                    (operation_code: 0 = BOX, 1 = CYLINDER, 2 = CONE, 3 = ARC3D, 4 = HALFSPHERE, 5 = TORUS, 21 = translate, 22 = rotate)
        '''
        rtn = []

        # split the line of operation into multiple commends
        steps = operation.split(").")
        if len(steps) == 1:
            steps[0] = steps[0][:-1]
        object_name = steps[0].split("=")[0]

        # iterate through each command
        for step in steps:
            temp = step.split(",")
            temp.pop(0)

            if step.find("BOX") != -1:
                operation_code = 0
                dimension = [0,0,0]
                # iterate through to find parameters
                for i in range(3):
                    if temp[i].find("H=") != -1:
                        dimension[0] = temp[i].replace("H=", "")
                    elif temp[i].find("L=") != -1:
                        dimension[1] = temp[i].replace("L=", "")
                    else:
                        dimension[2] = temp[i].replace("W=", "")
                rtn.append([operation_code, object_name, dimension])
                            
            elif step.find("CYLINDER") != -1:
                operation_code = 1
                dimension = [0,0,0]
                # iterate through to find parameters
                for i in range(len(temp)):
                    if temp[i].find("R=") != -1:
                        dimension[2] = temp[i].replace("R=", "")
                    elif temp[i].find("H=") != -1:
                        dimension[0] = temp[i].replace("H=", "")
                    elif temp[i].find("O=") != -1:
                        dimension[1] = temp[i].replace("O=", "")
                rtn.append([operation_code, object_name, dimension])

            elif step.find("CONE") != -1:
                operation_code = 2
                dimension = [0,0,0,0]
                for i in range(4):
                    if temp[i].find("R1=") != -1:
                        dimension[0] = temp[i].replace("R1=", "")
                    elif temp[i].find("R2=") != -1:
                        dimension[1] = temp[i].replace("R2=", "")
                    elif temp[i].find("H=") != -1:
                        dimension[2] = temp[i].replace("H=", "")
                    else:
                        dimension[3] = temp[i].replace("E=", "")
                rtn.append([operation_code, object_name, dimension])
                # error message if eccentricity applied
                if dimension[3] != 0:
                    print(f"ERROR: \"{step}\" is not an available operation! The eccentricity will be ignored!")
            
            elif step.find("ARC3D") != -1:
                operation_code = 3
                dimension = [0,0,0]
                for i in range(3):
                    if temp[i].find("D=") != -1:
                        dimension[0] = temp[i].replace("D=", "")
                    elif temp[i].find("R=") != -1:
                        dimension[1] = temp[i].replace("R=", "")
                    elif temp[i].find("A=") != -1:
                        dimension[2] = temp[i].replace("A=", "")
                rtn.append([operation_code, object_name, dimension])
            
            elif step.find("HALFSPHERE") != -1:
                operation_code = 4
                dimension = [0]
                dimension[0] = temp[0].replace("R=","")
                rtn.append([operation_code, object_name, dimension])

            elif step.find("TORUS") != -1:
                operation_code = 5
                dimension = [0,0]
                for i in range(2):
                    if temp[i].find("R1=") != -1:
                        dimension[0] = temp[i].replace("R1=", "")
                    elif temp[i].find("R2=") != -1:
                        dimension[1] = temp[i].replace("R2=", "")
                rtn.append([operation_code, object_name, dimension])

            elif step.find("translate") != -1:
                rtn.append(self.translate_shape(object_name, step))

            elif step.find("rotate") != -1:
                rtn.append(self.rotate_shape(object_name, step))

            # definition of local variables
            elif step.count("=") == 1:
                temp = operation.split("=")
                parameter_name = temp[0]
                exp = sc.Str_Conv(temp[1], self.parameters)
                self.parameters.append((parameter_name, exp.return_value()))
            
            else:
                print(f"ERROR: \"{step}\" is not an available operation")
        
        return rtn



    def translate_shape(self, object_name, step):
        '''
        This function process the tranlate command.

        Output: rtn = [operation_code = 21, object_name, translate_X, translate_Y, translate_Z]
        '''
        operation_code =21
        temp = step.split("((")
        temp[1] = temp[1].split(",")

        # iterate through to find and get rid of "))"
        i = 0
        while temp[1][2][-1] == ")" and i < 2:
            temp[1][2] = temp[1][2][:-1]
            i += 1
        return [operation_code, object_name, temp[1][0], temp[1][1], temp[1][2]]

    

    def rotate_shape(self, object_name, step):
        '''
        This function process the rotate command.

        Output: rtn = [operation_code = 22, object_name, rotate_axis, rotate_degree]
        '''
        operation_code = 22
        i = step.find("rotate")
        rotate_axis = step[i+6]
        j = step.find("(")
        rotate_degree = step[j:]
        return [operation_code, object_name, rotate_axis, rotate_degree]



    def erase_shape(self, operation):
        '''
        This function process the erase command.

        Output: rtn = [operation_code = 23, object_name]
        '''
        operation_code = 23
        object_name = operation.split(".")[0]
        return [operation_code, object_name]



    def edit_shape(self,operation):
        '''
        This function process the shape editing command.
        
        Output: rtn = [operation_code, object1, object2]
                    (operation_code: 30 = uniteWith, 31 = intersectWith, 32 = subtractForm)
        '''
        temp = operation.split(".")
        object1 = temp[0]
        temp[1] = temp[1].split("(")
        object2 = temp[1][1].replace(")", "")

        match temp[1][0]:
            case "subtractFrom":
                operation_code = 32
            case "uniteWith":
                operation_code = 30
            case "intersectWith":
                operation_code = 31

        return [operation_code, object1, object2]


    
    def set_parameter_value(self):
        '''
        This function find all the values self.operations and substitute the parameters with its default value.

        '''
        # iterate through operations
        for i, operation in enumerate(self.operations):
            match operation[0]:
                # translate, operation[2:] = X,Y,Z
                case 21:
                    temp = self.get_default_value(operation, 2)
                    temp = self.get_default_value(temp, 3)
                    temp = self.get_default_value(temp, 4)
                    self.operations[i] = temp
                # rotate, operation[3] = rotate_angle
                case 22:
                    temp = self.get_default_value(operation, 3)
                    self.operations[i] = temp
                # add_shape, operation[2] = list of dimension
                case num if 0 <= num <= 20:
                    temp = operation[2]
                    for j in range(len(operation[2])):
                        temp = self.get_default_value(temp, j)
                    self.operations[i][2] = temp


    
    def get_default_value(self, list, position):
        '''
        This function use Str_Conv to evaluate an expression with available parameters

        Input: list[position] = the expression

        Output: rtn = list with updated value
        '''
        # if expression is a number
        if str(list[position]).isdecimal():
            list[position] = int(list[position])
        # if expresion is a single parameter
        elif str(list[position]).isalnum():
            for parameter in self.parameters:
                if parameter[0] == list[position]:
                    list[position] = float(parameter[1])
        else:
            temp = sc.Str_Conv(list[position], self.parameters)
            list[position] = temp.return_value()
        
        return list



    

if __name__ == "__main__":

    ReadScript(FILENAME)
