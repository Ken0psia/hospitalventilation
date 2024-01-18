#Attempt to breakdown the labview program into readable python program
#Documentation should also be readable
from datetime import datetime

class HX94_TEMPRH:
    """This class is designed to convert readings from the HX94A and HX94C Temperature and 
    Relative Humidity (RH) sensors into relevant temperature and humidity values.
    The class supports readings in both current and voltage modes, and can provide 
    temperature readings in either Celsius or Fahrenheit. The relative humidity 
    is given as a percentage.

    Attributes:
        output_value (float): The current [A] or voltage [V] output of the sensor depending on the mode
        output_mode (str): The mode of output from the sensor; ('voltage','current')
        temp_units (str): The unit for temperature measurement; ('C','F')

    Outputs:
        temp (float): The temperature reading from the sensor, in the specified units ('C' or 'F').
        RH (float): The relative humidity reading from the sensor, in percentage form;
                    (e.g., 100% is represented as 100).

    Methods:
        read_sensor: Reads the sensor data; returns and updates temperature and RH values.  
    """

    def __init__(self, output_value: float, output_mode = 'CURRENT', temp_units ='F'):
        #defaults: output_mode = 'CURRENT'; temp_units='F'; based on current experiment setup (Fall 2023)
        #initialize vars
        self._output_mode = str.upper(output_mode) #uppercase
        self._output_value = output_value
        self._temp_units = str.upper(temp_units) #uppercase
        #check if valid input
        self._validate_parameters(self._output_mode, self._output_value, self._temp_units)

    def _validate_parameters(self, output_mode, output_value, temp_units):
        #raise error if any value not valid or within range of sensor specs
        if output_mode not in ['CURRENT', 'VOLTAGE']:
            raise ValueError('Invalid output mode')
        if temp_units not in ['C', 'F']:
            raise ValueError('Invalid temperature units')
        if output_mode == 'CURRENT' and (output_value < 0.004 or output_value > 0.02):
            raise ValueError('Current out of range')
        if output_mode == 'VOLTAGE' and (output_value < 0 or output_value > 1):
            raise ValueError('Voltage out of range')
    
    def read_sensor(self):
        '''Returns: (temp, RH)
        '''
        #update class values with sensor values
        if self._output_mode == 'CURRENT':
            self._current_mode()
        elif self._output_mode == 'VOLTAGE':
            self._voltage_mode()
        
        return(self.temp, self.RH)
        
    def _current_mode(self):
        #current range: 4-20 mA
        current_mA = self._output_value * 1000#convert to mA
        #calculate RH as per data sheet
        self.RH = (current_mA - 4) / 0.16
        
        #calculate temp as per data sheet
        #dependent on temp_units
        if self._temp_units == 'C':
            self.temp = (current_mA - 4) / 0.16
        elif self._temp_units == 'F':
            self.temp = (current_mA - 4) * 11.25 + 32 #divide by 0.08888 is given in data sheet but 1/0.08888 == 11.25
        
    def _voltage_mode(self):
        #voltage output: 0-1 VDC
        #calculate RH as per data sheet
        voltage = self._output_value
        self.RH = voltage * 100

        #calculate temp as per data sheet 
        #dependent on temp_units
        if self._temp_units == 'C':
            self.temp = voltage / 0.01 #says 0.1 in data sheet but data sheet is wrong :(
        elif self._temp_units == 'F':
            self.temp = (voltage * 180) + 32 #divide by 0.005555 given in data sheet but 1/0.005555 == 180

def WRITE_MCP4922(channel, value, GPIO):


    #from MCP49x2 data sheet
    command = 0b1010 if channel == 1 else 0b0010

    #high byte: shift command to make room for value
    #shift value over and truncate
    high = (command << 4) | ((value >> 8) & 0b1111)
    low = value & 0b11111111

    GPIO.output(GPIO, GPIO.LOW)

    #spi.xfer2([high,low])
    
    GPIO.output(GPIO, GPIO.HIGH)


now = datetime.now()
hour, minute, second = str(now).split(' ')[1][0:-5].split(":")
print(hour, minute, second)