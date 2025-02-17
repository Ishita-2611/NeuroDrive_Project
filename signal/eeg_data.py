from brainflow.board_shim import BoardShim, BrainFlowInputParams
import numpy as np
import pandas as pd
import time

# Configure BrainFlow parameters
params = BrainFlowInputParams()
params.serial_port = "/dev/cu.UBONCL410 Serial Port"  # Change based on your PC (Linux: "/dev/ttyUSB0", Mac: "/dev/tty.usbserial")

# Initialize Board
board = BoardShim(2, params)  # 2 is the board ID for the Upside Down Labs BCI Kit
board.prepare_session()
board.start_stream()

# Collect data for 30 seconds
print("Collecting EEG data...")
time.sleep(30)

# Stop and retrieve data
board.stop_stream()
data = board.get_board_data()
board.release_session()

# Save data to CSV
df = pd.DataFrame(data)
df.to_csv("eeg_data.csv", index=False)
print("Data saved to eeg_data.csv")
