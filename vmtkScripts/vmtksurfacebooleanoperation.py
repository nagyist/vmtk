#!/usr/bin/env python

## Program:   VMTK
## Module:    $RCSfile: vmtksurfacebooleanOperation.py,v $
## Language:  Python
## Date:      $Date: 2005/09/14 09:49:59 $
## Version:   $Revision: 1.7 $

##   Copyright (c) Luca Antiga, David Steinman. All rights reserved.
##   See LICENCE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even 
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
##      PURPOSE.  See the above copyright notices for more information.


import vtk
import vtkvmtk
import sys

import pypes

vmtksurfacebooleanoperation = 'vmtkSurfaceBooleanOperation'

class vmtkSurfaceBooleanOperation(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)
        
        self.Surface = None
        self.Surface2 = None

        self.Tolerance = 1E-6
        self.Operation = 'union'

        self.SetScriptName('vmtksurfacebooleanoperation')
        self.SetScriptDoc('perform a boolean operation between two surfaces')
        self.SetInputMembers([
            ['Surface','i','vtkPolyData',1,'','the input surface','vmtksurfacereader'],
            ['Surface2','i2','vtkPolyData',1,'','the second input surface','vmtksurfacereader'],
            ['Tolerance','tolerance','float',1,'(0.0,)','tolerance for considering two points coincident'],
            ['Operation','operation','str',1,'["union","intersection","difference"]','the boolean operation to be performed']
            ])
        self.SetOutputMembers([
            ['Surface','o','vtkPolyData',1,'','the output surface','vmtksurfacewriter']
            ])

    def Execute(self):

        if self.Surface == None:
            self.PrintError('Error: No Surface.')

        if self.Surface2 == None:
            self.PrintError('Error: No Surface2.')

        booleanOperationFilter = vtk.vtkBooleanOperationPolyDataFilter()
        booleanOperationFilter.SetInput(0,self.Surface)
        booleanOperationFilter.SetInput(1,self.Surface2)
        if self.Operation == 'union':
            booleanOperationFilter.SetOperationToUnion()
        elif self.Operation == 'intersection':
            booleanOperationFilter.SetOperationToIntersection()
        elif self.Operation == 'difference':
            booleanOperationFilter.SetOperationToDifference()
        booleanOperationFilter.SetTolerance(self.Tolerance)
        booleanOperationFilter.Update()

        self.Surface = booleanOperationFilter.GetOutput()

        if self.Surface.GetSource():
            self.Surface.GetSource().UnRegisterAllOutputs()

if __name__=='__main__':
    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()
