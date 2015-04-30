import ROOT as r
import glob
import numpy as np
import json

temperatures = ['p17', 'm20']
lines = [line.strip() for line in open('modules.list')]
modules=[]

parameters = {}
parameters['Noise'] = dict(json=False, chip = True, path = '*_1/Chips/Chip*/SCurveWidths/SCurveWidths.root', namedistr = 'Noise distribution', namefile = 'NoiseDistr.root', bin=100, xmin=0., xmax=600, xaxistitle = 'Noise [e^{-}]', gradB = 500, gradC = 1000)
parameters['PHCalibrationParameter1'] = dict(json=False, chip = True, path = '*_1/Chips/Chip*/PHCalibrationParameter1/PHCalibrationParameter1.root', namedistr = 'PH Calibration Parameter1', namefile = 'PHCalibrationParameter1.root', bin=350, xmin=-1., xmax=6, xaxistitle = 'Parameter 1', gradB = 4, gradC = 5) # We have to check gradB/C!! 
parameters['VcalThresholdWidth'] = dict(json=False, chip = False, path = '*_1/VcalThresholdWidth/VcalThresholdWidth.root', namedistr = 'Vcal Threshold Width', namefile = 'VcalThresholdWidth.root', bin=600, xmin=0., xmax=600, xaxistitle = 'Width of Vcal Threshold [e^{-}]', gradB = 200, gradC = 400)
parameters['RelativeGainWidth'] = dict(json = False, chip = False, path = '*_1/RelativeGainWidth/RelativeGainWidth.root', namedistr = 'Relative Gain Width', namefile = 'RelativeGainWidth.root', bin=150, xmin=0., xmax=0.25, xaxistitle = 'Relative Gain Width', gradB=0.1, gradC =0.2)
parameters['PedestalSpread'] = dict(json=False, chip = False, path = '*_1/PedestalSpread/PedestalSpread.root', namedistr = 'Pedestal Spread', namefile = 'PedestalSpread.root', bin=240, xmin=0., xmax=5500, xaxistitle = 'Average Pedestal [e^{-}]', gradB = 2500, gradC = 5000)
parameters['Current150V'] = dict(json = True, key = 'CurrentAtVoltage150V', chip = False, path = '*/IVCurve/KeyValueDictPairs.json', namedistr = 'Current at Voltage 150V', namefile = 'Current150V.root', bin=24, xmin=0, xmax=18, xaxistitle = 'Recalculated current at 150V [microA]', gradB = 3, gradC = 15)
parameters['SlopeIV'] = dict(json = True, key = 'Variation', chip = False, path = '*/IVCurve/KeyValueDictPairs.json', namedistr = 'Slope IV', namefile = 'SlopeIV.root', bin=12, xmin=0, xmax=12, xaxistitle = 'Slope IV [microA]', gradB = 400, gradC = 2)

def ModuleList():
   for line in lines:
      if line.startswith('#'):
         continue
      modules.append(line)


def GetFilePath(par, temperature):
   # In order to include the code in Moreweb cfr MoReWeb/Analyse/Controller.py                                                                                                      
   FilePath = []
   for module in modules:
      #print module
      FilePath += glob.glob(module+'/FinalResults-*/QualificationGroup/ModuleFulltest*'+temperature+parameters[par]['path'])
   return FilePath


def CreateHisto(FilePath, par):
   histo = r.TH1D(parameters[par]['namedistr'], parameters[par]['namedistr'], parameters[par]['bin'], parameters[par]['xmin'], parameters[par]['xmax'])
   for i in range(len(FilePath)):
      File = r.TFile(FilePath[i])
      cNoise = File.Get('c1')
      List = cNoise.GetListOfPrimitives()
      histochip = List[1]
      histo.Add(histochip)
   return histo


def CreateHisto2(FilePath, par):
   histo = r.TH1D(parameters[par]['namedistr'], parameters[par]['namedistr'], parameters[par]['bin'], parameters[par]['xmin'], parameters[par]['xmax'])
   for i in range(len(FilePath)):
      File = r.TFile(FilePath[i])
      cNoise = File.Get('c1')
      List = cNoise.GetListOfPrimitives()
      histochip = List[1]
      #print histochip.GetNbinsX()
      for j in range(histochip.GetNbinsX()):
         #if j==0 and str(par)=='RelativeGainWidth':
          #  continue
         #if histochip.GetBinContent(j+1) < 0.009:
          #  print 'File: '+str(FilePath[i])+' bin '+str(j+1)+' bincontent '+str(histochip.GetBinContent(j+1))
         histo.Fill(histochip.GetBinContent(j+1))
   return histo

def CreateHistoFromJson(FilePath, par):
   histo = r.TH1D(parameters[par]['namedistr'], parameters[par]['namedistr'], parameters[par]['bin'], parameters[par]['xmin'], parameters[par]['xmax'])
   for i in range(len(FilePath)):
      with open(FilePath[i]) as json_data:
         d = json.load(json_data)
         data = float(d[parameters[par]['key']]['Value'])
         histo.Fill(data)
   return histo

def main():
   ModuleList()
   for temperature in temperatures:
      for par in parameters.keys():
         FilePath = GetFilePath(par, temperature)
         if parameters[par]['json']:
            histo = CreateHistoFromJson(FilePath, par)
         elif parameters[par]['chip']:
            histo = CreateHisto(FilePath, par)
         else:
            histo = CreateHisto2(FilePath, par)
         canvas = r.TCanvas(str(parameters[par]['namedistr']+''+temperature), '', 1)
         canvas.cd()
         canvas.SetLogy()
         histo.SetXTitle(parameters[par]['xaxistitle'])
         max = histo.GetMaximum()
         r.gStyle.SetOptStat(111111)
         if parameters[par]['namedistr'] == 'Noise distribution':
            histo.RebinAxis(parameters[par]['gradC']*1.2, histo.GetXaxis())
         histo.Draw()
         Yaxis = histo.GetYaxis()
         Yaxis.SetRangeUser(0.5, 5*max)
         r.gPad.Update()
         gradB = r.TLine(parameters[par]['gradB'], 0, parameters[par]['gradB'], 10**r.gPad.GetUymax())
         gradC = r.TLine(parameters[par]['gradC'], 0, parameters[par]['gradC'], 10**r.gPad.GetUymax())
         gradB.SetLineColor(r.kOrange)
         gradC.SetLineColor(r.kRed)
         gradB.SetLineStyle(2)
         gradB.Draw()
         gradC.Draw()
         canvas.SaveAs(str(temperature+parameters[par]['namefile']))
         




main()
