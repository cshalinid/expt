import os

# Specify the paths where you want to save the dataset and index
dataset_path = "C:\\expt\\HuggingFace\\hfenv\\src\\datasetpath\\"
index_path = "C:\\expt\\HuggingFace\\hfenv\\src\\indexpath\\"

# Create a test file content
test_content = "This is a test file to check permissions."

try:
    # Create the dataset folder if it doesn't exist
    os.makedirs(dataset_path, exist_ok=True)

    # Create the index folder if it doesn't exist
    os.makedirs(index_path, exist_ok=True)

    # Create and save a test file in the dataset folder
    with open(os.path.join(dataset_path, "test.txt"), "w") as test_file:
        test_file.write(test_content)

    # Create and save a test file in the index folder
    with open(os.path.join(index_path, "test.txt"), "w") as test_file:
        test_file.write(test_content)

    print("Permissions test successful. You have write access to the specified folders.")
except Exception as e:
    print(f"Permissions test failed: {str(e)}")
