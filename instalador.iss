[Setup]
AppName=Otimizador RavenQuest
AppVersion=1.0
DefaultDirName={commonpf}\Otimizador RavenQuest
DefaultGroupName=Otimizador RavenQuest
OutputBaseFilename=setup_otimizador_ravenquest
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
SetupIconFile=C:\Users\Jefferson\Desktop\Nova pasta\icon.ico
UninstallDisplayIcon={app}\Otimizador_RavenQuest.exe

[Files]
Source: "C:\Users\Jefferson\Desktop\Nova pasta\dist\Otimizador_RavenQuest.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Otimizador RavenQuest"; Filename: "{app}\Otimizador_RavenQuest.exe"; IconFilename: "C:\Users\Jefferson\Desktop\Nova pasta\icon.ico"
Name: "{commondesktop}\Otimizador RavenQuest"; Filename: "{app}\Otimizador_RavenQuest.exe"; IconFilename: "C:\Users\Jefferson\Desktop\Nova pasta\icon.ico"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Criar ícone na área de trabalho"; GroupDescription: "Tarefas adicionais"; Flags: unchecked