from carbonkivy.uix.notification import CNotificationToast

def notification_error(subtitle):
    return CNotificationToast(
        title="Error",
        status="Error",
        subtitle=subtitle
    )

def notification_success(subtitle):
    return CNotificationToast(
        title="Success",
        status="Success",
        subtitle=subtitle
    )