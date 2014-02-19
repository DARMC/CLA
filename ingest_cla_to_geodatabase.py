import arcpy
from arcpy import env
import os

### Set Globals
output_folder = 'C:/Users/bmaionedowning/Desktop'
sp_ref = arcpy.SpatialReference(4326)

### Make a geodatabase to hold all FCs easily
print '>> Creating CLA Geodatabase'
cla_geodatabase = 'CLA.gdb'
arcpy.CreateFileGDB_management(output_folder,
                               cla_geodatabase)
env.workspace = cla_geodatabase

def make_point_layer_from_csv(csv_file, gdb):
    print '>> Creating Feature Class from file {0}...'.format(csv_file),

    # make xy event layer to hold geometries   
    tmp_xy_layer = csv_file.strip('.csv').replace(' ','_').lower()
    arcpy.MakeXYEventLayer_management(csv_file, 'Longitude', 'Latitude',
                                            tmp_xy_layer, sp_ref)
    print 'Got {0} points'.format(arcpy.GetCount_management(tmp_xy_layer))

    # copy geometries to feature class
    output_fc = os.path.join(gdb, tmp_xy_layer)
    arcpy.CopyFeatures_management(tmp_xy_layer, output_fc)

def make_movement_layer_from_csv(csv_file, gdb):
    print '>> Creating Feature Class from file {0}...'.format(csv_file)
    # TODO
                                                            
### Make csv
if __name__ == '__main__':
    for csv_file in ['Complete CLA Database Points.csv', 'all_points.csv']:
        make_point_layer_from_csv(csv_file, cla_geodatabase)
    os.remove('schema.ini')
    print '>> COMPLETED'
