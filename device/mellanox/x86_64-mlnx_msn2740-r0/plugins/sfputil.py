# sfputil.py
#
# Platform-specific SFP transceiver interface for SONiC
#

try:
    import time
    import subprocess
    from sonic_sfp.sfputilbase import SfpUtilBase
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))


class SfpUtil(SfpUtilBase):
    """Platform-specific SfpUtil class"""

    PORT_START = 0
    PORT_END = 31
    PORTS_IN_BLOCK = 32

    EEPROM_OFFSET = 1

    _port_to_eeprom_mapping = {}

    @property
    def port_start(self):
        return self.PORT_START

    @property
    def port_end(self):
        return self.PORT_END

    @property
    def qsfp_ports(self):
        return range(0, self.PORTS_IN_BLOCK + 1)

    @property
    def port_to_eeprom_mapping(self):
        return self._port_to_eeprom_mapping

    def __init__(self):
        eeprom_path = "/bsp/qsfp/qsfp{0}"

        for x in range(0, self.port_end + 1):
            self._port_to_eeprom_mapping[x] = eeprom_path.format(x + self.EEPROM_OFFSET)

        SfpUtilBase.__init__(self)

    def get_presence(self, port_num):
        # Check for invalid port_num
        if port_num < self.port_start or port_num > self.port_end:
            return False

        try:
            reg_file = open("/bsp/qsfp/qsfp%d_status" % (port_num+1))
        except IOError as e:
            print "Error: unable to open file: %s" % str(e)
            return False

        content = reg_file.readline().rstrip()

        # content is a string with the qsfp status
        if content == "good":
            return True

        return False

    def get_low_power_mode(self, port_num):
        # Check for invalid port_num
        if port_num < self.port_start or port_num > self.port_end:
            return False

        lpm_cmd = "docker exec syncd python /usr/share/sonic/platform/plugins/sfplpmget.py {}".format(port_num)

        try:
            output = subprocess.check_output(lpm_cmd, shell=True)
            if 'LPM ON' in output:
                return True
        except subprocess.CalledProcessError as e:
            print "Error! Unable to get LPM for {}, rc = {}, err msg: {}".format(port_num, e.returncode, e.output)
            return False

        return False

    def set_low_power_mode(self, port_num, lpmode):
        # Check for invalid port_num
        if port_num < self.port_start or port_num > self.port_end:
            return False

        lpm = 'on' if lpmode else 'off'
        lpm_cmd = "docker exec syncd python /usr/share/sonic/platform/plugins/sfplpmset.py {} {}".format(port_num, lpm)

        try:
            subprocess.check_output(lpm_cmd, shell=True)
            return True
        except subprocess.CalledProcessError as e:
            print "Error! Unable to set LPM for {}, rc = {}, err msg: {}".format(port_num, e.returncode, e.output)
            return False

        return False

    def reset(self, port_num):
        # Check for invalid port_num
        if port_num < self.port_start or port_num > self.port_end:
            return False

        lpm_cmd = "docker exec syncd python /usr/share/sonic/platform/plugins/sfpreset.py {}".format(port_num)

        try:
            subprocess.check_output(lpm_cmd, shell=True)
            return True
        except subprocess.CalledProcessError as e:
            print "Error! Unable to set LPM for {}, rc = {}, err msg: {}".format(port_num, e.returncode, e.output)
            return False

        return False
