import os
import json
import sys
from persona_analyser import process_document_collection
from outline_extractor import get_document_sections_from_outline

# These paths match the required docker run command
INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def main():
    # Create the output directory inside the container
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Define the path for the main input file
    challenge_input_path = os.path.join(INPUT_DIR, "challenge1b_input.json")
    
    # Check if the required input file exists
    if not os.path.exists(challenge_input_path):
        print(f"Error: 'challenge1b_input.json' not found in {INPUT_DIR}", file=sys.stderr)
        sys.exit(1)

    print("--- Processing document collection for Round 1B ---")
    
    # Read the input JSON
    with open(challenge_input_path, 'r', encoding='utf-8') as f:
        challenge_input = json.load(f)
    
    # Call the main processing function. The PDF directory is now the main INPUT_DIR.
    output_data = process_document_collection(challenge_input, get_document_sections_from_outline, INPUT_DIR)
    
    # Define the output path and save the results
    output_path = os.path.join(OUTPUT_DIR, "challenge1b_output.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
        
    print(f"-> Success: Output saved to 'challenge1b_output.json'")

if __name__ == "__main__":
    main()