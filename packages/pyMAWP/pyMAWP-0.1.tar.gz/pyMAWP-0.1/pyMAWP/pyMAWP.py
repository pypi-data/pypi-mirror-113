#!/usr/bin/env python
# coding: utf-8
# pyMAWP.py

# import numpy as np
import pandas as pd
# import math
# import scipy as sp
# import copy
from scipy import interpolate



class MAWP:
    ourVessels = [] # string for file name with our vessel info
    vesselData = [] # df to hold the vessel data
    # reference data
    flangeTables = pd.read_excel("./pyMAWP/dataMAWP_0.xlsx", sheet_name="flangeTables")
    materialStress = pd.read_excel("./pyMAWP/dataMAWP_0.xlsx", sheet_name="materialStress")
    def __init__(self, filename): # constructor
        self.ourVessels = filename
        self.vesselData = pd.read_excel(self.ourVessels, sheet_name="vessel")

        # first, fetch some values for max allowable stress and flange limits
        # use the temperature to interpolate from table
        self.vesselData['stress_kpa'] = 0.0

        for i,row in self.vesselData.iterrows():
            self.vesselData.at[i,"stress_kpa"] = interpolate.interp1d(self.materialStress[self.materialStress['material']==row['material']].T_C,
                                                                          self.materialStress[self.materialStress['material']==row['material']].stress_kpa, 'linear')(row['designTemp_C'])
    # end of init function
    #
    def getMAWP(self):
        # for each of the rows where findThis is MAWP, calculate P
        # use brute force
        for i,row in self.vesselData.iterrows():
            if (row['findThis'] == 'MAWP'):
                self.vesselData.at[i,"MAWP_kPa"] = row["stress_kpa"]*row["qualityFactor"]/(0.5*row["ID_mm"]/(0.875*row["wallThickness_mm"] - row["corrosionAllowance"]) - 0.4)
            if (row['findThis'] == 'wallThickness'):
                self.vesselData.at[i,"wallThickness_mm"] = (row["ID_mm"] / (2*row["stress_kpa"]*row["qualityFactor"]/row["MAWP_kPa"] + 0.4) + row["corrosionAllowance"])/0.875
        return()







