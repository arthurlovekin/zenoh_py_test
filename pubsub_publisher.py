import zenoh, random, time
random.seed()
from zenoh.ext import z_serialize

"""
Shows how to use the zenoh serializer (as opposed to json) to publish floats and strings.
Also shows how to set a namespace
"""
        
def publish_time():
    buf = time.time()
    print(f"Putting Float Data ('{rendered_namespace}/{time_key}': '{buf}')...")
    time_pub.put(z_serialize(buf))
    time.sleep(1)

def publish_temp():
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


if __name__ == "__main__":
    config = zenoh.Config()
    custom_namespace = '\"my_namespace\"' # needs to add extra quotes to make it a string in json5
    rendered_namespace = 'my_namespace'
    config.insert_json5("namespace", custom_namespace)

    with zenoh.open(config) as session:
        temp_key = 'myhome/kitchen/temp'
        temp_pub = session.declare_publisher(temp_key)

        time_key = 'myhome/kitchen/time'
        time_pub = session.declare_publisher(time_key)

        empty_key = 'myhome/kitchen/empty'
        empty_pub = session.declare_publisher(empty_key)

        while True:
            publish_temp()
            publish_time()
            publish_empty()
            time.sleep(1)
