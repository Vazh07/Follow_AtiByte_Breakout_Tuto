import pyglet
from pyglet.window import FPSDisplay, key
import pymunk
from pymunk.pyglet_util import DrawOptions

collision_types = {
    "ball": 1,
    "brick": 2,
    "bottom": 3,
    "player": 4
}


class Player(pymunk.Body):
    def __init__(self, space):
        super().__init__(10, float('inf'))
        self.position=640, 100
        shape = pymunk.Segment(self,(-50,0),(50,0),8)
        shape.elasticity = 0.98
        shape.collision_type = collision_types["player"]
        joint = pymunk.GrooveJoint(space.static_body, self, (100, 100), (1180, 100), (0, 0))
        space.add(self, shape)

class GameWindow(pyglet.wi  ndow.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(0,0)
        self.fps = FPSDisplay(self)
        self.space = pymunk.Space()
        self.options = DrawOptions()
        self.player = Player(self.space)

    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.options)
        self.fps.draw()

    def update(self, dt):
        self.space.step(dt)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.player.velocity = 600, 0
        elif symbol == key.LEFT:
            self.player.velocity = -600, 0

    def on_key_release(self, symbol, modifiers):
        if symbol in (key.LEFT, key.RIGHT):
            self.player.velocity = 0, 0

if __name__=="__main__":
    window = GameWindow(1280,900,"Breakout!", resizable=True)
    pyglet.clock.schedule_interval(window.update, 1/60.00)
    pyglet.app.run()
