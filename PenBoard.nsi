; run at end
; make main component mandatory

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

  !insertmacro MUI_PAGE_WELCOME			;Z ?
;Z  !insertmacro MUI_PAGE_LICENSE "${NSISDIR}\Docs\Modern UI\License.txt"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH			;Z ?

  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "PenBoard" SecMain

  SetOutPath "$INSTDIR"

  ;ADD YOUR OWN FILES HERE...
  File /r "dist\PenBoard\*"

  ;Store installation folder
  WriteRegStr HKCU "Software\PenBoard" "" $INSTDIR

  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ;create start-menu items
  CreateDirectory "$SMPROGRAMS\PenBoard"
  CreateShortCut "$SMPROGRAMS\PenBoard\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\PenBoard\PenBoard.lnk" "$INSTDIR\PenBoard.exe" "" "$INSTDIR\PenBoard.exe" 0


SectionEnd

Section /o "Create desktop shortcut" SecDesktop
  ;create desktop shortcut
  CreateShortCut "$DESKTOP\PenBoard.lnk" "$INSTDIR\PenBoard.exe" ""
SectionEnd


;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecMain ${LANG_ENGLISH} "PenBoard core component."
  LangString DESC_SecDesktop ${LANG_ENGLISH} "Create a desktop shortcut for PenBoard."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...

  Delete "$INSTDIR\Uninstall.exe"

  RMDir /r "$INSTDIR"

  ;Delete Desktop and Start Menu Shortcuts
  Delete "$DESKTOP\PenBoard.lnk"
  Delete "$SMPROGRAMS\PenBoard\*.*"
  RmDir  "$SMPROGRAMS\PenBoard"


  DeleteRegKey /ifempty HKCU "Software\PenBoard"

SectionEnd