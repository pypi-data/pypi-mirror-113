# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_kubernetes.flowcontrol.v1alpha1 as v1alpha1
    import pulumi_kubernetes.flowcontrol.v1beta1 as v1beta1
else:
    v1alpha1 = _utilities.lazy_import('pulumi_kubernetes.flowcontrol.v1alpha1')
    v1beta1 = _utilities.lazy_import('pulumi_kubernetes.flowcontrol.v1beta1')

