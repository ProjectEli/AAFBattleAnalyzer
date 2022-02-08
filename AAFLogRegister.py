if __name__ == '__main__':
    from src.AAFDbOperation import AAFDB
    db = AAFDB()
    # db.deleteDbAll()
    
    from src.AAFFileManager import FileManager
    dirList = [f'LogSet{x+1}' for x in range(3)]
    fm = FileManager(dirList)
    fm.gather_filenames()    
    fm.register_files(db) # this can take some time

    # View some results
    view = db.getView()
    for k in range( min(len(view),5) ):
        print(view[k])