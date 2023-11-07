from pyautocad import Autocad, APoint
from math import *



'''
This script accepts certain operations and load the command onto PLANT 3D using pyautocad. 
It works with read_script.py to load PLANT 3D code for testing purpose.

Input: operaitons = [[operation_code, object_name, operation-specific content....], [], ....]
            (operation_code: 0-20 = add_shape, 21 = translate, 22 = rotate, 23 = erase, 30-32 = edit shape)

Available operaionts:
    0 = BOX
    1 = CYLINDER (not elliptical)
    2 = CONE (without eccentricity)
    3 = ARC3D
    4 = HALFSHPERE
    5 = TORUS

    21 = MOVE
    22 = ROTATE3D
    23 = ERASE

    30 = UNION
    31 = INTERSECT
    32 = SUBTRACT
'''



class Ac():

    def __init__(self, operations):

        # create autocad instance
        self.acad = Autocad()
        self.doc = self.acad.model

        # create attributes
        self.operations = operations
        self.objects = []
        self.object_names = []
        self.object_centers = []
        self.origin = APoint(0, 0, 0)

        # load methods
        print("Start loading...")
        self.load_operations()
        print("Done loading!")



    def load_operations(self):
        '''
        This function goes through all the operations and perform the corresponding command on PLANT 3D.
        '''
        for operation in self.operations:
            # match operation_code
            match operation[0]:
                # BOX
                case 0: 
                    self.object_names.append(operation[1])
                    self.object_centers.append([0,0,0])
                    object1 = self.doc.AddBox(self.origin, operation[2][0], operation[2][1], operation[2][2])
                    self.objects.append(object1)
                # CYLINDER
                case 1: 
                    self.object_names.append(operation[1])
                    self.object_centers.append([0,0,0])
                    if operation[2][1] == 0:
                        object2 = self.doc.AddCylinder(APoint(0, 0, operation[2][0]/2), operation[2][2], operation[2][0])
                        self.objects.append(object2)
                    else:
                        object2 = self.doc.AddCylinder(APoint(0, 0, operation[2][0]/2), operation[2][2], operation[2][0])
                        helper = self.doc.AddCylinder(APoint(0, 0, operation[2][0]/2), operation[2][1], operation[2][0])
                        object2.Boolean(2, helper)
                        self.objects.append(object2)
                # CONE
                case 2:
                    self.object_names.append(operation[1])
                    self.object_centers.append([0,0,0])
                    if operation[2][1] == 0:
                        object2 = self.doc.AddCone(APoint(0, 0, operation[2][2]/2), operation[2][0], operation[2][2])
                        self.objects.append(object2)
                    else:
                        H = - operation[2][0] * operation[2][2] / (operation[2][1] - operation[2][0])
                        object2 = self.doc.AddCone(APoint(0, 0, H/2), operation[2][0], H)
                        helper = self.doc.AddCone(APoint(0, 0, (H + operation[2][2])/2), operation[2][0], H - operation[2][2])
                        object2.Boolean(2, helper)
                        self.objects.append(object2)
                # ARC3D
                case 3:
                    self.object_names.append(operation[1])
                    self.object_centers.append([0,0,0])
                    object1 = self.make_arc3d(operation)
                    self.objects.append(object1)
                # HALFSPHERE
                case 4:
                    self.object_names.append(operation[1])
                    self.object_centers.append([0,0,0])
                    object1 = self.doc.AddSphere(self.origin, operation[2][0])
                    helper = self.doc.AddBox(self.origin, operation[2][0]*2, operation[2][0]*2, operation[2][0])
                    helper.MOVE(self.origin, APoint(0,0,-operation[2][0]/2))
                    object1.Boolean(2, helper)
                    self.objects.append(object1)
                # TORUS
                case 5:
                    self.object_names.append(operation[1])
                    self.object_centers.append([0,0,0])
                    object1 = self.doc.AddTorus(self.origin, operation[2][0], operation[2][1])
                    self.objects.append(object1)
                # MOVE
                case 21:
                    try: 
                        i = self.object_names.index(operation[1])
                    except ValueError:
                        print(f"ERROR: Can't translate {operation[1]}!")
                    else:
                        if self.object_centers[i] == (0,0,0):
                            start_point = self.origin
                        else:
                            start_point = APoint(self.object_centers[i][0], self.object_centers[i][1], self.object_centers[i][2])
                        self.object_centers[i][0] += operation[2]
                        self.object_centers[i][1] += operation[3]
                        self.object_centers[i][2] += operation[4]
                        end_point = APoint(self.object_centers[i][0], self.object_centers[i][1], self.object_centers[i][2])
                        self.objects[i].Move(start_point, end_point)
                # ROTATE3D
                case 22: 
                    try: 
                        i = self.object_names.index(operation[1])
                    except ValueError:
                        print(f"ERROR: Can't rotate {operation[1]}!")
                    else:
                        angle = operation[3]/180*pi
                        if operation[2] == "X":
                            self.objects[i].Rotate3D(self.origin, APoint(100, 0, 0), angle)
                        elif operation[2] == "Y":
                            self.objects[i].Rotate3D(self.origin, APoint(0, 100, 0), angle)
                        elif operation[2] == "Z":
                            self.objects[i].Rotate3D(self.origin, APoint(0, 0, 100), angle)
                        else:
                            print(f"ERROR: Rotation \"{operation}\" incomplete!")
                # ERASE
                case 23:
                    try: 
                        i = self.object_names.index(operation[1])
                    except ValueError: 
                        print(f"ERROR: Can't erase {operation[1]}")
                    else: 
                        self.objects.pop(i)
                        self.object_names.pop(i)
                        self.object_centers.pop(i)
                # UNION, INTERSECT, SUBTRACT
                case num if 29 < num < 33: 
                    self.boolean_operations(operation)
                

       
    def boolean_operations(self, operation):
        '''
        This function perform the boolean operations of shape (union, intersect, subtract).
        '''
        try: 
            i = self.object_names.index(operation[1])
            j = self.object_names.index(operation[2])
        except ValueError: 
            print(f"ERROR: Can't perform \"{operation}\"")
        else:
            self.objects[i].Boolean(operation[0]-30, self.objects[j])


    def make_arc3d(self, operation):
        '''
        This function print a 3D arc object according to the operation

        operation = [operation_code, object_name, dimension=[D, R, A]]
        '''
        D = operation[2][0]
        R = operation[2][1]
        A = operation[2][2] /180 *pi

        object1 = self.doc.AddTorus(self.origin, R, D)
        temp1 = self.doc.AddBox(APoint(R/2+D/2, 0, 0), R+D, (R+D)*2, D*2)
        object1.Boolean(2, temp1)
        temp2 = self.doc.AddBox(APoint(R/2+D/2, 0, 0), R+D, (R+D)*2, D*2)
        temp2.Rotate3D(self.origin, APoint(0, 0, 10), pi-A)
        object1.Boolean(2, temp2)

        if A < pi:
            object1.MOVE(self.origin, APoint(R*tan(A/2), R, 0))
        elif operation[2][2] == 180:
            object1.MOVE(self.origin, APoint(R, R, 0))

        return object1

if __name__ == "__main__":
    operations = [[1, 'c1', [2.125, 0, 0.255]], [21, 'c1', 0, -1.755, -2.125], [1, 'c2', [2.125, 0, 0.255]], [21, 'c2', 0, 1.755, -2.125], 
                  [3, 'c3', [0.255, 1.755, 180]], [22, 'c3', 'Y', 90.0], [21, 'c3', 0, -1.755, 1.755]]
    op = Ac(operations)
    # [1, "c1", [10, 0, 3]]