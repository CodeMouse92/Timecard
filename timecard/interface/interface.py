from timecard.interface.app import App
from timecard.interface.appcontrols import AppControls
from timecard.interface.notes import Notes
from timecard.interface.timecontrols import TimeControls
from timecard.interface.timedisplay import TimeDisplay
from timecard.interface.workspace import Workspace


def build():
    """Construct the interface."""
    App.build()
    App.add_widget(TimeDisplay.build())
    App.add_widget(Notes.build())
    App.add_widget(TimeControls.build())
    App.add_widget(Workspace.build())
    App.add_widget(AppControls.build())


def run():
    """Run the interface."""
    build()
    return App.run()
