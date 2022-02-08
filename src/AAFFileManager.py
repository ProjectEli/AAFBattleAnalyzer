from pathlib import Path
from .AAFLogCore import process_logtext

class FileManager:
    def __init__(self,dirs):
        self.filenames = []
        self.Nfiles = 0
        
        if isinstance(dirs,str):
            self.dirList = [dirs]
        elif isinstance(dirs,list):
            self.dirList = dirs
        else:
            raise(ValueError('dirs can be single str or list of str'))
        
    def gather_filenames(self):
        from os import walk
        from os.path import join
        filenames = []
        for dirName in self.dirList:
            for root,_,files in walk(dirName): #depth 1 search
                if len(files):
                    for filename in files:
                        filenames.append(join(root,filename))
        self.filenames = filenames
        self.Nfiles = len(filenames)
        print(f'{self.Nfiles} files gathered')
        
    def readFile(self,fileName):
        ftext = None
        with open(fileName,encoding='utf8') as f:
            ftext = f.read()
        return ftext
    
    def registerFile(self,fileName,db):
        ftext = self.readFile(fileName)
        phaseContents = process_logtext(ftext)
        db.addPhaseInfoToDb(phaseContents,battle_info=Path(fileName).stem)
    
    def register_files(self,db):        
        import time
        start = time.time()
        for k, filename in enumerate(self.filenames):
            print(f'{k+1}/{self.Nfiles}, {filename}')
            self.registerFile(filename,db)
        end = time.time()
        print(f'elapsed time = {end-start} sec')
        
if __name__ == '__main__':
    from AAFLogCore import process_logtext