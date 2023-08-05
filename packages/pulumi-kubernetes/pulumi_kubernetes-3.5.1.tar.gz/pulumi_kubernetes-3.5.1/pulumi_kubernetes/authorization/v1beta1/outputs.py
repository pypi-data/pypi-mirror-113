# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'NonResourceAttributes',
    'NonResourceRule',
    'ResourceAttributes',
    'ResourceRule',
    'SelfSubjectAccessReviewSpec',
    'SelfSubjectRulesReviewSpec',
    'SubjectAccessReviewSpec',
    'SubjectAccessReviewStatus',
    'SubjectRulesReviewStatus',
]

@pulumi.output_type
class NonResourceAttributes(dict):
    """
    NonResourceAttributes includes the authorization attributes available for non-resource requests to the Authorizer interface
    """
    def __init__(__self__, *,
                 path: Optional[str] = None,
                 verb: Optional[str] = None):
        """
        NonResourceAttributes includes the authorization attributes available for non-resource requests to the Authorizer interface
        :param str path: Path is the URL path of the request
        :param str verb: Verb is the standard HTTP verb
        """
        if path is not None:
            pulumi.set(__self__, "path", path)
        if verb is not None:
            pulumi.set(__self__, "verb", verb)

    @property
    @pulumi.getter
    def path(self) -> Optional[str]:
        """
        Path is the URL path of the request
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter
    def verb(self) -> Optional[str]:
        """
        Verb is the standard HTTP verb
        """
        return pulumi.get(self, "verb")


@pulumi.output_type
class NonResourceRule(dict):
    """
    NonResourceRule holds information that describes a rule for the non-resource
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "nonResourceURLs":
            suggest = "non_resource_urls"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in NonResourceRule. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        NonResourceRule.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        NonResourceRule.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 verbs: Sequence[str],
                 non_resource_urls: Optional[Sequence[str]] = None):
        """
        NonResourceRule holds information that describes a rule for the non-resource
        :param Sequence[str] verbs: Verb is a list of kubernetes non-resource API verbs, like: get, post, put, delete, patch, head, options.  "*" means all.
        :param Sequence[str] non_resource_urls: NonResourceURLs is a set of partial urls that a user should have access to.  *s are allowed, but only as the full, final step in the path.  "*" means all.
        """
        pulumi.set(__self__, "verbs", verbs)
        if non_resource_urls is not None:
            pulumi.set(__self__, "non_resource_urls", non_resource_urls)

    @property
    @pulumi.getter
    def verbs(self) -> Sequence[str]:
        """
        Verb is a list of kubernetes non-resource API verbs, like: get, post, put, delete, patch, head, options.  "*" means all.
        """
        return pulumi.get(self, "verbs")

    @property
    @pulumi.getter(name="nonResourceURLs")
    def non_resource_urls(self) -> Optional[Sequence[str]]:
        """
        NonResourceURLs is a set of partial urls that a user should have access to.  *s are allowed, but only as the full, final step in the path.  "*" means all.
        """
        return pulumi.get(self, "non_resource_urls")


