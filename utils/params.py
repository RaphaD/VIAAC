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
MAX_CONNECTION_TIME = 60 * 60

# Flag received to tell that the program has to run the algo to identified by the message
FLAG_RAW_COMMAND = "[raw_command]"
# Flag received to tell that the program has to run the algo identified by the message and set the associated state in
# the database
FLAG_SET_STATE_RAW_COMMAND = "[raw_set_command]"
# Flag received to tell the client wants to get information from the server
FLAG_GET_STATE = "[get_state]"
