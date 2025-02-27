; Script de Inno Setup para instalar InventaryTech
[Setup]
AppName=InventaryTech
AppVersion=1.0.0
DefaultDirName={pf}\InventaryTech
DefaultGroupName=InventaryTech
UninstallDisplayIcon={app}\InventaryTech.exe
OutputDir=.
OutputBaseFilename=InventaryTech_Installer
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
SetupIconFile="icon_app.ico" 

[Files]
Source: "dist\InventaryTech.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon_app.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "db.sqlite3"; DestDir: "{app}"; Flags: ignoreversion
Source: "app\templates\*"; DestDir: "{app}\app\templates"; Flags: recursesubdirs createallsubdirs
Source: "app\static\*"; DestDir: "{app}\app\static"; Flags: recursesubdirs createallsubdirs
Source: "python_embedded\*"; DestDir: "{app}\python_embedded"; Flags: recursesubdirs createallsubdirs
Source: "config.ini"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\InventaryTech"; Filename: "{app}\InventaryTech.exe"; IconFilename: "{app}\icon_app.ico"
Name: "{commondesktop}\InventaryTech"; Filename: "{app}\InventaryTech.exe"; IconFilename: "{app}\icon_app.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\InventaryTech.exe"; Description: "Ejecutar InventaryTech"; Flags: nowait postinstall

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Opciones adicionales"
