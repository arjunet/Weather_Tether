from carbonkivy.uix.shell import UIShellLeftPanel, UIShellPanelSelectionItem
from kivy.properties import StringProperty
from kivy.animation import Animation

class SidePanel(UIShellLeftPanel):
    city1_panel_item = StringProperty("")
    city2_panel_item = StringProperty("")
    city3_panel_item = StringProperty("")

    def __init__(self, **kwargs):
        self.animation = Animation()
        super(SidePanel, self).__init__(**kwargs)

class CityPanelItem(UIShellPanelSelectionItem):
    text = StringProperty("")
    right_icon = StringProperty("")

    

    


    
