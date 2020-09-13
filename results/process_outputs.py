import os
import glob
import csv


frames = 10
detectorTypes = ["Shi-Tomasi", "Harris", "FAST", "BRISK", "ORB", "AKAZE", "SIFT"]
descriptorTypes =["BRISK", "BRIEF", "ORB", "FREAK", "AKAZE", "SIFT"]
keypoints_in_images = [{} for i in range(frames)]
mean_num_matches_combinations = dict()
mean_time_combinations = dict()
for descriptor in descriptorTypes:  # initialize:   descriptor -->> detectors: detector -->> time/num 
	mean_time_combinations[descriptor] = dict()
	mean_num_matches_combinations[descriptor] = dict()


cnt = 0
for filename in glob.glob('*.txt'):
	with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
		lines = f.readlines()

		image_index = 0
		detector_type, descriptor_type = "", ""
		time_taken = 0.0
		num_matches = 0
		for line in lines:
			if line is None:
				continue
			content = line.split() 
			if content[0] == "#1":
				image_index = int(content[4][-2])
				continue
			if content[1] == "detection":
				detector_type = content[0]
				# print(detector_type)
				num = int(content[3][2:])
				time = float(content[6])
				time_taken += time
				keypoints_in_images[image_index][detector_type] = [num, time] # detector_type -->> num, time
				# print(keypoints_in_images[image_index][detector_type])
				continue
			if content[1] == "descriptor":
				descriptor_type = content[0]
				time = float(content[-2])
				time_taken += time
				# print(descriptor_type, time)
				continue
			if "matches" in content:
				num_matches += int(content[4][2:])
		mean_time_taken = time_taken / frames
		mean_num_matches = int(num_matches / (frames - 1))
		if mean_num_matches != 0:
			mean_time_combinations[descriptor_type][detector_type] = mean_time_taken
			mean_num_matches_combinations[descriptor_type][detector_type] = mean_num_matches
			cnt += 1
			# print(descriptor_type, detector_type, mean_num_matches, mean_time_taken, cnt, filename)	
		else:
			print(filename)	

# with open('../NumOfKeyPoints.csv','w') as file:
# 	wr = csv.writer(file, quoting=csv.QUOTE_ALL)
# 	row0 = ["NumOfKeyPoints"] + detectorTypes
# 	wr.writerow(row0)
# 	for image_index in range(frames):
# 		line = ["image" + str(image_index)]
# 		for detector_type in detectorTypes:
# 			line.append(keypoints_in_images[image_index][detector_type][0])
# 		wr.writerow(line)

# with open('../TimeOfKeyPoints.csv','w') as file:
# 	wr = csv.writer(file, quoting=csv.QUOTE_ALL)
# 	row0 = ["TimeOfKeyPoints/ms"] + detectorTypes
# 	wr.writerow(row0)
# 	for image_index in range(frames):
# 		line = ["image" + str(image_index)]
# 		for detector_type in detectorTypes:
# 			line.append(keypoints_in_images[image_index][detector_type][1])
# 		wr.writerow(line)

with open('../MeanNumOfMatches.csv','w') as file:
	wr = csv.writer(file, quoting=csv.QUOTE_ALL)
	row0 = ["MeanNumOfMatches"] + detectorTypes
	wr.writerow(row0)
	for descriptor_type in descriptorTypes:
		line = [descriptor_type]
		for detector_type in detectorTypes:
			if descriptor_type not in mean_num_matches_combinations or \
			   detector_type not in mean_num_matches_combinations[descriptor_type]:
				line.append("NAN")
				continue
			line.append(mean_num_matches_combinations[descriptor_type][detector_type])
		wr.writerow(line)

with open('../MeanTimeOfMatches.csv','w') as file:
	wr = csv.writer(file, quoting=csv.QUOTE_ALL)
	row0 = ["MeanTimeOfMatches(ms)"] + detectorTypes
	wr.writerow(row0)
	for descriptor_type in descriptorTypes:
		line = [descriptor_type]
		for detector_type in detectorTypes:
			if descriptor_type not in mean_num_matches_combinations or \
			   detector_type not in mean_num_matches_combinations[descriptor_type]:
				line.append("NAN")
				continue
			line.append(mean_time_combinations[descriptor_type][detector_type])
		wr.writerow(line)

with open('../OverallPerformance.csv','w') as file:
	wr = csv.writer(file, quoting=csv.QUOTE_ALL)
	row0 = ["MeanNumOfMatches/MeanTimeOfMatches"] + detectorTypes
	wr.writerow(row0)
	for descriptor_type in descriptorTypes:
		line = [descriptor_type]
		for detector_type in detectorTypes:
			if descriptor_type not in mean_num_matches_combinations or \
			   detector_type not in mean_num_matches_combinations[descriptor_type]:
				line.append("NAN")
				continue
			line.append(mean_num_matches_combinations[descriptor_type][detector_type] / mean_time_combinations[descriptor_type][detector_type] * 1000)
		wr.writerow(line)
