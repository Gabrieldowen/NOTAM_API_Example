#!/bin/bash

# Remove the output JSON file(s)
echo "Removing output JSON files..."
rm -f TestData/TestNOTAM.json

# Optionally, remove all JSON files in the directory if needed
# rm -f /path/to/your/TestData/*.json

echo "Output JSON files removed."

# Stop all running processes related to your application
# This example uses `pkill` to match processes by a name pattern
# Replace 'your_process_name' with the actual name or pattern of your processes
echo "Stopping all running processes related to the application..."
pkill -f your_process_name

echo "All related processes stopped."

# End of script
