from typing import Dict, List, Optional

from pydantic import BaseModel


class VersionSummary(BaseModel):
    version_id: int


class ResourceStateSummary(BaseModel):
    version: VersionSummary


class ResourceBase(BaseModel):
    resource_cd: str


class ResourceReadonly(BaseModel):
    is_readonly: bool = False


class ResourceResourceUpdate(ResourceBase, ResourceReadonly):
    resource_desc: str
    tags: Optional[List[str]] = None
    features: Optional[Dict[str, str]] = None


class ResourceState(BaseModel):
    state: ResourceStateSummary = None


class Resource(ResourceResourceUpdate, ResourceState):
    def __eq__(self, other):
        return other == self.resource_cd
