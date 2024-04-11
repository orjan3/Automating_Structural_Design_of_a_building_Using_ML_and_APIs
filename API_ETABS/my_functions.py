import os
import sys
import comtypes.client
import numpy as np

def Conect_Etabs(path=None):
    # Create a helper object
    helper = comtypes.client.CreateObject('ETABSv1.Helper')
    helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
    try:
        # Try to get the active ETABS object
        myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        SapModel = myETABSObject.SapModel
    except(OSError, comtypes.COMError):
        # If no active ETABS object, create a new one
        myETABSObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject") 
        myETABSObject.ApplicationStart()
        SapModel = myETABSObject.SapModel
        SapModel.InitializeNewModel()

    # Open an existing ETABS file
    if path is not None:
        ret = SapModel.File.OpenFile(path)
        if ret != 0:
            print("Error opening ETABS file")
    return SapModel,myETABSObject,helper;

def Conect_Sap2000():
    helper = comtypes.client.CreateObject('SAP2000v1.Helper')
    helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
    mySapObject = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
    mySapObject.ApplicationStart()
    SapModel = mySapObject.SapModel
    SapModel.InitializeNewModel()
    return SapModel,mySapObject,helper;