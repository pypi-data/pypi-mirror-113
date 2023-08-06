# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import Dict, List, Any


class CancelExecutionRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        execution_id: str = None,
    ):
        self.region_id = region_id
        self.execution_id = execution_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        return self


class CancelExecutionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class CancelExecutionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CancelExecutionResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CancelExecutionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ChangeResourceGroupRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        resource_id: str = None,
        new_resource_group_id: str = None,
        resource_type: str = None,
    ):
        self.region_id = region_id
        self.resource_id = resource_id
        self.new_resource_group_id = new_resource_group_id
        self.resource_type = resource_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.new_resource_group_id is not None:
            result['NewResourceGroupId'] = self.new_resource_group_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('NewResourceGroupId') is not None:
            self.new_resource_group_id = m.get('NewResourceGroupId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        return self


class ChangeResourceGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ChangeResourceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ChangeResourceGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ChangeResourceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateApplicationRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        description: str = None,
        type: str = None,
        resource_group_id: str = None,
        cloud_monitor_contact_group_list: str = None,
        cloud_monitor_enable_subscribe_event: bool = None,
        cloud_monitor_enable_install_agent: bool = None,
        cloud_monitor_template_id_list: str = None,
        cloud_monitor_rule_enabled: bool = None,
    ):
        self.region_id = region_id
        self.name = name
        self.description = description
        self.type = type
        self.resource_group_id = resource_group_id
        self.cloud_monitor_contact_group_list = cloud_monitor_contact_group_list
        self.cloud_monitor_enable_subscribe_event = cloud_monitor_enable_subscribe_event
        self.cloud_monitor_enable_install_agent = cloud_monitor_enable_install_agent
        self.cloud_monitor_template_id_list = cloud_monitor_template_id_list
        self.cloud_monitor_rule_enabled = cloud_monitor_rule_enabled

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        if self.type is not None:
            result['Type'] = self.type
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.cloud_monitor_contact_group_list is not None:
            result['CloudMonitorContactGroupList'] = self.cloud_monitor_contact_group_list
        if self.cloud_monitor_enable_subscribe_event is not None:
            result['CloudMonitorEnableSubscribeEvent'] = self.cloud_monitor_enable_subscribe_event
        if self.cloud_monitor_enable_install_agent is not None:
            result['CloudMonitorEnableInstallAgent'] = self.cloud_monitor_enable_install_agent
        if self.cloud_monitor_template_id_list is not None:
            result['CloudMonitorTemplateIdList'] = self.cloud_monitor_template_id_list
        if self.cloud_monitor_rule_enabled is not None:
            result['CloudMonitorRuleEnabled'] = self.cloud_monitor_rule_enabled
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CloudMonitorContactGroupList') is not None:
            self.cloud_monitor_contact_group_list = m.get('CloudMonitorContactGroupList')
        if m.get('CloudMonitorEnableSubscribeEvent') is not None:
            self.cloud_monitor_enable_subscribe_event = m.get('CloudMonitorEnableSubscribeEvent')
        if m.get('CloudMonitorEnableInstallAgent') is not None:
            self.cloud_monitor_enable_install_agent = m.get('CloudMonitorEnableInstallAgent')
        if m.get('CloudMonitorTemplateIdList') is not None:
            self.cloud_monitor_template_id_list = m.get('CloudMonitorTemplateIdList')
        if m.get('CloudMonitorRuleEnabled') is not None:
            self.cloud_monitor_rule_enabled = m.get('CloudMonitorRuleEnabled')
        return self


class CreateApplicationResponseBodyApplicationCloudMonitorRule(TeaModel):
    def __init__(
        self,
        enable_subscribe_event: bool = None,
        enable_install_agent: bool = None,
        enabled: bool = None,
        contact_group_list: List[str] = None,
        template_id_list: List[int] = None,
    ):
        self.enable_subscribe_event = enable_subscribe_event
        self.enable_install_agent = enable_install_agent
        self.enabled = enabled
        self.contact_group_list = contact_group_list
        self.template_id_list = template_id_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enable_subscribe_event is not None:
            result['EnableSubscribeEvent'] = self.enable_subscribe_event
        if self.enable_install_agent is not None:
            result['EnableInstallAgent'] = self.enable_install_agent
        if self.enabled is not None:
            result['Enabled'] = self.enabled
        if self.contact_group_list is not None:
            result['ContactGroupList'] = self.contact_group_list
        if self.template_id_list is not None:
            result['TemplateIdList'] = self.template_id_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EnableSubscribeEvent') is not None:
            self.enable_subscribe_event = m.get('EnableSubscribeEvent')
        if m.get('EnableInstallAgent') is not None:
            self.enable_install_agent = m.get('EnableInstallAgent')
        if m.get('Enabled') is not None:
            self.enabled = m.get('Enabled')
        if m.get('ContactGroupList') is not None:
            self.contact_group_list = m.get('ContactGroupList')
        if m.get('TemplateIdList') is not None:
            self.template_id_list = m.get('TemplateIdList')
        return self


class CreateApplicationResponseBodyApplication(TeaModel):
    def __init__(
        self,
        type: str = None,
        is_system: bool = None,
        description: str = None,
        update_date: str = None,
        name: str = None,
        create_date: str = None,
        cloud_monitor_rule: CreateApplicationResponseBodyApplicationCloudMonitorRule = None,
    ):
        self.type = type
        self.is_system = is_system
        self.description = description
        self.update_date = update_date
        self.name = name
        self.create_date = create_date
        self.cloud_monitor_rule = cloud_monitor_rule

    def validate(self):
        if self.cloud_monitor_rule:
            self.cloud_monitor_rule.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.is_system is not None:
            result['IsSystem'] = self.is_system
        if self.description is not None:
            result['Description'] = self.description
        if self.update_date is not None:
            result['UpdateDate'] = self.update_date
        if self.name is not None:
            result['Name'] = self.name
        if self.create_date is not None:
            result['CreateDate'] = self.create_date
        if self.cloud_monitor_rule is not None:
            result['CloudMonitorRule'] = self.cloud_monitor_rule.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('IsSystem') is not None:
            self.is_system = m.get('IsSystem')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('UpdateDate') is not None:
            self.update_date = m.get('UpdateDate')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('CreateDate') is not None:
            self.create_date = m.get('CreateDate')
        if m.get('CloudMonitorRule') is not None:
            temp_model = CreateApplicationResponseBodyApplicationCloudMonitorRule()
            self.cloud_monitor_rule = temp_model.from_map(m['CloudMonitorRule'])
        return self


class CreateApplicationResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        application: CreateApplicationResponseBodyApplication = None,
    ):
        self.request_id = request_id
        self.application = application

    def validate(self):
        if self.application:
            self.application.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.application is not None:
            result['Application'] = self.application.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Application') is not None:
            temp_model = CreateApplicationResponseBodyApplication()
            self.application = temp_model.from_map(m['Application'])
        return self


class CreateApplicationResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateApplicationResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateApplicationResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateApplicationGroupRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        application_name: str = None,
        description: str = None,
        deploy_region_id: str = None,
        environment: str = None,
        create_type: str = None,
        import_cluster_id: str = None,
        name: str = None,
    ):
        self.region_id = region_id
        self.application_name = application_name
        self.description = description
        self.deploy_region_id = deploy_region_id
        self.environment = environment
        self.create_type = create_type
        self.import_cluster_id = import_cluster_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.application_name is not None:
            result['ApplicationName'] = self.application_name
        if self.description is not None:
            result['Description'] = self.description
        if self.deploy_region_id is not None:
            result['DeployRegionId'] = self.deploy_region_id
        if self.environment is not None:
            result['Environment'] = self.environment
        if self.create_type is not None:
            result['CreateType'] = self.create_type
        if self.import_cluster_id is not None:
            result['ImportClusterId'] = self.import_cluster_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ApplicationName') is not None:
            self.application_name = m.get('ApplicationName')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DeployRegionId') is not None:
            self.deploy_region_id = m.get('DeployRegionId')
        if m.get('Environment') is not None:
            self.environment = m.get('Environment')
        if m.get('CreateType') is not None:
            self.create_type = m.get('CreateType')
        if m.get('ImportClusterId') is not None:
            self.import_cluster_id = m.get('ImportClusterId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class CreateApplicationGroupResponseBodyApplicationGroup(TeaModel):
    def __init__(
        self,
        deploy_region_id: str = None,
        description: str = None,
        updated_date: str = None,
        created_date: str = None,
        application_name: str = None,
        name: str = None,
        environment: str = None,
        create_type: str = None,
        scaling_group_id: str = None,
        import_cluster_id: str = None,
    ):
        self.deploy_region_id = deploy_region_id
        self.description = description
        self.updated_date = updated_date
        self.created_date = created_date
        self.application_name = application_name
        self.name = name
        self.environment = environment
        self.create_type = create_type
        self.scaling_group_id = scaling_group_id
        self.import_cluster_id = import_cluster_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.deploy_region_id is not None:
            result['DeployRegionId'] = self.deploy_region_id
        if self.description is not None:
            result['Description'] = self.description
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.application_name is not None:
            result['ApplicationName'] = self.application_name
        if self.name is not None:
            result['Name'] = self.name
        if self.environment is not None:
            result['Environment'] = self.environment
        if self.create_type is not None:
            result['CreateType'] = self.create_type
        if self.scaling_group_id is not None:
            result['ScalingGroupId'] = self.scaling_group_id
        if self.import_cluster_id is not None:
            result['ImportClusterId'] = self.import_cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DeployRegionId') is not None:
            self.deploy_region_id = m.get('DeployRegionId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ApplicationName') is not None:
            self.application_name = m.get('ApplicationName')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Environment') is not None:
            self.environment = m.get('Environment')
        if m.get('CreateType') is not None:
            self.create_type = m.get('CreateType')
        if m.get('ScalingGroupId') is not None:
            self.scaling_group_id = m.get('ScalingGroupId')
        if m.get('ImportClusterId') is not None:
            self.import_cluster_id = m.get('ImportClusterId')
        return self


class CreateApplicationGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        application_group: CreateApplicationGroupResponseBodyApplicationGroup = None,
    ):
        self.request_id = request_id
        self.application_group = application_group

    def validate(self):
        if self.application_group:
            self.application_group.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.application_group is not None:
            result['ApplicationGroup'] = self.application_group.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ApplicationGroup') is not None:
            temp_model = CreateApplicationGroupResponseBodyApplicationGroup()
            self.application_group = temp_model.from_map(m['ApplicationGroup'])
        return self


class CreateApplicationGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateApplicationGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateApplicationGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateParameterRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        type: str = None,
        value: str = None,
        description: str = None,
        client_token: str = None,
        constraints: str = None,
        tags: Dict[str, Any] = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.type = type
        self.value = value
        self.description = description
        self.client_token = client_token
        self.constraints = constraints
        self.tags = tags
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.type is not None:
            result['Type'] = self.type
        if self.value is not None:
            result['Value'] = self.value
        if self.description is not None:
            result['Description'] = self.description
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.constraints is not None:
            result['Constraints'] = self.constraints
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Constraints') is not None:
            self.constraints = m.get('Constraints')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class CreateParameterShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        type: str = None,
        value: str = None,
        description: str = None,
        client_token: str = None,
        constraints: str = None,
        tags_shrink: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.type = type
        self.value = value
        self.description = description
        self.client_token = client_token
        self.constraints = constraints
        self.tags_shrink = tags_shrink
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.type is not None:
            result['Type'] = self.type
        if self.value is not None:
            result['Value'] = self.value
        if self.description is not None:
            result['Description'] = self.description
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.constraints is not None:
            result['Constraints'] = self.constraints
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Constraints') is not None:
            self.constraints = m.get('Constraints')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class CreateParameterResponseBodyParameter(TeaModel):
    def __init__(
        self,
        type: str = None,
        updated_date: str = None,
        updated_by: str = None,
        tags: Dict[str, Any] = None,
        description: str = None,
        constraints: str = None,
        resource_group_id: str = None,
        created_by: str = None,
        created_date: str = None,
        parameter_version: int = None,
        name: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.type = type
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.tags = tags
        self.description = description
        self.constraints = constraints
        self.resource_group_id = resource_group_id
        self.created_by = created_by
        self.created_date = created_date
        self.parameter_version = parameter_version
        self.name = name
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.description is not None:
            result['Description'] = self.description
        if self.constraints is not None:
            result['Constraints'] = self.constraints
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Constraints') is not None:
            self.constraints = m.get('Constraints')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class CreateParameterResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        parameter: CreateParameterResponseBodyParameter = None,
    ):
        self.request_id = request_id
        self.parameter = parameter

    def validate(self):
        if self.parameter:
            self.parameter.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.parameter is not None:
            result['Parameter'] = self.parameter.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Parameter') is not None:
            temp_model = CreateParameterResponseBodyParameter()
            self.parameter = temp_model.from_map(m['Parameter'])
        return self


class CreateParameterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateParameterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateParameterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreatePatchBaselineRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        description: str = None,
        client_token: str = None,
        operation_system: str = None,
        approval_rules: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.description = description
        self.client_token = client_token
        self.operation_system = operation_system
        self.approval_rules = approval_rules

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.operation_system is not None:
            result['OperationSystem'] = self.operation_system
        if self.approval_rules is not None:
            result['ApprovalRules'] = self.approval_rules
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('OperationSystem') is not None:
            self.operation_system = m.get('OperationSystem')
        if m.get('ApprovalRules') is not None:
            self.approval_rules = m.get('ApprovalRules')
        return self


class CreatePatchBaselineResponseBodyPatchBaseline(TeaModel):
    def __init__(
        self,
        operation_system: str = None,
        description: str = None,
        updated_date: str = None,
        updated_by: str = None,
        created_by: str = None,
        created_date: str = None,
        name: str = None,
        approval_rules: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.operation_system = operation_system
        self.description = description
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.created_by = created_by
        self.created_date = created_date
        self.name = name
        self.approval_rules = approval_rules
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.operation_system is not None:
            result['OperationSystem'] = self.operation_system
        if self.description is not None:
            result['Description'] = self.description
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.name is not None:
            result['Name'] = self.name
        if self.approval_rules is not None:
            result['ApprovalRules'] = self.approval_rules
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OperationSystem') is not None:
            self.operation_system = m.get('OperationSystem')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ApprovalRules') is not None:
            self.approval_rules = m.get('ApprovalRules')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class CreatePatchBaselineResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        patch_baseline: CreatePatchBaselineResponseBodyPatchBaseline = None,
    ):
        self.request_id = request_id
        self.patch_baseline = patch_baseline

    def validate(self):
        if self.patch_baseline:
            self.patch_baseline.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.patch_baseline is not None:
            result['PatchBaseline'] = self.patch_baseline.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PatchBaseline') is not None:
            temp_model = CreatePatchBaselineResponseBodyPatchBaseline()
            self.patch_baseline = temp_model.from_map(m['PatchBaseline'])
        return self


class CreatePatchBaselineResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreatePatchBaselineResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreatePatchBaselineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateSecretParameterRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        type: str = None,
        value: str = None,
        description: str = None,
        key_id: str = None,
        client_token: str = None,
        constraints: str = None,
        tags: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.type = type
        self.value = value
        self.description = description
        self.key_id = key_id
        self.client_token = client_token
        self.constraints = constraints
        self.tags = tags
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.type is not None:
            result['Type'] = self.type
        if self.value is not None:
            result['Value'] = self.value
        if self.description is not None:
            result['Description'] = self.description
        if self.key_id is not None:
            result['KeyId'] = self.key_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.constraints is not None:
            result['Constraints'] = self.constraints
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('KeyId') is not None:
            self.key_id = m.get('KeyId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Constraints') is not None:
            self.constraints = m.get('Constraints')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class CreateSecretParameterResponseBodyParameter(TeaModel):
    def __init__(
        self,
        type: str = None,
        updated_date: str = None,
        updated_by: str = None,
        key_id: str = None,
        tags: str = None,
        description: str = None,
        constraints: str = None,
        resource_group_id: str = None,
        created_by: str = None,
        created_date: str = None,
        parameter_version: int = None,
        name: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.type = type
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.key_id = key_id
        self.tags = tags
        self.description = description
        self.constraints = constraints
        self.resource_group_id = resource_group_id
        self.created_by = created_by
        self.created_date = created_date
        self.parameter_version = parameter_version
        self.name = name
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.key_id is not None:
            result['KeyId'] = self.key_id
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.description is not None:
            result['Description'] = self.description
        if self.constraints is not None:
            result['Constraints'] = self.constraints
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('KeyId') is not None:
            self.key_id = m.get('KeyId')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Constraints') is not None:
            self.constraints = m.get('Constraints')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class CreateSecretParameterResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        parameter: CreateSecretParameterResponseBodyParameter = None,
    ):
        self.request_id = request_id
        self.parameter = parameter

    def validate(self):
        if self.parameter:
            self.parameter.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.parameter is not None:
            result['Parameter'] = self.parameter.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Parameter') is not None:
            temp_model = CreateSecretParameterResponseBodyParameter()
            self.parameter = temp_model.from_map(m['Parameter'])
        return self


class CreateSecretParameterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateSecretParameterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateSecretParameterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateStateConfigurationRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        description: str = None,
        template_name: str = None,
        template_version: str = None,
        parameters: str = None,
        configure_mode: str = None,
        schedule_type: str = None,
        schedule_expression: str = None,
        targets: str = None,
        client_token: str = None,
        tags: Dict[str, Any] = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.description = description
        self.template_name = template_name
        self.template_version = template_version
        self.parameters = parameters
        self.configure_mode = configure_mode
        self.schedule_type = schedule_type
        self.schedule_expression = schedule_expression
        self.targets = targets
        self.client_token = client_token
        self.tags = tags
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.description is not None:
            result['Description'] = self.description
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        if self.configure_mode is not None:
            result['ConfigureMode'] = self.configure_mode
        if self.schedule_type is not None:
            result['ScheduleType'] = self.schedule_type
        if self.schedule_expression is not None:
            result['ScheduleExpression'] = self.schedule_expression
        if self.targets is not None:
            result['Targets'] = self.targets
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        if m.get('ConfigureMode') is not None:
            self.configure_mode = m.get('ConfigureMode')
        if m.get('ScheduleType') is not None:
            self.schedule_type = m.get('ScheduleType')
        if m.get('ScheduleExpression') is not None:
            self.schedule_expression = m.get('ScheduleExpression')
        if m.get('Targets') is not None:
            self.targets = m.get('Targets')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class CreateStateConfigurationShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        description: str = None,
        template_name: str = None,
        template_version: str = None,
        parameters: str = None,
        configure_mode: str = None,
        schedule_type: str = None,
        schedule_expression: str = None,
        targets: str = None,
        client_token: str = None,
        tags_shrink: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.description = description
        self.template_name = template_name
        self.template_version = template_version
        self.parameters = parameters
        self.configure_mode = configure_mode
        self.schedule_type = schedule_type
        self.schedule_expression = schedule_expression
        self.targets = targets
        self.client_token = client_token
        self.tags_shrink = tags_shrink
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.description is not None:
            result['Description'] = self.description
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        if self.configure_mode is not None:
            result['ConfigureMode'] = self.configure_mode
        if self.schedule_type is not None:
            result['ScheduleType'] = self.schedule_type
        if self.schedule_expression is not None:
            result['ScheduleExpression'] = self.schedule_expression
        if self.targets is not None:
            result['Targets'] = self.targets
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        if m.get('ConfigureMode') is not None:
            self.configure_mode = m.get('ConfigureMode')
        if m.get('ScheduleType') is not None:
            self.schedule_type = m.get('ScheduleType')
        if m.get('ScheduleExpression') is not None:
            self.schedule_expression = m.get('ScheduleExpression')
        if m.get('Targets') is not None:
            self.targets = m.get('Targets')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class CreateStateConfigurationResponseBodyStateConfiguration(TeaModel):
    def __init__(
        self,
        create_time: str = None,
        targets: str = None,
        tags: Dict[str, Any] = None,
        state_configuration_id: str = None,
        schedule_expression: str = None,
        template_name: str = None,
        template_version: str = None,
        configure_mode: str = None,
        schedule_type: str = None,
        parameters: Dict[str, Any] = None,
        description: str = None,
        resource_group_id: str = None,
        template_id: str = None,
    ):
        self.create_time = create_time
        self.targets = targets
        self.tags = tags
        self.state_configuration_id = state_configuration_id
        self.schedule_expression = schedule_expression
        self.template_name = template_name
        self.template_version = template_version
        self.configure_mode = configure_mode
        self.schedule_type = schedule_type
        self.parameters = parameters
        self.description = description
        self.resource_group_id = resource_group_id
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.targets is not None:
            result['Targets'] = self.targets
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.state_configuration_id is not None:
            result['StateConfigurationId'] = self.state_configuration_id
        if self.schedule_expression is not None:
            result['ScheduleExpression'] = self.schedule_expression
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.configure_mode is not None:
            result['ConfigureMode'] = self.configure_mode
        if self.schedule_type is not None:
            result['ScheduleType'] = self.schedule_type
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        if self.description is not None:
            result['Description'] = self.description
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Targets') is not None:
            self.targets = m.get('Targets')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('StateConfigurationId') is not None:
            self.state_configuration_id = m.get('StateConfigurationId')
        if m.get('ScheduleExpression') is not None:
            self.schedule_expression = m.get('ScheduleExpression')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('ConfigureMode') is not None:
            self.configure_mode = m.get('ConfigureMode')
        if m.get('ScheduleType') is not None:
            self.schedule_type = m.get('ScheduleType')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class CreateStateConfigurationResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        state_configuration: CreateStateConfigurationResponseBodyStateConfiguration = None,
    ):
        self.request_id = request_id
        self.state_configuration = state_configuration

    def validate(self):
        if self.state_configuration:
            self.state_configuration.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.state_configuration is not None:
            result['StateConfiguration'] = self.state_configuration.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('StateConfiguration') is not None:
            temp_model = CreateStateConfigurationResponseBodyStateConfiguration()
            self.state_configuration = temp_model.from_map(m['StateConfiguration'])
        return self


class CreateStateConfigurationResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateStateConfigurationResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateStateConfigurationResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateTemplateRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        content: str = None,
        tags: Dict[str, Any] = None,
        version_name: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.content = content
        self.tags = tags
        self.version_name = version_name
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.content is not None:
            result['Content'] = self.content
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.version_name is not None:
            result['VersionName'] = self.version_name
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('VersionName') is not None:
            self.version_name = m.get('VersionName')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class CreateTemplateShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        content: str = None,
        tags_shrink: str = None,
        version_name: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.content = content
        self.tags_shrink = tags_shrink
        self.version_name = version_name
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.content is not None:
            result['Content'] = self.content
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        if self.version_name is not None:
            result['VersionName'] = self.version_name
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        if m.get('VersionName') is not None:
            self.version_name = m.get('VersionName')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class CreateTemplateResponseBodyTemplate(TeaModel):
    def __init__(
        self,
        hash: str = None,
        updated_date: str = None,
        updated_by: str = None,
        tags: Dict[str, Any] = None,
        template_name: str = None,
        template_version: str = None,
        template_format: str = None,
        description: str = None,
        resource_group_id: str = None,
        created_by: str = None,
        created_date: str = None,
        template_id: str = None,
        has_trigger: bool = None,
        share_type: str = None,
    ):
        self.hash = hash
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.tags = tags
        self.template_name = template_name
        self.template_version = template_version
        self.template_format = template_format
        self.description = description
        self.resource_group_id = resource_group_id
        self.created_by = created_by
        self.created_date = created_date
        self.template_id = template_id
        self.has_trigger = has_trigger
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.hash is not None:
            result['Hash'] = self.hash
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.template_format is not None:
            result['TemplateFormat'] = self.template_format
        if self.description is not None:
            result['Description'] = self.description
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        if self.has_trigger is not None:
            result['HasTrigger'] = self.has_trigger
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Hash') is not None:
            self.hash = m.get('Hash')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('TemplateFormat') is not None:
            self.template_format = m.get('TemplateFormat')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        if m.get('HasTrigger') is not None:
            self.has_trigger = m.get('HasTrigger')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class CreateTemplateResponseBody(TeaModel):
    def __init__(
        self,
        template_type: str = None,
        request_id: str = None,
        template: CreateTemplateResponseBodyTemplate = None,
    ):
        self.template_type = template_type
        self.request_id = request_id
        self.template = template

    def validate(self):
        if self.template:
            self.template.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.template_type is not None:
            result['TemplateType'] = self.template_type
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.template is not None:
            result['Template'] = self.template.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TemplateType') is not None:
            self.template_type = m.get('TemplateType')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Template') is not None:
            temp_model = CreateTemplateResponseBodyTemplate()
            self.template = temp_model.from_map(m['Template'])
        return self


class CreateTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateTemplateResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteApplicationRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
    ):
        self.region_id = region_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DeleteApplicationResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteApplicationResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteApplicationResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteApplicationResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteApplicationGroupRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
    ):
        self.region_id = region_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DeleteApplicationGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteApplicationGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteApplicationGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteApplicationGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteExecutionsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        execution_ids: str = None,
    ):
        self.region_id = region_id
        self.execution_ids = execution_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.execution_ids is not None:
            result['ExecutionIds'] = self.execution_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ExecutionIds') is not None:
            self.execution_ids = m.get('ExecutionIds')
        return self


class DeleteExecutionsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteExecutionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteExecutionsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteExecutionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteParameterRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
    ):
        self.region_id = region_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DeleteParameterResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteParameterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteParameterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteParameterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeletePatchBaselineRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
    ):
        self.region_id = region_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DeletePatchBaselineResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeletePatchBaselineResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeletePatchBaselineResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeletePatchBaselineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteSecretParameterRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
    ):
        self.region_id = region_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DeleteSecretParameterResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteSecretParameterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteSecretParameterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteSecretParameterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteStateConfigurationsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        state_configuration_ids: str = None,
        client_token: str = None,
    ):
        self.region_id = region_id
        self.state_configuration_ids = state_configuration_ids
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.state_configuration_ids is not None:
            result['StateConfigurationIds'] = self.state_configuration_ids
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('StateConfigurationIds') is not None:
            self.state_configuration_ids = m.get('StateConfigurationIds')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        return self


class DeleteStateConfigurationsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteStateConfigurationsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteStateConfigurationsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteStateConfigurationsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteTemplateRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        auto_delete_executions: bool = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.auto_delete_executions = auto_delete_executions

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.auto_delete_executions is not None:
            result['AutoDeleteExecutions'] = self.auto_delete_executions
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('AutoDeleteExecutions') is not None:
            self.auto_delete_executions = m.get('AutoDeleteExecutions')
        return self


class DeleteTemplateResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteTemplateResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteTemplatesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_names: str = None,
        auto_delete_executions: bool = None,
    ):
        self.region_id = region_id
        self.template_names = template_names
        self.auto_delete_executions = auto_delete_executions

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_names is not None:
            result['TemplateNames'] = self.template_names
        if self.auto_delete_executions is not None:
            result['AutoDeleteExecutions'] = self.auto_delete_executions
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateNames') is not None:
            self.template_names = m.get('TemplateNames')
        if m.get('AutoDeleteExecutions') is not None:
            self.auto_delete_executions = m.get('AutoDeleteExecutions')
        return self


class DeleteTemplatesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteTemplatesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteTemplatesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteTemplatesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRegionsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        accept_language: str = None,
    ):
        self.region_id = region_id
        self.accept_language = accept_language

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.accept_language is not None:
            result['AcceptLanguage'] = self.accept_language
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('AcceptLanguage') is not None:
            self.accept_language = m.get('AcceptLanguage')
        return self


class DescribeRegionsResponseBodyRegions(TeaModel):
    def __init__(
        self,
        region_endpoint: str = None,
        local_name: str = None,
        region_id: str = None,
    ):
        self.region_endpoint = region_endpoint
        self.local_name = local_name
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_endpoint is not None:
            result['RegionEndpoint'] = self.region_endpoint
        if self.local_name is not None:
            result['LocalName'] = self.local_name
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionEndpoint') is not None:
            self.region_endpoint = m.get('RegionEndpoint')
        if m.get('LocalName') is not None:
            self.local_name = m.get('LocalName')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeRegionsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        regions: List[DescribeRegionsResponseBodyRegions] = None,
    ):
        self.request_id = request_id
        self.regions = regions

    def validate(self):
        if self.regions:
            for k in self.regions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Regions'] = []
        if self.regions is not None:
            for k in self.regions:
                result['Regions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.regions = []
        if m.get('Regions') is not None:
            for k in m.get('Regions'):
                temp_model = DescribeRegionsResponseBodyRegions()
                self.regions.append(temp_model.from_map(k))
        return self


class DescribeRegionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeRegionsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeRegionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GenerateExecutionPolicyRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        template_version: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.template_version = template_version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        return self


class GenerateExecutionPolicyResponseBody(TeaModel):
    def __init__(
        self,
        policy: str = None,
        request_id: str = None,
    ):
        self.policy = policy
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.policy is not None:
            result['Policy'] = self.policy
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Policy') is not None:
            self.policy = m.get('Policy')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GenerateExecutionPolicyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GenerateExecutionPolicyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GenerateExecutionPolicyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetApplicationRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
    ):
        self.region_id = region_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class GetApplicationResponseBodyApplicationCloudMonitorRule(TeaModel):
    def __init__(
        self,
        enable_subscribe_event: bool = None,
        enable_install_agent: bool = None,
        enabled: bool = None,
        contact_group_list: List[str] = None,
        template_id_list: List[int] = None,
    ):
        self.enable_subscribe_event = enable_subscribe_event
        self.enable_install_agent = enable_install_agent
        self.enabled = enabled
        self.contact_group_list = contact_group_list
        self.template_id_list = template_id_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enable_subscribe_event is not None:
            result['EnableSubscribeEvent'] = self.enable_subscribe_event
        if self.enable_install_agent is not None:
            result['EnableInstallAgent'] = self.enable_install_agent
        if self.enabled is not None:
            result['Enabled'] = self.enabled
        if self.contact_group_list is not None:
            result['ContactGroupList'] = self.contact_group_list
        if self.template_id_list is not None:
            result['TemplateIdList'] = self.template_id_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EnableSubscribeEvent') is not None:
            self.enable_subscribe_event = m.get('EnableSubscribeEvent')
        if m.get('EnableInstallAgent') is not None:
            self.enable_install_agent = m.get('EnableInstallAgent')
        if m.get('Enabled') is not None:
            self.enabled = m.get('Enabled')
        if m.get('ContactGroupList') is not None:
            self.contact_group_list = m.get('ContactGroupList')
        if m.get('TemplateIdList') is not None:
            self.template_id_list = m.get('TemplateIdList')
        return self


class GetApplicationResponseBodyApplication(TeaModel):
    def __init__(
        self,
        is_system: str = None,
        description: str = None,
        updated_date: str = None,
        resource_group_id: str = None,
        created_date: str = None,
        name: str = None,
        cloud_monitor_rule: GetApplicationResponseBodyApplicationCloudMonitorRule = None,
    ):
        self.is_system = is_system
        self.description = description
        self.updated_date = updated_date
        self.resource_group_id = resource_group_id
        self.created_date = created_date
        self.name = name
        self.cloud_monitor_rule = cloud_monitor_rule

    def validate(self):
        if self.cloud_monitor_rule:
            self.cloud_monitor_rule.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.is_system is not None:
            result['IsSystem'] = self.is_system
        if self.description is not None:
            result['Description'] = self.description
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.name is not None:
            result['Name'] = self.name
        if self.cloud_monitor_rule is not None:
            result['CloudMonitorRule'] = self.cloud_monitor_rule.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('IsSystem') is not None:
            self.is_system = m.get('IsSystem')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('CloudMonitorRule') is not None:
            temp_model = GetApplicationResponseBodyApplicationCloudMonitorRule()
            self.cloud_monitor_rule = temp_model.from_map(m['CloudMonitorRule'])
        return self


class GetApplicationResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        application: GetApplicationResponseBodyApplication = None,
    ):
        self.request_id = request_id
        self.application = application

    def validate(self):
        if self.application:
            self.application.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.application is not None:
            result['Application'] = self.application.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Application') is not None:
            temp_model = GetApplicationResponseBodyApplication()
            self.application = temp_model.from_map(m['Application'])
        return self


class GetApplicationResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetApplicationResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetApplicationResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetApplicationGroupRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
    ):
        self.region_id = region_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class GetApplicationGroupResponseBodyApplicationGroup(TeaModel):
    def __init__(
        self,
        deploy_region_id: str = None,
        description: str = None,
        updated_date: str = None,
        created_date: str = None,
        application_name: str = None,
        name: str = None,
        environment: str = None,
        create_type: str = None,
        scaling_group_id: str = None,
        import_cluster_id: str = None,
    ):
        self.deploy_region_id = deploy_region_id
        self.description = description
        self.updated_date = updated_date
        self.created_date = created_date
        self.application_name = application_name
        self.name = name
        self.environment = environment
        self.create_type = create_type
        self.scaling_group_id = scaling_group_id
        self.import_cluster_id = import_cluster_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.deploy_region_id is not None:
            result['DeployRegionId'] = self.deploy_region_id
        if self.description is not None:
            result['Description'] = self.description
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.application_name is not None:
            result['ApplicationName'] = self.application_name
        if self.name is not None:
            result['Name'] = self.name
        if self.environment is not None:
            result['Environment'] = self.environment
        if self.create_type is not None:
            result['CreateType'] = self.create_type
        if self.scaling_group_id is not None:
            result['ScalingGroupId'] = self.scaling_group_id
        if self.import_cluster_id is not None:
            result['ImportClusterId'] = self.import_cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DeployRegionId') is not None:
            self.deploy_region_id = m.get('DeployRegionId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ApplicationName') is not None:
            self.application_name = m.get('ApplicationName')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Environment') is not None:
            self.environment = m.get('Environment')
        if m.get('CreateType') is not None:
            self.create_type = m.get('CreateType')
        if m.get('ScalingGroupId') is not None:
            self.scaling_group_id = m.get('ScalingGroupId')
        if m.get('ImportClusterId') is not None:
            self.import_cluster_id = m.get('ImportClusterId')
        return self


class GetApplicationGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        application_group: GetApplicationGroupResponseBodyApplicationGroup = None,
    ):
        self.request_id = request_id
        self.application_group = application_group

    def validate(self):
        if self.application_group:
            self.application_group.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.application_group is not None:
            result['ApplicationGroup'] = self.application_group.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ApplicationGroup') is not None:
            temp_model = GetApplicationGroupResponseBodyApplicationGroup()
            self.application_group = temp_model.from_map(m['ApplicationGroup'])
        return self


class GetApplicationGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetApplicationGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetApplicationGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetExecutionTemplateRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        execution_id: str = None,
    ):
        self.region_id = region_id
        self.execution_id = execution_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        return self


class GetExecutionTemplateResponseBodyTemplate(TeaModel):
    def __init__(
        self,
        hash: str = None,
        updated_date: str = None,
        updated_by: str = None,
        tags: Dict[str, Any] = None,
        template_name: str = None,
        template_version: str = None,
        template_format: str = None,
        description: str = None,
        created_by: str = None,
        created_date: str = None,
        template_id: str = None,
        share_type: str = None,
    ):
        self.hash = hash
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.tags = tags
        self.template_name = template_name
        self.template_version = template_version
        self.template_format = template_format
        self.description = description
        self.created_by = created_by
        self.created_date = created_date
        self.template_id = template_id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.hash is not None:
            result['Hash'] = self.hash
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.template_format is not None:
            result['TemplateFormat'] = self.template_format
        if self.description is not None:
            result['Description'] = self.description
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Hash') is not None:
            self.hash = m.get('Hash')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('TemplateFormat') is not None:
            self.template_format = m.get('TemplateFormat')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class GetExecutionTemplateResponseBody(TeaModel):
    def __init__(
        self,
        content: str = None,
        request_id: str = None,
        template: GetExecutionTemplateResponseBodyTemplate = None,
    ):
        self.content = content
        self.request_id = request_id
        self.template = template

    def validate(self):
        if self.template:
            self.template.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['Content'] = self.content
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.template is not None:
            result['Template'] = self.template.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Template') is not None:
            temp_model = GetExecutionTemplateResponseBodyTemplate()
            self.template = temp_model.from_map(m['Template'])
        return self


class GetExecutionTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetExecutionTemplateResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetExecutionTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetInventorySchemaRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        aggregator: bool = None,
        type_name: str = None,
        max_results: int = None,
        next_token: str = None,
    ):
        self.region_id = region_id
        self.aggregator = aggregator
        self.type_name = type_name
        self.max_results = max_results
        self.next_token = next_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.aggregator is not None:
            result['Aggregator'] = self.aggregator
        if self.type_name is not None:
            result['TypeName'] = self.type_name
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Aggregator') is not None:
            self.aggregator = m.get('Aggregator')
        if m.get('TypeName') is not None:
            self.type_name = m.get('TypeName')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        return self


class GetInventorySchemaResponseBodySchemasAttributes(TeaModel):
    def __init__(
        self,
        name: str = None,
        data_type: str = None,
    ):
        self.name = name
        self.data_type = data_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.data_type is not None:
            result['DataType'] = self.data_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('DataType') is not None:
            self.data_type = m.get('DataType')
        return self


class GetInventorySchemaResponseBodySchemas(TeaModel):
    def __init__(
        self,
        version: str = None,
        type_name: str = None,
        attributes: List[GetInventorySchemaResponseBodySchemasAttributes] = None,
    ):
        self.version = version
        self.type_name = type_name
        self.attributes = attributes

    def validate(self):
        if self.attributes:
            for k in self.attributes:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.version is not None:
            result['Version'] = self.version
        if self.type_name is not None:
            result['TypeName'] = self.type_name
        result['Attributes'] = []
        if self.attributes is not None:
            for k in self.attributes:
                result['Attributes'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('TypeName') is not None:
            self.type_name = m.get('TypeName')
        self.attributes = []
        if m.get('Attributes') is not None:
            for k in m.get('Attributes'):
                temp_model = GetInventorySchemaResponseBodySchemasAttributes()
                self.attributes.append(temp_model.from_map(k))
        return self


class GetInventorySchemaResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: str = None,
        schemas: List[GetInventorySchemaResponseBodySchemas] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.schemas = schemas

    def validate(self):
        if self.schemas:
            for k in self.schemas:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['Schemas'] = []
        if self.schemas is not None:
            for k in self.schemas:
                result['Schemas'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.schemas = []
        if m.get('Schemas') is not None:
            for k in m.get('Schemas'):
                temp_model = GetInventorySchemaResponseBodySchemas()
                self.schemas.append(temp_model.from_map(k))
        return self


class GetInventorySchemaResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetInventorySchemaResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetInventorySchemaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetParameterRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        parameter_version: int = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.parameter_version = parameter_version
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class GetParameterResponseBodyParameter(TeaModel):
    def __init__(
        self,
        type: str = None,
        updated_date: str = None,
        updated_by: str = None,
        tags: Dict[str, Any] = None,
        value: str = None,
        description: str = None,
        constraints: str = None,
        resource_group_id: str = None,
        created_by: str = None,
        created_date: str = None,
        parameter_version: int = None,
        name: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.type = type
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.tags = tags
        self.value = value
        self.description = description
        self.constraints = constraints
        self.resource_group_id = resource_group_id
        self.created_by = created_by
        self.created_date = created_date
        self.parameter_version = parameter_version
        self.name = name
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.value is not None:
            result['Value'] = self.value
        if self.description is not None:
            result['Description'] = self.description
        if self.constraints is not None:
            result['Constraints'] = self.constraints
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Constraints') is not None:
            self.constraints = m.get('Constraints')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class GetParameterResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        parameter: GetParameterResponseBodyParameter = None,
    ):
        self.request_id = request_id
        self.parameter = parameter

    def validate(self):
        if self.parameter:
            self.parameter.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.parameter is not None:
            result['Parameter'] = self.parameter.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Parameter') is not None:
            temp_model = GetParameterResponseBodyParameter()
            self.parameter = temp_model.from_map(m['Parameter'])
        return self


class GetParameterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetParameterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetParameterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetParametersRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        names: str = None,
    ):
        self.region_id = region_id
        self.names = names

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.names is not None:
            result['Names'] = self.names
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Names') is not None:
            self.names = m.get('Names')
        return self


class GetParametersResponseBodyParameters(TeaModel):
    def __init__(
        self,
        type: str = None,
        updated_date: str = None,
        updated_by: str = None,
        tags: Dict[str, Any] = None,
        value: str = None,
        description: str = None,
        constraints: str = None,
        resource_group_id: str = None,
        created_by: str = None,
        created_date: str = None,
        parameter_version: int = None,
        name: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.type = type
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.tags = tags
        self.value = value
        self.description = description
        self.constraints = constraints
        self.resource_group_id = resource_group_id
        self.created_by = created_by
        self.created_date = created_date
        self.parameter_version = parameter_version
        self.name = name
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.value is not None:
            result['Value'] = self.value
        if self.description is not None:
            result['Description'] = self.description
        if self.constraints is not None:
            result['Constraints'] = self.constraints
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Constraints') is not None:
            self.constraints = m.get('Constraints')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class GetParametersResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        invalid_parameters: List[str] = None,
        parameters: List[GetParametersResponseBodyParameters] = None,
    ):
        self.request_id = request_id
        self.invalid_parameters = invalid_parameters
        self.parameters = parameters

    def validate(self):
        if self.parameters:
            for k in self.parameters:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.invalid_parameters is not None:
            result['InvalidParameters'] = self.invalid_parameters
        result['Parameters'] = []
        if self.parameters is not None:
            for k in self.parameters:
                result['Parameters'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('InvalidParameters') is not None:
            self.invalid_parameters = m.get('InvalidParameters')
        self.parameters = []
        if m.get('Parameters') is not None:
            for k in m.get('Parameters'):
                temp_model = GetParametersResponseBodyParameters()
                self.parameters.append(temp_model.from_map(k))
        return self


class GetParametersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetParametersResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetParametersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetParametersByPathRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        path: str = None,
        recursive: bool = None,
        next_token: str = None,
        max_results: int = None,
    ):
        self.region_id = region_id
        self.path = path
        self.recursive = recursive
        self.next_token = next_token
        self.max_results = max_results

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.path is not None:
            result['Path'] = self.path
        if self.recursive is not None:
            result['Recursive'] = self.recursive
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Path') is not None:
            self.path = m.get('Path')
        if m.get('Recursive') is not None:
            self.recursive = m.get('Recursive')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        return self


class GetParametersByPathResponseBodyParameters(TeaModel):
    def __init__(
        self,
        type: str = None,
        updated_date: str = None,
        updated_by: str = None,
        value: str = None,
        description: str = None,
        constraints: str = None,
        created_by: str = None,
        created_date: str = None,
        parameter_version: int = None,
        name: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.type = type
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.value = value
        self.description = description
        self.constraints = constraints
        self.created_by = created_by
        self.created_date = created_date
        self.parameter_version = parameter_version
        self.name = name
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.value is not None:
            result['Value'] = self.value
        if self.description is not None:
            result['Description'] = self.description
        if self.constraints is not None:
            result['Constraints'] = self.constraints
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Constraints') is not None:
            self.constraints = m.get('Constraints')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class GetParametersByPathResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        total_count: int = None,
        max_results: int = None,
        parameters: List[GetParametersByPathResponseBodyParameters] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.total_count = total_count
        self.max_results = max_results
        self.parameters = parameters

    def validate(self):
        if self.parameters:
            for k in self.parameters:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['Parameters'] = []
        if self.parameters is not None:
            for k in self.parameters:
                result['Parameters'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.parameters = []
        if m.get('Parameters') is not None:
            for k in m.get('Parameters'):
                temp_model = GetParametersByPathResponseBodyParameters()
                self.parameters.append(temp_model.from_map(k))
        return self


class GetParametersByPathResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetParametersByPathResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetParametersByPathResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetPatchBaselineRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
    ):
        self.region_id = region_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class GetPatchBaselineResponseBodyPatchBaseline(TeaModel):
    def __init__(
        self,
        operation_system: str = None,
        is_default: bool = None,
        description: str = None,
        updated_date: str = None,
        updated_by: str = None,
        created_by: str = None,
        created_date: str = None,
        name: str = None,
        approval_rules: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.operation_system = operation_system
        self.is_default = is_default
        self.description = description
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.created_by = created_by
        self.created_date = created_date
        self.name = name
        self.approval_rules = approval_rules
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.operation_system is not None:
            result['OperationSystem'] = self.operation_system
        if self.is_default is not None:
            result['IsDefault'] = self.is_default
        if self.description is not None:
            result['Description'] = self.description
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.name is not None:
            result['Name'] = self.name
        if self.approval_rules is not None:
            result['ApprovalRules'] = self.approval_rules
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OperationSystem') is not None:
            self.operation_system = m.get('OperationSystem')
        if m.get('IsDefault') is not None:
            self.is_default = m.get('IsDefault')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ApprovalRules') is not None:
            self.approval_rules = m.get('ApprovalRules')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class GetPatchBaselineResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        patch_baseline: GetPatchBaselineResponseBodyPatchBaseline = None,
    ):
        self.request_id = request_id
        self.patch_baseline = patch_baseline

    def validate(self):
        if self.patch_baseline:
            self.patch_baseline.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.patch_baseline is not None:
            result['PatchBaseline'] = self.patch_baseline.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PatchBaseline') is not None:
            temp_model = GetPatchBaselineResponseBodyPatchBaseline()
            self.patch_baseline = temp_model.from_map(m['PatchBaseline'])
        return self


class GetPatchBaselineResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetPatchBaselineResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetPatchBaselineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetSecretParameterRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        parameter_version: int = None,
        with_decryption: bool = None,
    ):
        self.region_id = region_id
        self.name = name
        self.parameter_version = parameter_version
        self.with_decryption = with_decryption

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.with_decryption is not None:
            result['WithDecryption'] = self.with_decryption
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('WithDecryption') is not None:
            self.with_decryption = m.get('WithDecryption')
        return self


class GetSecretParameterResponseBodyParameter(TeaModel):
    def __init__(
        self,
        type: str = None,
        updated_date: str = None,
        updated_by: str = None,
        key_id: str = None,
        tags: Dict[str, Any] = None,
        value: str = None,
        description: str = None,
        constraints: str = None,
        resource_group_id: str = None,
        created_by: str = None,
        created_date: str = None,
        parameter_version: int = None,
        name: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.type = type
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.key_id = key_id
        self.tags = tags
        self.value = value
        self.description = description
        self.constraints = constraints
        self.resource_group_id = resource_group_id
        self.created_by = created_by
        self.created_date = created_date
        self.parameter_version = parameter_version
        self.name = name
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.key_id is not None:
            result['KeyId'] = self.key_id
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.value is not None:
            result['Value'] = self.value
        if self.description is not None:
            result['Description'] = self.description
        if self.constraints is not None:
            result['Constraints'] = self.constraints
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('KeyId') is not None:
            self.key_id = m.get('KeyId')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Constraints') is not None:
            self.constraints = m.get('Constraints')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class GetSecretParameterResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        parameter: GetSecretParameterResponseBodyParameter = None,
    ):
        self.request_id = request_id
        self.parameter = parameter

    def validate(self):
        if self.parameter:
            self.parameter.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.parameter is not None:
            result['Parameter'] = self.parameter.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Parameter') is not None:
            temp_model = GetSecretParameterResponseBodyParameter()
            self.parameter = temp_model.from_map(m['Parameter'])
        return self


class GetSecretParameterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetSecretParameterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetSecretParameterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetSecretParametersRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        names: str = None,
        with_decryption: bool = None,
    ):
        self.region_id = region_id
        self.names = names
        self.with_decryption = with_decryption

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.names is not None:
            result['Names'] = self.names
        if self.with_decryption is not None:
            result['WithDecryption'] = self.with_decryption
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Names') is not None:
            self.names = m.get('Names')
        if m.get('WithDecryption') is not None:
            self.with_decryption = m.get('WithDecryption')
        return self


