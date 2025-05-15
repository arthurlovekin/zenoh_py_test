"""
Creates a liveliness token to which others can subscribe
and subscribes to liveliness tokens from others.
This way, you can detect on both ends which other nodes are alive.

To run this example, start two instances of this program,
each with different key arguments.

$ python liveliness_bidirectional.py --key1 liveliness/A --key2 liveliness/B

$ python liveliness_bidirectional.py --key1 liveliness/B --key2 liveliness/A

First you start one instance. Then when you start the second instance,
the first instance will print that the second instance is alive, 
and the second instance will print that the first instance is alive.
Then if you stop one instance, the other will print that the other instance is dead.
"""

import zenoh
import time

def run(key1: str, key2: str):
    config = zenoh.Config()
    with zenoh.open(config) as session:
        print(f"Declaring LivelinessToken on '{key1}'...")
        with session.liveliness().declare_token(key1) as token1:
            print(f"Searching for liveliness token on '{key2}'...")
            with session.liveliness().declare_subscriber(key2, history=True) as sub:
                for sample in sub:
                    if sample.kind == zenoh.SampleKind.PUT:
                        print(f"Received liveliness token from {sample.key_expr}")
                    elif sample.kind == zenoh.SampleKind.DELETE:
                        print(f"Liveliness token from {sample.key_expr} is no longer available")


                print("Press CTRL-C to quit...")
                while True:
                        time.sleep(1)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="liveliness_bidirectional", description="zenoh liveliness bidirectional example"
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

    run(args.key1, args.key2)

