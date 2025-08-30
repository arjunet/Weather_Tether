# Imports:

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from carbonkivy.app import CarbonApp

# Screen Python Code:


class SignupScreen(Screen):
    # KV File will handle UI elements
    def signup():
        # Replace below with signup code
        pass


class LoginScreen(Screen):
    # KV File will handle UI elements
    def Login():
        # Replace below with login code
        pass


class ForgotScreen(Screen):
    # KV File will handle UI elements
    def Send_Forgot_Email():
        # Replace below with sending forgot email code
        pass

# Build And Run The App:


class MainApp(CarbonApp):
    def build(self):

        # Light Mode
        Window.clearcolor = (1, 1, 1, 1)

        # Screen Manager Config:
        sm = ScreenManager()
        sm.add_widget(SignupScreen(name='Signup'))
        sm.add_widget(LoginScreen(name='Login'))
        sm.add_widget(ForgotScreen(name='Forgot'))
        sm.current = 'Signup'

        return sm


if __name__ == "__main__":
    MainApp().run()
