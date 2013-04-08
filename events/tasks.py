from celery import task
from .models import Event
from persist.exceptions import DoesNotExist

@task
def trigger_event(event_slug, *args, **kwargs):
    """
    Process a fired event, Trigger any registered event handlers

    An event can be split into parts by a : in order to subscribe to sub-events.

    For example the event for a switch press may be

    wemo:switch-press:1123-44334445

    It's up to each implementation to define its events.

    A subscriber may subscribe to any level of events "wemo", "wemo:switch_press", or "wemo:switch-press:1123-44334445"
    """
    splitevents = event_slug.split(":")
    c = len(splitevents)
    for i in range(c):
        try:
            # Get the event object(s)
            event = Event.retrieve(":".join(splitevents[:i+1]))
        except DoesNotExist:
            continue
        # Lookup which things are registered to this event type/device
        # Call those tasks
        event.call_listeners(*args, **kwargs)

