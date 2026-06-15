from carbonkivy.uix.notification import CNotificationToast
from kivy.clock import Clock

def notification_error(subtitle):
    notif = CNotificationToast(
        title="Error",
        status="Error",
        subtitle=subtitle
    )

    Clock.schedule_once(lambda dt: notif.dismiss(), 4.5)
    return notif 

def notification_success(subtitle):
    notif = CNotificationToast(
        title="Success",
        status="Success",
        subtitle=subtitle
    )
    Clock.schedule_once(lambda dt: notif.dismiss(), 4.5)
    return notif