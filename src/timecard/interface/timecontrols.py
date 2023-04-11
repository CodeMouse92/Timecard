"""Time Controls [Timecard]
Author(s): Jason C. McDonald

Controls the timer and saves the time entries to the log.
"""

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget

from timecard.data.timelog import TimeLog
from timecard.interface.logview import LogView
from timecard.interface.notes import Notes
from timecard.interface.timedisplay import TimeDisplay


class TimeControls:
    widget = QWidget()
    layout = QHBoxLayout()
    btn_startpause = QPushButton()
    btn_stopsave = QPushButton()

    start_callback = []
    resume_callback = []
    pause_callback = []
    stop_callback = []
    save_callback = []
    reset_callback = []

    @classmethod
    def build(cls):
        """Construct the interface."""
        cls.widget.setLayout(cls.layout)
        cls.layout.addWidget(cls.btn_startpause)
        cls.layout.addWidget(cls.btn_stopsave)

        cls._set_mode_stopped()

        return cls.widget

    @classmethod
    def connect(
        cls,
        on_start=None,
        on_resume=None,
        on_pause=None,
        on_stop=None,
        on_save=None,
        on_reset=None,
    ):
        """Connect callbacks to the time control events.
        Any callbacks not specified will not be overridden.
        (See disconnect() for removing callbacks.)

        Keyword arguments:
        on_start -- called when a new timer is started
        on_resume -- called when a timer is un-paused
        on_pause -- called when a timer is paused or tentatively-stopped
        on_stop -- called when a timer is stopped
        on_save -- called when a stopped timer is saved to log
        on_reset -- called when a stopped timer is cleared
        """
        if on_start and on_start not in cls.start_callback:
            cls.start_callback.append(on_start)

        if on_resume and on_resume not in cls.resume_callback:
            cls.resume_callback.append(on_resume)

        if on_pause and on_pause not in cls.pause_callback:
            cls.pause_callback.append(on_pause)

        if on_stop and on_stop not in cls.stop_callback:
            cls.stop_callback.append(on_stop)

        if on_save and on_save not in cls.save_callback:
            cls.save_callback.append(on_save)

        if on_reset and on_reset not in cls.reset_callback:
            cls.reset_callback.append(on_reset)

    @classmethod
    def disconnect(
        cls,
        on_start=None,
        on_resume=None,
        on_pause=None,
        on_stop=None,
        on_save=None,
        on_reset=None,
    ):
        """Disconnect functions from the time control events.
        Pass the function to remove from the callback.

        Keyword arguments:
        on_start -- called when a new timer is started
        on_resume -- called when a timer is un-paused
        on_pause -- called when a timer is paused or tentatively-stopped
        on_stop -- called when a timer is stopped
        on_save -- called when a stopped timer is saved to log
        on_reset -- called when a stopped timer is cleared
        """
        try:
            cls.start_callback.remove(on_start)
        except ValueError:
            pass

        try:
            cls.resume_callback.remove(on_resume)
        except ValueError:
            pass

        try:
            cls.pause_callback.remove(on_pause)
        except ValueError:
            pass

        try:
            cls.stop_callback.remove(on_stop)
        except ValueError:
            pass

        try:
            cls.save_callback.remove(on_save)
        except ValueError:
            pass

        try:
            cls.reset_callback.remove(on_reset)
        except ValueError:
            pass

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
        cls.btn_startpause.setIcon(QIcon.fromTheme("media-playback-start"))
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
        cls.btn_startpause.setIcon(QIcon.fromTheme("edit-undo"))
        cls.btn_startpause.setWhatsThis("Discard time and reset timer.")
        cls.btn_startpause.clicked.connect(cls.prompt_reset)

        cls.btn_stopsave.setIcon(QIcon.fromTheme("document-save"))
        cls.btn_stopsave.setWhatsThis("Save time and notes to log.")
        cls.btn_stopsave.setText("Save")
        cls.btn_stopsave.setEnabled(True)
        cls.btn_stopsave.clicked.connect(cls.save)

    @classmethod
    def _set_mode_prompt_reset(cls):
        """Set buttons to reset-prompt state."""

        cls._disconnect_buttons()

        cls.btn_startpause.setText("Confirm Reset")
        cls.btn_startpause.setIcon(QIcon.fromTheme("edit-undo"))
        cls.btn_startpause.setWhatsThis("Discard time and reset timer.")
        cls.btn_startpause.clicked.connect(cls.reset)

        cls.btn_stopsave.setIcon(QIcon.fromTheme("document-save"))
        cls.btn_stopsave.setWhatsThis("Save time and notes to log.")
        cls.btn_stopsave.setText("Save")
        cls.btn_stopsave.setEnabled(True)
        cls.btn_stopsave.clicked.connect(cls.save)

    @classmethod
    def _set_mode_prompt_stop(cls):
        """Set buttons to stopped-clock state."""

        cls._disconnect_buttons()

        cls.btn_startpause.setText("Resume")
        cls.btn_startpause.setIcon(QIcon.fromTheme("media-playback-start"))
        cls.btn_startpause.setWhatsThis("Resume timer from current time.")
        cls.btn_startpause.clicked.connect(cls.resume)

        cls.btn_stopsave.setText("Confirm Stop")
        cls.btn_stopsave.setIcon(QIcon.fromTheme("media-playback-stop"))
        cls.btn_stopsave.setWhatsThis(
            "Stop timer. Timer must be stopped " "before you can save."
        )
        cls.btn_stopsave.clicked.connect(cls.stop)
        cls.btn_stopsave.setEnabled(True)

    @classmethod
    def _set_mode_running(cls):
        """Set buttons to running-clock state."""

        cls._disconnect_buttons()

        cls.btn_startpause.setText("Pause")
        cls.btn_startpause.setIcon(QIcon.fromTheme("media-playback-pause"))
        cls.btn_startpause.setWhatsThis("Pause timer.")
        cls.btn_startpause.clicked.connect(cls.pause)

        cls.btn_stopsave.setText("Stop")
        cls.btn_stopsave.setIcon(QIcon.fromTheme("media-playback-stop"))
        cls.btn_stopsave.setWhatsThis(
            "Stop timer. Timer must be stopped " "before you can save."
        )
        cls.btn_stopsave.clicked.connect(cls.prompt_stop)
        cls.btn_stopsave.setEnabled(True)

    @classmethod
    def _set_mode_paused(cls):
        """Set buttons to paused-time state."""

        cls._disconnect_buttons()

        cls.btn_startpause.setText("Resume")
        cls.btn_startpause.setIcon(QIcon.fromTheme("media-playback-start"))
        cls.btn_startpause.setWhatsThis("Resume timer from current time.")
        cls.btn_startpause.clicked.connect(cls.resume)
        cls.btn_stopsave.setText("Stop")

        cls.btn_stopsave.setIcon(QIcon.fromTheme("media-playback-stop"))
        cls.btn_stopsave.setWhatsThis(
            "Stop timer. Timer must be stopped " "before you can save."
        )
        cls.btn_stopsave.clicked.connect(cls.prompt_stop)
        cls.btn_stopsave.setEnabled(True)

    @classmethod
    def start(cls):
        """Start a new timer."""

        cls._set_mode_running()
        TimeDisplay.start_time()
        for callback in cls.start_callback:
            callback()

    @classmethod
    def resume(cls):
        """Resume a paused timer."""

        cls._set_mode_running()
        TimeDisplay.start_time()
        for callback in cls.resume_callback:
            callback()

    @classmethod
    def pause(cls):
        """Pause a running timer."""

        cls._set_mode_paused()
        TimeDisplay.stop_time()
        for callback in cls.pause_callback:
            callback()

    @classmethod
    def prompt_stop(cls):
        """Pause timer and confirm stop."""

        cls._set_mode_prompt_stop()
        TimeDisplay.stop_time()
        for callback in cls.pause_callback:
            callback()

    @classmethod
    def cancel_stop(cls):
        """Resume timer after cancelling a stop request."""
        cls._set_mode_running()

    @classmethod
    def stop(cls):
        """Stop a timer."""
        # stop_time() already called from prompt_stop()
        cls._set_mode_save()
        TimeDisplay.reset_time()
        for callback in cls.stop_callback:
            callback()

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
        TimeDisplay.reset_time(erase=True)
        for callback in cls.save_callback:
            callback()

    @classmethod
    def reset(cls):
        """Discard a stopped timer's time instead of saving it."""

        cls._set_mode_stopped()
        TimeDisplay.reset_time(erase=True)
        TimeDisplay.show_default()
        Notes.clear()
        for callback in cls.reset_callback:
            callback()

    @classmethod
    def prompt_reset(cls):
        """Confirm reset."""

        cls._set_mode_prompt_reset()
