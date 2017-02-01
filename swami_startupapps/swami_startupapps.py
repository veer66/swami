#Moksha startup applications module for the Swami Control Panel

import os
import gtk

from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL
from efl import elementary
from efl.elementary.button import Button
from efl.elementary.box import Box
from efl.elementary.icon import Icon
from efl.elementary.image import Image

from elmextensions import StandardButton, SearchableList

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
EXPAND_HORIZ = EVAS_HINT_EXPAND, 0.0
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL
FILL_HORIZ = EVAS_HINT_FILL, 0.5
ALIGN_CENTER = 0.5, 0.5

UserHome = os.path.expanduser("~")

IconTheme = gtk.icon_theme_get_default()

ApplicationPaths = [ "/usr/share/applications/",
                "%s/.local/share/applications/"%UserHome]

class SwamiModule(Box):
    def __init__(self, rent):
        Box.__init__(self, rent)
        self.parent = rent
        
        #This appears on the button in the main swmai window
        self.name = "Startup Applications"
        #The section in the main window the button is added to
        self.section = "Applications"
        #Search terms that this module should appear for
        self.searchData = ["startup", "command", "applications", "apps"]
        #Command line argument to open this module directly
        self.launchArg = "--startupapps"
        #Should be none by default. This value is used internally by swami
        self.button = None
        
        self.icon = Icon(self, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        #Use FDO icons -> http://standards.freedesktop.org/icon-naming-spec/latest/ar01s04.html
        self.icon.standard_set('system-run')
        self.icon.show()
        
        self.mainBox = Box(self, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        self.mainBox.show()
        
        buttonBox = Box(self, size_hint_weight = EXPAND_HORIZ, size_hint_align = FILL_BOTH)
        buttonBox.horizontal = True
        
        buttonReturn = StandardButton(self, "Back", "go-previous", self.returnPressed)
        buttonReturn.show()
        
        buttonBox.pack_end(buttonReturn)
        buttonBox.show()
        
        desktopFiles = []
        
        for ourPath in ApplicationPaths:
            desktopFiles += [os.path.join(dp, f) for dp, dn, filenames in os.walk(ourPath) for f in filenames if os.path.splitext(f)[1] == '.desktop']
        
        self.applicationsList = applicationsList = SearchableList(self, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        #applicationsList.callback_item_focused_add(self.enableTZSelect)

        applicationsToAdd = []

        for d in desktopFiles:
            with open(d) as desktopFile:
                icon = None
                for line in desktopFile:
                    if line[:5] == "Name=":
                        name = line[5:][:-1]
                    
                    if line[:5] == "Icon=":
                        icon = line[5:]
                    
                
                if icon:
                    iconInfo = IconTheme.lookup_icon(icon.strip(), 48, 0)

                    if iconInfo:
                        iconObj = Image(self, file=iconInfo.get_filename(), size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
                    else:
                        iconObj = Icon(self, standard="preferences-system", size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
                else:
                    iconObj = Icon(self, standard="preferences-system", size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
                
                applicationsToAdd.append([name, iconObj])
                
        applicationsToAdd.sort()
        
        for a in applicationsToAdd:
            applicationsList.item_append(a[0], a[1])
                
        applicationsList.show()
        
        self.mainBox.pack_end(applicationsList)
        
        self.pack_end(self.mainBox)
        self.pack_end(buttonBox)
        
    def returnPressed(self, btn):
        self.parent.returnMain()
