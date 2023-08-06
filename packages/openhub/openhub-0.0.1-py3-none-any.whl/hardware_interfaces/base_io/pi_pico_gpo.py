import logging

from OpenHub.hardware_interfaces.base_io.base_io_interface import BaseIOInterface
from OpenHub.hardware_interfaces.base_io.pi_pico_gpi import PiPicoGPI


class PiPicoGPO(PiPicoGPI):
    logger = logging.getLogger(__name__)

    def __init__(self,default = 'off', *args, **kwargs):
        self.default = default
        super(PiPicoGPO, self).__init__(*args, **kwargs)
