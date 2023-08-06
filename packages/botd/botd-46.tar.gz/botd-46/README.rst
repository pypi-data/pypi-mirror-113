README
######

Welcome to BOTD,

BOTD is a pure python3 IRC chat bot that can run as a background daemon
for 24/7 a day presence in a IRC channel, it can be used to display RSS feeds,
act as a UDP to IRC relay and you can program your own commands for it.

BOTD is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

install
=======

installation is through pypi, use the superuser (sudo)::

 $ pip3 install botd --upgrade --force-reinstall
 $ cp /usr/local/share/botd/botd.service /etc/systemd/system
 $ systemctl enable botd
 $ botctl cfg server=botd.io
 $ systemctl start botd

rss
===

add an url use the rss command with an url::

 $ botctl rss https://github.com/bthate/botd/commits/master.atom
 ok

run the fnd (find) command to see what urls are registered::

 $ botctl fnd rss
 0 https://github.com/bthate/botd/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds::

 $ botctl ftc
 fetched 20

programming
===========

the bot package provides a library (ob.py) you can use to program objects 
under python3. It provides a basic Object, that mimics a dict while using 
attribute access and provides a save/load to/from json files on disk. objects
can be searched with a little database module, it uses read-only files to
improve persistence and a type in filename for reconstruction.

basic usage is this::

 >>> from ob import Object
 >>> o = Object()
 >>> o.key = "value"
 >>> o.key
 'value'

objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided as are the basic
methods like get, items, keys, register, set, update, values.

the bot.obj module has the basic methods like load and save as a object
function using an obj as the first argument::

 >>> import ob
 >>> ob.wd = "data"
 >>> o = ob.Object()
 >>> o["key"] = "value"
 >>> p = o.save()
 >>> p
 'ob.Object/4b58abe2-3757-48d4-986b-d0857208dd96/2021-04-12/21:15:33.734994
 >>> oo = ob.Object()
 >>> oo.load(p)
 >> oo.key
 'value'

great for giving objects peristence by having their state stored in files.

modules
=======

BOTD's bot package is a pure python3 bot library you can use to program 
bots, uses a JSON in file database with a versioned readonly storage and
reconstructs objects based on type information in the path.

the following modules are provided::

    adm			- administration
    all			- all modules
    cms			- commands
    fnd			- find
    irc			- intermet relay chat
    log			- log text
    rss			- rich site syndicate 
    tdo			- todo
    udp			- udp to irc relay

commands
========

modules are not read from a directory, instead you must include your own
written commands with a updated version of the code. First clone the
repository (as user)::

 $ git clone http://github.com/bthate/botd
 $ cd botd
 
to program your own commands, open bot/hlo.py (new file) and add the following
code::

    def hlo(event):
        event.reply("hello %s" % event.origin)

add the hlo module to the bot/all.py module::

    import bot.hlo

then install with python3 (using sudo)::

 $ python3 setup.py install
 $ python3 setup.py install_data

reload the systemd service::

 $ systemctl stop botd
 $ systemctl start botd

now you can type the "hlo" command, showing hello <user>::

 <bart> !hlo
 hello root@console

udp
===

there is also the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed in the channel.
output to the IRC channel is done with the use python3 code to send a UDP
packet to BOTD, it's unencrypted txt send to the bot and displayed in the
joined channels::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

to have the udp relay running, add udp to the all variable in bin/botd::

    all = "adm,cms,fnd,irc,krn,log,rss,tdo,udp"

users
=====

if the users option is set in the irc config then users need to be added 
before they can give commands, use the met command to introduce a user::

 $ sudo botctl met ~bart@botd.io
 ok

debug
=====

as of version 42 BOTD uses an internal bot package instead of botl. if you
want to use previous data change botl and botd to bot in /var/lib/botd/store.

contact
=======

"contributed back"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
|
| OTP-CR-117/19 otp.informationdesk@icc-cpi.int http://genocide.rtfd.io
