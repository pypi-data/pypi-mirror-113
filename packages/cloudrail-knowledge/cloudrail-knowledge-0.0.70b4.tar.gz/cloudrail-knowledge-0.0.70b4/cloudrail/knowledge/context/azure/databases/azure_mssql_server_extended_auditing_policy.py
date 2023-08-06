from typing import List, Optional

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import \
    AzureResourceType


class AzureSqlServerExtendedAuditingPolicy(AzureResource):
    """
        Attributes:
            retention_in_days: The number of days to retain logs for in the storage account.
            log_monitoring_enabled: An indication if audit events is enabled.
            server_id: The ID of the SQL server in which to associate the audit policy.
    """

    def __init__(self, server_id: str, retention_in_days: int, log_monitoring_enabled: bool) -> None:
        super().__init__(AzureResourceType.AZURERM_MSSQL_SERVER_EXTENDED_AUDITING_POLICY)
        self.server_id: str = server_id
        self.with_aliases(server_id)
        self.retention_in_days: int = retention_in_days
        self.log_monitoring_enabled: bool = log_monitoring_enabled

    def get_keys(self) -> List[str]:
        return [self._id]

    def get_name(self) -> str:
        pass

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        return f'Extended Audit policy for {self.server_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'SQL Server Extended Auditing Policy'
        else:
            return 'SQL Server Extended Auditing Policies'

    @property
    def is_tagable(self) -> bool:
        return False
