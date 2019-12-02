from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang import Builder


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            distx = (ball.center_x - self.center_x) * vx / abs(vx) * -1
            disty = abs(ball.center_y - self.center_y)
            b = self.top - self.width / 2 - self.center_y
            # this determines whether the paddle is hit at the end
            # the latter term distx checks if there are some glitches due to very quick paddle movement
            if disty > b + distx or distx < 0:
                offset = 0
                # hit above, set back ball and let ball move upwards
                if ball.center_y > self.center_y:
                    ball.y = self.top
                    bounced = Vector(vx, abs(vy))
                # hit below, set back ball and let ball move downwards
                else:
                    ball.y = self.y - ball.height
                    bounced = Vector(vx, -1 * abs(vy))
            else:
                # this offset lets the bounce angle decrease depending on how far to the edge the ball is hit
                offset = (ball.center_y - self.center_y) / (self.height / 2)
                bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def start_game(self):
        self.serve_ball()
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class MenuScreen(Screen):
    pass


class GameScreen(Screen):
    pass
    """"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
    """

class PongManager(ScreenManager):
    pass


main_kivy = Builder.load_file('pong.kv')


class PongApp(App):
    def build(self):
        return main_kivy


if __name__ == '__main__':
    PongApp().run()
