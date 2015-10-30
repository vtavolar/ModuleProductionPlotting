import ROOT as r
import glob
import os
import numpy as np
import json
from optparse import OptionParser, make_option

temperatures = ['p17', 'm20']


parameters = {}
parameters['NoiseROC'] = dict(json=False, chip=False, path='*_1/Noise/Noise.root', namedistr='noiseROC', titledistr='Mean Noise per ROC', namefile='NoiseROC', bin=100, xmin=0., xmax=600, xaxistitle = 'Mean Noise [e^{-}]', gradB = 500, gradC = 1000)
parameters['Noise'] = dict(json=False, chip = True, path = '*_1/Chips/Chip*/SCurveWidths/SCurveWidths.root', namedistr = 'noisePixel', titledistr = 'Noise per pixel', namefile = 'NoiseDistr', bin=100, xmin=0., xmax=600, xaxistitle = 'Noise [e^{-}]', gradB = 50, gradC = 400)
parameters['PHCalibrationParameter1'] = dict(json=False, chip = True, path = '*_1/Chips/Chip*/PHCalibrationParameter1/PHCalibrationParameter1.root', namedistr = 'p1', titledistr = 'PH Calibration Parameter1', namefile = 'PHCalibrationParameter1', bin=350, xmin=-1., xmax=6, xaxistitle = 'Parameter 1', gradB = 0, gradC = 2)
parameters['VcalThresholdWidth'] = dict(json=False, chip = False, path = '*_1/VcalThresholdWidth/VcalThresholdWidth.root', namedistr = 'vcalthrwidth', titledistr = 'Vcal Threshold Width', namefile = 'VcalThresholdWidth', bin=300, xmin=0., xmax=600, xaxistitle = 'Width of Vcal Threshold [e^{-}]', gradB = 200, gradC = 400)
parameters['RelativeGainWidth'] = dict(json = False, chip = False, path = '*_1/RelativeGainWidth/RelativeGainWidth.root', namedistr = 'relgainwidth', titledistr = 'Relative Gain Width', namefile = 'RelativeGainWidth', bin=120, xmin=0., xmax=0.25, xaxistitle = 'Relative Gain Width', gradB=0.1, gradC =0.2)
parameters['PedestalSpread'] = dict(json=False, chip = False, path = '*_1/PedestalSpread/PedestalSpread.root', namedistr = 'pedspread', titledistr = 'Pedestal Spread', namefile = 'PedestalSpread', bin=180, xmin=0., xmax=5500, xaxistitle = 'Average Pedestal [e^{-}]', gradB = 2500, gradC = 5000)
parameters['Current150V'] = dict(json = True, key = 'CurrentAtVoltage150V', chip = False, path = '*_1/IVCurve/KeyValueDictPairs.json', namedistr = 'LeakCurr150', titledistr = 'Leakage current at V=-150V', namefile = 'Current150V', bin=120, xmin=0, xmax=18, xaxistitle = 'Measured current at 150V [microA]', gradB = 3, gradC = 15)
parameters['SlopeIV'] = dict(json = True, key = 'Variation', chip = False, path = '*_1/IVCurve/KeyValueDictPairs.json', namedistr = 'slopeiv', titledistr = 'Slope IV', namefile = 'SlopeIV', bin=120, xmin=0, xmax=12, xaxistitle = 'Slope IV [microA]', gradB = 400, gradC = 2)
#parameters['RecalculatedCurrent150V'] = dict(json= False, key = 'CurrentAtVoltage150V', chip = False, path = '*_1/IVCurve/KeyValueDictPairs.json', namedistr = 'Recalculated Current at Voltage 150V', namefile = 'RecalculatedCurrent150V', bin=24, xmin=0, xmax=18, xaxistitle = 'Recalculated current at 150V [microA]', gradB = 3, gradC = 15)


def ModulesList():
   lines = [line.strip() for line in open(str(options.list))]
   modules=[]
   for line in lines:
      if line.startswith('#'):
         continue
      modules.append(line)
   return modules


def GetFilePath(modules, par, temperature):
   # In order to include the code in Moreweb cfr MoReWeb/Analyse/Controller.py                                                                                                      
   FilePath = []
   for module in modules:
      print module
      FilePath += glob.glob(module+'/FinalResults-*/QualificationGroup/ModuleFulltest*'+temperature+parameters[par]['path'])
#      FilePath += glob.glob(module.split('/',1)[0]+'/REV001/R001/'+module.split('/',1)[1]+'/QualificationGroup/ModuleFulltest*'+temperature+parameters[par]['path'])
      print FilePath

   return FilePath


