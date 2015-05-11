from ROOT import *
import glob


files = glob.glob('LUT/M*_R*/*_XraySpectrum_p17/commander_XraySpectrum.root')



def FitHistoSpectrum(histo, xmin, xmax):
    name = "fit_{0}".format(histo.GetName())
    gausfit = FitGaus(histo)
    gaus0 = gausfit.GetParameter(0)
    gaus1 = gausfit.GetParameter(1)
    gaus2 = gausfit.GetParameter(2)
    print 'Found Start parameter: ', gaus0, gaus1, gaus2
    
    myfit = TF1(name, "([0]+[1]*x+gaus(2)+gaus(5))*(1+TMath::Erf((x-[8])/[9]))/2", xmin, xmax)
    
    # Find the overall average in the y-direction to define some good starting parameters
    y_avg = histo.Integral() / histo.GetNbinsX()

    maxbin = gaus1
    maximum = gaus0
    signalSigma = gaus2

    # Find the overall mean
    mean = histo.GetMean()

    #Hard coded limit on the slope of the linear part
    param1limit = 0.5

    #Hard coded guess at the noise spread
    noiseSigma = 30

    #Hard coded trimvalue for the Erf turn on
    trimvalue = 40

    #Initial guess of constant part is half of the overall y-average
    myfit.SetParameter(0, y_avg / 2)
    print 'SetParameter0: ', myfit.GetParameter(0)

    # Limit on the constant part; it should be positive, and below the y-average
    # because the y-average is biased above the noise by the signal peak
    myfit.SetParLimits(0, 0, 2 * y_avg)
    print 'SetParameterLimits0: ', 0, 2 * y_avg

    #Initial guess of the linear part is flat
    myfit.SetParameter(1, 0)
    print 'SetParameter1: ', myfit.GetParameter(1)

    #Limits on the linear part, from the hardcoded value above
    myfit.SetParLimits(1, -4 * param1limit, 4 * param1limit)
    print 'SetParameterLimits1: ', -4 * param1limit, 4 * param1limit

    #Initial guess for the size of the signal is the maximum of the histogram
    myfit.SetParameter(2, maximum)
    print 'SetParameter2: ', myfit.GetParameter(2)
    myfit.SetParLimits(2, 0.5 * maximum, 2 * maximum)
    print 'SetParameterLimits2: ', 0.5 * maximum, 2 * maximum

    #Initial guess for the center of the signal to be where the maximum bin is located
    myfit.SetParameter(3, maxbin)
    print 'SetParameter3: ', myfit.GetParameter(3)

    low = maxbin - 2 * signalSigma

    #if low < trimvalue:
    #    low = trimvalue/2
    myfit.SetParLimits(3, low, maxbin + 2 * signalSigma)
    print 'SetParameterLimits3: ', maxbin + 2 * signalSigma
    
    #Initial guess for the sigma of the signal, from the hardcoded value above
    myfit.SetParameter(4, signalSigma)
    print 'SetParameter4: ', myfit.GetParameter(4)
    
    myfit.SetParLimits(4, signalSigma - 10, signalSigma + 10)
    print 'SetParameterLimits4: ', signalSigma - 10, signalSigma + 10

    #Initial guess for the size of the guassian noise to be half of the overall y-average (other half is the constant term)
    myfit.SetParameter(5, y_avg * 10)

    print 'SetParameter5: ', myfit.GetParameter(5)
    # Limits on the amount of gaussian noise, should be below y-average
    # but above 0 for the same reasons as listed for Par0
    myfit.SetParLimits(5, 0, y_avg * 20)
    print 'SetParameterLimits4: ', 0, y_avg * 20

    #Initial guess for gaussian noise at the mean of the histogram
    myfit.SetParameter(6, mean)
    #Limits on the location of the noise to be somewhere in the fit region
    myfit.SetParLimits(6, xmin, xmax)

    #Initial guess for the noise sigma, hardcoded above
    myfit.SetParameter(7, noiseSigma)
    #Limits on noise sigma, used to make sure the noise guassian doesn't accidentally try to fit the signal
    myfit.SetParLimits(7, noiseSigma, 10 * noiseSigma)

    #Initial guess for the turn on is at the hardcorded trimvalue
    myfit.SetParameter(8, trimvalue)
    #Limits on where the turn on occurs are guessed at +-10 away from the given trim value
    #goes to very low values, but doesn't seem to affect the fit too much. Maybe a lower bound can be set to e-5
    myfit.SetParLimits(8, 0, trimvalue + 30)

    #Initial guess for the turn on speed is set to 5
    myfit.SetParameter(9, 5)
    #Limit on turn on speed between 0.1 and 10. This value should be positive and shouldn't be much more below 0.1 otherwise it will affect the rest of the fit
    myfit.SetParLimits(9, 0.01, 20)

    histo.Fit(myfit, 'QS')
    backgroundFit = TF1(name, "([0]+[1]*x+gaus(2))*(1+TMath::Erf((x-[5])/[6]))/2", xmin, xmax)
    backgroundFit.FixParameter(0, myfit.GetParameter(0))
    backgroundFit.FixParameter(1, myfit.GetParameter(1))
    backgroundFit.FixParameter(2, myfit.GetParameter(5))
    backgroundFit.FixParameter(3, myfit.GetParameter(6))
    backgroundFit.FixParameter(4, myfit.GetParameter(7))
    backgroundFit.FixParameter(5, myfit.GetParameter(8))
    backgroundFit.FixParameter(6, myfit.GetParameter(9))
    backgroundFit.SetLineColor(ROOT.kRed)
    backgroundFit.SetLineStyle(2)
    histo.Fit(backgroundFit, "+Q")
    
