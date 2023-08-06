# Copyright 2021 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A connector class includes methods needed for connectors.
"""
from unifyconnectorframework.organization_client import OrganizationClient, DatasetOperation

class Connector:
    """
    Common connector class
    """
    def __init__(self, account_id, password, org_id, hostname, id="", labels={"category": ""}, version="0.0.0"):
        """
        Initiate a new connector

        :type account_id: string
        :param account_id: Service account identifier
        :type password: string
        :param password: Content to upload
        :type org_id: string
        :param org_id: Content to upload
        :type hostname: string
        :param hostname: Content to upload
        :type id: GUID
        :param id: Connector identifier
        :type label: dict
        :param label: Labels associated to connector, in format {"category": "[connector_category]"}
        :type version: string
        :param version: Connector version
        """
        self.id = id
        self.labels = labels
        self.version = version
        self.account_id = account_id
        self.connector_params = {"connector_id": self.id, "account_id": self.account_id, "labels": self.labels.get("category"), "version": self.version}
        self.organization_client = OrganizationClient(
            user_name=self.account_id,
            password=password,
            org_id=org_id,
            cluster=hostname,
            connector_params=self.connector_params)

    def list_datasets(self):
        """
        Retrieve all datasets.
        """
        return self.organization_client.list_datasets()

    def create_dataset(self, name, dataset_csv):
        """
        Create a new dataset.

        :type name: string
        :param name: Name of dataset
        :type dataset_csv: string
        :param dataset_csv: Content to upload
        """
        return self.organization_client.create_dataset(name, dataset_csv)

    def update_dataset(self, dataset_csv, dataset_name=None, dataset_id=None):
        """
        Update a dataset. If dataset does not exist, create a new dataset.

        :type dataset_csv: string
        :param dataset_csv: Content to upload
        :type dataset_name: string
        :param dataset_name: Name of dataset
        :type dataset_id: string
        :param dataset_id: Existing dataset id
        """
        return self.organization_client.update_dataset(dataset_csv, dataset_name, dataset_id)

    def truncate_dataset(self, dataset_id):
        """
        Truncate a dataset.

        :type dataset_id: string
        :param dataset_id: Existing dataset id
        """
        return self.organization_client.update_dataset(dataset_id)

    def append_dataset(self, dataset_id, dataset_csv):
        """
        Append a dataset.

        :type dataset_csv: string
        :param dataset_csv: Content to upload
        :type dataset_id: string
        :param dataset_id: Existing dataset id
        """
        return self.organization_client.append_dataset(dataset_id, dataset_csv)

    def update_dataset_labels(self, dataset_id, labels):
        """
        Updates labels for a dataset.

        :type dataset_id: string
        :param dataset_id: Existing dataset id
        :type labels: dict
        :param labels: Labels
        """
        return self.organization_client.update_dataset_labels(dataset_id, labels)

    def operate_dataset(self, dataset_csv, dataset_id=None, dataset_name=None, operation=DatasetOperation.UPDATE):
        """
        Operate dataset on given dataset_id. If dataset_id is not given, create a dataset first.
        If dataset is not valid, throw an error.

        :type dataset_csv: string
        :param dataset_csv: Content to upload
        :type dataset_name: string
        :param dataset_name: Name of dataset
        :type dataset_id: string
        :param dataset_id: Existing dataset id
        :type operation: Enum
        :param operation: Operation on dataset, update or append
        """
        return self.organization_client.operate_dataset(dataset_csv, dataset_id, dataset_name, operation)

    def upload_template(self, template_csv):
        """
        Upload asset template definition csv.

        :type template_csv: string
        :param template_csv: asset template definition in csv format
        """
        return self.organization_client.upload_template(template_csv)

    def upload_template_configuration(self, config_csv):
        """
        Upload asset template configuration parameter definition csv.

        :type config_csv: string
        :param config_csv: asset template configuration parameter definition in csv format
        """
        return self.organization_client.upload_template_configuration(config_csv)

    def update_template_categories(self, template_id, template_name, version, categories):
        """
        Update categories to an asset template.

        :type template_id: string
        :param template_id: Existing template id
        :type template_name: string
        :param template_name: Existing template name
        :type version: string
        :param version: Existing template id
        :type categories: dict
        :param categories: Labels
        """
        return self.organization_client.update_template_categories(template_id, template_name, version, categories)

    def list_templates(self):
        """
        Retrieve all asset templates
        """
        return self.organization_client.list_templates()
    