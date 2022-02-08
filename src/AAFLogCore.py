import re, itertools
from pyquery import PyQuery as pq
# from io import StringIO

class PhaseInfo(list):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __repr__(self) -> str:
        return f'[{len(self)} phases]'
    
class HpShields(list):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __repr__(self) -> str:
        return f'[{self[-1]} at endphase]'
    
class ResultTexts(list):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __repr__(self) -> str:
        return f'[{self[0]} at the end]'

def lineparse(txt):
    splittext = re.split('<br>|\n')
    return splittext

def digest_phaseinfo(phaseinfo):
    lines = phaseinfo.html().partition('</td>')[0].strip().split('<br/>')
    lineswithoutempty = []
    for elem in lines:
        if elem.strip():
            lineswithoutempty.append(elem)
    return lineswithoutempty

def process_logtext(logtext):
    d = pq(logtext)
    
    # extract enemy name
    myName = d('div.one-half-responsive > h3 > font:first').text()
    enemyName = d('div.one-half-responsive > h3 > font:last').text()
    
    # extract level difference
    levels = d('table.tab_des03 > tbody > tr > td[style*="font-size:1.2em"]')
    myLevel = int( levels.eq(0).find('b').eq(0).text() )
    enemyLevel = int( levels.eq(1).find('b').eq(0).text() )
    levelDifference = enemyLevel - myLevel
    
    # extract result text
    resultObj = d('table.tab_des03 > tbody > tr > td[style*="padding:10px;"]')
    resultTexts = digest_phaseinfo(resultObj)[2:] # cut useless buttons
    
    # extract phase
    hpShieldObj = d('table.tab_des03 > tbody > tr > td[style*="font-size:1em; font-weight:bold;"]>font')
    phasecontents = []
    hpShields = []
    for k in itertools.count(start=1):
        if not d('#phaseinfo'+str(k)):
            phases = k-1
            break
        else:
            hpShields.append( [ int(hpShieldObj.eq(k2).text()[:-2]) for k2 in range(4*(k-1),4*k)] ) # minus 2 for trimming percent char
            phasecontents.append( digest_phaseinfo( d(f'tr#phaseinfo{k}>td') ) )
    assert(phases)
    
    # extract winlose
    if '승리' in d('div .one-half-responsive > table > tbody > tr > td > font:first').text():
        isWin = True
    else:
        isWin =False
    return {'d':d, 'myName':myName, 'enemyName':enemyName, 'levels':(myLevel,enemyLevel,levelDifference), 
            'maxphase':phases, 'isWin':isWin, 'phaseInfo': PhaseInfo(phasecontents),'hpShields':HpShields(hpShields),
            'resultTexts':ResultTexts(resultTexts)}
    
if __name__ == '__main__':
    from pathlib import Path
    from os import getcwd
    from os.path import join
    from AAFFileManager import FileManager

    parent_path = Path(getcwd())
    dirName = join(parent_path,'LogSet3')
    fm = FileManager(dirName)
    fm.gather_filenames()
    
    fileName = fm.filenames[0]
    print(fileName)
    ftext = fm.readFile(fileName)
    print(len(ftext))
    phaseContents = process_logtext(ftext)
    print(phaseContents)