import re, os, glob

class DictDiffer(object):
	"""
	Calculate the difference between two dictionaries as:
	(1) items added
	(2) items removed
	(3) keys same in both but changed values
	(4) keys same in both and unchanged values
	"""
	def __init__(self, current_dict, next_dict, file):
		self.current_dict, self.next_dict = current_dict, next_dict
		self.set_current, self.set_past = set(current_dict.keys()), set(next_dict.keys())
		self.intersect = self.set_current.intersection(self.set_past)
		self.file = file
		self.output = ""
		self.different_keys = 0
		self.different_files = 0

	def find_difference(self):
		added = self.set_current - self.intersect 
		removed = self.set_past - self.intersect 
		changed = set()
		for o in self.intersect:
			if self.next_dict[o] != self.current_dict[o]:
				changed.add(o)

		if(len(added|removed|changed) != 0):
			self.output += "=================================================================================================\n"
			self.output += "SOURCE: " + source_file_list[file] + "\n"
			self.output += "TARGET: " + target_file_list[file] + "\n"
			self.different_files += 1
		if(len(added) != 0):
			self.output += "\nKeys in SOURCE but not in TARGET: \n"
			for key in added:
				self.output += "    " + key + "=" + self.current_dict[key] + "\n"
				self.different_keys += 2
		if(len(removed) != 0):
			self.output += "\nKeys in TARGET but not in SOURCE: \n"
			for key in removed:
				self.output += "    " + key + "=" + self.next_dict[key] + "\n"
				self.different_keys += 2
		if(len(changed) != 0):
			self.output += "\nDifferent values: \n"
			for key in changed:
				self.output += "    " + key + "=" + self.current_dict[key] + " (SOURCE)\n"
				self.output += "    " + key + "=" + self.next_dict[key] + " (TARGET)\n"
				self.different_keys += 1
		return [self.output, self.different_files, self.different_keys]

# add all .properties file path in paths to a list
def find_properties_in_paths(paths):
	file_lists = {}
	for start_path in paths:
		if os.path.isdir(start_path):
			for path, _, _ in os.walk(start_path):
				for file in glob.glob(path + "\\*.properties"):
					if (os.path.basename(file) in file_lists):
						file_lists[os.path.basename(file) + "-[duplicated]"] = file
					else:
						file_lists[os.path.basename(file)] = file
	for path in paths:
		if os.path.isfile(path):
			file_lists[os.path.basename(path)] = path
	return file_lists

# read input path from user
print("=================================================================================================")
print("=================================== DIFFERENCE FINDER PROGRAM ===================================")
print("=================================================================================================")
source_path = input("\n>>> Insert source path:\n")
target_path = input(">>> Insert target path:\n")		

# # default path
# source_path = "D:\\multipolar-project\\multipolar-task\\first-folder;D:\\multipolar-project\\multipolar-task\\application1.properties"
# target_path = "D:\\multipolar-project\\multipolar-task\\second-folder;D:\\multipolar-project\\multipolar-task\\application2.properties"

print("\n>> CONFIG\n")
print("SOURCE FILE LISTS: ")
print(source_path)
print("\nTARGET FILE LISTS: ")
print(target_path)

# split by semi colon
source_path = re.split(';', source_path)
target_path = re.split(';', target_path)

# add all .properties file path in source_path to a list
source_file_list = find_properties_in_paths(source_path)

# add all .properties file path in target_path to a list
target_file_list = find_properties_in_paths(target_path)

print("\n>> RESULT: ")

# calculate the total number of files and keys in source
num_of_keys = 0
for file in source_file_list.values():
	num_of_keys += len(open(file).read().split('\n'))
print("Total in SOURCE: " + str(len(source_file_list)) + " files, " + str(num_of_keys) + " keys")

# calculate the total number of files and keys in target
num_of_keys = 0
for file in target_file_list.values():
	num_of_keys += len(open(file).read().split('\n'))
print("Total in TARGET: " + str(len(target_file_list)) + " files, " + str(num_of_keys) + " keys")

# initialize values
num_of_different_files = 0
num_of_different_keys = 0
difference_result = ""

# find files existing in source/target but not the other
files_in_source_not_in_target = set(source_file_list.keys()) - set(target_file_list.keys())
if(files_in_source_not_in_target):
	difference_result += "Files exist in SOURCE but not in TARGET: \n"
	num_of_different_files += len(files_in_source_not_in_target)
	for file in files_in_source_not_in_target:
		difference_result += "    " + file
files_in_target_not_in_source = set(target_file_list.keys()) - set(source_file_list.keys())
if(files_in_target_not_in_source):
	difference_result += "\nFiles exist in TARGET but not in SOURCE: \n"
	num_of_different_files += len(files_in_target_not_in_source)
	for file in files_in_target_not_in_source:
		difference_result += "    " + file

difference_result += "\n\n>> DIFFERENCES:\n"
for file in source_file_list.keys():
	different = False
	if file in target_file_list.keys():		
		# convert .properties source file to dict
		source_content_dict = {}
		file_content = open(source_file_list[file]).read().split("\n")
		for line in file_content:
			if ((line.strip() != "") and (not line.strip().startswith("#")) and ("=" in line)):
				key_value = line.split("=")
				source_content_dict[key_value[0]] = key_value[1]

		# convert .properties target file to dict
		target_content_dict = {}
		file_content = open(target_file_list[file]).read().split("\n")
		for line in file_content:
			if ((line.strip() != "") and (not line.strip().startswith("#")) and ("=" in line)):
				key_value = line.split("=")
				target_content_dict[key_value[0]] = key_value[1]

		# find differences between two dictionaries
		d = DictDiffer(source_content_dict, target_content_dict, file)
		dict_difference = d.find_difference()
		difference_result += dict_difference[0]
		num_of_different_files += dict_difference[1]
		num_of_different_keys += dict_difference[2]
difference_result += "================================================================================================="

print("Difference: " + str(num_of_different_files) + " files, " + str(num_of_different_keys) + " keys\n")

print(difference_result)
wait = input("PRESS ENTER THREE TIMES TO EXIT")
wait = input()
wait = input()