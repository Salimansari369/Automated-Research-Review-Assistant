import os
import sys
import urllib.request
import zipfile
import subprocess

def download_and_setup_git():
    dest_dir = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git")
    os.makedirs(dest_dir, exist_ok=True)
    
    zip_path = os.path.expandvars(r"%TEMP%\MinGit.zip")
    url = "https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/MinGit-2.47.1-64-bit.zip"
    
    print(f"Downloading portable Git from {url}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
        out_file.write(response.read())
        
    print(f"Extracting Git to {dest_dir}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)
        
    git_cmd_dir = os.path.join(dest_dir, "cmd")
    git_exe = os.path.join(git_cmd_dir, "git.exe")
    
    print("Testing Git execution...")
    res = subprocess.run([git_exe, "--version"], capture_output=True, text=True)
    print("Git Output:", res.stdout.strip())
    
    # Add to current process PATH and user PATH
    os.environ["PATH"] = git_cmd_dir + os.pathsep + os.environ.get("PATH", "")
    
    # Update Windows User PATH via setx or powershell
    try:
        subprocess.run(
            ["powershell", "-Command", f"[Environment]::SetEnvironmentVariable('Path', '{git_cmd_dir};' + [Environment]::GetEnvironmentVariable('Path', 'User'), 'User')"],
            check=True
        )
        print("Successfully added Git to User PATH!")
    except Exception as e:
        print("Path update notice:", e)
        
    return git_exe

if __name__ == "__main__":
    download_and_setup_git()
