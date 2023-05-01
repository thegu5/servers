from mcstatus import JavaServer
from datetime import datetime
import json
import itertools
import threading
import sys
import time
import math

file_path_in = input("File with ips: ")
file_path_out = input("Output File: ")
# not_working_out = input("Not Working Ips Output File: ")
threads = 200
secondsInBetween = 1

all_info = []
done = 0
borked = 0
completelyDone = 0
totalPlayers = 0
# notWorking = []


def run(start, stop):
    global done
    global borked
    global completelyDone
    global totalPlayers
    for line in itertools.islice(Lines, start, stop):
        try:
            time.sleep(secondsInBetween)
            info = {}
            ip = str(line.strip())
            server = JavaServer(ip, 25565)
            status = server.status();

            try:
                version = status.raw["version"]['name']
            except:
                version = 'Unknown'

            try:
                description = status.raw["description"]['text']
            except:
                description = 'Unknown'

            try:
                maxPlayers = status.raw["players"]['max']
            except:
                maxPlayers = -1

            try:
                players = status.raw["players"]['sample']
            except:
                players = []
                
             try:
                currentPlayers = status.raw["players"]['online']
             except:
                currentPlayers = 0

            all_info.append({"ip": ip, "version": version, "description": description, "max_players": maxPlayers,
                             "known_players": players, "current_players": currentPlayers, "online": True})
            done += 1

        except Exception as e:
            # notWorking.append(str(line.strip()))
            borked += 1
    completelyDone += 1


file1 = open(file_path_in, 'r')
Lines = file1.readlines()
print('Starting')
print('Launching Threads')

total_ips = len(Lines)
ipsPerThread = math.floor(float(total_ips) / float(threads)) + 1
print(ipsPerThread)
startingEndingNum = -1

for thread in range(threads):

    threadnum = thread + 1

    if threadnum != threads:
        x = threading.Thread(target=run, args=(startingEndingNum + 1, startingEndingNum + ipsPerThread))
        print('Thread #{} - Range: {} - {}'.format(threadnum, startingEndingNum + 1, startingEndingNum + ipsPerThread))
        x.start()
    else:
        x = threading.Thread(target=run, args=(startingEndingNum + 1, len(Lines) - 1))
        print('Thread #{} - Range: {} - {}'.format(threadnum, startingEndingNum + 1, len(Lines) - 1))
        x.start()
    startingEndingNum += ipsPerThread

time.sleep(2)
call('clear' if os.name == 'posix' else 'cls')
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("Date and Time Started: ", dt_string)
while completelyDone != threads:
  percentDone = float(borked + done) / len(lines) * 100
  str = "{}% Complete, {} Threads Done, {} Working, {} Broken         ".format(
    round(percentDone, 2), completelyDone, done, borked)
  print(str, end="\r")
  sys.stdout.flush()
  time.sleep(0.2)

print('')
print("Done with data, printing to file.")

MyWorkingFile = open(file_path_out, 'w', encoding="utf-8")
print(json.dumps(all_info), file=MyWorkingFile)
MyWorkingFile.close()

"""
MyNotWorkingFile = open(not_working_out, 'w', encoding="utf-8")

for element in notWorking:
    print(json.dumps(element), file=MyNotWorkingFile)
MyNotWorkingFile.close()
"""

print("Done")