@pulumi.output_type
class ResourceAttributes(dict):
    """
    ResourceAttributes includes the authorization attributes available for resource requests to the Authorizer interface
    """
    def __init__(__self__, *,
                 group: Optional[str] = None,
                 name: Optional[str] = None,
                 namespace: Optional[str] = None,
                 resource: Optional[str] = None,
                 subresource: Optional[str] = None,
                 verb: Optional[str] = None,
                 version: Optional[str] = None):
        """
        ResourceAttributes includes the authorization attributes available for resource requests to the Authorizer interface
        :param str group: Group is the API Group of the Resource.  "*" means all.
        :param str name: Name is the name of the resource being requested for a "get" or deleted for a "delete". "" (empty) means all.
        :param str namespace: Namespace is the namespace of the action being requested.  Currently, there is no distinction between no namespace and all namespaces "" (empty) is defaulted for LocalSubjectAccessReviews "" (empty) is empty for cluster-scoped resources "" (empty) means "all" for namespace scoped resources from a SubjectAccessReview or SelfSubjectAccessReview
        :param str resource: Resource is one of the existing resource types.  "*" means all.
        :param str subresource: Subresource is one of the existing resource types.  "" means none.
        :param str verb: Verb is a kubernetes resource API verb, like: get, list, watch, create, update, delete, proxy.  "*" means all.
        :param str version: Version is the API Version of the Resource.  "*" means all.
        """
        if group is not None:
            pulumi.set(__self__, "group", group)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if resource is not None:
            pulumi.set(__self__, "resource", resource)
        if subresource is not None:
            pulumi.set(__self__, "subresource", subresource)
        if verb is not None:
            pulumi.set(__self__, "verb", verb)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def group(self) -> Optional[str]:
        """
        Group is the API Group of the Resource.  "*" means all.
        """
        return pulumi.get(self, "group")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name is the name of the resource being requested for a "get" or deleted for a "delete". "" (empty) means all.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def namespace(self) -> Optional[str]:
        """
        Namespace is the namespace of the action being requested.  Currently, there is no distinction between no namespace and all namespaces "" (empty) is defaulted for LocalSubjectAccessReviews "" (empty) is empty for cluster-scoped resources "" (empty) means "all" for namespace scoped resources from a SubjectAccessReview or SelfSubjectAccessReview
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter
    def resource(self) -> Optional[str]:
        """
        Resource is one of the existing resource types.  "*" means all.
        """
        return pulumi.get(self, "resource")

    @property
    @pulumi.getter
    def subresource(self) -> Optional[str]:
        """
        Subresource is one of the existing resource types.  "" means none.
        """
        return pulumi.get(self, "subresource")

    @property
    @pulumi.getter
    def verb(self) -> Optional[str]:
        """
        Verb is a kubernetes resource API verb, like: get, list, watch, create, update, delete, proxy.  "*" means all.
        """
        return pulumi.get(self, "verb")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version is the API Version of the Resource.  "*" means all.
        """
        return pulumi.get(self, "version")


