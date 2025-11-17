# How to Activate the Virtual Environment - Step by Step

## Step 1: Open PowerShell

1. Press `Windows Key + X` and select "Windows PowerShell" or "Terminal"
2. Or search for "PowerShell" in the Start menu
3. Navigate to your project folder:
   ```powershell
   cd "C:\Users\piron\OneDrive\Documents\AI Agents"
   ```

## Step 2: Activate the Virtual Environment

### Option A: Direct Activation (Try this first)
```powershell
.\venv\Scripts\Activate.ps1
```

### Option B: If you get an execution policy error

If you see an error like:
```
cannot be loaded because running scripts is disabled on this system
```

**Fix it by running this command first:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```powershell
.\venv\Scripts\Activate.ps1
```

### Option C: Alternative Activation Method

If PowerShell scripts are blocked, you can use:
```powershell
venv\Scripts\activate
```

## Step 3: Verify Activation

You should see `(venv)` at the beginning of your command prompt:
```
(venv) PS C:\Users\piron\OneDrive\Documents\AI Agents>
```

Also verify Python version:
```powershell
python --version
```
Should show: `Python 3.13.5`

## Alternative: Using Command Prompt (CMD)

If PowerShell doesn't work, you can use Command Prompt:

1. Open Command Prompt (cmd.exe)
2. Navigate to your project:
   ```cmd
   cd "C:\Users\piron\OneDrive\Documents\AI Agents"
   ```
3. Activate:
   ```cmd
   venv\Scripts\activate.bat
   ```

You should see `(venv)` in your prompt.

## Troubleshooting

### Issue: "The term '.\venv\Scripts\Activate.ps1' is not recognized"

**Solution:** Make sure you're in the correct directory:
```powershell
pwd  # Check current directory
# Should show: C:\Users\piron\OneDrive\Documents\AI Agents
```

### Issue: "Execution Policy" error

**Solution:** Run this command (you only need to do this once):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Type `Y` when prompted, then try activating again.

### Issue: Virtual environment not found

**Solution:** Make sure the venv folder exists:
```powershell
Test-Path .\venv\Scripts\Activate.ps1
# Should return: True
```

If it returns False, the virtual environment might not be created. Create it:
```powershell
py -3.13 -m venv venv
```

## Quick Reference

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**Git Bash:**
```bash
source venv/Scripts/activate
```

## After Activation

Once activated, you can:
1. Run the agent: `python main.py --name "Test Customer"`
2. Install packages: `pip install package_name`
3. Check installed packages: `pip list`

## Deactivating

When you're done, deactivate the environment:
```powershell
deactivate
```

