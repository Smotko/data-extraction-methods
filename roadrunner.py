import subprocess
import os
import glob
import time

from constants import FOLDER_NAMES

def roadrunner():
    for folder in FOLDER_NAMES:
        analyse_pages(folder)

def analyse_pages(folder_name):
    command = 'java -cp lib/roadrunner.jar:lib/nekohtml.jar:lib/xercesImpl.jar:lib/xmlParserAPIs.jar roadrunner.Shell' # base java command
    command += ' -N' + folder_name # output folder
    command += ' -Oexamples/prefs.xml' # preferences to be used

    # we have to work with absolute paths, because roadrunner runs in another folder
    examples_src_folder = os.getenv('RR_SRC_FOLDER', '.')
    pages = glob.glob(examples_src_folder + folder_name + '/' + folder_name + '/*')    
    for page in pages:
        command += ' ' + page

    os.chdir("RoadRunner")

    start_time = time.time()
    subprocess.run(command, shell=True, check=True)
    print('\nExecution time: {:.2f}s'.format(time.time() - start_time))

    os.chdir("..")

    print('--------------------------------------------\n')



