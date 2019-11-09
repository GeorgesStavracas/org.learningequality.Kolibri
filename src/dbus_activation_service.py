import dbus
import dbus.glib
import dbus.service
import os
import urllib.parse

from gi.repository import GLib
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Runs a D-Bus service to start and activate Kolibri on demand.
    """

    def handle(self, *args, **options):
        ActivationService()
        GLib.MainLoop().run()


def _get_terms(platform_data):
    return urllib.parse.quote(" ".join(platform_data.get("terms", [])))


def _get_url(terms, target_id):
    if terms:
        if target_id:
            return "/learn/#/topics/{id}?searchTerm={terms}".format(
                id=target_id, terms=terms
            )
        else:
            return "/learn/#/search?searchTerm={terms}".format(terms=terms)
    else:
        if target_id:
            return "/learn/#/topics/{id}".format(id=target_id)
        else:
            return ""


def _get_command(url=None):
    if url:
        return "/app/bin/open_kolibri.sh '{}'".format(url)
    else:
        return ""


dbus_args = {"dbus_interface": "org.freedesktop.Application"}


class ActivationService(dbus.service.Object):

    bus_name = "org.learningequality.Kolibri"
    _object_path = "/" + bus_name.replace(".", "/")

    def __init__(self):
        self.session_bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(self.bus_name, bus=self.session_bus)
        super().__init__(bus_name, self._object_path)

    @dbus.service.method(in_signature="a{sv}", **dbus_args)
    def Activate(self, platform_data):
        """The Activate method is called when the application is started
        without files to open."""
        os.system(_get_command())

    @dbus.service.method(in_signature="asa{sv}", **dbus_args)
    def Open(self, uris, platform_data):
        """The Open method is called when the application is started with files.
        The array of strings is an array of URIs, in UTF-8."""
        terms = _get_terms(platform_data)
        target_id = str(uris[0]) if uris else None
        url = _get_url(terms, target_id)
        os.system(_get_command(url))

    @dbus.service.method(in_signature="sava{sv}", **dbus_args)
    def ActivateAction(self, action_name, parameter, platform_data):
        """The ActivateAction method is called when Desktop Actions are activated.
        The action-name parameter is the name of the action."""
        os.system(_get_command())
