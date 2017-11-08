import subprocess


subprocess.call('x-terminal-emulator -e python3 client.py 127.0.0.1', shell=True)
subprocess.call('x-terminal-emulator -e python3 client.py 127.0.0.1 -w', shell=True)