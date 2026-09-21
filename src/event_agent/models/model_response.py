from pydantic import BaseModel, Field


class Event(BaseModel):
    city: str | None = Field(
        default=None,
        description="Name of the city where the Event is happening",
    )

    start_date_time: str | None = Field(
        default=None,
        description="Expected start date time of the event",
    )

    end_date_time: str | None = Field(
        default=None,
        description="Expected ending time of the event",
    )

    venue_name: str | None = Field(
        default=None, description="Name of the venue where the Event is happening"
    )


class Response(BaseModel):
    text: str = Field(description="Final Reply to the user's Query")

    event_response: list[Event] = Field(
        default_factory=list,
        description="Fill it whenever you have the events that you want to show to the user",
    )
