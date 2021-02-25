#!/usr/bin/env python
#pipod version 3-b
#Thankyou, LORD!!!


"""
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

CHANGELOG:

version 3-b:
    -changed seek method to standard music player mimicry
    -added seek time setting variables
    -caused file loader to ignore formats in the REJECTED_FORMATS setting
    -made tweaks to doc not having to do with above changes

version 2.7.1-b:
    -diverted from pexpect back to native python 2 commands module to lessen dependencies

version 2.7.1:
    -corrected attribute acess coding error in previous_file
    -corrected typo in changelog

version 2.7:
    -added SPEAK setting to optionally read song names
    -tweaks in comments not related to new version
    -code spacing adjustments

version 2.6:
    -made doc corrections and tweaks
    -replaced seek timing system with pygame's builtin timing system

version 2.5.1:
    -moved settings code to beginning of script

version 2.5:
    -changed to python 3 (replacing commands module with pexpect)
    -further documentation tune-ups
    -misc code tweaks

version 2.4:
    -added setting variable that allows shuffle
    -made several tune-ups to doc and comments

version 2.3:
    -added file sorting to correct hiearchy mixup

version 2.2:
    -set PATH variable so as to allow
    different file locations

version 2.1:
    -changed file loading system so
    as to allow hiearchy

version 2.0:
    -changed control system to sense hat
    -use sense hat as display
    -removed switch bounce delay

===ALL PREVIOUS VERSIONS USED GPIO BUTTONS===

version 1.5:
    -fixed bug caused by pausing then seeking

version 1.4:
    -added some simple messages

version 1.3:
    -added delay in control loop to 
    minimize switch bounce
    -added changelog and doc

===SYSTEM ERASURE DESTROYED EARLIER VERSION===

version 1.2:
    -fixed bug in pausing time that made 
    seek inaccurate

version 1.1:
    -file loading changes due to autostart 
    shortcut faliure to switch to working 
    directory

version 1.0:
    -initial working release
"""

#===settings===
PATH="/media/pi/" #Path to music files. Set to /media/pi to search all connected media (ie: flash drive)
SHUFFLE=False #Set to True for music shuffling
SPEAK=False #Read song names when paused (requires espeak)
SEEK_DELAY=0.3 #How long to wait before seeking begins
SEEK_AMOUNT=5 #How far to seek
REJECTED_FORMATS=(".wav", ".mid") #Which audio formats to ignore (added for issues with seekability)

#modules
import pygame
from pygame.locals import *
import time, sense_hat, commands

pygame.init()

#setup display for event recieving
DISPLAY=pygame.display.set_mode((400, 400))
pygame.display.set_caption("Pipod event reciever")

#audio system
mixer=pygame.mixer
mixer.music.set_endevent(USEREVENT) #this event is triggered when the music ends

hat=sense_hat.SenseHat() #the hat

#implement settings (other than PATH)
if SHUFFLE:
    import random

if SPEAK:
    try:
        import espeak.espeak as espeak

        #espeak settings. may be in the SETTINGS section in the future
        espeak.set_parameter(7, 5)
        espeak.set_voice("en-us")
        
    except ImportError as e:
        print("Error: espeak import failed! "+str(e))
        SPEAK=False
        
