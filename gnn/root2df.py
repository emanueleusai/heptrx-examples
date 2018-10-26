from ROOT import gROOT,TFile,TVector3
import numpy as np
import pandas as pd
import numpy as np

gROOT.SetBatch()

inputfile=TFile('savehits_output.root','READ')
t=inputfile.hits_tree

hits_keys=['evtid','hitid','barcode','volid','layid','x','y','z','r','phi','theta','eta']
particles_keys=['evtid', 'barcode', 'q','vx','vy','vz','p','theta','phi','pt','eta']

hits_dict={}
for key in hits_keys:
	hits_dict[key]=[]
particles_dict={}
for key in particles_keys:
	particles_dict[key]=[]

iev=-1
for e in t:
	iev=iev+1
	for itr in range(len(e.track_pt)):
		particles_dict['evtid'].append(iev)
		particles_dict['barcode'].append(itr)
		particles_dict['q'].append(e.track_charge[itr])
		particles_dict['vx'].append(e.track_vx[itr])
		particles_dict['vy'].append(e.track_vy[itr])
		particles_dict['vz'].append(e.track_vz[itr])
		vpar=TVector3(0,0,0)
		vpar.SetPtEtaPhi(e.track_pt[itr],e.track_eta[itr],e.track_phi[itr])
		particles_dict['p'].append(vpar.Mag())
		particles_dict['theta'].append(vpar.Theta())
		particles_dict['phi'].append(vpar.Phi())
		particles_dict['pt'].append(vpar.Pt())
		particles_dict['eta'].append(vpar.Eta())
		for ihit in range(len(e.track_hit_layer[itr])):
			hits_dict['evtid'].append(iev)
			hits_dict['hitid'].append(ihit)
			hits_dict['barcode'].append(itr)
			hits_dict['volid'].append(e.track_hit_sub_det[itr][ihit])
			hits_dict['layid'].append(e.track_hit_layer[itr][ihit])
			vhit=TVector3(e.track_hit_global_x[itr][ihit],e.track_hit_global_y[itr][ihit],e.track_hit_global_z[itr][ihit])
			hits_dict['x'].append(vhit.X())
			hits_dict['y'].append(vhit.Y())
			hits_dict['z'].append(vhit.Z())
			hits_dict['r'].append(vhit.Pt())
			hits_dict['phi'].append(vhit.Phi())
			hits_dict['theta'].append(vhit.Theta())
			hits_dict['eta'].append(vhit.Eta())

hits_df=pd.DataFrame(hits_dict)
particles_df=pd.DataFrame(particles_dict)

hits_df.to_pickle('hits_df.pkl')
hits_df.to_hdf('hits_df.h5', key='df', mode='w')

particles_df.to_pickle('particles_df.pkl')
particles_df.to_hdf('particles_df.h5', key='df', mode='w')