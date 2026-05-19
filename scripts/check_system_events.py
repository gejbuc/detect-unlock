import subprocess
import json

def get_system_errors():
    try:
        # Check System log for Critical (Level 1) or Error (Level 2) events
        cmd = [
            "powershell",
            "-Command",
            "Get-WinEvent -FilterHashtable @{LogName='System'; Level=1,2} -MaxEvents 10 | Select-Object TimeCreated, Id, ProviderName, Message | ConvertTo-Json"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if not result.stdout.strip():
            print("No recent system errors found.")
            return

        events = json.loads(result.stdout)
        if isinstance(events, dict):
            events = [events]
            
        print("=== RECENT WINDOWS SYSTEM CRASHES/ERRORS ===")
        for e in events:
            print(f"\nTime: {e.get('TimeCreated')}")
            print(f"Provider: {e.get('ProviderName')}")
            print(f"Event ID: {e.get('Id')}")
            print(f"Message: {e.get('Message')}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Failed to query event log: {e}")

if __name__ == "__main__":
    get_system_errors()
