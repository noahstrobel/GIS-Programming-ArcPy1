# Name: Noah Strobel

# Class: GISC-450 Spring 2021

# Created: 03/18/2021

# Purpose: This program reads in shapefile data, creates a geodatabase named "Strobel_ArcPy1",
# clips those shapefiles to Virginia Planning District 11, then extracts them to the newly-created geodatabase as
# feature classes. Additionally, the program creates a 5-mile buffer around landfills within the specified planning
# district. All geospatial functions are completed using arcpy.


import arcpy
import time
import os

time_start = time.time()


arcpy.env.overwriteOutput = True


def main():

    # Starting the program and printing its explanation

    print("\nThis script reads in shapefiles, creates a geodatabase, and then extracts those shapefiles to the")
    print("newly-created geodatabase as feature classes clipped to Virginia Planning District 11.")
    print("Additionally, it creates a 5-mile buffer around landfills within the specified planning district")
    print("and displays and counts extracted shapefiles.")

    print("\n---Script starting---")

    # Reading in the shapefiles via their file paths and names

    shp_rivers = r"C:\GISc450\ArcPy1\LabData\varivers.shp"
    shp_landfills = r"C:\GISc450\ArcPy1\LabData\landfills.shp"
    shp_boundaries = r"C:\GISc450\ArcPy1\LabData\vapdbounds.shp"
    shp_towns = r"C:\GISc450\ArcPy1\LabData\va_towns.shp"
    shp_roads = r"C:\GISc450\ArcPy1\LabData\vards.shp"

    workspace = r"C:\GISc450\ArcPy1"

    # Specifying the workspace and naming the soon-to-be created geodatabase

    gdb_name = "Strobel_ArcPy1.gdb"
    gdb_location = os.path.join(workspace, gdb_name)

    # The GDB's location has been specified as the workspace

    if arcpy.Exists(gdb_location):
        arcpy.Delete_management(gdb_location)
        if arcpy.Exists(gdb_location):
            print("\n---GDB not deleted---")
        else:
            print(f"\n---{gdb_name} created---")

    arcpy.CreateFileGDB_management(workspace, gdb_name)

    # The GDB has been created and specified as the new workspace

    arcpy.env.workspace = gdb_location

    # Asking a user to input the specified district number. The district_num int has been converted to a string

    # district_num = "11"

    # district_num = input("\nEnter a district number: ")
    # if district_num == "11":
    #     print("\nDistrict number 11 has been selected")
    # else:
    #     print("\nPlease enter the correct district number")

    # Selecting the "vapdbounds" layer by attribute (planning district == "11")

    pd_11 = arcpy.SelectLayerByAttribute_management(shp_boundaries, "NEW_SELECTION", "PD_NO = '11'")

    # Clipping the layers to the planning district boundaries

    arcpy.Clip_analysis(shp_boundaries, pd_11, "boundary")
    arcpy.Clip_analysis(shp_rivers, pd_11, "rivers")
    landfill_clip = arcpy.Clip_analysis(shp_landfills, pd_11, "landfills")
    arcpy.Clip_analysis(shp_towns, pd_11, "towns")
    arcpy.Clip_analysis(shp_roads, pd_11, "roads")

    # Creating a 5-mile buffer around the clipped landfill points

    arcpy.Buffer_analysis(landfill_clip, "landfills_buffer", "5 miles")

    # Printing the layers being extracted to the GDB using a for statement

    for layers in arcpy.ListFeatureClasses():
        print(f"{layers} extracted to {gdb_name}")

    # Counting and printing the number of layers being extracted

    num_layers = len(arcpy.ListFeatureClasses())
    print(f"\nNumber of layers extracted: {num_layers}")


if __name__ == '__main__':
    main()

# Finally, printing the script's run time

time_end = time.time()
total_time = time_end - time_start
minutes = int(total_time / 60)
seconds = total_time % 60
print(f"\n---Script completed in {minutes} minutes {int(seconds)} seconds---")