#    for i in range(10):
#        a = ROOT.Double(0)
#        b = ROOT.Double(0)
#        myfit.GetParLimits(i, a, b)
#        print i, '%8.2f [%6.2f,%6.2f]' % (myfit.GetParameter(i), a, b)

    #if 'TargetEnergy' in self.Attributes:
    #    targetEnergy = self.Attributes['TargetEnergy']
    #else:
    #    targetEnergy = 0
    #if self.Attributes.has_key('TargetNElectrons'):
    #    targetNElectrons = self.Attributes['TargetNElectrons']
    #else:
    #    targetNElectrons = 0
    #if 'Target' in self.Attributes:
    #    target = self.Attributes['Target']
    #else:
    #    target = 'unknown'
    #chi2_per_ndf = myfit.GetChisquare() / max(myfit.GetNDF(), 1)
    #self.ResultData['KeyValueDictPairs'].update(
    #    {
    #        'Center': {
    #            'Value': round(myfit.GetParameter(3), 2),
    #            'Label': 'Center of Peak',
    #            'Unit': 'Vcal',
    #            'Sigma': round(myfit.GetParError(3), 2),
    #        },
    #        'TargetEnergy': {
    #            'Value': round(targetEnergy, 2),
    #            'Label': 'Energy of target %s' % target,
    #            'Unit': 'eV',
    #        },
    #        'TargetNElectrons': {
    #            'Value': round(targetNElectrons, 2),
    #            'Label': 'Energy of target %s' % target,
    #            'Unit': 'nElectrons',
    #        },
    #        'Chi2PerNDF': {
    #            'Value': round(chi2_per_ndf, 2),
    #            'Label': 'Chi^2 per NDF',
    #            'Unit': ''
    #        },
    #        'Target': {
    #            'Value': target,
    #            'Label': 'Target',
    #            'Unit': ''
    #        }
    #    }
    #)
    #self.ResultData['KeyList'].extend(['Target','Center', 'TargetEnergy', 'TargetNElectrons', 'Chi2PerNDF'])
    #if self.verbose: print self.ResultData
    #if self.verbose: print self.ResultData['KeyValueDictPairs']
    #
    #if self.verbose:
    #    print 'fitted parameters of SCurve fit:'
    #    for i in range(10):
    #        a = ROOT.Double(0)
    #        b = ROOT.Double(0)
    #        myfit.GetParLimits(i, a, b)
    #        print 'Par %2d:\t' % i, '%8.2f [%6.2f,%6.2f]' % (myfit.GetParameter(i), a, b)
    return myfit
    
    # '''
    # * Function that attempts to fit a simple gaussian to a spectra
    #    *
    #    * Used to find initial guess for signal in other fits
    #'''
def FitGaus(histo):
    xpeak = histo.GetBinLowEdge(histo.GetMaximumBin())
    xmin = xpeak*0.85
    xmax = xpeak*1.15
    fit = TF1("gausFit", "gaus(0)", xmin, xmax)

    fit.SetParameter(1, xpeak)
    fit.SetParLimits(1, xmin, xmax)
    fit.SetParameter(2, (xmax-xmin)/2.)
    #Make sure we actually fit a 'signal like' peak, nothing too broad or narrow
    fit.SetParLimits(2, (xmax-xmin)/4., (xmax-xmin))

    histo.Fit(fit, 'QSR')
    return fit


def main():
    h_deltasigma = TH1D('h_deltasigma', 'h_deltasigma', 240, 0, 50) 
    cplot = TCanvas('cplot', '', 1)
    for file in files:
        pol2_file = TFile(file, 'READ')
        for chip in range(16):
            hpol2 = pol2_file.Get('Xray/q_Ag_C'+str(chip)+'_V0')
            pol2max = hpol2.GetBinLowEdge(hpol2.GetMaximumBin())
            #fitrange=15.
            #gauspol2 = TF1('gauspol2', 'gaus',pol2max-fitrange, pol2max+fitrange)
            cplot.cd()
            #hpol2.Fit(gauspol2, 'RS')
            fitResPol2 = FitGaus(hpol2)
            hpol2.Draw()
            #for fmt in ['.png', '.pdf', '.root']:
                #cplot.SaveAs(str(hpol2.GetName())+'_pol2'+str(fmt))
            sigmapol2 = fitResPol2.GetParameter(2)
            h_deltasigma.Fill(sigmapol2)
    ROOT.gStyle.SetOptStat(111111)
    h_deltasigma.Draw()
    for fmt in ['.png', '.pdf', '.root']:
        cplot.SaveAs('RealData_deltasigma'+str(fmt))
    
main()
