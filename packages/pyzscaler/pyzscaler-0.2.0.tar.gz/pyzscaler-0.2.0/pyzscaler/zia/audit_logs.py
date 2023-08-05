from restfly.endpoint import APIEndpoint


class AuditLogsAPI(APIEndpoint):

    def status(self):
        """
        Get the status of a request for an audit log report.

        Returns:
            :obj:`dict`
                Audit log report request status.

        """
        return self._get('auditlogEntryReport')

    # TODO: Need to test the create method and see which fields are optional and flag them.
    def create(self, start_time: int, end_time: int, action_types: list, category: str, sub_categories: list,
               action_result: str, action_interface: str, client_ip: str, admin_name: str):
        """
        Creates an audit log report for the specified time period and saves it as a CSV file. The report
        includes audit information for every call made to the cloud service API during the specified time period.
        Creating a new audit log report will overwrite a previously-generated report.

        Args:
            start_time:
                The timestamp, in epoch, of the admin's last login.
            end_time:
                The timestamp, in epoch, of the admin's last logout.
            action_types:
                The action performed by the admin in the Zscaler Admin Portal (i.e., Admin UI) or API.
            category:
                The location in the Zscaler Admin Portal (i.e., Admin UI) where the actionType was performed.
            sub_categories:
                The area within a category where the actionType was performed.
            action_result:
                The outcome (i.e., Failure or Success) of an actionType.
            action_interface:
                The interface (i.e., Admin UI or API) where the actionType was performed.
            client_ip:
                The source IP address for the admin.
            admin_name:
                The admin's login ID.

        Returns:
            :obj:`str`
                The status code for the operation.

        """
        payload = {
            "startTime": start_time,
            "endTime": end_time,
            "actionTypes": action_types,
            "category": category,
            "subcategories": sub_categories,
            "actionResult": action_result,
            "actionInterface": action_interface,
            "clientIp": client_ip,
            "adminName": admin_name
        }
        return self._post('auditlogEntryReport', json=payload)

    def cancel(self):
        """
        Cancels the request to create an audit log report.

        Returns:
            :obj:`str`
                The operation response code.

        """
        return self._delete('auditlogEntryReport')

    def download(self):
        """
        Downloads the most recently created audit log report.

        Returns:
            :obj:`csv`

        """
        return self._get('auditlogEntryReport/download')