@pulumi.output_type
class ResourceRule(dict):
    """
    ResourceRule is the list of actions the subject is allowed to perform on resources. The list ordering isn't significant, may contain duplicates, and possibly be incomplete.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "apiGroups":
            suggest = "api_groups"
        elif key == "resourceNames":
            suggest = "resource_names"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ResourceRule. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ResourceRule.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ResourceRule.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 verbs: Sequence[str],
                 api_groups: Optional[Sequence[str]] = None,
                 resource_names: Optional[Sequence[str]] = None,
                 resources: Optional[Sequence[str]] = None):
        """
        ResourceRule is the list of actions the subject is allowed to perform on resources. The list ordering isn't significant, may contain duplicates, and possibly be incomplete.
        :param Sequence[str] verbs: Verb is a list of kubernetes resource API verbs, like: get, list, watch, create, update, delete, proxy.  "*" means all.
        :param Sequence[str] api_groups: APIGroups is the name of the APIGroup that contains the resources.  If multiple API groups are specified, any action requested against one of the enumerated resources in any API group will be allowed.  "*" means all.
        :param Sequence[str] resource_names: ResourceNames is an optional white list of names that the rule applies to.  An empty set means that everything is allowed.  "*" means all.
        :param Sequence[str] resources: Resources is a list of resources this rule applies to.  "*" means all in the specified apiGroups.
                "*/foo" represents the subresource 'foo' for all resources in the specified apiGroups.
        """
        pulumi.set(__self__, "verbs", verbs)
        if api_groups is not None:
            pulumi.set(__self__, "api_groups", api_groups)
        if resource_names is not None:
            pulumi.set(__self__, "resource_names", resource_names)
        if resources is not None:
            pulumi.set(__self__, "resources", resources)

    @property
    @pulumi.getter
    def verbs(self) -> Sequence[str]:
        """
        Verb is a list of kubernetes resource API verbs, like: get, list, watch, create, update, delete, proxy.  "*" means all.
        """
        return pulumi.get(self, "verbs")

    @property
    @pulumi.getter(name="apiGroups")
    def api_groups(self) -> Optional[Sequence[str]]:
        """
        APIGroups is the name of the APIGroup that contains the resources.  If multiple API groups are specified, any action requested against one of the enumerated resources in any API group will be allowed.  "*" means all.
        """
        return pulumi.get(self, "api_groups")

    @property
    @pulumi.getter(name="resourceNames")
    def resource_names(self) -> Optional[Sequence[str]]:
        """
        ResourceNames is an optional white list of names that the rule applies to.  An empty set means that everything is allowed.  "*" means all.
        """
        return pulumi.get(self, "resource_names")

    @property
    @pulumi.getter
    def resources(self) -> Optional[Sequence[str]]:
        """
        Resources is a list of resources this rule applies to.  "*" means all in the specified apiGroups.
         "*/foo" represents the subresource 'foo' for all resources in the specified apiGroups.
        """
        return pulumi.get(self, "resources")


@pulumi.output_type
class SelfSubjectAccessReviewSpec(dict):
    """
    SelfSubjectAccessReviewSpec is a description of the access request.  Exactly one of ResourceAuthorizationAttributes and NonResourceAuthorizationAttributes must be set
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "nonResourceAttributes":
            suggest = "non_resource_attributes"
        elif key == "resourceAttributes":
            suggest = "resource_attributes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SelfSubjectAccessReviewSpec. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SelfSubjectAccessReviewSpec.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SelfSubjectAccessReviewSpec.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 non_resource_attributes: Optional['outputs.NonResourceAttributes'] = None,
                 resource_attributes: Optional['outputs.ResourceAttributes'] = None):
        """
        SelfSubjectAccessReviewSpec is a description of the access request.  Exactly one of ResourceAuthorizationAttributes and NonResourceAuthorizationAttributes must be set
        :param 'NonResourceAttributesArgs' non_resource_attributes: NonResourceAttributes describes information for a non-resource access request
        :param 'ResourceAttributesArgs' resource_attributes: ResourceAuthorizationAttributes describes information for a resource access request
        """
        if non_resource_attributes is not None:
            pulumi.set(__self__, "non_resource_attributes", non_resource_attributes)
        if resource_attributes is not None:
            pulumi.set(__self__, "resource_attributes", resource_attributes)

    @property
    @pulumi.getter(name="nonResourceAttributes")
    def non_resource_attributes(self) -> Optional['outputs.NonResourceAttributes']:
        """
        NonResourceAttributes describes information for a non-resource access request
        """
        return pulumi.get(self, "non_resource_attributes")

    @property
    @pulumi.getter(name="resourceAttributes")
    def resource_attributes(self) -> Optional['outputs.ResourceAttributes']:
        """
        ResourceAuthorizationAttributes describes information for a resource access request
        """
        return pulumi.get(self, "resource_attributes")


@pulumi.output_type
class SelfSubjectRulesReviewSpec(dict):
    def __init__(__self__, *,
                 namespace: Optional[str] = None):
        """
        :param str namespace: Namespace to evaluate rules for. Required.
        """
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[str]:
        """
        Namespace to evaluate rules for. Required.
        """
        return pulumi.get(self, "namespace")


