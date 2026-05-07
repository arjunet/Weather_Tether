from kivy.utils import platform

def trigger_password_suggestion():
    if platform == "android":
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        View = autoclass('android.view.View')
    
        activity = PythonActivity.mActivity
        window = activity.getWindow()
        view = window.getDecorView()
    
        view.setImportantForAutofill(View.IMPORTANT_FOR_AUTOFILL_YES)
        view.setAutofillHints([View.AUTOFILL_HINT_PASSWORD])

    else:
        pass