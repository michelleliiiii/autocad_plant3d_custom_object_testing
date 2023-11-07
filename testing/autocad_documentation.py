from pyautocad import Autocad, APoint, aDouble

# set up connection with the current active drawing in AutoCAD (make an instance)
acad = Autocad()
acad.prompt("Hello, Autocad from Python\n")

# print some properties of the app
print (acad.doc.Name)
print(acad.app.Application.Name)
print(acad.app.Caption)
print(acad.app.ActiveDocument.Name)
print(acad.app.Path)
print(acad.app.FullName)

# print all menubar instanaces
print(acad.app.Documents)
for i in acad.app.Documents:
    print(i.Name)

# check the state of
print(acad.app.GetAcadState().IsQuiescent)

# close drawing file and exist application
acad.app.Quit()

# update the application
acad.app.Update()

# specify x and y coordinates of circle center point
point1 = APoint(100.0,100.0) # x and y coordinates of points
# add circle to drawing
circle1 = acad.model.AddCircle(point1,100)
circle2 = acad.model.AddCircle(APoint(200.0,200.0),100)
circle3 = acad.model.AddCircle(APoint(300.0,300.0),100)
# change color of circle to red
circle1.Color = 10 # 10 is a red color
# check layer assignment
print("current layer: "  + str(circle1.Layer))
# check current linetype
print("current linetype: " + str(circle1.Linetype))
# check linetype scale
print("current linetype scale: " + str(circle1.LinetypeScale))
# check current line weight
print("current line weight: " + str(circle1.Lineweight))
# check current thickness
print("current thickness: " + str(circle1.Thickness))
# check current material
print("current material:" + str(circle1.Material))


# pyautocad Add()-method  
# object.Add(Name)
acad.doc.Layers.Add(layer_name)

# Add block to AutoCAD
object.Add(Insertion_Point, Block_Name)
b1 = acad.doc.Blocks.Add(ip, "Test_block_1")
l1 = b1.AddLine(APoint(100, 100, 0), APoint(350, 350, 0))
c1 = b1.AddCircle(APoint(200, 250, 0), 150)

# insert block at InsertPoint
object.InsertBlock(InsertionPoint, Name , Xscale , Yscale , ZScale , Rotation , Password)
acad.model.InsertBlock(APoint(250, 500, 0), "Test_block_1", 1, 1, 1, 0)

#Rotate the polygon
polygond = polygond.Rotate(APoint(100, 25, 0), 3.14*185/180)

acad.app.ZoomExtents()


c2 = c1.Copy()
#obj.Move(previous location, new location)
c2.Move(APoint(100, 100), APoint(300, 300))

l2 = l1.Copy()
# obj.Rotate(Base point, Angle of rotation)
l2.Rotate(APoint(100,100), pi*90/180)

el2 = el1.Offset(10)

# obj.ScaleEntity(Base point, Scaling factor)
c3 = c2.ScaleEntity(APoint(300, 300), 0.5)

l2.Highlight(True) 

'''
p1 = APoint(0, 0)
p2 = APoint(50, 25)
for i in range(5):
    text = acad.model.AddText('Hi %s!' % i, p1, 2.5)
    acad.model.AddLine(p1, p2)
    acad.model.AddCircle(p1, 10)
    p1.y += 10

dp = APoint(10, 0)
for text in acad.iter_objects('Text'):
    print('text: %s at: %s' % (text.TextString, text.InsertionPoint))
    text.InsertionPoint = APoint(text.InsertionPoint) + dp

for obj in acad.iter_objects(['Circle', 'Line']):
    print(obj.ObjectName)
'''
