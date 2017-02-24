#!/usr/bin/python
# Degaussing Program
# Mon Jun 27 2016 Jeff and Henri
# Fri Feb 17 15:07:39 CST 2017 Jeff and Mike removed the scope for degaussing.


import base_module as bm
import numpy
import time

print('\nInitializing devices:\n')

degaussing = bm.degaussing("/dev/usbtmc1")

print('I think the function generator is\n')
degaussing.printName()

# Degauss Settings

freq_degauss = 10
volt_degauss = 10
sample_rate = 10000

#magnetic field parameters
field_amp = .5
field_freq= .01


# if (raw_input("\nHave you set the ramp (Y)/N ?  ")=="N"):
#    degaussing.rampset()
#    raw_input("Press ENTRE to continue.")
#print ('setting the ramp')
#degaussing.rampset()
print ('Please close the switch.')
raw_input("press ENTER to continue.")
print('\nStarting degaussing')
#    scope_data.scope_degauss(mod_freq)
degaussing.func_gen_degauss(freq_degauss,volt_degauss,sample_rate)
print("Degaussing completed")

print ('Please open the switch.')
raw_input("pres ENTER to continue.")

degaussing.mag_field(field_amp,field_freq)
