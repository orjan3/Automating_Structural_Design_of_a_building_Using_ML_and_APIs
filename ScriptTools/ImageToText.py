import os
import sys
import clr

clr.AddReference("System.Runtime.InteropServices")
from System.Runtime.InteropServices import Marshal

#set the following path to the installed ETABS program directory
clr.AddReference(R'C:\Program Files\Computers and Structures\ETABS 20\ETABSv1.dll')
from ETABSv1 import *

#set the following flag to True to execute on a remote computer
Remote = False

#if the above flag is True, set the following variable to the hostname of the remote computer
#remember that the remote computer must have ETABS installed and be running the CSiAPIService.exe
RemoteComputer = "SpareComputer-DT"

#set the following flag to True to attach to an existing instance of the program
#otherwise a new instance of the program will be started
AttachToInstance = True

#set the following flag to True to manually specify the path to ETABS.exe
#this allows for a connection to a version of ETABS other than the latest installation
#otherwise the latest installed version of ETABS will be launched
SpecifyPath = True

#if the above flag is set to True, specify the path to ETABS below
ProgramPath = "C:\Program Files\Computers and Structures\ETABS 20\ETABS.exe"

#full path to the model
#set it to the desired path of your model
APIPath = 'C:\CSi_ETABS_API_Example'
if not os.path.exists(APIPath):
    try:
        os.makedirs(APIPath)
    except OSError:
        pass
ModelPath = APIPath + os.sep + 'API_1-001.edb'

#create API helper object
helper = cHelper(Helper())

if AttachToInstance:
    #attach to a running instance of ETABS
    try:
        #get the active ETABS object        
        if Remote:
            myETABSObject = cOAPI(helper.GetObjectHost(RemoteComputer, "CSI.ETABS.API.ETABSObject"))
        else:
            myETABSObject = cOAPI(helper.GetObject("CSI.ETABS.API.ETABSObject"))
    except:
        print("No running instance of the program found or failed to attach.")
        sys.exit(-1)

else:
    if SpecifyPath:
        try:
            #'create an instance of the ETABS object from the specified path
            if Remote:
                myETABSObject = cOAPI(helper.CreateObjectHost(RemoteComputer, ProgramPath))
            else:
                myETABSObject = cOAPI(helper.CreateObject(ProgramPath))
        except :
            print("Cannot start a new instance of the program from " + ProgramPath)
            sys.exit(-1)
    else:

        try: 
            #create an instance of the ETABS object from the latest installed ETABS
            if Remote:
                myETABSObject = cOAPI(helper.CreateObjectProgIDHost(RemoteComputer, "CSI.ETABS.API.ETABSObject"))
            else:
                myETABSObject = cOAPI(helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject"))

        except:
            print("Cannot start a new instance of the program.")
            sys.exit(-1)



#create SapModel object
SapModel = cSapModel(myETABSObject.SapModel)

#initialize model
SapModel.InitializeNewModel()

#create new blank model
File = cFile(SapModel.File)
ret = File.NewBlank()

#define material property

ret = SapModel.PropMaterial.SetMaterial("Concrete", eMatType.Concrete)

