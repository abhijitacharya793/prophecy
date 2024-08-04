import re
import glob
import click
from os.path import isfile

from helper import find_linked_files, prepare_context
from constants import template, path_example, prompt_get_controller_path, prompt_get_curl_commands
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="codeqwen:7b")


# Usage:
# python main.py predict C:\Users\Abhijit\Documents\Security\Repository\spring-boot-tutorial\springboot2-jpa-h2-crud-example/

@click.command()
@click.argument("project_dir", type=click.STRING)
def predict(project_dir):
    print(f"[@] Getting the APIs for project: {project_dir}")
    # get all files and identify all potential controllers
    all_files = []

    for i in range(0, 12):
        all_files += glob.glob(f"{project_dir}{'*/' * i}*.java")

    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | model
    result = chain.invoke(
        {
            "context": "\n".join(all_files) + path_example,
            "question": prompt_get_controller_path
        }
    )
    result = re.sub(r'(\d+\.\s*|- |```|\* |`)', '', result)

    print(f"[@] \n{result}")
    # Get each controller and add the curl commands to the curls array
    curl_commands = []

    for start_file in result.split("\n"):
        if isfile(start_file):
            linked_files = find_linked_files(start_file, project_dir)
            linked_files.add(start_file)
            # print(f"[@] linked files: \n {linked_files}")

            context = prepare_context(linked_files)

            api_details = chain.invoke(
                {
                    "context": context,
                    "question": prompt_get_curl_commands
                }
            )
            api_details = re.sub(r'(\d+\.\s*|- |```)', '', api_details)
            if api_details:
                for line in api_details.split("\n"):
                    if "curl " in line:
                        curl_commands.append(line)

            if len(curl_commands) > 0:
                print("[@] Extracted API Details:\n")
                for curl in curl_commands:
                    print(f"\t{curl}")
            else:
                print("[>] Failed to extract API details.")
