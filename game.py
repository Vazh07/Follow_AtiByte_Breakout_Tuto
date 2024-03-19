import pyglet
from pyglet.window import FPSDisplay, key
import pymunk
from pymunk.pyglet_util import DrawOptions
from pymunk.vec2d import Vec2d
import random

collision_types = {
    "ball": 1,
    "brick": 2,
    "bottom": 3,
    "player": 4
}


class Ball(pymunk.Body):
    def __init__(self, space, position):
        super().__init__(1, float('inf'))
        self.position = position.x, position.y+18
        shape = pymunk.Circle(self, 10)
        shape.elasticity = 0.98
        shape.collision_type = collision_types["ball"]
        self.spc = space
        self.on_paddle = True
        self.velocity_func = self.constant_velocity
        self.joint = pymunk.GrooveJoint(space.static_body, self, (100, 118), (1180, 118), (0, 0))
        space.add(self, shape, self.joint)

    def shoot(self):
        self.on_paddle = False
        self.spc.remove(self.joint)
        direction = Vec2d(random.choice([-50, 50]), random.choice([500, 50]))
        self.apply_impulse_at_local_point(direction)

    def constant_velocity(self, body, gravity, damping, dt):
        body.velocity = body.velocity.normalized()*600

class Player(pymunk.Body):
    def __init__(self, space):
        super().__init__(10, float('inf'))
        self.position=640, 100
        shape = pymunk.Segment(self,(-50,0),(50,0),8)
        shape.elasticity = 0.98
        shape.collision_type = collision_types["player"]
        joint = pymunk.GrooveJoint(space.static_body, self, (100, 100), (1180, 100), (0, 0))
        space.add(self, shape, joint)


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(0,0)
        self.fps = FPSDisplay(self)
        self.space = pymunk.Space()
        self.options = DrawOptions()
        self.player = Player(self.space)
        self.ball = Ball(self.space, self.player.position)

    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.options)
        self.fps.draw()

    def update(self, dt):
        self.space.step(dt)

    def on_key_press(self, symbol, modifiers):
        dir = None
        if symbol == key.RIGHT:
            dir = 600, 0
            self.player.velocity = dir
        elif symbol == key.LEFT:
            dir = -600, 0
            self.player.velocity = dir
        if dir and self.ball.on_paddle:
            self.ball.velocity = dir
        if symbol == key.SPACE:
            self.ball.shoot()

    def on_key_release(self, symbol, modifiers):
        if symbol in (key.LEFT, key.RIGHT):
            self.player.velocity = 0, 0
            if self.ball.on_paddle:
                self.ball.velocity = 0, 0

if __name__=="__main__":
    window = GameWindow(1280,900,"Breakout!", resizable=True)
    pyglet.clock.schedule_interval(window.update, 1/60.00)
    pyglet.app.run()
