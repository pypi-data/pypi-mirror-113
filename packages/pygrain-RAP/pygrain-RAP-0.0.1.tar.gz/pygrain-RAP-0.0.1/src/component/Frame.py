from .Component import Component


class Frame(Component):
    def __init__(self, parent):
        super().__init__(parent)
        self.components = []

    def event(self, name):
        for component in self.components:
            component.event(name)

    def draw(self, screen):
        for component in self.components:
            component.draw(screen)

    def add_component(self, component):
        self.components.append(component)

    def update(self):
        self.parent.update()

