"""
Script to:
    1. Heat the hot plate to "temperature" degrees C
    2. Hold for time "at_temperature_hold_time_minutes" minutes
    3. Turn off the hot plate for "off_temperature_hold_time_minutes" minutes
    4. Repeat steps 1-3 "n_cycles" number of times
"""

import logging
import time
from datetime import datetime, timedelta

from ika.magnetic_stirrer import MagneticStirrer


logger = logging.getLogger('temperature cycles script')
logger.setLevel(logging.INFO)
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=format, level=logging.INFO)


if __name__ == '__main__':
    # todo fill in these variables

    # todo temperature to go to in degrees Celsius
    temperature = 30

    # todo number of times to go to the set temperature
    n_cycles = 2

    # todo minutes to hold each temperature at
    at_temperature_hold_time_minutes = 5

    # todo minutes to hold at with heating off
    off_temperature_hold_time_minutes = 5

    # todo ika plate comport
    port = 'COM4'

    # todo wait time frequency - frequency to log the remaining time and current plate temperature during the at
    #  temperature/off temperature waits, and the frequency to check if the heating/off heat steps should end,
    #  in seconds
    wait_time_frequency = 60  # seconds

    # shouldn't need to edit anything under this line
    # ------------------------------------------------------------
    plate = MagneticStirrer(device_port=port, safe_connect=False)

    logger.info(f'do {n_cycles} temperature cycles: heat to {temperature} C for '
                f'{at_temperature_hold_time_minutes} minutes then turn off heat for '
                f'{off_temperature_hold_time_minutes} minutes')
    for i in range(n_cycles):
        logger.info(f'start temperature cycle {i + 1} / {n_cycles}')
        logger.info(f'heat at {temperature} C for {at_temperature_hold_time_minutes} minutes')
        plate.target_temperature = temperature
        plate.start_heating()
        start_at_temperature_time = datetime.now()
        end_at_temperature_time = start_at_temperature_time + timedelta(minutes=at_temperature_hold_time_minutes)
        while datetime.now() < end_at_temperature_time:
            at_temperature_time_remaining_minutes = round(((end_at_temperature_time - datetime.now()).seconds) / 60, 2)
            logger.info(f'heat and wait at {temperature} C - time remaining: {at_temperature_time_remaining_minutes} '
                        f'minutes - current plate temperature: {plate.hotplate_sensor_temperature} ')
            time.sleep(wait_time_frequency)

        logger.info(f'turn off heating for {off_temperature_hold_time_minutes} minutes')
        plate.stop_heating()
        start_off_temperature_time = datetime.now()
        end_off_temperature_time = start_off_temperature_time + timedelta(minutes=off_temperature_hold_time_minutes)
        while datetime.now() < end_off_temperature_time:
            off_temperature_time_remaining_minutes = round(((end_off_temperature_time - datetime.now()).seconds) / 60, 2)
            logger.info(f'heat off and wait - time remaining: {off_temperature_time_remaining_minutes} minutes - '
                        f'current plate temperature: {plate.hotplate_sensor_temperature} C')
            time.sleep(wait_time_frequency)

        logger.info(f'temperature cycle {i + 1} / {n_cycles} completed')

    logger.info('completed all temperature cycles, script ending')


