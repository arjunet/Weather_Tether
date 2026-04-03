from carbonkivy.uix.notification import CNotificationInline
from carbonkivy.uix.notification import CNotificationToast

def notification_error(subtitle):
    return CNotificationInline(
        title="Error",
        status="Error",
        subtitle=subtitle  # This takes the text from main.py
    )

def notification_success(subtitle):
    return CNotificationInline(
        title="Success",
        status="Success",
        subtitle=subtitle
    )

def forgot_notification():
    return CNotificationToast(
                title="Success",
                subtitle="Successfully Sent Reset Email. If You Don't See It, Check Your Spam Folder. If You Still Don't See It, The Email May Not Be Registered.",
                status="Success",
                pos_hint={"center_x": 0.5, "y": 0.57},
            )