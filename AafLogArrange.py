# from bs4 import BeautifulSoup
from operator import index
from os import walk
from tkinter.font import families
from pyquery import PyQuery as pq
import itertools
from collections import Counter
import matplotlib.pyplot as plt
import re


# predefined values
dataDir = 'Logset2'

# scan files
fileList = []
for _,_,filenames in walk(dataDir):
    fileList.extend(filenames)
    break
nLogs = len(filenames)
print(nLogs)

# parse files
levelDifference = []
phases = []
winLose = []
enemyName = []
foresees = []
for filename in fileList:
    with open(dataDir+'/'+filename,encoding='utf8') as f:
        fstr = f.read()
        d = pq(fstr)
        # extract enemy name
        enemyName.append( d('div .one-half-responsive > h3 > font:last').text() )
        
        # extract level difference
        levels = d('table.tab_des03 > tbody > tr > td[style*="font-size:1.2em"]')
        myLevel = int( levels.eq(0).find('b').eq(0).text() )
        enemyLevel = int( levels.eq(1).find('b').eq(0).text() )
        levelDifference.append(enemyLevel - myLevel)
        
        # extract phase
        for k in itertools.count(start=1):
            if not d('#phaseinfo'+str(k)):
                phases.append(k-1)
                break
        
        # extract winlose
        if '승리' in d('div .one-half-responsive > table > tbody > tr > td > font:first').text():
            winLose.append(True)
        else:
            winLose.append(False)
            
        # extract foresee
        foresees.append( len(re.findall('당신은 적의 움직임을 <b>예지</b>', fstr)))
        

#print(Counter(enemyName))
#print(foresees)

# calculate winning rate
maxPhase = max(phases)
winPhases = []
losePhases = []
for k, isWin in enumerate(winLose):
    if isWin: winPhases.append(phases[k])
    else: losePhases.append(phases[k])
nWin = len(winPhases)
nLose = len(losePhases)
nTotal = len(phases)
winRate = 100 * nWin / nTotal # float in python 3

# gather data by enemyName
fullList = []
for k in range(nLogs):
    fullList.append( [k, enemyName[k], phases[k], winLose[k], levelDifference[k],foresees[k]] )
    
def ArrangeByName(acc,cur): # accumulator and current item
    name = cur[1] # enemyName
    if name not in acc:
        acc[name] = []
    acc[name].append( cur[2:] )
    return acc

from functools import reduce
arrangedByName = reduce(ArrangeByName,fullList,{}) # {} is initial value for accumulator

def Avg(numList): return sum(numList)/len(numList)
def WinningRate(boolList): return Avg( list(map(int,boolList)) ) # map for bool to int
def ExtractPhase(fullList): return list(map(lambda x: x[0],fullList))
def ExtractWinLose(fullList): return list(map(lambda x: x[1], fullList))
def ExtractLevelDifference(fullList): return list(map(lambda x: x[2], fullList))
def ExtractForesees(fullList): return list(map(lambda x: x[3], fullList))
def MultiplyBy(numList,multiplier): return list(map(lambda x: x*multiplier,numList))
def GroupDataByEnemyName(arrangedByName):
    enemyNames = arrangedByName.keys()
    counts = []
    avgPhases = []
    winRates = []
    avgForesees = []
    avgLevelDifferences = []
    for enemyName in enemyNames:
        enemyLogs = arrangedByName[enemyName]
        counts.append( len(enemyLogs) )
        avgPhases.append( Avg( ExtractPhase(enemyLogs) ) )
        winRates.append( WinningRate( ExtractWinLose(enemyLogs) ) )
        avgLevelDifferences.append( Avg( ExtractLevelDifference(enemyLogs) ) )
        avgForesees.append( Avg( ExtractForesees(enemyLogs)))
    return (enemyNames,counts,avgPhases,winRates,avgLevelDifferences,avgForesees)

enemyNames, countsByEnemyName, avgPhasesByEnemyName, \
    winRatesByEnemyName, avgLevelDifferenceByEnemyName, avgForeseesByEnemyName \
        = GroupDataByEnemyName(arrangedByName)
avgForeseesRateByEnemyName \
    = [100 * avgForeseesByEnemyName[k]/avgPhasesByEnemyName[k] for k in range(len(enemyNames))]
        
# import font for 한글
from matplotlib import font_manager,rc
font_path = 'D2Coding-Ver1.3.2-20180524-all.ttc'
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font',family=font)

plt.figure(1)
plt.hist( (winPhases,losePhases),bins=range(maxPhase+1), 
         histtype='barstacked', label=('승','패'))
plt.title(f'{nTotal}전 {nWin}승 {nLose}패, 승률:{winRate}%')
plt.xlabel('종료 페이즈')
plt.ylabel('전투 수')
plt.legend( )

plt.figure(2)
plt.scatter(avgPhasesByEnemyName,countsByEnemyName,s=MultiplyBy(winRatesByEnemyName,500),c=winRatesByEnemyName,cmap='Spectral')
plt.xlabel('평균 페이즈')
plt.ylabel('전투 수') #size = 승률
for k, name in enumerate(enemyNames):
    plt.annotate(f'{name},{winRatesByEnemyName[k]*100:.2f}%승', (avgPhasesByEnemyName[k]+0.2,countsByEnemyName[k]+0.12),
                 rotation=30, fontsize=8 )

plt.figure(3)
plt.scatter(avgLevelDifferenceByEnemyName,avgPhasesByEnemyName,
            s=MultiplyBy(winRatesByEnemyName,500),c=winRatesByEnemyName,cmap='Spectral')
plt.xlabel('평균 레벨차') #size = 승률
plt.ylabel('평균 페이즈')
for k, name in enumerate(enemyNames):
    plt.annotate(f'{name},{winRatesByEnemyName[k]*100:.2f}%승', (avgLevelDifferenceByEnemyName[k]+1.5,avgPhasesByEnemyName[k]+0.1),
                 rotation=30, fontsize=8 )
    
plt.figure(4)
plt.scatter(avgPhasesByEnemyName,avgForeseesRateByEnemyName,s=MultiplyBy(countsByEnemyName,50),
            c=winRatesByEnemyName,cmap='Spectral',alpha=0.5)
plt.xlabel('평균 페이즈')
plt.ylabel('평균 예지 발동률 (%)') #size = 승률
plt.text(7,30,'원 면적=조우횟수\n원 색상=승률')
for k, name in enumerate(enemyNames):
    plt.annotate(f'{name}', (avgPhasesByEnemyName[k]+0.2,avgForeseesRateByEnemyName[k]+0.5),
                 rotation=30, fontsize=8 )
plt.colorbar()
plt.show()

#print(Counter(phases))
#print(Counter(winLose))