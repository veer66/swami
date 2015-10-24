#Swami skel module for the Swami Control Panel

from efl import ecore

from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL
from efl import elementary
from efl.elementary.button import Button
from efl.elementary.box import Box
from efl.elementary.icon import Icon
from efl.elementary.frame import Frame
from efl.elementary.list import List
from efl.elementary.entry import Entry

from elmextensions import StandardButton
from elmextensions import StandardPopup

from KeyboardLayouts import KeyboardLayouts

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
EXPAND_HORIZ = EVAS_HINT_EXPAND, 0.0
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL
FILL_HORIZ = EVAS_HINT_FILL, 0.5
ALIGN_CENTER = 0.5, 0.5

def searchList(text, lst):
    for item in lst:
        if text.lower() in item.lower()[:len(text)]:
            return lst.index(item)
    return 0

class SwamiModule(Box):
    def __init__(self, rent):
        Box.__init__(self, rent)
        self.parent = rent
        
        self.name = "Keyboard Layout"
        self.section = "System Settings"
        self.searchData = ["keyboard", "layout", "system", "input"]
        self.launchArg = "--keyboard"
        self.button = None
        
        self.icon = Icon(self, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        #Use FDO icons -> http://standards.freedesktop.org/icon-naming-spec/latest/ar01s04.html
        self.icon.standard_set('input-keyboard')
        self.icon.show()
        
        #print(list(KeyboardLayouts))
        
        self.keyboardList = keyboardList = List(self, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        keyboardList.callback_item_focused_add(self.enableKBSelect)
        self.keys = list(KeyboardLayouts)
        self.keys.sort()
        for kbl in self.keys:
            keyboardList.item_append(kbl)
        keyboardList.go()
        keyboardList.show()
        
        self.keyboardItems = keyboardList.items_get()
        
        sframe = Frame(self, size_hint_weight=EXPAND_HORIZ, size_hint_align=FILL_HORIZ)
        sframe.text = "Search"
        self.search = search = Entry(self)
        search.single_line = True
        search.callback_changed_add(self.searchChange)
        sframe.content = search
        search.show()
        sframe.show()
        
        self.mainBox = Box(self, size_hint_weight = EXPAND_BOTH, size_hint_align = FILL_BOTH)
        self.mainBox.pack_end(keyboardList)
        self.mainBox.pack_end(sframe)
        self.mainBox.show()
        
        buttonBox = Box(self, size_hint_weight = EXPAND_HORIZ, size_hint_align = FILL_BOTH)
        buttonBox.horizontal = True
        
        self.buttonKBSelect = buttonKBSelect = StandardButton(self, "Apply Selected", "ok", self.applyPressed)
        buttonKBSelect.disabled = True
        buttonKBSelect.show()
        
        buttonReturn = StandardButton(self, "Back", "go-previous", self.returnPressed)
        buttonReturn.show()
        
        buttonBox.pack_end(buttonKBSelect)
        buttonBox.pack_end(buttonReturn)
        buttonBox.show()
        
        self.pack_end(self.mainBox)
        self.pack_end(buttonBox)
    
    def enableKBSelect(self, lst, item):
        self.buttonKBSelect.disabled = False
    
    def applyPressed(self, btn):
        selectKB = self.keyboardList.selected_item_get().text
        print selectKB
        print KeyboardLayouts[selectKB]
        cmd = ecore.Exe("setxkbmap %s"%(KeyboardLayouts[selectKB]))
        
        compPop = StandardPopup(self, "%s keymap applied for current session."%selectKB, 'ok')
        compPop.show()
    
    def searchChange( self, entry ):
        #print entry.text
        zeindex = searchList(entry.text, self.keys)
        self.keyboardItems[zeindex].selected_set(True)
        self.keyboardItems[zeindex].bring_in()
        self.search.focus = True
    
    def returnPressed(self, btn):
        self.parent.returnMain()
