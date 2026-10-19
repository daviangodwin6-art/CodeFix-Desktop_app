; Inno Setup script for the CodeFix desktop app. Build after `pyinstaller codefix.spec`:
;   iscc installer.iss            (optionally /DAppVersion=1.2.3)
; Output: installer\CodeFix-Setup.exe. Per-user install, no admin rights needed.
; User data (%APPDATA%\CodeFix: projects, database, .env) is left alone by the uninstaller.

#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif

[Setup]
AppId={{6F0C1D52-9B7E-4C55-A1E3-6C0DEF1A2B37}
AppName=CodeFix
AppVersion={#AppVersion}
AppPublisher=CodeFix
DefaultDirName={localappdata}\Programs\CodeFix
DefaultGroupName=CodeFix
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=installer
OutputBaseFilename=CodeFix-Setup
SetupIconFile=assets\codefix.ico
UninstallDisplayIcon={app}\CodeFix.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\CodeFix\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\CodeFix"; Filename: "{app}\CodeFix.exe"
Name: "{autodesktop}\CodeFix"; Filename: "{app}\CodeFix.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\CodeFix.exe"; Description: "{cm:LaunchProgram,CodeFix}"; Flags: nowait postinstall skipifsilent
