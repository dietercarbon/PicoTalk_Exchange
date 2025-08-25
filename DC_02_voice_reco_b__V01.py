from DFRobot_DF2301Q_I2C import DFRobot_DF2301Q_I2C
from micropython import const
from utime import sleep


SDA_PIN = const(0)
SCL_PIN = const(1)
SLEEP_SECONDS = const(3)


def setup(sensor) -> None:
    """
    Set up the DFRobot DF2301Q sensor
    :param sensor: instance of DFRobot_DF2301Q_I2C
    :return: None
    """
    sensor.set_volume(10)
    sensor.set_mute_mode(0)
    sensor.set_wake_time(20)


def get_cmd_id(sensor) -> int:
    """
    Get the command id from the DF2301Q sensor
    :param sensor: instance of DFRobot_DF2301Q_I2C
    :return: int
    """
    command_id = sensor.get_cmdid()

    if command_id != 0:
        return int(command_id)


if __name__ == "__main__":
    voice_sensor = DFRobot_DF2301Q_I2C(sda=SDA_PIN, scl=SCL_PIN)
    setup(sensor=voice_sensor)

    print('Speak your commands:')

    while True:
        cmd_id = get_cmd_id(sensor=voice_sensor)

        if isinstance(cmd_id, int):
            print(f'COMMAND ID: {cmd_id}')

        sleep(SLEEP_SECONDS)

