from .Component import Component


class Frame(Component):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.components = []
        parent.switch_frame(self)

    def event(self, name):
        done = False
        for component in self.components:
            done = component.event(name)
            if done:
                return done

        return done

    def draw(self, screen):
        super().draw(screen)
        for component in self.components[::-1]:
            component.draw(screen)

    def add_component(self, component):
        self.components.insert(0, component)

    def update(self):
        self.parent.update()

