# openHAB-snap

openHAB packaged as a snap. It consists of:
  - java runtime (21)
  - openHAB run time

## How to install

This openHAB snap is available in the Ubuntu store. Install via:

$ snap install openhab

## How to use

After install, assuming you and the device on which it was installed are on the same network, you should be able to reach the openHAB interface by visiting `<device address>`:8080 in your browser.
Port on which web interface is exposed can be configured. For more help run $ openhab.help

For more information about openHAB refer to http://www.openhab.org

## Building openHAB Snap

### Method 1: Snapcraft with Automatic Container Management (Recommended)

Use this method when running on a host system where snapcraft can manage containers automatically:

```bash
# Install dependencies
snap install snapcraft --classic
snap install multipass --classic  # Fallback backend

# Clone and build
git clone https://github.com/openhab/openhab-snap.git
cd openhab-snap
snapcraft  # Snapcraft will automatically create and manage build containers
```

### Method 2: Manual LXC Container (Nested/Restricted Environments)

Use this method when snapcraft cannot manage containers (e.g., inside existing containers, restricted environments):

**Prerequisites:**
- LXC/LXD installed and configured
- Sufficient disk space
- Understanding of basic Linux commands

**Steps:**

1. **Container Setup:**
   ```bash
   lxc launch ubuntu:22.04/arm64 openhab-arm64  # Launch ARM64 build container
   lxc exec openhab-arm64 bash
   ```

2. **Install Dependencies:**
   ```bash
   apt update && apt install -y rpm xmlto bzip2
   snap install snapcraft --classic
   ```

3. **Clone and Build:**
   ```bash
   git clone https://github.com/openhab/openhab-snap.git
   cd openhab-snap
   snapcraft --destructive-mode  # Builds directly in current environment
   ```

4. **Transfer and Install (on Host):**
   ```bash
   exit  # Exit container
   lxc file pull openhab-arm64/root/openhab-snap/openhab_*.snap .
   snap stop openhab  # Stop existing instance if any
   snap install --dangerous openhab_*.snap
   ```

**Notes:**
- **Method 1**: Snapcraft manages containers automatically, provides cleaner isolation
- **Method 2**: Required when LXC nesting is unavailable or snapcraft lacks container privileges  
- Use `--destructive-mode` only when snapcraft cannot create its own build environment
- The `--dangerous` flag is needed because the snap is not from the official store
- For different architectures, adapt the image tag (e.g., `ubuntu:22.04/amd64`) and use the appropriate platform, cross-compilation is not supported with snapcraft.
