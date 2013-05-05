Title: Raspberry Pi and my Third Screen
Tags: raspberry, shell, quassel, tmux
Category: Computers

Today, I finally figured out what was wrong with my Raspberry Pi.
It [worked before](http://file3.status.net/i/identica/encukou-20130120T115619-yw8xyls.jpeg),
connected to a TV, without ethernet, and with a power supply and keyboard
borrowed from my brother.
When I got my own accessories for it, though, I found the USB ports and network
were dead.

Well, today I finally got around to some debugging, and found that the faulty
part was the USB cable between the box and the power supply (i.e. a phone
charger). Don't ask me how much I spent diagnosing that.
Luckily, I can easily get micro-USB cable, even on a Saturday.
(Okay, not nearly easily enough, but I did get one.)

Hooray! A working computer! Let's try new things with it!
I've used `apt` in Ubuntu for quite some time, so I thought Raspbian would be too
boring, and decided to go for Arch. So far it's been working nicely.

<!-- PELICAN_END_SUMMARY -->

Quassel
=======

My first reason for having a Pi is a (hopefully) always-on IRC client.
I've been using [Quassel](http://www.quassel-irc.org/) at work, where I leave
a Core running on a virtual machine in the lab, and connect to that with the
graphical client. That way I don't miss anything when my laptop is off.

It turns out Arch's official repos only have the monolithic build of Quassel
(the core and client all in one), but a nice person called joschi maintains a
[Core-only](https://aur.archlinux.org/packages.php?ID=42085) package
in the AUR.
It worked for me with one modification – I had to update the list of
supported arcitectures.
The `pkgbuild`'s error message included the name of my architecture ('armv6h'),
and the `PKGBUILD` file left no doubt where that string should go.
All clear!

The compile took quite some time (I don't know exactly how much because I've
interrupted it a few times to reboot while tinkering), but it paid off.
I'm on IRC again!

Half an hour after I reported my success to the Quassel AUR maintainer,
the arch was added to the package. Thanks, joschi!

My third monitor
================

Now for the other thing I had in mind for the little box.
My laptop's graphics card only supports two screens, and I sometimes get the
feeling that two is too few.

Looks like a job for the Pi! I have a monitor conected to it, now I just need
to wire it up to my computer.
Well, actually, before I do that, I see the default virtual terminal font
is rather large.
A `sudo pacman -S terminus-font` and a `setfont ter-112n` in an rc file
will make many more letters fit on the screen.

Now, the first step to connect the two machines was of course to SSH to the Pi,
so I don't have to plug the keyboard back and forth.
And also to get the middle-clicky pasting goodness of an X terminal emulator.
(Goodness, did I miss that!)

And after that... hm. Let's see what I want to do, exactly.

I need to run commands on the main machine, control them from the main machine,
but have them display on the little box. Sounds easy, right?

Turns out, it's not that easy. At least for me –
I sure hope there's an easier solution than what I came up with.

Since I need to display the console on the Pi, I started up a `tmux` session
there.
I can connect to it from my main box, but I'd like to have a “write-only”
connection: I just want to send the keystrokes over, I don't need to see the
third monitor's contents on the main monitor – it's on the other monitor!
I could make the console window really small, but `tmux` insists on making
the logical terminal just big enough for the smallest client connected to it.
I briefly tried to find a way to use an infinitesimally small font in
a terminal emulator, but to no avail.

Luckily, thanks to research for [my talk for this summer's EuroPython](https://ep2013.europython.eu/conference/talks/terminals-command-lines-and-text-interfaces),
I know that terminal size is just two properties I can set rather easily.
`stty cols 256; stty rows 256;` and voilà, `tmux` thinks it has a window
that's larger than my new monitor.
The only drawback is that whenever the window is resized, it picks up the new
size.
My research notes tell me this is handled by SIGWINCH, a SIGnal that gets
sent whenever the WINdow size CHanges.
Luckily, there's a [signal-blocking program](http://stackoverflow.com/a/4515549/99057)
on StackOverflow, on which I do a quick `s/SIGINT/SIGWINCH/` and compile.
I hack up a command to run SSH with the `stty`s and a signal-blocked `tmux`,
all in a uniquely titled `xterm`, and then use KDE's nifty Window Settings
to make the `xterm` window very tiny, borderless, always-on-top, on all
desktops, and in the upper left corner of the screen.

Glorious.

I think I'll name it `pi-remote`.

(Also, thank goodness for xterm's simplicity: unlike modern programs that
try very very hard to never let users shoot themselves in the foot, xterm can
be resized small enough to be useless.
Well, useless for anything except what I'm trying to do here.)

A circle of SSH
===============

Now that I have a way to control my second monitor, there's one more goal:
running stuff on the main box.
Do do that, I need to SSH back to it. Close the loop, so to say.

I'd like to go passwordless, and I'd rather not leave a private key
that grants access to my main box lying around on the Pi.
I think it's time for some SSH agent forwarding.
It turns out Github has a [nice article](https://help.github.com/articles/using-ssh-agent-forwarding)
on how to set that up – put some lines in `~/.ssh/config`, uncomment one in
`/etc/ssh/sshd_config`, restart sshd – not straightforward but easy enough.

Oh, and I need to trust the key.
I think this is the first time I've put my own key for a machine in that
machine's `authorized_keys`.

The part that I didn't find an elegant solution for is passing the agent
forwarding info through tmux.
This stuff is passed around in environment variables, but the tmux session is
already running, with its own environment.
There's probably an amazingly obvious way to do this, but after a while of
searching I decided for a brute-force approach: before joining the session I
save the SSH-related env:

    :::bash
    env | grep ^SSH  > ~/.ssh/third_monitor_callback_env

and before SSH-ing back, I restore it.

    :::bash
    while read line; do declare -x "$line" done < ~/.ssh/third_monitor_callback_env

Works for me.

It doesn't call back automatically.
The main machine is a laptop, so it may not always be there,
and the pi should be usable without it.


The red freehand arrow
======================

In the end, I have a Raspberry-Pi-controlled third monitor, in retro text mode.
I'll use it mainly for display (logs, stdout of GUI or web things, etc.),
but if I need control, I just click the top-left corner on my mouse-enabled
main screen and type away.
A popular generalization of [Fitts' law](http://en.wikipedia.org/wiki/Fitts%27s_law)
says this is very convenient, and I'm sure not arguing with that.

[![Screenshot of my screen with a red freehand arrow pointing at the pi-remote](|filename|../images/2013-05-04-screenshot.png){.size-full}](|filename|../images/2013-05-04-screenshot.png)

Here's a review of my files, for future reference:

At the main machine, named `tapio`, there's:

* ~/bin/pi-remote:

        :::bash
        xterm -T 'rpi remote!' +sb call-to-pi &

* ~/bin/call-to-pi:

        :::bash
        ssh -t eckpi 'env | grep ^SSH  > ~/.ssh/third_monitor_callback_env; stty cols 256; stty rows 256; ~/bin/nowinch tmux attach-session -t third-monitor'

* ~/.kde/share/config/kwinrulesrc (partial):

        :::text
        [1]
        Description=Window settings for xterm
        above=true
        aboverule=3
        clientmachine=tapio
        clientmachinematch=0
        desktop=-1
        desktoprule=3
        fsplevel[$d]
        fsplevelrule[$d]
        noborder=true
        noborderrule=3
        position=0,0
        positionrule=2
        size=26,20
        sizerule=3
        title=rpi remote!
        titlematch=1
        types=1
        wmclass=xterm
        wmclasscomplete=false
        wmclassmatch=1

And at the Pi side, there's `~/bin/nowinch` modified from the signal blocker
from [StackOverflow](http://stackoverflow.com/a/4515549/99057),
and `~/bin/tapio` to SSH back home:

    :::bash
    while read line; do
        declare -x "$line"
    done < ~/.ssh/third_monitor_callback_env
    ssh tapio

And, of course, an always-on `tmux` session.
I sometimes press Ctrl-D by mistake and don't want to get disconnected,
so I run the shell in a loop:

    :::bash
    tmux new-session -s third-monitor 'while true; bash; reset; done'


I sure hope there is an easier way to do this. Anyone?
