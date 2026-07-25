import sys
import os

# Add root folder to sys.path so we can import utils.logging_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from utils.logging_utils import get_logger

def main():
    logger = get_logger("SandboxTest")
    print("--- Test Started ---")
    logger.info("Testing custom system logging: INFO level")
    logger.warning("Testing custom system logging: WARNING level")
    logger.error("Testing custom system logging: ERROR level")
    print("--- Test Finished ---")
    
    # Verify file content
    log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage", "log", "app.log"))
    print(f"Checking log file at: {log_file_path}")
    if os.path.exists(log_file_path):
        print("Log file exists! Reading last few lines:")
        with open(log_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-3:]:
                print(f"  [File] {line.strip()}")
    else:
        print("Log file NOT found!")

if __name__ == "__main__":
    main()
