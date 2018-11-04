from IPython.display import display
from PIL import Image
import urllib
from io import BytesIO
import sys
import math

start_col = float(sys.argv[1])
start_row = float(sys.argv[2])
cols = float(sys.argv[1]) / float(sys.argv[3])
rows = float(sys.argv[2]) / float(sys.argv[4])

print(cols)
print(rows)


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

    deg = deg2num(start_col, start_row, zoom)
    mapimg = Image.new("RBG", (256, 256))
    imgdata = urllib.request.urlopen(
        "https://tile.openstreetmap.org/14/{}/{}.png".format(deg[0], deg[1])).read()
    img = Image.open(BytesIO(imgdata))
    print(img.size)
    display(img)


main()
