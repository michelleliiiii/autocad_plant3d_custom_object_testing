import win32com.client

acad = win32com.client.gencache.EnsureDispatch("{8B4929F8-076F-4AEC-AFEE-8928747B7AE3}")



#doc = acad.ActiveDocument   # Document object
print(dir(acad))
print(acad.Visible)

#acad.Documents.Open("X:\AutoCAD\Plant 3D\Scripting_Test\Plant 3D Models\TEST1.dwg")
#help(acad)
'''
for entity in acad.ActiveDocument.ModelSpace:
    name = entity.EntityName
    print(name)
    print(entity.Layer)
    print(entity.ObjectID)

    print(entity.GetBoundingBox())

'''

















'''
# iterate trough all objects (entities) in the currently opened drawing
# and if its a BlockReference, display its attributes and some other things.
for entity in acad.ActiveDocument.ModelSpace:
    print ("!")
    name = entity.EntityName
    print (name)
    print(entity.Layer)
    print(entity.ObjectID)
    if name == 'AcDbBlockReference':
        HasAttributes = entity.HasAttributes
        if HasAttributes:
            print(entity.Name)
            print(entity.Layer)
            print(entity.ObjectID)
            for attrib in entity.GetAttributes():
                print("  {}: {}".format(attrib.TagString, attrib.TextString))
                
                # update text
                attrib.TextString = 'modified with python'
                attrib.Update()
'''