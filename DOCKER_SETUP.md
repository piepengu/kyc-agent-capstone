# Docker Desktop Setup Guide

## What You Need

Yes, you need **Docker Desktop** (not just a plugin) to build and run Docker containers locally.

## Step-by-Step Installation

### Step 1: Download Docker Desktop

1. Go to: https://www.docker.com/products/docker-desktop/
2. Click **"Download for Windows"**
3. The installer will download (`Docker Desktop Installer.exe`)

### Step 2: Install Docker Desktop

1. **Run the installer** (`Docker Desktop Installer.exe`)
2. **Enable WSL 2** (if prompted):
   - Docker Desktop requires WSL 2 (Windows Subsystem for Linux 2)
   - If not installed, the installer will guide you
   - You may need to restart your computer
3. **Follow the installation wizard**:
   - Accept the license agreement
   - Choose installation location (default is fine)
   - Check "Use WSL 2 instead of Hyper-V" (recommended)
   - Click "Install"
4. **Restart your computer** if prompted

### Step 3: Start Docker Desktop

1. **Launch Docker Desktop** from Start Menu
2. **Accept the service agreement** when it starts
3. **Wait for Docker to start** (whale icon in system tray)
4. **Sign in** (optional, but recommended):
   - Create a free Docker Hub account at https://hub.docker.com/
   - Sign in through Docker Desktop

### Step 4: Verify Installation

Open PowerShell and run:

```powershell
# Check Docker version
docker --version

# Check Docker is running
docker info

# Test with a simple container
docker run hello-world
```

**Expected Output:**
```
Docker version 24.x.x, build ...
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

### Step 5: Configure Docker Desktop (Optional)

1. **Open Docker Desktop Settings** (gear icon)
2. **Resources**:
   - Allocate at least 2GB RAM (4GB recommended)
   - Allocate at least 2 CPU cores
3. **General**:
   - Enable "Start Docker Desktop when you log in" (optional)
   - Enable "Use the WSL 2 based engine" (if available)

## Troubleshooting

### Issue: "Docker Desktop requires WSL 2"

**Solution:**
1. Install WSL 2:
   ```powershell
   wsl --install
   ```
2. Restart your computer
3. Update WSL 2:
   ```powershell
   wsl --update
   ```

### Issue: "Docker daemon is not running"

**Solution:**
1. Make sure Docker Desktop is running (check system tray)
2. If not running, start Docker Desktop from Start Menu
3. Wait for the whale icon to appear in system tray

### Issue: "Cannot connect to Docker daemon"

**Solution:**
1. Restart Docker Desktop
2. Check if WSL 2 is enabled:
   ```powershell
   wsl --status
   ```
3. Restart your computer if needed

## Testing Docker with KYC Bot

Once Docker Desktop is installed and running:

```powershell
# Navigate to project directory
cd "C:\Users\piron\OneDrive\Documents\AI Agents"

# Build the Docker image
docker build -t kyc-bot:test .

# Run the container (API server mode)
docker run -d --name kyc-bot-test --env-file .env -p 8080:8080 kyc-bot:test

# Test it
Invoke-WebRequest -Uri http://localhost:8080/health -Method GET

# View logs
docker logs kyc-bot-test

# Stop and remove
docker stop kyc-bot-test
docker rm kyc-bot-test
```

## Resources

- [Docker Desktop Documentation](https://docs.docker.com/desktop/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- [WSL 2 Installation Guide](https://learn.microsoft.com/en-us/windows/wsl/install)

