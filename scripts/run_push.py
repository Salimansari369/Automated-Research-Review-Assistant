import os
import subprocess

def push_to_github():
    git_exe = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\cmd\git.exe")
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("Executing git push...")
    try:
        res = subprocess.run([git_exe, "push", "-u", "origin", "main"], cwd=cwd, text=True)
        print("Exit code:", res.returncode)
    except Exception as e:
        print("Push error:", e)

if __name__ == "__main__":
    push_to_github()
