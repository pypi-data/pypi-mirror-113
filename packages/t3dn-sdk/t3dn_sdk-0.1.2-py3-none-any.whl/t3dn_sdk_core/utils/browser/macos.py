import subprocess


def get_default_browser_path():
    script = '''
use AppleScript version "2.5"
use framework "Foundation"
use framework "AppKit"
use scripting additions

set NSWorkspace to a reference to NSWorkspace of current application
set sharedWorkspace to sharedWorkspace() of NSWorkspace
set |NSURL| to a reference to |NSURL| of current application
set urlNSString to (current application's NSString)'s stringWithString:"http://"
set testURL to |NSURL|'s URLWithString:urlNSString

set theURL to sharedWorkspace()'s URLForApplicationToOpenURL:testURL
return theURL's |path|() as string
'''
    browser = subprocess.check_output(args=['osascript'],
                                      input=script,
                                      encoding='UTF-8').strip()
    if browser:
        return browser
