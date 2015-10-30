import ROOT as r
import glob
import os
from optparse import OptionParser, make_option

import os
r.gROOT.Macro( os.path.expanduser( '/home/vtavolar/rootlogon.C' ) )

parameters = {}
parameters['NoiseROC'] = dict(file='NoiseROC', canvas = 'noiseROC', xaxistitle = 'Mean Noise [e^{-}]', gradB = 500, gradC = 1000)
parameters['Noise'] = dict(file='NoiseDistr', canvas = 'noisePixel', xaxistitle = 'Noise [e^{-}]', gradB = 50, gradC = 400)
parameters['RelativeGainWidth'] = dict(file='RelativeGainWidth', canvas = 'relgainwidth', xaxistitle = 'Relative Gain Width', gradB = 0.1, gradC = 0.2)
parameters['VcalThresholdWidth'] = dict(file='VcalThresholdWidth', canvas = 'vcalthrwidth', xaxistitle = 'Width of Vcal Threshold [e^{-}]', gradB = 200, gradC = 400)
parameters['PHCalibrationParameter1'] = dict(file='PHCalibrationParameter1', canvas = 'p1', xaxistitle = 'Parameter 1', gradB = 0, gradC = 2)
parameters['PedestalSpread'] = dict(file='PedestalSpread', canvas = 'pedspread', xaxistitle = 'Average Pedestal [e^{-}]', gradB = 2500, gradC = 5000)
#Only in case the current is measured at -20C:
parameters['Current150V'] = dict(file='Current150V', canvas = 'LeakCurr150', xaxistitle = 'I_{leak}(-150V)  [#muA]', gradB = 2, gradC = 10)
parameters['SlopeIV'] = dict(file='SlopeIV', canvas = 'slopeiv', xaxistitle = 'I_{leak}(-150V)/I_{leak}(-100)', gradB = 400, gradC = 2)


# This is for all modules:
#ProdCenters = ['CERN_all', 'PERUGIA', 'AACHEN', 'ETH']
# This is for all modules with ROC digv21resppin
#ProdCenters = ['CERN', 'ETH']
ProdCenters = ['Aachen', 'CERN', 'DESY', 'ETH', 'Perugia']
temperatures = ['m20', 'p17']

def GetFilePath(par, temperature):
   FilePath = []
   for ProdCenter in ProdCenters:
      FilePath += glob.glob(str(options.indir)+'/'+ProdCenter+'*/'+temperature+parameters[par]['file']+'.root')
   print FilePath
   return FilePath


def CreateStack(FilePath, par, temperature):
   stack = r.THStack('stack', parameters[par]['canvas'])
   listdata =[[],[],[],[],[]]
   Legend = r.TLegend(0.15,0.75,0.25,0.9)
   Legend.SetBorderSize(0)
   Legend.SetFillStyle(0)
   for i in range(len(FilePath)):
      File = r.TFile(FilePath[i])
      File.ls()
      cFile = File.Get(str(parameters[par]['canvas'])+'_'+str(temperature))
#      cFile.Print()
      List = cFile.GetListOfPrimitives()
      histo = List[1]
      Legend.AddEntry(histo.GetName(), str(FilePath[i].split('/')[1]), 'f')
#      histo.SetName(FilePath[i][8:11])
      histo.SetLineColor(i+1001)
      histo.SetFillColor(i+1001)
      stack.Add(histo)
      histo.SetStats(0)
      listdata[i].append(histo.GetEntries())
      histo.GetXaxis().SetRangeUser(histo.GetMean() - 3*histo.GetRMS(), histo.GetMean() + 3*histo.GetRMS())
      listdata[i].append(histo.GetMean())
      listdata[i].append(histo.GetRMS())      
      histo.GetXaxis().UnZoom()
   return stack, listdata, Legend



def main(options,args):
   r.gStyle.SetOptTitle(0);
   if not os.path.exists(str(options.outdir)):
      os.mkdir(str(options.outdir))
   for temperature in temperatures:
      for par in parameters.keys():  
         FilePath = GetFilePath(par, temperature)
         stack, listdata, Legend = CreateStack(FilePath, par, temperature)
         canvas = r.TCanvas(parameters[par]['canvas'], "", 1)
         canvas.cd()
         max = stack.GetMaximum()
         if options.logy:
            stack.SetMaximum(max*12)
            stack.SetMinimum(0.5)
            canvas.SetLogy(1)
         if not options.logy:
            stack.SetMaximum(max*1.2)
            stack.SetMinimum(0.5)
            canvas.SetLogy(0)
         stack.Draw()
         if par == 'Noise' or par == 'PHCalibrationParameter1':
            stack.GetYaxis().SetTitle('# Pixels')
         elif par == 'Current150V' or par == 'SlopeIV':
            stack.GetYaxis().SetTitle('# Modules')
         else:
            stack.GetYaxis().SetTitle('# ROCs')
         stack.GetXaxis().SetTitle(parameters[par]['xaxistitle'])
         canvas.Update()
