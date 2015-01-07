PATHEXT=.COM;.EXE;.BAT;.CMD;.PY;.PYW
cd C:\Documents and Settings\Adrian Nye\My Documents\FamilyRhyme\rhymeRawData
parsepron.py > logfile
prunewords.py >> logfile
genrhymes.py >> logfile
type logfile

