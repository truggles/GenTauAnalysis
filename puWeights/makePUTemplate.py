import os
import subprocess


# New minBias xsec: https://hypernews.cern.ch/HyperNews/CMS/get/luminosity/613/2/1/1/1.html
def makeDataPUTemplate( cert, puJson, year='17' ) :
    executeArray = [
        'pileupCalc.py',
        '-i',
        #'/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions%s/13TeV/%s' % (year, cert),
        cert,
        '--inputLumiJSON',
        '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions%s/13TeV/PileUp/%s' % (year, puJson),
        '--calcMode',
        'true',
        '--minBiasXsec',
        '69200',
        '--maxPileupBin',
        '80',
        '--numPileupBins',
        '800',
        'DataTemplate.root']
    subprocess.call( executeArray )



if __name__ == '__main__' :

    #base = ''
    #cert = base+'data/Cert_294927-304797_RunB-E_13TeV_PromptReco_Collisions17_JSON.txt' # All Run B - E
    base = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/'
    cert = base+'Cert_294927-306126_13TeV_PromptReco_Collisions17_JSON.txt' # 38.72/fb
    year = '17'
    makeDataPUTemplate( cert, 'pileup_latest.txt', year )


