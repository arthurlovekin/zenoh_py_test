import zenoh
import json
import time
import threading

class NetworkRobotBridge:
    def __init__(self, zenoh_config_name):
        """Start the velocity command subscriber"""
        config = zenoh.Config.from_file(zenoh_config_name)

        self.robot_client = None  # spawn the Go2 or husky according to the environment
        self.running = True
        with zenoh.open(config) as session:
            sub = session.declare_subscriber('robot/velocity/command', self.command_callback)
            print("Velocity command subscriber started. Waiting for commands...")
            
            # Keep the subscriber running
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping subscriber...")
                self.running = False
                # Exiting the 'with' block will stop the subscriber

    def command_callback(self, sample):
        """Callback for received velocity commands"""
        command_data = sample.payload.to_string()
        print(f"Received command: {command_data}")
        
        # Now you would actually make the robot move using the robot client

if __name__ == "__main__":
    # Create and start the robot controller
    config_name = "zenoh-peer-config.json5"
    controller = NetworkRobotBridge(config_name)