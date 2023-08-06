from .Component import Component
import pygame
from .util import show_text


class Button(Component):
    def __init__(self, parent, x=0, y=0, text=lambda: '', **kwargs):
        super().__init__(parent, x=x, y=y, **kwargs)
        self.text = text

    def on_left_click(self, func):
        self.set_action('left click', func)
        return self

    def on_right_click(self, func):
        self.set_action('right click', func)
        return self

    def on_middle_click(self, func):
        self.set_action('middle click', func)
        return self

    def draw(self, screen):
        x, y = self.get_x(), self.get_y()
        super().draw(screen)
        show_text(screen, self.get_text(), x + self.width / 2,
                  y + self.height / 2, font_size=self.font_size)

    def set_text(self, text):
        self.set_property('text', text)

    def get_text(self):
        return self.get_property('text')
