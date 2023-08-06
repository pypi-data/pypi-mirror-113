class Component:
    def __init__(self, parent):
        self.parent = parent
        self.parent.add_component(self)

    def get_parent(self):
        return self.parent

    def draw(self, screen):
        pass

    def event(self, name):
        pass

