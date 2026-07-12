from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot

class TrueCueComponent(ControlSurfaceComponent):
    """
    Custom component that remaps the 'cue level' potentiometer
    to control the last send's value for the selected track.
    """

    def __init__(self, *a, **k):
        (super(TrueCueComponent, self).__init__)(*a, **k)
        self._cue_encoder = None
        self._on_selected_track_changed.subject = self.song().view
        self._on_selected_track_changed()

    def set_cue_encoder(self, encoder):
        self._cue_encoder = encoder
        self._update_encoder_connection()

    @subject_slot('selected_track')
    def _on_selected_track_changed(self):
        """ Triggered on selection of a new track """
        track = self.song().view.selected_track
        self._on_sends_changed.subject = track.mixer_device
        self._update_encoder_connection()

    @subject_slot('sends')
    def _on_sends_changed(self):
        """ Triggered on change of state from sends part """
        self._update_encoder_connection()

    def _update_encoder_connection(self):
        """ Core logic maps encoder to selected track's last send """
        if self._cue_encoder is not None:
            self._cue_encoder.release_parameter()
            if self.is_enabled():
                track = self.song().view.selected_track
                if track != self.song().master_track:
                    sends = track.mixer_device.sends
                    if len(sends) > 0:
                        last_send = sends[-1]
                        self._cue_encoder.connect_to(last_send)

    def update(self):
        """ Inherited method called when the component is enabled/disabled. """
        super(TrueCueComponent, self).update()
        self._update_encoder_connection()