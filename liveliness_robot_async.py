import zenoh
import asyncio

"""
Robot object that can detect liveliness of other robots. Implemented using asyncio.
"""

class LivelinessRobot():
    def __init__(self, liveliness_key: str, liveliness_key_other: str):
        self.liveliness_key = liveliness_key
        self.liveliness_key_other = liveliness_key_other
        self.position = 5
        self.session = None
        self.token = None
        self.subscriber = None
        self.running = False

    async def start(self):
        """Start the robot and initialize zenoh session with liveliness tokens"""
        self.session = zenoh.open(zenoh.Config())
        print(f"Declaring LivelinessToken on '{self.liveliness_key}'...")
        self.token = self.session.liveliness().declare_token(self.liveliness_key)
        
        print(f"Searching for liveliness token on '{self.liveliness_key_other}'...")
        self.subscriber = self.session.liveliness().declare_subscriber(
            self.liveliness_key_other, 
            history=True
        )
        
        self.running = True
        # Start the liveliness monitoring task
        asyncio.create_task(self._monitor_liveliness())

    async def stop(self):
        """Stop the robot and cleanup zenoh resources"""
        self.running = False
        if self.subscriber:
            self.subscriber.undeclare()
        if self.token:
            self.token.undeclare()
        if self.session:
            self.session.close()

    async def _monitor_liveliness(self):
        """Monitor liveliness tokens from other robots"""
        while self.running:
            try:
                for sample in self.subscriber:
                    if sample.kind == zenoh.SampleKind.PUT:
                        print(f"Received liveliness token from {sample.key_expr}")
                    elif sample.kind == zenoh.SampleKind.DELETE:
                        print(f"Liveliness token from {sample.key_expr} is no longer available")
            except Exception as e:
                print(f"Error in liveliness monitoring: {e}")
            await asyncio.sleep(0.1)

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position


async def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog="liveliness_robot", description="zenoh liveliness robot example"
    )
    parser.add_argument(
        "--key1",
        "-k1",
        dest="key1",
        default="liveliness/A",
        type=str,
        help="The key expression to write.",
    )
    parser.add_argument(
        "--key2",
        "-k2",
        dest="key2",
        default="liveliness/B",
        type=str,
        help="The key expression to write.",
    )

    args = parser.parse_args()

    robot = LivelinessRobot(args.key1, args.key2)
    await robot.start()
    
    try:
        print("Robot started. Press CTRL-C to quit...")
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await robot.stop()


if __name__ == "__main__":
    asyncio.run(main())