from plyer import notification
import time

while True:
    time.sleep(3600)

    notification.notify(
        title="It's time to break",
        message="An hour has passed",
        timeout=5
    )
