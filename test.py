from pypresence import Presence
import time

client_id = '763966672893509642'

class test:
    state = "test"
    details = "test"
    large_image = "test"
    small_image = "test"
    large_text = "test"
    small_text = "test"
    start = 1602216040

try :
    RPC = Presence(client_id)
    RPC.connect()
    print("RPC connection successful.")
except ConnectionRefusedError:
    raise Exception("Failed RPC connection.")

while True:
    RPC.update(details="Coding or Jamming out.", large_image='me', start=test.start, large_text="Yes it's me. Stop asking.")
    time.sleep(15)
