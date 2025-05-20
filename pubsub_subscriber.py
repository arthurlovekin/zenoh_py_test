import zenoh, time
from zenoh.ext import z_deserialize, Float64
import json

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

def json_listener(sample):
    print(f"Received {sample.kind} ('{sample.key_expr}': '{sample.payload.to_string()}')")
    try:
        data = json.loads(sample.payload.to_string())
        print("Received JSON data:")
        for key, value in data.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error parsing JSON: {e}")

if __name__ == "__main__":
    config = zenoh.Config()
    config.insert_json5("namespace", '\"my_namespace\"')

    with zenoh.open(config) as session:
        print("Starting subscriber...")
        temp_sub = session.declare_subscriber('zenoh_test/key/temp', string_listener)
        time_sub = session.declare_subscriber('zenoh_test/key/time', float_listener)
        json_sub = session.declare_subscriber('zenoh_test/key/json', json_listener)
        empty_sub = session.declare_subscriber('zenoh_test/key/empty', empty_listener)

        time.sleep(60)