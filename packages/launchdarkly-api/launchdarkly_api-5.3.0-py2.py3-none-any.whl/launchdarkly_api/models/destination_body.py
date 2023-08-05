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


class DestinationBody(object):
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
        'kind': 'str',
        'config': 'object',
        'on': 'bool'
    }

    attribute_map = {
        'name': 'name',
        'kind': 'kind',
        'config': 'config',
        'on': 'on'
    }

    def __init__(self, name=None, kind=None, config=None, on=None):  # noqa: E501
        """DestinationBody - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._kind = None
        self._config = None
        self._on = None
        self.discriminator = None

        self.name = name
        self.kind = kind
        self.config = config
        if on is not None:
            self.on = on

    @property
    def name(self):
        """Gets the name of this DestinationBody.  # noqa: E501

        A human-readable name for your data export destination.  # noqa: E501

        :return: The name of this DestinationBody.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DestinationBody.

        A human-readable name for your data export destination.  # noqa: E501

        :param name: The name of this DestinationBody.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def kind(self):
        """Gets the kind of this DestinationBody.  # noqa: E501

        The data export destination type. Available choices are kinesis, google-pubsub, mparticle, or segment.  # noqa: E501

        :return: The kind of this DestinationBody.  # noqa: E501
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this DestinationBody.

        The data export destination type. Available choices are kinesis, google-pubsub, mparticle, or segment.  # noqa: E501

        :param kind: The kind of this DestinationBody.  # noqa: E501
        :type: str
        """
        if kind is None:
            raise ValueError("Invalid value for `kind`, must not be `None`")  # noqa: E501
        allowed_values = ["google-pubsub", "kinesis", "mparticle", "segment"]  # noqa: E501
        if kind not in allowed_values:
            raise ValueError(
                "Invalid value for `kind` ({0}), must be one of {1}"  # noqa: E501
                .format(kind, allowed_values)
            )

        self._kind = kind

    @property
    def config(self):
        """Gets the config of this DestinationBody.  # noqa: E501

        destination-specific configuration.  # noqa: E501

        :return: The config of this DestinationBody.  # noqa: E501
        :rtype: object
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this DestinationBody.

        destination-specific configuration.  # noqa: E501

        :param config: The config of this DestinationBody.  # noqa: E501
        :type: object
        """
        if config is None:
            raise ValueError("Invalid value for `config`, must not be `None`")  # noqa: E501

        self._config = config

    @property
    def on(self):
        """Gets the on of this DestinationBody.  # noqa: E501

        Whether the data export destination is on or not.  # noqa: E501

        :return: The on of this DestinationBody.  # noqa: E501
        :rtype: bool
        """
        return self._on

    @on.setter
    def on(self, on):
        """Sets the on of this DestinationBody.

        Whether the data export destination is on or not.  # noqa: E501

        :param on: The on of this DestinationBody.  # noqa: E501
        :type: bool
        """

        self._on = on

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
        if issubclass(DestinationBody, dict):
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
        if not isinstance(other, DestinationBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
