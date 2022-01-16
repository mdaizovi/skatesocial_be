class EventResponseChoices:
    GOING = "G"
    NOT_GOING = "N"
    MAYBE = "M"

    CHOICES = (
        (GOING, "Going"),
        (NOT_GOING, "Not Going"),
        (MAYBE, "Maybe"),
    )


class EventWheelChoices:
    SKATEBOARD = "B"
    ROLLERSKATES = "R"
    INLINES = "I"
    WHEELCHAIR = "C"

    CHOICES = (
        (SKATEBOARD, "B"),
        (ROLLERSKATES, "R"),
        (INLINES, "I"),
        (WHEELCHAIR, "C"),
    )
