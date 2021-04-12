with open('D:/Git_Repos/Realtime_Animal_Tracking/Realtime_Animal_Tracking/DatasetTrain.txt', 'r') as f:
  lines = f.readlines()

with open('D:/Git_Repos/Realtime_Animal_Tracking/Realtime_Animal_Tracking/DatasetTrain.txt', 'w') as f:
    for line in lines:
        start = line[:13]
        end = line[13:]
        f.write(start + "image" + end)