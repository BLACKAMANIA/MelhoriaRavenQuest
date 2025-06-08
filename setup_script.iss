; Inno Setup Script para Otimizador RavenQuest
; Assinatura: SanJéffersonBLK

[Setup]
AppName=Otimizador RavenQuest
AppVersion=1.0
AppPublisher=SanJéffersonBLK
DefaultDirName={pf}\Otimizador RavenQuest
DefaultGroupName=Otimizador RavenQuest
OutputBaseFilename=OtimizadorRavenQuest_Installer
Compression=lzma
SolidCompression=yes
SetupIconFile=C:\Users\Jefferson\Desktop\Nova pasta\icon.ico
DisableProgramGroupPage=no
DisableReadyPage=no
DisableStartupPrompt=no

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Files]
Source: "dist\otimizador_ravenquest.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Jefferson\Desktop\Nova pasta\background.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Jefferson\Desktop\Nova pasta\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Jefferson\Desktop\Nova pasta\interface_config.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Otimizador RavenQuest"; Filename: "{app}\otimizador_ravenquest.exe"; IconFilename: "{app}\icon.ico"; WorkingDir: "{app}"
Name: "{commondesktop}\Otimizador RavenQuest"; Filename: "{app}\otimizador_ravenquest.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon; WorkingDir: "{app}"

[Tasks]
Name: "desktopicon"; Description: "Criar ícone na Área de Trabalho"; GroupDescription: "Opções adicionais:"

[Run]
Filename: "{app}\otimizador_ravenquest.exe"; Description: "Executar Otimizador RavenQuest"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: dirifempty; Name: "{app}"

[Code]
// Assinatura no rodapé do instalador
procedure InitializeWizard();
begin
  WizardForm.StatusLabel.Caption := 'Instalador criado por SanJéffersonBLK';
end;
