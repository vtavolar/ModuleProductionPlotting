import ROOT as r
import glob

parameters = {}
parameters['Noise'] = dict(file='NoiseDistr', canvas = 'Noise distribution', xaxistitle = 'Noise [e^{-}]', gradB = 500, gradC = 1000)
parameters['RelativeGainWidth'] = dict(file='RelativeGainWidth', canvas = 'Relative Gain Width', xaxistitle = 'Relative Gain Width', gradB = 0.1, gradC = 0.2)
parameters['VcalThresholdWidth'] = dict(file='VcalThresholdWidth', canvas = 'Vcal Threshold Width', xaxistitle = 'Width of Vcal Threshold [e^{-}]', gradB = 200, gradC = 400)
parameters['PHCalibrationParameter1'] = dict(file='PHCalibrationParameter1', canvas = 'PH Calibration Parameter1', xaxistitle = 'Parameter 1', gradB = 4, gradC = 5)
parameters['PedestalSpread'] = dict(file='PedestalSpread', canvas = 'Pedestal Spread', xaxistitle = 'Average Pedestal [e^{-}]', gradB = 2500, gradC = 5000)
#Only in case the current is measured at -20C:
parameters['Current150V'] = dict(file='Current150V', canvas = 'Current at Voltage 150V', xaxistitle = 'Measured current at 150V [microA]', gradB = 3, gradC = 15)
parameters['SlopeIV'] = dict(file='SlopeIV', canvas = 'Slope IV', xaxistitle = 'Slope IV [microA]', gradB = 400, gradC = 2)


# This is for all modules:
#ProdCenters = ['CERN_all', 'PERUGIA', 'AACHEN', 'ETH']
# This is for all modules with ROC digv21resppin
ProdCenters = ['CERN_respin', 'ETH']
temperatures = ['m20', 'p17']

def GetFilePath(par, temperature):
   FilePath = []
   for ProdCenter in ProdCenters:
      FilePath += glob.glob('Results/'+ProdCenter+'*/'+temperature+parameters[par]['file']+'.root')
   return FilePath


def CreateStack(FilePath, par, temperature):
   stack = r.THStack('stack', parameters[par]['canvas'])
   for i in range(len(FilePath)):
      File = r.TFile(FilePath[i])
      cFile = File.Get(parameters[par]['canvas']+temperature)
      List = cFile.GetListOfPrimitives()
      histo = List[1]
      histo.SetName(FilePath[i][8:11])
      histo.SetLineColor(i+2)
      histo.SetFillColor(i+2)
      stack.Add(histo)
      histo.SetStats(0)
      histo.SetXTitle(parameters[par]['xaxistitle'])
   return stack


def main():
   for temperature in temperatures:
      for par in parameters.keys():  
         FilePath = GetFilePath(par, temperature)
         stack = CreateStack(FilePath, par, temperature)
         canvas = r.TCanvas(parameters[par]['canvas'], "", 1)
         canvas.cd()
         canvas.SetLogy()
         max = stack.GetMaximum()
         stack.SetMaximum(max*10)
         stack.SetMinimum(0.5)
         stack.Draw()
         gradB = r.TLine(parameters[par]['gradB'], 0, parameters[par]['gradB'], max)
         gradC = r.TLine(parameters[par]['gradC'], 0, parameters[par]['gradC'], max)
         gradB.SetLineColor(r.kOrange)
         gradC.SetLineColor(r.kBlack)
         gradB.SetLineStyle(2)
         gradB.SetLineWidth(3)
         gradC.SetLineWidth(3)
         gradB.Draw()
         gradC.Draw()
         #latex = r.TLatex()
         #latex.SetNDC()
         #latex.SetTextAlign(13)
         #latex.DrawLatex(0.2, 0.87, '#color[2]{N: '+'{:.0f}'.format(histom20.GetEntries())+'  Mean: '+'{:.3f}'.format(histom20.GetMean())+'  RMS: '+'{:.3f}'.format(histom20.GetRMS())+'}')
         #latex.DrawLatex(0.2, 0.82, '#color[3]{N: '+'{:.0f}'.format(histop17.GetEntries())+'  Mean: '+'{:.3f}'.format(histop17.GetMean())+'  RMS: '+'{:.3f}'.format(histop17.GetRMS())+'}')
         Legend = r.TLegend(0.5,0.55,0.75,0.75)
         Legend.AddEntry('CER', 'CERN', 'f')
         #Legend.AddEntry('PER', 'PERUGIA', 'f')
         #Legend.AddEntry('AAC', 'AACHEN', 'f')
         Legend.AddEntry('ETH', 'ETHZ', 'f')
         Legend.SetBorderSize(0)
         #Legend.AddEntry('gradB', 'Grade B threshold', 'l')
         #Legend.AddEntry('gradC', 'Grade C threshold', 'l')
         Legend.Draw()
         for fmt in ['.png', '.pdf', '.root']:
            canvas.SaveAs(temperature+'ProdCentersStack'+parameters[par]['file']+str(fmt))




main()
