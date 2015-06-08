__author__ = 'fums'

# Some variables needed for the server initialisation
PORT_SERVER = 9004  # Opened port
CLIENT_TRESHOLD = 5  # Same-time connections

# Some variables needed for the arduino communication initialisation
USB_PORT = "/dev/ttyACM0"
BAUDRATE = 9600

# Some variables needed for the main server initialisation
# Time before checking connection time
SOCKET_TIMEOUT = 2.0
# Size of the buffer used to receive messages from clients
BUFFER_SIZE = 1024
# Unactivity time before closing connection with
MAX_CONNECTION_TIME = 10