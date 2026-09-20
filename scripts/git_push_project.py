import os
import subprocess

def run_git_operations():
    git_cmd_dir = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\cmd")
    git_exe = os.path.join(git_cmd_dir, "git.exe")
    if not os.path.exists(git_exe):
        git_exe = "git"
        
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    def run_cmd(args):
        cmd = [git_exe] + args
        print(f"> {' '.join(cmd)}")
        res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        if res.stdout:
            print(res.stdout.strip())
        if res.stderr:
            print("[stderr]:", res.stderr.strip())
        return res

    print("--- 1. Git Init ---")
    run_cmd(["init"])
    
    # Configure user name / email if not set
    run_cmd(["config", "user.name", "Salim Ansari"])
    run_cmd(["config", "user.email", "salimansari369@users.noreply.github.com"])
    
    print("\n--- 2. Git Add ---")
    run_cmd(["add", "."])
    
    print("\n--- 3. Git Commit ---")
    run_cmd(["commit", "-m", "feat: Automated Literature Review Assistant with Agentic AI, Whisper STT, and Dual Themes"])
    
    print("\n--- 4. Set Main Branch ---")
    run_cmd(["branch", "-M", "main"])
    
    print("\n--- 5. Add Remote ---")
    run_cmd(["remote", "remove", "origin"])
    run_cmd(["remote", "add", "origin", "https://github.com/Salimansari369/Automated-Research-Review-Assistant.git"])
    
    print("\n--- 6. Git Status ---")
    run_cmd(["status"])

if __name__ == "__main__":
    run_git_operations()