#         if options.logy:
#            gradB = r.TLine(parameters[par]['gradB'], 0, parameters[par]['gradB'], stack.GetMaximum()*12.)
#            gradC = r.TLine(parameters[par]['gradC'], 0, parameters[par]['gradC'], stack.GetMaximum()*12.)
#            gradB = r.TLine(parameters[par]['gradB'], canvas.GetUymin(), parameters[par]['gradB'], canvas.GetUymax()*10)
#            gradC = r.TLine(parameters[par]['gradC'], canvas.GetUymin(), parameters[par]['gradC'], canvas.GetUymax()*10)
         if not options.logy:
#            gradB = r.TLine(parameters[par]['gradB'], 0, parameters[par]['gradB'], stack.GetMaximum()*1.2)
#            gradC = r.TLine(parameters[par]['gradC'], 0, parameters[par]['gradC'], stack.GetMaximum()*1.2)
            gradB = r.TLine(parameters[par]['gradB'], canvas.GetUymin(), parameters[par]['gradB'], canvas.GetUymax()*0.8)
            gradC = r.TLine(parameters[par]['gradC'], canvas.GetUymin(), parameters[par]['gradC'], canvas.GetUymax()*0.8)
         #r.gPad.Update()
         #Ymax = r.gPad.GetUymax()
         #gradB = r.TLine(parameters[par]['gradB'], 0, parameters[par]['gradB'], Ymax)
         #gradC = r.TLine(parameters[par]['gradC'], 0, parameters[par]['gradC'], Ymax)
         if options.logy:
            if par == 'PHCalibrationParameter1' or par =='Noise':
               gradB = r.TLine(parameters[par]['gradB'], stack.GetYaxis().GetXmin(), parameters[par]['gradB'], stack.GetMaximum())
               gradC = r.TLine(parameters[par]['gradC'], stack.GetYaxis().GetXmin(), parameters[par]['gradC'], stack.GetMaximum())
            else:
               gradB = r.TLine(parameters[par]['gradB'], stack.GetYaxis().GetXmin(), parameters[par]['gradB'], stack.GetMaximum()*4.)
               gradC = r.TLine(parameters[par]['gradC'], stack.GetYaxis().GetXmin(), parameters[par]['gradC'], stack.GetMaximum()*4.)
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
         gradeLegend = r.TLegend(0.80, 0.80, 0.95, 0.90)
         gradeLegend.SetBorderSize(0)
         gradeLegend.SetFillStyle(0)
         gradeLegend.SetTextSize(0.032)
         if par not in ['Noise', 'PHCalibrationParameter1']:
            if par != 'SlopeIV':
               gradeLegend.AddEntry(gradB, "B", "l")
            if par not in ['Noise', 'NoiseROC', 'PHCalibrationParameter1']:
               gradeLegend.AddEntry(gradC, "C", "l")
         else:
            print 'drawing box'
            bhl = r.TBox(stack.GetXaxis().GetXmin(),  stack.GetYaxis().GetXmin(), parameters[par]['gradB'], stack.GetMaximum())
            bhl.SetFillColor(2)
            bhl.SetFillStyle(3004)
            bhr = r.TBox(parameters[par]['gradC'],  stack.GetYaxis().GetXmin(), stack.GetXaxis().GetXmax(), stack.GetMaximum())
            bhr.SetFillColor(2)
            bhr.SetFillStyle(3004)
            bhl.Draw()
            bhr.Draw()
            gradeLegend.AddEntry(bhl, "defect", "f")
         gradeLegend.Draw()
         latex = r.TLatex()
         latex.SetNDC()
         latex.SetTextAlign(13)
         latex.SetTextSize(0.03)
         latex.SetTextColor(1001)
         latex.DrawLatex(0.3, 0.89, 'N: '+'{0:.0f}'.format(listdata[0][0])+'  Mean: '+'{0:.3f}'.format(listdata[0][1])+'  RMS: '+'{0:.3f}'.format(listdata[0][2]))
         latex.SetTextColor(1002)
         latex.DrawLatex(0.3, 0.86, 'N: '+'{0:.0f}'.format(listdata[1][0])+'  Mean: '+'{0:.3f}'.format(listdata[1][1])+'  RMS: '+'{0:.3f}'.format(listdata[1][2]))
         latex.SetTextColor(1003)
         latex.DrawLatex(0.3, 0.83, 'N: '+'{0:.0f}'.format(listdata[2][0])+'  Mean: '+'{0:.3f}'.format(listdata[2][1])+'  RMS: '+'{0:.3f}'.format(listdata[2][2]))
         latex.SetTextColor(1004)
         latex.DrawLatex(0.3, 0.80, 'N: '+'{0:.0f}'.format(listdata[3][0])+'  Mean: '+'{0:.3f}'.format(listdata[3][1])+'  RMS: '+'{0:.3f}'.format(listdata[3][2]))
         latex.SetTextColor(1005)
         latex.DrawLatex(0.3, 0.77, 'N: '+'{0:.0f}'.format(listdata[4][0])+'  Mean: '+'{0:.3f}'.format(listdata[4][1])+'  RMS: '+'{0:.3f}'.format(listdata[4][2]))
  #       latex.DrawLatex(0.3, 0.89, '#color[2]{N: '+'{0:.0f}'.format(listdata[0][0])+'  Mean: '+'{0:.3f}'.format(listdata[0][1])+'  RMS: '+'{0:.3f}'.format(listdata[0][2])+'}')
  #       latex.DrawLatex(0.3, 0.86, '#color[3]{N: '+'{0:.0f}'.format(listdata[1][0])+'  Mean: '+'{0:.3f}'.format(listdata[1][1])+'  RMS: '+'{0:.3f}'.format(listdata[1][2])+'}')
  #       latex.DrawLatex(0.3, 0.83, '#color[4]{N: '+'{0:.0f}'.format(listdata[2][0])+'  Mean: '+'{0:.3f}'.format(listdata[2][1])+'  RMS: '+'{0:.3f}'.format(listdata[2][2])+'}')
  #       latex.DrawLatex(0.3, 0.80, '#color[5]{N: '+'{0:.0f}'.format(listdata[3][0])+'  Mean: '+'{0:.3f}'.format(listdata[3][1])+'  RMS: '+'{0:.3f}'.format(listdata[3][2])+'}')
  #       latex.DrawLatex(0.3, 0.77, '#color[6]{N: '+'{0:.0f}'.format(listdata[4][0])+'  Mean: '+'{0:.3f}'.format(listdata[4][1])+'  RMS: '+'{0:.3f}'.format(listdata[4][2])+'}')
