import zenoh
import json
import time
import random
from typing import Union, Optional



def publish_velocity_command(pub, 
                             linear_x, 
                             linear_y, 
                             linear_z,
                             angular_x,
                             angular_y,
                             angular_z):
    """
    Publish a velocity command to be executed by the robot.
    
    Args:
        pub: Zenoh publisher
        linear_x: x velocity
        linear_y: y velocity
        linear_z: z velocity
        angular_x: x angular velocity
        angular_y: y angular velocity
        angular_z: z angular velocity
    """
    # Create a command payload with all velocity components
    command = {
        "linear": {
            "x": linear_x,
            "y": linear_y,
            "z": linear_z
        },
        "angular": {
            "x": angular_x,
            "y": angular_y,
            "z": angular_z
        }
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
                publish_velocity_command(pub,
                                         linear_x=0.0,
                                         linear_y=0.0,
                                         linear_z=0.0,
                                         angular_x=0.0,
                                         angular_y=0.0,
                                         angular_z=yaw_vel)
                
                # Wait a bit before next command
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\nStopping publisher...")
            # Send a final stop command
            publish_velocity_command(pub, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) 