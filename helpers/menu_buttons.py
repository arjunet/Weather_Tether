from carbonkivy.uix.button import CButtonCircular
from kivy.lang import builder


class Edit_Day(CButtonCircular):
    def __init__(self, **kwargs):
        super(Edit_Day, self).__init__(**kwargs)

class Delete_Day(CButtonCircular):
    def __init__(self, **kwargs):
        super(Delete_Day, self).__init__(**kwargs)

class Edit_Night(CButtonCircular):
    def __init__(self, **kwargs):
        super(Edit_Night, self).__init__(**kwargs)

class Delete_Night(CButtonCircular):
    def __init__(self, **kwargs):
        super(Delete_Night, self).__init__(**kwargs)