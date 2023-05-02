from mcstatus import JavaServer
from datetime import datetime
from subprocess import call
import json
import itertools
import threading
import sys
import time
import math
import os

file_path = "Servers.json"
threads = 300
secondsInBetween = 1

all_info = []
done = 0
borked = 0
completelyDone = 0
totalPlayers = 0


def run(start, stop):
  global done
  global borked
  global completelyDone
  global totalPlayers
  for line in itertools.islice(lines, start, stop + 1):
    try:
      time.sleep(secondsInBetween)

      ip = line.get("ip")
      server = JavaServer(ip, 25565, timeout=5)
      status = server.status()

      try:
        version = status.raw["version"]['name']
      except:
        version = line.get("version")

      try:
        description = status.raw["description"]['text']
      except:
        description = line.get("description")

      try:
        max_players = status.raw["players"]['max']
      except:
        max_players = line.get("max_players")
        
      try:
        current_players = status.raw["players"]['online']
      except:
        current_players = 0;
      
      try:
        players = status.raw["players"]['sample']
        players = [json.dumps(player) for player in players if player['uuid'] != "00000000-0000-0000-0000-000000000000"]
      except:
        players = []
      
      known_players = line.get('known_players')
      known_players = [json.dumps(player) for player in known_players if player['uuid'] != "00000000-0000-0000-0000-000000000000"]  

      """
      try:
        icon = status.raw["favicon"]
      except:
        icon = "data:image/png;base64,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"
      """  
      
      all_info.append({
        "ip": ip,
        "version": version,
        "description": description,
        "max_players": max_players,
        "known_players": list(set(players + line.get('known_players'))),
        "current_players": current_players,
        #"icon": icon,
        "online": True
      })
      done += 1

    except Exception:
      all_info.append({
        "ip": line["ip"],
        "version": line.get("version"),
        "description": line.get("description"),
        "max_players": line.get("max_players"),
        "known_players": line.get("known_players"),
        "current_players": 0,
        #"icon": line.get("icon"),
        "online": False
      })
      borked += 1
  completelyDone += 1


file1 = open(file_path, 'r', encoding="utf-8")
lines = json.load(file1)
print('Starting')
print('Launching Threads')

total_ips = len(lines)
ipsPerThread = math.floor(float(total_ips) / float(threads)) + 1
print(ipsPerThread)
startingEndingNum = -1

for thread in range(threads):

  threadnum = thread + 1

  if threadnum != threads:
    x = threading.Thread(target=run,
                         args=(startingEndingNum + 1,
                               startingEndingNum + ipsPerThread))
    print('Thread #{} - Range: {} - {}'.format(
      threadnum, startingEndingNum + 1, startingEndingNum + ipsPerThread))
    x.start()
  else:
    x = threading.Thread(target=run,
                         args=(startingEndingNum + 1, len(lines) - 1))
    print('Thread #{} - Range: {} - {}'.format(threadnum,
                                               startingEndingNum + 1,
                                               len(lines) - 1))
    x.start()
  startingEndingNum += ipsPerThread

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("Date and Time Started: ", dt_string)

time.sleep(2)
call('clear' if os.name == 'posix' else 'cls')
percentDone = 0
while percentDone != 100:
  percentDone = float(borked + done) / len(lines) * 100
  str = "{}% Complete, {} Threads Done, {} Working, {} Broken, {} Todo        ".format(
    round(percentDone, 2), completelyDone, done, borked, len(lines))
  print(str, end="\r")
  sys.stdout.flush()
  time.sleep(0.2)

print('')
print("Printing to file.")
os.remove(file_path)
MyWorkingFile = open(file_path, 'w', encoding="utf-8")

print(json.dumps(all_info), file=MyWorkingFile)

  
MyWorkingFile.close()

print("Done")