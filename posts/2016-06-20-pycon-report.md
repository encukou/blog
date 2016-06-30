Title: PyCon 2016 Report
Tags: conference, pycon


I attended PyCon 2016, the annual Python language conference, which took part
between May 28th to June 5th.

Here's a long, rambling and somewhat personal report of what I got from
the conference.

<!-- PELICAN_END_SUMMARY -->

I found accommodation through Airbnb, and ended up staying with Jov,
a laid-back drummer.  He apparently prepared a lot of info about local
breweries to share with his guest, but as I don't drink, we had to find
other topics to talk about.  Which we did!
I'm never going to stay at a conference hotel again if I can help
it. (Except at PyCon PL, of course.)


## Language Summit

Saturday and Sunday before the main conference were "tutorial days", with
opportinities to learn various technologies, either paid by the attendees
or sponsored.  Unfortunately, I registered late enough that the interesting
free ones were already full.  However, on Saturday another event was held:
the [Language Summit], to which Nick Coghlan kindly invided me.

The Summit is a gathering of Python core developers and people invited by them
at which language issues are discussed.  Though there are no recordings,
the Summit was covered by Jake Edge in [LWN].
My talk aimed to relate the perspective of Fedora (and redistributors in
general) to Python developers.
Specifically, I talked about:

  * Python 3 porting: Many people in the Python ecosystem use the [PyPI]
    as the canonical list of Python software, so tools tracking Python 3
    porting progress (e.g. [WoS]) are usually biased against system tools
    (e.g. DNF, Samba, Openstack) and applications (e.g. pitivi, Inkscape).
    Fedora's [PortingDB] arguably gives a better subset of "popular open-
    source packages".  I gave an introduction to PortingDB, how we use it
    and how to look at the data.  I also mentioned that we're nearing having
    50% of packages ported, hopefully as soon as Fedora 25.
    I talked about major software that is not ported yet. Anything based on
    GTK2 will need to be ported to GTK 3 to get Python 3 support; wxWidgets
    support for py3 is still incomplete. The other blockers are Ansible,
    enterprise-y software (Samba, FreeIPA), VCSs (Mercurial, Bazaar),
    and large parts of the Fedora infrastructure.  Unsurprisingly,
    all are projects that are not published on PyPI.
    I also linked porting guides: [py3c] for extension modules, the [RPM
    porting Guide][RPG] for RPMs, and the upcoming Conservative Porting
    Guide.
  * pyp2rpm & COPR PyPI rebuilds: I talked briefly how we're trying to
    rebuild all PyPI packages in COPR, which would help with packaging
    Python 3 compatible versions of software.  Tying in to a previous talk,
    I mentioned that since running tests is part of building a RPM,
    these automatic COPR builds could provide integration tests for
    Python packages – something both Fedora and the Python ecosystem
    need.
  * System Python: I presented the need for a lighter standard library
    that could be used for minimal systems.  More than three-fourths of
    Python's stdlib are not needed at runtime by most applications, and
    parts like the test suite and TK are already split out of python-libs
    in Fedora.  The idea was met with understanding, though (rather
    surprisingly for me) Kushal Das from Fedora Cloud objected to
    splitting the stdlib, preferring a full Python even in the base cloud
    image.
    I noted that splitting the standard library, and letting packages
    opt-in to defining exactly which parts they need, might be useful for
    projects like MicroPython, or making Python work on Android.  I learned
    that this might be good for Windows as well.  However, I said that
    neither I nor Red Hat's python-maint has resources to commit to a
    general solution yet.

Overall, the audience was responsive and asked good questions. We ran a bit
over the 20 minutes I had allocated, but at that point running over was
a common theme at Language Summit.

Other Language Summit talks focused on security, porting to Python 3,
removing the GIL, core dev workflows, automated testing, gradual typing,
and JITs.  Read the LWN reports if you're interested.


I went to see the city on Sunday, and returned on Monday for the first
day of conference talks.


# Monday

Meals at PyCon took place in the Expo hall, among sponsor booths.  Most
sponsors were either developing Python apps, or providing services to
deploy them, debug them, or otherwise make Python developers' lives easier.

I was happy to see a section of the Expo Hall dedicated to open-source
projects: Cookiecutter, BeeWare, Django Girls and PyLadies, Read the Docs,
Plone, Pyramid, and the Recurse Center.  Of course, the were also open-source
projects in the "paid" section: I counted Ansible, Sentry, OpenShift,
Elastic, and Docker.

Below are my notes from talks, open spaces, and discussions I attended.

**Ned Batchelder: Machete Mode Debugging.**
  This talk didn't have much new material for me, but it illustrates what
  for me is a large part of Python's appeal: it's possible to do very
  effective (but nasty) hacks to solve a problem quickly, once one knows
  the language internals.  A necessary part of what makes this appealing
  is then the resistance to these hacks ever leaving a development machine.
  This resistance is largely cultural: Python could be a very different
  language even if the syntax stayed the same.

