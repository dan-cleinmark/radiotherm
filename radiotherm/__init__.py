from .thermostat import Thermostat, CommonThermostat, CT50v109, CT50v188, CT50v194, CT80RevB2v103
from . import discover
from . import fields

THERMOSTATS = (CT50v109, CT50v188, CT50v194, CT80RevB2v103,)


def get_thermostat_class(model):
    """
    :param model:   string representation of the thermostat's model, in
                    whatever format the thermostat itself returns.
    :type model:    str

    :returns:       subclass of CommonThermostat, or None if there is not a
                    matching subclass found in THERMOSTATS.
    """
    for thermostat in THERMOSTATS:
        if issubclass(thermostat, Thermostat) and thermostat.MODEL == model:
            return thermostat


def get_thermostat(host_address=None):
    """
    If a host_address is not passed, auto-discovery will happen. Auto-discovery
    will only succeed then exactly 1 thermostat is on your network.

    :param host_address:    optional address for a thermostat. This can be an
                            IP address or domain name.

    :returns:   instance of a CommonThermostat subclass, or None if a matching
                subclass cannot be found.
    """
    if host_address is None:
        discovered_addresses = discover.discover_address()
        if len(discovered_addresses) > 1:
           raise IOError("Found %d thermostats and I don't know which to pick." % len(thermostats))
        host_address = discovered_addresses[0]
    initial = CommonThermostat(host_address)
    model = initial.model.get('raw')
    thermostat_class = get_thermostat_class(model)
    if thermostat_class is not None:
        return thermostat_class(host_address)


def get_thermostats():
    """
    Auto-discovers all thermostats on the network

    :returns:   list of CommonThermostat objects, or None if a matching
                subclass cannot be found.
    """
    host_addrs = discover.discover_address()
    for host_address in host_addrs:
        initial = CommonThermostat(host_address)
        model = initial.model.get('raw')
        thermostat_class = get_thermostat_class(model)
        if thermostat_class is not None:
            yield thermostat_class(host_address)
