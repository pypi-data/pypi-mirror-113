import xmltodict

from onlineafspraken.api.client import OnlineAfsprakenAPI
from onlineafspraken.schema.general import (
    GetAgendaResponse,
    GetAgendasResponse,
    GetAppointmentTypeResponse,
    GetAppointmentTypesResponse,
    GetResourceResponse,
    GetResourcesResponse,
    RequiresConfirmationResponse,
)


def get_agenda(agenda_id) -> GetAgendaResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("getAgenda", id=agenda_id)

    return GetAgendaResponse.parse_obj(resp["Response"])


def get_agendas() -> GetAgendasResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("getAgendas")

    return GetAgendasResponse.parse_obj(resp["Response"])


def get_appointment_type(type_id) -> GetAppointmentTypeResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("getAppointmentType", id=type_id)

    return GetAppointmentTypeResponse.parse_obj(resp["Response"])


def get_appointment_types():
    api = OnlineAfsprakenAPI()
    resp = api.get("getAppointmentTypes")

    return GetAppointmentTypesResponse.parse_obj(resp["Response"])


def get_resource(resource_id) -> GetResourceResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("getResource", id=resource_id)

    return GetResourceResponse.parse_obj(resp["Response"])


def get_resources() -> GetResourcesResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("getAppointmentType")

    return GetResourcesResponse.parse_obj(resp["Response"])


def requires_confirmation() -> RequiresConfirmationResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("requiresConfirmation")

    return RequiresConfirmationResponse.parse_obj(resp["Response"])
