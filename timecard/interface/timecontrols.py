from PySide2.QtWidgets import QPushButton, QHBoxLayout, QWidget
from PySide2.QtGui import QIcon

from timecard.interface.notes import Notes
from timecard.interface.timedisplay import TimeDisplay


class TimeControls:
    widget = QWidget()
    layout = QHBoxLayout()
    btn_startpause = QPushButton()
    btn_stop = QPushButton()

    start_callback = None
    resume_callback = None
    pause_callback = None
    stop_callback = None

    @classmethod
    def build(cls):
        cls.widget.setLayout(cls.layout)
        cls.layout.addWidget(cls.btn_startpause)
        cls.layout.addWidget(cls.btn_stop)

        cls._set_mode_stopped()

        return cls.widget

    @classmethod
    def connect(cls, /, start, resume, pause, stop):
        """Connect functions to the time control events.
        """
        cls.start_callback = start
        cls.resume_callback = resume
        cls.pause_callback = pause
        cls.stop_callback = stop

    @classmethod
    def _disconnect_buttons(cls):
        """
        Disconnect signals from the control buttons.
        This must be done before new signals can be added properly.
        """
        try:
            cls.btn_startpause.clicked.disconnect()
        except RuntimeError:
            pass

        try:
            cls.btn_stop.clicked.disconnect()
        except RuntimeError:
            pass

    @classmethod
    def _set_mode_stopped(cls):
        """
        Set buttons to stopped-clock state.
        """
        cls._disconnect_buttons()

        cls.btn_startpause.setText("Start")
        cls.btn_startpause.setIcon(QIcon.fromTheme('media-playback-start'))
        cls.btn_startpause.clicked.connect(cls.start)

        cls.btn_stop.setIcon(QIcon.fromTheme(None))
        cls.btn_stop.setText("Stopped")
        cls.btn_stop.setEnabled(False)

        TimeDisplay.stop_time()
        TimeDisplay.reset_time()

    @classmethod
    def _set_mode_prompt_stop(cls):
        """
        Set buttons to stopped-clock state.
        """
        cls._disconnect_buttons()

        cls.btn_startpause.setText("Resume")
        cls.btn_startpause.setIcon(QIcon.fromTheme('media-playback-start'))
        cls.btn_startpause.clicked.connect(cls.resume)

        cls.btn_stop.setText("Confirm Stop")
        cls.btn_stop.setIcon(QIcon.fromTheme('media-playback-stop'))
        cls.btn_stop.clicked.connect(cls.stop)
        cls.btn_stop.setEnabled(True)

    @classmethod
    def _set_mode_running(cls):
        """
        Set buttons to running-clock state.
        """
        cls._disconnect_buttons()

        cls.btn_startpause.setText("Pause")
        cls.btn_startpause.setIcon(QIcon.fromTheme('media-playback-pause'))
        cls.btn_startpause.clicked.connect(cls.pause)

        cls.btn_stop.setText("Stop")
        cls.btn_stop.setIcon(QIcon.fromTheme('media-playback-stop'))
        cls.btn_stop.clicked.connect(cls.prompt_stop)
        cls.btn_stop.setEnabled(True)

        TimeDisplay.start_time()

    @classmethod
    def _set_mode_paused(cls):
        """
        Set buttons to paused-time state.
        """
        cls._disconnect_buttons()

        cls.btn_startpause.setText("Resume")
        cls.btn_startpause.setIcon(QIcon.fromTheme('media-playback-start'))
        cls.btn_startpause.clicked.connect(cls.resume)
        cls.btn_stop.setText("Stop")

        cls.btn_stop.setIcon(QIcon.fromTheme('media-playback-stop'))
        cls.btn_stop.clicked.connect(cls.prompt_stop)
        cls.btn_stop.setEnabled(True)

        TimeDisplay.stop_time()

    @classmethod
    def start(cls):
        cls._set_mode_running()
        if cls.start_callback:
            cls.start_callback()

    @classmethod
    def resume(cls):
        cls._set_mode_running()
        if cls.resume_callback:
            cls.resume_callback()

    @classmethod
    def pause(cls):
        cls._set_mode_paused()
        if cls.pause_callback:
            cls.pause_callback()

    @classmethod
    def prompt_stop(cls):
        cls._set_mode_prompt_stop()
        if cls.pause_callback:
            cls.pause_callback()

    @classmethod
    def stop(cls):
        cls._set_mode_stopped()
        if cls.stop_callback:
            cls.stop_callback()
