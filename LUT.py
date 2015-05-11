#!/usr/bin/env python

from optparse import OptionParser, make_option
from ROOT import *
import subprocess
import multiprocessing
import os
from array import array
from ctypes import *
import struct
import numpy as np

treeName="finalTree"
data = TChain(treeName)
mc = TChain(treeName)

histos={}

ROOT.gROOT.SetBatch()
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(11111)

def customizeCanvas(c):
    c.Range(0,0,1,1)
    c.SetFillColor(0)
    c.SetBorderMode(0)
    c.SetBorderSize(2)
    c.SetTickx(1)
    c.SetLeftMargin(0.13)
    c.SetRightMargin(0.07)
    c.SetTopMargin(0.09)
    c.SetBottomMargin(0.1)
    c.SetFrameFillStyle(0)
    c.SetFrameBorderMode(0)


def drawText(additional_text):
    tex_m=TLatex()
    tex_m.SetNDC()
    tex_m.SetTextAlign(12)
    tex_m.SetTextSize(0.037)
    tex_m.SetLineWidth(2)
    tex_m.DrawLatex(0.25,0.94,text)
    
    if (additional_text != ""):
        tex_m.SetTextSize(0.045)
        tex_m.DrawLatex(0.63,0.63,additional_text)
        
#def plot(variable,plotsDir,additional_cuts="1",pars['additional_text']="",savefmts=[".C",".png",".pdf"]):
def chargeLUT(savefmts=[".C",".png",".pdf",".root"]):
    for target in range(6):
        try:
            os.stat('LUT')
        except:
            os.mkdir('LUT') 
        out_path = 'LUT/M0209_8timesData/00'+str(target)+'_XraySpectrum_p17'
        try:
            os.stat(out_path)
        except:
            os.makedirs(out_path)
        outfile = TFile(str(out_path)+"/commander_XraySpectrum.root", "RECREATE")
        cdXray = outfile.mkdir('Xray')
        cdXray.cd()
        in_path = "M0209_VcalCalibrationTanH_fullRange_2015-04-30_14h40m_1430397616/00"+str(target+2)+"_XraySpectrum_p17/commander_XraySpectrum.root"
        print in_path
        infileXray = TFile(in_path, "READ")
        tree = infileXray.Get('Xray/events')
#        infileLUT = TFile("phCurvesLowRange.root", "READ")
        gP = [[[[0. for x in range(3)]for x in range(80)]for x in range(52)]for x in range(16)]
        for chip in range(16):
            f = open("M0209_VcalCalibrationTanH_fullRange_2015-04-30_14h40m_1430397616/00"+str(target+2)+"_XraySpectrum_p17/8New_phCalibrationFitErr35_C"+str(chip)+".dat")
            lines = [line.strip() for line in f]
            lines = lines[3:]
            for line in lines:
                gP[chip][int(line.split()[5])][int(line.split()[6])][0] = float(line.split()[0])
                gP[chip][int(line.split()[5])][int(line.split()[6])][1] = float(line.split()[1])
                gP[chip][int(line.split()[5])][int(line.split()[6])][2] = float(line.split()[2])
        hQ = TH1D('init','init', 1, 0., 1.)
        hQs={}
        for chip in range(16):
            hQ = TH1D('q_Ag_C'+str(chip)+'_V0','q_Ag_C'+str(chip)+'_V0', 2000, 0., 2000.)
            hQs[chip]=hQ
        for chip in range(16):
            print hQs[chip].GetName()
        ph=0.
#        chip=array("h")
#        chip.append(0)
        for entry in tree:
            for i in range(len(entry.pval)):
                ph=entry.pval[i]
                #print ph
  #              chip = chip_t()
 #               chip.Chip=int(entry.proc[i])
#                print chip.Chip
                #print type(entry.proc[i])
                #print ord(entry.proc[i])
                
                chip = ord(entry.proc[i])
#                chip1=0
#                libc.sscanf(entry.proc[i], "%h", chip1)
#                chip=c_ushort()
#                chip.value = entry.proc[i]
                #print chip
                col=ord(entry.pcol[i])
                #print col
                row=ord(entry.prow[i])
                #print row
                #print 'PhCurves/phcurve_Vcal_c'+str(col)+'_r'+str(row)+'_C'+str(chip)
#                hLUT = infileLUT.Get('PhCurves/phcurve_vcal_c'+str(col)+'_r'+str(row)+'_C'+str(chip))
                print 'Parameters '+str(gP[chip][col][row][0])+' '+str(gP[chip][col][row][1])+' '+str(gP[chip][col][row][2])+' ph '+str(ph)
                charge = (-gP[chip][col][row][1]+np.sqrt(gP[chip][col][row][1]**2-4*(gP[chip][col][row][0]-ph)*gP[chip][col][row][2]))/(2*gP[chip][col][row][2])
                #print 'charge '+str(charge)
                #charge = hLUT.GetBinLowEdge(hLUT.FindFirstBinAbove(ph))
                hQs[chip].Fill(charge)
        outfile.cd()
        cdXray.cd()
        for hqi in hQs:
            hQs[hqi].Write()
        outfile.Write()
        outfile.Close()
        infileXray.Close()
#        infileLUT.Close()

#    
#if __name__ == "__main__":
#    parser = OptionParser(option_list=[
#        make_option("--dataFiles",
#                    action="store", type="string", dest="dataFiles",
#                    default="data.txt",
#                    help="", metavar=""
#                    ),
#        make_option("--mcFiles",
#                    action="store", type="string", dest="mcFiles",
#                    default="mc.txt",
#                    help="", metavar=""
#                    ),
#        make_option("--plotsDir",
#                    action="store", type="string", dest="plotsDir",
#                    default="plots/",
#                    help="", metavar=""
#                    ),
#        make_option("--additionalText",
#                    action="store", type="string", dest="additionalText",
#                    default="",
#                    help="", metavar=""
#                    ),
#        make_option("--additionalCuts",
#                    action="store", type="string", dest="additionalCuts",
#                    default="1",
#                    help="", metavar=""
#                    ),
#        make_option("--numberOfCPU",
#                    action="store", type="int", dest="numberOfCPU",
#                    default=-1,
#                    help="", metavar=""
#                    )
#        ])
#    
#    (options, args) = parser.parse_args()
    
def main():
    chargeLUT();

main()
