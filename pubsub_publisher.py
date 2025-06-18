import zenoh, random, time
import argparse
random.seed()
from zenoh.ext import z_serialize
import json

"""
Shows how to use the zenoh serializer (as opposed to json) to publish floats and strings.
Also shows how to set a namespace
"""
        
def publish_float():
    buf = time.time()
    print(f"Putting Float Data ('{rendered_namespace}/{time_key}': '{buf}')...")
    time_pub.put(z_serialize(buf))
    time.sleep(1)

def publish_string():
    t = random.randint(15, 30)
    buf = f"{t}"
    print(f"Putting String Data ('{rendered_namespace}/{temp_key}': '{buf}')...")
    temp_pub.put(buf)
    time.sleep(1)

def publish_empty():
    buf = ""
    print(f"Putting Empty Data ('{rendered_namespace}/{empty_key}': '{buf}')...")
    empty_pub.put(buf)
    time.sleep(1)

def publish_json():
    buf = {
        "name": "John",
        "age": 30,
        "city": "New York"
    }
    print(f"Putting JSON Data ('{rendered_namespace}/{json_key}': '{buf}')...")
    json_pub.put(json.dumps(buf))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='zenoh-pub',
                                    description='zenoh publisher example')
    parser.add_argument('-c', '--config', type=str, help='path to the configuration file')
    args = parser.parse_args()

    if args.config:
        config = zenoh.Config.from_json5(open(args.config).read())
    else:
        config = zenoh.Config()
        
    custom_namespace = '\"my_namespace\"' # needs to add extra quotes to make it a string in json5
    rendered_namespace = 'my_namespace'
    config.insert_json5("namespace", custom_namespace)

    with zenoh.open(config) as session:
        print("Starting publisher...")
        temp_key = 'zenoh_test/key/temp'
        temp_pub = session.declare_publisher(temp_key)

        time_key = 'zenoh_test/key/time'
        time_pub = session.declare_publisher(time_key)

        empty_key = 'zenoh_test/key/empty'
        empty_pub = session.declare_publisher(empty_key)

        json_key = 'zenoh_test/key/json'
        json_pub = session.declare_publisher(json_key)

        while True:
            publish_float()
            publish_string()
            publish_empty()
            publish_json()
            time.sleep(1)
