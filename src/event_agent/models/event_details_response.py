from event_agent.models.search_events_response import Event, TicketmasterModel


class PublicSale(TicketmasterModel):
    start_date_time: str | None = None
    end_date_time: str | None = None


class Sales(TicketmasterModel):
    public: PublicSale | None = None


class Seatmap(TicketmasterModel):
    static_url: str | None = None


class TicketLimit(TicketmasterModel):
    info: str | None = None


class AgeRestrictions(TicketmasterModel):
    legal_age_enforced: bool | None = None
    age_rule_description: str | None = None


class EventDetailsResponse(Event):
    sales: Sales | None = None
    seatmap: Seatmap | None = None
    ticket_limit: TicketLimit | None = None
    age_restrictions: AgeRestrictions | None = None
