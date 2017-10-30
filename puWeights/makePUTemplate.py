import os
import subprocess


# New minBias xsec: https://hypernews.cern.ch/HyperNews/CMS/get/luminosity/613/2/1/1/1.html
def makeDataPUTemplate( cert, puJson, year='17' ) :
    executeArray = [
        'pileupCalc.py',
        '-i',
        '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions%s/13TeV/%s' % (year, cert),
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

    cert = 'PromptReco/Cert_294927-304507_13TeV_PromptReco_Collisions17_JSON.txt' # 24.92/fb
    year = '17'
    makeDataPUTemplate( cert, 'pileup_latest.txt', year )


