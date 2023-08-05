# coding: utf-8

"""
    LaunchDarkly REST API

    Build custom integrations with the LaunchDarkly REST API  # noqa: E501

    OpenAPI spec version: 5.3.0
    Contact: support@launchdarkly.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class FeatureFlagScheduledChangesConflicts(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'instructions': 'list[FeatureFlagScheduledChangesConflictsInstructions]'
    }

    attribute_map = {
        'instructions': 'instructions'
    }

    def __init__(self, instructions=None):  # noqa: E501
        """FeatureFlagScheduledChangesConflicts - a model defined in Swagger"""  # noqa: E501

        self._instructions = None
        self.discriminator = None

        if instructions is not None:
            self.instructions = instructions

    @property
    def instructions(self):
        """Gets the instructions of this FeatureFlagScheduledChangesConflicts.  # noqa: E501


        :return: The instructions of this FeatureFlagScheduledChangesConflicts.  # noqa: E501
        :rtype: list[FeatureFlagScheduledChangesConflictsInstructions]
        """
        return self._instructions

    @instructions.setter
    def instructions(self, instructions):
        """Sets the instructions of this FeatureFlagScheduledChangesConflicts.


        :param instructions: The instructions of this FeatureFlagScheduledChangesConflicts.  # noqa: E501
        :type: list[FeatureFlagScheduledChangesConflictsInstructions]
        """

        self._instructions = instructions

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(FeatureFlagScheduledChangesConflicts, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, FeatureFlagScheduledChangesConflicts):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
