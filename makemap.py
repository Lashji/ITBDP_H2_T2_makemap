from IPython.display import display
from PIL import Image
import urllib
from io import BytesIO
import sys
import math


def get_coords():
    tmp = []
    for i in range (1, 6):
        tmp.append(float(sys.argv[i]))
    return tmp

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) +
                                (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def main():
    zoom = int(sys.argv[5])
    start_col = float(sys.argv[1])
    start_row = float(sys.argv[2])
    filename = str(sys.argv[6])
    process_img(start_col, start_row, zoom, filename)
    
def save(mapimg, fn):
    mapimg.save(fn)

def process_img(start_col, start_row, zoom, filename):
    user_coords = get_coords()
    deg_start = deg2num(user_coords[0], user_coords[1], user_coords[4])
    deg_end = deg2num(user_coords[2], user_coords[3], user_coords[4])
    cols = get_tile_count(deg_start[0], deg_end[0])
    rows = get_tile_count(deg_start[1], deg_end[1])

    mapimg = Image.new("RGB", (cols*256, rows*256))

    start_col = deg_start[0]
    start_row = deg_start[1]

    for col in range (start_col, start_col+cols + 1):
        for row in range(start_row, start_row + rows + 1):
            imgdata = urllib.request.urlopen(
                  "https://tile.openstreetmap.org/{}/{}/{}.png".format(zoom, col, row)).read()
            img = Image.open(BytesIO(imgdata))
            mapimg.paste(img,((col-start_col)*256, (row-start_row)*256))
    mapimg
    save(mapimg, filename)



def get_tile_count(start_deg, end_deg):
    
    return end_deg - start_deg 

main()