**Brett Cannon, Dino Viehland: Pyjion.**
  This was a rehash of the Language Summit talk, with some points
  elaborated further.  Adding JIT hooks to core Python is a great idea
  that could make speeding up the reference interpreter – or creaing
  debugging tool – easy and thus allowing healthy competition between
  various approaches.  (It would also allow proprietary speed-up addons;
  but hopefully Microsoft has learned the idea that collaboration
  works better.)

**Drew Fisher: Object-Capabilities, Cap'n Proto.**
  Object capabilities are a great framework for building secure systems.
  Sadly, not the default in today's frameworks.
  I didn't see any functional programming talks at PyCon; I assume this
  is because they all tend to be similar and everybody knows the material
  by now.  I can't wait until object capabilities reac a similar "exotic
  but well-known" status.

**Open Space: Meetup Organizers.**
  As the Pyvo meetups in Brno are struggling with too many attendees,
  we're planning to add parallel beginner-focused events to split the
  audience.  It turns out many meetups across the world are doing the same,
  and hopefully I'll be able to use my notes in Brno soon.
  (This Open Space continued with another session on Wednesday.)

**Open Space: Python and Rust.**
  When it comes to Rust, I'm interested in the concept of a Mozilla-supported
  compiled language, and despite never trying it for a serious project,
  whenever I read about the technical choices that go in the languahe,
  I have nothing but respect for its developers.
  Since I don't know much about Rust I planned to join the Rust open space
  as a silent lurker, but I was able to provide some details about CPython
  internals that might make it easier to build Python-Rust bridges.

**Open Space: IoT, MicroPython, automation.**
  This open space had an interesting topic and great people (Nicholas
  Tollervey and Paulus Schoutsen were both there), but there was a lack
  of good talking points, so I didn't get much more out of it than an
  urge to try giving a MicroPython-themed lightning talk.
  And I did get to hold a BBC Micro:Bit :)

**Lightning Talks.**
  The best part of the conference – a mixt of mini-talks ranging from
  funny to practical to dead serious.  Professionally, the most important
  was probably about "star_destroyer" – a tool that removes "import *"
  statements in a smart way.

After the talks, Sentry and Linode sponsored an evening at the local arcade,
even providing quarters to feed the Marios and Pacmans.  Even nerdier than
PyCon itself.


# Tuesday

**Guido van Rossum: Keynote**
  Guido is a great language designer and community leader, but
  I'm not much of a fan of his keynotes :(

**Parisa Tabriz: Keynote**
  A talk about security.  To me the most important point was that while
  software engineers spend time thinking about making things work, security
  engineers think about making things break.  It's a mindset everyone
  should slip into at times.

**Daniele Procida: Documentation-driven development.**
  Django is a perfect example of how great documentation, great community,
  and great product go together.  Daniele talked about the importance of
  the process of documenting, rather than having documentation, and
  he process of informing, rather than publishing information.  And he
  explained a few guidelines for great documentation.

**Anthony Scopatz: xonsh.**
  xonsh is a shell that is, syntax-wise, a hybrid between (Ba)sh and Python.
  Based on the presentation, it looks like the merge was (surprisingly for
  me) done relatively cleanly and respectfully.  I need to try it out
  soon.

**Glyph: Shipping Software To Users With Python.**
  An overview of practices for shipping Python software: the good and the
  bad, the existing ones, the near future, and the ideal state.
  I've heard more than one person say this was the most informative talk
  at Pycon.  I seem to be more interested in teaching programming and
  building tools for programmers than in real-world apps, but this was still
  a great overview.

**Paul Kehrer: Reliably Distributing Compiled Modules.**
  Packaging is perhaps the area of Python ecosystem that is changing most
  rapidly, so good talks on these topics are always welcome – especially
  if it broadens awareness of manylinux wheels.

**Amber Brown: The Report Of Twisted’s Death.**
  Unfortunately, I didn't get much out of this talk, but other people's
  reactions were positive, so it's probably just me.
  Amber's talk at the Language Summit was much better.

**Katie Bell: The computer science of marking computer science assignments.**
  This talk ended up mainly focusing on computational geometry, which
  is a fun subject.  Although it had "computer science" in the title,
  it was a little underresearched – but as Katie learned some better
  techniques from the audience, everyone kept smiling.

**Russell Keith-Magee: A tale of two cellphones: Python on Android and iOS.**
  I consider this the most important talk of this PyCon.  Russel's BeeWare
  project is not the first to bring Python to mobile phones (and I have
  big respect for Kivy), but it aims to make Python a first-class language
  for native apps. Also, it seems designed from the ground up for long-term
  maintainability, both technical and social.
  I had to leave in the middle of the talk to prepare my lightning talk,
  but I made sure to watch the recording before the sprints later.

**Lightning Talks.**
  My lightning talk was on the fun side of the spectrum: how to make
  a cheap glowing, Wi-Fi controlled balloon.
  A notable talk in this block by Nathaniel Smith introduced `async yield`.
  I asked Nathaniel afterwards if he's planning to add this feature (which
  I think is conspicuously missing from Python) to the language, and he said
  it's actually the prototype just for that. Yipee!
  Oh, and Larry Hastings gave a very entertaining talk, not about Python
  but about speed gaming.  I heard about #dsdad before, but I had no idea
  he's a Python release manager!

