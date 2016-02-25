import h5py
import numpy

# Create the file to store C5G7 multi-groups cross-sections
f = h5py.File('materials-data.h5')
f.attrs["# groups"] = 2

# Create a group to specify that MGXS are split by material (vs. cell)
material_group = f.create_group('material')

###############################################################################
################################      fuel      ###############################
###############################################################################

# Create a subgroup for fuel materials data
fuel = material_group.create_group('fuel')

sigma_t = numpy.array([2.0/9.0, 5.0/6.0])
sigma_s = numpy.array([ 71.0/360.0,  .02, 
                        0.0,         11.0/15.0])                    
sigma_f = numpy.array([1.0/480.0, 1.0/16.0])
nu_sigma_f = numpy.array([2.4, 2.4])
chi = numpy.array([1.0, 0.0])

# Create datasets for each cross-section type
fuel.create_dataset('total', data=sigma_t)
fuel.create_dataset('scatter matrix', data=sigma_s)
fuel.create_dataset('fission', data=sigma_f)
fuel.create_dataset('nu-fission', data=nu_sigma_f)
fuel.create_dataset('chi', data=chi)

###############################################################################
##############################      water     #################################
###############################################################################

# Create a subgroup for water materials data
water = material_group.create_group('water')

sigma_t = numpy.array([2.0/9.0, 5.0/3.0])
sigma_s = numpy.array([ 71.0/360.0,  .025, 
                        0.0,         47.0/30.0])                    
sigma_f = numpy.array([0.0, 0.0])
nu_sigma_f = numpy.array([2.4, 2.4])
chi = numpy.array([0.0, 0.0])

# Create datasets for each cross-section type
water.create_dataset('total', data=sigma_t)
water.create_dataset('scatter matrix', data=sigma_s)
water.create_dataset('fission', data=sigma_f)
water.create_dataset('nu-fission', data=nu_sigma_f)
water.create_dataset('chi', data=chi)

# Close the hdf5 data file
f.close()
