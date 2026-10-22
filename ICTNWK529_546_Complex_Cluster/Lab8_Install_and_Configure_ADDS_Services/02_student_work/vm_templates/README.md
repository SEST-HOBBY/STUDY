# VM templates for DC1 and DC2 (2026-10-22)

Two files per VM: `<name>.vmx` (the VM definition, same hardware as the 2025 DC2 VM but 4 GB RAM, a
SAS disk, the Server 2019 ISO attached and a bridged NIC) and `create_<name>.cmd` (makes the folder
`D:\Lab8-VMs\<name>`, creates the empty 60 GB disk with vmware-vdiskmanager, copies the .vmx in and opens
it in Workstation).

Use: copy `DC1.vmx` and `create_DC1.cmd` to the SB computer, double-click `create_DC1.cmd`. Same with the
DC2 pair on the MG computer. Then in Workstation: VM > Settings (confirm 4096 MB, 2 CPUs, CD/DVD = the ISO,
Network Adapter = Bridged), VM > Snapshot > Take Snapshot "0-empty", then Power on and install Windows
(walkthrough section E).

If the VM folder should be elsewhere, edit the `set "VMDIR=..."` line first. If the ISO is not at
`E:\OS ISO Files\Windows Server 2019\...199664ce.iso`, Workstation says so at power-on: VM > Settings >
CD/DVD > Browse to it. Hardware version 18 opens in Workstation/Player 16.1 and later; decline any upgrade
offer so both PCs stay compatible.
