from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.Control import control_list, ButtonControl
from _Framework.SubjectSlot import subject_slot

class GroupFoldComponent(ControlSurfaceComponent):
    """
    Custom component that allows to fold/unfold
    grouped tracks by holding shift and pressing
    track's clip stop button.
    """

    fold_buttons = control_list(ButtonControl, control_count=8, color='DefaultButton.Off')

    def __init__(self, session_component, *a, **k):
        (super(GroupFoldComponent, self).__init__)(*a, **k)
        self._session = session_component
        
        self._on_visible_tracks_changed.subject = self.song()
        self._on_session_offset_changed.subject = self._session
        
        self._on_visible_tracks_changed()

    @fold_buttons.pressed
    def fold_buttons(self, button):
        """ 
        Triggered when any of the 8 button
        combinations is met
        """
        track_index = button.index + self._session.track_offset()
        tracks = self.song().visible_tracks

        if track_index < len(tracks):
            target_track = tracks[track_index] 
            if target_track.is_foldable:
                # Toggle the fold state
                target_track.fold_state = not target_track.fold_state
        
        self.update_leds()

    @subject_slot('visible_tracks')
    def _on_visible_tracks_changed(self):
        """ 
        Triggered when tracks are created, deleted, moved, 
        OR when a group track is folded/unfolded in the GUI 
        (because child tracks appear/disappear).
        """
        self.update_leds()

    @subject_slot('offset')
    def _on_session_offset_changed(self):
        """ Triggered when track bank navigates left/right """
        self.update_leds()

    def update(self):
        """ Inherited framework method triggered on state changes """
        super(GroupFoldComponent, self).update()
        self.update_leds()

    def update_leds(self):
        """
        Core Logic: 
        Iterates through the 8 hardware buttons and assigns the 
        correct Skin String based on the Ableton track state.
        """
        if not self.is_enabled():
            return
        
        tracks = self.song().visible_tracks
        track_offset = self._session.track_offset()

        for button in self.fold_buttons:
            track_index = button.index + track_offset
            
            if track_index < len(tracks):
                track = tracks[track_index]
                
                if track.is_foldable and not track.fold_state:
                    button.color = 'DefaultButton.On' 
                else:
                    button.color = 'DefaultButton.Off' 
            else:
                # If we are looking at an empty track slot
                button.color = 'DefaultButton.Off'