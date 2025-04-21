#!/bin/bash

# Terminal 1: Run serverMain.py in Def-Programming/Server
gnome-terminal -- bash -c "cd ./Server && python3.12 serverMain.py; exec bash"

# Wait 2 seconds
sleep 2

# Terminal 2: Run client.py in Def-Programming/Client/Backend
gnome-terminal -- bash -c "cd ./Client/Backend && python3.12 client.py; exec bash"