#         Legend = r.TLegend(0.15,0.75,0.25,0.9)
#         Legend.AddEntry(, 'CERN', 'f')
         #Legend.AddEntry('PER', 'PERUGIA', 'f')
         #Legend.AddEntry('AAC', 'AACHEN', 'f')
#         Legend.AddEntry('ETH', 'ETHZ', 'f')
#         Legend.SetBorderSize(0)
#         Legend.SetFillStyle(0)
         #Legend.AddEntry('gradB', 'Grade B threshold', 'l')
         #Legend.AddEntry('gradC', 'Grade C threshold', 'l')
         Legend.Draw()
         for fmt in ['.png', '.pdf', '.root']:
            if options.logy:
               canvas.SaveAs(str(options.outdir)+'/'+temperature+'_'+parameters[par]['file']+'_log'+str(fmt))
            if not options.logy:
               canvas.SaveAs(str(options.outdir)+'/'+temperature+'_'+parameters[par]['file']+str(fmt))


if __name__ == "__main__":
    parser = OptionParser(option_list=[
            make_option("--indir",
                        action="store", type="string", dest="indir",
                        default="HISTOS/",
                        help="", metavar=""
                        ),
            make_option("--outdir",
                        action="store", type="string", dest="outdir",
                        default="CompareProdCenters/",
                        help="", metavar=""
                        ),
            make_option("--logy",
                        action="store_true", dest="logy"
                        ),
            make_option("--nology",
                        action="store_false", dest="logy"
                        )
            ])
    (options, args) = parser.parse_args()

    
    main(options,args)
