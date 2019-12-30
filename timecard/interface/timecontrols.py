"""Time Controls [Timecard]
Author(s): Jason C. McDonald

Controls the timer and saves the time entries to the log.
"""

from PySide2.QtWidgets import QPushButton, QHBoxLayout, QWidget
from PySide2.QtGui import QIcon

from timecard.interface.notes import Notes
from timecard.interface.timedisplay import TimeDisplay
from timecard.data.timelog import TimeLog
from timecard.interface.logview import LogView


class TimeControls:
    widget = QWidget()
    layout = QHBoxLayout()
    btn_startpause = QPushButton()
    btn_stopsave = QPushButton()

    start_callback = None
    resume_callback = None
    pause_callback = None
    stop_callback = None
    save_callback = None
    reset_callback = None

    @classmethod
    def build(cls):
        """Construct the interface."""
        cls.widget.setLayout(cls.layout)
        cls.layout.addWidget(cls.btn_startpause)
        cls.layout.addWidget(cls.btn_stopsave)

        cls._set_mode_stopped()

        return cls.widget

    @classmethod
    def connect(cls, start=None, resume=None, pause=None,
                stop=None, save=None, reset=None):
        """Connect callbacks to the time control events.
        Any callbacks not specified will not be overridden.
        (See disconnect() for removing callbacks.)

        Keyword arguments:
        start -- called when a new timer is started
        resume -- called when a timer is un-paused
        pause -- called when a timer is paused or tentatively-stopped
        stop -- called when a timer is stopped
        save -- called when a stopped timer is saved to log
        reset -- called when a stopped timer is cleared
        """
        if start:
            cls.start_callback = start

        if resume:
            cls.resume_callback = resume

        if pause:
            cls.pause_callback = pause

        if stop:
            cls.stop_callback = stop

        if save:
            cls.save_callback = save

        if reset:
            cls.reset_callback = reset

    @classmethod
    def disconnect(cls, start=False, resume=False, pause=False,
                   stop=False, save=False, reset=False):
        """Disconnect functions from the time control events.
        Pass True to any of the keyword arguments to clear the associated
        callback.

        Keyword arguments:
        start -- called when a new timer is started
        resume -- called when a timer is un-paused
        pause -- called when a timer is paused or tentatively-stopped
        stop -- called when a timer is stopped
        save -- called when a stopped timer is saved to log
        reset -- called when a stopped timer is cleared
        """
        if start:
            cls.start_callback = None

        if resume:
            cls.resume_callback = None

        if pause:
            cls.pause_callback = None

        if stop:
            cls.stop_callback = None

        if save:
            cls.save_callback = None

        if reset:
            cls.reset_callback = None

    @classmethod
    def _disconnect_buttons(cls):
        """Disconnect signals from the control buttons.
        This must be done before new signals can be added properly.
        """
        try:
            cls.btn_startpause.clicked.disconnect()
        except RuntimeError:
            pass

        try:
            cls.btn_stopsave.clicked.disconnect()
        except RuntimeError:
            pass

    @classmethod
    def _set_mode_stopped(cls):
        """Set buttons to stopped-clock state."""
        cls._disconnect_buttons()

        cls.btn_startpause.setText("Start")
        cls.btn_startpause.setIcon(QIcon.fromTheme('media-playback-start'))
        cls.btn_startpause.setWhatsThis("Start a new timer.")
        cls.btn_startpause.clicked.connect(cls.start)

        cls.btn_stopsave.setIcon(QIcon.fromTheme(None))
        cls.btn_stopsave.setText("Stopped")
        cls.btn_stopsave.setWhatsThis("Timer is already stopped.")
        cls.btn_stopsave.setEnabled(False)

    @classmethod
    def _set_mode_save(cls):
        """Set buttons to save-or-reset state."""

        cls._disconnect_buttons()

        cls.btn_startpause.setText("Reset")
        cls.btn_startpause.setIcon(QIcon.fromTheme('edit-undo'))
        cls.btn_startpause.setWhatsThis("Discard time and reset timer.")
        cls.btn_startpause.clicked.connect(cls.prompt_reset)

        cls.btn_stopsave.setIcon(QIcon.fromTheme('document-save'))
        cls.btn_stopsave.setWhatsThis("Save time and notes to log.")
        cls.btn_stopsave.setText("Save")
        cls.btn_stopsave.setEnabled(True)
        cls.btn_stopsave.clicked.connect(cls.save)

    @classmethod
    def _set_mode_prompt_reset(cls):
        """Set buttons to reset-prompt state."""

        cls._disconnect_buttons()

        cls.btn_startpause.setText("Confirm Reset")
        cls.btn_startpause.setIcon(QIcon.fromTheme('edit-undo'))
        cls.btn_startpause.setWhatsThis("Discard time and reset timer.")
        cls.btn_startpause.clicked.connect(cls.reset)

        cls.btn_stopsave.setIcon(QIcon.fromTheme('document-save'))
        cls.btn_stopsave.setWhatsThis("Save time and notes to log.")
        cls.btn_stopsave.setText("Save")
        cls.btn_stopsave.setEnabled(True)
        cls.btn_stopsave.clicked.connect(cls.save)

    @classmethod
    def _set_mode_prompt_stop(cls):
        """Set buttons to stopped-clock state."""

        cls._disconnect_buttons()

        cls.btn_startpause.setText("Resume")
        cls.btn_startpause.setIcon(QIcon.fromTheme('media-playback-start'))
        cls.btn_startpause.setWhatsThis("Resume timer from current time.")
        cls.btn_startpause.clicked.connect(cls.resume)

        cls.btn_stopsave.setText("Confirm Stop")
        cls.btn_stopsave.setIcon(QIcon.fromTheme('media-playback-stop'))
        cls.btn_stopsave.setWhatsThis("Stop timer. Timer must be stopped "
                                      "before you can save.")
        cls.btn_stopsave.clicked.connect(cls.stop)
        cls.btn_stopsave.setEnabled(True)

    @classmethod
    def _set_mode_running(cls):
        """Set buttons to running-clock state."""

        cls._disconnect_buttons()

        cls.btn_startpause.setText("Pause")
        cls.btn_startpause.setIcon(QIcon.fromTheme('media-playback-pause'))
        cls.btn_startpause.setWhatsThis("Pause timer.")
        cls.btn_startpause.clicked.connect(cls.pause)

        cls.btn_stopsave.setText("Stop")
        cls.btn_stopsave.setIcon(QIcon.fromTheme('media-playback-stop'))
        cls.btn_stopsave.setWhatsThis("Stop timer. Timer must be stopped "
                                      "before you can save.")
        cls.btn_stopsave.clicked.connect(cls.prompt_stop)
        cls.btn_stopsave.setEnabled(True)

    @classmethod
    def _set_mode_paused(cls):
        """Set buttons to paused-time state."""

        cls._disconnect_buttons()

        cls.btn_startpause.setText("Resume")
        cls.btn_startpause.setIcon(QIcon.fromTheme('media-playback-start'))
        cls.btn_startpause.setWhatsThis("Resume timer from current time.")
        cls.btn_startpause.clicked.connect(cls.resume)
        cls.btn_stopsave.setText("Stop")

        cls.btn_stopsave.setIcon(QIcon.fromTheme('media-playback-stop'))
        cls.btn_stopsave.setWhatsThis("Stop timer. Timer must be stopped "
                                      "before you can save.")
        cls.btn_stopsave.clicked.connect(cls.prompt_stop)
        cls.btn_stopsave.setEnabled(True)

    @classmethod
    def start(cls):
        """Start a new timer."""

        cls._set_mode_running()
        TimeDisplay.start_time()
        if cls.start_callback:
            cls.start_callback()

    @classmethod
    def resume(cls):
        """Resume a paused timer."""

        cls._set_mode_running()
        TimeDisplay.start_time()
        if cls.resume_callback:
            cls.resume_callback()

    @classmethod
    def pause(cls):
        """Pause a running timer."""

        cls._set_mode_paused()
        TimeDisplay.stop_time()
        if cls.pause_callback:
            cls.pause_callback()

    @classmethod
    def prompt_stop(cls):
        """Pause timer and confirm stop."""

        cls._set_mode_prompt_stop()
        TimeDisplay.stop_time()
        if cls.pause_callback:
            cls.pause_callback()

    @classmethod
    def cancel_stop(cls):
        """Resume timer after cancelling a stop request."""
        cls._set_mode_running()

    @classmethod
    def stop(cls):
        """Stop a timer."""
        # DO NOT call TimeDisplay.stop_time() again; it will double the time
        cls._set_mode_save()
        TimeDisplay.reset_time()
        if cls.stop_callback:
            cls.stop_callback()

    @classmethod
    def save(cls):
        """Save a stopped timer's time to the log."""

        cls._set_mode_stopped()
        notes = Notes.get_text()
        timestamp = TimeDisplay.get_timestamp()
        TimeLog.add_to_log(timestamp, *TimeDisplay.get_time(), notes)
        LogView.refresh()
        Notes.clear()
        TimeDisplay.stop_time()
        TimeDisplay.reset_time()
        if cls.save_callback:
            cls.save_callback()

    @classmethod
    def reset(cls):
        """Discard a stopped timer's time instead of saving it."""

        cls._set_mode_stopped()
        TimeDisplay.show_default()
        Notes.clear()
        if cls.reset_callback:
            cls.reset_callback()

    @classmethod
    def prompt_reset(cls):
        """Confirm reset."""

        cls._set_mode_prompt_reset()
