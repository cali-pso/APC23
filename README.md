# APC23

## Presentation

This is my custom remote script for a personalized integration of Akai's APC40 MkII with Ableton Live 12.2.4.
It is a copy of the original remote script with added components that fix workflow issues I was encountering on live sets.
It is meant to change overtime, as my needs for said live sets evolve. This is an unofficial product, I am not affiliated
with neither Akai nor Ableton.

## Usage

Just drag and drop the APC23 folder into your User Library -> Remote Scripts. Create that folder if needed.
Then select the APC23 entry in the dropdown menu in Preferences -> Tempo & MIDI -> MIDI -> Control Surfaces
and choose the appropriate MIDI input/output. That's it, enjoy !

## Key changes

- __TrueCue__: The "CueLevel" encoder now maps to the selected track's last send instead of master track's cue level.
- __GroupFold__: The per-track clip stop buttons have been reassigned to group expanding/collapsing : if track is
foldable - meaning it is a group -, pressing it's clip stop button will expand it and show the tracks it contains.
Expanded tracks are shown by a blinking clip stop button. Pressing the button again will collapse the group, turning
the button back off.
- __TrackLock__: When device lock is disabled, selected track will always default to track named "Control" or, in it's absence, track index 0. Holding another track's select button allows to edit it's parameters until release. Enabling device lock resumes normal behavior.

### Fancy your own features ?

Feel free to contact me if you feel a custom script could solve some of your long lasting issues that are not answered to
by the list above.
