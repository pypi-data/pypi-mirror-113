import logging
import board
import busio

from OpenHub.hardware_interfaces.base_io.base_io_interface import BaseIOInterface

from adafruit_mcp3xxx.analog_in import AnalogIn
from OpenHub.hardware_interfaces.channels.channel_interface import ChannelInterface
import logging
import uuid


class MCPAnalogIO(BaseIOInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, mcp=None, channel_index=None, hardware_serial_no=None, serial_no=uuid.uuid4(),
                 *args, **kwargs):
        super(MCPAnalogIO, self).__init__(*args, **kwargs)
        self.analog_in = AnalogIn(mcp, channel_index)
