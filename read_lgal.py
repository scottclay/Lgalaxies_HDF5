import numpy as np
import os


###############################################
# Code to read the INPUT trees for L-Galaxies #
###############################################

def read_snap(folder,file_prefix,firstfile,lastfile,props,template):
    """ Reads L-Galaxy output files.
    Returns: (nTrees,nHalos,nTreeHalos,gals)
    Inputs: (folder,file_prefix,firstfile,lastfile,props,template)
    props - list of properties to return
    template - structure dtype definition for database """
    filter_list = []
    for prop in props:
        if props[prop]:
            filter_list.append((prop,template[prop]))
    filter_dtype = np.dtype(filter_list)
    # First loop to determine how many galaxies there are:
    nTrees = 0
    nHalos = 0
    for ifile in range(firstfile,lastfile+1):
        filename = folder+'/'+file_prefix+"_"+"%d"%(ifile)
        f = open(filename,"rb")
        this_nTrees =  np.fromfile(f,np.int32,1)[0]
        nTrees += this_nTrees
        this_nHalos = np.fromfile(f,np.int32,1)[0]
        nHalos += this_nHalos
        f.close()
    # Allocate arrays
    print("Total nGals = ",nHalos)
    nTreeHalos = np.empty(nTrees,dtype=np.int32)
    gals = np.empty(nHalos,dtype=filter_dtype)
    # Second loop to populate arrays
    nTrees = 0
    nHalos = 0
    for ifile in range(firstfile,lastfile+1):
        filename = folder+'/'+file_prefix+"_"+"%d"%(ifile)
        f = open(filename,"rb")
        this_nTrees =  np.fromfile(f,np.int32,1)[0]
        this_nHalos = np.fromfile(f,np.int32,1)[0]
        print("File ", ifile," nGals = ",this_nHalos)
        addednTreeHalos = np.fromfile(f,np.int32,this_nTrees)
        nTreeHalos[nTrees:nTrees+this_nTrees]=addednTreeHalos
        this_addedGalaxy = np.fromfile(f,template,this_nHalos) # all properties
        addedGalaxy = np.empty(this_nHalos,dtype=filter_dtype) # selected props
        for prop in template.names:
            if props[prop]:
#                try:
                addedGalaxy[prop] = this_addedGalaxy[prop]
#                except:
#                    embed()
        gals[nHalos:nHalos+this_nHalos] = addedGalaxy
        nTrees += this_nTrees
        nHalos += this_nHalos
        f.close()
    return (nTrees,nHalos,nTreeHalos,gals)
