"""Response of Ticketmaster GET /discovery/v2/venues/{id}, the get_venue_details tool.

The body is a single venue object, the same shape Ticketmaster embeds in an event
under _embedded.venues, so the fields come from Venue. This subclass exists to give
the endpoint its own name and a place for detail-only fields, should any appear.
"""

from event_agent.models.search_events_response import Venue


class VenueDetailsResponse(Venue):
    pass
