sudo apt update
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install -y python3.12 python3.12-venv python3.12-dev
curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3.12 get-pip.py
sudo apt install -y libffi-dev build-essential
python3.12 -m pip install --force-reinstall cryptography