def CreateHisto(FilePath, par):
   histo = r.TH1D(parameters[par]['namedistr'], parameters[par]['titledistr'], parameters[par]['bin'], parameters[par]['xmin'], parameters[par]['xmax'])
   for i in range(len(FilePath)):
      File = r.TFile(FilePath[i])
      cNoise = File.Get('c1')
      List = cNoise.GetListOfPrimitives()
      histochip = List[1]
      histo.Add(histochip)
   return histo


def CreateHisto2(FilePath, par):
   histo = r.TH1D(parameters[par]['namedistr'], parameters[par]['titledistr'], parameters[par]['bin'], parameters[par]['xmin'], parameters[par]['xmax'])
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
   histo = r.TH1D(parameters[par]['namedistr'], parameters[par]['titledistr'], parameters[par]['bin'], parameters[par]['xmin'], parameters[par]['xmax'])
   for i in range(len(FilePath)):
      with open(FilePath[i]) as json_data:
         d = json.load(json_data)
         data = float(d[parameters[par]['key']]['Value'])
         histo.Fill(data)
   return histo


def CreateHistoFromJsonForRecalculatedCurrent(FilePath, par):
   histo = r.TH1D(parameters[par]['namedistr'], parameters[par]['titledistr'], parameters[par]['bin'], parameters[par]['xmin'], parameters[par]['xmax'])
   for i in range(len(FilePath)):
      with open(FilePath[i]) as json_data:
         d = json.load(json_data)
         data = float(d[parameters[par]['key']]['Value'])
         print data
         dataRecalculated = data*(290.15/253.15)**2*np.exp((1.12/(2*8.62e-5))*(253.15**-1-290.15**-1))
         histo.Fill(dataRecalculated)
         print dataRecalculated
   return histo




def main(options,args):
   modules = ModulesList()
   if not os.path.exists(str(options.outdir)):
      os.mkdir(str(options.outdir))
   for temperature in temperatures:
      for par in parameters.keys():
         FilePath = GetFilePath(modules, par, temperature)
         if parameters[par]['json']:
            histo = CreateHistoFromJson(FilePath, par)
         elif par == 'RecalculatedCurrent150V':
            if temperature == 'p17':
               continue
            else:
               histo = CreateHistoFromJsonForRecalculatedCurrent(FilePath, par)
         elif parameters[par]['chip']:
            histo = CreateHisto(FilePath, par)
         else:
            histo = CreateHisto2(FilePath, par)
         canvas = r.TCanvas(str(parameters[par]['namedistr']+'_'+temperature), '', 1)
         canvas.cd()
         canvas.SetLogy()
         histo.SetXTitle(parameters[par]['xaxistitle'])         
         max = histo.GetMaximum()
         r.gStyle.SetOptStat(111111)
         if parameters[par]['namedistr'] == 'noisePixel':
            histo.RebinAxis(parameters[par]['gradC']*1.2, histo.GetXaxis())
         histo.Draw()
         histo.GetYaxis().SetRangeUser(0.5, 5*max)
         if par == 'Noise' or par == 'PHCalibrationParameter1':
            histo.GetYaxis().SetTitle('# Pixels')
         elif par == 'Current150V' or par == 'SlopeIV':
            histo.GetYaxis().SetTitle('# Modules')
         else:
            histo.GetYaxis().SetTitle('# ROCs')
         r.gPad.Update()
         gradB = r.TLine(parameters[par]['gradB'], 0, parameters[par]['gradB'], 10**r.gPad.GetUymax())
         gradC = r.TLine(parameters[par]['gradC'], 0, parameters[par]['gradC'], 10**r.gPad.GetUymax())
         gradB.SetLineColor(r.kOrange)
         if par == 'Noise' or par == 'PHCalibrationParameter1':
            gradC.SetLineColor(r.kOrange)
         else:
            gradC.SetLineColor(r.kRed)
         gradB.SetLineStyle(2)
         gradC.SetLineStyle(2)
         gradB.Draw()
         gradC.Draw()
         for fmt in ['.png', '.pdf', '.root']:
            canvas.SaveAs(str(options.outdir)+'/'+str(temperature+parameters[par]['namefile'])+str(fmt))


if __name__ == "__main__":
    parser = OptionParser(option_list=[
            make_option("--list",
                        action="store", type="string", dest="list",
                        default="modules.list",
                        help="", metavar=""
                        ),
            make_option("--outdir",
                        action="store", type="string", dest="outdir",
                        default="HISTOS",
                        help="", metavar=""
                        )
            ])
    (options, args) = parser.parse_args()

    
    main(options,args)
