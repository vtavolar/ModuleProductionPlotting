import glob

N = 8
files = glob.glob('M*/*XraySpectrum_p17/phCalibrationFitErr35_C*')
x1 = 50
x2 = 245

for file in files:
    lines = [line.strip() for line in open(file)]
    new_lines = []
    for i in range(3):
        new_lines.append(lines[i])
    for i in range(4160):
        p0 = float(lines[i+3].split()[0])
        p1 = float(lines[i+3].split()[1])
        p2 = float(lines[i+3].split()[2])
        p3 = lines[i+3].split()[3]
        new_p2 = N*p2
        new_p1 = p1+(1-N)*p2*(x1+x2)
        new_p0 = p0+(p1-new_p1)*x2+(1-N)*p2*x2**2
        pix_row = lines[i+3].split()[5]
        pix_col = lines[i+3].split()[6]
        new_lines.append('{:e}'.format(new_p0)+' '+'{:e}'.format(new_p1)+' '+'{:e}'.format(new_p2)+' '+p3+'   Pix '+pix_row+' '+pix_col)
    f = open(file[0:86]+str(N)+'New_'+file[86:], 'w+')
    for item in new_lines:
        f.write("%s\n" % item)
    f.close()


