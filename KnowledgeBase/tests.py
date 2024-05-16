from semantic_network import *


def test0():
    print("Test 0: Everything is working fine")

    engine = SemanticNetwork()

    engine.reset()

    engine.declare(Drum(unbalanced_load=False, additional_water=False, jerking=False))
    engine.declare(Door(closed=True, caught_laundry=False, water_leak=False))
    engine.declare(DetergentDrawer(too_much_detergent=False, fabric_softener_remaining=False))
    engine.declare(WaterOutlet(blocked=False, caught=False, jammed=False, connected_too_high=False, water_leak=False,
                    damaged=False, connected_correctly=True))
    engine.declare(DrainPipe(blocked=False, caught=False, jammed=False, unapproved_extension=False))
    engine.declare(PowerCord(plugged_in=True))
    engine.declare(Button(flashing=False))
    engine.declare(Display(on=True, errors=[]))
    engine.declare(Program())

    engine.run()


def test1():
    print("Test 1: Various simple problems")

    engine = SemanticNetwork()

    engine.reset()

    engine.declare(Drum(jerking=True))
    engine.declare(Door(closed=False))
    engine.declare(DetergentDrawer(too_much_detergent=True))
    engine.declare(WaterOutlet())
    engine.declare(DrainPipe())
    engine.declare(PowerCord(plugged_in=False))
    engine.declare(Button())
    engine.declare(Display(errors=['E:30/-20']))
    engine.declare(Program())

    engine.run()


def test2():
    print("Test 2: Water system problems")

    engine = SemanticNetwork()

    engine.reset()

    engine.declare(Drum())
    engine.declare(Door())
    engine.declare(DetergentDrawer())
    engine.declare(WaterOutlet(caught=True, connected_too_high=True, water_leak=True, damaged=True, connected_correctly=True))
    engine.declare(DrainPipe(blocked=True, jammed=True))
    engine.declare(PowerCord())
    engine.declare(Button())
    engine.declare(Display(errors=['E:30 / -80']))
    engine.declare(Program())

    engine.run()


def test3():
    print("Test 3: Multiple errors on the display")

    engine = SemanticNetwork()

    engine.reset()

    engine.declare(Drum(unbalanced_load=True, additional_water=True))
    engine.declare(Door(closed=False))
    engine.declare(DetergentDrawer())
    engine.declare(WaterOutlet(caught=True, connected_too_high=True))
    engine.declare(DrainPipe())
    engine.declare(PowerCord())
    engine.declare(Button())
    engine.declare(Display(errors=["E:60 / -2B", "E:30/-20", "E:30 / -80"]))
    engine.declare(Program())

    engine.run()


def test4():
    print("Test 4: Drum and detergent drawer problems")

    engine = SemanticNetwork()

    engine.reset()

    engine.declare(Drum(unbalanced_load=True, additional_water=True))
    engine.declare(Door())
    engine.declare(DetergentDrawer(too_much_detergent=True, fabric_softener_remaining=True))
    engine.declare(WaterOutlet())
    engine.declare(DrainPipe())
    engine.declare(PowerCord())
    engine.declare(Button())
    engine.declare(Display(errors=["E:30/-20", "E:60 / -2B"]))
    engine.declare(Program(supports_fabric_softener=False))

    engine.run()


def test5():
    print("Test 5: ")

    engine = SemanticNetwork()

    engine.reset()

    engine.declare(Drum())
    engine.declare(Door(caught_laundry=True, water_leak=True))
    engine.declare(DetergentDrawer())
    engine.declare(WaterOutlet())
    engine.declare(DrainPipe())
    engine.declare(PowerCord())
    engine.declare(Button(name="Start/Pause", flashing=True))
    engine.declare(Display(on=False))
    engine.declare(Program())

    engine.run()


if __name__ == '__main__':
    test0()

    print()
    print()

    test1()

    print()
    print()

    test2()

    print()
    print()

    test3()

    print()
    print()

    test4()

    print()
    print()

    test5()
