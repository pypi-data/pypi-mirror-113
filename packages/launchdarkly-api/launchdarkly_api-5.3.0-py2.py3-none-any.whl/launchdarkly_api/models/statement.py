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


class Statement(object):
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
        'resources': 'list[str]',
        'not_resources': 'list[str]',
        'actions': 'list[str]',
        'not_actions': 'list[str]',
        'effect': 'str'
    }

    attribute_map = {
        'resources': 'resources',
        'not_resources': 'notResources',
        'actions': 'actions',
        'not_actions': 'notActions',
        'effect': 'effect'
    }

    def __init__(self, resources=None, not_resources=None, actions=None, not_actions=None, effect=None):  # noqa: E501
        """Statement - a model defined in Swagger"""  # noqa: E501

        self._resources = None
        self._not_resources = None
        self._actions = None
        self._not_actions = None
        self._effect = None
        self.discriminator = None

        if resources is not None:
            self.resources = resources
        if not_resources is not None:
            self.not_resources = not_resources
        if actions is not None:
            self.actions = actions
        if not_actions is not None:
            self.not_actions = not_actions
        if effect is not None:
            self.effect = effect

    @property
    def resources(self):
        """Gets the resources of this Statement.  # noqa: E501


        :return: The resources of this Statement.  # noqa: E501
        :rtype: list[str]
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this Statement.


        :param resources: The resources of this Statement.  # noqa: E501
        :type: list[str]
        """

        self._resources = resources

    @property
    def not_resources(self):
        """Gets the not_resources of this Statement.  # noqa: E501

        Targeted resource will be those resources NOT in this list. The \"resources`\" field must be empty to use this field.  # noqa: E501

        :return: The not_resources of this Statement.  # noqa: E501
        :rtype: list[str]
        """
        return self._not_resources

    @not_resources.setter
    def not_resources(self, not_resources):
        """Sets the not_resources of this Statement.

        Targeted resource will be those resources NOT in this list. The \"resources`\" field must be empty to use this field.  # noqa: E501

        :param not_resources: The not_resources of this Statement.  # noqa: E501
        :type: list[str]
        """

        self._not_resources = not_resources

    @property
    def actions(self):
        """Gets the actions of this Statement.  # noqa: E501


        :return: The actions of this Statement.  # noqa: E501
        :rtype: list[str]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """Sets the actions of this Statement.


        :param actions: The actions of this Statement.  # noqa: E501
        :type: list[str]
        """

        self._actions = actions

    @property
    def not_actions(self):
        """Gets the not_actions of this Statement.  # noqa: E501

        Targeted actions will be those actions NOT in this list. The \"actions\" field must be empty to use this field.  # noqa: E501

        :return: The not_actions of this Statement.  # noqa: E501
        :rtype: list[str]
        """
        return self._not_actions

    @not_actions.setter
    def not_actions(self, not_actions):
        """Sets the not_actions of this Statement.

        Targeted actions will be those actions NOT in this list. The \"actions\" field must be empty to use this field.  # noqa: E501

        :param not_actions: The not_actions of this Statement.  # noqa: E501
        :type: list[str]
        """

        self._not_actions = not_actions

    @property
    def effect(self):
        """Gets the effect of this Statement.  # noqa: E501


        :return: The effect of this Statement.  # noqa: E501
        :rtype: str
        """
        return self._effect

    @effect.setter
    def effect(self, effect):
        """Sets the effect of this Statement.


        :param effect: The effect of this Statement.  # noqa: E501
        :type: str
        """
        allowed_values = ["allow", "deny"]  # noqa: E501
        if effect not in allowed_values:
            raise ValueError(
                "Invalid value for `effect` ({0}), must be one of {1}"  # noqa: E501
                .format(effect, allowed_values)
            )

        self._effect = effect

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
        if issubclass(Statement, dict):
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
        if not isinstance(other, Statement):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
