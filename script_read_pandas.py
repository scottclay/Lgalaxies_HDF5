#=========================================================================
#
#  Script to read in L-galaxies snapshot data
#
#  To force a re-read of the data do Gal=None
#
#-------------------------------------------------------------------------

# Imports
# 
import sys

#datadir = '../../Hen15_Dustmodel/output/'
datadir   = '/lustre/scratch/astro/sc558/Clay17/MR/'
output_dir = '/lustre/scratch/astro/sc558/Clay17/MR/Pandas/'

sys.path.insert(0,datadir)

# Template structure for L-Galaxies data
sys.path.append('../data/')
sys.path.append('../src/')
import snap_template   # structure temple for data
import read_lgal       # function to read in data
# 
#-------------------------------------------------------------------------
import time 
start_all = time.time()
# Parameters

# Snaplist file
#snaplist_file = '../MRPlancksnaplist.txt'
snaplist_file = '/lustre/scratch/astro/sc558/snaplists/MRPlancksnaplist.txt'
# Define what snapshot you want

#file_prefix = ['0.00','1.04','2.07','3.11','3.95','5.03','5.92','6.97'

file_prefix = {
	0.00:58,
	1.04:38,
	2.07:30,
	3.11:25,
	3.95:22,
	5.03:19,
	5.92:17,
	6.97:15,
	8.22:13,
	8.93:12,	
	9.72:11,	
	10.57:10,	
	11.51:9,	
	12.53:8,		
	13.66:7,
	14.90:6
	}

min_redshift = 0.00
max_redshift = 15.00

# Define which files you want to read in
firstfile = 0
lastfile = 100

desired_redshifts = {}
for redshift in file_prefix.keys():
	if redshift>=min_redshift and redshift <= max_redshift+0.5:
		#print(redshift,file_prefix[redshift])
		desired_redshifts.update({redshift:file_prefix[redshift]})

print(desired_redshifts)

for i, redshift in enumerate(desired_redshifts.keys(),int(round(min_redshift))):
	snapshot = desired_redshifts[redshift]
	file_prefix = "SA_z"+str("%.2f" % redshift)
	#output_file = "../data/MR/lgal_z"+str(i)+".pkl"
	output_file = output_dir+"lgal_z"+str(i)
	snapdir = datadir+"snapdir_0"+str(snapshot)"
	#print(i,snapshot, file_prefix, output_file)
	

	# Define what properties you want to read in
	props = snap_template.properties_used

	props['Type'] = True
	props['ColdGas'] = True
	props['StellarMass'] = True
	props['BulgeMass'] = True
	props['DiskMass'] = True
	props['HotGas'] = True
	props['ICM'] = True
	props['MetalsColdGas'] = True
	props['MetalsBulgeMass'] = True
	props['MetalsDiskMass'] = True
	props['MetalsHotGas'] = True
	props['MetalsEjectedMass'] = True
	props['MetalsICM'] = True
	props['Sfr'] = True
	props['SfrBulge'] = True
	props['DiskMass_elements'] = True
	props['BulgeMass_elements'] = True
	props['ColdGas_elements'] = True
	props['HotGas_elements'] = True
	#props['DustMassISM'] = True
	props['DustRatesISM'] = True
	props['Dust_elements'] = True
	props['Attenuation_Dust'] = True
	props['Mag'] = True
	props['MagDust'] = True
	props['GasDiskRadius'] = True
	# 
	#-------------------------------------------------------------------------

	# Working body of the program

	# Read in galaxy output
	(nTrees,nHalos,nTreeHalos,gals) = \
		read_lgal.read_snap(snapdir,file_prefix,firstfile,lastfile,\
								props,snap_template.struct_dtype)


	import pickle as cPickle
	fout = open(output_file+".pkl",'wb')
	cPickle.dump(gals,fout,cPickle.HIGHEST_PROTOCOL)
	fout.close()
	
	columns = []
	columns_dt = []
	for i in props.keys():
		if props[i]==True:
			columns.append(i)
			columns_dt.append(snap_template.struct_dtype[i])

	new_names = {
		"MetalsColdGas":['MetalsColdGas.AGB','MetalsColdGas.SNII','MetalsColdGas.SNIA'],
		"MetalsBulgeMass":['MetalsBulgeMass.AGB','MetalsBulgeMass.SNII','MetalsBulgeMass.SNIA'],
		"MetalsDiskMass":['MetalsDiskMass.AGB','MetalsDiskMass.SNII','MetalsDiskMass.SNIA'],
		"MetalsHotGas":['MetalsHotGas.AGB','MetalsHotGas.SNII','MetalsHotGas.SNIA'],
		"MetalsEjectedMass":['MetalsEjectedMass.AGB','MetalsEjectedMass.SNII','MetalsEjectedMass.SNIA'],
		"MetalsICM":['MetalsICM.AGB','MetalsICM.SNII','MetalsICM.SNIA'],
		"MagDust":['MagDust.FUV','MagDust.NUV'],
		"Mag":['Mag.FUV','Mag.NUV'],
		"DiskMass_elements":['DiskMass.H','DiskMass.He','DiskMass.C','DiskMass.N','DiskMass.O','DiskMass.Ne','DiskMass.Mg','DiskMass.Si','DiskMass.S','DiskMass.Ca','DiskMass.Fe'],
		"BulgeMass_elements":['BulgeMass.H','BulgeMass.He','BulgeMass.C','BulgeMass.N','BulgeMass.O','BulgeMass.Ne','BulgeMass.Mg','BulgeMass.Si','BulgeMass.S','BulgeMass.Ca','BulgeMass.Fe'],
		"ColdGas_elements":['ColdGas.H','ColdGas.He','ColdGas.C','ColdGas.N','ColdGas.O','ColdGas.Ne','ColdGas.Mg','ColdGas.Si','ColdGas.S','ColdGas.Ca','ColdGas.Fe'],
		"HotGas_elements":['HotGas.H','HotGas.He','HotGas.C','HotGas.N','HotGas.O','HotGas.Ne','HotGas.Mg','HotGas.Si','HotGas.S','HotGas.Ca','HotGas.Fe'],
		"DustRatesISM":['DustRate.AGB','DustRate.SNII','DustRate.SNIA','DustRate.GROW','DustRate.DEST'],
		"Dust_elements":['Dust.H','Dust.He','Dust.C','Dust.N','Dust.O','Dust.Ne','Dust.Mg','Dust.Si','Dust.S','Dust.Ca','Dust.Fe']
	}

	import pandas as pd
#	start = time.time()

	gals2 = pd.DataFrame()
	for column in columns:
		gals2[column]=list(gals[column])

	gals3=gals2
	for i in gals3.loc[:, gals3.dtypes == object].columns:
		temp_df = pd.DataFrame()
		temp_df = pd.DataFrame(gals3[i].values.tolist(),columns= new_names[i])
		gals3 = pd.concat([gals3,temp_df],axis=1)
		gals3 = gals3.drop(i, axis=1)
		print("Finished "+i)

#	end = time.time()
#	print(str((end - start)) + " secs")
	
	gals3.to_pickle(output_file+'pandas.pkl')
	
#	gals3.to_hdf(output_file+'pandas.hdf',key='gal',format='t')
	
#	import h5py
#	h5save = h5py.File(output_file+".hdf5", "w")
#	h5save.create_dataset('gals', data=gals)
#	h5save.close()

#end_all = time.time()
#print(str((end_all - start_all)) + " secs")






