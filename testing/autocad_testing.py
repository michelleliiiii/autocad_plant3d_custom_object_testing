from pyautocad import Autocad, APoint, aDouble
from math import *

# create Autocad instance (active drawing)
acad = Autocad()

# print string in python terminal/command prompt in autocad
acad.prompt("Hello, Autocad from Python\n")

# print some properties of the app
print (acad.doc.Name)
print(acad.app.ActiveDocument.Name)
print(acad.app.Application.Name)
print(acad.app.Caption)
print(acad.app.Path)
print(acad.app.FullName)

# create points
p1 = APoint(0,0,0)
p2 = APoint(100,100,0)
p3 = APoint(500,400,0)

# add general items
l1 = acad.model.AddLine(p1, p2)
c1 = acad.model.AddCircle(p1, 100)
c1.Color = 11
c3 = c1.ScaleEntity(APoint(300, 300), 0.5)
el1 = acad.model.AddEllipse(p1, p3, 0.5)
# acad.model.AddArc(<Center Point of Circle>, <Radius>, <Start Angle>, <End Angle>)
arc1 = acad.model.AddArc(p1, 100, 0, 6)

# create customized block
b1 = acad.doc.Blocks.Add(p1, "Block 1")
# add components to the block
l2 = b1.AddLine(p1,p2)
c2 = b1.AddCircle(p1,100)
p1 = b1.AddPolyline(aDouble(0,0,0,100,100,0,200,0,0,0,0,0))

# certain properties of a block
print("Object Name: " + b1.ObjectName)
print("Name of Block: " + b1.Name)
print("Native units of measures for the Block: ", end="")
print(b1.Units)
print("Is scaling allowed for the Block ? ", end="")
print(b1.BlockScaling)
print("Is the Block explodable ? ", end="")
print(b1.Explodable)
print("Is the Block dynamic ? ", end="")
print(b1.IsDynamicBlock)

# insert block at certain location
b2 = acad.model.InsertBlock(p3, "Block 1",1,1,1,0)
#b2.Explode()

# create array
#arr1 = c1.ArrayPolar(10, round(pi), aDouble(550, 600, 0))

# attribute object
a1 = b1.AddAttribute(50, 0, "DATE", aDouble(200, 100, 0), "DATE", "Date: 17/07/2022")

# pyautocad Add()-method  
# object.Add(Name)
acad.doc.Layers.Add("Eq")

# operation
c3 = c1.Copy()
#obj.Move(previous location, new location)
c3.Move(APoint(100, 100), APoint(300, 300))
l2 = l1.Copy()
# obj.Rotate(Base point, Angle of rotation)
l2.Rotate(APoint(100,100), pi*90/180)

el2 = el1.Offset(10)
