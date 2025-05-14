import zenoh

if __name__ == "__main__":
    with zenoh.open(zenoh.Config()) as session:
      replies = session.get('myhome/kitchen/temp')
      for reply in replies:
          try:
              print("Received ('{}': '{}')"
                  .format(reply.ok.key_expr, reply.ok.payload.to_string()))
          except:
              print("Received (ERROR: '{}')"
                  .format(reply.err.payload.to_string()))