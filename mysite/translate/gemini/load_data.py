import google.generativeai as genai
import json


def load_file_content(file_path: str) -> str:
	with open(file_path, "r") as f:
		content = f.read()
		
	return content
	
def load_data_from_manifest(manifest_file: str) -> list[dict[str, str]]:
	with open(manifest_file, "r") as f:
		manifest = json.load(f)
	
	data = []

	for entry in manifest:
		js_content = load_file_content(entry["javascript"])
		ts_content = load_file_content(entry["typescript"])
		
		data.append({"text_input": js_content, "output": ts_content})
	
	return data

def create_trained_model(id: str) -> None:
	training_data = load_data_from_manifest("training.json")

	genai.create_tuned_model(
		id=id,
		source_model="models/gemini-1.0-pro-001",
		training_data=training_data,
		batch_size=16,
		epoch_count=100,
	)
	
	print(genai.get_tuned_model("tunedModels/" + id))
