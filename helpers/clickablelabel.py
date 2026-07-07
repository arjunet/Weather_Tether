from carbonkivy.uix.label import CLabelNeutral
from kivy.uix.behaviors import ButtonBehavior

class ClickableLabel(CLabelNeutral, ButtonBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Force the widget's layout box to automatically match the text size
        self.bind(texture_size=self._update_size)

    def _update_size(self, instance, value):
        # Update width and height dynamically so the background canvas stretches perfectly too!
        self.width = value[0]
        self.height = value[1]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch('on_press')
            return True
        return super().on_touch_down(touch)