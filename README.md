
# SSH IP Filtering and DHCP Cleanup Script

This Python script performs the following tasks:
1. Connects to multiple servers via SSH to retrieve a list of IP addresses using the command `diagnose firewall auth list`.
2. Filters a specified IP range, excluding the IPs retrieved from the servers.
3. Executes DHCP lease cleanup commands on the servers based on the filtered IP ranges.

## Prerequisites

- Python 3.x installed on your system.
- The `paramiko` library for SSH communication.
- Threading support for parallel execution.

Install the required library with:
```bash
pip install paramiko
```

## Usage

1. **Update Server Details**:
   Modify the `servers` list in the script with the appropriate hostname, username, and password:
   ```python
   servers = [
       {"hostname": "10.0.0.1", "username": "admin", "password": "password"},
       # Add more servers as needed
   ]
   ```

2. **Specify IP Range**:
   Update the `start_ip` and `end_ip` variables to define the range you want to filter:
   ```python
   start_ip = "192.168.160.10"
   end_ip = "192.168.167.254"
   ```

3. **Run the Script**:
   Execute the script:
   ```bash
   python script_name.py
   ```

4. **Output**:
   - Prints the extracted IP addresses from the servers.
   - Displays the filtered IP ranges.
   - Executes the DHCP lease cleanup commands for the filtered IP ranges.

## Features

- Connects to multiple servers via SSH in parallel using threading.
- Filters IP ranges dynamically without using temporary files.
- Sends DHCP cleanup commands to the servers.

## Script Flow

1. **Extract IP Addresses**:
   - Connects to each server and retrieves IP addresses based on the command output.
   - Uses regex to extract valid IPs.

2. **Generate Filtered Ranges**:
   - Excludes the retrieved IPs from a specified range.
   - Supports IP range splitting and output in contiguous blocks.

3. **Execute Commands**:
   - Sends DHCP cleanup commands for each filtered IP or IP range.

## Example Output

```
Direcciones IP extraídas: ['192.168.160.12', '192.168.160.15']
Rangos filtrados generados:
192.168.160.10-192.168.160.11
192.168.160.13-192.168.160.14
192.168.160.16-192.168.167.254
```

## Customization

- Modify the `base_command` variable to change the DHCP cleanup command:
  ```python
  base_command = "execute dhcp lease-clear"
  ```

- Add more servers to the `servers` list as needed.

## Notes

- Ensure the user account used has sufficient permissions to execute the SSH commands on the servers.
- The script does not save any data to files; all processing is done in-memory.

## License

This script is provided under the MIT License. Feel free to use and modify it as needed.
