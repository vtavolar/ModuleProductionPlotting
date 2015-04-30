import ROOT as r
import glob

parameters = {}
parameters['Noise'] = dict(file='NoiseDistr.root', canvas = 'Noise distribution', xaxistitle = 'Noise [e^{-}]', gradB = 500, gradC = 1000)
parameters['RelativeGainWidth'] = dict(file='RelativeGainWidth.root', canvas = 'Relative Gain Width', xaxistitle = 'Relative Gain Width', gradB = 0.1, gradC = 0.2)
parameters['VcalThresholdWidth'] = dict(file='VcalThresholdWidth.root', canvas = 'Vcal Threshold Width', xaxistitle = 'Width of Vcal Threshold [e^{-}]', gradB = 200, gradC = 400)
parameters['PHCalibrationParameter1'] = dict(file='PHCalibrationParameter1.root', canvas = 'PH Calibration Parameter1', xaxistitle = 'Parameter 1', gradB = 4, gradC = 5)
parameters['PedestalSpread'] = dict(file='PedestalSpread.root', canvas = 'Pedestal Spread', xaxistitle = 'Average Pedestal [e^{-}]', gradB = 2500, gradC = 5000)
#Only in case the current is measured at -20C:
parameters['Current150V'] = dict(file='Current150V.root', canvas = 'Current at Voltage 150V', xaxistitle = 'Recalculated current at 150V [microA]', gradB = 3, gradC = 15)
parameters['SlopeIV'] = dict(file='SlopeIV.root', canvas = 'Slope IV', xaxistitle = 'Slope IV [microA]', gradB = 400, gradC = 2)

def main():
   r.gStyle.SetPaintTextFormat("3.2f")
   for par in parameters.keys():
      #FilePathm20 = GetFilePath('m20')
      #FilePathp17 = GetFilePath('p17')
      Filem20 = r.TFile('m20'+parameters[par]['file'])
      cFilem20 = Filem20.Get(parameters[par]['canvas']+'m20')
      Listm20 = cFilem20.GetListOfPrimitives()
      histom20 = Listm20[1]
      Filep17 = r.TFile('p17'+parameters[par]['file'])
      cFilep17 = Filep17.Get(parameters[par]['canvas']+'p17')
      Listp17 = cFilep17.GetListOfPrimitives()
      histop17 = Listp17[1]
      histom20.SetName('m20')
      histop17.SetName('p17')
      canvas = r.TCanvas(parameters[par]['canvas'], "", 1)
      canvas.cd()
      canvas.SetLogy()
      histom20.SetLineColor(2)
      histop17.SetLineColor(3)
      m20max= histom20.GetMaximum()
      p17max= histop17.GetMaximum()
      histom20.Draw()
      histop17.Draw('SAME')
      m20Yaxis = histom20.GetYaxis()
      p17Yaxis = histop17.GetYaxis()
      if m20max>p17max:
         m20Yaxis.SetRangeUser(0.5, 1.2*m20max)
         p17Yaxis.SetRangeUser(0.5, 1.2*m20max)
      else:
         m20Yaxis.SetRangeUser(0.5, 1.2*p17max)
         p17Yaxis.SetRangeUser(0.5, 1.2*p17max)
      histom20.SetStats(0)
      histop17.SetStats(0)
      histom20.SetXTitle(parameters[par]['xaxistitle'])
      latex = r.TLatex()
      latex.SetNDC()
      latex.SetTextAlign(13)
      latex.DrawLatex(0.4, 0.85, '#color[2]{N: '+str(histom20.GetEntries())+'  Mean: '+str(histom20.GetMean())+'  RMS: '+str(histom20.GetRMS())+'}')
      latex.DrawLatex(0.4, 0.75, '#color[3]{N: '+str(histop17.GetEntries())+'  Mean: '+str(histop17.GetMean())+'  RMS: '+str(histop17.GetRMS())+'}')
      gradB = r.TLine(parameters[par]['gradB'], 0, parameters[par]['gradB'], 10**r.gPad.GetUymax())
      gradC = r.TLine(parameters[par]['gradC'], 0, parameters[par]['gradC'], 10**r.gPad.GetUymax())
      gradB.SetLineColor(r.kOrange)
      gradC.SetLineColor(r.kRed)
      gradB.SetLineStyle(2)
      gradB.Draw()
      gradC.Draw()
      Legend = r.TLegend(0.6,0.3,0.85,0.5)
      Legend.AddEntry('p17', 'Fulltest at 17 C', 'l')
      Legend.AddEntry('m20', 'Fulltest at -20 C', 'l')
      Legend.SetBorderSize(0)
      #Legend.AddEntry('gradB', 'Grade B threshold', 'l')
      #Legend.AddEntry('gradC', 'Grade C threshold', 'l')
      Legend.Draw()
      canvas.SaveAs(parameters[par]['file'])




main()
