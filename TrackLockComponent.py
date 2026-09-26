from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class TrackLockComponent(ControlSurfaceComponent):

    def __init__(self, session_component, control_track_name="Control", *a, **k):
        super(TrackLockComponent, self).__init__(*a, **k)
        self._session = session_component
        self._control_track_name = control_track_name
        self._dev_lock_active = False
        self._held_indices = []
        self._select_button_elements = []
        self._lock_button_element = None

    def set_select_buttons(self, buttons):
        for index, button in enumerate(self._select_button_elements):
            button.remove_value_listener(self._select_value_listeners[index])
        self._select_button_elements = list(buttons)
        self._select_value_listeners = [partial(self._on_select_value, i) for i in range(len(self._select_button_elements))]
        for button, listener in zip(self._select_button_elements, self._select_value_listeners):
            button.add_value_listener(listener)

    def set_lock_button(self, button):
        if self._lock_button_element is not None:
            self._lock_button_element.remove_value_listener(self._on_lock_value)
        self._lock_button_element = button
        if button is not None:
            button.add_value_listener(self._on_lock_value)

    def _on_select_value(self, index, value):
        if value != 0:
            self._register_held_track(index)
        else:
            self._leave_held_track(index)

    def _on_lock_value(self, value):
        if value != 0:
            self._flip_dev_lock_state()

    def _register_held_track(self, index):
        if self._dev_lock_active is False:
            if index in self._held_indices:
                self._held_indices.remove(index)
            self._held_indices.append(index)

    def _leave_held_track(self, index):
        if self._dev_lock_active is False:
            if index in self._held_indices:
                self._held_indices.remove(index)
            cur_track = self._track_at_index(index)
            if cur_track.is_foldable:
                            cur_track.fold_state = not cur_track.fold_state
            if self._held_indices:
                track = self._track_at_index(self._held_indices[-1])
            else:
                track = self._find_control_track()
            if track is not None:
                self.song().view.selected_track = track

    def _flip_dev_lock_state(self):
        self._dev_lock_active = not self._dev_lock_active
        self._held_indices = []
        if not self._dev_lock_active:
            track = self._find_control_track()
            if track is not None:
                self.song().view.selected_track = track

    def _track_at_index(self, index):
        tracks = self.song().visible_tracks
        track_index = index + self._session.track_offset()
        if track_index < len(tracks):
            return tracks[track_index]
        return None

    def _find_control_track(self):
        for track in self.song().tracks:
            if track.name == self._control_track_name:
                return track
        return None

    def update(self):
        super(TrackLockComponent, self).update()
        if not self._dev_lock_active:
            track = self._find_control_track()
            if track is not None:
                self.song().view.selected_track = track