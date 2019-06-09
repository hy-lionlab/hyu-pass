MaxMind provides a PPA for recent version of Ubuntu. To add the PPA to your APT sources, run:

```
$ sudo add-apt-repository ppa:maxmind/ppa
```

Then install the packages by running:

```
$ sudo apt update
$ sudo apt install libmaxminddb0 libmaxminddb-dev mmdb-bin
```

If you are on OS X and you have homebrew (see http://brew.sh/) you can install libmaxminddb via brew.

```
$ brew install libmaxminddb
```