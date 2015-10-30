import ListModules
import Histo
import HistoCompareTempStack
import HistoCompareProdCenters
import os
import subprocess


#prodCenters=['Aachen', 'CERN', 'DESY', 'ETH', 'KIT', 'Perugia']
prodCenters=['Aachen', 'CERN', 'DESY', 'KIT', 'Perugia']


def main():
    for center in prodCenters:
        #        os.system("Listodules")
        print center
#        subprocess.Popen([
#                "/usr/bin/python", 
#                "ListModules.py",
#                "--folder=DATA/"+str(center)+"/",
#                "--outfile=modules"+str(center)+".list"
#                ])
        cmd = ["/usr/bin/python", "/home/vtavolar/Documents/GradingScripts/Histo.py","--list=/home/vtavolar//Documents/GradingScripts/modules"+str(center)+".list","--outdir=/home/vtavolar//Documents/GradingScripts/HISTOS/"+str(center)+"/"]
#        cmd = ["/usr/bin/python /home/vtavolar/Documents/GradingScripts/Histo.py"]
        print cmd
        subprocess.call(cmd)
#        subprocess.Popen([
#                "/usr/bin/python",
#                "Histo.py",
#                "--list=modules"+str(center)+".list",
#                "--outdir=HISTOS/"+str(center)+"/"
#                ])
#    cmd = "/usr/bin HistoCompareProdCenters.py"
#    subprocess.call(cmd)
#    subprocess.Popen([
#            "/usr/bin/python",
#            "HistoCompareProdCenters.py"
#            ])
    
        
main()
