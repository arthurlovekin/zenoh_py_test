import threading
import time
from zenoh.ext import z_serialize, z_deserialize, Float64
from typing import Optional, Callable

# TODO: use liveliness instead https://github.com/eclipse-zenoh/roadmap/blob/main/rfcs/ALL/Liveliness.md
class Heartbeat:
    """
    Publishes a heartbeat and listens for a heartbeat from a peer 
    in order to detect network connection loss.
    
    Attributes:
        heartbeat_interval_seconds (float): Time between heartbeat publications
        heartbeat_timeout_seconds (float): Time before considering connection lost
        _connected (bool): Current connection state
        _last_heartbeat_local_time (Optional[float]): Time of last received heartbeat
        _last_heartbeat_remote_time (Optional[float]): Remote timestamp of last received heartbeat
        _heartbeat_running (bool): Whether the heartbeat thread is running
        _heartbeat_thread (Optional[threading.Thread]): The heartbeat thread
    """
    
    def __init__(self, 
                 session,
                 pub_topic: str,
                 sub_topic: str,
                 heartbeat_interval_seconds: float = 0.1,
                 heartbeat_timeout_seconds: float = 1.0,
                 on_disconnect: Optional[Callable[[], None]] = None,
                 on_connect: Optional[Callable[[], None]] = None):
        """Initialize the Heartbeat.
        
        Args:
            session: Zenoh session to use for communication
            topic: Topic to use for heartbeat messages
            heartbeat_interval_seconds: Time between heartbeat publications
            heartbeat_timeout_seconds: Time before considering connection lost
            on_disconnect: Optional callback to execute when connection is lost
            on_connect: Optional callback to execute when connection is restored
        """
        self.session = session
        self.pub_topic = pub_topic
        self.sub_topic = sub_topic
        self.heartbeat_interval_seconds = heartbeat_interval_seconds
        self.heartbeat_timeout_seconds = heartbeat_timeout_seconds
        self.on_disconnect = on_disconnect
        self.on_connect = on_connect
        self.connected = False

        self._last_heartbeat_local_time = None
        self._last_heartbeat_remote_time = None
        self._heartbeat_running = False
        self._heartbeat_thread = None
        self._heartbeat_pub = None
        self._heartbeat_sub = None

        self.start()
        print(f"Publishing heartbeat on {self.pub_topic} and listening on {self.sub_topic}. Waiting for connection...")
        
    def start(self):
        """Start the heartbeat thread."""
        if self._heartbeat_thread is not None and self._heartbeat_thread.is_alive():
            return

        self._heartbeat_running = True
        self._heartbeat_pub = self.session.declare_publisher(self.pub_topic)
        self._heartbeat_sub = self.session.declare_subscriber(self.sub_topic, self.handle_heartbeat)
        self._heartbeat_thread = threading.Thread(target=self._heartbeat_loop)
        self._heartbeat_thread.daemon = True
        self._heartbeat_thread.start()
        
    def stop(self):
        """Stop the heartbeat thread."""
        self._heartbeat_running = False
        if self._heartbeat_thread is not None:
            self._heartbeat_thread.join(timeout=1.0)
            self._heartbeat_thread = None
        if self._heartbeat_sub is not None:
            self._heartbeat_sub = None
        if self._heartbeat_pub is not None:
            self._heartbeat_pub = None

            
    def handle_heartbeat(self, sample):
        """Handle an incoming heartbeat message.
        
        Args:
            sample: Zenoh sample containing the heartbeat message
        """
        try:
            # Deserialize the float value directly
            remote_time = z_deserialize(Float64, sample.payload)
            if remote_time is None:
                print("Warning: Received heartbeat with no timestamp")
                return

            local_time = time.time()
            if (self._last_heartbeat_local_time is None or 
                self._last_heartbeat_remote_time is None
                or (remote_time > self._last_heartbeat_remote_time and 
                    local_time > self._last_heartbeat_local_time)):
                self._last_heartbeat_local_time = local_time
                self._last_heartbeat_remote_time = remote_time
                if not self.connected and self.on_connect:
                    self.on_connect()
                self.connected = True
        except Exception as e:
            print(f"Warning: Error processing heartbeat: {e}")
            
    def _heartbeat_loop(self):
        """Main heartbeat loop that publishes heartbeats and monitors connection."""
        while self._heartbeat_running:
            try:
                # Publish our heartbeat as a serialized float
                current_time = time.time()
                self._heartbeat_pub.put(z_serialize(current_time))

                # Check if we've received a heartbeat
                if self._last_heartbeat_local_time is not None:
                    time_since_last = current_time - self._last_heartbeat_local_time
                    if time_since_last > self.heartbeat_timeout_seconds:
                        if self.connected:
                            print(f"Warning: Network connection broken. No heartbeat received for {time_since_last:.2f} seconds")
                            self.connected = False
                            if self.on_disconnect:
                                self.on_disconnect()
                    else:
                        if not self.connected:
                            print("Network connection restored")
                            self.connected = True
                            if self.on_connect:
                                self.on_connect()

                # Sleep until next heartbeat
                time.sleep(self.heartbeat_interval_seconds)
            except Exception as e:
                print(f"Error in heartbeat loop: {e}")
                time.sleep(self.heartbeat_interval_seconds)  # Still sleep to prevent tight loop
                
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop() 