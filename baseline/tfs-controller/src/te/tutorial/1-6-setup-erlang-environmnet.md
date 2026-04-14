# 1.5. Setup Erlang Environment

First we need to install Erlang. There is multiple way, for development we will
be using *ASDF*, a tool that allows the installation of multiple version of Erlang
at the same time, and switch from one version to the other at will.


## 1.5.1. Setup Erlang using asdf

First, install any missing dependencies:

    sudo apt install curl git autoconf libncurses-dev build-essential m4 libssl-dev 

Download *ASDF* tool to the local account:

    git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.10.2

Make *ASDF* activate on login by adding these lines at the end of the `~/.bashrc` file:

    . $HOME/.asdf/asdf.sh
    . $HOME/.asdf/completions/asdf.bash

Logout and log back in to activate *ASDF*.

*ASDF* supports multiple tools by installing there corresponding plugins.
Install *ASDF* plugin for Erlang:

    asdf plugin add erlang https://github.com/asdf-vm/asdf-erlang.git

Install a version of Erlang:

    asdf install erlang 24.3.4.2

Activate Erlang locally for TFS controller. This will create a local file
called `.tool-versions` defining which version of the tools to use when
running under the current directory:

    cd tfs-ctrl/
    asdf local erlang 24.3.4.2

Erlang projects uses a build tool called rebar3. It is used to manager project
dependenecies, compile a project and generate project releases.
Install rebar3 localy from source:

    cd ~
    git clone https://github.com/erlang/rebar3.git
    cd rebar3
    asdf local erlang 24.3.4.2
    ./bootstrap
    ./rebar3 local install

Update `~/.bashrc` to use rebar3 by adding this line at the end:

    export PATH=$HOME/.cache/rebar3/bin:$PATH

Logout and log back in.
