from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class TicketmasterModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, extra="ignore")


class Page(TicketmasterModel):
    size: int | None = None
    number: int | None = None
    total_elements: int | None = None


class Image(TicketmasterModel):
    url: str
    ratio: str | None = None
    width: int | None = None
    height: int | None = None
    fallback: bool | None = None
    attribution: str | None = None


class City(TicketmasterModel):
    name: str | None = None


class State(TicketmasterModel):
    name: str | None = None
    state_code: str | None = None


class Country(TicketmasterModel):
    name: str | None = None
    country_code: str | None = None


class Venue(TicketmasterModel):
    id: str
    name: str | None = None
    url: str | None = None
    city: City | None = None
    state: State | None = None
    postal_code: str | None = None
    timezone: str | None = None


class EmbeddedVenue(TicketmasterModel):
    id: str
    name: str | None = None
    city: City | None = None
    state: State | None = None
    country: Country | None = None


class EmbeddedAttraction(TicketmasterModel):
    id: str
    name: str | None = None


class LocalDateTime(TicketmasterModel):
    local_date: str | None = None
    local_time: str | None = None
    date_time: str | None = None


class EventStatus(TicketmasterModel):
    code: str | None = None


class Dates(TicketmasterModel):
    start: LocalDateTime | None = None
    timezone: str | None = None
    status: EventStatus | None = None


class EventEmbedded(TicketmasterModel):
    venues: list[EmbeddedVenue] = Field(default_factory=list)
    attractions: list[EmbeddedAttraction] = Field(default_factory=list)


class Event(TicketmasterModel):
    id: str
    name: str | None = None
    url: str | None = None
    info: str | None = None
    dates: Dates | None = None
    embedded: EventEmbedded | None = Field(default=None, alias="_embedded")


class SearchEventsEmbedded(TicketmasterModel):
    events: list[Event] = Field(default_factory=list)


class SearchEventsResponse(TicketmasterModel):
    embedded: SearchEventsEmbedded | None = Field(default=None, alias="_embedded")
    page: Page | None = None
