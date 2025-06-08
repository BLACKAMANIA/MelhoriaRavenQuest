[Setup]
AppName=Otimizador RavenQuest
AppVersion=1.0
DefaultDirName={pf}\Otimizador RavenQuest
DefaultGroupName=Otimizador RavenQuest
OutputBaseFilename=Otimizador_RavenQuest_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\otimizador_ravenquest.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "background.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "interface_config.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Otimizador RavenQuest"; Filename: "{app}\otimizador_ravenquest.exe"
Name: "{group}\Desinstalar Otimizador RavenQuest"; Filename: "{uninstallexe}"
