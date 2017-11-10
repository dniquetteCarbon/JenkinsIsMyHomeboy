import serial
import logging

from homeboy.homeboy_core import HomeboyCore
from homeboy.homeboy_effects import HomeboyEffects
from homeboy.jenkins_query import JenkinsQuery
from homeboy.light_data import LightData

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

