with open('D:/Git_Repos/Realtime_Animal_Tracking/Realtime_Animal_Tracking/DatasetTest.txt', 'r') as f:
  lines = f.readlines()

with open('D:/Git_Repos/Realtime_Animal_Tracking/Realtime_Animal_Tracking/DatasetTest.txt', 'w') as f:
    for line in lines:
        start = line[:13]
        end = line[1:]
        f.write("/content/Realtime_Animal_Tracking" + end)