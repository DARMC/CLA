import arcpy
from arcpy import env
import os

def set_up_geodatabase(output_folder, path):
    """
    Create a geodatabase with name 'path' in the valid directory
    'output_folder'. If an existing database with the same name
    is found, it will be overwritten.

    Parameters
    ----------
    output_folder : folder to create geodatabase in
    path : name of the geodatabase to create
    """
    print '>> Creating CLA Geodatabase'
    if os.path.isfile(path):
        print '>> Overwriting existing version of CLA database'
        os.remove(path)
    arcpy.CreateFileGDB_management(output_folder, path)

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
    # set output folder, geodatabase name and target spatial reference
    output_folder = r'C:/Users/bmaionedowning/Desktop'
    gdb_path = 'CLA.gdb'
    sp_ref = arcpy.SpatialReference(4326)

    # set up geodatabase to hold all output layers
    set_up_geodatabase(output_folder, gdb_path)
    arcpy.env.workspace = gdb_path

    for csv_file in ['Complete CLA Database Points.csv', 'all_points.csv']:
        make_point_layer_from_csv(csv_file, gdb_path)

    os.remove('schema.ini')
    print '>> COMPLETED'
