"""Response of Ticketmaster GET /discovery/v2/events, the search_events tool.

Keys arrive in camelCase and map to snake_case fields. Unknown keys are kept
(extra="allow"), so nothing Ticketmaster sends is dropped.
"""

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class TicketmasterModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, extra="allow")


class Link(TicketmasterModel):
    href: str


class ResourceLinks(TicketmasterModel):
    self_link: Link | None = Field(default=None, alias="self")


class PageLinks(TicketmasterModel):
    self_link: Link | None = Field(default=None, alias="self")
    first: Link | None = None
    prev: Link | None = None
    next: Link | None = None
    last: Link | None = None


class Page(TicketmasterModel):
    size: int | None = None
    total_elements: int | None = None
    total_pages: int | None = None
    number: int | None = None


class Image(TicketmasterModel):
    url: str
    ratio: str | None = None
    width: int | None = None
    height: int | None = None
    fallback: bool | None = None
    attribution: str | None = None


class NamedRef(TicketmasterModel):
    id: str | None = None
    name: str | None = None


class Classification(TicketmasterModel):
    primary: bool | None = None
    family: bool | None = None
    segment: NamedRef | None = None
    genre: NamedRef | None = None
    sub_genre: NamedRef | None = None
    type: NamedRef | None = None
    sub_type: NamedRef | None = None


class ExternalLink(TicketmasterModel):
    url: str | None = None
    id: str | None = None
    name: str | None = None


class TicketTextLines(TicketmasterModel):
    line1: str | None = None
    line2: str | None = None
    line3: str | None = None
    line4: str | None = None
    line5: str | None = None
    line6: str | None = None


class City(TicketmasterModel):
    name: str | None = None


class State(TicketmasterModel):
    name: str | None = None
    state_code: str | None = None


class Country(TicketmasterModel):
    name: str | None = None
    country_code: str | None = None


class Address(TicketmasterModel):
    line1: str | None = None
    line2: str | None = None


class Location(TicketmasterModel):
    latitude: str | None = None
    longitude: str | None = None


class Dma(TicketmasterModel):
    id: int | None = None


class TwitterHandle(TicketmasterModel):
    handle: str | None = None


class Social(TicketmasterModel):
    twitter: TwitterHandle | None = None


class BoxOfficeInfo(TicketmasterModel):
    phone_number_detail: str | None = None
    open_hours_detail: str | None = None
    accepted_payment_detail: str | None = None
    will_call_detail: str | None = None


class GeneralInfo(TicketmasterModel):
    general_rule: str | None = None
    child_rule: str | None = None


class Ada(TicketmasterModel):
    ada_phones: str | None = None
    ada_custom_copy: str | None = None
    ada_hours: str | None = None


class Venue(TicketmasterModel):
    id: str
    name: str | None = None
    type: str | None = None
    test: bool | None = None
    url: str | None = None
    locale: str | None = None
    aliases: list[str] = Field(default_factory=list)
    images: list[Image] = Field(default_factory=list)
    postal_code: str | None = None
    timezone: str | None = None
    city: City | None = None
    state: State | None = None
    country: Country | None = None
    address: Address | None = None
    location: Location | None = None
    markets: list[NamedRef] = Field(default_factory=list)
    dmas: list[Dma] = Field(default_factory=list)
    social: Social | None = None
    box_office_info: BoxOfficeInfo | None = None
    parking_detail: str | None = None
    accessible_seating_detail: str | None = None
    general_info: GeneralInfo | None = None
    ada: Ada | None = None
    external_links: dict[str, list[ExternalLink]] | None = None
    upcoming_events: dict[str, int] | None = None
    links: ResourceLinks | None = Field(default=None, alias="_links")


class Attraction(TicketmasterModel):
    id: str
    name: str | None = None
    type: str | None = None
    test: bool | None = None
    url: str | None = None
    locale: str | None = None
    aliases: list[str] = Field(default_factory=list)
    images: list[Image] = Field(default_factory=list)
    classifications: list[Classification] = Field(default_factory=list)
    external_links: dict[str, list[ExternalLink]] | None = None
    upcoming_events: dict[str, int] | None = None
    draft_status: str | None = None
    links: ResourceLinks | None = Field(default=None, alias="_links")


class PublicSale(TicketmasterModel):
    start_date_time: str | None = None
    end_date_time: str | None = None
    start_tbd: bool | None = Field(default=None, alias="startTBD")
    start_tba: bool | None = Field(default=None, alias="startTBA")