class GetSecretParametersResponseBodyParameters(TeaModel):
    def __init__(
        self,
        type: str = None,
        updated_date: str = None,
        updated_by: str = None,
        key_id: str = None,
        tags: Dict[str, Any] = None,
        value: str = None,
        description: str = None,
        constraints: str = None,
        resource_group_id: str = None,
        created_by: str = None,
        created_date: str = None,
        parameter_version: int = None,
        name: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.type = type
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.key_id = key_id
        self.tags = tags
        self.value = value
        self.description = description
        self.constraints = constraints
        self.resource_group_id = resource_group_id
        self.created_by = created_by
        self.created_date = created_date
        self.parameter_version = parameter_version
        self.name = name
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.key_id is not None:
            result['KeyId'] = self.key_id
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.value is not None:
            result['Value'] = self.value
        if self.description is not None:
            result['Description'] = self.description
        if self.constraints is not None:
            result['Constraints'] = self.constraints
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('KeyId') is not None:
            self.key_id = m.get('KeyId')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Constraints') is not None:
            self.constraints = m.get('Constraints')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class GetSecretParametersResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        invalid_parameters: List[str] = None,
        parameters: List[GetSecretParametersResponseBodyParameters] = None,
    ):
        self.request_id = request_id
        self.invalid_parameters = invalid_parameters
        self.parameters = parameters

    def validate(self):
        if self.parameters:
            for k in self.parameters:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.invalid_parameters is not None:
            result['InvalidParameters'] = self.invalid_parameters
        result['Parameters'] = []
        if self.parameters is not None:
            for k in self.parameters:
                result['Parameters'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('InvalidParameters') is not None:
            self.invalid_parameters = m.get('InvalidParameters')
        self.parameters = []
        if m.get('Parameters') is not None:
            for k in m.get('Parameters'):
                temp_model = GetSecretParametersResponseBodyParameters()
                self.parameters.append(temp_model.from_map(k))
        return self


class GetSecretParametersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetSecretParametersResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetSecretParametersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetSecretParametersByPathRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        path: str = None,
        recursive: bool = None,
        next_token: str = None,
        max_results: int = None,
        with_decryption: bool = None,
    ):
        self.region_id = region_id
        self.path = path
        self.recursive = recursive
        self.next_token = next_token
        self.max_results = max_results
        self.with_decryption = with_decryption

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.path is not None:
            result['Path'] = self.path
        if self.recursive is not None:
            result['Recursive'] = self.recursive
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.with_decryption is not None:
            result['WithDecryption'] = self.with_decryption
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Path') is not None:
            self.path = m.get('Path')
        if m.get('Recursive') is not None:
            self.recursive = m.get('Recursive')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('WithDecryption') is not None:
            self.with_decryption = m.get('WithDecryption')
        return self


class GetSecretParametersByPathResponseBodyParameters(TeaModel):
    def __init__(
        self,
        type: str = None,
        updated_date: str = None,
        updated_by: str = None,
        key_id: str = None,
        value: str = None,
        description: str = None,
        constraints: str = None,
        created_by: str = None,
        created_date: str = None,
        parameter_version: int = None,
        name: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.type = type
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.key_id = key_id
        self.value = value
        self.description = description
        self.constraints = constraints
        self.created_by = created_by
        self.created_date = created_date
        self.parameter_version = parameter_version
        self.name = name
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.key_id is not None:
            result['KeyId'] = self.key_id
        if self.value is not None:
            result['Value'] = self.value
        if self.description is not None:
            result['Description'] = self.description
        if self.constraints is not None:
            result['Constraints'] = self.constraints
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('KeyId') is not None:
            self.key_id = m.get('KeyId')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Constraints') is not None:
            self.constraints = m.get('Constraints')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class GetSecretParametersByPathResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        total_count: int = None,
        max_results: int = None,
        parameters: List[GetSecretParametersByPathResponseBodyParameters] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.total_count = total_count
        self.max_results = max_results
        self.parameters = parameters

    def validate(self):
        if self.parameters:
            for k in self.parameters:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['Parameters'] = []
        if self.parameters is not None:
            for k in self.parameters:
                result['Parameters'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.parameters = []
        if m.get('Parameters') is not None:
            for k in m.get('Parameters'):
                temp_model = GetSecretParametersByPathResponseBodyParameters()
                self.parameters.append(temp_model.from_map(k))
        return self


class GetSecretParametersByPathResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetSecretParametersByPathResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetSecretParametersByPathResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetServiceSettingsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
    ):
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class GetServiceSettingsResponseBodyServiceSettings(TeaModel):
    def __init__(
        self,
        delivery_oss_bucket_name: str = None,
        delivery_oss_key_prefix: str = None,
        delivery_oss_enabled: bool = None,
        delivery_sls_enabled: bool = None,
        delivery_sls_project_name: str = None,
        rdc_enterprise_id: str = None,
    ):
        self.delivery_oss_bucket_name = delivery_oss_bucket_name
        self.delivery_oss_key_prefix = delivery_oss_key_prefix
        self.delivery_oss_enabled = delivery_oss_enabled
        self.delivery_sls_enabled = delivery_sls_enabled
        self.delivery_sls_project_name = delivery_sls_project_name
        self.rdc_enterprise_id = rdc_enterprise_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.delivery_oss_bucket_name is not None:
            result['DeliveryOssBucketName'] = self.delivery_oss_bucket_name
        if self.delivery_oss_key_prefix is not None:
            result['DeliveryOssKeyPrefix'] = self.delivery_oss_key_prefix
        if self.delivery_oss_enabled is not None:
            result['DeliveryOssEnabled'] = self.delivery_oss_enabled
        if self.delivery_sls_enabled is not None:
            result['DeliverySlsEnabled'] = self.delivery_sls_enabled
        if self.delivery_sls_project_name is not None:
            result['DeliverySlsProjectName'] = self.delivery_sls_project_name
        if self.rdc_enterprise_id is not None:
            result['RdcEnterpriseId'] = self.rdc_enterprise_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DeliveryOssBucketName') is not None:
            self.delivery_oss_bucket_name = m.get('DeliveryOssBucketName')
        if m.get('DeliveryOssKeyPrefix') is not None:
            self.delivery_oss_key_prefix = m.get('DeliveryOssKeyPrefix')
        if m.get('DeliveryOssEnabled') is not None:
            self.delivery_oss_enabled = m.get('DeliveryOssEnabled')
        if m.get('DeliverySlsEnabled') is not None:
            self.delivery_sls_enabled = m.get('DeliverySlsEnabled')
        if m.get('DeliverySlsProjectName') is not None:
            self.delivery_sls_project_name = m.get('DeliverySlsProjectName')
        if m.get('RdcEnterpriseId') is not None:
            self.rdc_enterprise_id = m.get('RdcEnterpriseId')
        return self


class GetServiceSettingsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        service_settings: List[GetServiceSettingsResponseBodyServiceSettings] = None,
    ):
        self.request_id = request_id
        self.service_settings = service_settings

    def validate(self):
        if self.service_settings:
            for k in self.service_settings:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['ServiceSettings'] = []
        if self.service_settings is not None:
            for k in self.service_settings:
                result['ServiceSettings'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.service_settings = []
        if m.get('ServiceSettings') is not None:
            for k in m.get('ServiceSettings'):
                temp_model = GetServiceSettingsResponseBodyServiceSettings()
                self.service_settings.append(temp_model.from_map(k))
        return self


class GetServiceSettingsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetServiceSettingsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetServiceSettingsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTemplateRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        template_version: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.template_version = template_version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        return self


class GetTemplateResponseBodyTemplate(TeaModel):
    def __init__(
        self,
        hash: str = None,
        updated_date: str = None,
        updated_by: str = None,
        template_type: str = None,
        tags: Dict[str, Any] = None,
        template_name: str = None,
        template_version: str = None,
        template_format: str = None,
        description: str = None,
        resource_group_id: str = None,
        created_by: str = None,
        created_date: str = None,
        version_name: str = None,
        template_id: str = None,
        has_trigger: bool = None,
        share_type: str = None,
    ):
        self.hash = hash
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.template_type = template_type
        self.tags = tags
        self.template_name = template_name
        self.template_version = template_version
        self.template_format = template_format
        self.description = description
        self.resource_group_id = resource_group_id
        self.created_by = created_by
        self.created_date = created_date
        self.version_name = version_name
        self.template_id = template_id
        self.has_trigger = has_trigger
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.hash is not None:
            result['Hash'] = self.hash
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.template_type is not None:
            result['TemplateType'] = self.template_type
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.template_format is not None:
            result['TemplateFormat'] = self.template_format
        if self.description is not None:
            result['Description'] = self.description
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.version_name is not None:
            result['VersionName'] = self.version_name
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        if self.has_trigger is not None:
            result['HasTrigger'] = self.has_trigger
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Hash') is not None:
            self.hash = m.get('Hash')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('TemplateType') is not None:
            self.template_type = m.get('TemplateType')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('TemplateFormat') is not None:
            self.template_format = m.get('TemplateFormat')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('VersionName') is not None:
            self.version_name = m.get('VersionName')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        if m.get('HasTrigger') is not None:
            self.has_trigger = m.get('HasTrigger')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class GetTemplateResponseBody(TeaModel):
    def __init__(
        self,
        content: str = None,
        request_id: str = None,
        template: GetTemplateResponseBodyTemplate = None,
    ):
        self.content = content
        self.request_id = request_id
        self.template = template

    def validate(self):
        if self.template:
            self.template.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['Content'] = self.content
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.template is not None:
            result['Template'] = self.template.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Template') is not None:
            temp_model = GetTemplateResponseBodyTemplate()
            self.template = temp_model.from_map(m['Template'])
        return self


class GetTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetTemplateResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListActionsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        oosaction_name: str = None,
        max_results: int = None,
        next_token: str = None,
    ):
        self.region_id = region_id
        self.oosaction_name = oosaction_name
        self.max_results = max_results
        self.next_token = next_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.oosaction_name is not None:
            result['OOSActionName'] = self.oosaction_name
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('OOSActionName') is not None:
            self.oosaction_name = m.get('OOSActionName')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        return self


class ListActionsResponseBodyActions(TeaModel):
    def __init__(
        self,
        popularity: int = None,
        action_type: str = None,
        description: str = None,
        created_date: str = None,
        template_version: str = None,
        oosaction_name: str = None,
        properties: str = None,
    ):
        self.popularity = popularity
        self.action_type = action_type
        self.description = description
        self.created_date = created_date
        self.template_version = template_version
        self.oosaction_name = oosaction_name
        self.properties = properties

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.popularity is not None:
            result['Popularity'] = self.popularity
        if self.action_type is not None:
            result['ActionType'] = self.action_type
        if self.description is not None:
            result['Description'] = self.description
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.oosaction_name is not None:
            result['OOSActionName'] = self.oosaction_name
        if self.properties is not None:
            result['Properties'] = self.properties
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Popularity') is not None:
            self.popularity = m.get('Popularity')
        if m.get('ActionType') is not None:
            self.action_type = m.get('ActionType')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('OOSActionName') is not None:
            self.oosaction_name = m.get('OOSActionName')
        if m.get('Properties') is not None:
            self.properties = m.get('Properties')
        return self


class ListActionsResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        actions: List[ListActionsResponseBodyActions] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.actions = actions

    def validate(self):
        if self.actions:
            for k in self.actions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['Actions'] = []
        if self.actions is not None:
            for k in self.actions:
                result['Actions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.actions = []
        if m.get('Actions') is not None:
            for k in m.get('Actions'):
                temp_model = ListActionsResponseBodyActions()
                self.actions.append(temp_model.from_map(k))
        return self


class ListActionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListActionsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListActionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListApplicationGroupsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        application_name: str = None,
        deploy_region_id: bool = None,
        environment: bool = None,
        max_results: int = None,
        next_token: str = None,
    ):
        self.region_id = region_id
        self.application_name = application_name
        self.deploy_region_id = deploy_region_id
        self.environment = environment
        self.max_results = max_results
        self.next_token = next_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.application_name is not None:
            result['ApplicationName'] = self.application_name
        if self.deploy_region_id is not None:
            result['DeployRegionId'] = self.deploy_region_id
        if self.environment is not None:
            result['Environment'] = self.environment
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ApplicationName') is not None:
            self.application_name = m.get('ApplicationName')
        if m.get('DeployRegionId') is not None:
            self.deploy_region_id = m.get('DeployRegionId')
        if m.get('Environment') is not None:
            self.environment = m.get('Environment')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        return self


class ListApplicationGroupsResponseBodyApplicationGroups(TeaModel):
    def __init__(
        self,
        deploy_region_id: str = None,
        description: str = None,
        updated_date: str = None,
        created_date: str = None,
        application_name: str = None,
        name: str = None,
        environment: str = None,
        create_type: str = None,
        scaling_group_id: str = None,
        import_cluster_id: str = None,
    ):
        self.deploy_region_id = deploy_region_id
        self.description = description
        self.updated_date = updated_date
        self.created_date = created_date
        self.application_name = application_name
        self.name = name
        self.environment = environment
        self.create_type = create_type
        self.scaling_group_id = scaling_group_id
        self.import_cluster_id = import_cluster_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.deploy_region_id is not None:
            result['DeployRegionId'] = self.deploy_region_id
        if self.description is not None:
            result['Description'] = self.description
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.application_name is not None:
            result['ApplicationName'] = self.application_name
        if self.name is not None:
            result['Name'] = self.name
        if self.environment is not None:
            result['Environment'] = self.environment
        if self.create_type is not None:
            result['CreateType'] = self.create_type
        if self.scaling_group_id is not None:
            result['ScalingGroupId'] = self.scaling_group_id
        if self.import_cluster_id is not None:
            result['ImportClusterId'] = self.import_cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DeployRegionId') is not None:
            self.deploy_region_id = m.get('DeployRegionId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ApplicationName') is not None:
            self.application_name = m.get('ApplicationName')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Environment') is not None:
            self.environment = m.get('Environment')
        if m.get('CreateType') is not None:
            self.create_type = m.get('CreateType')
        if m.get('ScalingGroupId') is not None:
            self.scaling_group_id = m.get('ScalingGroupId')
        if m.get('ImportClusterId') is not None:
            self.import_cluster_id = m.get('ImportClusterId')
        return self


class ListApplicationGroupsResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        application_groups: List[ListApplicationGroupsResponseBodyApplicationGroups] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.application_groups = application_groups

    def validate(self):
        if self.application_groups:
            for k in self.application_groups:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['ApplicationGroups'] = []
        if self.application_groups is not None:
            for k in self.application_groups:
                result['ApplicationGroups'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.application_groups = []
        if m.get('ApplicationGroups') is not None:
            for k in m.get('ApplicationGroups'):
                temp_model = ListApplicationGroupsResponseBodyApplicationGroups()
                self.application_groups.append(temp_model.from_map(k))
        return self


class ListApplicationGroupsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListApplicationGroupsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListApplicationGroupsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListApplicationsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        is_system: bool = None,
        max_results: int = None,
        next_token: str = None,
    ):
        self.region_id = region_id
        self.is_system = is_system
        self.max_results = max_results
        self.next_token = next_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.is_system is not None:
            result['IsSystem'] = self.is_system
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('IsSystem') is not None:
            self.is_system = m.get('IsSystem')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        return self


class ListApplicationsResponseBodyApplicationsCloudMonitorRule(TeaModel):
    def __init__(
        self,
        enable_subscribe_event: bool = None,
        enable_install_agent: bool = None,
        enabled: bool = None,
        contact_group_list: List[str] = None,
        template_id_list: List[int] = None,
    ):
        self.enable_subscribe_event = enable_subscribe_event
        self.enable_install_agent = enable_install_agent
        self.enabled = enabled
        self.contact_group_list = contact_group_list
        self.template_id_list = template_id_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enable_subscribe_event is not None:
            result['EnableSubscribeEvent'] = self.enable_subscribe_event
        if self.enable_install_agent is not None:
            result['EnableInstallAgent'] = self.enable_install_agent
        if self.enabled is not None:
            result['Enabled'] = self.enabled
        if self.contact_group_list is not None:
            result['ContactGroupList'] = self.contact_group_list
        if self.template_id_list is not None:
            result['TemplateIdList'] = self.template_id_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EnableSubscribeEvent') is not None:
            self.enable_subscribe_event = m.get('EnableSubscribeEvent')
        if m.get('EnableInstallAgent') is not None:
            self.enable_install_agent = m.get('EnableInstallAgent')
        if m.get('Enabled') is not None:
            self.enabled = m.get('Enabled')
        if m.get('ContactGroupList') is not None:
            self.contact_group_list = m.get('ContactGroupList')
        if m.get('TemplateIdList') is not None:
            self.template_id_list = m.get('TemplateIdList')
        return self


