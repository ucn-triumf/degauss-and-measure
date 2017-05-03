#!/usr/bin/python
# Degaussing Program
# Mon Jun 27 2016 Jeff and Henri
# Fri Feb 17 15:07:39 CST 2017 Jeff and Mike removed the scope for degaussing.
# Fri Mar 17 09:08:05 CDT 2017 recommend to "upgrade" to pyusb at some point.


import base_module as bm
import numpy
import time

print('\nInitializing devices:\n')

datetime = time.strftime('%d_%m_%Y__%H_%M_%S')

degaussing = bm.degaussing("/dev/usbtmc0")
scope_data = bm.TekScope("/dev/usbtmc1")

runlog = "runlog.txt"
runno=0
try:
    f = open(runlog,'r')
except IOError:
    print 'cannot open',runlog
    runno=1
else:
    linelist = f.readlines()
    f.close()
    oldrunno=int(linelist[-1].split(' ')[0])
    runno=oldrunno+1
    print 'Last run was:  ',oldrunno
    print 'This run is:  ',runno
f = open(runlog,'a')


print('I think the function generator is\n')
degaussing.printName()
print('I think the scope is\n')
scope_data.printName()


# Degauss Settings

freq_degauss = 10
volt_degauss = 10
offset_degauss = 0.0
sample_rate = 20000

#magnetic field parameters
field_amp = .5
field_freq= .01

f.write("%d %s %f %f %f %f %f %f\n" % (runno,datetime,freq_degauss,volt_degauss,offset_degauss,sample_rate,field_amp,field_freq))



# if (raw_input("\nHave you set the ramp (Y)/N ?  ")=="N"):
#    degaussing.rampset()
#    raw_input("Press ENTRE to continue.")
#print ('setting the ramp')
#degaussing.rampset()
print ('Please close the switch.')
scope_data.run()
raw_input("press ENTER to continue.")
print('\nStarting degaussing')
#    scope_data.scope_degauss(mod_freq)
degaussing.func_gen_degauss(freq_degauss,volt_degauss,offset_degauss,sample_rate)
print("Degaussing completed")

print ('Please open the switch.')
raw_input("press ENTER to continue.")

degaussing.mag_field(field_amp,field_freq)

time.sleep(1/field_freq+10)

print("\nSaving data:")
scope_data.adjusting()
#raw_input("pres ENTER to continue.")

scope_data.data_array()
#raw_input("pres ENTER to continue.")

scope_data.time_scale()
#raw_input("pres ENTER to continue.")

scope_data.save_data(runno)
