import zenoh
import json
import time
import random
from typing import Union, Optional

class Velocity:
    def __init__(self, x_vel: float = 0.0, y_vel: float = 0.0, z_vel: float = 0.0):
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.z_vel = z_vel

def publish_velocity_command(pub, linear_velocity: Velocity, angular_velocity: Velocity, 
                            duration: Optional[float] = None, name: str = ""):
    """
    Publish a velocity command to be executed by the robot.
    
    Args:
        pub: Zenoh publisher
        linear_velocity (Velocity): contains x velocity (x_vel), y velocity (y_vel), z_vel is discarded
        angular_velocity (Velocity): contains yaw to turn by (z_vel), x_vel and y_vel are discarded
        duration (optional, Union[float, None]): number of seconds that the robot should move before stopping
        name (optional, str): unused
    """
    # Create a command payload with all velocity components
    command = {
        "linear": {
            "x": linear_velocity.x_vel,
            "y": linear_velocity.y_vel
        },
        "angular": {
            "z": angular_velocity.z_vel
        },
        "duration": duration
    }
    
    # Convert to JSON string
    payload = json.dumps(command)
    
    print(f"Publishing velocity command: {payload}")
    pub.put(payload)


if __name__ == "__main__":
    # Load configuration from file
    config_name = "zenoh-peer-config.json5"
    config = zenoh.Config.from_file(config_name)
    
    with zenoh.open(config) as session:
        # Declare publisher once
        key = 'robot/velocity/command'
        pub = session.declare_publisher(key)
        
        print("Starting continuous velocity command publisher...")
        print("Press Ctrl+C to stop")
        
        try:
            yaw_vel = 0.5
            while True:
                # Generate random velocities
                yaw_vel *= -1
                linear_vel = Velocity(x_vel=0.0, y_vel=0.0, z_vel=0.0)
                angular_vel = Velocity(x_vel=0.0, y_vel=0.0, z_vel=yaw_vel)
                duration = 2.0
                publish_velocity_command(pub, linear_vel, angular_vel, duration)
                
                # Wait a bit before next command
                time.sleep(2*duration)
                
        except KeyboardInterrupt:
            print("\nStopping publisher...")
            # Send a final stop command
            publish_velocity_command(pub, Velocity(), Velocity(), None) 