class ListApplicationsResponseBodyApplications(TeaModel):
    def __init__(
        self,
        type: str = None,
        is_system: bool = None,
        description: str = None,
        update_date: str = None,
        resource_group_id: str = None,
        created_date: str = None,
        name: str = None,
        cloud_monitor_rule: ListApplicationsResponseBodyApplicationsCloudMonitorRule = None,
    ):
        self.type = type
        self.is_system = is_system
        self.description = description
        self.update_date = update_date
        self.resource_group_id = resource_group_id
        self.created_date = created_date
        self.name = name
        self.cloud_monitor_rule = cloud_monitor_rule

    def validate(self):
        if self.cloud_monitor_rule:
            self.cloud_monitor_rule.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.is_system is not None:
            result['IsSystem'] = self.is_system
        if self.description is not None:
            result['Description'] = self.description
        if self.update_date is not None:
            result['UpdateDate'] = self.update_date
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.name is not None:
            result['Name'] = self.name
        if self.cloud_monitor_rule is not None:
            result['CloudMonitorRule'] = self.cloud_monitor_rule.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('IsSystem') is not None:
            self.is_system = m.get('IsSystem')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('UpdateDate') is not None:
            self.update_date = m.get('UpdateDate')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('CloudMonitorRule') is not None:
            temp_model = ListApplicationsResponseBodyApplicationsCloudMonitorRule()
            self.cloud_monitor_rule = temp_model.from_map(m['CloudMonitorRule'])
        return self


class ListApplicationsResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        applications: List[ListApplicationsResponseBodyApplications] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.applications = applications

    def validate(self):
        if self.applications:
            for k in self.applications:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['Applications'] = []
        if self.applications is not None:
            for k in self.applications:
                result['Applications'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.applications = []
        if m.get('Applications') is not None:
            for k in m.get('Applications'):
                temp_model = ListApplicationsResponseBodyApplications()
                self.applications.append(temp_model.from_map(k))
        return self


class ListApplicationsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListApplicationsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListApplicationsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListExecutionLogsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        execution_id: str = None,
        task_execution_id: str = None,
        log_type: str = None,
        max_results: int = None,
        next_token: str = None,
    ):
        self.region_id = region_id
        self.execution_id = execution_id
        self.task_execution_id = task_execution_id
        self.log_type = log_type
        self.max_results = max_results
        self.next_token = next_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        if self.task_execution_id is not None:
            result['TaskExecutionId'] = self.task_execution_id
        if self.log_type is not None:
            result['LogType'] = self.log_type
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        if m.get('TaskExecutionId') is not None:
            self.task_execution_id = m.get('TaskExecutionId')
        if m.get('LogType') is not None:
            self.log_type = m.get('LogType')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        return self


