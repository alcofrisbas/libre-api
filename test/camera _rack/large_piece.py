import librepycad.librepycad as lpc
CAMERA_WIDTH  = 112.6
CAMERA_HEIGHT = 69.9
CAMERA_DEPTH  = 45.3

DRIVE_WIDTH = 12
DRIVE_DEPTH = 28
DRIVE_HEIGHT = 69


STRAP_HOLE_X = 10
STRAP_HOLE_Y = CAMERA_HEIGHT-10

SPACER_D = 5

LARGE_HEIGHT = CAMERA_HEIGHT
LARGE_WIDTH =  CAMERA_DEPTH+SPACER_D+ DRIVE_DEPTH
SMALL_HEIGHT = CAMERA_HEIGHT
SMALL_WIDTH = SPACER_D+ DRIVE_DEPTH

SMALL_OFFSET_X = LARGE_WIDTH + 10
SMALL_OFFSET_Y =  0


MAIN_RADIUS  = 5
HOLE_RAD = 2.5/2
MOUNT_RAD = 6.5/2
LOCATOR_RAD =  2.5/2
N_HOLES = 3
HOLE_PAD =  5
LOCATOR_X = 20
LOCATOR_Y = 20
# not sure  why  the -1,but  it works for now. 
SPACING = (LARGE_HEIGHT-2*HOLE_PAD)/(N_HOLES-1)
HOLE_Ys = [i*SPACING+HOLE_PAD for i in range(N_HOLES)]
LARGE_X  = LARGE_WIDTH-HOLE_PAD
SMALL_X =  SMALL_OFFSET_X+SMALL_WIDTH-HOLE_PAD



with lpc.Project("outputs/camera_rack1") as rack1:
    with  lpc.CADFile("rack1") as large:
        large.add(lpc.RadiusBox(lpc.Coord(0, 0), lpc.Coord(LARGE_WIDTH, LARGE_HEIGHT), MAIN_RADIUS))
        for y in HOLE_Ys:
            large.add(lpc.Circle(lpc.Coord(LARGE_X, y),HOLE_RAD))
        large.add(lpc.Circle(lpc.Coord(STRAP_HOLE_X, STRAP_HOLE_Y), MOUNT_RAD))
        large.add(lpc.Circle(lpc.Coord(LOCATOR_X, LOCATOR_Y), LOCATOR_RAD))


        large.add(lpc.RadiusBox(lpc.Coord(SMALL_OFFSET_X, SMALL_OFFSET_Y), lpc.Coord(SMALL_OFFSET_X+SMALL_WIDTH, SMALL_OFFSET_Y+SMALL_HEIGHT), MAIN_RADIUS))
        for y in HOLE_Ys:
            large.add(lpc.Circle(lpc.Coord(SMALL_X, y),HOLE_RAD))