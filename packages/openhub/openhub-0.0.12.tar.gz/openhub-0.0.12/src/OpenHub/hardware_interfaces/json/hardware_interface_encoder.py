import json
from OpenHub import HardwareInterface
from OpenHub.hardware_interfaces.channels import ChannelEncoder


class HardwareEncoder(json.JSONEncoder):
    channel_encoder = ChannelEncoder()

    def default(self, o):
        if isinstance(o, HardwareInterface):
            hardware_json = o.__dict__
            encoded_channels = []
            for channel in o.channels:
                encoded_channels.append(json.dumps(channel, cls=ChannelEncoder))

            hardware_json['channels'] = encoded_channels
            return hardware_json

        return json.JSONEncoder.default(self, o)
