import os
import tempfile
import subprocess


def generate_and_obfuscate_script(server_url, salt):
    # Original Python script with placeholders
    with open("generated_client.py", "r") as fp:
        original_script = fp.read()

    # Replace placeholders with provided parameters
    script_with_values = original_script.replace('>>>SERVER_URL<<<', f'"{server_url}"').replace('>>>SALT<<<',
                                                                                                f'"{salt}"')

    # Create a temporary directory to store the script
    with tempfile.TemporaryDirectory() as temp_dir:
        script_path = os.path.join(temp_dir, 'script.py')

        # Write the modified script to a temporary file
        with open(script_path, 'w') as script_file:
            script_file.write(script_with_values)

        # Compile the script using python -OO -m py_compile
        try:
            subprocess.run(['python', '-OO', '-m', 'py_compile', script_path], check=True)

            # Get the path of the compiled .pyo file
            compiled_path = script_path + 'o'

            # Read the compiled bytecode file
            with open(compiled_path, 'rb') as compiled_file:
                compiled_code = compiled_file.read()

            return compiled_code  # Return the compiled bytecode

        except subprocess.CalledProcessError as e:
            print(f"Error during compilation: {e}")
            return None