class ListExecutionLogsResponseBodyExecutionLogs(TeaModel):
    def __init__(
        self,
        task_execution_id: str = None,
        message: str = None,
        log_type: str = None,
        timestamp: str = None,
    ):
        self.task_execution_id = task_execution_id
        self.message = message
        self.log_type = log_type
        self.timestamp = timestamp

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.task_execution_id is not None:
            result['TaskExecutionId'] = self.task_execution_id
        if self.message is not None:
            result['Message'] = self.message
        if self.log_type is not None:
            result['LogType'] = self.log_type
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskExecutionId') is not None:
            self.task_execution_id = m.get('TaskExecutionId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('LogType') is not None:
            self.log_type = m.get('LogType')
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        return self


class ListExecutionLogsResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        is_truncated: bool = None,
        max_results: int = None,
        execution_logs: List[ListExecutionLogsResponseBodyExecutionLogs] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.is_truncated = is_truncated
        self.max_results = max_results
        self.execution_logs = execution_logs

    def validate(self):
        if self.execution_logs:
            for k in self.execution_logs:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.is_truncated is not None:
            result['IsTruncated'] = self.is_truncated
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['ExecutionLogs'] = []
        if self.execution_logs is not None:
            for k in self.execution_logs:
                result['ExecutionLogs'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('IsTruncated') is not None:
            self.is_truncated = m.get('IsTruncated')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.execution_logs = []
        if m.get('ExecutionLogs') is not None:
            for k in m.get('ExecutionLogs'):
                temp_model = ListExecutionLogsResponseBodyExecutionLogs()
                self.execution_logs.append(temp_model.from_map(k))
        return self


class ListExecutionLogsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListExecutionLogsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListExecutionLogsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListExecutionRiskyTasksRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        return self


class ListExecutionRiskyTasksResponseBodyRiskyTasks(TeaModel):
    def __init__(
        self,
        service: str = None,
        api: str = None,
        task: List[str] = None,
        template: List[str] = None,
    ):
        self.service = service
        self.api = api
        self.task = task
        self.template = template

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.service is not None:
            result['Service'] = self.service
        if self.api is not None:
            result['API'] = self.api
        if self.task is not None:
            result['Task'] = self.task
        if self.template is not None:
            result['Template'] = self.template
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Service') is not None:
            self.service = m.get('Service')
        if m.get('API') is not None:
            self.api = m.get('API')
        if m.get('Task') is not None:
            self.task = m.get('Task')
        if m.get('Template') is not None:
            self.template = m.get('Template')
        return self


class ListExecutionRiskyTasksResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        risky_tasks: List[ListExecutionRiskyTasksResponseBodyRiskyTasks] = None,
    ):
        self.request_id = request_id
        self.risky_tasks = risky_tasks

    def validate(self):
        if self.risky_tasks:
            for k in self.risky_tasks:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['RiskyTasks'] = []
        if self.risky_tasks is not None:
            for k in self.risky_tasks:
                result['RiskyTasks'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.risky_tasks = []
        if m.get('RiskyTasks') is not None:
            for k in m.get('RiskyTasks'):
                temp_model = ListExecutionRiskyTasksResponseBodyRiskyTasks()
                self.risky_tasks.append(temp_model.from_map(k))
        return self


class ListExecutionRiskyTasksResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListExecutionRiskyTasksResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListExecutionRiskyTasksResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListExecutionsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        status: str = None,
        execution_id: str = None,
        start_date_before: str = None,
        start_date_after: str = None,
        end_date_before: str = None,
        end_date_after: str = None,
        mode: str = None,
        executed_by: str = None,
        parent_execution_id: str = None,
        ram_role: str = None,
        include_child_execution: bool = None,
        category: str = None,
        tags: Dict[str, Any] = None,
        max_results: int = None,
        next_token: str = None,
        sort_field: str = None,
        sort_order: str = None,
        resource_id: str = None,
        resource_template_name: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.status = status
        self.execution_id = execution_id
        self.start_date_before = start_date_before
        self.start_date_after = start_date_after
        self.end_date_before = end_date_before
        self.end_date_after = end_date_after
        self.mode = mode
        self.executed_by = executed_by
        self.parent_execution_id = parent_execution_id
        self.ram_role = ram_role
        self.include_child_execution = include_child_execution
        self.category = category
        self.tags = tags
        self.max_results = max_results
        self.next_token = next_token
        self.sort_field = sort_field
        self.sort_order = sort_order
        self.resource_id = resource_id
        self.resource_template_name = resource_template_name
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.status is not None:
            result['Status'] = self.status
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        if self.start_date_before is not None:
            result['StartDateBefore'] = self.start_date_before
        if self.start_date_after is not None:
            result['StartDateAfter'] = self.start_date_after
        if self.end_date_before is not None:
            result['EndDateBefore'] = self.end_date_before
        if self.end_date_after is not None:
            result['EndDateAfter'] = self.end_date_after
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.executed_by is not None:
            result['ExecutedBy'] = self.executed_by
        if self.parent_execution_id is not None:
            result['ParentExecutionId'] = self.parent_execution_id
        if self.ram_role is not None:
            result['RamRole'] = self.ram_role
        if self.include_child_execution is not None:
            result['IncludeChildExecution'] = self.include_child_execution
        if self.category is not None:
            result['Category'] = self.category
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.sort_field is not None:
            result['SortField'] = self.sort_field
        if self.sort_order is not None:
            result['SortOrder'] = self.sort_order
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_template_name is not None:
            result['ResourceTemplateName'] = self.resource_template_name
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        if m.get('StartDateBefore') is not None:
            self.start_date_before = m.get('StartDateBefore')
        if m.get('StartDateAfter') is not None:
            self.start_date_after = m.get('StartDateAfter')
        if m.get('EndDateBefore') is not None:
            self.end_date_before = m.get('EndDateBefore')
        if m.get('EndDateAfter') is not None:
            self.end_date_after = m.get('EndDateAfter')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('ExecutedBy') is not None:
            self.executed_by = m.get('ExecutedBy')
        if m.get('ParentExecutionId') is not None:
            self.parent_execution_id = m.get('ParentExecutionId')
        if m.get('RamRole') is not None:
            self.ram_role = m.get('RamRole')
        if m.get('IncludeChildExecution') is not None:
            self.include_child_execution = m.get('IncludeChildExecution')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('SortField') is not None:
            self.sort_field = m.get('SortField')
        if m.get('SortOrder') is not None:
            self.sort_order = m.get('SortOrder')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceTemplateName') is not None:
            self.resource_template_name = m.get('ResourceTemplateName')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class ListExecutionsShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        status: str = None,
        execution_id: str = None,
        start_date_before: str = None,
        start_date_after: str = None,
        end_date_before: str = None,
        end_date_after: str = None,
        mode: str = None,
        executed_by: str = None,
        parent_execution_id: str = None,
        ram_role: str = None,
        include_child_execution: bool = None,
        category: str = None,
        tags_shrink: str = None,
        max_results: int = None,
        next_token: str = None,
        sort_field: str = None,
        sort_order: str = None,
        resource_id: str = None,
        resource_template_name: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.status = status
        self.execution_id = execution_id
        self.start_date_before = start_date_before
        self.start_date_after = start_date_after
        self.end_date_before = end_date_before
        self.end_date_after = end_date_after
        self.mode = mode
        self.executed_by = executed_by
        self.parent_execution_id = parent_execution_id
        self.ram_role = ram_role
        self.include_child_execution = include_child_execution
        self.category = category
        self.tags_shrink = tags_shrink
        self.max_results = max_results
        self.next_token = next_token
        self.sort_field = sort_field
        self.sort_order = sort_order
        self.resource_id = resource_id
        self.resource_template_name = resource_template_name
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.status is not None:
            result['Status'] = self.status
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        if self.start_date_before is not None:
            result['StartDateBefore'] = self.start_date_before
        if self.start_date_after is not None:
            result['StartDateAfter'] = self.start_date_after
        if self.end_date_before is not None:
            result['EndDateBefore'] = self.end_date_before
        if self.end_date_after is not None:
            result['EndDateAfter'] = self.end_date_after
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.executed_by is not None:
            result['ExecutedBy'] = self.executed_by
        if self.parent_execution_id is not None:
            result['ParentExecutionId'] = self.parent_execution_id
        if self.ram_role is not None:
            result['RamRole'] = self.ram_role
        if self.include_child_execution is not None:
            result['IncludeChildExecution'] = self.include_child_execution
        if self.category is not None:
            result['Category'] = self.category
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.sort_field is not None:
            result['SortField'] = self.sort_field
        if self.sort_order is not None:
            result['SortOrder'] = self.sort_order
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_template_name is not None:
            result['ResourceTemplateName'] = self.resource_template_name
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        if m.get('StartDateBefore') is not None:
            self.start_date_before = m.get('StartDateBefore')
        if m.get('StartDateAfter') is not None:
            self.start_date_after = m.get('StartDateAfter')
        if m.get('EndDateBefore') is not None:
            self.end_date_before = m.get('EndDateBefore')
        if m.get('EndDateAfter') is not None:
            self.end_date_after = m.get('EndDateAfter')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('ExecutedBy') is not None:
            self.executed_by = m.get('ExecutedBy')
        if m.get('ParentExecutionId') is not None:
            self.parent_execution_id = m.get('ParentExecutionId')
        if m.get('RamRole') is not None:
            self.ram_role = m.get('RamRole')
        if m.get('IncludeChildExecution') is not None:
            self.include_child_execution = m.get('IncludeChildExecution')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('SortField') is not None:
            self.sort_field = m.get('SortField')
        if m.get('SortOrder') is not None:
            self.sort_order = m.get('SortOrder')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceTemplateName') is not None:
            self.resource_template_name = m.get('ResourceTemplateName')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class ListExecutionsResponseBodyExecutionsCurrentTasks(TeaModel):
    def __init__(
        self,
        task_execution_id: str = None,
        task_name: str = None,
        task_action: str = None,
    ):
        self.task_execution_id = task_execution_id
        self.task_name = task_name
        self.task_action = task_action

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.task_execution_id is not None:
            result['TaskExecutionId'] = self.task_execution_id
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.task_action is not None:
            result['TaskAction'] = self.task_action
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskExecutionId') is not None:
            self.task_execution_id = m.get('TaskExecutionId')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('TaskAction') is not None:
            self.task_action = m.get('TaskAction')
        return self


class ListExecutionsResponseBodyExecutions(TeaModel):
    def __init__(
        self,
        status: str = None,
        waiting_status: str = None,
        targets: str = None,
        status_reason: str = None,
        tags: Dict[str, Any] = None,
        last_successful_trigger_time: str = None,
        mode: str = None,
        safety_check: str = None,
        template_name: str = None,
        template_version: str = None,
        create_date: str = None,
        update_date: str = None,
        description: str = None,
        last_trigger_time: str = None,
        parent_execution_id: str = None,
        last_trigger_status: str = None,
        status_message: str = None,
        outputs: str = None,
        executed_by: str = None,
        end_date: str = None,
        is_parent: bool = None,
        start_date: str = None,
        execution_id: str = None,
        parameters: Dict[str, Any] = None,
        counters: Dict[str, Any] = None,
        resource_group_id: str = None,
        category: str = None,
        template_id: str = None,
        ram_role: str = None,
        resource_status: str = None,
        current_tasks: List[ListExecutionsResponseBodyExecutionsCurrentTasks] = None,
    ):
        self.status = status
        self.waiting_status = waiting_status
        self.targets = targets
        self.status_reason = status_reason
        self.tags = tags
        self.last_successful_trigger_time = last_successful_trigger_time
        self.mode = mode
        self.safety_check = safety_check
        self.template_name = template_name
        self.template_version = template_version
        self.create_date = create_date
        self.update_date = update_date
        self.description = description
        self.last_trigger_time = last_trigger_time
        self.parent_execution_id = parent_execution_id
        self.last_trigger_status = last_trigger_status
        self.status_message = status_message
        self.outputs = outputs
        self.executed_by = executed_by
        self.end_date = end_date
        self.is_parent = is_parent
        self.start_date = start_date
        self.execution_id = execution_id
        self.parameters = parameters
        self.counters = counters
        self.resource_group_id = resource_group_id
        self.category = category
        self.template_id = template_id
        self.ram_role = ram_role
        self.resource_status = resource_status
        self.current_tasks = current_tasks

    def validate(self):
        if self.current_tasks:
            for k in self.current_tasks:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.waiting_status is not None:
            result['WaitingStatus'] = self.waiting_status
        if self.targets is not None:
            result['Targets'] = self.targets
        if self.status_reason is not None:
            result['StatusReason'] = self.status_reason
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.last_successful_trigger_time is not None:
            result['LastSuccessfulTriggerTime'] = self.last_successful_trigger_time
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.safety_check is not None:
            result['SafetyCheck'] = self.safety_check
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.create_date is not None:
            result['CreateDate'] = self.create_date
        if self.update_date is not None:
            result['UpdateDate'] = self.update_date
        if self.description is not None:
            result['Description'] = self.description
        if self.last_trigger_time is not None:
            result['LastTriggerTime'] = self.last_trigger_time
        if self.parent_execution_id is not None:
            result['ParentExecutionId'] = self.parent_execution_id
        if self.last_trigger_status is not None:
            result['LastTriggerStatus'] = self.last_trigger_status
        if self.status_message is not None:
            result['StatusMessage'] = self.status_message
        if self.outputs is not None:
            result['Outputs'] = self.outputs
        if self.executed_by is not None:
            result['ExecutedBy'] = self.executed_by
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        if self.is_parent is not None:
            result['IsParent'] = self.is_parent
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        if self.counters is not None:
            result['Counters'] = self.counters
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.category is not None:
            result['Category'] = self.category
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        if self.ram_role is not None:
            result['RamRole'] = self.ram_role
        if self.resource_status is not None:
            result['ResourceStatus'] = self.resource_status
        result['CurrentTasks'] = []
        if self.current_tasks is not None:
            for k in self.current_tasks:
                result['CurrentTasks'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('WaitingStatus') is not None:
            self.waiting_status = m.get('WaitingStatus')
        if m.get('Targets') is not None:
            self.targets = m.get('Targets')
        if m.get('StatusReason') is not None:
            self.status_reason = m.get('StatusReason')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('LastSuccessfulTriggerTime') is not None:
            self.last_successful_trigger_time = m.get('LastSuccessfulTriggerTime')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('SafetyCheck') is not None:
            self.safety_check = m.get('SafetyCheck')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('CreateDate') is not None:
            self.create_date = m.get('CreateDate')
        if m.get('UpdateDate') is not None:
            self.update_date = m.get('UpdateDate')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('LastTriggerTime') is not None:
            self.last_trigger_time = m.get('LastTriggerTime')
        if m.get('ParentExecutionId') is not None:
            self.parent_execution_id = m.get('ParentExecutionId')
        if m.get('LastTriggerStatus') is not None:
            self.last_trigger_status = m.get('LastTriggerStatus')
        if m.get('StatusMessage') is not None:
            self.status_message = m.get('StatusMessage')
        if m.get('Outputs') is not None:
            self.outputs = m.get('Outputs')
        if m.get('ExecutedBy') is not None:
            self.executed_by = m.get('ExecutedBy')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        if m.get('IsParent') is not None:
            self.is_parent = m.get('IsParent')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        if m.get('Counters') is not None:
            self.counters = m.get('Counters')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        if m.get('RamRole') is not None:
            self.ram_role = m.get('RamRole')
        if m.get('ResourceStatus') is not None:
            self.resource_status = m.get('ResourceStatus')
        self.current_tasks = []
        if m.get('CurrentTasks') is not None:
            for k in m.get('CurrentTasks'):
                temp_model = ListExecutionsResponseBodyExecutionsCurrentTasks()
                self.current_tasks.append(temp_model.from_map(k))
        return self


class ListExecutionsResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        executions: List[ListExecutionsResponseBodyExecutions] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.executions = executions

    def validate(self):
        if self.executions:
            for k in self.executions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['Executions'] = []
        if self.executions is not None:
            for k in self.executions:
                result['Executions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.executions = []
        if m.get('Executions') is not None:
            for k in m.get('Executions'):
                temp_model = ListExecutionsResponseBodyExecutions()
                self.executions.append(temp_model.from_map(k))
        return self


class ListExecutionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListExecutionsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListExecutionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListInstancePatchesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        instance_id: str = None,
        max_results: int = None,
        next_token: str = None,
        patch_statuses: str = None,
    ):
        self.region_id = region_id
        self.instance_id = instance_id
        self.max_results = max_results
        self.next_token = next_token
        self.patch_statuses = patch_statuses

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.patch_statuses is not None:
            result['PatchStatuses'] = self.patch_statuses
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('PatchStatuses') is not None:
            self.patch_statuses = m.get('PatchStatuses')
        return self


class ListInstancePatchesResponseBodyPatches(TeaModel):
    def __init__(
        self,
        severity: str = None,
        status: str = None,
        installed_time: str = None,
        kbid: str = None,
        title: str = None,
        classification: str = None,
    ):
        self.severity = severity
        self.status = status
        self.installed_time = installed_time
        self.kbid = kbid
        self.title = title
        self.classification = classification

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.severity is not None:
            result['Severity'] = self.severity
        if self.status is not None:
            result['Status'] = self.status
        if self.installed_time is not None:
            result['InstalledTime'] = self.installed_time
        if self.kbid is not None:
            result['KBId'] = self.kbid
        if self.title is not None:
            result['Title'] = self.title
        if self.classification is not None:
            result['Classification'] = self.classification
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Severity') is not None:
            self.severity = m.get('Severity')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('InstalledTime') is not None:
            self.installed_time = m.get('InstalledTime')
        if m.get('KBId') is not None:
            self.kbid = m.get('KBId')
        if m.get('Title') is not None:
            self.title = m.get('Title')
        if m.get('Classification') is not None:
            self.classification = m.get('Classification')
        return self


class ListInstancePatchesResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        patches: List[ListInstancePatchesResponseBodyPatches] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.patches = patches

    def validate(self):
        if self.patches:
            for k in self.patches:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['Patches'] = []
        if self.patches is not None:
            for k in self.patches:
                result['Patches'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.patches = []
        if m.get('Patches') is not None:
            for k in m.get('Patches'):
                temp_model = ListInstancePatchesResponseBodyPatches()
                self.patches.append(temp_model.from_map(k))
        return self


class ListInstancePatchesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListInstancePatchesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListInstancePatchesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListInstancePatchStatesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        max_results: int = None,
        next_token: str = None,
        instance_ids: str = None,
    ):
        self.region_id = region_id
        self.max_results = max_results
        self.next_token = next_token
        self.instance_ids = instance_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.instance_ids is not None:
            result['InstanceIds'] = self.instance_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('InstanceIds') is not None:
            self.instance_ids = m.get('InstanceIds')
        return self


class ListInstancePatchStatesResponseBodyInstancePatchStates(TeaModel):
    def __init__(
        self,
        missing_count: str = None,
        operation_end_time: str = None,
        owner_information: str = None,
        installed_other_count: str = None,
        instance_id: str = None,
        operation_type: str = None,
        operation_start_time: str = None,
        failed_count: str = None,
        baseline_id: str = None,
        installed_pending_reboot_count: str = None,
        installed_rejected_count: str = None,
        patch_group: str = None,
        installed_count: str = None,
    ):
        self.missing_count = missing_count
        self.operation_end_time = operation_end_time
        self.owner_information = owner_information
        self.installed_other_count = installed_other_count
        self.instance_id = instance_id
        self.operation_type = operation_type
        self.operation_start_time = operation_start_time
        self.failed_count = failed_count
        self.baseline_id = baseline_id
        self.installed_pending_reboot_count = installed_pending_reboot_count
        self.installed_rejected_count = installed_rejected_count
        self.patch_group = patch_group
        self.installed_count = installed_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.missing_count is not None:
            result['MissingCount'] = self.missing_count
        if self.operation_end_time is not None:
            result['OperationEndTime'] = self.operation_end_time
        if self.owner_information is not None:
            result['OwnerInformation'] = self.owner_information
        if self.installed_other_count is not None:
            result['InstalledOtherCount'] = self.installed_other_count
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.operation_type is not None:
            result['OperationType'] = self.operation_type
        if self.operation_start_time is not None:
            result['OperationStartTime'] = self.operation_start_time
        if self.failed_count is not None:
            result['FailedCount'] = self.failed_count
        if self.baseline_id is not None:
            result['BaselineId'] = self.baseline_id
        if self.installed_pending_reboot_count is not None:
            result['InstalledPendingRebootCount'] = self.installed_pending_reboot_count
        if self.installed_rejected_count is not None:
            result['InstalledRejectedCount'] = self.installed_rejected_count
        if self.patch_group is not None:
            result['PatchGroup'] = self.patch_group
        if self.installed_count is not None:
            result['InstalledCount'] = self.installed_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MissingCount') is not None:
            self.missing_count = m.get('MissingCount')
        if m.get('OperationEndTime') is not None:
            self.operation_end_time = m.get('OperationEndTime')
        if m.get('OwnerInformation') is not None:
            self.owner_information = m.get('OwnerInformation')
        if m.get('InstalledOtherCount') is not None:
            self.installed_other_count = m.get('InstalledOtherCount')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('OperationType') is not None:
            self.operation_type = m.get('OperationType')
        if m.get('OperationStartTime') is not None:
            self.operation_start_time = m.get('OperationStartTime')
        if m.get('FailedCount') is not None:
            self.failed_count = m.get('FailedCount')
        if m.get('BaselineId') is not None:
            self.baseline_id = m.get('BaselineId')
        if m.get('InstalledPendingRebootCount') is not None:
            self.installed_pending_reboot_count = m.get('InstalledPendingRebootCount')
        if m.get('InstalledRejectedCount') is not None:
            self.installed_rejected_count = m.get('InstalledRejectedCount')
        if m.get('PatchGroup') is not None:
            self.patch_group = m.get('PatchGroup')
        if m.get('InstalledCount') is not None:
            self.installed_count = m.get('InstalledCount')
        return self


class ListInstancePatchStatesResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        instance_patch_states: List[ListInstancePatchStatesResponseBodyInstancePatchStates] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.instance_patch_states = instance_patch_states

    def validate(self):
        if self.instance_patch_states:
            for k in self.instance_patch_states:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['InstancePatchStates'] = []
        if self.instance_patch_states is not None:
            for k in self.instance_patch_states:
                result['InstancePatchStates'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.instance_patch_states = []
        if m.get('InstancePatchStates') is not None:
            for k in m.get('InstancePatchStates'):
                temp_model = ListInstancePatchStatesResponseBodyInstancePatchStates()
                self.instance_patch_states.append(temp_model.from_map(k))
        return self


class ListInstancePatchStatesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListInstancePatchStatesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListInstancePatchStatesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListInstanceStateReportsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        instance_id: str = None,
        state_configuration_id: str = None,
        max_results: int = None,
        next_token: str = None,
    ):
        self.region_id = region_id
        self.instance_id = instance_id
        self.state_configuration_id = state_configuration_id
        self.max_results = max_results
        self.next_token = next_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.state_configuration_id is not None:
            result['StateConfigurationId'] = self.state_configuration_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('StateConfigurationId') is not None:
            self.state_configuration_id = m.get('StateConfigurationId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        return self


class ListInstanceStateReportsResponseBodyStateReports(TeaModel):
    def __init__(
        self,
        report_status: str = None,
        report_info: str = None,
        success_apply_time: str = None,
        state_configuration_id: str = None,
        instance_id: str = None,
        mode: str = None,
        report_time: str = None,
    ):
        self.report_status = report_status
        self.report_info = report_info
        self.success_apply_time = success_apply_time
        self.state_configuration_id = state_configuration_id
        self.instance_id = instance_id
        self.mode = mode
        self.report_time = report_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.report_status is not None:
            result['ReportStatus'] = self.report_status
        if self.report_info is not None:
            result['ReportInfo'] = self.report_info
        if self.success_apply_time is not None:
            result['SuccessApplyTime'] = self.success_apply_time
        if self.state_configuration_id is not None:
            result['StateConfigurationId'] = self.state_configuration_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.report_time is not None:
            result['ReportTime'] = self.report_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ReportStatus') is not None:
            self.report_status = m.get('ReportStatus')
        if m.get('ReportInfo') is not None:
            self.report_info = m.get('ReportInfo')
        if m.get('SuccessApplyTime') is not None:
            self.success_apply_time = m.get('SuccessApplyTime')
        if m.get('StateConfigurationId') is not None:
            self.state_configuration_id = m.get('StateConfigurationId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('ReportTime') is not None:
            self.report_time = m.get('ReportTime')
        return self


class ListInstanceStateReportsResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        state_reports: List[ListInstanceStateReportsResponseBodyStateReports] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.state_reports = state_reports

    def validate(self):
        if self.state_reports:
            for k in self.state_reports:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['StateReports'] = []
        if self.state_reports is not None:
            for k in self.state_reports:
                result['StateReports'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.state_reports = []
        if m.get('StateReports') is not None:
            for k in m.get('StateReports'):
                temp_model = ListInstanceStateReportsResponseBodyStateReports()
                self.state_reports.append(temp_model.from_map(k))
        return self


class ListInstanceStateReportsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListInstanceStateReportsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListInstanceStateReportsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListInventoryEntriesRequestFilter(TeaModel):
    def __init__(
        self,
        value: List[str] = None,
        operator: str = None,
        name: str = None,
    ):
        self.value = value
        self.operator = operator
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.operator is not None:
            result['Operator'] = self.operator
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Operator') is not None:
            self.operator = m.get('Operator')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class ListInventoryEntriesRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        type_name: str = None,
        max_results: int = None,
        next_token: str = None,
        filter: List[ListInventoryEntriesRequestFilter] = None,
    ):
        self.instance_id = instance_id
        self.type_name = type_name
        self.max_results = max_results
        self.next_token = next_token
        self.filter = filter

    def validate(self):
        if self.filter:
            for k in self.filter:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.type_name is not None:
            result['TypeName'] = self.type_name
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        result['Filter'] = []
        if self.filter is not None:
            for k in self.filter:
                result['Filter'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('TypeName') is not None:
            self.type_name = m.get('TypeName')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        self.filter = []
        if m.get('Filter') is not None:
            for k in m.get('Filter'):
                temp_model = ListInventoryEntriesRequestFilter()
                self.filter.append(temp_model.from_map(k))
        return self


class ListInventoryEntriesResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        schema_version: str = None,
        max_results: int = None,
        capture_time: str = None,
        type_name: str = None,
        instance_id: str = None,
        entries: List[Dict[str, Any]] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.schema_version = schema_version
        self.max_results = max_results
        self.capture_time = capture_time
        self.type_name = type_name
        self.instance_id = instance_id
        self.entries = entries

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.schema_version is not None:
            result['SchemaVersion'] = self.schema_version
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.capture_time is not None:
            result['CaptureTime'] = self.capture_time
        if self.type_name is not None:
            result['TypeName'] = self.type_name
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.entries is not None:
            result['Entries'] = self.entries
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SchemaVersion') is not None:
            self.schema_version = m.get('SchemaVersion')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('CaptureTime') is not None:
            self.capture_time = m.get('CaptureTime')
        if m.get('TypeName') is not None:
            self.type_name = m.get('TypeName')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Entries') is not None:
            self.entries = m.get('Entries')
        return self


class ListInventoryEntriesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListInventoryEntriesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListInventoryEntriesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListParametersRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        max_results: int = None,
        next_token: str = None,
        sort_field: str = None,
        sort_order: str = None,
        type: str = None,
        path: str = None,
        recursive: bool = None,
        tags: Dict[str, Any] = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.max_results = max_results
        self.next_token = next_token
        self.sort_field = sort_field
        self.sort_order = sort_order
        self.type = type
        self.path = path
        self.recursive = recursive
        self.tags = tags
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.sort_field is not None:
            result['SortField'] = self.sort_field
        if self.sort_order is not None:
            result['SortOrder'] = self.sort_order
        if self.type is not None:
            result['Type'] = self.type
        if self.path is not None:
            result['Path'] = self.path
        if self.recursive is not None:
            result['Recursive'] = self.recursive
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('SortField') is not None:
            self.sort_field = m.get('SortField')
        if m.get('SortOrder') is not None:
            self.sort_order = m.get('SortOrder')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Path') is not None:
            self.path = m.get('Path')
        if m.get('Recursive') is not None:
            self.recursive = m.get('Recursive')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class ListParametersShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        max_results: int = None,
        next_token: str = None,
        sort_field: str = None,
        sort_order: str = None,
        type: str = None,
        path: str = None,
        recursive: bool = None,
        tags_shrink: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.max_results = max_results
        self.next_token = next_token
        self.sort_field = sort_field
        self.sort_order = sort_order
        self.type = type
        self.path = path
        self.recursive = recursive
        self.tags_shrink = tags_shrink
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.sort_field is not None:
            result['SortField'] = self.sort_field
        if self.sort_order is not None:
            result['SortOrder'] = self.sort_order
        if self.type is not None:
            result['Type'] = self.type
        if self.path is not None:
            result['Path'] = self.path
        if self.recursive is not None:
            result['Recursive'] = self.recursive
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('SortField') is not None:
            self.sort_field = m.get('SortField')
        if m.get('SortOrder') is not None:
            self.sort_order = m.get('SortOrder')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Path') is not None:
            self.path = m.get('Path')
        if m.get('Recursive') is not None:
            self.recursive = m.get('Recursive')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class ListParametersResponseBodyParameters(TeaModel):
    def __init__(
        self,
        type: str = None,
        updated_date: str = None,
        updated_by: str = None,
        tags: Dict[str, Any] = None,
        description: str = None,
        created_by: str = None,
        resource_group_id: str = None,
        created_date: str = None,
        parameter_version: str = None,
        name: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.type = type
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.tags = tags
        self.description = description
        self.created_by = created_by
        self.resource_group_id = resource_group_id
        self.created_date = created_date
        self.parameter_version = parameter_version
        self.name = name
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.description is not None:
            result['Description'] = self.description
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class ListParametersResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        total_count: int = None,
        max_results: int = None,
        parameters: List[ListParametersResponseBodyParameters] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.total_count = total_count
        self.max_results = max_results
        self.parameters = parameters

    def validate(self):
        if self.parameters:
            for k in self.parameters:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['Parameters'] = []
        if self.parameters is not None:
            for k in self.parameters:
                result['Parameters'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.parameters = []
        if m.get('Parameters') is not None:
            for k in m.get('Parameters'):
                temp_model = ListParametersResponseBodyParameters()
                self.parameters.append(temp_model.from_map(k))
        return self


class ListParametersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListParametersResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListParametersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListParameterVersionsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        max_results: int = None,
        next_token: str = None,
        share_type: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.max_results = max_results
        self.next_token = next_token
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class ListParameterVersionsResponseBodyParameterVersions(TeaModel):
    def __init__(
        self,
        parameter_version: int = None,
        value: str = None,
        updated_date: str = None,
        updated_by: str = None,
    ):
        self.parameter_version = parameter_version
        self.value = value
        self.updated_date = updated_date
        self.updated_by = updated_by

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.value is not None:
            result['Value'] = self.value
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        return self


class ListParameterVersionsResponseBody(TeaModel):
    def __init__(
        self,
        type: str = None,
        next_token: str = None,
        request_id: str = None,
        description: str = None,
        max_results: int = None,
        created_by: str = None,
        created_date: str = None,
        name: str = None,
        total_count: int = None,
        id: str = None,
        parameter_versions: List[ListParameterVersionsResponseBodyParameterVersions] = None,
    ):
        self.type = type
        self.next_token = next_token
        self.request_id = request_id
        self.description = description
        self.max_results = max_results
        self.created_by = created_by
        self.created_date = created_date
        self.name = name
        self.total_count = total_count
        self.id = id
        self.parameter_versions = parameter_versions

    def validate(self):
        if self.parameter_versions:
            for k in self.parameter_versions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.description is not None:
            result['Description'] = self.description
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.name is not None:
            result['Name'] = self.name
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.id is not None:
            result['Id'] = self.id
        result['ParameterVersions'] = []
        if self.parameter_versions is not None:
            for k in self.parameter_versions:
                result['ParameterVersions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        self.parameter_versions = []
        if m.get('ParameterVersions') is not None:
            for k in m.get('ParameterVersions'):
                temp_model = ListParameterVersionsResponseBodyParameterVersions()
                self.parameter_versions.append(temp_model.from_map(k))
        return self


class ListParameterVersionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListParameterVersionsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListParameterVersionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListPatchBaselinesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        operation_system: str = None,
        share_type: str = None,
        max_results: int = None,
        next_token: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.operation_system = operation_system
        self.share_type = share_type
        self.max_results = max_results
        self.next_token = next_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.operation_system is not None:
            result['OperationSystem'] = self.operation_system
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('OperationSystem') is not None:
            self.operation_system = m.get('OperationSystem')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        return self


class ListPatchBaselinesResponseBodyPatchBaselines(TeaModel):
    def __init__(
        self,
        operation_system: str = None,
        is_default: bool = None,
        description: str = None,
        updated_date: str = None,
        updated_by: str = None,
        created_by: str = None,
        created_date: str = None,
        name: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.operation_system = operation_system
        self.is_default = is_default
        self.description = description
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.created_by = created_by
        self.created_date = created_date
        self.name = name
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.operation_system is not None:
            result['OperationSystem'] = self.operation_system
        if self.is_default is not None:
            result['IsDefault'] = self.is_default
        if self.description is not None:
            result['Description'] = self.description
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OperationSystem') is not None:
            self.operation_system = m.get('OperationSystem')
        if m.get('IsDefault') is not None:
            self.is_default = m.get('IsDefault')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class ListPatchBaselinesResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        patch_baselines: List[ListPatchBaselinesResponseBodyPatchBaselines] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.patch_baselines = patch_baselines

    def validate(self):
        if self.patch_baselines:
            for k in self.patch_baselines:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['PatchBaselines'] = []
        if self.patch_baselines is not None:
            for k in self.patch_baselines:
                result['PatchBaselines'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.patch_baselines = []
        if m.get('PatchBaselines') is not None:
            for k in m.get('PatchBaselines'):
                temp_model = ListPatchBaselinesResponseBodyPatchBaselines()
                self.patch_baselines.append(temp_model.from_map(k))
        return self


class ListPatchBaselinesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListPatchBaselinesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListPatchBaselinesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListResourceExecutionStatusRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        execution_id: str = None,
        max_results: int = None,
        next_token: str = None,
    ):
        self.region_id = region_id
        self.execution_id = execution_id
        self.max_results = max_results
        self.next_token = next_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        return self


class ListResourceExecutionStatusResponseBodyResourceExecutionStatus(TeaModel):
    def __init__(
        self,
        outputs: str = None,
        status: str = None,
        execution_time: str = None,
        resource_id: str = None,
        execution_id: str = None,
    ):
        self.outputs = outputs
        self.status = status
        self.execution_time = execution_time
        self.resource_id = resource_id
        self.execution_id = execution_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.outputs is not None:
            result['Outputs'] = self.outputs
        if self.status is not None:
            result['Status'] = self.status
        if self.execution_time is not None:
            result['ExecutionTime'] = self.execution_time
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Outputs') is not None:
            self.outputs = m.get('Outputs')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('ExecutionTime') is not None:
            self.execution_time = m.get('ExecutionTime')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        return self


class ListResourceExecutionStatusResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        resource_execution_status: List[ListResourceExecutionStatusResponseBodyResourceExecutionStatus] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.resource_execution_status = resource_execution_status

    def validate(self):
        if self.resource_execution_status:
            for k in self.resource_execution_status:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['ResourceExecutionStatus'] = []
        if self.resource_execution_status is not None:
            for k in self.resource_execution_status:
                result['ResourceExecutionStatus'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.resource_execution_status = []
        if m.get('ResourceExecutionStatus') is not None:
            for k in m.get('ResourceExecutionStatus'):
                temp_model = ListResourceExecutionStatusResponseBodyResourceExecutionStatus()
                self.resource_execution_status.append(temp_model.from_map(k))
        return self


class ListResourceExecutionStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListResourceExecutionStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListResourceExecutionStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListSecretParametersRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        max_results: int = None,
        next_token: str = None,
        sort_field: str = None,
        sort_order: str = None,
        path: str = None,
        recursive: bool = None,
        tags: Dict[str, Any] = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.max_results = max_results
        self.next_token = next_token
        self.sort_field = sort_field
        self.sort_order = sort_order
        self.path = path
        self.recursive = recursive
        self.tags = tags
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.sort_field is not None:
            result['SortField'] = self.sort_field
        if self.sort_order is not None:
            result['SortOrder'] = self.sort_order
        if self.path is not None:
            result['Path'] = self.path
        if self.recursive is not None:
            result['Recursive'] = self.recursive
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('SortField') is not None:
            self.sort_field = m.get('SortField')
        if m.get('SortOrder') is not None:
            self.sort_order = m.get('SortOrder')
        if m.get('Path') is not None:
            self.path = m.get('Path')
        if m.get('Recursive') is not None:
            self.recursive = m.get('Recursive')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class ListSecretParametersShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        max_results: int = None,
        next_token: str = None,
        sort_field: str = None,
        sort_order: str = None,
        path: str = None,
        recursive: bool = None,
        tags_shrink: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.max_results = max_results
        self.next_token = next_token
        self.sort_field = sort_field
        self.sort_order = sort_order
        self.path = path
        self.recursive = recursive
        self.tags_shrink = tags_shrink
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.sort_field is not None:
            result['SortField'] = self.sort_field
        if self.sort_order is not None:
            result['SortOrder'] = self.sort_order
        if self.path is not None:
            result['Path'] = self.path
        if self.recursive is not None:
            result['Recursive'] = self.recursive
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('SortField') is not None:
            self.sort_field = m.get('SortField')
        if m.get('SortOrder') is not None:
            self.sort_order = m.get('SortOrder')
        if m.get('Path') is not None:
            self.path = m.get('Path')
        if m.get('Recursive') is not None:
            self.recursive = m.get('Recursive')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class ListSecretParametersResponseBodyParameters(TeaModel):
    def __init__(
        self,
        type: str = None,
        updated_date: str = None,
        updated_by: str = None,
        key_id: str = None,
        tags: Dict[str, Any] = None,
        description: str = None,
        resource_group_id: str = None,
        created_by: str = None,
        created_date: str = None,
        parameter_version: str = None,
        name: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.type = type
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.key_id = key_id
        self.tags = tags
        self.description = description
        self.resource_group_id = resource_group_id
        self.created_by = created_by
        self.created_date = created_date
        self.parameter_version = parameter_version
        self.name = name
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.key_id is not None:
            result['KeyId'] = self.key_id
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.description is not None:
            result['Description'] = self.description
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('KeyId') is not None:
            self.key_id = m.get('KeyId')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class ListSecretParametersResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        parameters: List[ListSecretParametersResponseBodyParameters] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.parameters = parameters

    def validate(self):
        if self.parameters:
            for k in self.parameters:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['Parameters'] = []
        if self.parameters is not None:
            for k in self.parameters:
                result['Parameters'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.parameters = []
        if m.get('Parameters') is not None:
            for k in m.get('Parameters'):
                temp_model = ListSecretParametersResponseBodyParameters()
                self.parameters.append(temp_model.from_map(k))
        return self


class ListSecretParametersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListSecretParametersResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListSecretParametersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListSecretParameterVersionsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        max_results: int = None,
        next_token: str = None,
        share_type: str = None,
        with_decryption: bool = None,
    ):
        self.region_id = region_id
        self.name = name
        self.max_results = max_results
        self.next_token = next_token
        self.share_type = share_type
        self.with_decryption = with_decryption

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        if self.with_decryption is not None:
            result['WithDecryption'] = self.with_decryption
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        if m.get('WithDecryption') is not None:
            self.with_decryption = m.get('WithDecryption')
        return self


class ListSecretParameterVersionsResponseBodyParameterVersions(TeaModel):
    def __init__(
        self,
        parameter_version: int = None,
        value: str = None,
        updated_date: str = None,
        updated_by: str = None,
    ):
        self.parameter_version = parameter_version
        self.value = value
        self.updated_date = updated_date
        self.updated_by = updated_by

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.value is not None:
            result['Value'] = self.value
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        return self


class ListSecretParameterVersionsResponseBody(TeaModel):
    def __init__(
        self,
        type: str = None,
        next_token: str = None,
        request_id: str = None,
        description: str = None,
        max_results: int = None,
        created_by: str = None,
        created_date: str = None,
        name: str = None,
        total_count: int = None,
        id: str = None,
        parameter_versions: List[ListSecretParameterVersionsResponseBodyParameterVersions] = None,
    ):
        self.type = type
        self.next_token = next_token
        self.request_id = request_id
        self.description = description
        self.max_results = max_results
        self.created_by = created_by
        self.created_date = created_date
        self.name = name
        self.total_count = total_count
        self.id = id
        self.parameter_versions = parameter_versions

    def validate(self):
        if self.parameter_versions:
            for k in self.parameter_versions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.description is not None:
            result['Description'] = self.description
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.name is not None:
            result['Name'] = self.name
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.id is not None:
            result['Id'] = self.id
        result['ParameterVersions'] = []
        if self.parameter_versions is not None:
            for k in self.parameter_versions:
                result['ParameterVersions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        self.parameter_versions = []
        if m.get('ParameterVersions') is not None:
            for k in m.get('ParameterVersions'):
                temp_model = ListSecretParameterVersionsResponseBodyParameterVersions()
                self.parameter_versions.append(temp_model.from_map(k))
        return self


class ListSecretParameterVersionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListSecretParameterVersionsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListSecretParameterVersionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListStateConfigurationsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        template_version: str = None,
        state_configuration_ids: str = None,
        tags: Dict[str, Any] = None,
        max_results: int = None,
        next_token: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.template_version = template_version
        self.state_configuration_ids = state_configuration_ids
        self.tags = tags
        self.max_results = max_results
        self.next_token = next_token
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.state_configuration_ids is not None:
            result['StateConfigurationIds'] = self.state_configuration_ids
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('StateConfigurationIds') is not None:
            self.state_configuration_ids = m.get('StateConfigurationIds')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class ListStateConfigurationsShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        template_version: str = None,
        state_configuration_ids: str = None,
        tags_shrink: str = None,
        max_results: int = None,
        next_token: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.template_version = template_version
        self.state_configuration_ids = state_configuration_ids
        self.tags_shrink = tags_shrink
        self.max_results = max_results
        self.next_token = next_token
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.state_configuration_ids is not None:
            result['StateConfigurationIds'] = self.state_configuration_ids
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('StateConfigurationIds') is not None:
            self.state_configuration_ids = m.get('StateConfigurationIds')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class ListStateConfigurationsResponseBodyStateConfigurations(TeaModel):
    def __init__(
        self,
        update_time: str = None,
        create_time: str = None,
        targets: str = None,
        tags: Dict[str, Any] = None,
        state_configuration_id: str = None,
        schedule_expression: str = None,
        template_name: str = None,
        template_version: str = None,
        configure_mode: str = None,
        schedule_type: str = None,
        parameters: str = None,
        description: str = None,
        resource_group_id: str = None,
        template_id: str = None,
    ):
        self.update_time = update_time
        self.create_time = create_time
        self.targets = targets
        self.tags = tags
        self.state_configuration_id = state_configuration_id
        self.schedule_expression = schedule_expression
        self.template_name = template_name
        self.template_version = template_version
        self.configure_mode = configure_mode
        self.schedule_type = schedule_type
        self.parameters = parameters
        self.description = description
        self.resource_group_id = resource_group_id
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.targets is not None:
            result['Targets'] = self.targets
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.state_configuration_id is not None:
            result['StateConfigurationId'] = self.state_configuration_id
        if self.schedule_expression is not None:
            result['ScheduleExpression'] = self.schedule_expression
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.configure_mode is not None:
            result['ConfigureMode'] = self.configure_mode
        if self.schedule_type is not None:
            result['ScheduleType'] = self.schedule_type
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        if self.description is not None:
            result['Description'] = self.description
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Targets') is not None:
            self.targets = m.get('Targets')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('StateConfigurationId') is not None:
            self.state_configuration_id = m.get('StateConfigurationId')
        if m.get('ScheduleExpression') is not None:
            self.schedule_expression = m.get('ScheduleExpression')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('ConfigureMode') is not None:
            self.configure_mode = m.get('ConfigureMode')
        if m.get('ScheduleType') is not None:
            self.schedule_type = m.get('ScheduleType')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class ListStateConfigurationsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        state_configurations: List[ListStateConfigurationsResponseBodyStateConfigurations] = None,
    ):
        self.request_id = request_id
        self.state_configurations = state_configurations

    def validate(self):
        if self.state_configurations:
            for k in self.state_configurations:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['StateConfigurations'] = []
        if self.state_configurations is not None:
            for k in self.state_configurations:
                result['StateConfigurations'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.state_configurations = []
        if m.get('StateConfigurations') is not None:
            for k in m.get('StateConfigurations'):
                temp_model = ListStateConfigurationsResponseBodyStateConfigurations()
                self.state_configurations.append(temp_model.from_map(k))
        return self


class ListStateConfigurationsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListStateConfigurationsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListStateConfigurationsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTagKeysRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        max_results: int = None,
        next_token: str = None,
        resource_type: str = None,
    ):
        self.region_id = region_id
        self.max_results = max_results
        self.next_token = next_token
        self.resource_type = resource_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        return self


class ListTagKeysResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        keys: List[str] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.keys = keys

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.keys is not None:
            result['Keys'] = self.keys
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('Keys') is not None:
            self.keys = m.get('Keys')
        return self


class ListTagKeysResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListTagKeysResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListTagKeysResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTagResourcesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        resource_ids: Dict[str, Any] = None,
        resource_type: str = None,
        tags: Dict[str, Any] = None,
        next_token: str = None,
    ):
        self.region_id = region_id
        self.resource_ids = resource_ids
        self.resource_type = resource_type
        self.tags = tags
        self.next_token = next_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_ids is not None:
            result['ResourceIds'] = self.resource_ids
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceIds') is not None:
            self.resource_ids = m.get('ResourceIds')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        return self


class ListTagResourcesShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        resource_ids_shrink: str = None,
        resource_type: str = None,
        tags_shrink: str = None,
        next_token: str = None,
    ):
        self.region_id = region_id
        self.resource_ids_shrink = resource_ids_shrink
        self.resource_type = resource_type
        self.tags_shrink = tags_shrink
        self.next_token = next_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_ids_shrink is not None:
            result['ResourceIds'] = self.resource_ids_shrink
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceIds') is not None:
            self.resource_ids_shrink = m.get('ResourceIds')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        return self


class ListTagResourcesResponseBodyTagResourcesTagResource(TeaModel):
    def __init__(
        self,
        resource_type: str = None,
        tag_value: str = None,
        resource_id: str = None,
        tag_key: str = None,
    ):
        self.resource_type = resource_type
        self.tag_value = tag_value
        self.resource_id = resource_id
        self.tag_key = tag_key

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tag_value is not None:
            result['TagValue'] = self.tag_value
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('TagValue') is not None:
            self.tag_value = m.get('TagValue')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        return self


class ListTagResourcesResponseBodyTagResources(TeaModel):
    def __init__(
        self,
        tag_resource: List[ListTagResourcesResponseBodyTagResourcesTagResource] = None,
    ):
        self.tag_resource = tag_resource

    def validate(self):
        if self.tag_resource:
            for k in self.tag_resource:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['TagResource'] = []
        if self.tag_resource is not None:
            for k in self.tag_resource:
                result['TagResource'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.tag_resource = []
        if m.get('TagResource') is not None:
            for k in m.get('TagResource'):
                temp_model = ListTagResourcesResponseBodyTagResourcesTagResource()
                self.tag_resource.append(temp_model.from_map(k))
        return self


class ListTagResourcesResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        tag_resources: ListTagResourcesResponseBodyTagResources = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.tag_resources = tag_resources

    def validate(self):
        if self.tag_resources:
            self.tag_resources.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.tag_resources is not None:
            result['TagResources'] = self.tag_resources.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TagResources') is not None:
            temp_model = ListTagResourcesResponseBodyTagResources()
            self.tag_resources = temp_model.from_map(m['TagResources'])
        return self


class ListTagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListTagResourcesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListTagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTagValuesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        max_results: int = None,
        next_token: str = None,
        resource_type: str = None,
        key: str = None,
    ):
        self.region_id = region_id
        self.max_results = max_results
        self.next_token = next_token
        self.resource_type = resource_type
        self.key = key

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.key is not None:
            result['Key'] = self.key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Key') is not None:
            self.key = m.get('Key')
        return self


class ListTagValuesResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        values: List[str] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.values = values

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.values is not None:
            result['Values'] = self.values
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('Values') is not None:
            self.values = m.get('Values')
        return self


class ListTagValuesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListTagValuesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListTagValuesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTaskExecutionsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        execution_id: str = None,
        status: str = None,
        start_date_before: str = None,
        start_date_after: str = None,
        end_date_before: str = None,
        end_date_after: str = None,
        task_execution_id: str = None,
        task_name: str = None,
        task_action: str = None,
        parent_task_execution_id: str = None,
        include_child_task_execution: bool = None,
        max_results: int = None,
        next_token: str = None,
        sort_field: str = None,
        sort_order: str = None,
    ):
        self.region_id = region_id
        self.execution_id = execution_id
        self.status = status
        self.start_date_before = start_date_before
        self.start_date_after = start_date_after
        self.end_date_before = end_date_before
        self.end_date_after = end_date_after
        self.task_execution_id = task_execution_id
        self.task_name = task_name
        self.task_action = task_action
        self.parent_task_execution_id = parent_task_execution_id
        self.include_child_task_execution = include_child_task_execution
        self.max_results = max_results
        self.next_token = next_token
        self.sort_field = sort_field
        self.sort_order = sort_order

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        if self.status is not None:
            result['Status'] = self.status
        if self.start_date_before is not None:
            result['StartDateBefore'] = self.start_date_before
        if self.start_date_after is not None:
            result['StartDateAfter'] = self.start_date_after
        if self.end_date_before is not None:
            result['EndDateBefore'] = self.end_date_before
        if self.end_date_after is not None:
            result['EndDateAfter'] = self.end_date_after
        if self.task_execution_id is not None:
            result['TaskExecutionId'] = self.task_execution_id
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.task_action is not None:
            result['TaskAction'] = self.task_action
        if self.parent_task_execution_id is not None:
            result['ParentTaskExecutionId'] = self.parent_task_execution_id
        if self.include_child_task_execution is not None:
            result['IncludeChildTaskExecution'] = self.include_child_task_execution
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.sort_field is not None:
            result['SortField'] = self.sort_field
        if self.sort_order is not None:
            result['SortOrder'] = self.sort_order
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('StartDateBefore') is not None:
            self.start_date_before = m.get('StartDateBefore')
        if m.get('StartDateAfter') is not None:
            self.start_date_after = m.get('StartDateAfter')
        if m.get('EndDateBefore') is not None:
            self.end_date_before = m.get('EndDateBefore')
        if m.get('EndDateAfter') is not None:
            self.end_date_after = m.get('EndDateAfter')
        if m.get('TaskExecutionId') is not None:
            self.task_execution_id = m.get('TaskExecutionId')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('TaskAction') is not None:
            self.task_action = m.get('TaskAction')
        if m.get('ParentTaskExecutionId') is not None:
            self.parent_task_execution_id = m.get('ParentTaskExecutionId')
        if m.get('IncludeChildTaskExecution') is not None:
            self.include_child_task_execution = m.get('IncludeChildTaskExecution')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('SortField') is not None:
            self.sort_field = m.get('SortField')
        if m.get('SortOrder') is not None:
            self.sort_order = m.get('SortOrder')
        return self


class ListTaskExecutionsResponseBodyTaskExecutions(TeaModel):
    def __init__(
        self,
        child_execution_id: str = None,
        outputs: str = None,
        status: str = None,
        end_date: str = None,
        parent_task_execution_id: str = None,
        task_name: str = None,
        start_date: str = None,
        loop_item: str = None,
        create_date: str = None,
        execution_id: str = None,
        task_action: str = None,
        task_execution_id: str = None,
        update_date: str = None,
        loop: Dict[str, Any] = None,
        template_id: str = None,
        loop_batch_number: int = None,
        status_message: str = None,
        extra_data: Dict[str, Any] = None,
        properties: str = None,
    ):
        self.child_execution_id = child_execution_id
        self.outputs = outputs
        self.status = status
        self.end_date = end_date
        self.parent_task_execution_id = parent_task_execution_id
        self.task_name = task_name
        self.start_date = start_date
        self.loop_item = loop_item
        self.create_date = create_date
        self.execution_id = execution_id
        self.task_action = task_action
        self.task_execution_id = task_execution_id
        self.update_date = update_date
        self.loop = loop
        self.template_id = template_id
        self.loop_batch_number = loop_batch_number
        self.status_message = status_message
        self.extra_data = extra_data
        self.properties = properties

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.child_execution_id is not None:
            result['ChildExecutionId'] = self.child_execution_id
        if self.outputs is not None:
            result['Outputs'] = self.outputs
        if self.status is not None:
            result['Status'] = self.status
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        if self.parent_task_execution_id is not None:
            result['ParentTaskExecutionId'] = self.parent_task_execution_id
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.loop_item is not None:
            result['LoopItem'] = self.loop_item
        if self.create_date is not None:
            result['CreateDate'] = self.create_date
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        if self.task_action is not None:
            result['TaskAction'] = self.task_action
        if self.task_execution_id is not None:
            result['TaskExecutionId'] = self.task_execution_id
        if self.update_date is not None:
            result['UpdateDate'] = self.update_date
        if self.loop is not None:
            result['Loop'] = self.loop
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        if self.loop_batch_number is not None:
            result['LoopBatchNumber'] = self.loop_batch_number
        if self.status_message is not None:
            result['StatusMessage'] = self.status_message
        if self.extra_data is not None:
            result['ExtraData'] = self.extra_data
        if self.properties is not None:
            result['Properties'] = self.properties
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ChildExecutionId') is not None:
            self.child_execution_id = m.get('ChildExecutionId')
        if m.get('Outputs') is not None:
            self.outputs = m.get('Outputs')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        if m.get('ParentTaskExecutionId') is not None:
            self.parent_task_execution_id = m.get('ParentTaskExecutionId')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('LoopItem') is not None:
            self.loop_item = m.get('LoopItem')
        if m.get('CreateDate') is not None:
            self.create_date = m.get('CreateDate')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        if m.get('TaskAction') is not None:
            self.task_action = m.get('TaskAction')
        if m.get('TaskExecutionId') is not None:
            self.task_execution_id = m.get('TaskExecutionId')
        if m.get('UpdateDate') is not None:
            self.update_date = m.get('UpdateDate')
        if m.get('Loop') is not None:
            self.loop = m.get('Loop')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        if m.get('LoopBatchNumber') is not None:
            self.loop_batch_number = m.get('LoopBatchNumber')
        if m.get('StatusMessage') is not None:
            self.status_message = m.get('StatusMessage')
        if m.get('ExtraData') is not None:
            self.extra_data = m.get('ExtraData')
        if m.get('Properties') is not None:
            self.properties = m.get('Properties')
        return self


class ListTaskExecutionsResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        task_executions: List[ListTaskExecutionsResponseBodyTaskExecutions] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.task_executions = task_executions

    def validate(self):
        if self.task_executions:
            for k in self.task_executions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['TaskExecutions'] = []
        if self.task_executions is not None:
            for k in self.task_executions:
                result['TaskExecutions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.task_executions = []
        if m.get('TaskExecutions') is not None:
            for k in m.get('TaskExecutions'):
                temp_model = ListTaskExecutionsResponseBodyTaskExecutions()
                self.task_executions.append(temp_model.from_map(k))
        return self


class ListTaskExecutionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListTaskExecutionsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListTaskExecutionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTemplatesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        template_format: str = None,
        share_type: str = None,
        created_by: str = None,
        created_date_before: str = None,
        created_date_after: str = None,
        tags: Dict[str, Any] = None,
        category: str = None,
        max_results: int = None,
        next_token: str = None,
        sort_field: str = None,
        sort_order: str = None,
        has_trigger: bool = None,
        template_type: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.template_format = template_format
        self.share_type = share_type
        self.created_by = created_by
        self.created_date_before = created_date_before
        self.created_date_after = created_date_after
        self.tags = tags
        self.category = category
        self.max_results = max_results
        self.next_token = next_token
        self.sort_field = sort_field
        self.sort_order = sort_order
        self.has_trigger = has_trigger
        self.template_type = template_type
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_format is not None:
            result['TemplateFormat'] = self.template_format
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date_before is not None:
            result['CreatedDateBefore'] = self.created_date_before
        if self.created_date_after is not None:
            result['CreatedDateAfter'] = self.created_date_after
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.category is not None:
            result['Category'] = self.category
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.sort_field is not None:
            result['SortField'] = self.sort_field
        if self.sort_order is not None:
            result['SortOrder'] = self.sort_order
        if self.has_trigger is not None:
            result['HasTrigger'] = self.has_trigger
        if self.template_type is not None:
            result['TemplateType'] = self.template_type
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateFormat') is not None:
            self.template_format = m.get('TemplateFormat')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDateBefore') is not None:
            self.created_date_before = m.get('CreatedDateBefore')
        if m.get('CreatedDateAfter') is not None:
            self.created_date_after = m.get('CreatedDateAfter')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('SortField') is not None:
            self.sort_field = m.get('SortField')
        if m.get('SortOrder') is not None:
            self.sort_order = m.get('SortOrder')
        if m.get('HasTrigger') is not None:
            self.has_trigger = m.get('HasTrigger')
        if m.get('TemplateType') is not None:
            self.template_type = m.get('TemplateType')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class ListTemplatesShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        template_format: str = None,
        share_type: str = None,
        created_by: str = None,
        created_date_before: str = None,
        created_date_after: str = None,
        tags_shrink: str = None,
        category: str = None,
        max_results: int = None,
        next_token: str = None,
        sort_field: str = None,
        sort_order: str = None,
        has_trigger: bool = None,
        template_type: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.template_format = template_format
        self.share_type = share_type
        self.created_by = created_by
        self.created_date_before = created_date_before
        self.created_date_after = created_date_after
        self.tags_shrink = tags_shrink
        self.category = category
        self.max_results = max_results
        self.next_token = next_token
        self.sort_field = sort_field
        self.sort_order = sort_order
        self.has_trigger = has_trigger
        self.template_type = template_type
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_format is not None:
            result['TemplateFormat'] = self.template_format
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date_before is not None:
            result['CreatedDateBefore'] = self.created_date_before
        if self.created_date_after is not None:
            result['CreatedDateAfter'] = self.created_date_after
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        if self.category is not None:
            result['Category'] = self.category
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.sort_field is not None:
            result['SortField'] = self.sort_field
        if self.sort_order is not None:
            result['SortOrder'] = self.sort_order
        if self.has_trigger is not None:
            result['HasTrigger'] = self.has_trigger
        if self.template_type is not None:
            result['TemplateType'] = self.template_type
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateFormat') is not None:
            self.template_format = m.get('TemplateFormat')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDateBefore') is not None:
            self.created_date_before = m.get('CreatedDateBefore')
        if m.get('CreatedDateAfter') is not None:
            self.created_date_after = m.get('CreatedDateAfter')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('SortField') is not None:
            self.sort_field = m.get('SortField')
        if m.get('SortOrder') is not None:
            self.sort_order = m.get('SortOrder')
        if m.get('HasTrigger') is not None:
            self.has_trigger = m.get('HasTrigger')
        if m.get('TemplateType') is not None:
            self.template_type = m.get('TemplateType')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class ListTemplatesResponseBodyTemplates(TeaModel):
    def __init__(
        self,
        hash: str = None,
        updated_date: str = None,
        updated_by: str = None,
        template_type: str = None,
        tags: Dict[str, Any] = None,
        template_name: str = None,
        template_version: str = None,
        template_format: str = None,
        popularity: int = None,
        total_execution_count: int = None,
        description: str = None,
        resource_group_id: str = None,
        created_by: str = None,
        created_date: str = None,
        category: str = None,
        has_trigger: bool = None,
        template_id: str = None,
        share_type: str = None,
    ):
        self.hash = hash
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.template_type = template_type
        self.tags = tags
        self.template_name = template_name
        self.template_version = template_version
        self.template_format = template_format
        self.popularity = popularity
        self.total_execution_count = total_execution_count
        self.description = description
        self.resource_group_id = resource_group_id
        self.created_by = created_by
        self.created_date = created_date
        self.category = category
        self.has_trigger = has_trigger
        self.template_id = template_id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.hash is not None:
            result['Hash'] = self.hash
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.template_type is not None:
            result['TemplateType'] = self.template_type
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.template_format is not None:
            result['TemplateFormat'] = self.template_format
        if self.popularity is not None:
            result['Popularity'] = self.popularity
        if self.total_execution_count is not None:
            result['TotalExecutionCount'] = self.total_execution_count
        if self.description is not None:
            result['Description'] = self.description
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.category is not None:
            result['Category'] = self.category
        if self.has_trigger is not None:
            result['HasTrigger'] = self.has_trigger
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Hash') is not None:
            self.hash = m.get('Hash')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('TemplateType') is not None:
            self.template_type = m.get('TemplateType')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('TemplateFormat') is not None:
            self.template_format = m.get('TemplateFormat')
        if m.get('Popularity') is not None:
            self.popularity = m.get('Popularity')
        if m.get('TotalExecutionCount') is not None:
            self.total_execution_count = m.get('TotalExecutionCount')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('HasTrigger') is not None:
            self.has_trigger = m.get('HasTrigger')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class ListTemplatesResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        templates: List[ListTemplatesResponseBodyTemplates] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.templates = templates

    def validate(self):
        if self.templates:
            for k in self.templates:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['Templates'] = []
        if self.templates is not None:
            for k in self.templates:
                result['Templates'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.templates = []
        if m.get('Templates') is not None:
            for k in m.get('Templates'):
                temp_model = ListTemplatesResponseBodyTemplates()
                self.templates.append(temp_model.from_map(k))
        return self


class ListTemplatesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListTemplatesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListTemplatesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTemplateVersionsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        max_results: int = None,
        next_token: str = None,
        share_type: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.max_results = max_results
        self.next_token = next_token
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class ListTemplateVersionsResponseBodyTemplateVersions(TeaModel):
    def __init__(
        self,
        description: str = None,
        updated_date: str = None,
        updated_by: str = None,
        version_name: str = None,
        template_version: str = None,
        template_format: str = None,
    ):
        self.description = description
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.version_name = version_name
        self.template_version = template_version
        self.template_format = template_format

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.version_name is not None:
            result['VersionName'] = self.version_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.template_format is not None:
            result['TemplateFormat'] = self.template_format
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('VersionName') is not None:
            self.version_name = m.get('VersionName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('TemplateFormat') is not None:
            self.template_format = m.get('TemplateFormat')
        return self


class ListTemplateVersionsResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        template_versions: List[ListTemplateVersionsResponseBodyTemplateVersions] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.template_versions = template_versions

    def validate(self):
        if self.template_versions:
            for k in self.template_versions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['TemplateVersions'] = []
        if self.template_versions is not None:
            for k in self.template_versions:
                result['TemplateVersions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.template_versions = []
        if m.get('TemplateVersions') is not None:
            for k in m.get('TemplateVersions'):
                temp_model = ListTemplateVersionsResponseBodyTemplateVersions()
                self.template_versions.append(temp_model.from_map(k))
        return self


class ListTemplateVersionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListTemplateVersionsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListTemplateVersionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class NotifyExecutionRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        execution_id: str = None,
        notify_type: str = None,
        notify_note: str = None,
        task_name: str = None,
        task_execution_id: str = None,
        execution_status: str = None,
        parameters: str = None,
        loop_item: str = None,
        task_execution_ids: str = None,
    ):
        self.region_id = region_id
        self.execution_id = execution_id
        self.notify_type = notify_type
        self.notify_note = notify_note
        self.task_name = task_name
        self.task_execution_id = task_execution_id
        self.execution_status = execution_status
        self.parameters = parameters
        self.loop_item = loop_item
        self.task_execution_ids = task_execution_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        if self.notify_type is not None:
            result['NotifyType'] = self.notify_type
        if self.notify_note is not None:
            result['NotifyNote'] = self.notify_note
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.task_execution_id is not None:
            result['TaskExecutionId'] = self.task_execution_id
        if self.execution_status is not None:
            result['ExecutionStatus'] = self.execution_status
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        if self.loop_item is not None:
            result['LoopItem'] = self.loop_item
        if self.task_execution_ids is not None:
            result['TaskExecutionIds'] = self.task_execution_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        if m.get('NotifyType') is not None:
            self.notify_type = m.get('NotifyType')
        if m.get('NotifyNote') is not None:
            self.notify_note = m.get('NotifyNote')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('TaskExecutionId') is not None:
            self.task_execution_id = m.get('TaskExecutionId')
        if m.get('ExecutionStatus') is not None:
            self.execution_status = m.get('ExecutionStatus')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        if m.get('LoopItem') is not None:
            self.loop_item = m.get('LoopItem')
        if m.get('TaskExecutionIds') is not None:
            self.task_execution_ids = m.get('TaskExecutionIds')
        return self


class NotifyExecutionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class NotifyExecutionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: NotifyExecutionResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = NotifyExecutionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RegisterDefaultPatchBaselineRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
    ):
        self.region_id = region_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class RegisterDefaultPatchBaselineResponseBodyPatchBaseline(TeaModel):
    def __init__(
        self,
        operation_system: str = None,
        description: str = None,
        updated_date: str = None,
        updated_by: str = None,
        created_by: str = None,
        created_date: str = None,
        name: str = None,
        approval_rules: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.operation_system = operation_system
        self.description = description
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.created_by = created_by
        self.created_date = created_date
        self.name = name
        self.approval_rules = approval_rules
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.operation_system is not None:
            result['OperationSystem'] = self.operation_system
        if self.description is not None:
            result['Description'] = self.description
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.name is not None:
            result['Name'] = self.name
        if self.approval_rules is not None:
            result['ApprovalRules'] = self.approval_rules
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OperationSystem') is not None:
            self.operation_system = m.get('OperationSystem')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ApprovalRules') is not None:
            self.approval_rules = m.get('ApprovalRules')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class RegisterDefaultPatchBaselineResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        patch_baseline: RegisterDefaultPatchBaselineResponseBodyPatchBaseline = None,
    ):
        self.request_id = request_id
        self.patch_baseline = patch_baseline

    def validate(self):
        if self.patch_baseline:
            self.patch_baseline.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.patch_baseline is not None:
            result['PatchBaseline'] = self.patch_baseline.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PatchBaseline') is not None:
            temp_model = RegisterDefaultPatchBaselineResponseBodyPatchBaseline()
            self.patch_baseline = temp_model.from_map(m['PatchBaseline'])
        return self


class RegisterDefaultPatchBaselineResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RegisterDefaultPatchBaselineResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RegisterDefaultPatchBaselineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SearchInventoryRequestFilter(TeaModel):
    def __init__(
        self,
        value: List[str] = None,
        operator: str = None,
        name: str = None,
    ):
        self.value = value
        self.operator = operator
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.operator is not None:
            result['Operator'] = self.operator
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Operator') is not None:
            self.operator = m.get('Operator')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class SearchInventoryRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        next_token: str = None,
        max_results: int = None,
        filter: List[SearchInventoryRequestFilter] = None,
        aggregator: List[str] = None,
    ):
        self.region_id = region_id
        self.next_token = next_token
        self.max_results = max_results
        self.filter = filter
        self.aggregator = aggregator

    def validate(self):
        if self.filter:
            for k in self.filter:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['Filter'] = []
        if self.filter is not None:
            for k in self.filter:
                result['Filter'].append(k.to_map() if k else None)
        if self.aggregator is not None:
            result['Aggregator'] = self.aggregator
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.filter = []
        if m.get('Filter') is not None:
            for k in m.get('Filter'):
                temp_model = SearchInventoryRequestFilter()
                self.filter.append(temp_model.from_map(k))
        if m.get('Aggregator') is not None:
            self.aggregator = m.get('Aggregator')
        return self


class SearchInventoryResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        max_results: int = None,
        entities: List[Dict[str, Any]] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.max_results = max_results
        self.entities = entities

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        if self.entities is not None:
            result['Entities'] = self.entities
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        if m.get('Entities') is not None:
            self.entities = m.get('Entities')
        return self


class SearchInventoryResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SearchInventoryResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SearchInventoryResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetServiceSettingsRequest(TeaModel):
    def __init__(
        self,
        delivery_oss_enabled: bool = None,
        delivery_oss_bucket_name: str = None,
        delivery_oss_key_prefix: str = None,
        delivery_sls_project_name: str = None,
        delivery_sls_enabled: bool = None,
        region_id: str = None,
        rdc_enterprise_id: str = None,
    ):
        self.delivery_oss_enabled = delivery_oss_enabled
        self.delivery_oss_bucket_name = delivery_oss_bucket_name
        self.delivery_oss_key_prefix = delivery_oss_key_prefix
        self.delivery_sls_project_name = delivery_sls_project_name
        self.delivery_sls_enabled = delivery_sls_enabled
        self.region_id = region_id
        self.rdc_enterprise_id = rdc_enterprise_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.delivery_oss_enabled is not None:
            result['DeliveryOssEnabled'] = self.delivery_oss_enabled
        if self.delivery_oss_bucket_name is not None:
            result['DeliveryOssBucketName'] = self.delivery_oss_bucket_name
        if self.delivery_oss_key_prefix is not None:
            result['DeliveryOssKeyPrefix'] = self.delivery_oss_key_prefix
        if self.delivery_sls_project_name is not None:
            result['DeliverySlsProjectName'] = self.delivery_sls_project_name
        if self.delivery_sls_enabled is not None:
            result['DeliverySlsEnabled'] = self.delivery_sls_enabled
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.rdc_enterprise_id is not None:
            result['RdcEnterpriseId'] = self.rdc_enterprise_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DeliveryOssEnabled') is not None:
            self.delivery_oss_enabled = m.get('DeliveryOssEnabled')
        if m.get('DeliveryOssBucketName') is not None:
            self.delivery_oss_bucket_name = m.get('DeliveryOssBucketName')
        if m.get('DeliveryOssKeyPrefix') is not None:
            self.delivery_oss_key_prefix = m.get('DeliveryOssKeyPrefix')
        if m.get('DeliverySlsProjectName') is not None:
            self.delivery_sls_project_name = m.get('DeliverySlsProjectName')
        if m.get('DeliverySlsEnabled') is not None:
            self.delivery_sls_enabled = m.get('DeliverySlsEnabled')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('RdcEnterpriseId') is not None:
            self.rdc_enterprise_id = m.get('RdcEnterpriseId')
        return self


class SetServiceSettingsResponseBodyServiceSettings(TeaModel):
    def __init__(
        self,
        delivery_oss_bucket_name: str = None,
        delivery_oss_key_prefix: str = None,
        delivery_oss_enabled: bool = None,
        delivery_sls_enabled: bool = None,
        delivery_sls_project_name: str = None,
        rdc_enterprise_id: str = None,
    ):
        self.delivery_oss_bucket_name = delivery_oss_bucket_name
        self.delivery_oss_key_prefix = delivery_oss_key_prefix
        self.delivery_oss_enabled = delivery_oss_enabled
        self.delivery_sls_enabled = delivery_sls_enabled
        self.delivery_sls_project_name = delivery_sls_project_name
        self.rdc_enterprise_id = rdc_enterprise_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.delivery_oss_bucket_name is not None:
            result['DeliveryOssBucketName'] = self.delivery_oss_bucket_name
        if self.delivery_oss_key_prefix is not None:
            result['DeliveryOssKeyPrefix'] = self.delivery_oss_key_prefix
        if self.delivery_oss_enabled is not None:
            result['DeliveryOssEnabled'] = self.delivery_oss_enabled
        if self.delivery_sls_enabled is not None:
            result['DeliverySlsEnabled'] = self.delivery_sls_enabled
        if self.delivery_sls_project_name is not None:
            result['DeliverySlsProjectName'] = self.delivery_sls_project_name
        if self.rdc_enterprise_id is not None:
            result['RdcEnterpriseId'] = self.rdc_enterprise_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DeliveryOssBucketName') is not None:
            self.delivery_oss_bucket_name = m.get('DeliveryOssBucketName')
        if m.get('DeliveryOssKeyPrefix') is not None:
            self.delivery_oss_key_prefix = m.get('DeliveryOssKeyPrefix')
        if m.get('DeliveryOssEnabled') is not None:
            self.delivery_oss_enabled = m.get('DeliveryOssEnabled')
        if m.get('DeliverySlsEnabled') is not None:
            self.delivery_sls_enabled = m.get('DeliverySlsEnabled')
        if m.get('DeliverySlsProjectName') is not None:
            self.delivery_sls_project_name = m.get('DeliverySlsProjectName')
        if m.get('RdcEnterpriseId') is not None:
            self.rdc_enterprise_id = m.get('RdcEnterpriseId')
        return self


class SetServiceSettingsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        service_settings: List[SetServiceSettingsResponseBodyServiceSettings] = None,
    ):
        self.request_id = request_id
        self.service_settings = service_settings

    def validate(self):
        if self.service_settings:
            for k in self.service_settings:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['ServiceSettings'] = []
        if self.service_settings is not None:
            for k in self.service_settings:
                result['ServiceSettings'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.service_settings = []
        if m.get('ServiceSettings') is not None:
            for k in m.get('ServiceSettings'):
                temp_model = SetServiceSettingsResponseBodyServiceSettings()
                self.service_settings.append(temp_model.from_map(k))
        return self


class SetServiceSettingsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetServiceSettingsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetServiceSettingsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartExecutionRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        template_version: str = None,
        mode: str = None,
        loop_mode: str = None,
        parent_execution_id: str = None,
        safety_check: str = None,
        parameters: str = None,
        client_token: str = None,
        tags: Dict[str, Any] = None,
        description: str = None,
        template_content: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.template_version = template_version
        self.mode = mode
        self.loop_mode = loop_mode
        self.parent_execution_id = parent_execution_id
        self.safety_check = safety_check
        self.parameters = parameters
        self.client_token = client_token
        self.tags = tags
        self.description = description
        self.template_content = template_content
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.loop_mode is not None:
            result['LoopMode'] = self.loop_mode
        if self.parent_execution_id is not None:
            result['ParentExecutionId'] = self.parent_execution_id
        if self.safety_check is not None:
            result['SafetyCheck'] = self.safety_check
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.description is not None:
            result['Description'] = self.description
        if self.template_content is not None:
            result['TemplateContent'] = self.template_content
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('LoopMode') is not None:
            self.loop_mode = m.get('LoopMode')
        if m.get('ParentExecutionId') is not None:
            self.parent_execution_id = m.get('ParentExecutionId')
        if m.get('SafetyCheck') is not None:
            self.safety_check = m.get('SafetyCheck')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('TemplateContent') is not None:
            self.template_content = m.get('TemplateContent')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class StartExecutionShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        template_version: str = None,
        mode: str = None,
        loop_mode: str = None,
        parent_execution_id: str = None,
        safety_check: str = None,
        parameters: str = None,
        client_token: str = None,
        tags_shrink: str = None,
        description: str = None,
        template_content: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.template_version = template_version
        self.mode = mode
        self.loop_mode = loop_mode
        self.parent_execution_id = parent_execution_id
        self.safety_check = safety_check
        self.parameters = parameters
        self.client_token = client_token
        self.tags_shrink = tags_shrink
        self.description = description
        self.template_content = template_content
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.loop_mode is not None:
            result['LoopMode'] = self.loop_mode
        if self.parent_execution_id is not None:
            result['ParentExecutionId'] = self.parent_execution_id
        if self.safety_check is not None:
            result['SafetyCheck'] = self.safety_check
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        if self.description is not None:
            result['Description'] = self.description
        if self.template_content is not None:
            result['TemplateContent'] = self.template_content
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('LoopMode') is not None:
            self.loop_mode = m.get('LoopMode')
        if m.get('ParentExecutionId') is not None:
            self.parent_execution_id = m.get('ParentExecutionId')
        if m.get('SafetyCheck') is not None:
            self.safety_check = m.get('SafetyCheck')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('TemplateContent') is not None:
            self.template_content = m.get('TemplateContent')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class StartExecutionResponseBodyExecutionCurrentTasks(TeaModel):
    def __init__(
        self,
        task_execution_id: str = None,
        task_name: str = None,
        task_action: str = None,
    ):
        self.task_execution_id = task_execution_id
        self.task_name = task_name
        self.task_action = task_action

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.task_execution_id is not None:
            result['TaskExecutionId'] = self.task_execution_id
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.task_action is not None:
            result['TaskAction'] = self.task_action
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskExecutionId') is not None:
            self.task_execution_id = m.get('TaskExecutionId')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('TaskAction') is not None:
            self.task_action = m.get('TaskAction')
        return self


class StartExecutionResponseBodyExecution(TeaModel):
    def __init__(
        self,
        outputs: str = None,
        status: str = None,
        end_date: str = None,
        executed_by: str = None,
        is_parent: bool = None,
        tags: Dict[str, Any] = None,
        start_date: str = None,
        safety_check: str = None,
        mode: str = None,
        template_name: str = None,
        create_date: str = None,
        template_version: str = None,
        execution_id: str = None,
        parameters: str = None,
        description: str = None,
        counters: Dict[str, Any] = None,
        update_date: str = None,
        resource_group_id: str = None,
        parent_execution_id: str = None,
        ram_role: str = None,
        template_id: str = None,
        status_message: str = None,
        loop_mode: str = None,
        current_tasks: List[StartExecutionResponseBodyExecutionCurrentTasks] = None,
    ):
        self.outputs = outputs
        self.status = status
        self.end_date = end_date
        self.executed_by = executed_by
        self.is_parent = is_parent
        self.tags = tags
        self.start_date = start_date
        self.safety_check = safety_check
        self.mode = mode
        self.template_name = template_name
        self.create_date = create_date
        self.template_version = template_version
        self.execution_id = execution_id
        self.parameters = parameters
        self.description = description
        self.counters = counters
        self.update_date = update_date
        self.resource_group_id = resource_group_id
        self.parent_execution_id = parent_execution_id
        self.ram_role = ram_role
        self.template_id = template_id
        self.status_message = status_message
        self.loop_mode = loop_mode
        self.current_tasks = current_tasks

    def validate(self):
        if self.current_tasks:
            for k in self.current_tasks:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.outputs is not None:
            result['Outputs'] = self.outputs
        if self.status is not None:
            result['Status'] = self.status
        if self.end_date is not None:
            result['EndDate'] = self.end_date
        if self.executed_by is not None:
            result['ExecutedBy'] = self.executed_by
        if self.is_parent is not None:
            result['IsParent'] = self.is_parent
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.start_date is not None:
            result['StartDate'] = self.start_date
        if self.safety_check is not None:
            result['SafetyCheck'] = self.safety_check
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.create_date is not None:
            result['CreateDate'] = self.create_date
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        if self.description is not None:
            result['Description'] = self.description
        if self.counters is not None:
            result['Counters'] = self.counters
        if self.update_date is not None:
            result['UpdateDate'] = self.update_date
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.parent_execution_id is not None:
            result['ParentExecutionId'] = self.parent_execution_id
        if self.ram_role is not None:
            result['RamRole'] = self.ram_role
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        if self.status_message is not None:
            result['StatusMessage'] = self.status_message
        if self.loop_mode is not None:
            result['LoopMode'] = self.loop_mode
        result['CurrentTasks'] = []
        if self.current_tasks is not None:
            for k in self.current_tasks:
                result['CurrentTasks'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Outputs') is not None:
            self.outputs = m.get('Outputs')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('EndDate') is not None:
            self.end_date = m.get('EndDate')
        if m.get('ExecutedBy') is not None:
            self.executed_by = m.get('ExecutedBy')
        if m.get('IsParent') is not None:
            self.is_parent = m.get('IsParent')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('StartDate') is not None:
            self.start_date = m.get('StartDate')
        if m.get('SafetyCheck') is not None:
            self.safety_check = m.get('SafetyCheck')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('CreateDate') is not None:
            self.create_date = m.get('CreateDate')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Counters') is not None:
            self.counters = m.get('Counters')
        if m.get('UpdateDate') is not None:
            self.update_date = m.get('UpdateDate')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('ParentExecutionId') is not None:
            self.parent_execution_id = m.get('ParentExecutionId')
        if m.get('RamRole') is not None:
            self.ram_role = m.get('RamRole')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        if m.get('StatusMessage') is not None:
            self.status_message = m.get('StatusMessage')
        if m.get('LoopMode') is not None:
            self.loop_mode = m.get('LoopMode')
        self.current_tasks = []
        if m.get('CurrentTasks') is not None:
            for k in m.get('CurrentTasks'):
                temp_model = StartExecutionResponseBodyExecutionCurrentTasks()
                self.current_tasks.append(temp_model.from_map(k))
        return self


class StartExecutionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        execution: StartExecutionResponseBodyExecution = None,
    ):
        self.request_id = request_id
        self.execution = execution

    def validate(self):
        if self.execution:
            self.execution.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.execution is not None:
            result['Execution'] = self.execution.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Execution') is not None:
            temp_model = StartExecutionResponseBodyExecution()
            self.execution = temp_model.from_map(m['Execution'])
        return self


class StartExecutionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: StartExecutionResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = StartExecutionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class TagResourcesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        resource_ids: Dict[str, Any] = None,
        resource_type: str = None,
        tags: Dict[str, Any] = None,
    ):
        self.region_id = region_id
        self.resource_ids = resource_ids
        self.resource_type = resource_type
        self.tags = tags

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_ids is not None:
            result['ResourceIds'] = self.resource_ids
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tags is not None:
            result['Tags'] = self.tags
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceIds') is not None:
            self.resource_ids = m.get('ResourceIds')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        return self


class TagResourcesShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        resource_ids_shrink: str = None,
        resource_type: str = None,
        tags_shrink: str = None,
    ):
        self.region_id = region_id
        self.resource_ids_shrink = resource_ids_shrink
        self.resource_type = resource_type
        self.tags_shrink = tags_shrink

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_ids_shrink is not None:
            result['ResourceIds'] = self.resource_ids_shrink
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceIds') is not None:
            self.resource_ids_shrink = m.get('ResourceIds')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        return self


class TagResourcesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class TagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: TagResourcesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = TagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class TriggerExecutionRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        execution_id: str = None,
        type: str = None,
        content: str = None,
        client_token: str = None,
    ):
        self.region_id = region_id
        self.execution_id = execution_id
        self.type = type
        self.content = content
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        if self.type is not None:
            result['Type'] = self.type
        if self.content is not None:
            result['Content'] = self.content
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        return self


class TriggerExecutionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class TriggerExecutionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: TriggerExecutionResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = TriggerExecutionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UntagResourcesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        resource_ids: Dict[str, Any] = None,
        resource_type: str = None,
        tag_keys: Dict[str, Any] = None,
        all: bool = None,
    ):
        self.region_id = region_id
        self.resource_ids = resource_ids
        self.resource_type = resource_type
        self.tag_keys = tag_keys
        self.all = all

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_ids is not None:
            result['ResourceIds'] = self.resource_ids
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tag_keys is not None:
            result['TagKeys'] = self.tag_keys
        if self.all is not None:
            result['All'] = self.all
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceIds') is not None:
            self.resource_ids = m.get('ResourceIds')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('TagKeys') is not None:
            self.tag_keys = m.get('TagKeys')
        if m.get('All') is not None:
            self.all = m.get('All')
        return self


class UntagResourcesShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        resource_ids_shrink: str = None,
        resource_type: str = None,
        tag_keys_shrink: str = None,
        all: bool = None,
    ):
        self.region_id = region_id
        self.resource_ids_shrink = resource_ids_shrink
        self.resource_type = resource_type
        self.tag_keys_shrink = tag_keys_shrink
        self.all = all

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_ids_shrink is not None:
            result['ResourceIds'] = self.resource_ids_shrink
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tag_keys_shrink is not None:
            result['TagKeys'] = self.tag_keys_shrink
        if self.all is not None:
            result['All'] = self.all
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceIds') is not None:
            self.resource_ids_shrink = m.get('ResourceIds')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('TagKeys') is not None:
            self.tag_keys_shrink = m.get('TagKeys')
        if m.get('All') is not None:
            self.all = m.get('All')
        return self


class UntagResourcesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UntagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UntagResourcesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UntagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateApplicationGroupRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        scaling_group_id: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.scaling_group_id = scaling_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.scaling_group_id is not None:
            result['ScalingGroupId'] = self.scaling_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ScalingGroupId') is not None:
            self.scaling_group_id = m.get('ScalingGroupId')
        return self


class UpdateApplicationGroupResponseBodyApplicationGroup(TeaModel):
    def __init__(
        self,
        deploy_region_id: str = None,
        description: str = None,
        updated_date: str = None,
        created_date: str = None,
        application_name: str = None,
        name: str = None,
        environment: str = None,
        create_type: str = None,
        scaling_group_id: str = None,
        import_cluster_id: str = None,
    ):
        self.deploy_region_id = deploy_region_id
        self.description = description
        self.updated_date = updated_date
        self.created_date = created_date
        self.application_name = application_name
        self.name = name
        self.environment = environment
        self.create_type = create_type
        self.scaling_group_id = scaling_group_id
        self.import_cluster_id = import_cluster_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.deploy_region_id is not None:
            result['DeployRegionId'] = self.deploy_region_id
        if self.description is not None:
            result['Description'] = self.description
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.application_name is not None:
            result['ApplicationName'] = self.application_name
        if self.name is not None:
            result['Name'] = self.name
        if self.environment is not None:
            result['Environment'] = self.environment
        if self.create_type is not None:
            result['CreateType'] = self.create_type
        if self.scaling_group_id is not None:
            result['ScalingGroupId'] = self.scaling_group_id
        if self.import_cluster_id is not None:
            result['ImportClusterId'] = self.import_cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DeployRegionId') is not None:
            self.deploy_region_id = m.get('DeployRegionId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ApplicationName') is not None:
            self.application_name = m.get('ApplicationName')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Environment') is not None:
            self.environment = m.get('Environment')
        if m.get('CreateType') is not None:
            self.create_type = m.get('CreateType')
        if m.get('ScalingGroupId') is not None:
            self.scaling_group_id = m.get('ScalingGroupId')
        if m.get('ImportClusterId') is not None:
            self.import_cluster_id = m.get('ImportClusterId')
        return self


class UpdateApplicationGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        application_group: UpdateApplicationGroupResponseBodyApplicationGroup = None,
    ):
        self.request_id = request_id
        self.application_group = application_group

    def validate(self):
        if self.application_group:
            self.application_group.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.application_group is not None:
            result['ApplicationGroup'] = self.application_group.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ApplicationGroup') is not None:
            temp_model = UpdateApplicationGroupResponseBodyApplicationGroup()
            self.application_group = temp_model.from_map(m['ApplicationGroup'])
        return self


class UpdateApplicationGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateApplicationGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateApplicationGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateExecutionRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        execution_id: str = None,
        parameters: str = None,
        client_token: str = None,
    ):
        self.region_id = region_id
        self.execution_id = execution_id
        self.parameters = parameters
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.execution_id is not None:
            result['ExecutionId'] = self.execution_id
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ExecutionId') is not None:
            self.execution_id = m.get('ExecutionId')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        return self


class UpdateExecutionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateExecutionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateExecutionResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateExecutionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateInstanceInformationRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        instance_id: str = None,
        agent_version: str = None,
        platform_type: str = None,
        platform_name: str = None,
        platform_version: str = None,
        ip_address: str = None,
        computer_name: str = None,
        agent_name: str = None,
    ):
        self.region_id = region_id
        self.instance_id = instance_id
        self.agent_version = agent_version
        self.platform_type = platform_type
        self.platform_name = platform_name
        self.platform_version = platform_version
        self.ip_address = ip_address
        self.computer_name = computer_name
        self.agent_name = agent_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.agent_version is not None:
            result['AgentVersion'] = self.agent_version
        if self.platform_type is not None:
            result['PlatformType'] = self.platform_type
        if self.platform_name is not None:
            result['PlatformName'] = self.platform_name
        if self.platform_version is not None:
            result['PlatformVersion'] = self.platform_version
        if self.ip_address is not None:
            result['IpAddress'] = self.ip_address
        if self.computer_name is not None:
            result['ComputerName'] = self.computer_name
        if self.agent_name is not None:
            result['AgentName'] = self.agent_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('AgentVersion') is not None:
            self.agent_version = m.get('AgentVersion')
        if m.get('PlatformType') is not None:
            self.platform_type = m.get('PlatformType')
        if m.get('PlatformName') is not None:
            self.platform_name = m.get('PlatformName')
        if m.get('PlatformVersion') is not None:
            self.platform_version = m.get('PlatformVersion')
        if m.get('IpAddress') is not None:
            self.ip_address = m.get('IpAddress')
        if m.get('ComputerName') is not None:
            self.computer_name = m.get('ComputerName')
        if m.get('AgentName') is not None:
            self.agent_name = m.get('AgentName')
        return self


class UpdateInstanceInformationResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateInstanceInformationResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateInstanceInformationResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateInstanceInformationResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateParameterRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        value: str = None,
        description: str = None,
        tags: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.value = value
        self.description = description
        self.tags = tags
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.value is not None:
            result['Value'] = self.value
        if self.description is not None:
            result['Description'] = self.description
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class UpdateParameterResponseBodyParameter(TeaModel):
    def __init__(
        self,
        type: str = None,
        updated_date: str = None,
        updated_by: str = None,
        tags: str = None,
        description: str = None,
        constraints: str = None,
        resource_group_id: str = None,
        created_by: str = None,
        created_date: str = None,
        parameter_version: int = None,
        name: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.type = type
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.tags = tags
        self.description = description
        self.constraints = constraints
        self.resource_group_id = resource_group_id
        self.created_by = created_by
        self.created_date = created_date
        self.parameter_version = parameter_version
        self.name = name
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.description is not None:
            result['Description'] = self.description
        if self.constraints is not None:
            result['Constraints'] = self.constraints
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Constraints') is not None:
            self.constraints = m.get('Constraints')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class UpdateParameterResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        parameter: UpdateParameterResponseBodyParameter = None,
    ):
        self.request_id = request_id
        self.parameter = parameter

    def validate(self):
        if self.parameter:
            self.parameter.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.parameter is not None:
            result['Parameter'] = self.parameter.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Parameter') is not None:
            temp_model = UpdateParameterResponseBodyParameter()
            self.parameter = temp_model.from_map(m['Parameter'])
        return self


class UpdateParameterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateParameterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateParameterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdatePatchBaselineRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        description: str = None,
        client_token: str = None,
        approval_rules: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.description = description
        self.client_token = client_token
        self.approval_rules = approval_rules

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.approval_rules is not None:
            result['ApprovalRules'] = self.approval_rules
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('ApprovalRules') is not None:
            self.approval_rules = m.get('ApprovalRules')
        return self


class UpdatePatchBaselineResponseBodyPatchBaseline(TeaModel):
    def __init__(
        self,
        operation_system: str = None,
        description: str = None,
        updated_date: str = None,
        updated_by: str = None,
        created_by: str = None,
        created_date: str = None,
        name: str = None,
        approval_rules: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.operation_system = operation_system
        self.description = description
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.created_by = created_by
        self.created_date = created_date
        self.name = name
        self.approval_rules = approval_rules
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.operation_system is not None:
            result['OperationSystem'] = self.operation_system
        if self.description is not None:
            result['Description'] = self.description
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.name is not None:
            result['Name'] = self.name
        if self.approval_rules is not None:
            result['ApprovalRules'] = self.approval_rules
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OperationSystem') is not None:
            self.operation_system = m.get('OperationSystem')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ApprovalRules') is not None:
            self.approval_rules = m.get('ApprovalRules')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class UpdatePatchBaselineResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        patch_baseline: UpdatePatchBaselineResponseBodyPatchBaseline = None,
    ):
        self.request_id = request_id
        self.patch_baseline = patch_baseline

    def validate(self):
        if self.patch_baseline:
            self.patch_baseline.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.patch_baseline is not None:
            result['PatchBaseline'] = self.patch_baseline.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PatchBaseline') is not None:
            temp_model = UpdatePatchBaselineResponseBodyPatchBaseline()
            self.patch_baseline = temp_model.from_map(m['PatchBaseline'])
        return self


class UpdatePatchBaselineResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdatePatchBaselineResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdatePatchBaselineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateSecretParameterRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        value: str = None,
        description: str = None,
        tags: Dict[str, Any] = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.value = value
        self.description = description
        self.tags = tags
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.value is not None:
            result['Value'] = self.value
        if self.description is not None:
            result['Description'] = self.description
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class UpdateSecretParameterShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        name: str = None,
        value: str = None,
        description: str = None,
        tags_shrink: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.name = name
        self.value = value
        self.description = description
        self.tags_shrink = tags_shrink
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.name is not None:
            result['Name'] = self.name
        if self.value is not None:
            result['Value'] = self.value
        if self.description is not None:
            result['Description'] = self.description
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class UpdateSecretParameterResponseBodyParameter(TeaModel):
    def __init__(
        self,
        type: str = None,
        updated_date: str = None,
        updated_by: str = None,
        key_id: str = None,
        tags: str = None,
        description: str = None,
        constraints: str = None,
        resource_group_id: str = None,
        created_by: str = None,
        created_date: str = None,
        parameter_version: int = None,
        name: str = None,
        id: str = None,
        share_type: str = None,
    ):
        self.type = type
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.key_id = key_id
        self.tags = tags
        self.description = description
        self.constraints = constraints
        self.resource_group_id = resource_group_id
        self.created_by = created_by
        self.created_date = created_date
        self.parameter_version = parameter_version
        self.name = name
        self.id = id
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.key_id is not None:
            result['KeyId'] = self.key_id
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.description is not None:
            result['Description'] = self.description
        if self.constraints is not None:
            result['Constraints'] = self.constraints
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.parameter_version is not None:
            result['ParameterVersion'] = self.parameter_version
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('KeyId') is not None:
            self.key_id = m.get('KeyId')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Constraints') is not None:
            self.constraints = m.get('Constraints')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('ParameterVersion') is not None:
            self.parameter_version = m.get('ParameterVersion')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class UpdateSecretParameterResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        parameter: UpdateSecretParameterResponseBodyParameter = None,
    ):
        self.request_id = request_id
        self.parameter = parameter

    def validate(self):
        if self.parameter:
            self.parameter.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.parameter is not None:
            result['Parameter'] = self.parameter.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Parameter') is not None:
            temp_model = UpdateSecretParameterResponseBodyParameter()
            self.parameter = temp_model.from_map(m['Parameter'])
        return self


class UpdateSecretParameterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateSecretParameterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateSecretParameterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateStateConfigurationRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        description: str = None,
        parameters: Dict[str, Any] = None,
        configure_mode: str = None,
        schedule_type: str = None,
        schedule_expression: str = None,
        targets: str = None,
        client_token: str = None,
        state_configuration_id: str = None,
        tags: Dict[str, Any] = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.description = description
        self.parameters = parameters
        self.configure_mode = configure_mode
        self.schedule_type = schedule_type
        self.schedule_expression = schedule_expression
        self.targets = targets
        self.client_token = client_token
        self.state_configuration_id = state_configuration_id
        self.tags = tags
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.description is not None:
            result['Description'] = self.description
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        if self.configure_mode is not None:
            result['ConfigureMode'] = self.configure_mode
        if self.schedule_type is not None:
            result['ScheduleType'] = self.schedule_type
        if self.schedule_expression is not None:
            result['ScheduleExpression'] = self.schedule_expression
        if self.targets is not None:
            result['Targets'] = self.targets
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.state_configuration_id is not None:
            result['StateConfigurationId'] = self.state_configuration_id
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        if m.get('ConfigureMode') is not None:
            self.configure_mode = m.get('ConfigureMode')
        if m.get('ScheduleType') is not None:
            self.schedule_type = m.get('ScheduleType')
        if m.get('ScheduleExpression') is not None:
            self.schedule_expression = m.get('ScheduleExpression')
        if m.get('Targets') is not None:
            self.targets = m.get('Targets')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('StateConfigurationId') is not None:
            self.state_configuration_id = m.get('StateConfigurationId')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class UpdateStateConfigurationShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        description: str = None,
        parameters_shrink: str = None,
        configure_mode: str = None,
        schedule_type: str = None,
        schedule_expression: str = None,
        targets: str = None,
        client_token: str = None,
        state_configuration_id: str = None,
        tags_shrink: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.description = description
        self.parameters_shrink = parameters_shrink
        self.configure_mode = configure_mode
        self.schedule_type = schedule_type
        self.schedule_expression = schedule_expression
        self.targets = targets
        self.client_token = client_token
        self.state_configuration_id = state_configuration_id
        self.tags_shrink = tags_shrink
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.description is not None:
            result['Description'] = self.description
        if self.parameters_shrink is not None:
            result['Parameters'] = self.parameters_shrink
        if self.configure_mode is not None:
            result['ConfigureMode'] = self.configure_mode
        if self.schedule_type is not None:
            result['ScheduleType'] = self.schedule_type
        if self.schedule_expression is not None:
            result['ScheduleExpression'] = self.schedule_expression
        if self.targets is not None:
            result['Targets'] = self.targets
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.state_configuration_id is not None:
            result['StateConfigurationId'] = self.state_configuration_id
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Parameters') is not None:
            self.parameters_shrink = m.get('Parameters')
        if m.get('ConfigureMode') is not None:
            self.configure_mode = m.get('ConfigureMode')
        if m.get('ScheduleType') is not None:
            self.schedule_type = m.get('ScheduleType')
        if m.get('ScheduleExpression') is not None:
            self.schedule_expression = m.get('ScheduleExpression')
        if m.get('Targets') is not None:
            self.targets = m.get('Targets')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('StateConfigurationId') is not None:
            self.state_configuration_id = m.get('StateConfigurationId')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class UpdateStateConfigurationResponseBodyStateConfiguration(TeaModel):
    def __init__(
        self,
        update_time: str = None,
        create_time: str = None,
        targets: str = None,
        tags: Dict[str, Any] = None,
        state_configuration_id: str = None,
        schedule_expression: str = None,
        template_name: str = None,
        template_version: str = None,
        configure_mode: str = None,
        schedule_type: str = None,
        parameters: str = None,
        description: str = None,
        resource_group_id: str = None,
        template_id: str = None,
    ):
        self.update_time = update_time
        self.create_time = create_time
        self.targets = targets
        self.tags = tags
        self.state_configuration_id = state_configuration_id
        self.schedule_expression = schedule_expression
        self.template_name = template_name
        self.template_version = template_version
        self.configure_mode = configure_mode
        self.schedule_type = schedule_type
        self.parameters = parameters
        self.description = description
        self.resource_group_id = resource_group_id
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.targets is not None:
            result['Targets'] = self.targets
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.state_configuration_id is not None:
            result['StateConfigurationId'] = self.state_configuration_id
        if self.schedule_expression is not None:
            result['ScheduleExpression'] = self.schedule_expression
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.configure_mode is not None:
            result['ConfigureMode'] = self.configure_mode
        if self.schedule_type is not None:
            result['ScheduleType'] = self.schedule_type
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        if self.description is not None:
            result['Description'] = self.description
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Targets') is not None:
            self.targets = m.get('Targets')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('StateConfigurationId') is not None:
            self.state_configuration_id = m.get('StateConfigurationId')
        if m.get('ScheduleExpression') is not None:
            self.schedule_expression = m.get('ScheduleExpression')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('ConfigureMode') is not None:
            self.configure_mode = m.get('ConfigureMode')
        if m.get('ScheduleType') is not None:
            self.schedule_type = m.get('ScheduleType')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class UpdateStateConfigurationResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        state_configuration: List[UpdateStateConfigurationResponseBodyStateConfiguration] = None,
    ):
        self.request_id = request_id
        self.state_configuration = state_configuration

    def validate(self):
        if self.state_configuration:
            for k in self.state_configuration:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['StateConfiguration'] = []
        if self.state_configuration is not None:
            for k in self.state_configuration:
                result['StateConfiguration'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.state_configuration = []
        if m.get('StateConfiguration') is not None:
            for k in m.get('StateConfiguration'):
                temp_model = UpdateStateConfigurationResponseBodyStateConfiguration()
                self.state_configuration.append(temp_model.from_map(k))
        return self


class UpdateStateConfigurationResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateStateConfigurationResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateStateConfigurationResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateTemplateRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        content: str = None,
        tags: Dict[str, Any] = None,
        version_name: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.content = content
        self.tags = tags
        self.version_name = version_name
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.content is not None:
            result['Content'] = self.content
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.version_name is not None:
            result['VersionName'] = self.version_name
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('VersionName') is not None:
            self.version_name = m.get('VersionName')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class UpdateTemplateShrinkRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        template_name: str = None,
        content: str = None,
        tags_shrink: str = None,
        version_name: str = None,
        resource_group_id: str = None,
    ):
        self.region_id = region_id
        self.template_name = template_name
        self.content = content
        self.tags_shrink = tags_shrink
        self.version_name = version_name
        self.resource_group_id = resource_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.content is not None:
            result['Content'] = self.content
        if self.tags_shrink is not None:
            result['Tags'] = self.tags_shrink
        if self.version_name is not None:
            result['VersionName'] = self.version_name
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('Tags') is not None:
            self.tags_shrink = m.get('Tags')
        if m.get('VersionName') is not None:
            self.version_name = m.get('VersionName')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        return self


