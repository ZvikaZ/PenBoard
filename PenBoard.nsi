; run at end
; add to start
; add to desktop?
; uninstall not working

;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  Name "PenBoard"
  OutFile "dist\PenBoard Installer.exe"
  Unicode True

  ;Default installation folder
  InstallDir "$PROGRAMFILES\PenBoard"

  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\PenBoard" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel admin  ;Z user

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING      ;Z what's this?

;--------------------------------
;Pages

;Z  !insertmacro MUI_PAGE_LICENSE "${NSISDIR}\Docs\Modern UI\License.txt"
;Z  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES

  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "PenBoard" SecDummy

  SetOutPath "$INSTDIR"

  ;ADD YOUR OWN FILES HERE...
  File /r "dist\PenBoard"

  ;Store installation folder
  WriteRegStr HKCU "Software\PenBoard" "" $INSTDIR

  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecDummy ${LANG_ENGLISH} "A test section."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} $(DESC_SecDummy)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...

  Delete "$INSTDIR\Uninstall.exe"

  RMDir "$INSTDIR"

  DeleteRegKey /ifempty HKCU "Software\PenBoard"

SectionEnd