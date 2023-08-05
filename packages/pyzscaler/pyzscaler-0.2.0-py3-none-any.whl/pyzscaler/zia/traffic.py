from restfly.endpoint import APIEndpoint
from box import Box, BoxList


class TrafficForwardingAPI(APIEndpoint):

    def list_gre_tunnels(self):
        """
        Retrieves a list of GRE tunnels.

        Returns:
            :obj:`list`
                The list of GRE tunnels configured in ZIA.

        Examples:
            >>> gre_tunnels = zia.traffic.gre_list()

        """
        return self._get('greTunnels', box=BoxList)

    def gre_details(self, id: str):
        """
        Retrieves info for a given GRE tunnel.

        Args:
            id (str):
                The unique identifier for the GRE tunnel.

        Returns:
            :obj:`dict`
                The GRE tunnel resource record.

        Examples:
            >>> gre_tunnel = zia.traffic.gre_details('3542')

        """
        return self._get(f'greTunnels/{id}')

    def gre_available_ranges(self):
        """
        Retrieves a list of available GRE tunnel ranges.

        Returns:
            :obj:`list`
                A list of available GRE tunnel ranges.

        Examples:
            >>> gre_tunnel_ranges = zia.traffic.gre_available_ranges()

        """
        return self._get('greTunnels/availableInternalIpRanges', box=BoxList)

    def gre_validate_ip(self, ip: str):
        # TODO: Come back and verify Returns / Example with output
        """
        Retrieves the static IP address and location mapping information for the specified GRE tunnel IP address.

        Args:
            ip (str):
                The static IP address being validated.

        Returns:
            :obj:`dict`
                Static IP address and location mapping information

        Examples:
            >>> gre_tunnel_ip = zia.traffic.gre_validate_ip('172.16.1.2')

        """
        return self._get(f'greTunnels/validateIP/{ip}')

    def add_gre_tunnel(self, source_ip: str, primary_dest_vip: object, secondary_dest_vip: object,
                       internal_ip_range: str,
                       within_country: bool, **kwargs):
        """
        Add a new GRE tunnel.

        Args:
            source_ip (str):
                The source IP address of the GRE tunnel. This is typically a static IP address in the organisation
                or SD-WAN.
            primary_dest_vip (object):
                The primary destination data center and virtual IP address (VIP) of the GRE tunnel.
            secondary_dest_vip (object):
                The secondary destination data center and virtual IP address (VIP) of the GRE tunnel.
            internal_ip_range (str):
                The start of the internal IP address in /29 CIDR range.
            within_country (bool):
                Restrict the data center virtual IP addresses (VIPs) only to those within the same country as the
                source IP address.

        Keyword Args:
             **comment (str):
                Additional information about this GRE tunnel
             **ip_unnumbered (bool):
                This is required to support the automated SD-WAN provisioning of GRE tunnels, when set to true
                gre_tun_ip and gre_tun_id are set to null

        Returns:
            :obj:`dict`
                The resource record for the newly created GRE tunnel.

        """

        # TODO: Add checks for params

        payload = {
            'sourceIp': source_ip,
            'primaryDestVip': primary_dest_vip,
            'secondaryDestVip': secondary_dest_vip,
            'internalIpRange': internal_ip_range,
            'within_country': within_country,
            'comment': kwargs.get('comment', ''),
            'ipUnnumbered': kwargs.get('ip_unnumbered', False)
        }

        return self._post('greTunnels', json=payload)

    def list_static_ips(self):
        """
        Retrieves a list of the configured static IPs.

        Returns:
            :obj:`list`
                A list of the configured static IPs

        Examples:
            >>> static_ips = zia.traffic.list_static_ips()

        """
        return self._get('staticIP', box=BoxList)

    def get_static_ip(self, id: str):
        """
        Retrieves information for a specified static IP.

        Args:
            id (str):
                The unique identifier for the static IP.

        Returns:
            :obj:`dict`
                The resource record for the static IP

        Examples:
            >>> static_ip = zia.traffic.get_static_ip('364')

        """
        return self._get(f'staticIP/{id}')

    def add_static_ip(self, ip_address=None, comment=None, **kwargs):
        """
        Adds a new static IP.

        Args:
            ip_address (str):
                The static IP address
            comment (str):
                Additional information about this static IP address.

        Keyword Args:
            **geo_override (bool):
                If not set, geographic coordinates and city are automatically determined from the IP address.
                Otherwise, the latitude and longitude coordinates must be provided.
            **routable_ip (bool):
                Indicates whether a non-RFC 1918 IP address is publicly routable. This attribute is ignored if there
                is no ZIA Private Service Edge associated to the organization.
            **latitude (float):
                Required only if the geoOverride attribute is set. Latitude with 7 digit precision after
                decimal point, ranges between -90 and 90 degrees.
            **longitude (float):
                Required only if the geoOverride attribute is set. Longitude with 7 digit precision after decimal
                point, ranges between -180 and 180 degrees.

        Returns:
            :obj:`dict`
                The resource record for the newly created static IP.

        """
        # TODO: Add checks for params

        payload = {
            'ipAddress': ip_address,
            'geoOverride': kwargs.get('geo_override', False),
            'routableIP': kwargs.get('routable_ip', True),
            'comment': comment
        }
        return self._post('staticIP', json=payload, box=False)

    def validate_static_ip(self, ip_address=None, comment=None, **kwargs):
        payload = {
            'ipAddress': ip_address,
            'geoOverride': kwargs.get('geo_override', False),
            'routableIP': kwargs.get('routable_ip', True),
            'comment': comment
        }
        return self._post('staticIP/validate', json=payload, box=False)

    def get_static_ip(self, id):
        return self._get(f'staticIP/{id}')

    def update_static_ip(self, id):
        return self._put(f'staticIP/{id}')

    def delete_static_ip(self, id):
        return self._delete(f'staticIP/{id}')

    def list_vips(self):
        return self._get('vips')

    def list_vips_recommended(self):
        return self._get('vips/recommendedList')

    def list_vpn_credentials(self):
        return self._get('vpnCredentials')

    def add_vpn_credentials(self, type: str, **kwargs):
        """
        Add new VPN credentials.

        Args:
            type (str):
                VPN authentication type (i.e., how the VPN credential is sent to the server). It is not modifiable
                after VpnCredential is created.

                Must be either CN, IP, UFQDN or XAUTH

        Keyword Args:
            fqdn (str):
                Fully Qualified Domain Name. Applicable only to UFQDN or XAUTH (or HOSTED_MOBILE_USERS) auth type.
            pre_shared_key (str):
                Pre-shared key. This is a required field for UFQDN and IP auth type.
            comments (str):
                Additional information about this VPN credential.

        Returns:
            :obj:`dict`
                The newly created VPN credential resource record.

        """

        payload = {
            'type': type,
            'fqdn': kwargs.get('fqdn', ''),
            'preSharedKey': kwargs.get('pre_shared_key', ''),
            'comments': kwargs.get('comments', '')
        }

        return self._post('vpnCredentials', json=payload)

    def bulk_delete_vpn_credentials(self, ids):
        # TODO: add request chunks if VPN credentials >100
        """
        Bulk delete VPN credentials.

        Args:
            ids (list):
                List of credential IDs that will be deleted.

        Returns:
            :obj:`str`
                Response code for operation.

        """

        payload = {
            "ids": ids
        }

        return self._post('vpnCredentials/bulkDelete', json=payload)

    def get_vpn_credentials(self, id):
        """
        Get VPN credentials for the specified ID.

        Args:
            id (str):
                The VPN credential unique identifier.

        Returns:
            :obj:`dict`
                The resource record for the requested VPN credentials.

        """
        return self._get(f'vpnCredentials/{id}')

    def update_vpn_credentials(self, type: str, **kwargs):
        """
        Update VPN credentials with the specified ID.

        Args:
            type (str):
                VPN authentication type (i.e., how the VPN credential is sent to the server). It is not modifiable
                after VpnCredential is created.

                Must be either CN, IP, UFQDN or XAUTH

        Keyword Args:
            fqdn (str):
                Fully Qualified Domain Name. Applicable only to UFQDN or XAUTH (or HOSTED_MOBILE_USERS) auth type.
            pre_shared_key (str):
                Pre-shared key. This is a required field for UFQDN and IP auth type.
            comments (str):
                Additional information about this VPN credential.

        Returns:
            :obj:`dict`
                The newly updated VPN credential resource record.

        """

        payload = {
            'type': type,
            'fqdn': kwargs.get('fqdn', ''),
            'preSharedKey': kwargs.get('pre_shared_key', ''),
            'comments': kwargs.get('comments', '')
        }

        return self._post('vpnCredentials', json=payload)

    def delete_vpn_credentials(self, id):
        """
        Delete VPN credentials for the specified ID.

        Args:
            id (str):
                The unique identifier for the VPN credentials that will be deleted.

        Returns:
            :obj:`str`
                Response code for the operation.

        Examples:
            >>> zia.traffic.delete_vpn_credentials('65')

        """
        return self._delete(f'vpnCredentials/{id}')
