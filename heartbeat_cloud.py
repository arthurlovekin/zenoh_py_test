from heartbeat import Heartbeat
import time
import zenoh

# TODO: use liveliness instead https://github.com/eclipse-zenoh/roadmap/blob/main/rfcs/ALL/Liveliness.md
def on_disconnect():
    print("Disconnected from Robot")

def on_connect():
    print("Connected to Robot")

with zenoh.open(zenoh.Config()) as session:
    heartbeat = Heartbeat(
        session=session,
        pub_topic='cloud/heartbeat',
        sub_topic='robot/heartbeat',
        heartbeat_interval_seconds=0.5,
        heartbeat_timeout_seconds=2.0,
        on_disconnect=on_disconnect,
        on_connect=on_connect,
    )

    while True: 
        time.sleep(1)