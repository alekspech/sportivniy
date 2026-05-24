import sys 
import time

for i in range(6):
    sys.stdout.write(f'\r{i} csgo')
    sys.stdout.flush()
    time.sleep(1) 