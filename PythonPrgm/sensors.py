#Attempt to breakdown the labview program into readable python program
#Documentation should also be readable

class HX94A:
    """This class represents the HX94A Temperature and Relative Humidity (RH) sensor. 
    It's designed to acquire readings from the sensor and convert these readings into 
    relevant temperature and humidity values.

    The class supports readings in both current and voltage modes, and can provide 
    temperature readings in either Celsius or Fahrenheit. The relative humidity 
    is given as a percentage.

    Attributes:
        output_value (float): The current or voltage output of the sensor depending on the mode
        output_mode (str): The mode of output from the sensor; ('voltage','current')
        temp_units (str): The unit for temperature measurement; ('C','F')

    Outputs:
        temp (float): The temperature reading from the sensor, in the specified units ('C' or 'F').
        RH (float): The relative humidity reading from the sensor, in percentage form; (e.g., 100% is represented as 100).

    Methods:
        read_sensor: Reads the sensor data and updates the temperature and RH values according to the specified mode and units.
    """

    def __init__(self, output_value: float, output_mode = 'CURRENT', temp_units ='F'):
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
        #update class values with sensor values
        if self._output_mode == 'CURRENT':
            self._current_mode()
        elif self._output_mode == 'VOLTAGE':
            self._voltage_mode()
        
        return(self.temp, self.RH)
        
    def _current_mode(self):
        #current output: 4-20 mA
        #convert to mA
        current_mA = self._output_value * 1000
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


sensor = HX94A(.008)
print(sensor.read_sensor())