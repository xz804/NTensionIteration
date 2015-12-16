
def WriteToGid(istep, FemInf):

    Node_xy = FemInf.Node_xy
    Elem    = FemInf.Elem
    U_tot   = FemInf.U_tot
    Eps     = FemInf.Eps
    Phase   = FemInf.Phase
    Hmax    = FemInf.Hmax



    Nnode = int(Node_xy.shape[0])
    Nelem = int(Elem.shape[0])
    NGP   = 3

    ####### Write information to *.msh

    file_msh = "gid_result"+str(istep)+".post.msh"

    f_index01 = file(file_msh,'w')

    f_index01.write('# Maillage GiD\n')

    f_index01.write('MESH "" dimension 2 ElemType Triangle Nnode 6\n')

    f_index01.write('Coordinates\n'
                    '# node number  coordinate_x   coordinate_y\n')

    for i in range(Nnode):
        f_index01.write('%d   %f   %f\n'% (Node_xy[i,0], Node_xy[i,1], Node_xy[i,2]))

    f_index01.write('end coordinates\n')

    f_index01.write('Elements\n')

    for i in range(Nelem):
        f_index01.write('%d  %d  %d  %d  %d  %d  %d\n'% (Elem[i,0], Elem[i,1], Elem[i,2], Elem[i,3], Elem[i,4], Elem[i,5], Elem[i,6]))

    f_index01.close()


    ####### Write information to *.res

    file_res = "gid_result"+str(istep)+".post.res"

    f_index02 = file(file_res,'w')

    f_index02.write('GiD Post Results File 1.0\n')
    f_index02.write('GaussPoints "3P-Gauss" ElemType Triangle\n'
                     'Number of Gauss Points: 3\n'
                     'Natural Coordinates: Given\n'
                     '0.666667   0.166667\n'
                     '0.166667   0.666667\n'
                     '0.166667   0.166667\n'
                     'End gausspoints\n')

    #  write displacements
    tem_str = 'Result "Displacements" "Rock" '+str(istep)+' Vector OnNodes'
    f_index02.write(tem_str)
    f_index02.write('\n')
    f_index02.write('ComponentNames "Ux_tot", "Uy_tot"\n'
                     'Values\n')

    for i in range(Nnode):
        f_index02.write("%d  %f  %f\n" % (i+1,U_tot[2*i],U_tot[2*i+1]))

    f_index02.write('End Values\n')


    #  write Phase field
    tem_str = 'Result "Phase-Field" "Rock" '+str(istep)+' Scalar OnNodes'
    f_index02.write(tem_str)
    f_index02.write('\n')
    f_index02.write('ComponentNames "Phase_Sn"\n'
                     'Values\n')

    for i in range(Nnode):
        f_index02.write("%d  %f\n" % (i+1,Phase[i]))

    f_index02.write('End Values\n')


    # write strains
    tem_str = 'Result "Strain" "Rock" '+str(istep)+' Vector OnGaussPoints "3P-Gauss"'
    f_index02.write(tem_str)
    f_index02.write('\n')
    f_index02.write('ComponentNames "EpsXX", "EpsYY", "EpsZZ", "EpsXY"\n'
                     'Values\n')
    for i in range(Nelem):
        f_index02.write("%d  " % (i+1))
        for j in range(NGP):
            f_index02.write("%f  %f  %f  %f\n" % (Eps[i,4*j], Eps[i,4*j+1], Eps[i,4*j+2], Eps[i,4*j+3]))

    f_index02.write('End Values\n')

    # write Hmax
    tem_str = 'Result "Hmax" "Rock" '+str(istep)+' Scalar OnGaussPoints "3P-Gauss"'
    f_index02.write(tem_str)
    f_index02.write('\n')
    f_index02.write('ComponentNames "H"\n'
                     'Values\n')
    for i in range(Nelem):
        f_index02.write("%d  " % (i+1))
        for j in range(NGP):
            f_index02.write("%f \n" % (Hmax[i,j]))

    f_index02.write('End Values\n')


    f_index02.close()