The day ended with a PyLadies charity auction, which was quite fun but
the wrong kind of fun for me, I guess.


# Wednesday

Wednesday started with keynotes (about the Python Software Foundation,
and about Plone), the first of which I missed for the Meetups open space.
As for Plone, I definitely suggest the talk to anyone interested in
designing sustainable projects – the history of such a large and long-lived
project is fascinating.

After the keynotes, there was the poster session. Some notes from there:

  * hdbscan – a library I just saw mentioned at Pyvo Ostrava was here
    with its authors.
  * An interesting system for data visualization was presented, but
    unfortunately it'll only be open-sourced after publication of the
    paper.
  * PyMoms – meetups with provided childcare. I need to suggest this to
    the local PyLadies.

And then talks resumed:

**Anne DeCusatis: More Than Binary: Inclusive Gender Collection and You.**
  I went to this talk more for the discussion at the end than for the
  talk itself.  In English, the only part of the language that's different
  between genders is pronouns (he/she), and there are efforts to be more
  welcoming to people who are neither or both male and/or female.
  However, the Czech language only supports the case of an animate object
  being either male or female.  I would imagine this makes it practically
  mandatory for non-binary people to choose one of the two, leading
  to public perception that non-binary people just don't exist.  But, the
  fact that they do exist is just about the only thing in this area that
  I can be sure about.  And, as we all know, diversity is important – both
  diversity of programmers, to get various points of view, and diversity
  of users, so that we don't make some people's lives harder by just not
  thinking about them in our designs.
  The speaker sadly couldn't provide any pointers for exploring this space
  further, but I got some from people standing by.

**Laura Rupprecht: What can software engineers learn from the medical field?**
  I came late, as discussion from the previous talk took more than the break.
  Beyond the concept of "triage", which comes from medical field, there
  are are other concepts we can learn from doctors.  The one I liked was
  the fact that teaching hospitals have better outcomes.  The software
  world reflect this in code reviews, pair programming, and internships.
  I believe software development internships – or even apprenticeships –
  should be *much* more common than they are now, and they should serve both
  to train new contributors/employees, and to ensure simplicity – and thus
  maintainability – of the resulting code.

**Jacob Kovac: Revitalizing Python Game Development.**
  This was a talk about Kivy, which does "Packaging", "Performance", and
  "Platforms" right for Python-based games.
  I like Kivy – I made software for my Master's thesis in it – but it
  always felt as a monolith that's a bit removed from the Python ecosysyem.
  Still, just like Django is currently the king of web frameworks, I would
  not object to Kivy becoming the king for Python game development.
  I believe the project needs much better community management, though.

**K Lars Lohn: Keynote.**
  This was a masterpiece of a keynote. It brought tears to my eyes.


In the evening, I got together with Christian Heimes, Paul Hildebrandt,
Katie Bell, and a couple other people for dinner at the McMenamins School,
a elementary school turned into a hotel and restaurant.


# Sprints (Thursday, Friday, Sunday)

I sprinted on CPython, and got Nick Coghlan and Eric Snow review and refine
my [upcoming PEP].  It felt like several weeks of work getting done in two
days.
Late Friday, after I sendt the pre-PEP to review, Ubuntu's Matthias Klose
told me about a file naming problem in Python 3 versions of Samba's supporting
packages.  We discussed until we identified the problem and found a possible
solution (which still needs to be implemented).
After that I went to the BeeWare table and picked a task: getting the float
test suite to pass in VOC, the Python-to-Java compiler used for Android
support.  I found out this required writing `float.__repr__()`, since the
tests do textual comparisons, so I didn't finish by a long shot.
I took Saturday off, and returned on Sunday to finish a `__repr__`
implementation that usually does the same thing as CPython's (and never gives
an unreasonable result – it will just sometimes show an extra digit).
The atmosphere at the BeeWare table (and, for example, at the Cookiecutter
table beside it) was extremely pleasant and welcoming, something I need to
learn to emulate when I'll run sprints.

During Sunday, lots of people left to catch their planes, including Russel
the BeeWare sprint leader, so my pull request was merged only some time
next week.
After the sprints, I got some Fedora swag from Remy to bring back to Brno,
and joined fellow BeeWare sprinters – Jeremy, Marina and Holly – for dinner
and board games.

And that was it!  I spent a few days after the conference enjoying the city
of Portland, then hopped on a train to Seattle and back home.


[Language Summit]: https://us.pycon.org/2016/events/langsummit/
[LWN]: https://lwn.net/Articles/688969/
[PyPI]: https://pypi.python.org/pypi
[WoS]: https://python3wos.appspot.com/
[PortingDB]: http://fedora.portingdb.xyz/
[py3c]: https://py3c.readthedocs.io/en/latest/guide.html
[RPG]: http://python-rpm-porting.readthedocs.io/en/latest/
[upcoming PEP]: https://github.com/encukou/peps/blob/module-state-access/pep-9999.txt
