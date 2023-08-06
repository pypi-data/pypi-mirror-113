import pygame


class Component:
    def __init__(self, parent, x=0, y=0, font_color=(0, 0, 0),
                 bg_colour=(255, 255, 255), border_color=(0, 0, 0),
                 border_thickness=1, font_size=20, width=1, height=1,
                 colour=(0, 0, 0)):
        self.parent = parent
        self.parent.add_component(self)
        self.x = x
        self.y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_colour = font_color
        self.bg_colour = bg_colour
        self.border_colour = border_color
        self.border_thickness = border_thickness
        self.font_size = font_size
        self.colour = colour
        self.actions = {}

    def get_parent(self):
        return self.parent

    def draw(self, screen):
        x, y = self.get_x(), self.get_y()
        pygame.draw.rect(screen, self.bg_colour,
                         (x, y, self.width, self.height))

        pygame.draw.rect(screen, self.border_colour,
                         (x, y, self.width, self.height),
                         width=self.border_thickness)

    def event(self, name):
        if name in self.actions:
            if 'click' in name and not self.mouseover():
                return False

            self.actions[name](self)
            return True

    def get_x(self):
        return self.get_parent().get_x() + self.x

    def get_y(self):
        return self.get_parent().get_y() + self.y

    def set_width(self, width):
        self.width = width
        self.parent.update()

    def get_property(self, name):
        prop = self.__getattribute__(name)
        if callable(prop):
            prop = prop()

        return prop

    def set_property(self, name, value):
        self.__setattr__(name, value)
        self.parent.update()

    def get_action(self, name):
        return self.actions[name]

    def set_action(self, name, func):
        self.actions[name] = func

    def mouseover(self):
        x, y = pygame.mouse.get_pos()
        return (
                self.get_x() <= x <= self.get_x() + self.width and
                self.get_x() <= y <= self.get_x() + self.height
        )