class UpdateTemplateResponseBodyTemplate(TeaModel):
    def __init__(
        self,
        hash: str = None,
        updated_date: str = None,
        updated_by: str = None,
        tags: Dict[str, Any] = None,
        template_name: str = None,
        template_version: str = None,
        template_format: str = None,
        description: str = None,
        resource_group_id: str = None,
        created_by: str = None,
        created_date: str = None,
        template_id: str = None,
        has_trigger: bool = None,
        share_type: str = None,
    ):
        self.hash = hash
        self.updated_date = updated_date
        self.updated_by = updated_by
        self.tags = tags
        self.template_name = template_name
        self.template_version = template_version
        self.template_format = template_format
        self.description = description
        self.resource_group_id = resource_group_id
        self.created_by = created_by
        self.created_date = created_date
        self.template_id = template_id
        self.has_trigger = has_trigger
        self.share_type = share_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.hash is not None:
            result['Hash'] = self.hash
        if self.updated_date is not None:
            result['UpdatedDate'] = self.updated_date
        if self.updated_by is not None:
            result['UpdatedBy'] = self.updated_by
        if self.tags is not None:
            result['Tags'] = self.tags
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.template_format is not None:
            result['TemplateFormat'] = self.template_format
        if self.description is not None:
            result['Description'] = self.description
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.created_by is not None:
            result['CreatedBy'] = self.created_by
        if self.created_date is not None:
            result['CreatedDate'] = self.created_date
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        if self.has_trigger is not None:
            result['HasTrigger'] = self.has_trigger
        if self.share_type is not None:
            result['ShareType'] = self.share_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Hash') is not None:
            self.hash = m.get('Hash')
        if m.get('UpdatedDate') is not None:
            self.updated_date = m.get('UpdatedDate')
        if m.get('UpdatedBy') is not None:
            self.updated_by = m.get('UpdatedBy')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('TemplateFormat') is not None:
            self.template_format = m.get('TemplateFormat')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('CreatedBy') is not None:
            self.created_by = m.get('CreatedBy')
        if m.get('CreatedDate') is not None:
            self.created_date = m.get('CreatedDate')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        if m.get('HasTrigger') is not None:
            self.has_trigger = m.get('HasTrigger')
        if m.get('ShareType') is not None:
            self.share_type = m.get('ShareType')
        return self


class UpdateTemplateResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        template: UpdateTemplateResponseBodyTemplate = None,
    ):
        self.request_id = request_id
        self.template = template

    def validate(self):
        if self.template:
            self.template.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.template is not None:
            result['Template'] = self.template.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Template') is not None:
            temp_model = UpdateTemplateResponseBodyTemplate()
            self.template = temp_model.from_map(m['Template'])
        return self


class UpdateTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateTemplateResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ValidateTemplateContentRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        content: str = None,
    ):
        self.region_id = region_id
        self.content = content

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.content is not None:
            result['Content'] = self.content
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        return self


class ValidateTemplateContentResponseBodyTasks(TeaModel):
    def __init__(
        self,
        outputs: str = None,
        type: str = None,
        description: str = None,
        name: str = None,
        properties: str = None,
    ):
        self.outputs = outputs
        self.type = type
        self.description = description
        self.name = name
        self.properties = properties

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.outputs is not None:
            result['Outputs'] = self.outputs
        if self.type is not None:
            result['Type'] = self.type
        if self.description is not None:
            result['Description'] = self.description
        if self.name is not None:
            result['Name'] = self.name
        if self.properties is not None:
            result['Properties'] = self.properties
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Outputs') is not None:
            self.outputs = m.get('Outputs')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Properties') is not None:
            self.properties = m.get('Properties')
        return self


