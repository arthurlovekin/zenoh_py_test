import zenoh, time
from zenoh.ext import z_deserialize, Float64

"""
Shows how to use the zenoh serializer (as opposed to json) to subscribe to floats and strings.
Also shows how to set a namespace
"""

def print_sample_attributes(sample):
    attrs = [attr for attr in dir(sample) if not attr.startswith("__") and not callable(getattr(sample, attr))]
    print("Available sample attributes:")
    for attr in attrs:
        try:
            value = getattr(sample, attr)
        except Exception as e:
            value = f"<error: {e}>"
        print(f"  {attr}: {value}")


def string_listener(sample):
    print(f"Received {sample.kind} ('{sample.key_expr}': '{sample.payload.to_string()}')")
    # print_sample_attributes(sample)

def float_listener(sample):
    print(f"Received {sample.kind} ('{sample.key_expr}': '{z_deserialize(Float64, sample.payload)}')")
    # print_sample_attributes(sample)

def empty_listener(sample):
    print(f"Received {sample.kind} ('{sample.key_expr}': '{sample.payload.to_string()}')")

if __name__ == "__main__":
    config = zenoh.Config()
    config.insert_json5("namespace", '\"my_namespace\"')

    with zenoh.open(config) as session:
        temp_sub = session.declare_subscriber('myhome/kitchen/temp', string_listener)
        time_sub = session.declare_subscriber('myhome/kitchen/time', float_listener)
        vel_sub = session.declare_subscriber('cmd_vel', string_listener)
        empty_sub = session.declare_subscriber('myhome/kitchen/empty', empty_listener)

        time.sleep(60)