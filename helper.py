import os
import re

reference_dirs = ["src/main/java"]


# Step 1: Parse Java Files to Identify Linked Files
def find_imports_and_references(file_path):
    linked_files = set()
    
    with open(file_path, 'r') as file:
        content = file.read()
        
        # Find imports
        import_pattern = re.compile(r'import\s+([\w\.]+);')
        imports = import_pattern.findall(content)
        # print(f"[@] imports -> {imports}")
        
        # Find class and method references
        class_reference_pattern = re.compile(r'\b([A-Z][a-zA-Z0-9_]+)\b')
        class_references = class_reference_pattern.findall(content)
        # print(f"\n[@] class -> {class_references}")

        # Collect all unique references
        linked_files.update(imports)
        linked_files.update(class_references)
    # print(f"\n[@] links -> {linked_files}")
    return linked_files


def resolve_file_paths(project_dir, references):
    file_paths = set()
    for reference in references:
        # Convert package reference to a relative file path
        reference_path = reference.replace('.', os.sep) + '.java'
        # Walk through the directory tree to find the correct file
        for root in reference_dirs:
            root = os.path.join(project_dir, root)
            potential_path = os.path.join(root, reference_path)
            if os.path.exists(potential_path):
                file_paths.add(potential_path)
                break  # Stop searching once the file is found
    return file_paths


def find_linked_files(start_file, project_dir):
    linked_files = find_imports_and_references(start_file)
    linked_file_paths = resolve_file_paths(project_dir, linked_files)
    
    all_files = set(linked_file_paths)
    
    # Recursively find linked files
    for file_path in linked_file_paths:
        all_files.update(find_linked_files(file_path, project_dir))
    # print(f"[@] all files {all_files}")
    return all_files


# Step 2: Prepare Prompt for Ollama API
def prepare_context(linked_files):
    context = ""
    for file_path in linked_files:
        with open(file_path, 'r') as file:
            context += f"File: {file_path}\n"
            context += file.read() + "\n\n"
    
    return context
