import subprocess
from os import listdir
from os.path import isfile, join
import time
import sys

passed = 0
failed = 0
timeWarning = 0

def sorter(x):
    x = x[24:]
    return int(''.join(x.split('Boxes')))

def getTestCaseList():
    testPath = "./TestCases/"
    return [testPath + f for f in listdir(testPath) if isfile(join(testPath, f))]

def getResults():
    result = dict()
    resPath = "./results/"
    files = [f for f in listdir(resPath) if isfile(join(resPath, f))]
    for i in files:
        res = int(open(resPath + i).read().strip())
        result[i] = res
    return result

def prepareOutput(testName, result, expected, tim):
    global passed, failed, timeWarning
    status = result == expected
    timeStatus = tim < 1
    line = testName + " | "
    line += "OUTPUT: " + str(result) + " | "
    line += "EXPECTED: " + str(expected) + " | "
    line += "TIME: " + str(tim)
    if status and timeStatus:
        passed += 1
        line = "\033[92mPassed\033[0m | " + line
        print(line)
    elif status and not timeStatus:
        timeWarning += 1
        line = "\033[93mTime Warning\033[0m | " + line
        print(line)
    else:
        failed +=1
        line = "\033[91mFailed\033[0m | " + line
        print(line)
    print("-"*100)

def tester(testCases, results):
    global passed, failed, timeWarning
    prog = sys.argv[1]
    for i in testCases:
        inp = open(i)
        start = time.time()
        p = subprocess.Popen(prog, stdin=inp, stdout=subprocess.PIPE)
        out = int(p.stdout.read())
        tim = time.time() - start
        testName = i.split('/')[-1]
        prepareOutput(testName, out, results[testName], tim)
    print("\033[94mTotal: ", passed+failed+timeWarning, '\033[0m', " \033[92mPassed: ", passed, '\033[0m', " \033[91mFailed: ", failed, '\033[0m', " \033[93mTime Fail: ", timeWarning, '\033[0m')

if __name__ == "__main__":
    testCases = getTestCaseList()
    testCases = sorted(testCases, key=sorter)
    results = getResults()
    tester(testCases, results)