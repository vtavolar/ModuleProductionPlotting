import ROOT as r
import glob

def main():
    stack = r.THStack('Sigma Distribution', 'SigmaDistr',)
    File1 = r.TFile('RealData_deltasigma.root')
    cFile1 = File1.Get('cplot')
    List1 = cFile1.GetListOfPrimitives()
    histo1 = List1[1]
    File2 = r.TFile('2timesData_deltasigma.root')
    cFile2 = File2.Get('cplot')
    List2 = cFile2.GetListOfPrimitives()
    histo2 = List2[1]                         
    File3 = r.TFile('4timesData_deltasigma.root')
    cFile3 = File3.Get('cplot')
    List3 = cFile3.GetListOfPrimitives()
    histo3 = List3[1]
    canvas = r.TCanvas('c1', '', 1)
    canvas.cd()
    histo1.SetStats(0)
    histo2.SetStats(0) 
    histo3.SetStats(0) 
    histo1.SetName('RealData')
    histo2.SetName('2gP')
    histo3.SetName('4gP')
    histo1.SetLineColor(2)
    histo2.SetLineColor(3)
    histo3.SetLineColor(4)
    stack.Add(histo1)
    stack.Add(histo2)
    stack.Add(histo3)
    #max = stack.GetMaximum()
    #stack.SetMaximum(max*1.2)
    stack.Draw('nostack')
    Legend = r.TLegend(0.6,0.55,0.85,0.75)
    Legend.AddEntry('RealData', 'Real p2', 'l')
    Legend.AddEntry('2gP', '2*p2', 'l')
    Legend.AddEntry('4gP', '4*p2', 'l')
    Legend.SetBorderSize(0)
    Legend.Draw()
    for fmt in ['.png', '.pdf', '.root']:
        canvas.SaveAs('stack_sigmadistr'+str(fmt))


main()
