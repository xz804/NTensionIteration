# -*- coding: utf-8 -*-
"""
Created on Mon Nov 02 08:58:06 2015

@author: xz804
"""

import os
import PhaFra
import numpy as np
import datetime, time

def main():
    print "Current working dir: %s \n" % os.getcwd()

    #------  Mesh node and Mesh element information stored in DataStructFem
    Node_xy, Elem = PhaFra.ReadInp("CrackNotched.inp")

    FemInf   = PhaFra.DataStruct.DataStructFem('Tri6',Node_xy,Elem)

    #-----   Material information stored in DataStructMaterial
    E        = 210.
    Gamma    = 0.3
    Density  = 0.
    ProbType = "PlaneStress"
    PhaseType = "PhaseIso"
    GcI      = 2.7e-3
    GcII     = GcI
    Lc       = 0.0075
    PhaseEta = 0
    MatInf = PhaFra.DataStruct.DataStructMaterial(E,Gamma,Density,GcI,GcII,Lc,PhaseEta,ProbType,PhaseType)

    #-----   Boundary Condition information stored in DataStructFem
    UBound = []
    for inode in range(int(Node_xy.shape[0])):
        if  Node_xy[inode,2]<1e-5:
            UBound.append([inode,"Uy",0.])
        elif Node_xy[inode,2]>0.999999:
            UBound.append([inode,"Uy",1e-5])
    FemInf.UBound = UBound
    #-----   Macro control information stored in DataStructMacro
    MacroInf = PhaFra.DataStruct.DataStructMacro()

    now = time.strftime("%Y-%m-%d %H:%M:%S")
    MacroInf.File_Time.write(now)
    MacroInf.File_Time.write('\n')



    ###########################################################
    print ("Initialization  ----  completed \n")
    ###########################################################

    nstep = 310

    for istep in range(nstep):

        NUBound = len(UBound)
        if istep<50:
            for i in range(NUBound):
                if  FemInf.UBound[i][2] >1e-9:
                    FemInf.UBound[i][2] = 1e-4*(istep+1)
        else:

            for i in range(NUBound):
                if  FemInf.UBound[i][2] >1e-9:
                    FemInf.UBound[i][2] = 1e-5*(istep-49)+0.005

        FemInf = PhaFra.SolFractureElasStatics(FemInf,MatInf,MacroInf)


        if ((istep<50 and istep%1 == 0) or istep%10 == 0):
            PhaFra.WriteToGid(istep, FemInf)


        print ("========istep = %d completed=========" % (istep))

    now = time.strftime("%Y-%m-%d %H:%M:%S")
    MacroInf.File_Time.write(now)

    MacroInf.FileClose()

if __name__ == "__main__":
    main()
