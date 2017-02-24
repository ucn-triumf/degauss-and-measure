# Fri Feb 17 15:07:39 CST 2017
# Jeff and Mike modified for Agilent 33522A function generator.

import os
import time
import numpy

datetime = time.strftime('%d_%m_%Y__%H_%M_%S')


voltagescale = "200E-2"
voltagescalech3 = "200E-3"
filename = datetime+"test"

class Instrument:

    """ Instrument base class"""

    def __init__(self,device):
        self.device = device
        self.FILE = os.open(device, os.O_RDWR)

    def write(self,command):
        os.write(self.FILE,command)

    def read(self,length=4000):
        return os.read(self.FILE, length)

    def getName(self):
        self.write("*IDN?")
        return self.read(300)

    def printName(self):
        self.name=self.getName()
        print(self.name)

    def sendReset(self):
        self.write("*RST")

    def read_scope(self):
        self.read_scope_data = read_scope_data


# degaussing using an Agilent 33522A

class degaussing(Instrument):

    """Class to do idealization"""

    def rampset(self):

        """ Setting the ramp"""

       # print('This function is not necessary for Agilent 33522A.')
       # print('Should put here all the stuff that you should do to get the arb set up properly')
        print ('Load an arbitrary waveform segment from the internal drive into volatile memory for channel one and selects it for use')

        #self.write("MMEMO:LOAD:DATA1 INT:\Builtin\DG.arb")
       # self.write("FUNC:ARB"INT:\Builtin\DG.arb"")

    def func_gen_degauss(self, freq_degauss,volt_degauss,sample_rate):
        self.write("OUTP2 OFF")
        print('Agilent configured for degaussing sequence')
        self.write("SOUR1:BURS:STAT OFF") # Burst off
        self.write("SOUR1:FUNC SIN")
        self.write("SOUR1:AM:INT:FUNC ARB")
        freq_degauss_str = str(freq_degauss)
        self.write("SOUR1:FREQ "+freq_degauss_str)
        volt_degauss_str = str(volt_degauss)
        self.write("SOUR1:VOLT "+volt_degauss_str)
        self.write("SOUR1:PHAS 0.0")
        self.write("FUNC:ARB:SRAT "+str(sample_rate)) # change sample
        # rate for
        # arbitrary
        # waveform in
        # order to
        # change ramp
        self.write("SOUR1:VOLT:OFFS 0.00") # Carrier freq is 60 Hz @ 10 Vpp
        self.write("SOUR1:AM:DEPT 100") # Modulation depth = 100%
        self.write("SOUR1:AM:STAT ON") #Modulation on
        self.write("OUTP ON") # Turn on the instrument output
        
        # figure out how long to wait
        # The waveform DG has 10^6 samples
        num_samples=1000000
        full_time=num_samples/sample_rate
        wait_time=full_time*0.55
        
        time.sleep(wait_time)
#        self.write("OUTP:TRIG OFF") # Turn off
#        self.write("OUTP:SYNC OFF")
#        self.write("SOUR1:VOLT 0.01")
#        self.write("SOUR1:AM:DEPT 0") # Modulation depth = 0%
#        self.write("SOUR1:AM:STAT OFF") # Turn AM modulation off
        self.write("OUTP OFF ")
        
        # Do some commands to stop triggers from coming (set up burst mode)
         #self.write("OUTP:TRIG:SOUR CH1")
         #self.write("TRIG:SOUR IMM")
         ###self.write("SOUR1:FUNC SIN")
         ###self.write("SOUR1:BURS:NCYC 1") # One cycle
         ###self.write("SOUR1:BURS:STAT ON") # Burst on
         ###self.write("BURS:MODE TRIG")
         ###self.write("TRIG:SOUR BUS") # Set trigger source to bus
        
        
    def mag_field(self,field_amp,field_freq):
        self.write("SOUR2:FUNC RAMP")
        field_freq_str = str(field_freq)
        self.write("SOUR2:FREQ "+field_freq_str)
        field_amp_str = str(field_amp)
        self.write("SOUR2:VOLT "+field_amp_str)
        self.write("SOUR2:BURS:NCYC 1")
        self.write("OUTP2 ON")
        self.write("BURS:MODE TRIG")
        self.write("TRIG:SOUR INT")
        self.write("SOUR2:BURS:STAT ON")
