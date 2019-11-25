from . import App, LogView, Notes, TimeControls, TimeDisplay


def build():
    App.add_widget(TimeDisplay.build())
    App.add_widget(Notes.build())
    App.add_widget(TimeControls.build())
    App.add_widget(LogView.build())


def demo_data():
    TimeDisplay.show_time(7, 14, 21)
