import socket
import serial
import time
import logging
import serial.tools.list_ports
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('arduino_comm.log'),
        logging.StreamHandler()
    ]
)

def find_arduino_port(preferred_ports=None):
    """
    Dynamically find Arduino port with optional preferred port list.
    
    :param preferred_ports: List of preferred port names/patterns
    :return: First matching port or None
    """
    preferred_ports = preferred_ports or ['USB', 'ACM', 'Arduino']
    
    ports = list(serial.tools.list_ports.comports())
    logging.info(f"Available ports: {[port.device for port in ports]}")
    
    # First try exact match with preferred ports
    for port in ports:
        for pref in preferred_ports:
            if pref.lower() in port.description.lower() or pref.lower() in port.device.lower():
                logging.info(f"Found Arduino port: {port.device} ({port.description})")
                return port.device
    
    # Fallback to default ports if no match
    if sys.platform.startswith('win'):
        fallback_ports = [f'COM{i}' for i in range(1, 21)]  # COM1-COM20
    else:
        fallback_ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0']
    
    for fallback in fallback_ports:
        try:
            test_serial = serial.Serial(fallback, 9600, timeout=1)
            test_serial.close()
            logging.info(f"Using fallback port: {fallback}")
            return fallback
        except (serial.SerialException, OSError):
            continue
    
    logging.error("No suitable Arduino port found")
    return None

def establish_serial_connection(port, baudrate=9600, timeout=2):
    """
    Establish and verify serial connection.
    
    :param port: Serial port name
    :param baudrate: Communication speed
    :param timeout: Connection timeout
    :return: Serial connection object
    """
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
            write_timeout=timeout
        )
        time.sleep(2)  # Allow Arduino reset time
        ser.flush()
        
        # Test connection
        ser.write(b"TEST\n")
        time.sleep(0.1)
        if ser.in_waiting:
            response = ser.readline().decode().strip()
            logging.info(f"Arduino test response: {response}")
        
        logging.info(f"Serial connection established on {port}")
        return ser
    except serial.SerialException as e:
        logging.error(f"Serial connection error: {e}")
        return None

def setup_socket_server(host='0.0.0.0', port=5005, max_retries=5):
    """
    Set up TCP socket server.
    
    :param host: Binding host
    :param port: Binding port
    :param max_retries: Maximum number of port binding retries
    :return: Socket server object
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    for retry in range(max_retries):
        try:
            server.bind((host, port + retry))
            server.listen(1)
            logging.info(f"Socket server listening on {host}:{port + retry}")
            return server
        except socket.error as e:
            logging.warning(f"Port {port + retry} binding failed: {e}")
            if retry == max_retries - 1:
                logging.error("All port binding attempts failed")
                return None
            continue
    return None

def handle_arduino_communication(ser, conn):
    """
    Handle communication between socket and Arduino.
    
    :param ser: Serial connection
    :param conn: Socket connection
    """
    try:
        while True:
            # Receive command from socket
            data = conn.recv(1024).decode().strip()
            if not data:
                logging.info("Connection lost")
                break
            
            logging.info(f"Received command: {data}")
            
            # Verify serial connection is still valid
            if not ser.is_open:
                logging.error("Serial connection lost")
                conn.send("SERIAL_ERROR".encode())
                break
            
            # Send to Arduino
            try:
                ser.write((data + "\n").encode())
            except serial.SerialException as e:
                logging.error(f"Failed to write to Arduino: {e}")
                conn.send("WRITE_ERROR".encode())
                break
            
            # Wait for Arduino response
            start_time = time.time()
            response = ""
            while time.time() - start_time < 2:
                if ser.in_waiting:
                    try:
                        response = ser.readline().decode().strip()
                        if response:
                            logging.info(f"Arduino response: {response}")
                            conn.send(response.encode())
                            break
                    except serial.SerialException as e:
                        logging.error(f"Failed to read from Arduino: {e}")
                        conn.send("READ_ERROR".encode())
                        return
                time.sleep(0.1)
            
            if not response:
                logging.warning("No Arduino response")
                conn.send("NO_RESPONSE".encode())
    
    except (socket.error, serial.SerialException) as e:
        logging.error(f"Communication error: {e}")

def main():
    """
    Main communication loop.
    """
    # Find Arduino port
    arduino_port = find_arduino_port()
    if not arduino_port:
        logging.critical("Cannot proceed without Arduino port")
        return
    
    # Establish serial connection
    ser = establish_serial_connection(arduino_port)
    if not ser:
        logging.critical("Serial connection failed")
        return
    
    # Setup socket server
    server = setup_socket_server()
    if not server:
        logging.critical("Socket server setup failed")
        ser.close()
        return
    
    try:
        while True:
            logging.info("Waiting for Raspberry Pi connection...")
            conn, addr = server.accept()
            
            try:
                logging.info(f"Connected by {addr}")
                handle_arduino_communication(ser, conn)
            except Exception as e:
                logging.error(f"Connection handling error: {e}")
            finally:
                conn.close()
    
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        server.close()
        ser.close()

if __name__ == "__main__":
    main()