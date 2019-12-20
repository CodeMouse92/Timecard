from . import App, LogView, Notes, TimeControls, TimeDisplay


def build():
    """Construct the interface."""
    App.build()
    App.add_widget(TimeDisplay.build())
    App.add_widget(Notes.build())
    App.add_widget(TimeControls.build())
    App.add_widget(LogView.build())


def run():
    """Run the interface."""
    build()
    return App.run()
