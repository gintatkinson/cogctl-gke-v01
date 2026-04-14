# NBI Component

The NBI component uses libyang to validate and process messages. Follow instructions below to install it.


## IMPORTANT
**TL;DR**: Use kafka-python for consuming from kafka in the NBI component.

Why:

`confluent-kafka` is written in C, thus, it bypasses eventlet monkey_patches that convert normal threads into green_threads.
That implies methods such as consumer.poll() become blocking in eventlet scenario used by gunicorn web server.

## Install libyang
- Ref: https://github.com/CESNET/libyang
- Ref: https://github.com/CESNET/libyang-python/

__NOTE__: APT package is extremely outdated and does not work for our purposes.

### Build Requisites
```bash
sudo apt-get install build-essential cmake libpcre2-dev
sudo apt-get install python3-dev gcc python3-cffi
```

### Build from source
```bash
mkdir ~/tfs-ctrl/libyang
git clone https://github.com/CESNET/libyang.git ~/tfs-ctrl/libyang
cd ~/tfs-ctrl/libyang
git fetch
git checkout v2.1.148
mkdir ~/tfs-ctrl/libyang/build
cd ~/tfs-ctrl/libyang/build
cmake -D CMAKE_BUILD_TYPE:String="Release" ..
make
sudo make install
sudo ldconfig
```

### Install Python bindings
```bash
pip install libyang==2.8.4
```
