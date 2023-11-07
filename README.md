# autocad_plant3d_custom_object_testing

## AutoCAD Plant3D Python Custom Objects

Plant3D allows user to create customed 3D pipe supports using Python code. To test the code, we need to register the script by restarting Plant3D for every change. 

This script loads the python code for Plant 3D cutom parts and load the corresponding shape on Plant 3D. 
Comparing to normal testing process that requires the restart of PLANT 3D, this script provide a faster way to test/debug the code. 


## Run the Script

1. Make sure Plant3D is opened to a new file in the background.
2. Put the Plant3D script in the same folder as the codes.
3. Open "read_script.py" file
4. Replace the value of the variable "FILENAME" on line 28 with the name of the file containing Plant3D script (exclude extension ".py")
5. Run "read_script.py"
6. the corresponding shape will load on the PLANT 3D interface

### Restrictions on code format:        
    1. comments can't be on the same line as code (e.g. h1 = BOX(s, L, W, H) # this is a box)
    2. different shapes need to have different names 
    4. don't assign the same shape with different names (e.g. h2 = h1.translate((x,y,z)))
    5. don't support if-else statements or other condition logic
    6. only support the following comments: (the rest will be ignored)
    [BOX, CYLINDER, CONE, ARC3D, HALFSPHERE, TORUS, translate, rotate, subtractFrom, intersectWith, uniteWith]

