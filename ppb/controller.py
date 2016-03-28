import logging

import ppb.engine as engine
from ppb.event import Tick


class Controller(object):
    """
    A basic controller interface.

    Requires a hardware middleware that provides access to a keys, mouse, and
    events function.
    """

    def __init__(self, scene, hardware):
        """
        Attributes: keys: A dictionary of the hardware keys
                    mouse: An object definition of a mouse

        :param scene: Publisher
        :param hardware: An object with a keys, mouse and events functions.
                         keys should return a dictionary of the key state.
                         mouse should return an object representation of the mouse.
                         events should return hardware events translated into ppb events.
        :return:
        """
        scene.subscribe(Tick, self.tick)
        self.keys = None
        self.mouse = None
        self.hardware = hardware

    def tick(self, event):
        """
        Update the key and mouse state. Push hardware events to the queue.

        :param event: ppb.Event
        :return:
        """
        # Due to a pygame problem, must get the events before key and button states.
        events = self.hardware.events()
        for e in events:
            engine.message(e)
        self.keys = self.hardware.keys()
        self.mouse = self.hardware.mouse()

    def key(self, key_id):
        try:
            return self.keys[key_id]
        except TypeError:
            return False

    def __repr__(self):
        return "Controller[keys: {}, mouse: {}]".format(self.keys, self.mouse)
