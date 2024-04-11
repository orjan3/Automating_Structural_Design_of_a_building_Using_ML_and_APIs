import os
import sys
import comtypes.client
from my_functions import *

# Connect to ETABS
ETABSModel, myETABSObject, helper = Conect_Etabs()
ETABSModel.File.NewBlank()

# Define units
kgf_m_C = 8
ETABSModel.SetPresentUnits(kgf_m_C)

# Define materials

## Concrete
ETABSModel.PropMaterial.SetMaterial('Concrete210', 2) # 2: Concrete
E = 15000*(210**0.5)*10000
ETABSModel.PropMaterial.SetMPIsotropic('Concrete210', E, 0.2, 9.90E-06) # E: Modulus of elasticity, 0.2: Poisson's ratio, 9.90E-06: Coefficient of thermal expansion
ETABSModel.PropMaterial.SetWeightAndMass('Concrete210', 1, 2400) # 1: Weight per unit volume is specified, 2400: Weight per unit volume

## Steel
ETABSModel.PropMaterial.SetMaterial('RebarSteel', 6) # 6: Rebar steel
Fy = 4200 # Yield strength
ETABSModel.PropMaterial.SetMPIsotropic('RebarSteel', 2.0E10, 0.2, 9.90E-06) # 2.0E10: Modulus of elasticity, 0.2: Poisson's ratio, 9.90E-06: Coefficient of thermal expansion
ETABSModel.PropMaterial.SetWeightAndMass('RebarSteel', 1, 7850) # 1: Weight per unit volume is specified, 7850: Weight per unit volume
ETABSModel.PropMaterial.SetORebar("RebarSteel", 42000000, 63000000, 
                                  46000000, 69000000, 
                                  2, 2, 0.02, 0.1, False) # 42000000: Fy, 63000000: Fu, 46000000: Fy, 69000000: Fu, 2: Fy, 2: Fu, 0.02: Strain at Fy, 0.1: Strain at Fu, False: Is rebar


# Define sections

## Column
### Rectangular section
ETABSModel.PropFrame.SetRectangle('CR', 
                                  'Concrete210', 
                                  0.45, 0.45) # 'CR': Section name, 'Concrete210': Material name, 0.45: Width, 0.45: Depth

### Circular section
ETABSModel.PropFrame.SetCircle('CC', 
                               'Concrete210', 
                               0.40) # 'CC': Section name, 'Concrete210': Material name, 0.40: Diameter

## Beam
### Rectangular section
ETABSModel.PropFrame.SetRectangle('BR', 
                                  'Concrete210', 
                                  0.30, 0.60) # 'BR': Section name, 'Concrete210': Material name, 0.30: Width, 0.60: Depth

## Slab
ETABSModel.PropArea.SetSlab('Losa',
                            0,
                            2,
                            'Concrete210',
                            0.20) # 'Slab': Section name, 0: Slab, 1: Shell Thick, 'Concrete210': Material name, 0.20: Thickness


# Define frame objects
h = 3 # Height

coord_dict = {'A': [0, 0, 0], 'B': [10, 0, 0], 'C': [5, 4, 0], 'D': [0, 4, 0],  # First floor
              'E':[0,0,h], 'F':[10,0,h], 'G':[5,4,h], 'H':[0,4,h]}              # Second floor



## Columns
[Column1, _] = ETABSModel.FrameObj.AddByCoord(coord_dict['A'][0], coord_dict['A'][1], coord_dict['A'][2],
                               coord_dict['E'][0], coord_dict['E'][1], coord_dict['E'][2],
                               '', 
                               'CR') # 'A': Start point, 'E': End point, '': Section name, 'C1': Section property name

[Column2, _] = ETABSModel.FrameObj.AddByCoord(coord_dict['B'][0], coord_dict['B'][1], coord_dict['B'][2],
                                 coord_dict['F'][0], coord_dict['F'][1], coord_dict['F'][2],
                                 '', 
                                 'CR') # 'B': Start point, 'F': End point, '': Section name, 'C1': Section property name

[Column3, _] = ETABSModel.FrameObj.AddByCoord(coord_dict['C'][0], coord_dict['C'][1], coord_dict['C'][2],
                               coord_dict['G'][0], coord_dict['G'][1], coord_dict['G'][2],
                               '',
                               'CC') # 'C': Start point, 'G': End point, '': Section name, 'C1': Section property name

[Column4, _] = ETABSModel.FrameObj.AddByCoord(coord_dict['D'][0], coord_dict['D'][1], coord_dict['D'][2],
                                 coord_dict['H'][0], coord_dict['H'][1], coord_dict['H'][2],
                                 '',
                                 'CC') # 'D': Start point, 'H': End point, '': Section name, 'C1': Section property name

