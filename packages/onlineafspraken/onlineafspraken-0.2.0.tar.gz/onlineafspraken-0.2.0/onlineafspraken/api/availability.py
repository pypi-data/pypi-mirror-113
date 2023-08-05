from typing import List

from pydantic import ValidationError

from onlineafspraken.api.client import OnlineAfsprakenAPI
from onlineafspraken.schema.availability import (
    GetBookableDaysResponse,
    GetBookableTimesResponse,
    BookableTimeSchema,
)


def get_bookable_days(
    agenda_id, appointment_type_id, start_date, end_date, resource_id=None
) -> GetBookableDaysResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get(
        "getBookableDays",
        AgendaId=agenda_id,
        AppointmentTypeId=appointment_type_id,
        StartDate=start_date,
        EndDate=end_date,
        ResourceId=resource_id,
    )

    return GetBookableDaysResponse.parse_obj(resp["Response"])


def get_bookable_times(
    agenda_id,
    appointment_type_id,
    date,
    resource_id=None,
    start_time=None,
    end_time=None,
) -> List[BookableTimeSchema]:
    api = OnlineAfsprakenAPI()
    resp = api.get(
        "getBookableTimes",
        AgendaId=agenda_id,
        AppointmentTypeId=appointment_type_id,
        Date=date,
        ResourceId=resource_id,
        StartTime=start_time,
        EndTime=end_time,
    )

    try:
        response_object = GetBookableTimesResponse.parse_obj(resp["Response"])
    except ValidationError:

        # correcting the list
        resp["Response"]["Objects"]["BookableTime"] = [resp["Response"]["Objects"]["BookableTime"]]

        response_object = GetBookableTimesResponse.parse_obj(resp["Response"])

    if response_object.objects:
        return response_object.objects["BookableTime"]
    return []
