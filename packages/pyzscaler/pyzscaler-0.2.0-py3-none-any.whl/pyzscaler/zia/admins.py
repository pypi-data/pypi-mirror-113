from box import BoxList
from restfly.endpoint import APIEndpoint


class AdminManagementAPI(APIEndpoint):

    def list_lite(self):
        """Retrieves only name and ID for all admin and auditor users.

        Returns:
            :obj:`list`: A list of admin and auditor users.

        """
        return self._get('adminRoles/lite', box=BoxList)

    def list(self):
        """Retrieves all admin and auditor users.

        Returns:
            :obj:`list`: A list of admin and auditor users.

        """
        return self._get('adminUsers', box=BoxList)

    # TODO: Come back and create admin creation method
    def add(self, login_name: str, user_name: str, email: str, **kwargs):
        """Adds a new auditor or admin user.

        Args:
            login_name (str):
                Admin or auditor's login name. loginName is in email format and uses the domain name associated to
                the Zscaler account.
            user_name (str):
                Admin or auditor's username.
            email (str):
                Admin or auditor's email address.
            **kwargs:
                Keyword arguments documented below

        Keyword Args:
            comments (str):
                Additional information about the admin or auditor.

        Returns:
            :obj:`dict`: The newly created admin or auditor resource record.

        """
        payload = {
            'loginName': login_name,
            'userName': user_name,
            'email': email,
            'role': kwargs.get('role', {}),
            'comments': kwargs.get('comments', ''),
            'adminScope': kwargs.get('admin_scope', {}),
            'isNonEditable': kwargs.get('is_non_editable', False),
            'isAuditor': kwargs.get('is_auditor', False),
            'password': kwargs.get('password', ''),
            'isPasswordLoginAllowed': kwargs.get('password_allowed', False),
            'isSecurityReportCommEnabled': kwargs.get('security_reports', False),
            'isServiceUpdateCommEnabled': kwargs.get('service_updates', False),
            'isProductUpdateCommEnabled': kwargs.get('product_updates', False),
            'isPasswordExpired': kwargs.get('password_expired', False),
            'isExecMobileAppEnabled': kwargs.get('exec_mobile', False)
        }
        return self._post('adminUsers')

    def update(self, id: str):
        return self._put(f'adminUsers/{id}')

    def delete(self, id: str):
        """Delete an admin or auditor user for the specified ID

        Args:
            id (str):
                The unique identifier for the admin or auditor user.

        Returns:
            :obj:`str`: The operation response code.

        """
        return self._delete(f'adminUsers/{id}')
