# openHAB-snap

openHAB packaged as a snap. It consists of:
  - java runtime (zulu 8)
  - openHAB run time

## How to install

This openHAB snap is available in the Ubuntu store. Install via:

$ snap install openhab

## How to use

After install, assuming you and the device on which it was installed are on the same network, you should be able to reach the openHAB interface by visiting `<device address>`:8080 in your browser.
Port on which web interface is exposed can be configured. For more help run $ openhab.help

For more information about openHAB refer to http://www.openhab.org


## Building OpenHAB Snap for ARM64 within LXC/LXD

This guide outlines the steps to build an OpenHAB SNAP package for ARM64 architecture within an LXC/LXD container. The same procedure works for amd64 assuming the lxc container is on amd64.

**Prerequisites:**

* LXC/LXD installed and configured.
* Sufficient disk space.
* Understanding of basic Linux commands.

**Steps:**

1. **Container Setup:**

   ```bash
   lxc launch ubuntu:22.04/arm64 openhab-arm64 # Launch the ARM64 build container
   lxc exec openhab-arm64 bash
   ```

2. **Install Dependencies:**

   In the container :
   ```bash
   apt update && apt install -y rpm xmlto bzip2  # Install required build tools
   snap install snapcraft --classic              # Install Snapcraft
   snap install multipass --classic            # Install Multipass (needed for some build steps)
   ```

3. **Clone and Prepare OpenHAB Snap Repository:**

   ```bash
   git clone https://github.com/openhab/openhab-snap.git
   cd openhab-snap
   git checkout
   ```

4. **Build the OpenHAB Snap:**

   ```bash
   snapcraft --destructive-mode  # Initiate the SNAP build process.
   ```

5. **Transfer and Install the SNAP (Host Machine):**

   * **Exit the Container:** `exit`
   * **Pull the SNAP file:** `lxc file pull openhab-arm64/root/openhab-snap/openhab_5.1.0-SNAPSHOT-bn4770_arm64.snap .`
   * **Stop the existing OpenHAB instance (if any):** `snap stop openhab`
   * **Install the newly built SNAP:** `snap install --dangerous openhab_5.1.0-SNAPSHOT-bn4770_arm64.snap`

**Important Notes:**

*  `--destructive-mode` rebuilds from scratch, ensuring a clean build.
*  Adjust the `openhab_5.1.0-SNAPSHOT-bn4770_arm64.snap` filename to match the actual generated file name.
*  The `--dangerous` flag is needed because the SNAP is not from the official SNAP store.
*  This guide focuses on building a SNAP for ARM64. Adapt the image tag (`ubuntu:22.04/arm64`) if you need a different architecture.
*  Comments regarding `lxd init`, `uidmap`, `usermod`, and  `snap install lxd` are no longer needed in this streamlined process.
