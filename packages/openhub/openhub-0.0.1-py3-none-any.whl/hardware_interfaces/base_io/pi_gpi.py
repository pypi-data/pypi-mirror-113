import logging

from OpenHub.hardware_interfaces.base_io.base_io_interface import BaseIOInterface
from OpenHub.hardware_interfaces.base_io.pi_pico_gpi import PiPicoGPI
import RPi.GPIO as GPIO


class PiGPI(PiPicoGPI):
    logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super(PiGPI, self).__init__(*args, **kwargs)
        GPIO.setup(self.pin, GPIO.IN)
