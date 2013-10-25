### General shapefile functions for easy reuse ###

## Depends
import shapefile as shp
import urllib

## Functions
def write_prj_file(fname, epsg=4326):
    """
    Writes .prj file fname associated with target projection epsg.
    Writes to epsg 4326 (WGS 1984) by default. Honestly, kwarg is only included for robustness.
    """
    try:
        wktString  = urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg))
        with open('{0}.prj'.format(fname), 'w') as prjFile:
            prjFile.write(wktString.read())
    except IOError:
        print 'Unable to fetch EPSG string for prj file. Projection can be still be defined on import to GIS client'
    return True

def set_up_shapefile(fieldNames):
    """
    Returns a shapefile with specified field names and a blank,
    well-shaped attribute table
    """
    sf = shp.Writer(shp.POLYLINE)
    sf.autoBalance = 1
    for f in fieldNames:
        sf.field(f, 'C', '255')
        for r in sf.records:
            r.append('')
    return sf

def add_line_geometry(sf, x1, y1, x2, y2, row):
    """
    Add exactly two points to a shapefile
    """
    sf.line(parts = [[[x1, y1],[x2, y2]]])
    for r in row:
    	r = r.encode('utf-8', errors='replace')
    sf.records.append(row)

    return sf

if __name__ == '__main__':
	print  'Shapefile Functions V1.0'