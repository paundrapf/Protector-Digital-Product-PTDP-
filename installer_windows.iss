; PTDP Windows Installer Script
; Inno Setup 6.x required
; This script creates a professional Windows installer for PTDP Creator and Viewer

#define MyAppName "PTDP - Protector Digital Product"
#define MyAppVersion "2.0"
#define MyAppPublisher "PTDP Team"
#define MyAppURL "https://ptdp.io"
#define MyAppExeName "PTDP-Creator.exe"
#define MyAppExeName2 "PTDP-Viewer.exe"

[Setup]
; App Information
AppId={{8F9A2B3C-4D5E-6F7A-8B9C-0D1E2F3A4B5C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Install Directory
DefaultDirName={autopf}\PTDP
DefaultGroupName={#MyAppName}
AllowNoIcons=yes

; Output
OutputDir=installer_output
OutputBaseFilename=PTDP-Setup-v{#MyAppVersion}
Compression=lzma2/max
SolidCompression=yes

; Icons and Graphics
SetupIconFile=website\favicon.ico
WizardStyle=modern

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Architecture
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; Uninstall
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "indonesian"; MessagesFile: "compiler:Languages\Indonesian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Main executables
Source: "dist\windows\PTDP-Creator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\windows\PTDP-Viewer.exe"; DestDir: "{app}"; Flags: ignoreversion

; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "USER_GUIDE.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "QUICKSTART.md"; DestDir: "{app}"; Flags: ignoreversion

; Sample files (optional)
Source: "samples\*"; DestDir: "{app}\samples"; Flags: ignoreversion recursesubdirs createallsubdirs; Tasks: 

[Icons]
; Start Menu Icons
Name: "{group}\PTDP Creator"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\PTDP Viewer"; Filename: "{app}\{#MyAppExeName2}"
Name: "{group}\User Guide"; Filename: "{app}\USER_GUIDE.md"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

; Desktop Icons (optional)
Name: "{autodesktop}\PTDP Creator"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{autodesktop}\PTDP Viewer"; Filename: "{app}\{#MyAppExeName2}"; Tasks: desktopicon

; Quick Launch Icons (optional)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\PTDP Creator"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\PTDP Viewer"; Filename: "{app}\{#MyAppExeName2}"; Tasks: quicklaunchicon

[Run]
; Launch after install
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,PTDP Creator}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  if not IsWin64 then
  begin
    MsgBox('This application requires a 64-bit version of Windows.', mbError, MB_OK);
    Result := False;
  end;
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpWelcome then
  begin
    WizardForm.NextButton.Caption := SetupMessage(msgButtonNext);
  end;
end;
