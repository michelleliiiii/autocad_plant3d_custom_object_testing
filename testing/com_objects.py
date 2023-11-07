import pythoncom

context = pythoncom.CreateBindCtx(0)

# get running object table
running_coms = pythoncom.GetRunningObjectTable()

monikers = running_coms.EnumRunning()
acad = False

for moniker in monikers:
    print('-'*100)
    print(moniker.GetDisplayName(context, moniker))
    #print(moniker.Hash())
    print(moniker.IsSystemMoniker())
    if moniker.GetDisplayName(context, moniker) == "!{8B4929F8-076F-4AEC-AFEE-8928747B7AE3}":
        acad = True

print(acad)


#help(running_coms)
