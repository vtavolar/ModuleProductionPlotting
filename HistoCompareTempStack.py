import ROOT as r
import glob

parameters = {}
parameters['Noise'] = dict(file='NoiseDistr', canvas = 'Noise distribution', xaxistitle = 'Noise [e^{-}]', gradB = 500, gradC = 1000)
parameters['RelativeGainWidth'] = dict(file='RelativeGainWidth', canvas = 'Relative Gain Width', xaxistitle = 'Relative Gain Width', gradB = 0.1, gradC = 0.2)
parameters['VcalThresholdWidth'] = dict(file='VcalThresholdWidth', canvas = 'Vcal Threshold Width', xaxistitle = 'Width of Vcal Threshold [e^{-}]', gradB = 200, gradC = 400)
parameters['PHCalibrationParameter1'] = dict(file='PHCalibrationParameter1', canvas = 'PH Calibration Parameter1', xaxistitle = 'Parameter 1', gradB = 4, gradC = 5)
parameters['PedestalSpread'] = dict(file='PedestalSpread', canvas = 'Pedestal Spread', xaxistitle = 'Average Pedestal [e^{-}]', gradB = 2500, gradC = 5000)
#Only in case the current is measured at -20C:
parameters['Current150V'] = dict(file='Current150V', canvas = 'Current at Voltage 150V', xaxistitle = 'Recalculated current at 150V [microA]', gradB = 3, gradC = 15)
parameters['SlopeIV'] = dict(file='SlopeIV', canvas = 'Slope IV', xaxistitle = 'Slope IV [microA]', gradB = 400, gradC = 2)



def main():
   for par in parameters.keys():
      #FilePathm20 = GetFilePath('m20')
      #FilePathp17 = GetFilePath('p17')
      Filem20 = r.TFile('m20'+parameters[par]['file']+'.root')
      cFilem20 = Filem20.Get(parameters[par]['canvas']+'m20')
      Listm20 = cFilem20.GetListOfPrimitives()
      histom20 = Listm20[1]
      Filep17 = r.TFile('p17'+parameters[par]['file']+'.root')
      cFilep17 = Filep17.Get(parameters[par]['canvas']+'p17')
      Listp17 = cFilep17.GetListOfPrimitives()
      histop17 = Listp17[1]
      histom20.SetName('m20')
      histop17.SetName('p17')
      canvas = r.TCanvas(parameters[par]['canvas'], "", 1)
      canvas.cd()
      canvas.SetLogy()
      stack = r.THStack('stack', parameters[par]['canvas'])
      histom20.SetLineColor(2)
      histop17.SetLineColor(3)
      histom20.SetFillColor(2)
      histop17.SetFillColor(3)
      stack.Add(histom20)
      stack.Add(histop17)
      histom20.SetStats(0)
      histop17.SetStats(0)
      histom20.SetXTitle(parameters[par]['xaxistitle'])
      max = stack.GetMaximum()
      stack.SetMaximum(max*10)
      stack.SetMinimum(0.5)
      stack.Draw()
      gradB = r.TLine(parameters[par]['gradB'], 0, parameters[par]['gradB'], max)
      gradC = r.TLine(parameters[par]['gradC'], 0, parameters[par]['gradC'], max)
      gradB.SetLineColor(r.kOrange)
      gradC.SetLineColor(r.kBlue)
      gradB.SetLineStyle(2)
      gradB.SetLineWidth(3)
      gradC.SetLineWidth(3)
      gradB.Draw()
      gradC.Draw()
      latex = r.TLatex()
      latex.SetNDC()
      latex.SetTextAlign(13)
      latex.DrawLatex(0.2, 0.87, '#color[2]{N: '+'{:.0f}'.format(histom20.GetEntries())+'  Mean: '+'{:.3f}'.format(histom20.GetMean())+'  RMS: '+'{:.3f}'.format(histom20.GetRMS())+'}')
      latex.DrawLatex(0.2, 0.82, '#color[3]{N: '+'{:.0f}'.format(histop17.GetEntries())+'  Mean: '+'{:.3f}'.format(histop17.GetMean())+'  RMS: '+'{:.3f}'.format(histop17.GetRMS())+'}')
      Legend = r.TLegend(0.5,0.55,0.75,0.75)
      Legend.AddEntry('p17', 'Fulltest at 17 C', 'f')
      Legend.AddEntry('m20', 'Fulltest at -20 C', 'f')
      Legend.SetBorderSize(0)
      #Legend.AddEntry('gradB', 'Grade B threshold', 'l')
      #Legend.AddEntry('gradC', 'Grade C threshold', 'l')
      Legend.Draw()
      canvas.SaveAs(parameters[par]['file']+'.root')




main()
