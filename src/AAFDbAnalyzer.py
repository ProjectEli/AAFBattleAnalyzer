from AAFDbOperation import AAFDB
import re

def MultiplyBy(numList,multiplier): return list(map(lambda x: x*multiplier,numList))

class DBAnalyzer:
    def __init__(self,dbObj:AAFDB) -> None:
        self.db = dbObj.db
        self.cur = self.db.cursor()
        self.fullTableSqlString = '''FROM Battle
                                    left join Phase on Battle.battleId = Phase.battleId
                                    left join PhaseInfo on PhaseInfo.phaseId = Phase.phaseId '''
        self.fontSize = 9
        self.subplot = 1
        self.xlim = [0, 22]
    
    def selectDamageTaken(self):
        # self.cur.execute(f'''select Battle.battleInfo, Phase.phaseNum , PhaseInfo.lineNum , PhaseInfo.lineVal 
        #                      from Battle 
        #                      left join Phase on Battle.battleId = Phase.battleId
        #                      left join PhaseInfo on PhaseInfo.phaseId = Phase.phaseId 
        #                      where PhaseInfo.lineVal like Battle.myName||'%%입었다%'
        #                      order by battleInfo asc, phaseNum asc, lineNum asc''')
        self.cur.execute(f'''SELECT PhaseInfo.lineVal 
                            {self.fullTableSqlString}
                            where PhaseInfo.lineVal like Battle.myName||'%%입었다%';''')
        return self.cur.fetchall()
    
    def extractDamage(self,text):
        try:
            dmg = int( re.search('>(.+?)</font>',text).group(1) )
        except:
            dmg = 0
        return dmg
    
    def extractDamageTaken(self):
        refinedTable = self.selectDamageTaken()
        return [self.extractDamage(rows[0]) for rows in refinedTable]
    
    def selectLoots(self):
        self.cur.execute(f'''select BattleResult.lineVal 
                            from Battle 
                            left join BattleResult on Battle.battleId = BattleResult.battleId
                            where BattleResult.lineVal like '당신은 쓰러진%'
                            order by battleInfo asc;''')
        return self.cur.fetchall()
    
    def extractLootFromText(self,text):
        try:
            lootText = re.search('>(\w+)/<(.+?)>',text[::-1]).group(2)[::-1] # search from backside
        except:
            lootText = ''
        return lootText
    
    def extractRoots(self):
        refinedTable = self.selectLoots()
        return [self.extractLootFromText(rows[0]) for rows in refinedTable]
    
    def bubblePlotData(self):
        # self.cur.execute('''SELECT Battle.enemyName, avg(Battle.maxPhase), count(*), avg(Battle.isWin), avg(Battle.levelDifference)
        #                     FROM Battle
        #                     where substr(Battle.battleInfo, 9, 10) >= '08'
        #                     GROUP BY Battle.enemyName;''')
        self.cur.execute('''SELECT Battle.enemyName, avg(Battle.maxPhase), count(*), avg(Battle.isWin), avg(Battle.levelDifference)
                            FROM Battle
                            GROUP BY Battle.enemyName;''')
        return self.cur.fetchall()
    
    def setupPlots(self):
        # import font for 한글
        from matplotlib import font_manager,rc
        font_path = 'D2Coding-Ver1.3.2-20180524-all.ttc'
        font = font_manager.FontProperties(fname=font_path).get_name()
        rc('font',family=font)
        
        import matplotlib.pyplot as plt
        return plt
    
    def plotBubbles(self, plt):
        avgPhases = []
        enemyNames = []
        encounters = []
        winRates = []
        avgLevelDifferences = []
        
        d = self.bubblePlotData()
        for row in d:
            enemyName,avgPhase,encounter,winRate,avgLevelDifference = row
            enemyNames.append(enemyName)
            avgPhases.append(avgPhase)
            encounters.append(encounter)
            winRates.append(winRate)
            avgLevelDifferences.append(avgLevelDifference)
            
        if not self.subplot:
            plt.figure(11)
            plt.scatter(avgPhases,winRates,s=MultiplyBy(encounters,10),
                        c=winRates,cmap='Spectral',alpha=0.5)
            plt.xlabel('평균 페이즈')
            plt.ylabel('승률') #size = 승률
            plt.title('원 면적=조우횟수, 원 색상=승률')
            for k, name in enumerate(enemyNames):
                plt.annotate(f'{name}', (avgPhases[k]+0.2,winRates[k]-0.005),
                            rotation=0, fontsize=8 )
            plt.colorbar()
            
            plt.figure(12)
            plt.scatter(avgPhases,avgLevelDifferences,s=MultiplyBy(encounters,10),
                        c=winRates,cmap='Spectral',alpha=0.3)
            plt.xlabel('평균 페이즈')
            plt.ylabel('적과의 평균 레벨차') #size = 승률
            plt.title('원 면적=조우횟수, 원 색상=승률')
            for k, name in enumerate(enemyNames):
                plt.annotate(f'{name}', (avgPhases[k]+0.2,avgLevelDifferences[k]-0.5),
                            rotation=0, fontsize=8 )
            plt.colorbar()
        else:
            plt.figure(100)
            plt.subplot(5,9,2)
            plt.scatter(avgPhases,winRates,s=MultiplyBy(encounters,1),
                        c=winRates,cmap='Spectral',alpha=0.5)
            plt.xticks(fontsize=self.fontSize)
            plt.yticks(fontsize=self.fontSize)
            plt.xlabel('평균 페이즈',fontsize=self.fontSize,labelpad=-2)
            plt.ylabel('승률',fontsize=self.fontSize,labelpad=-30) #size = 승률
            plt.title('원 면적=조우횟수, \n원 색상=승률',fontsize=self.fontSize)
            ax = plt.gca()
            # ax.xaxis.tick_top()
            ax.tick_params(axis="y",direction="in", pad=2)
            ax.tick_params(axis="x",direction="in", pad=1.5)
            for k, name in enumerate(enemyNames):
                if avgPhases[k]+0.2 >8:
                    plt.annotate(f'{name}', (avgPhases[k]-1,winRates[k]-0.005),
                                rotation=0, fontsize=self.fontSize/2 )
                else:
                    plt.annotate(f'{name}', (avgPhases[k]+0.2,winRates[k]-0.005),
                                rotation=0, fontsize=self.fontSize/2 )
            # cb = plt.colorbar()
            # cb.ax.tick_params(labelsize=self.fontSize)
            
            plt.figure(100)
            plt.subplot(5,9,3)
            plt.scatter(avgPhases,avgLevelDifferences,s=MultiplyBy(encounters,1),
                        c=winRates,cmap='Spectral',alpha=0.3)

            plt.xlabel('평균 페이즈',fontsize=self.fontSize,labelpad=-2)
            plt.ylabel('적과의 평균 레벨차',fontsize=self.fontSize) #size = 승률
            plt.title('원 면적=조우횟수, \n원 색상=승률',fontsize=self.fontSize)
            ax = plt.gca()
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
            plt.xticks(fontsize=self.fontSize)
            plt.yticks(fontsize=self.fontSize)
            ax.tick_params(axis="x",direction="in", pad=1.5)
            for k, name in enumerate(enemyNames):
                if avgPhases[k]+0.2 >8:
                    plt.annotate(f'{name}', (avgPhases[k]-1,avgLevelDifferences[k]-0.5),
                                rotation=0, fontsize=self.fontSize/2,zorder=-3 )
                else:
                    plt.annotate(f'{name}', (avgPhases[k]+0.2,avgLevelDifferences[k]-0.5),
                                rotation=0, fontsize=self.fontSize/2,zorder=-3 )
            # cb = plt.colorbar()
            # cb.ax.tick_params(labelsize=self.fontSize)
            
        
    def stackedBarData(self):
        self.cur.execute('''SELECT Battle.maxPhase
                            FROM Battle
                            where Battle.isWin = 1
                            ;''')
        wins= self.cur.fetchall()
        self.cur.execute('''SELECT Battle.maxPhase
                            FROM Battle
                            where Battle.isWin = 0
                            ;''')
        loses= self.cur.fetchall()
        return {'wins':wins,'loses':loses}
    
    def plotStackedBars(self,plt):
        d = self.stackedBarData()
        wins = [row[0] for row in d['wins']]
        loses = [row[0] for row in d['loses']]
        
        maxPhase = max( max(wins), max(loses))
        nWin = len(wins)
        nLose = len(loses)
        nTotal = nWin+nLose
        winRate = 100* nWin / nTotal # float in python 3+
        
        if not self.subplot:
            plt.figure(1)
            plt.hist( (wins,loses),bins=range(maxPhase+1), 
                    histtype='barstacked', label=('승','패'))
            plt.title(f'{nTotal}전 {nWin}승 {nLose}패, 승률:{winRate}%')
            plt.xlabel('종료 페이즈')
            plt.ylabel('전투 수')
            plt.legend( )
        else:
            plt.figure(100)
            plt.subplot(5,9,1)
            plt.hist( (wins,loses),bins=range(maxPhase+1), 
                    histtype='barstacked', label=('승','패'))
            ax = plt.gca()
            ax.set_xlim(self.xlim)
            plt.xticks(fontsize=self.fontSize)
            plt.yticks(fontsize=self.fontSize)
            plt.title(f'{nTotal}전 {nWin}승 {nLose}패,\n 승률:{winRate}%',fontsize=self.fontSize)
            # plt.xlabel('종료 페이즈',fontsize=self.fontSize)
            plt.ylabel('전투 수',fontsize=self.fontSize)
            plt.legend( )
        
        
    def endPhaseHpShieldData(self):
        self.cur.execute('''SELECT COUNT(*), Battle.maxPhase  , AVG(Phase.myHP) ,AVG(Phase.myShield) , AVG(Phase.enemyHP) , AVG(Phase.enemyShield )
                            FROM Battle
                            left join Phase on Battle.battleId = Phase.battleId
                            where Phase.PhaseNum = Battle.maxPhase
                            GROUP BY Battle.maxPhase ;''')
        return self.cur.fetchall()
    
    def plotEndPhaseHpShieldData(self,plt):
        from numpy import array
        d= self.endPhaseHpShieldData()
        encounters = array([row[0] for row in d])
        nEncounters = sum(encounters)
        
        endPhases = array([row[1] for row in d])
        myHps = [row[2] for row in d]
        myShields = [row[3] for row in d]
        enemyHps = [row[4] for row in d]
        enemyShields = [row[5] for row in d]
        width = 0.3
        
        plt.figure(31)
        plt.bar(endPhases-width*0.5,myHps,label='내 HP',width=width,color='tab:blue')
        plt.bar(endPhases-width*0.5,myShields,label='내 쉴드',bottom=myHps,width=width,color='tab:gray')
        plt.bar(endPhases+width*0.5,enemyHps,label='적 HP',width=width,color='tab:green')
        plt.bar(endPhases+width*0.5,enemyShields,label='적 쉴드',bottom=enemyHps,width=width,color='tab:purple')
        plt.xlabel('종료 페이즈')
        plt.ylabel('HP 및 쉴드 (%)')
        plt.title(f'{nEncounters}전 데이터')
        plt.legend()
        
    def endPhaseHpShieldDataByEnemyName(self):
        self.cur.execute('''SELECT Battle.enemyName ,COUNT(*)
                            FROM Battle
                            left join Phase on Battle.battleId = Phase.battleId
                            where Phase.PhaseNum = Battle.maxPhase
                            GROUP BY Battle.enemyName  ;''')
        enemyNames = self.cur.fetchall()
        hpShieldData = {}
        encounters = {}
        for enemyName,encounter in enemyNames:
            self.cur.execute(f'''SELECT Battle.maxPhase  , AVG(Phase.myHP) ,AVG(Phase.myShield) , AVG(Phase.enemyHP) , AVG(Phase.enemyShield )
                                FROM Battle
                                left join Phase on Battle.battleId = Phase.battleId
                                where Phase.PhaseNum = Battle.maxPhase AND Battle.enemyName = '{enemyName}'
                                GROUP BY Battle.maxPhase   ;''')
            hpShieldData[enemyName] = self.cur.fetchall()
            encounters[enemyName] = encounter
        return (hpShieldData, encounters)
    
    def getMainMonitorResolution(self):
        import ctypes
        user32 = ctypes.windll.user32
        return (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
    
    def getPossibleRows(self,nFigs):
        from math import floor,ceil
        mainMonitorWidth, mainMonitorHeight = self.getMainMonitorResolution()
        
        # defaultFigSize = [6.4,4.8] # inches
        defaultDpi = 80
        defaultWidth = 6.4*defaultDpi
        defaultHeight = 4.8*defaultDpi
        windowMenubarHeight=35
        possibleRows = floor(mainMonitorHeight/(defaultHeight + windowMenubarHeight))
        possibleCols = floor(mainMonitorWidth/defaultWidth)
        
        if nFigs > (possibleCols*possibleRows):
            print('half size')
            defaultHeight = ceil(defaultHeight/2.5)
            defaultWidth = ceil(defaultWidth/2.5)
            
            possibleCols = floor(mainMonitorWidth/defaultWidth)
            possibleRows = floor(mainMonitorHeight/(defaultHeight + windowMenubarHeight))
            
        return (possibleRows,possibleCols,defaultWidth,defaultHeight, \
            mainMonitorWidth, mainMonitorHeight,windowMenubarHeight)
    
    def resizeFigs(self,plt,nFigs):
        from math import floor
        possibleRows,possibleCols,defaultWidth,defaultHeight, \
            mainMonitorWidth, mainMonitorHeight,windowMenubarHeight = self.getPossibleRows(nFigs)
        for k in range(nFigs):
            plt.figure(100+k)
            mngr = plt.get_current_fig_manager()
            yind = floor(k/possibleCols)
            xind = k%possibleCols # remainder
            pos1 = xind*defaultWidth + 1
            pos2 = (yind)*(defaultHeight + windowMenubarHeight) + 1
            pos3 = defaultWidth
            pos4 = defaultHeight
            mngr.window.setGeometry(pos1,pos2,pos3,pos4)
    
    def plotEndPhaseHpShieldDataByEnemyName(self,plt):
        width = 0.3

        d, dEncounters= self.endPhaseHpShieldDataByEnemyName()
        nFigs = len(d.keys())
        
        # scaling
        possibleRows,possibleCols,defaultWidth,defaultHeight, \
            mainMonitorWidth, mainMonitorHeight,windowMenubarHeight = self.getPossibleRows(nFigs)
        print(possibleRows,possibleCols, nFigs)
        
        plt.figure(100)
        for k, enemyName in enumerate(d.keys()):
            dEnemy = d[enemyName]
            nEncounters = dEncounters[enemyName]
            from numpy import array
            endPhases = array([row[0] for row in dEnemy])
            myHps = [row[1] for row in dEnemy]
            myShields = [row[2] for row in dEnemy]
            enemyHps = [row[3] for row in dEnemy]
            enemyShields = [row[4] for row in dEnemy]
            
            # plt.rcParams['figure.figsize']=[2,1]
            plt.subplot(possibleRows,possibleCols,(possibleRows*possibleCols)-k)
            plt.bar(endPhases-width*0.5,myHps,label='내 HP',width=width,color='tab:blue')
            plt.bar(endPhases-width*0.5,myShields,label='내 쉴드',bottom=myHps,width=width,color='tab:gray')
            plt.bar(endPhases+width*0.5,enemyHps,label='적 HP',width=width,color='tab:green')
            plt.bar(endPhases+width*0.5,enemyShields,label='적 쉴드',bottom=enemyHps,width=width,color='tab:purple')
            
            ax = plt.gca()
            ax.set_ylim([0, 130])
            ax.set_xlim(self.xlim)
            # ax.xaxis.tick_top()
            if k+1 > possibleCols:
                pass
                # plt.xticks(visible=False)
            else:
                plt.xlabel('종료 페이즈', fontsize = self.fontSize)
                
            if ((k+1)%possibleCols) ==0:
                plt.ylabel('HP 및 쉴드 (%)',fontsize = self.fontSize)
            else:
                pass
                # plt.yticks(visible=False)
            # if ((k+1)%possibleRows) ==1:
            #     plt.xlabel('종료 페이즈', fontsize = self.fontSize)
            

            
            # ax.xaxis.set_label_position('top') 
            plt.xticks(fontsize=self.fontSize)
            plt.yticks(fontsize=self.fontSize)
            plt.title(f'{enemyName}: {nEncounters}전',fontsize=self.fontSize)
        
        plt.subplot(possibleRows,possibleCols,(possibleRows*possibleCols)-nFigs)
        plt.bar(0,0,label='내 HP',width=width,color='tab:blue')
        plt.bar(0,0,label='내 쉴드',bottom=myHps,width=width,color='tab:gray')
        plt.bar(0,0,label='적 HP',width=width,color='tab:green')
        plt.bar(0,0,label='적 쉴드',bottom=enemyHps,width=width,color='tab:purple')
        
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        # ax.axes.yaxis.set_visible(False)
        ax.set_ylim([0, 130])
        plt.yticks(fontsize=self.fontSize)
        plt.ylabel('HP 및 쉴드 (%)',fontsize = self.fontSize)
        # plt.yticks(visible=False)
        # plt.xticks(visible=False)
        
        plt.legend()
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(0,windowMenubarHeight,mainMonitorWidth, mainMonitorHeight-windowMenubarHeight)
        # plt.tight_layout()
        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05, hspace=0.3)
            
        # self.resizeFigs(plt,nFigs)
        
    def plotLoots(self,plt):
        from collections import Counter
        cSorted = Counter(self.extractRoots()).most_common()
        lootNames = [elem[0] for elem in cSorted]
        counts = [elem[1] for elem in cSorted]
        
        plt.figure(40)
        ypos = range(len(lootNames))
        # cmap rescale
        from matplotlib import cm
        import numpy as np
        rescale = lambda y: (y-np.min(y)) / (np.max(y)-np.min(y))
        cmap = cm.get_cmap('Spectral')        
        rescaledCmap = [cmap(x) for x in rescale(counts)]
        plt.barh(ypos,counts,align='center',color = rescaledCmap)
        plt.xticks(np.arange(0, max(counts)+1, 2))
        plt.yticks(ypos,labels=lootNames)
        ax = plt.gca()
        ax.invert_yaxis()
        plt.xlabel('누적 획득 수량 (개)')
        plt.tight_layout()
        plt.title(f'{dbObj.totalBattles()}전, 총 {sum(counts)}개 획득')
        
            
    
if __name__ == '__main__':
    from pathlib import Path
    from os import getcwd
    from os.path import join

    parent_path = Path(getcwd())
    dbObj = AAFDB(join(parent_path,'AAFLog.db'))
    dba = DBAnalyzer(dbObj)
    
    plt = dba.setupPlots()
    # dba.plotBubbles(plt)
    # dba.plotStackedBars(plt)
    # dba.plotEndPhaseHpShieldData(plt)
    # # print( dba.getMainMonitorResolution() )
    # dba.plotEndPhaseHpShieldDataByEnemyName(plt)
    dba.plotLoots(plt)
    plt.show()