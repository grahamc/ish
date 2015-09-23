# `ish`

![example](./contrib/example.gif)

## Instance-SSH ...ish.

[![Build Status](https://travis-ci.org/grahamc/ish.svg?branch=master)](https://travis-ci.org/grahamc/ish)

`ish` connects you to a server in your AWS account based on properties of the
server. Notably useful when you don't care which server *exactly*, just a
server of a particular type.

Currently you can connect to servers based on their:

 - name tag
 - instance id
 - autoscaling group membership
 - image id (AMI)

If more than one server matches the attribute, it will pick one and connect
you to it.

If you pass additional parameters, they will get appended to the ssh command.

In the example command, `/usr/bin/ssh ip_address echo "hello_there"` is the
run command:

```
$ ish name:openvpn echo "hello there"
hello there
```

`ish` also supports autocompletion (read below.)

## Installation

You can install via:

 - setuptools using `python3 setup.py install` and source the `contrib/ish-autocomplete` script.
 - Homebrew using `brew install https://raw.githubusercontent.com/grahamc/ish/master/ish.rb`


## Details

### Caching

To improve performance, instance metadata is stored in `$HOME/.ish.json`. This
file should be automatically replaced if it is over 60 seconds old, but delete
it if you experience issues.

### AWS Configuration

`ish` uses `boto3` which uses the standard AWS configuration stack. Read more
here: https://boto3.readthedocs.org/en/latest/guide/configuration.html#configuration-sources

### SSH Configuration

The command run is `ssh IP`. If you want to set additional configuration
settings, please use your `~/.ssh/config`.

An example SSH configuration might be

```
Host 172.*
    StrictHostKeyChecking no
    IdentityFile ~/.ssh/keys/aws-keys
    User yourusername
```

#### `ish` connects to the private instance IP

You might find this article helpful if you use a bastion / jump-host instead
of a VPN: http://edgeofsanity.net/article/2012/10/15/ssh-leap-frog.html

### Autocomplete

A full list of supported targets can be found with `ish --completion`, and a
bash and zsh compatible autocomplete script is found in `./contrib/`.

#### Auto-completing targets with spaces in them

Targets with spaces in them must be quoted, but will be autocompleted without
them. Example:

```
$ ish name:Logstash Ingestion
```

## Contributing

 - `flake8` must pass with no exceptions
 - `coverage` must report 100% coverage
 - it must run perfectly on python 3, python 2 is not supported.
