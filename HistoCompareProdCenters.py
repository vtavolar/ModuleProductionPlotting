import ROOT as r
import glob

parameters = {}
parameters['NoiseROC'] = dict(file='NoiseROC', canvas = 'Mean Noise per ROC', xaxistitle = 'Mean Noise [e^{-}]', gradB = 500, gradC = 1000)
parameters['Noise'] = dict(file='NoiseDistr', canvas = 'Noise distribution', xaxistitle = 'Noise [e^{-}]', gradB = 50, gradC = 400)
parameters['RelativeGainWidth'] = dict(file='RelativeGainWidth', canvas = 'Relative Gain Width', xaxistitle = 'Relative Gain Width', gradB = 0.1, gradC = 0.2)
parameters['VcalThresholdWidth'] = dict(file='VcalThresholdWidth', canvas = 'Vcal Threshold Width', xaxistitle = 'Width of Vcal Threshold [e^{-}]', gradB = 200, gradC = 400)
parameters['PHCalibrationParameter1'] = dict(file='PHCalibrationParameter1', canvas = 'PH Calibration Parameter1', xaxistitle = 'Parameter 1', gradB = 0, gradC = 2)
parameters['PedestalSpread'] = dict(file='PedestalSpread', canvas = 'Pedestal Spread', xaxistitle = 'Average Pedestal [e^{-}]', gradB = 2500, gradC = 5000)
#Only in case the current is measured at -20C:
parameters['Current150V'] = dict(file='Current150V', canvas = 'Current at Voltage 150V', xaxistitle = 'Measured current at 150V [microA]', gradB = 2, gradC = 10)
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
   listdata =[[],[]]
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
      listdata[i].append(histo.GetEntries())
      listdata[i].append(histo.GetMean())
      listdata[i].append(histo.GetRMS())      
   return stack, listdata



def main():
   for temperature in temperatures:
      for par in parameters.keys():  
         FilePath = GetFilePath(par, temperature)
         stack, listdata = CreateStack(FilePath, par, temperature)
         canvas = r.TCanvas(parameters[par]['canvas'], "", 1)
         canvas.cd()
         canvas.SetLogy()
         max = stack.GetMaximum()
         stack.SetMaximum(max*12)
         stack.SetMinimum(0.5)
         stack.Draw()
         if par == 'Noise' or par == 'PHCalibrationParameter1':
            stack.GetYaxis().SetTitle('# Pixels')
         elif par == 'Current150V' or par == 'SlopeIV':
            stack.GetYaxis().SetTitle('# Modules')
         else:
            stack.GetYaxis().SetTitle('# ROCs')
         stack.GetXaxis().SetTitle(parameters[par]['xaxistitle'])
         canvas.Update()
         #r.gPad.Update()
         #Ymax = r.gPad.GetUymax()
         #gradB = r.TLine(parameters[par]['gradB'], 0, parameters[par]['gradB'], Ymax)
         #gradC = r.TLine(parameters[par]['gradC'], 0, parameters[par]['gradC'], Ymax)
         if par == 'PHCalibrationParameter1' or 'Noise':
            gradB = r.TLine(parameters[par]['gradB'], 0, parameters[par]['gradB'], stack.GetMaximum()*3)
            gradC = r.TLine(parameters[par]['gradC'], 0, parameters[par]['gradC'], stack.GetMaximum()*3)
         else:
            gradB = r.TLine(parameters[par]['gradB'], 0, parameters[par]['gradB'], stack.GetMaximum()*5)
            gradC = r.TLine(parameters[par]['gradC'], 0, parameters[par]['gradC'], stack.GetMaximum()*5)
         gradB.SetLineColor(r.kOrange)
         if par == 'Noise' or par == 'PHCalibrationParameter1':
            gradC.SetLineColor(r.kOrange)
         else:
            gradC.SetLineColor(r.kRed)
         gradB.SetLineStyle(2)
         gradC.SetLineStyle(2)
         gradB.SetLineWidth(3)
         gradC.SetLineWidth(3)
         gradB.Draw()
         gradC.Draw()
         latex = r.TLatex()
         latex.SetNDC()
         latex.SetTextAlign(13)
         latex.DrawLatex(0.3, 0.87, '#color[2]{N: '+'{:.0f}'.format(listdata[0][0])+'  Mean: '+'{:.3f}'.format(listdata[0][1])+'  RMS: '+'{:.3f}'.format(listdata[0][2])+'}')
         latex.DrawLatex(0.3, 0.82, '#color[3]{N: '+'{:.0f}'.format(listdata[1][0])+'  Mean: '+'{:.3f}'.format(listdata[1][1])+'  RMS: '+'{:.3f}'.format(listdata[1][2])+'}')
         Legend = r.TLegend(0.15,0.75,0.25,0.9)
         Legend.AddEntry('CER', 'CERN', 'f')
         #Legend.AddEntry('PER', 'PERUGIA', 'f')
         #Legend.AddEntry('AAC', 'AACHEN', 'f')
         Legend.AddEntry('ETH', 'ETHZ', 'f')
         Legend.SetBorderSize(0)
         Legend.SetFillStyle(0)
         #Legend.AddEntry('gradB', 'Grade B threshold', 'l')
         #Legend.AddEntry('gradC', 'Grade C threshold', 'l')
         Legend.Draw()
         for fmt in ['.png', '.pdf', '.root']:
            canvas.SaveAs('Results/CompareModulesRespin/'+temperature+'ProdCentersStack'+parameters[par]['file']+str(fmt))




main()
