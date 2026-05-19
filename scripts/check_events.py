import subprocess
import json
import sys

def get_recent_errors():
    try:
        # Query Windows Event Viewer for Application errors (Level=2) from the last hour
        cmd = [
            "powershell",
            "-Command",
            "Get-WinEvent -FilterHashtable @{LogName='Application'; Level=2} -MaxEvents 5 | Select-Object TimeCreated, Id, ProviderName, Message | ConvertTo-Json"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if not result.stdout.strip():
            print("No recent application errors found in the Event Log.")
            return

        events = json.loads(result.stdout)
        if isinstance(events, dict):
            events = [events]
            
        print("=== RECENT WINDOWS APPLICATION ERRORS ===")
        for e in events:
            print(f"\nTime: {e.get('TimeCreated')}")
            print(f"Provider: {e.get('ProviderName')}")
            print(f"Event ID: {e.get('Id')}")
            print(f"Message: {e.get('Message')}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Failed to query event log: {e}")

if __name__ == "__main__":
    get_recent_errors()
