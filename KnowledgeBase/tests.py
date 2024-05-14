from semantic_network import *


def test1():
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
    engine = SemanticNetwork()

    engine.reset()

    engine.declare(Drum())
    engine.declare(Door())
    engine.declare(DetergentDrawer())
    engine.declare(WaterOutlet(blocked=False, caught=True, jammed=False, connected_too_high=True, water_leak=True, damaged=True, connected_correctly=True))
    engine.declare(DrainPipe(blocked=True, caught=False, jammed=True, unapproved_extension=False))
    engine.declare(PowerCord())
    engine.declare(Button())
    engine.declare(Display(errors=['E:30 / -80']))
    engine.declare(Program())

    engine.run()


def test3():
    engine = SemanticNetwork()

    engine.reset()

    engine.declare(Drum())
    engine.declare(Door())
    engine.declare(DetergentDrawer())
    engine.declare(WaterOutlet())
    engine.declare(DrainPipe())
    engine.declare(PowerCord())
    engine.declare(Button())
    engine.declare(Display())
    engine.declare(Program())


if __name__ == '__main__':
    print("Test 1: Various simple problems")
    test1()

    print()
    print()

    print("Test 2: Water system problems with all fields filled")
    test2()