class ValidateTemplateContentResponseBody(TeaModel):
    def __init__(
        self,
        outputs: str = None,
        request_id: str = None,
        parameters: str = None,
        ram_role: str = None,
        tasks: List[ValidateTemplateContentResponseBodyTasks] = None,
    ):
        self.outputs = outputs
        self.request_id = request_id
        self.parameters = parameters
        self.ram_role = ram_role
        self.tasks = tasks

    def validate(self):
        if self.tasks:
            for k in self.tasks:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.outputs is not None:
            result['Outputs'] = self.outputs
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.parameters is not None:
            result['Parameters'] = self.parameters
        if self.ram_role is not None:
            result['RamRole'] = self.ram_role
        result['Tasks'] = []
        if self.tasks is not None:
            for k in self.tasks:
                result['Tasks'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Outputs') is not None:
            self.outputs = m.get('Outputs')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')
        if m.get('RamRole') is not None:
            self.ram_role = m.get('RamRole')
        self.tasks = []
        if m.get('Tasks') is not None:
            for k in m.get('Tasks'):
                temp_model = ValidateTemplateContentResponseBodyTasks()
                self.tasks.append(temp_model.from_map(k))
        return self


class ValidateTemplateContentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ValidateTemplateContentResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ValidateTemplateContentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


