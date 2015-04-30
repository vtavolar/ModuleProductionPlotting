import glob

ModulesList = glob.glob('*_FullQualification*')
f = open('modules.list', 'w+')
for item in ModulesList:
    f.write("%s\n" % item)
f.close()
