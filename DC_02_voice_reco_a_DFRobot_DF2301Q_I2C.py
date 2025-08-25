from micropython import const
from machine import I2C, Pin
from utime import sleep


DF2301Q_I2C_ADDR = const(0x64)


class DFRobot_DF2301Q_I2C:
    """
    MicroPython class for communication with the DF2301Q from DFRobot via I2C
    """

    DF2301Q_I2C_REG_CMDID = const(0x02)
    DF2301Q_I2C_REG_PLAY_CMDID = const(0x03)
    DF2301Q_I2C_REG_SET_MUTE = const(0x04)
    DF2301Q_I2C_REG_SET_VOLUME = const(0x05)
    DF2301Q_I2C_REG_WAKE_TIME = const(0x06)
    DF2301Q_I2C_8BIT_RANGE = const(0xFF)
    DF2301Q_I2C_PLAY_CMDID_DURATION = const(1)

    def __init__(self, sda, scl, i2c_addr=DF2301Q_I2C_ADDR, i2c_bus=0):
        """
        Initialize the DF2301Q I2C communication
        :param sda: I2C SDA pin
        :param scl: I2C SCL pin
        :param i2c_addr: I2C address
        :param i2c_bus: I2C bus number
        """
        self._addr = i2c_addr

        try:
            self._i2c = I2C(i2c_bus, sda=Pin(sda), scl=Pin(scl))
        except Exception as err:
            print(f'Could not initialize i2c! bus: {i2c_bus}, sda: {sda}, scl: {scl}, error: {err}')

    def _write_reg(self, reg, data) -> None:
        """
        Writes data to the I2C register
        :param reg: register address
        :param data: data to write
        :return: None
        """
        if isinstance(data, int):
            data = [data]

        try:
            self._i2c.writeto_mem(self._addr, reg, bytearray(data))
        except Exception as err:
            print(f'Write issue: {err}')

    def _read_reg(self, reg, length) -> bytes:
        """
        Reads data from the I2C register
        :param reg: register address
        :param length: number of bytes to read
        :return: bytes or 0
        """
        try:
            result = self._i2c.readfrom_mem(self._addr, reg, length)
        except Exception as err:
            print(f'Read issue: {err}')
            result = [0, 0]

        return result

   
    def get_cmdid(self) -> int:
        """
        Returns the current command id
        :return: int
        """
        cmd = self._read_reg(self.DF2301Q_I2C_REG_CMDID, 1)
        if type(cmd) == bytes:
            return int.from_bytes(cmd, "big") # Change bytes to int
        elif type(cmd) == list:
            return 0  # Return 0 in case of read failure

    def get_wake_time(self) -> int:
        """
        Returns the current wake-up duration
        :return: int
        """
        return int(self._read_reg(self.DF2301Q_I2C_REG_WAKE_TIME, 1))

    def play_by_cmdid(self, cmdid: int) -> None:
        """
        Play the current command words by command id
        :param cmdid: command words as integer
        :return: None
        """
        self._write_reg(self.DF2301Q_I2C_REG_PLAY_CMDID, int(cmdid))
        sleep(self.DF2301Q_I2C_PLAY_CMDID_DURATION)

    def set_wake_time(self, wake_time: int) -> None:
        """
        Set the wake-up duration of the device
        :param wake_time: integer between 0 and 255
        :return: None
        """
        wake_up_time = int(wake_time) & self.DF2301Q_I2C_8BIT_RANGE
        self._write_reg(self.DF2301Q_I2C_REG_WAKE_TIME, wake_up_time)

    def set_volume(self, vol: int) -> None:
        """
        Set the volume of the device
        :param vol: integer between 1 and 7
        :return: None
        """
        self._write_reg(self.DF2301Q_I2C_REG_SET_VOLUME, int(vol))

    def set_mute_mode(self, mode) -> None:
        """
        Set the mute mode of the device
        :param mode: integer 0 for off, 1 for on
        :return: None
        """
        self._write_reg(self.DF2301Q_I2C_REG_SET_MUTE, int(bool(mode)))                    
