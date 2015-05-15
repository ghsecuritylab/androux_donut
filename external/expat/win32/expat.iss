; Basic setup script for the Inno Setup installer builder.  For more
; information on the free installer builder, see www.jrsoftware.org.
;
; This script was contributed by Tim Peters.
; The current version is used with Inno Setup 2.0.19.

[Setup]
AppName=expat
AppId=expat
AppVersion=2.0.0
AppVerName=expat 2.0.0
AppCopyright=Copyright � 1998-2006 Thai Open Source Software Center, Clark Cooper, and the Expat maintainers
DefaultDirName={sd}\Expat-2.0.0
AppPublisher=The Expat Developers
AppPublisherURL=http://www.libexpat.org/
AppSupportURL=http://www.libexpat.org/
AppUpdatesURL=http://www.libexpat.org/
UninstallDisplayName=Expat XML Parser (version 2.0.0)
UninstallFilesDir={app}\Uninstall

Compression=bzip/9
SourceDir=..
OutputDir=win32
DisableStartupPrompt=yes
AllowNoIcons=yes
DisableProgramGroupPage=yes
DisableReadyPage=yes

[Files]
Flags: ignoreversion; Source: xmlwf\Release\*.exe;        DestDir: "{app}"
Flags: ignoreversion; Source: win32\MANIFEST.txt;         DestDir: "{app}"
Flags: ignoreversion; Source: Changes;                    DestDir: "{app}"; DestName: Changes.txt
Flags: ignoreversion; Source: COPYING;                    DestDir: "{app}"; DestName: COPYING.txt
Flags: ignoreversion; Source: README;                     DestDir: "{app}"; DestName: README.txt
Flags: ignoreversion; Source: doc\*.html;                 DestDir: "{app}\Doc"
Flags: ignoreversion; Source: doc\*.css;                  DestDir: "{app}\Doc"
Flags: ignoreversion; Source: doc\*.png;                  DestDir: "{app}\Doc"
Flags: ignoreversion; Source: lib\Release\*.dll;          DestDir: "{app}\Libs"
Flags: ignoreversion; Source: lib\Release\*.lib;          DestDir: "{app}\Libs"
Flags: ignoreversion; Source: lib\Release-w\*.dll;        DestDir: "{app}\Libs"
Flags: ignoreversion; Source: lib\Release-w\*.lib;        DestDir: "{app}\Libs"
Flags: ignoreversion; Source: lib\Release_static\*.lib;   DestDir: "{app}\StaticLibs"
Flags: ignoreversion; Source: lib\Release-w_static\*.lib; DestDir: "{app}\StaticLibs"
Flags: ignoreversion; Source: expat.dsw;                  DestDir: "{app}\Source"
Flags: ignoreversion; Source: win32\README.txt;           DestDir: "{app}\Source"
Flags: ignoreversion; Source: bcb5\*.bp*;                 DestDir: "{app}\Source\bcb5"
Flags: ignoreversion; Source: bcb5\*.mak;                 DestDir: "{app}\Source\bcb5"
Flags: ignoreversion; Source: bcb5\*.def;                 DestDir: "{app}\Source\bcb5"
Flags: ignoreversion; Source: bcb5\*.txt;                 DestDir: "{app}\Source\bcb5"
Flags: ignoreversion; Source: bcb5\*.bat;                 DestDir: "{app}\Source\bcb5"
Flags: ignoreversion; Source: lib\*.c;                    DestDir: "{app}\Source\lib"
Flags: ignoreversion; Source: lib\*.h;                    DestDir: "{app}\Source\lib"
Flags: ignoreversion; Source: lib\*.def;                  DestDir: "{app}\Source\lib"
Flags: ignoreversion; Source: lib\*.dsp;                  DestDir: "{app}\Source\lib"
Flags: ignoreversion; Source: examples\*.c;               DestDir: "{app}\Source\examples"
Flags: ignoreversion; Source: examples\*.dsp;             DestDir: "{app}\Source\examples"
Flags: ignoreversion; Source: tests\*.c;                  DestDir: "{app}\Source\tests"
Flags: ignoreversion; Source: tests\*.cpp;                DestDir: "{app}\Source\tests"
Flags: ignoreversion; Source: tests\*.h;                  DestDir: "{app}\Source\tests"
Flags: ignoreversion; Source: tests\README.txt;           DestDir: "{app}\Source\tests"
Flags: ignoreversion; Source: tests\benchmark\*.c;        DestDir: "{app}\Source\tests\benchmark"
Flags: ignoreversion; Source: tests\benchmark\*.ds*;      DestDir: "{app}\Source\tests\benchmark"
Flags: ignoreversion; Source: tests\benchmark\README.txt; DestDir: "{app}\Source\tests\benchmark"
Flags: ignoreversion; Source: xmlwf\*.c*;                 DestDir: "{app}\Source\xmlwf"
Flags: ignoreversion; Source: xmlwf\*.h;                  DestDir: "{app}\Source\xmlwf"
Flags: ignoreversion; Source: xmlwf\*.dsp;                DestDir: "{app}\Source\xmlwf"

[Messages]
WelcomeLabel1=Welcome to the Expat XML Parser Setup Wizard
WelcomeLabel2=This will install [name/ver] on your computer.%n%nExpat is an XML parser with a C-language API, and is primarily made available to allow developers to build applications which use XML using a portable API and fast implementation.%n%nIt is strongly recommended that you close all other applications you have running before continuing. This will help prevent any conflicts during the installation process.