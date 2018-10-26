
'''
==============
3D scatterplot
==============

Demonstration of a basic scatterplot in 3D.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import ROOT
from array import array

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

inputfile=ROOT.TFile('savehits_output.root','READ')
t=inputfile.hits_tree
outfile=ROOT.TFile('rh.root','RECREATE')

matcheff=ROOT.TH2F('matcheff','',2,0,2,7,0,7)
matchden=ROOT.TH2F('matchden','',2,0,2,7,0,7)

histo_layer=ROOT.TH1F('histo_layer','',7,0,7)

for e in t:
	for tr in range(len(e.track_pt)):
		for hit in range(len(e.track_hit_sub_det[tr])):
			if e.track_hit_sub_det[tr][hit]==5:
				histo_layer.Fill(e.track_hit_layer[tr][hit])
				print(e.track_hit_layer[tr][hit])



	for rh in range(len(e.hit_global_x)):
		if e.hit_recotrack_match[rh]:
			a=0
			if e.hit_simtrack_match[rh]:
				a=1
			matcheff.Fill(a,e.hit_sub_det[rh])
			matchden.Fill(0,e.hit_sub_det[rh])
			matchden.Fill(1,e.hit_sub_det[rh])
		
matcheff.Divide(matchden)
matcheff.Write()
c=ROOT.TCanvas('c','',600,600)
matcheff.Draw('colz')
c.SaveAs('pdf/matcheff.pdf')
d=ROOT.TCanvas('c','',600,600)
histo_layer.Draw('colz')
d.SaveAs('pdf/histo_layer.pdf')
outfile.Close()
inputfile.Close()
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# n = 100

# # For each set of style and range settings, plot n random points in the box
# # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
# rechits_t=list(map(list, zip(*rechits)))

# xs = array( 'd' , rechits_t[0])
# ys = array( 'd' , rechits_t[1])
# zs = array( 'd' , rechits_t[2])
# ax.scatter(zs, xs, ys, c='b',alpha=0.5, marker='.',s=1)

# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')

# plt.show()
