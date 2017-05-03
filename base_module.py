# Fri Feb 17 15:07:39 CST 2017
# Jeff and Mike modified for Agilent 33522A function generator.

import os
import time
import numpy

datetime = time.strftime('%d_%m_%Y__%H_%M_%S')


voltagescale = "200E-2"
voltagescalech3 = "200E-3"
#filename = datetime+"test"

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

    def func_gen_degauss(self, freq_degauss,volt_degauss,offset_degauss,sample_rate):
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
        offset_degauss_str = str(offset_degauss)
        self.write("SOUR1:VOLT:OFFS "+offset_degauss_str)
        self.write("SOUR1:AM:DEPT 100") # Modulation depth = 100%
        self.write("SOUR1:AM:STAT ON") #Modulation on
        self.write("OUTP ON") # Turn on the instrument output
        
        # figure out how long to wait
        # The waveform DG has 10^6 samples
        num_samples=1000000
        full_time=num_samples/sample_rate
        wait_time=full_time*0.5+2
        
        time.sleep(wait_time)
#        self.write("OUTP:TRIG OFF") # Turn off
#        self.write("OUTP:SYNC OFF")
#        self.write("SOUR1:VOLT 0.01")
#        self.write("SOUR1:AM:DEPT 0") # Modulation depth = 0%
#        self.write("SOUR1:AM:STAT OFF") # Turn AM modulation off
        self.write("OUTP OFF")
        
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
        self.write("TRIG2:SOUR BUS")
        self.write("SOUR2:BURS:NCYC 1")
        self.write("SOUR2:BURS:MODE TRIG")
        self.write("SOUR2:BURS:STAT ON")
        self.write("OUTP2 ON")
        self.write("*TRG")



class TekScope(Instrument):
    
    """ Tektronix DPO 4054 class"""

    def scope_degauss(self,mod_freq):
        print("Scope configured for degaussing sequence")
        self.write("TRIG:A:MOD AUTO")
        self.write("ACQ:STATE RUN")
        self.write("HOR:DEL:MOD OFF")
	time_scale_degauss = 0.04/mod_freq
	time_scale_degauss_str = str(time_scale_degauss)
        self.write("HOR:SCA "+time_scale_degauss_str) # Has to be 0.04/mod_freq to get full degausse sequence
        self.write("HOR:RECO 10000")
        self.write("HOR:POS 0")
        self.write("TRIG:A:EDGE:SOU LINE")
	self.write("CH1:SCALe "+voltagescale) 
        self.write("CH2:SCALe "+voltagescale)
	self.write("CH3:SCALe "+voltagescalech3)
	self.write("CH4:SCALe "+voltagescalech3)
        
    def scope_bh(self,freq_bh):
        print("Scope configured for a B-H curve measurement")
        self.write("TRIG:A:MOD NORMAL")
        self.write("ACQ:STATE STOP")
	time_scale_bh = 0.2/freq_bh
	if time_scale_bh < 0.04:
	    time_scale_bh = 0.04
	#if time_scale_bh == 0.04:
	    #time_scale_bh = 0.1
        else :
            time_scale_bh = time_scale_bh
	time_scale_bh_str = str(time_scale_bh)
        self.write("HOR:SCA "+time_scale_bh_str)
        self.write("HOR:RECO 10000")
        self.write("HOR:POS 0")
        self.write("TRIG:A:EDGE:SOU CH4")
        self.write("ACQ:STATE RUN")
	self.write("CH1:SCALe "+voltagescale) 
        self.write("CH2:SCALe "+voltagescale)
	self.write("CH3:SCALe "+voltagescalech3)
        time.sleep(1)

####################### Data Acquisiton #######################
    
    def read_data( self ):
        self.write( "CURV?" )
        rawdata = self.read(20000) # 20000 saves whole scope 
        return numpy.frombuffer( rawdata[7:-1], 'i2' )
    
    def scale_data( self,source ):

        """method to scale data """

        self.write("DATA:SOURCE " + source)
        data = self.read_data()
        print("Got data for "+ source)
        self.write("WFMPRE:YMUlt?")
        ymult = float(self.read(200))
        self.write("WFMPRE:YOFF?")
        yoff=float(self.read(200))
        self.write("WFMPRE:YZERO?")
        yzero = float(self.read(200))
        print("For "+source,ymult,yoff,yzero)

        data = ((data - yoff) * ymult) + yzero
        return data

    def get_xdata(self):

        """Method to get horizontal data array from a scope"""

        self.write("HORIZONTAL:MAIN:SCALE?")
        self.timescale = float(self.read(20))
        self.write("HORIZONTAL:MAIN:POSITION?")
        self.timeoffset = float(self.read(20))
        self.write("HORIZONTAL:RECORDLENGTH?")
        self.time_size=int(self.read(30))

        self.time=numpy.arange(0,self.timescale*10,self.timescale*10/self.time_size)
        return self.time

    """ reading scope"""

    def adjusting(self):
        self.write("ACQ:STATE STOP") # Stop data acquisition
        self.write("DATA:WIDTH 2") # Set data width to 2 for better resolution
        self.write("DATA:ENCD SRI") # Set data format to binary, zero is center-frame and big endian

    def data_array(self):
         
        self.write("SELECT?")
        self.wfms=self.read(20)
        print(self.wfms)

        # parse into array of characters
        self.wfms = self.wfms.strip().split(";")

        if self.wfms[0]=="1":
            self.ch1data = self.scale_data("CH1")

        if self.wfms[1]=="1":
            self.ch2data = self.scale_data("CH2")

        if self.wfms[2]=="1":
            self.ch3data = self.scale_data("CH3")
	if self.wfms[3]=="1":
            self.ch4data = self.scale_data("CH4")

    def time_scale(self):
         #get the time scale

        self.write("HORIZONTAL:MAIN:SCALE?")
        self.timescale = float(self.read(20))

        # Get the timescale offset
        self.write("HORIZONTAL:MAIN:POSITION?")
        self.timeoffset = float(self.read(20))

        # Get the length of the horizontal record
        self.write("HORIZONTAL:RECORDLENGTH?")
        self.time_size = int(self.read(30))

        self.time = numpy.arange(0,self.timescale*10,self.timescale*10/self.time_size)
        print(self.time)
#        self.write("ACQ:STATE RUN")

    def save_data(self,runno):
        filename='run'+str(runno).zfill(5)+'.dat'
        print(filename)
        with open(filename,'w') as thefile:
            for item1,item2,item3,item4,item5 in zip(self.time,self.ch1data,self.ch2data,self.ch3data,self.ch4data):
                print>>thefile,item1,item2,item3,item4,item5

    def run(self):
        self.write("ACQ:STATE RUN")
