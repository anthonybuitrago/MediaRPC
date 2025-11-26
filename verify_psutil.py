import utils
import sys

print("Testing is_process_running with 'python'...")
# We are running python, so it should be True
if utils.is_process_running("python.exe") or utils.is_process_running("python"):
    print("✅ Python detected")
else:
    print("❌ Python NOT detected")

print("Testing is_process_running with 'non_existent_process_12345'...")
if not utils.is_process_running("non_existent_process_12345"):
    print("✅ Non-existent process correctly NOT detected")
else:
    print("❌ False positive on non-existent process")
