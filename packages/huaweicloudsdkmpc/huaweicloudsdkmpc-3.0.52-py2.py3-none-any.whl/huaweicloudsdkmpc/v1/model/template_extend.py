# coding: utf-8

import re
import six





class TemplateExtend:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'audio': 'AudioExtendSettings',
        'video': 'VideoExtendSettings'
    }

    attribute_map = {
        'audio': 'audio',
        'video': 'video'
    }

    def __init__(self, audio=None, video=None):
        """TemplateExtend - a model defined in huaweicloud sdk"""
        
        

        self._audio = None
        self._video = None
        self.discriminator = None

        if audio is not None:
            self.audio = audio
        if video is not None:
            self.video = video

    @property
    def audio(self):
        """Gets the audio of this TemplateExtend.


        :return: The audio of this TemplateExtend.
        :rtype: AudioExtendSettings
        """
        return self._audio

    @audio.setter
    def audio(self, audio):
        """Sets the audio of this TemplateExtend.


        :param audio: The audio of this TemplateExtend.
        :type: AudioExtendSettings
        """
        self._audio = audio

    @property
    def video(self):
        """Gets the video of this TemplateExtend.


        :return: The video of this TemplateExtend.
        :rtype: VideoExtendSettings
        """
        return self._video

    @video.setter
    def video(self, video):
        """Sets the video of this TemplateExtend.


        :param video: The video of this TemplateExtend.
        :type: VideoExtendSettings
        """
        self._video = video

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        import simplejson as json
        return json.dumps(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TemplateExtend):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
