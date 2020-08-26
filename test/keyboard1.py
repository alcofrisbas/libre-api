import librepycad.librepycad as lpc

KSW = 14.0
KSD = 5.05
T_X = 0
T_Y = 0
BOX_OFF_X = -KSD
BOX_OFF_Y = -KSD
M_TOP = 10
M_BOTTOM = 12
M_LEFT = 2
M_RIGHT = 2
RAD = 1
SF_THICK_X = 10
SF_THICK_Y = 15

TEENSY_W = 18.38
TEENSY_H = 35.56
TEENSY_X = 0
TEENSY_Y = 0

T_USB_W = 8.06
T_USB_H = 5.1

#holes and screws
H_R = 1.25
S_R = 2.5
# hole distance from something
STANDOFF_X = 2
STANDOFF_Y = 2

PIN_SPACE = 1.27
PIN_R = 0.5 # change if nec
RST_X = 10
RST_Y = 9


def cross(center, size):
    l1 = lpc.L(lpc.Coord(center.x-size, center.y), lpc.Coord(center.x+size, center.y))
    l2 = lpc.L(lpc.Coord(center.x, center.y-size), lpc.Coord(center.x, center.y+size))
    return l1, l2


with lpc.Project("kb1") as kb1:
    ROW_OFFSET = KSW+KSD
    key_holes = []
    for r in range(3):
        T_Y += KSW+KSD
        for c in range(11):
            if r == 0:
                T_X += KSW+KSD
            key_holes.append(lpc.Coord(c*(KSW+KSD), r*(KSW+KSD)+ROW_OFFSET))
    T_Y += KSW+KSD
    T_X += KSD
    T_Y += KSD
    for c in range(6):
        key_holes.append(lpc.Coord(c*(KSW+KSD), 0*(KSW+KSD)))
    key_holes.append(lpc.Coord(8*(KSW+KSD), 0*(KSW+KSD)))

    key_holes.append(lpc.Coord(5*(KSW+KSD) + 1.5*(KSW+KSD), 0))
    key_holes.append(lpc.Coord(8*(KSW+KSD) + 1.5*(KSW+KSD), 0))

    with lpc.CADFile("keys") as keys:
        for hole in key_holes:
            second = lpc.Coord(KSW,KSW, "rel")
            keys.add(lpc.Rectangle(hole, second))
        FULL_C1 = lpc.Coord(BOX_OFF_X-M_LEFT,BOX_OFF_Y-M_BOTTOM)
        FULL_C2 = lpc.Coord(BOX_OFF_X+T_X+M_RIGHT,BOX_OFF_Y+T_Y+M_TOP)
        keys.add(lpc.RadiusBox(FULL_C1,
                               FULL_C2,
                               RAD,
                               draw_sides=[True, True, True, True],
                               draw_arcs =[True, True, True, True],
                               mirror_arcs = [False, False,
                                              False, False,
                                              False, False,
                                              False, False]))

    # with lpc.CADFile("keys") as keys:
    #     for hole in key_holes:
    #         second = lpc.Coord(KSW,KSW, "rel")
    #         keys.add(lpc.Rectangle(hole, second))
    #         FULL_C1 = lpc.Coord(BOX_OFF_X-M_LEFT,BOX_OFF_Y-M_BOTTOM)
    #         FULL_C2 = lpc.Coord(BOX_OFF_X+T_X+M_RIGHT,BOX_OFF_Y+T_Y+M_TOP)
    #         keys.add(lpc.RadiusBox(FULL_C1,
    #                                FULL_C2,
    #                                RAD,
    #                                draw_sides=[True, True, True, True],
    #                                draw_arcs =[True, True, True, True],
    #                                mirror_arcs = [False, False,
    #                                               False, False,
    #                                               False, False,
    #                                               False, False]))

    with lpc.CADFile("teensy32") as teensy:
        TEENSY_X = FULL_C2.x - TEENSY_W - 40
        TEENSY_Y = FULL_C2.y - TEENSY_H - SF_THICK_Y/2 + 2
        TEENSY_PLUG_1 = lpc.Coord(TEENSY_X+TEENSY_W/2-T_USB_W/2, TEENSY_Y+TEENSY_H-T_USB_H+1)
        TEENSY_PLUG_2 = lpc.Coord(TEENSY_X+TEENSY_W/2+T_USB_W/2, TEENSY_Y+TEENSY_H+1)
        teensy.add(lpc.Rectangle(lpc.Coord(TEENSY_X, TEENSY_Y),lpc.Coord(TEENSY_X+TEENSY_W, TEENSY_Y+TEENSY_H)))
        teensy.add(lpc.Rectangle(TEENSY_PLUG_1, TEENSY_PLUG_2))

        teensy.add(cross(lpc.Coord(TEENSY_X+PIN_SPACE, TEENSY_Y+TEENSY_H-PIN_SPACE), PIN_R))
        teensy.add(cross(lpc.Coord(TEENSY_X+RST_X, TEENSY_Y+TEENSY_H-RST_Y), PIN_R))


    with lpc.CADFile("standoff_layer") as standoff_layer:
        c1 = lpc.Coord(FULL_C1.x + SF_THICK_X/2, FULL_C1.y + SF_THICK_Y/2)
        c2 = lpc.Coord(FULL_C2.x - SF_THICK_X/2, FULL_C2.y - SF_THICK_Y/2)
        standoff_layer.add(lpc.RadiusBox(FULL_C1, FULL_C2, RAD))
        standoff_layer.add(lpc.RadiusBox(c1, c2, RAD+2))#, draw_arcs=[False, False, False, False]))

        # standoff_layer.add(lpc.Arc(lpc.Coord(c1.x, c1.y), RAD+2, 0, 90, center=True))
        # standoff_layer.add(lpc.Arc(lpc.Coord(c2.x, c1.y), RAD+2, 90, 180, center=True))
        # standoff_layer.add(lpc.Arc(lpc.Coord(c2.x, c2.y), RAD+2, 180, 270, center=True))
        # standoff_layer.add(lpc.Arc(lpc.Coord(c1.x, c2.y), RAD+2, 270, 360, center=True))

    with lpc.CADFile("retainer") as retainer:
        b_thic = 5
        gap = 0.5
        c1 = lpc.Coord(FULL_C1.x + SF_THICK_X/2, FULL_C1.y + SF_THICK_Y/2)
        c2 = lpc.Coord(FULL_C2.x - SF_THICK_X/2, FULL_C2.y - SF_THICK_Y/2)
        retainer.add(lpc.RadiusBox(FULL_C1, FULL_C2, RAD, draw_sides=(False, True, True, True)))

        retainer.add(lpc.RadiusBox(c1, c2, RAD+2,
                                   draw_sides=[False, True, True, True]))
        # retainer.add(lpc.L(lpc.Coord(FULL_C1.x, TEENSY_Y+TEENSY_H),
        #                    lpc.Coord(FULL_C2.x, TEENSY_Y+TEENSY_H)))

        retainer.add(lpc.L(lpc.Coord(c1.x+RAD+2, c2.y),
                           lpc.Coord(TEENSY_X-5-RAD-2, c2.y)))
        retainer.add(lpc.L(lpc.Coord(TEENSY_X+TEENSY_W+RAD+gap+b_thic+2, c2.y),
                           lpc.Coord(c2.x-RAD-2, c2.y)))

        # outer gap box
        retainer.add(lpc.RadiusBox(lpc.Coord(TEENSY_X-gap-b_thic, TEENSY_Y-gap-b_thic),
                                   lpc.Coord(TEENSY_X+TEENSY_W+gap+b_thic, c2.y), RAD+2,
                                   draw_sides=[False, True, True, True],
                                   mirror_arcs=[False, True,
                                                False, False,
                                                False, False,
                                                True, False]))
        # inner gap
        retainer.add(lpc.RadiusBox(lpc.Coord(TEENSY_X-gap, TEENSY_Y-gap),
                                   lpc.Coord(TEENSY_X+TEENSY_W+gap, TEENSY_Y+TEENSY_H+gap), RAD,
                                   draw_sides=[False, True, True, True],
                                   draw_arcs=[True, True, True, True],
                                   mirror_arcs=[False, False,
                                                False, False,
                                                False, False,
                                                False, False]))
        # lines for plug
        retainer.add(lpc.L(lpc.Coord(TEENSY_PLUG_1.x-2, TEENSY_Y+TEENSY_H+gap),
                           lpc.Coord(TEENSY_PLUG_1.x-2, FULL_C2.y)))
        retainer.add(lpc.L(lpc.Coord(TEENSY_PLUG_2.x+2, TEENSY_Y+TEENSY_H+gap),
                           lpc.Coord(TEENSY_PLUG_2.x+2, FULL_C2.y)))

        retainer.add(lpc.L(lpc.Coord(FULL_C1.x+RAD, FULL_C2.y ),
                           lpc.Coord(TEENSY_PLUG_1.x-2, FULL_C2.y)))
        retainer.add(lpc.L(lpc.Coord(TEENSY_PLUG_2.x+2, FULL_C2.y),
                           lpc.Coord(FULL_C2.x-RAD, FULL_C2.y)))

        retainer.add(lpc.L(lpc.Coord(TEENSY_X-gap+RAD, TEENSY_Y+TEENSY_H+gap),
                           lpc.Coord(TEENSY_PLUG_1.x-2, TEENSY_Y+TEENSY_H+gap)))
        retainer.add(lpc.L(lpc.Coord(TEENSY_PLUG_2.x+2, TEENSY_Y+TEENSY_H+gap),
                           lpc.Coord(TEENSY_X+TEENSY_W+gap-RAD, TEENSY_Y+TEENSY_H+gap)))

        # retainer.add(lpc.Arc(lpc.Coord(c1.x, c1.y), RAD+2, 0, 90, center=True))
        # retainer.add(lpc.Arc(lpc.Coord(c2.x, c1.y), RAD+2, 90, 180, center=True))
        # retainer.add(lpc.Arc(lpc.Coord(c2.x, c2.y), RAD+2, 180, 270, center=True))
        # retainer.add(lpc.Arc(lpc.Coord(c1.x, c2.y), RAD+2, 270, 360, center=True))
    with lpc.CADFile("under_teensy") as UT:
        UT.add(lpc.RadiusBox(FULL_C1, FULL_C2, RAD))
        UT.add(lpc.RadiusBox(lpc.Coord(TEENSY_X, TEENSY_Y+TEENSY_H-RST_Y-RAD),
                             lpc.Coord(TEENSY_X+RST_X+RAD, TEENSY_H+TEENSY_Y),RAD))


    with lpc.CADFile("baseplate") as baseplate:
        baseplate.add(lpc.RadiusBox(FULL_C1, FULL_C2, RAD))
        num_slots = 10
        space = 5
        x_s = FULL_C1.x +SF_THICK_X/2
        x_f = FULL_C2.x - SF_THICK_X/2
        y_s = FULL_C1.y + SF_THICK_Y/2
        y_f = FULL_C2.y - SF_THICK_Y/2
        # baseplate.add(lpc.L(lpc.Coord(x_s, y_s), lpc.Coord(x_f, y_f)))
        total_space = space*(num_slots-1)
        total = x_f - x_s
        without_spaces = total-total_space
        slot_size = without_spaces/num_slots
        lst = []
        for i in range(num_slots):
            x1 = x_s + (slot_size+space)*i
            x2 = x1 + slot_size
            y1 = y_s
            y2 = y_f
            r = lpc.RadiusBox(lpc.Coord(x1, y1),
                                     lpc.Coord(x2,y2),
                                     RAD)
            lst.append(r)
        lst[-3].c2.y = TEENSY_Y - gap - space

        lst[-2].ds = (False, True, True, False)
        lst[-2].da = (True, True, True, False)
        print(lst[-1].da)

        for item in lst:
            print(item.da)
            baseplate.add(item)
        # lower left corner of -2
        x1 = lst[-2].c1.x
        y1 = lst[-2].c1.y

        x2 = lst[-2].c1.x
        y2 = TEENSY_Y-gap-space

        x3 = TEENSY_X+TEENSY_W + space
        y3 = TEENSY_Y-gap-space

        x4 = TEENSY_X+TEENSY_W+space
        y4 = lst[-2].c2.y

        x5 = lst[-2].c2.x
        y5 = lst[-2].c2.y


        baseplate.add(lpc.L(lpc.Coord(x1, y1+RAD),
                            lpc.Coord(x2, y2-RAD)))
        baseplate.add(lpc.L(lpc.Coord(x2+RAD, y2),
                            lpc.Coord(x3-RAD, y3)))
        baseplate.add(lpc.L(lpc.Coord(x3, y3+RAD),
                            lpc.Coord(x4, y4-RAD)))
        baseplate.add(lpc.L(lpc.Coord(x4+RAD, y4),
                            lpc.Coord(x5-RAD, y5)))

        baseplate.add(lpc.Arc(lpc.Coord(x2+RAD, y2-RAD),RAD, 90, 180, center=True))
        baseplate.add(lpc.Arc(lpc.Coord(x3-RAD, y3+RAD),RAD, -90, 0, center=True))
        baseplate.add(lpc.Arc(lpc.Coord(x4+RAD, y4-RAD),RAD, 90, 180, center=True))

        baseplate.add(lpc.RadiusBox(lpc.Coord(TEENSY_X-gap, TEENSY_Y-gap),
                                   lpc.Coord(TEENSY_X+TEENSY_W+gap, TEENSY_Y+TEENSY_H+gap), RAD))

    with lpc.CADFile("holes") as holes:
        h_ur = lpc.Coord(FULL_C2.x-S_R-STANDOFF_X, FULL_C2.y-S_R-STANDOFF_Y)
        h_lr = lpc.Coord(FULL_C2.x-S_R-STANDOFF_X, FULL_C1.y+S_R+STANDOFF_Y)
        h_ul = lpc.Coord(FULL_C1.x+S_R+STANDOFF_X, FULL_C2.y-S_R-STANDOFF_Y)
        h_ll = lpc.Coord(FULL_C1.x+S_R+STANDOFF_X, FULL_C1.y+S_R+STANDOFF_Y)

        holes.add(cross(h_ur, H_R))
        holes.add(cross(h_ul, H_R))
        holes.add(cross(h_lr, H_R))
        holes.add(cross(h_ll, H_R))
        holes.add(cross(lpc.Coord((h_ll.x + h_lr.x)/2, h_ll.y), H_R))
        holes.add(cross(lpc.Coord((h_ll.x + h_lr.x)/2, h_ul.y), H_R))

    with lpc.CADFile("screws") as screws:
        screws.add(cross(h_ur, S_R))
        screws.add(cross(h_ul, S_R))
        screws.add(cross(h_lr, S_R))
        screws.add(cross(h_ll, S_R))


    with lpc.CADFile("measurements") as measurements:
        measurements.add(lpc.Da(FULL_C1,
                                lpc.Coord(FULL_C2.x,FULL_C1.y),
                                lpc.Coord(0,FULL_C1.y-10)))
        measurements.add(lpc.Da(FULL_C1,
                                lpc.Coord(FULL_C1.x, FULL_C2.y),
                                lpc.Coord(FULL_C1.x-10,0)))