@pulumi.output_type
class SubjectAccessReviewSpec(dict):
    """
    SubjectAccessReviewSpec is a description of the access request.  Exactly one of ResourceAuthorizationAttributes and NonResourceAuthorizationAttributes must be set
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "nonResourceAttributes":
            suggest = "non_resource_attributes"
        elif key == "resourceAttributes":
            suggest = "resource_attributes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SubjectAccessReviewSpec. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SubjectAccessReviewSpec.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SubjectAccessReviewSpec.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 extra: Optional[Mapping[str, Sequence[str]]] = None,
                 group: Optional[Sequence[str]] = None,
                 non_resource_attributes: Optional['outputs.NonResourceAttributes'] = None,
                 resource_attributes: Optional['outputs.ResourceAttributes'] = None,
                 uid: Optional[str] = None,
                 user: Optional[str] = None):
        """
        SubjectAccessReviewSpec is a description of the access request.  Exactly one of ResourceAuthorizationAttributes and NonResourceAuthorizationAttributes must be set
        :param Mapping[str, Sequence[str]] extra: Extra corresponds to the user.Info.GetExtra() method from the authenticator.  Since that is input to the authorizer it needs a reflection here.
        :param Sequence[str] group: Groups is the groups you're testing for.
        :param 'NonResourceAttributesArgs' non_resource_attributes: NonResourceAttributes describes information for a non-resource access request
        :param 'ResourceAttributesArgs' resource_attributes: ResourceAuthorizationAttributes describes information for a resource access request
        :param str uid: UID information about the requesting user.
        :param str user: User is the user you're testing for. If you specify "User" but not "Group", then is it interpreted as "What if User were not a member of any groups
        """
        if extra is not None:
            pulumi.set(__self__, "extra", extra)
        if group is not None:
            pulumi.set(__self__, "group", group)
        if non_resource_attributes is not None:
            pulumi.set(__self__, "non_resource_attributes", non_resource_attributes)
        if resource_attributes is not None:
            pulumi.set(__self__, "resource_attributes", resource_attributes)
        if uid is not None:
            pulumi.set(__self__, "uid", uid)
        if user is not None:
            pulumi.set(__self__, "user", user)

    @property
    @pulumi.getter
    def extra(self) -> Optional[Mapping[str, Sequence[str]]]:
        """
        Extra corresponds to the user.Info.GetExtra() method from the authenticator.  Since that is input to the authorizer it needs a reflection here.
        """
        return pulumi.get(self, "extra")

    @property
    @pulumi.getter
    def group(self) -> Optional[Sequence[str]]:
        """
        Groups is the groups you're testing for.
        """
        return pulumi.get(self, "group")

    @property
    @pulumi.getter(name="nonResourceAttributes")
    def non_resource_attributes(self) -> Optional['outputs.NonResourceAttributes']:
        """
        NonResourceAttributes describes information for a non-resource access request
        """
        return pulumi.get(self, "non_resource_attributes")

    @property
    @pulumi.getter(name="resourceAttributes")
    def resource_attributes(self) -> Optional['outputs.ResourceAttributes']:
        """
        ResourceAuthorizationAttributes describes information for a resource access request
        """
        return pulumi.get(self, "resource_attributes")

    @property
    @pulumi.getter
    def uid(self) -> Optional[str]:
        """
        UID information about the requesting user.
        """
        return pulumi.get(self, "uid")

    @property
    @pulumi.getter
    def user(self) -> Optional[str]:
        """
        User is the user you're testing for. If you specify "User" but not "Group", then is it interpreted as "What if User were not a member of any groups
        """
        return pulumi.get(self, "user")


@pulumi.output_type
class SubjectAccessReviewStatus(dict):
    """
    SubjectAccessReviewStatus
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "evaluationError":
            suggest = "evaluation_error"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SubjectAccessReviewStatus. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SubjectAccessReviewStatus.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SubjectAccessReviewStatus.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 allowed: bool,
                 denied: Optional[bool] = None,
                 evaluation_error: Optional[str] = None,
                 reason: Optional[str] = None):
        """
        SubjectAccessReviewStatus
        :param bool allowed: Allowed is required. True if the action would be allowed, false otherwise.
        :param bool denied: Denied is optional. True if the action would be denied, otherwise false. If both allowed is false and denied is false, then the authorizer has no opinion on whether to authorize the action. Denied may not be true if Allowed is true.
        :param str evaluation_error: EvaluationError is an indication that some error occurred during the authorization check. It is entirely possible to get an error and be able to continue determine authorization status in spite of it. For instance, RBAC can be missing a role, but enough roles are still present and bound to reason about the request.
        :param str reason: Reason is optional.  It indicates why a request was allowed or denied.
        """
        pulumi.set(__self__, "allowed", allowed)
        if denied is not None:
            pulumi.set(__self__, "denied", denied)
        if evaluation_error is not None:
            pulumi.set(__self__, "evaluation_error", evaluation_error)
        if reason is not None:
            pulumi.set(__self__, "reason", reason)

    @property
    @pulumi.getter
    def allowed(self) -> bool:
        """
        Allowed is required. True if the action would be allowed, false otherwise.
        """
        return pulumi.get(self, "allowed")

    @property
    @pulumi.getter
    def denied(self) -> Optional[bool]:
        """
        Denied is optional. True if the action would be denied, otherwise false. If both allowed is false and denied is false, then the authorizer has no opinion on whether to authorize the action. Denied may not be true if Allowed is true.
        """
        return pulumi.get(self, "denied")

    @property
    @pulumi.getter(name="evaluationError")
    def evaluation_error(self) -> Optional[str]:
        """
        EvaluationError is an indication that some error occurred during the authorization check. It is entirely possible to get an error and be able to continue determine authorization status in spite of it. For instance, RBAC can be missing a role, but enough roles are still present and bound to reason about the request.
        """
        return pulumi.get(self, "evaluation_error")

    @property
    @pulumi.getter
    def reason(self) -> Optional[str]:
        """
        Reason is optional.  It indicates why a request was allowed or denied.
        """
        return pulumi.get(self, "reason")


