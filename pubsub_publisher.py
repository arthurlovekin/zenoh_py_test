import zenoh, random, time
import json
from typing import Optional
random.seed()
from zenoh.ext import z_serialize


# class Velocity:
#     def __init__(self, x_vel: float = 0.0, y_vel: float = 0.0, z_vel: float = 0.0):
#         self.x_vel = x_vel
#         self.y_vel = y_vel
#         self.z_vel = z_vel

# def publish_velocity_command(linear_velocity: Velocity, angular_velocity: Velocity, 
#                             duration: Optional[float] = None, name: str = ""):
#        # Create a command payload with all velocity components
#         command = {
#             "linear": {
#                 "x": linear_velocity.x_vel,
#                 "y": linear_velocity.y_vel,
#                 "z": 0
#             },
#             "angular": {
#                 "x": 0,
#                 "y": 0,
#                 "z": angular_velocity.z_vel
#             },
#             "duration": duration
#         }
        
#         # Convert to JSON string
#         payload = json.dumps(command)
        
#         print(f"Publishing velocity command: {payload}")
#         vel_pub.put(payload)
        
def publish_time():
    buf = time.time()
    print(f"Putting Float Data ('{time_key}': '{buf}')...")
    time_pub.put(z_serialize(buf))
    time.sleep(1)

def publish_temp():
    t = random.randint(15, 30)
    buf = f"{t}"
    print(f"Putting String Data ('{temp_key}': '{buf}')...")
    temp_pub.put(buf)
    time.sleep(1)


if __name__ == "__main__":
    with zenoh.open(zenoh.Config()) as session:
        temp_key = 'myhome/kitchen/temp'
        temp_pub = session.declare_publisher(temp_key)

        time_key = 'myhome/kitchen/time'
        time_pub = session.declare_publisher(time_key)

        vel_topic = 'cmd_vel'
        vel_pub = session.declare_publisher(vel_topic)

        while True:
            publish_temp()
            publish_time()
            # publish_velocity_command(
            #      Velocity(x_vel=0.5, y_vel=0.0), 
            #      Velocity(z_vel=0.2), duration=3.0
            # )
            time.sleep(3)
