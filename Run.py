import os
import subprocess
import sys
import tomllib


def run_endpoint(endpoint, port, toml_file):
    endpoint_file = f"{endpoint}.Endpoint"
    if os.path.exists(f"{endpoint}\\Endpoint.py"):
        # Execute the Endpoint.py script with the port as an argument
        process = (
            subprocess.Popen([sys.executable, "-m", endpoint_file, str(port), toml_file], shell=True))
        return process
    else:
        print(f"Endpoint script for {endpoint} not found at {endpoint_file}.")

# def run_client():
#     endpoint_file = f"{endpoint}.Endpoint"
#     if os.path.exists(f"{endpoint}\\Endpoint.py"):
#         # Execute the Endpoint.py script with the port as an argument
#         process = (
#             subprocess.Popen([sys.executable, "-m", endpoint_file, str(port), toml_file], shell=True))
#         return process
#     else:
#         print(f"Script for client not found at {endpoint_file}.")


def main(toml_file):
    processes = []

    try:
        with open(toml_file, "rb") as toml:
            config = tomllib.load(toml)
    except Exception as e:
        print(f"Error loading TOML file: {e}")
        sys.exit(1)

    # Fetch the endpoints to run
    endpoints_to_run = config.get("EndpointToRun", [])

    # Check for the RunClient flag (if needed later)
    run_client = config.get("RunClient", False)

    # Iterate over each endpoint and run its script with the specified port
    for endpoint in endpoints_to_run:
        # Get the endpoint's configuration
        endpoint_config = config.get(endpoint)

        if endpoint_config:
            port = endpoint_config.get("Port")
            if port:
                print(f"Running {endpoint} on port {port}")
                process = run_endpoint(endpoint, port, toml_file)
                processes.append((endpoint, process))
            else:
                print(f"Port not specified for {endpoint}")
        else:
            print(f"No configuration found for {endpoint}")

    # if run_client:

    for endpoint, process in processes:
        stdout, stderr = process.communicate()  # Capture output if needed
        print(f"{endpoint} finished running.")
        if stderr:
            print(f"Error in {endpoint}: {stderr.decode()}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run.py <config_file.toml>")
        sys.exit(1)

    toml_file_path = sys.argv[1]
    main(toml_file_path)
