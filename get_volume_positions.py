import fire
import numpy as np
import ROOT
import csv

def get_volume_position(input_file, isROOT, volName):
    """
    Function that calls a ROOT cpp macro that calculates the module offsets from
    an edep-sim ROOT file OR geometry GDML.
    
    Will return an empty list if the active LAr volumes are not found.
    Note that the cpp script has a handful of hard-coded volume names in order to find the module
    offsets. So if the script isn't finding the offsets, you should check the cpp script and the
    GDML and make sure it's looking for the right volumes.
    
    Args:
        input_file (str): path to an input ROOT file
        isROOT (bool): True if input file is ROOT file, False if not (i.e. GDML)
    """
    foundTGeoManager, global_origins = ROOT.get_volume_position(input_file, isROOT, volName)
    if not foundTGeoManager:
        print(f'No TGeoManager found in {input_file}, cannot get module offsets.')
        return None
    elif foundTGeoManager:
        # Convert the result to a Python list
        global_origins_list = [[global_origins.at(i).at(j) for j in range(global_origins.at(i).size())] for i in range(global_origins.size())]
        return global_origins_list

def main(input_file):
    if input_file.split('.')[-1] == 'root':
        isROOT = True
    else:
        isROOT = False
    ROOT.gROOT.ProcessLine('.L get_volume_position.cpp')
    volumes = ['volTPCActive', 'volLArBath', 'volLAr']
    for volName in volumes:
        module_offsets_GDML = get_volume_position(input_file, isROOT, volName)
        for pos in module_offsets_GDML:
            print(f'position of volume {volName} = {pos}'+'\n')    
        if module_offsets_GDML is not None and len(module_offsets_GDML) == 0:
            print(f'Volume {volName} not found in TGeoManager of input file, check volume name.')
    #print(f'module offsets = {module_offsets_GDML}')

if __name__ == "__main__":
    fire.Fire(main)
