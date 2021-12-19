vgm2mid Version 0.5 by Paul Jensen
-----------------------------------

NOTE: WORD WRAP must be enabled in order to properly view this file


Contents
--------

1) What is vgm2mid?
2) Changes in this version
3) Features
4) Planned Features
5) Known Bugs
6) Revision History
7) FAQs
8) Special Thanks
9) Where to Send Comments, Questions, Bug Reports, etc.


What is vgm2mid?
----------------

vgm2mid converts .VGM files into standard .MID files.  The purpose of the program is to aid those who want to create MIDI music files based on the soundtracks of video games.


Changes in this version
-----------------------

(Version 0.5)
Added YM2413 instrument selection
Improved file reading code.  Files are now read instantly.
Lots of internal changes

Features
--------

Support for most features of the PSG
Support for most features of the Yamaha YM2413
Support for most features of the Yamaha YM2612
Supports regular and compressed .VGM files, and .GYM files
Batch File Conversion


Planned Features
----------------

Support for all sound chips in the .VGM spec
(Done!) Support for compressed .VGM files (.VGZ)
Built-in .GYM->.VGM converter
(Done!) Pitch Bending
(Done! And more to come...) More options than 'Start' ;)	
	

Known Bugs
----------

Let me know if you find any.
pj@emulationzone.org?subject=vgm2mid_bug_report


Revision History
----------------
(Version 0.41 bugfix release)
(Hopefully) fixed bug where vgm2mid failed to unload completely upon exit
Fixed stupid bug that broke YM2413 support
For MIDI authors: Changed note routine, correct notes, both positive and negative pitch wheel events now.

(Version 0.4)
Interface:
New and (IMO) improved user interface
Added support for batch conversion
Inproved conversion progress status
Added options screen

All Soundchips:
Added disabling of chip features on a per channel basis via the options screen
Fixed some bugs

Misc.:
Fixed 'subscript out of range' bug with some .VGZ files
Drastic reduction of .VGZ decompression speed

(Version 0.35)
All Soundchips:
Implemented 'real' MD/Gen and SMS timing
New FNum -> Hz code
New Hz -> MIDI note code (Thanks, Maxim)
All supported soundchips are now in 'perfect' tune

YM2612:
Implemented volume changes, which never worked in gym2mid, but do now.
(Note:  Test this with a log of Streets of Rage)
DAC support (digital audio channel or digital to analog converter)
(Note:  The DAC is supported by detecting a PAN change (speaker selection) for the DAC, and creating a Bass Drum event at that time.  Consequently, this does not work with all games, as they do not all use DAC stereo, and some games 'overuse' the DAC-- you'll know it when you hear it-- so I also added an option to disable the DAC.)

(Version 0.3)
Added YM2413 support (Master System FM)
Fixed .VGZ support (hopefully)

(Version 0.25)
Support for compressed .VGM files (.VGZ)

(Version 0.2)
.GYM support
Accurate pitch bending for (hopefully) all soundcards
'Perfect' note accuracy

(Version 0.11 - Not Publicly Released)
Reverted to old note algorithm
PSG Volume 0 no longer turns off the current MIDI note
Program no longer crashes when selected .MID file is already 	open.

(Version 0.1)
First release


FAQs
----

Q: How do I create a .VGM file?
A: So far only the emulators Meka and Dega support .VGM logging.  Please check out their respective readme's for information, or try http://www.smspower/org/music .

Q: How do I create a .GYM file?
A: AFAIK, current versions of the following emulators support .GYM logging:
Genecyst (x.xx)
Gens
DGen
Megasis

As stated above, please check out their respective readme's for information.


Special Thanks
--------------

(In no particular order)
To 'Bo', or whatever your real name is, for composing the music for Phantasy Star, Space Harrier, Castle of Illusion, and other fantastic games.

To Yuzo Koshiro, for composing the music for Revenge of Shinobi, Streets of Rage, etc.  You stimulated my interest in music.
(BTW, Yuzo Koshiro makes regular posts in the forum on his company's website.  Check it out at www.ancient.co.jp.  Click on the 'English' button.)

To Zoop/Bock/Omar, for creating Meka.

To Dave, for creating DTMNT, DGen, Final Burn, and Dega, and for helping create the .VGM file format.
(Dave, don't let people give you crap)

To Maxim, for creating a great Winamp plugin, and for lots of advice.

To unfnknblvbl, for advice.

To Sardu, for creating Genecyst, and helping to get the music log rolling.  (joke. funny?)

To EmulationZone, for hosting gym2mid, vgm2mid, and the PSODVj2eRt


Contact Info
------------

Please *DO* feel free to send any questions, comments, or bug reports to me,
Paul Jensen
( pj@emulationzone.org ).

Please *DO* visit the vgm2mid homepage periodically to learn about updates, and new utilities. 			
( http://www.emulationzone.org/projects/gym2mid/index.htm )

Please *DO* read the documentation.  It should answer most of your questions.

Please *DO* check out the Music section of SMS Power.
( http://www.smspower.org/music )

Please *DO NOT* send me any ROM requests.