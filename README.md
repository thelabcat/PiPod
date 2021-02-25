This is Pipod version 3-b, a python program which turns a 
raspberry pi with an AstroPi sense hat into a music player.

This software is mostly a mental recollection duplicate of the 
original pipod software due to the original's destruction in 
an accidental system erasing. Version number includes destroyed 
version.

MANUAL:

Introduction:

Pipod is designed to work with the AstroPi sense hat
so the software can be run without a mouse or keyboard. 
A different control system is possible provided a loop is 
made which moves to the next file based on the USEREVENT in 
pygame.event by calling next_file(). Note that the current 
loop also handles the difference between seeking and changing 
files. Separately, also note that some formats cannot be seeked by the 
current version of the pygame mixer and are thus ignored based on the 
REJECTED_FORMATS setting. The two known current ones are WAV and MIDI.

Setup:

Change the absolute variables under "settings" to match preferences (be 
careful with the REJECTED_FORMATS setting: removing formats from it 
that cannot be seeked by the pygame mixer will cause Pipod to crash if 
a seek is attempted on them. However, adding formats which can be 
seeked will not cause a crash; they will just be ignored). Place all 
desired music in the folder specified by the PATH variable. The nature 
of music loading allows file-folder hiearchy and plays files in order: 
For two folders A and B, Pipod will play all files in A before files in 
B. Create a desktop configuration file which loads the script in python 
(This is Pipod B, which is configured to function with only native 
modules, but thus only works with python 2 currently). The desktop file 
can then be placed in /home/pi/.config/autostart to load Pipod at boot. 
Connect the sense hat before boot.

Operation:

Pipod will start playing automatically on run. The sense
hat joystick serves as the controller with the same
orientation as the Apple iPod; up and down for volume, left 
and right for changing files, left and right hold for seeking, 
and center for pause/play.

If Pipod is seeked back to the beginning of a song, it will not 
move to the one before it. It will, however, move to the 
next song if it is seeked to the end of the current one.
Pipod treats the list of files like a ring. When it reaches 
the end, it will loop around to the first one. Pipod has no 
in-operation shuffle function (There is a variable SHUFFLE
which, if set to True, will shuffle the music).

If the setting SPEAK is enabled and espeak is installed, Pipod
will read the name of the current song when paused. Altering espeak
settings is not recommended unless you know what you are doing. You
may find information from help("espeak.espeak") to be useful. The
espeak settings are just before the Pipod object.

Troubleshooting:

-Pipod depends on the system "find" command plus the modules pygame,
random, time, commands, and (only if SPEAK is enabled) the
python espeak API (all but espeak are native on Raspbian).

-If you have other programs with GUI's which load at boot, they
may interfere with Pipod's joystick event reciever window.

-The SPEAK setting will only work if the python espeak
API is installed.

-older versions of pygame, and even modern versions with certain music
types, may not be able to seek. This is known to be the case with
pygame 1.9.1 playing MIDI or WAV files, so these files (really, any files 
in the REJECTED_FORMATS setting) will be ignored.