class Presale(TicketmasterModel):
    name: str | None = None
    description: str | None = None
    short_description: str | None = None
    link_description: str | None = None
    url: str | None = None
    start_date_time: str | None = None
    end_date_time: str | None = None


class Sales(TicketmasterModel):
    public: PublicSale | None = None
    presales: list[Presale] = Field(default_factory=list)


class LocalDateTime(TicketmasterModel):
    local_date: str | None = None
    local_time: str | None = None
    date_time: str | None = None


class EventStart(LocalDateTime):
    date_tbd: bool | None = Field(default=None, alias="dateTBD")
    date_tba: bool | None = Field(default=None, alias="dateTBA")
    time_tba: bool | None = Field(default=None, alias="timeTBA")
    no_specific_time: bool | None = None


class EventEnd(LocalDateTime):
    approximate: bool | None = None
    no_specific_time: bool | None = None


class EventAccess(TicketmasterModel):
    start_approximate: bool | None = None
    end_approximate: bool | None = None


class EventStatus(TicketmasterModel):
    code: str | None = None


class Dates(TicketmasterModel):
    start: EventStart | None = None
    end: EventEnd | None = None
    initial_start_date: LocalDateTime | None = None
    access: EventAccess | None = None
    timezone: str | None = None
    status: EventStatus | None = None
    span_multiple_days: bool | None = None


class Promoter(TicketmasterModel):
    id: str | None = None
    name: str | None = None
    description: str | None = None


class Seatmap(TicketmasterModel):
    static_url: str | None = None


class Accessibility(TicketmasterModel):
    info: str | None = None
    ticket_limit: int | None = None
    url: str | None = None
    url_text: str | None = None


class TicketLimit(TicketmasterModel):
    info: str | None = None


class AgeRestrictions(TicketmasterModel):
    legal_age_enforced: bool | None = None
    age_rule_description: str | None = None


class Enabled(TicketmasterModel):
    enabled: bool | None = None


class Ticketing(TicketmasterModel):
    safe_tix: Enabled | None = None
    all_inclusive_pricing: Enabled | None = None


class Product(TicketmasterModel):
    id: str | None = None
    name: str | None = None
    type: str | None = None
    url: str | None = None
    classifications: list[Classification] = Field(default_factory=list)
    on_upsell_landing_page: bool | None = None


class Outlet(TicketmasterModel):
    type: str | None = None
    url: str | None = None


class LinkMoreInfo(TicketmasterModel):
    url: str | None = None
    descriptions: dict[str, str] | None = None


class EventLinks(TicketmasterModel):
    self_link: Link | None = Field(default=None, alias="self")
    attractions: list[Link] = Field(default_factory=list)
    venues: list[Link] = Field(default_factory=list)


class EventEmbedded(TicketmasterModel):
    venues: list[Venue] = Field(default_factory=list)
    attractions: list[Attraction] = Field(default_factory=list)


class Event(TicketmasterModel):
    id: str
    name: str | None = None
    type: str | None = None
    test: bool | None = None
    url: str | None = None
    locale: str | None = None
    name_origin: str | None = None
    description: str | None = None
    info: str | None = None
    please_note: str | None = None
    images: list[Image] = Field(default_factory=list)
    sales: Sales | None = None
    dates: Dates | None = None
    doors_times: LocalDateTime | None = None
    classifications: list[Classification] = Field(default_factory=list)
    promoter: Promoter | None = None
    promoters: list[Promoter] = Field(default_factory=list)
    seatmap: Seatmap | None = None
    accessibility: Accessibility | None = None
    ticket_limit: TicketLimit | None = None
    age_restrictions: AgeRestrictions | None = None
    ticketing: Ticketing | None = None
    products: list[Product] = Field(default_factory=list)
    outlets: list[Outlet] = Field(default_factory=list)
    link_more_info: LinkMoreInfo | None = None
    ticket_text_lines: dict[str, TicketTextLines] | None = None
    upsell_landing_page_url: str | None = None
    links: EventLinks | None = Field(default=None, alias="_links")
    embedded: EventEmbedded | None = Field(default=None, alias="_embedded")


class SearchEventsEmbedded(TicketmasterModel):
    events: list[Event] = Field(default_factory=list)


class SearchEventsResponse(TicketmasterModel):
    embedded: SearchEventsEmbedded | None = Field(default=None, alias="_embedded")
    page: Page | None = None
    links: PageLinks | None = Field(default=None, alias="_links")
