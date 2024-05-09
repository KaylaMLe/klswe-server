import google.generativeai as genai
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def evaluate_tuned_model(id: str) -> None:
	model = genai.get_tuned_model("tunedModels/" + id)
	snapshots = pd.DataFrame(model.tuning_task.snapshots)
	sns.lineplot(data=snapshots, x="epoch", y="mean_loss")
	plt.show()

def check_model(id: str) -> None:
	model = genai.get_tuned_model("tunedModels/" + id)
	print(model)

def test_prompt(id: str) -> None:
	model = genai.GenerativeModel(model_name="tunedModels/" + id)
	javascript_code = """
	// Define a function to create a person object
	function createPerson(name, age, isStudent) {
		return {
			name,
			age,
			isStudent,
		};
	}

	// Define a function to get the type of a variable
	function getType(variable) {
		return typeof variable;
	}

	// Define a function to perform addition
	function add(a, b) {
		return a + b;
	}

	// Define a function to concatenate strings
	function concatenateStrings(a, b) {
		return a + b;
	}

	// Main function
	function main() {
		// Create a person object
		const person = createPerson('John', 25, true);

		// Print person details
		console.log('Person:', person);

		// Perform addition
		const sum = add(5, 3);
		console.log('Sum:', sum);

		// Concatenate strings
		const concatenatedString = concatenateStrings('Hello, ', 'world!');
		console.log('Concatenated String:', concatenatedString);

		// Get type of variables
		console.log('Type of person:', getType(person));
		console.log('Type of sum:', getType(sum));
		console.log('Type of concatenatedString:', getType(concatenatedString));
	}

	// Call the main function
	main();
	"""
	typescript_translation = model.generate_content(javascript_code)

	print(">>> Original JavaScript <<<\n")
	print(javascript_code)
	print("\n>>> TypeScript Translation <<<\n")
	print(typescript_translation.text)

if __name__ == "__main__":
	test_prompt("js-to-ts-model-001")