@pulumi.output_type
class SubjectRulesReviewStatus(dict):
    """
    SubjectRulesReviewStatus contains the result of a rules check. This check can be incomplete depending on the set of authorizers the server is configured with and any errors experienced during evaluation. Because authorization rules are additive, if a rule appears in a list it's safe to assume the subject has that permission, even if that list is incomplete.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "nonResourceRules":
            suggest = "non_resource_rules"
        elif key == "resourceRules":
            suggest = "resource_rules"
        elif key == "evaluationError":
            suggest = "evaluation_error"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SubjectRulesReviewStatus. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SubjectRulesReviewStatus.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SubjectRulesReviewStatus.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 incomplete: bool,
                 non_resource_rules: Sequence['outputs.NonResourceRule'],
                 resource_rules: Sequence['outputs.ResourceRule'],
                 evaluation_error: Optional[str] = None):
        """
        SubjectRulesReviewStatus contains the result of a rules check. This check can be incomplete depending on the set of authorizers the server is configured with and any errors experienced during evaluation. Because authorization rules are additive, if a rule appears in a list it's safe to assume the subject has that permission, even if that list is incomplete.
        :param bool incomplete: Incomplete is true when the rules returned by this call are incomplete. This is most commonly encountered when an authorizer, such as an external authorizer, doesn't support rules evaluation.
        :param Sequence['NonResourceRuleArgs'] non_resource_rules: NonResourceRules is the list of actions the subject is allowed to perform on non-resources. The list ordering isn't significant, may contain duplicates, and possibly be incomplete.
        :param Sequence['ResourceRuleArgs'] resource_rules: ResourceRules is the list of actions the subject is allowed to perform on resources. The list ordering isn't significant, may contain duplicates, and possibly be incomplete.
        :param str evaluation_error: EvaluationError can appear in combination with Rules. It indicates an error occurred during rule evaluation, such as an authorizer that doesn't support rule evaluation, and that ResourceRules and/or NonResourceRules may be incomplete.
        """
        pulumi.set(__self__, "incomplete", incomplete)
        pulumi.set(__self__, "non_resource_rules", non_resource_rules)
        pulumi.set(__self__, "resource_rules", resource_rules)
        if evaluation_error is not None:
            pulumi.set(__self__, "evaluation_error", evaluation_error)

    @property
    @pulumi.getter
    def incomplete(self) -> bool:
        """
        Incomplete is true when the rules returned by this call are incomplete. This is most commonly encountered when an authorizer, such as an external authorizer, doesn't support rules evaluation.
        """
        return pulumi.get(self, "incomplete")

    @property
    @pulumi.getter(name="nonResourceRules")
    def non_resource_rules(self) -> Sequence['outputs.NonResourceRule']:
        """
        NonResourceRules is the list of actions the subject is allowed to perform on non-resources. The list ordering isn't significant, may contain duplicates, and possibly be incomplete.
        """
        return pulumi.get(self, "non_resource_rules")

    @property
    @pulumi.getter(name="resourceRules")
    def resource_rules(self) -> Sequence['outputs.ResourceRule']:
        """
        ResourceRules is the list of actions the subject is allowed to perform on resources. The list ordering isn't significant, may contain duplicates, and possibly be incomplete.
        """
        return pulumi.get(self, "resource_rules")

    @property
    @pulumi.getter(name="evaluationError")
    def evaluation_error(self) -> Optional[str]:
        """
        EvaluationError can appear in combination with Rules. It indicates an error occurred during rule evaluation, such as an authorizer that doesn't support rule evaluation, and that ResourceRules and/or NonResourceRules may be incomplete.
        """
        return pulumi.get(self, "evaluation_error")


