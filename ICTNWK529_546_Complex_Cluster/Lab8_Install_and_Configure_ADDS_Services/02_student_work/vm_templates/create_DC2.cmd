@echo off
rem Creates the DC2 virtual machine folder and 60 GB disk, then opens it in VMware Workstation.
rem Edit VMDIR if you want the VM somewhere else (keep it OUT of OneDrive).
set "VMDIR=D:\Lab8-VMs\DC2"
set "VDM=C:\Program Files (x86)\VMware\VMware Workstation\vmware-vdiskmanager.exe"
set "VMW=C:\Program Files (x86)\VMware\VMware Workstation\vmware.exe"
if not exist "%VDM%" set "VDM=C:\Program Files\VMware\VMware Workstation\vmware-vdiskmanager.exe"
if not exist "%VMW%" set "VMW=C:\Program Files\VMware\VMware Workstation\vmware.exe"
if not exist "%VDM%" (echo vmware-vdiskmanager.exe not found - is Workstation Pro installed? & pause & exit /b 1)
if exist "%VMDIR%\DC2.vmdk" (echo %VMDIR%\DC2.vmdk already exists - nothing done. & pause & exit /b 1)
mkdir "%VMDIR%" 2>nul
echo Creating 60 GB growable disk %VMDIR%\DC2.vmdk ...
"%VDM%" -c -s 60GB -a lsilogic -t 0 "%VMDIR%\DC2.vmdk"
if errorlevel 1 (echo Disk creation failed. & pause & exit /b 1)
copy /y "%~dp0DC2.vmx" "%VMDIR%\DC2.vmx" >nul
echo.
echo DC2 created in %VMDIR%. Opening it in Workstation (do not power on until you have checked VM ^> Settings).
start "" "%VMW%" "%VMDIR%\DC2.vmx"
pause
