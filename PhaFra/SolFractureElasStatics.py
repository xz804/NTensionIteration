# -*- coding: utf-8 -*-
"""
Created on Mon Nov 02 09:00:45 2015

@author: xz804
"""

import numpy as np

from scipy.linalg import *

import SolElasStatics as SolFEM
import SolPhaseField  as SolPha
#from DataStruct import *


def SolFractureElasStatics(FemInf,MatInf,MacroInf):
    """
    read Abaqus-generated inp file

    Call ReadNode
    Call ReadElement

    Node_info       node information
    Element_info    element information
    """

    Iter = 0
    FlagIter = True
    while (FlagIter):

        #-----  solve Elastic Static Problem in 2D
        FemInf = SolFEM.SolElasStatics(FemInf,MatInf,MacroInf)

        PhaseN = FemInf.Phase

        #------ solve Phase Field
        FemInf = SolPha.SolPhaseField(FemInf,MatInf,MacroInf)


        ErrorS = norm(PhaseN-FemInf.Phase)

        print("Iter no. = %d,  Max Iter  = %d  \n" % (Iter,   MacroInf.IterMax))
        print("Error S  = %f,  Tolerance = %f  \n" % (ErrorS, MacroInf.IterTol))

        Iter = Iter +1

        if Iter >= MacroInf.IterMax or ErrorS < MacroInf.IterTol:
            FlagIter = False


    return FemInf
    
    
    
    
