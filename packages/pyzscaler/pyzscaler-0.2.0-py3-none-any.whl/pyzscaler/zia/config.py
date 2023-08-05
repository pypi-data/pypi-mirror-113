from restfly.endpoint import APIEndpoint
from box import Box, BoxList


class ActivationAPI(APIEndpoint):

    def status(self):
        """
        Gets the activation status for a configuration change.

        Returns:
            :obj:`dict`
                Configuration status object.

        Examples:
            >>> config_status = zia.config.status()

        """
        return self._get('status')

    def activate(self):
        """
        Activates configuration changes.

        Returns:
            :obj:`dict`
                Configuration status object.

        Examples:
            >>> config_activate = zia.config.activate()

        """
        return self._post('status/activate')
