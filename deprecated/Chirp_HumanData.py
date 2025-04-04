import asyncio
from pathlib import Path

from autoclean import Pipeline

# Define paths - modify these to match your system
EXAMPLE_OUTPUT_DIR = Path("/srv2/RAWDATA/Autoclean_Example_Chirp/output")  # Where processed data will be stored
CONFIG_FILE = Path("configs/autoclean_config.yaml")  # Path to config relative to this example

# Create output directory if it doesn't exist
EXAMPLE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def process_single_file():
    """Example of processing a single EEG file."""
    # Create pipeline instance
    pipeline = Pipeline(
        autoclean_dir=EXAMPLE_OUTPUT_DIR,
        autoclean_config=CONFIG_FILE,
        verbose='INFO'
    )
    
    # Example file path - modify this to point to your EEG file
    file_path = Path("C:/Users/Gam9LG/Documents/DATA/n141_resting/raw/0199_rest.raw")
    
    # Process the file
    pipeline.process_file(
        file_path=file_path,
        task="RestingEyesOpen",  # Choose appropriate task
    )

async def batch_process():
    """Example of batch processing multiple EEG files asynchronously."""
    # Create pipeline instance
    pipeline = Pipeline(
        autoclean_dir=EXAMPLE_OUTPUT_DIR,
        autoclean_config=CONFIG_FILE,
        verbose='INFO'
    )
    
    # Example directory path - modify this to point to your EEG files
    directory = Path("/srv2/RAWDATA/Autoclean_Example_Chirp/input")
    
    # Process all files in directory
    await pipeline.process_directory_async(
        directory=directory,
        task="ChirpDefault",  # Choose appropriate task
        sub_directories=False,
        max_concurrent=5
    )

if __name__ == "__main__":
    #print("Processing single file...")
    #process_single_file()
    
     #Uncomment to run batch processing
     print("Batch processing...")
     asyncio.run(batch_process())

