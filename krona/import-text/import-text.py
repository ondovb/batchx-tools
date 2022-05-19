#!/usr/bin/python3
import json
import os
import subprocess
import sys
import pandas as pd
from pandas.api.types import is_numeric_dtype


# Parse json
with open("/batchx/input/input.json", "r") as inputFile:
    inputJson = inputFile.read()
parsedJson = json.loads(inputJson)

# BX_MEMORY & BX_VCPUS
bxMemory = os.environ['BX_MEMORY']
bxVcpus = os.environ['BX_VCPUS']

# textFile
textFile = parsedJson["textFile"]
print("First lines of the input 'textFile':", flush=True)
subprocess.check_call ("head " + textFile, shell=True)
print("-----------------------------------------------------------------------------", flush=True)

# withQuantityColumn
# if set to 'false' add '-q' 
withQuantityColumnString = ""
if "withQuantityColumn" not in parsedJson or parsedJson.get("withQuantityColumn"):
    print("First column WILL be considered as the quantity column.", flush=True)
    # reading manifest file into a pandas dataframe
    checkTextFile = pd.read_csv(textFile, sep='\t', comment='#', header=None)
    if not is_numeric_dtype(checkTextFile[0]):
        raise ValueError("At least one value in the quantity column is not numeric.")
else:
    print("First column WILL NOT be considered as the quantity column.", flush=True)
    withQuantityColumnString = " -q"

# define output dir
outputDir = "/batchx/output/" 

# krona outputDir
outputDir = outputDir + "krona/"
os.mkdir(outputDir)

# outputPrefix
outputPrefix = "krona"
if "outputPrefix" in parsedJson:
    outputPrefix = parsedJson["outputPrefix"]

# krona ouputs
kronagram = outputDir + outputPrefix + ".html"

# run krona
try:
    kronaVersionCmd = "ktImportText | head -2"
    subprocess.check_call (kronaVersionCmd, shell=True)
    kronagramCmd = "ktImportText"\
        + withQuantityColumnString\
        + " -o " + kronagram\
        + " " + textFile
    print(kronagramCmd, flush=True)
    subprocess.check_call (kronagramCmd, shell=True)
except subprocess.CalledProcessError as e:
        print(e)
        exit(e.returncode)
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

# Write output json file
outputJson = {
    'kronagram': kronagram
}

with open('/batchx/output/output.json', 'w+') as json_file:
    json.dump(outputJson, json_file)