#finally, the pipod object
class Pipod(object):
    def __init__(self):
        print("This is Pipod")
        
        #basic start values
        self.state="stop"
        self._volume=100
        self.volume=self._volume
        
        #get music files
        self.files=commands.getoutput("find "+PATH+"/").split("\n")

        #if we cannot load a file (it is a non-music file), or it is a rejected format, remove it
        for f in self.files[:]:
            try:
                for rf in REJECTED_FORMATS:
                    if rf in f or rf.upper() in f:
                        raise TypeError
                mixer.music.load(f)
            except:
                self.files.remove(f)

        self.files.sort() #get files in order

        if SHUFFLE:
            random.shuffle(self.files) #if SHUFFLE is set to true, shuffle.

        #start playing!
        self.curfile=-1
        self.next_file()
        
    def next_file(self):
        """load the next file. if we're at the end of the list, start over."""
        self.stop() #stop current music
        print("Next file")
        self.curfile+=1 #next file index

        #loop around
        if self.curfile>len(self.files)-1:
            self.curfile=0

            if SHUFFLE:
                random.shuffle(self.files) #if SHUFFLE is set to true, shuffle.
        
        #load next file and play
        new=self.files[self.curfile]
        mixer.music.load(new)
        self.play()
        
    def previous_file(self):
        """load the previous file. if we're at the beginning of the list, move to the end."""
        self.stop() #stop current music
        print("previous file")
        self.curfile-=1 #previous file index

        #loop around
        if self.curfile<0:
            self.curfile=len(self.files)-1

            if SHUFFLE:
                random.shuffle(self.files) #if SHUFFLE is set to true, shuffle.

        #load previous file and play
        new=self.files[self.curfile]
        mixer.music.load(new)
        self.play()
        
    def play(self):
        """play music"""
        print("Play")
        #if we are paused, unpause
        if self.state=="pause":
            mixer.music.unpause()
        else: #otherwise (we are stopped), start at the beginning
            mixer.music.play(0, 0)
            self.before_seek_time=0 #this is needed because seeking resets pygame's timer

        #current state is now playing
        self.state="play"

        if SPEAK:
            espeak.cancel() #stop any current speaking
        
    def pause(self):
        """pause music"""
        print("Pause")
        self.state="pause" #current state is now paused
        mixer.music.pause() #pause audio

        if SPEAK:
            espeak.synth(self.files[self.curfile].split("/")[-1].split(".")[0])
            
    def stop(self):
        """stop music"""
        print("Stop")
        mixer.music.stop() #stop audio
        self.state="stop" #current state is now stopped
        
    def seek_forward(self):
        """seek forward"""
        print("Seek forward")

        #if we are not playing, play
        if self.state!="play":
            self.play()
            
        play_time=mixer.music.get_pos()/1000.0
        play_time+=self.before_seek_time
        self.before_seek_time=play_time*1+SEEK_AMOUNT
        
        mixer.music.play(0, play_time+SEEK_AMOUNT) #play music at new position
        
    def seek_back(self):
        """seek back"""
        print("Seek back")

        #if we are not playing, play
        if self.state!="play":
            self.play()
            
        play_time=mixer.music.get_pos()/1000.0
        play_time+=self.before_seek_time
        self.before_seek_time=play_time-SEEK_AMOUNT
        if self.before_seek_time<0:
            self.stop()
            self.play()
        else:
            mixer.music.play(0, play_time-SEEK_AMOUNT) #play music at new position
    
    #===old seek/skip functions===
    #def forward(self):
        #"""the forward button"""
        ##if we are paused, skip
        #if self.state=="play":
            #self.seek_forward()
        ##otherwise, seek
        #else:
            #self.next_file()
            
    #def back(self):
        #"""the back button"""
        ##if we are paused, skip
        #if self.state=="play":
            #self.seek_back()
        ##otherwise, seek
        #else:
            #self.previous_file()
    #============================
    
    def vol_up(self):
        """turn volume up"""
        self.volume+=5
        
    def vol_down(self):
        """turn volume down"""
        self.volume-=5
        
    @property
    def volume(self):
        """get our volume"""
        return self._volume
    
    @volume.setter
    def volume(self, new):
        """set our volume"""
        self._volume=new

        #limit to 5-100
        if self._volume>100:
            self._volume=100
        if self._volume<5:
            self._volume=5
        
        mixer.music.set_volume(self._volume/100.0) #actual volume changing

#kick off!
pp=Pipod()

#status variables for seeking

#are the left or right keys down, and if so when were they pressed (when not false, these are time values)
leftkey=False
rightkey=False

#have we started seeking (to avoid skipping after seeking finishes)
seeking_back=False
seeking_forward=False

while True:
    for e in pygame.event.get():
        #if we are at the end of a file, skip
        if e.type==mixer.music.get_endevent():
            pp.next_file()
        
        #key events
        elif e.type==KEYDOWN:
            #if left is pressed, prepare to seek or skip back
            if e.key==K_LEFT:
                hat.show_letter("(")
                leftkey=time.time()

            #if right is pressed, prepare to seek or skip forward
            elif e.key==K_RIGHT:
                hat.show_letter(")")
                rightkey=time.time()
                
            #if up is pressed, turn up volume
            elif e.key==K_UP:
                hat.show_letter("+")
                pp.vol_up()
                time.sleep(0.05)
                hat.clear()

            #if down is pressed, turn down volume
            elif e.key==K_DOWN:
                hat.show_letter("-")
                pp.vol_down()
                time.sleep(0.05)
                hat.clear()

            #if center is pressed, pause or play
            elif e.key==K_RETURN:
                if pp.state=="play":
                    hat.show_letter("#")
                    pp.pause()
                else:
                    hat.show_letter(">")
                    pp.play()
                time.sleep(0.05)
                hat.clear()

        elif e.type==KEYUP:
            #if left is released, end seeking back or skip back
            if e.key==K_LEFT:
                hat.clear()
                if not seeking_back:
                    pp.previous_file()
                else:
                    seeking_back=False
                leftkey=False

            #if right is released, end seeking forward or skip forward
            elif e.key==K_RIGHT:
                print("right key up")
                hat.clear()
                if not seeking_forward:
                    pp.next_file()
                else:
                    seeking_forward=False
                rightkey=False
        
    #seeking
    
    #if left key is being held down, start seeking back and reset the timer
    if leftkey:
        curtime=time.time()
        if curtime-leftkey>SEEK_DELAY:
            leftkey=curtime*1
            if not seeking_back:
                seeking_back=True
            pp.seek_back()
    
    #if right key is being held down, start seeking forward and reset the timer
    if rightkey:
        curtime=time.time()
        if curtime-rightkey>SEEK_DELAY:
            rightkey=curtime*1
            if not seeking_forward:
                seeking_forward=True
            pp.seek_forward()
