# -*- coding: utf-8 -*-
"""
This program takes tide guage data and creates a time of inundation for a 
series of elevations.

Created on Wed Jan 11 07:57:47 2017

@author: smudd
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import rcParams

def Inundation_tool(FileName):
    #First we need to load the tide data
    HourlyData = ParseMalaysianTideRecord(FileName)
    
    elev = np.linspace(0,400,81)
    print("Elevations are: ")    
    print(elev)
    
    [inundation_times,inundation_fractions] = CalculateInundationSimple(elev, HourlyData)
    PlotInundationFraction(elev,inundation_fractions)

def ParseMalaysianTideRecord(FileName):
    #See if the parameter files exist
    if os.access(FileName,os.F_OK):
        this_file = open(FileName, 'r')
        lines = this_file.readlines()
    else:
        print("FILE DOES NOT EXIST, ending program. Check your filename.")
        
    
    # first read the header
    Line = lines[1]
    location = Line.split(',')
    location = location[0]
    
    Line = lines[2]
    GagueNumber = Line.split(',')
    GagueNumber = GagueNumber[4]
    
    Line = lines[3]
    Year = Line.split(',')
    Year = Year[4]

    # Now remove the header
    del lines[0:4]
    
    print lines[0]

    # print the results
    print("Here is the gague information: ")
    print("location: "+location)
    print("GagueNumber: "+GagueNumber)
    print("Year: "+Year)
    
    # now get the number of lines left 
    print("The number of lines are: "+ str(len(lines)))
    print("The number of months are: "+ str(len(lines)/33))
    
    HourlyData = GetHourlySeriesFromLines(lines)
    #print("The number of days are: "+ str(len(HourlyData)))
    return HourlyData
    
def GetHourlySeriesFromLines(lines):
    # This reads the data into a time series that has days as the rows 
    # and hours as the column. It converts string information into integer information
    HourlyData = []
    #day = -1    
    for Line in lines:
        data = Line.split(',')
        
        # Check to see if this is a line containing data
        # 
        if ((data[0] != "Monthly") & (data[0] != "DAY")):
            
            # it is data. Get rid of the first element since this just is the day of the month            
            del data[0]
            del data[-1]
            
            # Start a new vector
            this_vector = []
            
            # Convert the data to integer data (these are mm values for the tide)
            for datum in data:
                this_vector.append(int(datum))
            
            # Add the vector to the main data value
            HourlyData.append(this_vector)
            
        #else:
            # It isn't data. Say so
            #print("No data on this line, the first element is: "+ data[0])  
            
    #print(HourlyData)
        
    return HourlyData
        
def CalculateInundationSimple(elevations, HourlyData):
    # This function calculates the inundation in a very simple way, simply 
    # adding an hour to the total inundation if the tidal stage is greater than
    # the elevation

    # it is a bit easier to flatten the vector of data
    FlattenedHourlyData = []    
    for day in HourlyData:
        #print "Day: "
        #print day
        FlattenedHourlyData.extend(day)
        
    print FlattenedHourlyData
    
    # Turn lists into arrays for efficient data processing
    FHD = np.asarray(FlattenedHourlyData)
    z = np.asarray(elevations)
    
    total_inundation = np.zeros(len(z))
    
    total_hours = 0
    # now go through each hourly data point and add
    for datum in FHD:
        if datum != 0:
            total_hours=total_hours+1           
            greater_list = np.less_equal(z,datum)
            
            for i, isTrue in enumerate(greater_list):
                if(isTrue):
                    total_inundation[i] = total_inundation[i]+1
                
    
    print("Innundation times: ")
    print(total_inundation)

    inundation_fraction = np.divide(total_inundation,total_hours)
    print("Inundation fraction: ")
    print(inundation_fraction)        
    return total_inundation,inundation_fraction
    
def PlotInundationFraction(elevations,inundation_fraction):
 
    label_size = 10
    #title_size = 30
    axis_size = 12

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = label_size

    # make a figure, sized for a ppt slide
    fig = plt.figure(1, facecolor='white',figsize=(4.92126,3.5))

    gs = plt.GridSpec(100,100,bottom=0.25,left=0.1,right=1.0,top=1.0)
    ax = fig.add_subplot(gs[25:100,10:95])
    
    plt.plot(inundation_fraction,elevations)

    ax.spines['top'].set_linewidth(1)
    ax.spines['left'].set_linewidth(1)
    ax.spines['right'].set_linewidth(1)
    ax.spines['bottom'].set_linewidth(1)     
 
    ax.set_xlabel("Fraction of time inundated")
    ax.set_ylabel("Elevation above datum (mm)")

    plt.show()         

if __name__ == "__main__":
    FileName = "C:\\Users\\smudd\\students\\ghazali\\CENDERING2015.csv"
    Inundation_tool(FileName)
