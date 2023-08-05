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


class SubscriptionBody(object):
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
        'name': 'str',
        'statements': 'list[Statement]',
        'config': 'object',
        'on': 'bool',
        'tags': 'list[str]'
    }

    attribute_map = {
        'name': 'name',
        'statements': 'statements',
        'config': 'config',
        'on': 'on',
        'tags': 'tags'
    }

    def __init__(self, name=None, statements=None, config=None, on=None, tags=None):  # noqa: E501
        """SubscriptionBody - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._statements = None
        self._config = None
        self._on = None
        self._tags = None
        self.discriminator = None

        self.name = name
        if statements is not None:
            self.statements = statements
        self.config = config
        if on is not None:
            self.on = on
        if tags is not None:
            self.tags = tags

    @property
    def name(self):
        """Gets the name of this SubscriptionBody.  # noqa: E501

        A human-readable name for your subscription configuration.  # noqa: E501

        :return: The name of this SubscriptionBody.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SubscriptionBody.

        A human-readable name for your subscription configuration.  # noqa: E501

        :param name: The name of this SubscriptionBody.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def statements(self):
        """Gets the statements of this SubscriptionBody.  # noqa: E501


        :return: The statements of this SubscriptionBody.  # noqa: E501
        :rtype: list[Statement]
        """
        return self._statements

    @statements.setter
    def statements(self, statements):
        """Sets the statements of this SubscriptionBody.


        :param statements: The statements of this SubscriptionBody.  # noqa: E501
        :type: list[Statement]
        """

        self._statements = statements

    @property
    def config(self):
        """Gets the config of this SubscriptionBody.  # noqa: E501

        Integration-specific configuration fields.  # noqa: E501

        :return: The config of this SubscriptionBody.  # noqa: E501
        :rtype: object
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this SubscriptionBody.

        Integration-specific configuration fields.  # noqa: E501

        :param config: The config of this SubscriptionBody.  # noqa: E501
        :type: object
        """
        if config is None:
            raise ValueError("Invalid value for `config`, must not be `None`")  # noqa: E501

        self._config = config

    @property
    def on(self):
        """Gets the on of this SubscriptionBody.  # noqa: E501

        Whether the integration subscription is active or not.  # noqa: E501

        :return: The on of this SubscriptionBody.  # noqa: E501
        :rtype: bool
        """
        return self._on

    @on.setter
    def on(self, on):
        """Sets the on of this SubscriptionBody.

        Whether the integration subscription is active or not.  # noqa: E501

        :param on: The on of this SubscriptionBody.  # noqa: E501
        :type: bool
        """

        self._on = on

    @property
    def tags(self):
        """Gets the tags of this SubscriptionBody.  # noqa: E501

        Tags for the integration subscription.  # noqa: E501

        :return: The tags of this SubscriptionBody.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this SubscriptionBody.

        Tags for the integration subscription.  # noqa: E501

        :param tags: The tags of this SubscriptionBody.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

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
        if issubclass(SubscriptionBody, dict):
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
        if not isinstance(other, SubscriptionBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
