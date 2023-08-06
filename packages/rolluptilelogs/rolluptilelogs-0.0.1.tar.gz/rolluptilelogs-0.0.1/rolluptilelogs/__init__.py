import click
import numpy
import sys


@click.command()
@click.argument('zoom', type=click.INT)
def cli(zoom):
    rolledup = numpy.zeros((2**zoom, 2**zoom), numpy.int64)

    for line in sys.stdin.readlines():
        # Turn z/x/y N into variables
        coords = line.split(' ', 1)
        splitline=coords[0].split('/',2)
        z = int(splitline[0])

        # Skip lower zooms
        if z >= zoom:
            # Convert to integers
            x = int(splitline[1])
            y = int(splitline[2])
            N = int(coords[1])

            # Work out what the x/y at zoom is
            rolled_x = int(x / 2 ** (z-zoom))
            rolled_y = int(y / 2 ** (z-zoom))
            rolledup[rolled_x, rolled_y] += N

    for x in range(0, 2**zoom):
        for y in range(0, 2**zoom):
            if rolledup[x, y] > 0:
                print("{}/{}/{} {}".format(zoom, x, y, rolledup[x, y]))
