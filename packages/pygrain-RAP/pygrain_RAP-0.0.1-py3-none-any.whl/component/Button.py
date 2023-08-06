from .Component import Component
import pygame
from .util import show_text


class Button(Component):
    def __init__(self, parent, x=0, y=0, width=0, height=0, text=lambda: "",
                 font_color=(0, 0, 0), bg_colour=(255, 255, 255),
                 border_color=(0, 0, 0), border_thickness=1, font_size=10):
        super().__init__(parent)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_colour = font_color
        self.bg_colour = bg_colour
        self.border_colour = border_color
        self.border_thickness = border_thickness
        self.font_size = font_size
        self.actions = {}

    def on_left_click(self, func):
        self.actions['left click'] = func
        return self

    def on_right_click(self, func):
        self.actions['right click'] = func
        return self

    def on_middle_click(self, func):
        self.actions['middle click'] = func
        return self

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_colour,
                         (self.x, self.y, self.width, self.height))

        pygame.draw.rect(screen, self.border_colour,
                         (self.x, self.y, self.width, self.height),
                         width=self.border_thickness)

        show_text(screen, self.text(), self.x + self.width / 2, self.y + self.height / 2,
                  font_size=self.font_size)

    def mouseover(self):
        x, y = pygame.mouse.get_pos()
        return (
                self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height
        )

    def event(self, name):
        if name in self.actions and self.mouseover():
            return self.actions[name](self)

    def set_text(self, text):
        self.text = text
        self.parent.update()

    def get_text(self):
        return self.text()
