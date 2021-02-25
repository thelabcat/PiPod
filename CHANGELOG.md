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
