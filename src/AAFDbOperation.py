import sqlite3

class AAFDB:
    def __init__(self,db_filename='AAFLog.db') -> None:
        self.db_filename = db_filename
        self.db = self.openDb(db_filename)
        self.cur = self.db.cursor()
        self.tableNames = ['Battle','Phase','PhaseInfo','BattleResult']

    def openDb(self,db_filename):
        return sqlite3.connect(db_filename)
    
    def createTableAll(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Battle (
                            battleId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
                            battleInfo STRING,
                            myName STRING,
                            enemyName STRING,
                            maxPhase INTEGER,
                            isWin INTEGER,
                            myLevel INTEGER,
                            enemyLevel INTEGER,
                            levelDifference INTEGER
                            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Phase (
                            phaseId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
                            battleId INTEGER NOT NULL,
                            phaseNum INTEGER NOT NULL,
                            myHP INTEGER NOT NULL,
                            myShield INTEGER NOT NULL,
                            enemyHP INTEGER NOT NULL,
                            enemyShield INTEGER NOT NULL,
                            FOREIGN KEY (battleId) REFERENCES Battle(battleId));''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS PhaseInfo (
                            lineId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
                            phaseId INTEGER NOT NULL,
                            lineNum INTEGER NOT NULL,
                            lineVal TEXT NOT NULL,
                            FOREIGN KEY (phaseId) REFERENCES Phase(phaseId));''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS BattleResult (
                            lineId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
                            battleId INTEGER NOT NULL,
                            lineNum INTEGER NOT NULL,
                            lineVal TEXT NOT NULL,
                            FOREIGN KEY (battleId) REFERENCES Battle(battleId)
                            );''')
        self.db.commit()
    
    def deleteTableAll(self):
        for tableName in self.tableNames:
            self.cur.execute(f'delete from {tableName}')
            self.cur.execute(f"delete from sqlite_sequence where name='{tableName}';")
        self.db.commit()
    
    def dropTableAll(self):
        for tableName in self.tableNames:
            self.cur.execute(f'drop table IF EXISTS {tableName}')
        self.db.commit()
        
    def totalBattles(self):
        self.cur.execute(f'''SELECT COUNT(*) FROM Battle''')
        return self.cur.fetchall()[0][0]
        
    def getView(self,options=''):
        self.cur.execute(f'''select Battle.battleInfo, Phase.phaseNum , PhaseInfo.lineNum , PhaseInfo.lineVal 
                            from Battle 
                            left join Phase on Battle.battleId = Phase.battleId
                            left join PhaseInfo on PhaseInfo.phaseId = Phase.phaseId 
                            order by battleInfo asc, phaseNum asc, lineNum asc
                            {options}''')
        return self.cur.fetchall()

    def getMaxBattleIds(self):
        self.cur.execute('SELECT MAX(battle_id) FROM Battle')
        self.max_battle_id = self.cur.fetchall()[0][0]
        return self.max_battle_id
    
    def getMaxPhaseIds(self):
        self.cur.execute('SELECT MAX(phase_id) FROM Phase')
        return self.cur.fetchall()[0][0]
    
    def addPhaseInfoToDb(self,phaseContents,battle_info):
        phaseInfo = phaseContents['phaseInfo']
        hpShields = phaseContents['hpShields']
        resultTexts = phaseContents['resultTexts']
        
        # add battle and get battle_id
        self.cur.execute(f'''INSERT into Battle (battleInfo, myName, enemyName, maxPhase, myLevel,enemyLevel,levelDifference,isWin) 
                        values('{battle_info}',
                               '{phaseContents['myName']}',
                               '{phaseContents['enemyName']}',
                                {phaseContents['maxphase']},
                                {phaseContents['levels'][0]},
                                {phaseContents['levels'][1]},
                                {phaseContents['levels'][2]},
                                {phaseContents['isWin']}
                                )''')
        self.cur.execute(f'select battleId from Battle where rowid = {self.cur.lastrowid};')
        battleId = self.cur.fetchall()[0][0]
        
        # add battleResult line data
        for lineIndex, lineVal in enumerate(resultTexts):
            lineNum = lineIndex+1
            self.cur.execute(f'''INSERT into BattleResult  (battleId,lineNum ,lineVal)
                                 values ({battleId},{lineNum},'{lineVal}')''')
        
        # add phaseInfo line data
        for phaseIndex, phase in enumerate(phaseInfo):
            # add phase and get phase_id
            phaseNum = phaseIndex+1
            myHP,myShield,enemyHP,enemyShield = hpShields[phaseIndex]
            self.cur.execute(f'''INSERT into Phase (battleId, phaseNum,myHP,myShield,enemyHP,enemyShield)
                             values({battleId},{phaseNum}, {myHP},{myShield},{enemyHP},{enemyShield})''')
            self.cur.execute(f'select phaseId from Phase where rowid = {self.cur.lastrowid};')
            phaseId = self.cur.fetchall()[0][0]
            
            for lineIndex, lineVal in enumerate(phase):
                lineNum = lineIndex+1
                # add phaseinfo data line by line
                self.cur.execute(f'''INSERT into PhaseInfo  (phaseId,lineNum ,lineVal)
                                 values ({phaseId},{lineNum},'{lineVal}')''')
            self.db.commit()

if __name__ == '__main__':
    from pathlib import Path
    from os import getcwd
    from os.path import join

    parent_path = Path(getcwd())
    db = AAFDB(join(parent_path,'AAFLog.db'))
    db.dropTableAll()
    db.createTableAll()