
from .telemetry import send_telemetry
from .utils import load_action_engine, load_instructions
from .command_center import CommandCenter
from defaults import default_get_playwright_driver
import os
import argparse
import importlib.util
from pathlib import Path
from tqdm import tqdm
import inspect

import warnings
warnings.filterwarnings("ignore")


def import_from_path(path):
    # Convert the path to a Python module path
    module_name = Path(path).stem
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def build():
    parser = argparse.ArgumentParser(description='Process a file.')
    parser.add_argument('--file_path', type=str, required=True, help='the path to the file')
    parser.add_argument('--config_path', type=str, required=True, help='the path to the Python config file')
    args = parser.parse_args()
    file_path = args.file_path
    config_path = args.config_path

    action_engine, page, browser = load_action_engine(config_path, streaming=False, get_driver=default_get_playwright_driver)

    base_url, instructions = load_instructions(file_path)
    page.goto(base_url)
    output = f"page.goto('{base_url.strip()}')\n"

    template_code = """\n########################################\n# Query: {instruction}\n# Code:\n{code}"""

    file_path = os.path.basename(file_path)
    file_path, _ = os.path.splitext(file_path)
    config_path = os.path.basename(config_path)
    config_path, _ = os.path.splitext(config_path)
    output_fn = file_path + "_" + config_path + ".py"

    for instruction in tqdm(instructions):
        print(f"Processing instruction: {instruction}")
        html = page.content()
        code, source_nodes = action_engine.get_action(instruction, html)
        try:
            exec(code)
        except Exception as e:
            print(f"Error in code execution: {code}")
            print("Error:", e)
            print(f"Saving output to {output_fn}")
            with open(output_fn, "w") as file:
                file.write(output)
            break
        output += "\n" + template_code.format(instruction=instruction, code=code).strip()
        send_telemetry(action_engine.llm.metadata.model_name, code, b"", html, source_nodes, instruction, base_url, "Lavague-build")

    print(f"Saving output to {output_fn}")
    with open(output_fn, "w") as file:
        file.write(output)

    browser.close()
    
def launch():
    parser = argparse.ArgumentParser(description='Process a file.')
    parser.add_argument('--file_path', type=str, required=True, help='the path to the file')
    parser.add_argument('--config_path', type=str, required=True, help='the path to the Python config file')
    args = parser.parse_args()
    file_path = args.file_path
    config_path = args.config_path

    action_engine, page, browser = load_action_engine(config_path, streaming=True, get_driver=default_get_playwright_driver)

    base_url, instructions = load_instructions(file_path)
    command_center = CommandCenter(action_engine, page, browser)
    command_center.run(base_url, instructions)

    browser.close()