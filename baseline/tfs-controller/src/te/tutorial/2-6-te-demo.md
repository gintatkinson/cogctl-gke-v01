# 2.6. Traffic Engineering Demo

## Setup Test-Bed

### Setup libyang

    $ sudo apt update
    $ sudo apt-get install cmake libpcre2-dev git make build-essential
    $ mkdir -p ~/testbed
    $ cd ~/testbed
    $ git clone git@github.com:CESNET/libyang.git
    $ cd libyang
    $ git checkout v2.0.0
    $ mkdir build; cd build
    $ cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D CMAKE_BUILD_TYPE:String="Release" ..
    $ make
    $ sudo make install


### Setup Free Range Routing

    $ sudo apt update
    $ sudo apt-get install git autoconf automake libtool make libreadline-dev texinfo pkg-config libpam0g-dev libjson-c-dev bison flex libc-ares-dev python3-dev python3-sphinx install-info build-essential libsnmp-dev perl libcap-dev python2 libelf-dev libunwind-dev protobuf-c-compiler libprotobuf-c-dev libsystemd-dev
    $ mkdir -p ~/testbed
    $ cd ~/testbed
    $ git clone git@github.com:opensourcerouting/frr.git
    $ cd frr
    $ curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
    $ sudo python2 ./get-pip.py
    $ export CFLAGS="-I /usr/local/include -g -O2"
    $ sudo rm -rf /usr/lib/frr
    $ sudo rm -rf /var/run/frr
    $ sudo mkdir -p /etc/frr
    $ sudo mkdir -p /var/run/frr
    $ sudo chown -R root:root /etc/frr
    $ ./bootstrap.sh
    $ ./configure \
        --prefix=/usr \
        --includedir=\${prefix}/include \
        --enable-exampledir=\${prefix}/share/doc/frr/examples \
        --bindir=\${prefix}/bin \
        --sbindir=\${prefix}/lib/frr \
        --libdir=\${prefix}/lib/frr \
        --libexecdir=\${prefix}/lib/frr \
        --localstatedir=/var/run/frr \
        --sysconfdir=/etc/frr \
        --with-moduledir=\${prefix}/lib/frr/modules \
        --enable-configfile-mask=0640 \
        --enable-logfile-mask=0640 \
        --enable-snmp=agentx \
        --enable-multipath=64 \
        --enable-user=root \
        --enable-group=root \
        --enable-vty-group=root \
        --enable-vtysh \
        --with-pkg-git-version \
        --with-pkg-extra-version=-MyOwnFRRVersion \
        --enable-systemd=yes \
        --enable-config-rollbacks \
        --enable-pathd \
        --enable-pcep
    $ make
    $ sudo make install


### Setup NetGen

    $ sudo apt update
    $ sudo apt-get install git ruby ruby-dev tmux gettext-base
    $ mkdir -p ~/testbed
    $ cd ~/testbed
    $ git clone git@github.com:sylane/netgen.git
    $ cd netgen
    $ git checkout teraflow
    $ sudo gem install bundler:1.15
    $ bundle _1.15_ install


### Run the Test-Bed

First load the [teraflow configuration file](~/tfs-ctrl/src/te/tests/topology-descriptors.json) using the webui.

In first console:
    $ cd ~/testbed
    $ ../tfs-ctrl/src/te/tests/start-testbed.sh

Then in second console:
    $ sudo -i
    # cd /tmp/negen
    # ./tmux.sh

Be sure that both PCC connected to the TE service before going further.
This can be done by looking at the TE service log:

    $ kubectl --namespace tfs logs $(kubectl --namespace tfs get pods --selector=app=teservice -o name) -c server

### Setup a flow from the Erlang console

We will setup two unidirectional flow between router 1 and 6.
We will use the binding label 1111 for the flow from router 1 to router 6, and the binding label 6666 for the flow from router 6 to router 1.

    $ kubectl --namespace tfs exec -ti $(kubectl --namespace tfs get pods --selector=app=teservice -o name) -c server -- /tfte/bin/tfte remote_console
    1> {ok, Flow1to6} = epce_server:initiate_flow(<<"foo">>, {1, 1, 1, 1}, {6, 6, 6, 6}, 1111).
    2> {ok, Flow6to1} = epce_server:initiate_flow(<<"bar">>, {6, 6, 6, 6}, {1, 1, 1, 1}, 6666).

Another option is to use the router names:

    1> {ok, Flow1to6} = epce_server:initiate_flow(<<"foo">>, <<"RT1">>, <<"RT6">>, 1111).
    2> {ok, Flow6to1} = epce_server:initiate_flow(<<"bar">>, <<"RT6">>, <<"RT1">>, 6666).

Now if we go to the tmux session src (Ctrl-B 0) we can ping dst:

    $ ping 9.9.9.2

From the Erlang console we can update the initiated flows to change the path the packets are flowing through:

    3> epce_server:update_flow(Flow6to1, [16050, 16030, 16010]).

### Setup a flow using the GRPC test script

This does the same as the the setup from the Erlang console, but through GRPC.
After deploying Teraflow (with te), get the te service ip using:

    $ kubectl -n tfs get services

Replace the IP in the python script `src/te/tests/test_te_service.py`.
Be sure the topology as been loaded, and netgen started as described previously,
and run the following command from the root of the teraflow controller:

    $ PYTHONPATH=./src python src/te/tests/test_te_service.py
