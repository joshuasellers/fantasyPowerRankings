import consts
import glob, os
from docx2pdf import convert
import time
import document
import sleeperFunctions


if __name__ == '__main__':
    sleeperFunctions.update_player_data() # call every once in a while to keep this up to date
    filename = 'week' + str(consts.WEEK()) + 'results'
    print("Removing any previous files")
    for f in glob.glob("*.docx"):
        os.remove(f)
    for f in glob.glob("*.pdf"):
        os.remove(f)
    time.sleep(5)
    print("Creating new docx file")
    document.create_docx(filename + '.docx')
    time.sleep(2.5)
    print("Converting new docx file to a PDF file")
    if os.path.exists(filename + '.docx'):
        convert(filename + '.docx')
