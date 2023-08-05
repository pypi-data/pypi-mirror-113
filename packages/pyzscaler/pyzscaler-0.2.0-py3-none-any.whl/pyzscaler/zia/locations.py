from restfly.endpoint import APIEndpoint
from box import Box, BoxList


class LocationsAPI(APIEndpoint):

    def list(self):
        """
        Provides a list of configured locations.

        Returns:
            :obj:`list`: List of configured locations.

        Examples:
            >>> locations = zia.locations.list()

        """
        return self._get('locations', box=BoxList)

    def add(self, name: str, **kwargs):
        """
        Adds a new location.

        Args:
            name (str):
                Location name.

        Keyword Args:
            ip_address (list):
                    For locations: IP addresses of the egress points that are provisioned in the Zscaler Cloud.
                    Each entry is a single IP address (e.g., 238.10.33.9).

                    For sub-locations: Egress, internal, or GRE tunnel IP addresses. Each entry is either a single
                    IP address, CIDR (e.g., 10.10.33.0/24), or range (e.g., 10.10.33.1-10.10.33.10)).

        Returns:
            :obj:`dict`: The newly created location resource record

        Todo:
            * Check sensible defaults for commented params
            * Update docs after defaults have been set
        """
        payload = {
            'name': name,
            'parentId': kwargs.get('parent_id', 0),
            'ipAddresses': kwargs.get('ip_addresses', []),
            'upBandwidth': kwargs.get('up_bandwidth', 0),
            'dnBandwidth': kwargs.get('down_bandwidth', 0),
            'country': kwargs.get('country', 'UNITED_STATES'),
            'tz': kwargs.get('tz', 'GMT'),
            'authRequired': kwargs.get('auth_required', False),
            'xffForwardEnabled': kwargs.get('xff_forward_enabled', False),
            'surrogateIp': kwargs.get('surrogate_ip', False),
            'idleTimeInMinutes': kwargs.get('idle_time_in_minutes', 0),
            'displayTimeUnit': kwargs.get('display_time_unit', 'MINUTE'),
            'surrogateIpEnforcedForKnownBrowsers': kwargs.get('surrogate_enforcement', False),
            # 'surrogateRefreshTimeInMinutes': kwargs.get('surrogate_refresh_time', 5),
            'surrogateRefreshTimeUnit': kwargs.get('surrogate_refresh_units', 'MINUTE'),
            'ofwEnabled': kwargs.get('ofw_enabled', False),
            'ipsControl': kwargs.get('ips_control', False),
            'aupEnabled': kwargs.get('aup_enabled', False),
            'cautionEnabled': kwargs.get('caution_enabled', False),
            'aupBlockInternetUntilAccepted': kwargs.get('aup_block_internet', False),
            'aupForceSslInspection': kwargs.get('aup_force_ssl', False),
            # 'aupTimeoutInDays': kwargs.get('aup_timeout', 1)

        }

        return self._post('locations', json=payload)

    def detail(self, id: str):
        """
        Get the location information for the specified ID.

        Args:
            id (str):
                The unique identifier for the location.

        Returns:
            :obj:`dict`: The requested location resource record.

        """
        return self._get(f'locations/{id}')

    def sub_detail(self, id: str):
        """
        Get the sub-location information for the specified location ID.

        Args:
            id (str):
                The unique identifier for the parent location.

        Returns:
            :obj:`list`: A list of sub-locations configured for the parent location.

        """
        return self._get(f'locations/{id}/sublocations', box=BoxList)

    def lite(self):
        """
        Returns only the name and ID of all configured locations.

        Returns:
            :obj:`list`: A list of configured locations.

        """
        return self._get('locations/lite')

    def update(self, id: str):
        # TODO: Finish the update method

        return self._put(f'locations/{id}')

    def delete(self, id: str):
        """
        Deletes the location or sub-location for the specified ID

        Args:
            id (str):
                The unique identifier for the location or sub-location.

        Returns:
            :obj:`str`: Response code for the operation.

        """
        return self._delete(f'locations/{id}')
