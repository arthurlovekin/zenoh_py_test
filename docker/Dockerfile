# syntax=docker/dockerfile:1

# How to build and run:
# docker build -t zenoh-pubsub .
# docker run --network host zenoh-pubsub pubsub_subscriber.py
# docker run --network host zenoh-pubsub pubsub_publisher.py

FROM python:3.9-slim
WORKDIR /app
RUN pip install --no-cache-dir eclipse-zenoh
COPY pubsub_publisher.py .
COPY pubsub_subscriber.py .

# run python -u to avoid buffering
ENTRYPOINT ["python", "-u"] 
CMD ["pubsub_publisher.py"]