## Beams
[Beam1, _] = ETABSModel.FrameObj.AddByCoord(coord_dict['E'][0], coord_dict['E'][1], coord_dict['E'][2],
                                coord_dict['F'][0], coord_dict['F'][1], coord_dict['F'][2],
                                '',
                                'BR') # 'E': Start point, 'F': End point, '': Section name, 'B1': Section property name

[Beam2, _] = ETABSModel.FrameObj.AddByCoord(coord_dict['F'][0], coord_dict['F'][1], coord_dict['F'][2],
                                coord_dict['G'][0], coord_dict['G'][1], coord_dict['G'][2],
                                '',
                                'BR') # 'F': Start point, 'G': End point, '': Section name, 'B1': Section property name

[Beam3, _] = ETABSModel.FrameObj.AddByCoord(coord_dict['G'][0], coord_dict['G'][1], coord_dict['G'][2],
                                coord_dict['H'][0], coord_dict['H'][1], coord_dict['H'][2],
                                '',
                                'BR') # 'G': Start point, 'H': End point, '': Section name, 'B1': Section property name

[Beam4, _] = ETABSModel.FrameObj.AddByCoord(coord_dict['H'][0], coord_dict['H'][1], coord_dict['H'][2],
                                    coord_dict['E'][0], coord_dict['E'][1], coord_dict['E'][2],
                                    '',
                                    'BR') # 'H': Start point, 'E': End point, '': Section name, 'B1': Section property name
                    

## Slabs
x_list = [coord_dict['F'][0], coord_dict['G'][0], coord_dict['H'][0], coord_dict['E'][0]]
y_list = [coord_dict['F'][1], coord_dict['G'][1], coord_dict['H'][1], coord_dict['E'][1]]
z_list = [coord_dict['F'][2], coord_dict['G'][2], coord_dict['H'][2], coord_dict['E'][2]]

ETABSModel.AreaObj.AddByCoord(4,
                              x_list, 
                              y_list, 
                              z_list, 
                              '', 
                              'Losa')

ETABSModel.View.RefreshView(0, False)


# Define loads
ETABSModel.LoadPatterns.Add('FH',
                            8,
                            0,
                            True)

ETABSModel.LoadPatterns.Add('CV',
                            3,
                            0,
                            True)

ETABSModel.LoadPatterns.Add('Carga Muerta',
                            2,
                            0,
                            True)

ETABSModel.LoadPatterns.Add('Carga Viva de Piso',
                            4,
                            0,
                            True)

ETABSModel.LoadPatterns.Add('Carga Viva de Techo',
                            11,
                            0,
                            True)

# Cambiar nombre de Load Pattern
ETABSModel.LoadPatterns.ChangeName("DEAD", "Peso Propio")
ETABSModel.LoadCases.ChangeName("DEAD","Peso Propio")

# Add Mass Source
Mass_Loads = ["Carga Muerta", "Peso Propio", "Carga Viva de Piso", "Carga Viva de Techo"]
ETABSModel.PropMaterial.SetMassSource(3, len(Mass_Loads), Mass_Loads, [1.0, 1.0, 0.5, 0.5])

# Add X-axis Load at top of each column
PointForce = [10, 0, 0, 0, 0, 0]
Restraints = [True, True, True, True, True, True]
Col_list = [Column1, Column2, Column3, Column4]

for i in range(4):
    [Point1, Point2, _] = ETABSModel.FrameObj.GetPoints(Col_list[i], '', '')
    ETABSModel.PointObj.SetLoadForce(Point2, 'FH', PointForce) # Add load at top of each column
    ETABSModel.PointObj.SetRestraint(Point1, Restraints) # Add restrains at base of each column

# Distribute loads gravity at all beams
q = 100 # kgf/m
Beam_list = [Beam1, Beam2, Beam3, Beam4]

for i in range(4):
    ETABSModel.FrameObj.SetLoadDistributed(Beam_list[i], 'CV', 1, 10, 0, 1, q, q, 'Global', True, True)


# Define combinations
ETABSModel.RespCombo.Add('Combination1', 0)
ETABSModel.RespCombo.Add('Combination2', 0)

# Combination1
Load_names = ['Carga Muerta', 'Carga Viva de Piso']
Load_factors = [1.4, 1.7]
for i in range(len(Load_names)):
    ETABSModel.RespCombo.SetCaseList('Combination1', 0, Load_names[i], Load_factors[i])

# Combination2
Load_names = ['Carga Muerta', 'Peso Propio', 'Carga Viva de Piso', 'Carga Viva de Techo']
Load_factors = [1.0, 1.0, 0.5, 0.5]
for i in range(len(Load_names)):
    ETABSModel.RespCombo.SetCaseList('Combination2', 0, Load_names[i], Load_factors[i])

# Save model
ETABSModel.File.Save(r'C:\Users\kurt-\Desktop\UC Berkeley\Spring 2024\API ETABS + Python\Tarea\Tarea1.edb')

