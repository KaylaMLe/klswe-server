import json
import os


# Get a list of all files in the training directory
files = os.listdir("./training")

# Filter out the .js and .jsx files
js_files = [f for f in files if f.endswith(".js") or f.endswith(".jsx")]

# Create a dictionary to hold the file mappings
file_mappings = []

# For each .js/.jsx file, add a mapping to the corresponding .ts/.tsx file
for js_file in js_files:
	# Get the base name of the file (without the extension)
	base_name = os.path.splitext(js_file)[0]

	# Determine the corresponding .ts/.tsx file name
	ts_file = base_name + ".ts" if js_file.endswith(".js") else base_name + ".tsx"

	file_mappings.append({
		"javascript": f"./training/{js_file}",
		"typescript": f"./training/{ts_file}"
	})

# Write the dictionary to a JSON file
with open("training.json", "w") as f:
	json.dump(file_mappings, f, indent=2)
