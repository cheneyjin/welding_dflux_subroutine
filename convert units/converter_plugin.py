"""
=================================================================
 original written by:   James Lockley, ABAQUS UK, Jan 2005

 converts units from one measurement unit to another according to the formula
 described in units.py

 e.g. 'K': {'C': 'x-273'}   Temperature: Celsius --> Kelvin 


 
================================================================="""





from abaqusGui import *
import abaqusGui as ag
import os

try:
    import units
    unitImport = 1
except:
    unitImport = 0
    


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def convertUnits(value, property, unit1, unit2):
    return eval(units.properties[property][unit1][unit2].replace('x', '%s')%value)



###########################################################################
# Class definition
###########################################################################

class ConvertForm(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        AFXForm.__init__(self, owner)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):
        if unitImport:
            return ConvertDB(self)
        else:
            mainWindow = getAFXApp().getAFXMainWindow()
            showAFXInformationDialog(mainWindow, 'There is an Error in units.py\n Please check the python syntax is correct.')



###########################################################################
# Class definition
###########################################################################

class ConvertDB(AFXDataDialog):

    [
        CONVERT,
        RELOAD,
        HELP,
        VIEW
        ] = range(AFXDataDialog.ID_LAST, AFXDataDialog.ID_LAST+4)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):
        
        # Construct the base class.
        #
        AFXDataDialog.__init__(self, form, 'Convert Units',
                               opts=DIALOG_ACTIONS_SEPARATOR,w=457)

        # Function Mapping
        FXMAPFUNC(self, SEL_COMMAND, self.CONVERT, ConvertDB.onCmdConvert)
        FXMAPFUNC(self, SEL_COMMAND, self.RELOAD,  ConvertDB.onCmdReload)
        FXMAPFUNC(self, SEL_COMMAND, self.HELP, ConvertDB.onCmdHelp)
        FXMAPFUNC(self, SEL_COMMAND, self.VIEW, ConvertDB.onCmdView)

        # Start Adding widgets
        vf = FXVerticalFrame(self)
        hf = FXHorizontalFrame(vf)
        self.propCB =  AFXComboBox(hf, 10, 10, 'Physical Property')


        hf = FXHorizontalFrame(vf)

        self.valueTF = AFXTextField(hf, 9, '')
        self.unit1CB = AFXComboBox(hf, 5, 5, ' ')
        FXButton(hf, '-->', ic=None,  w=10, 
                 tgt=self, sel=self.CONVERT, opts=LAYOUT_FILL_X|BUTTON_NORMAL)

        self.answer = AFXTextField(hf, 9,  '')
        self.answer.setEditable(FALSE)
        self.unit2CB = AFXComboBox(hf, 5, 5, ' ')


        # Dynamically populate lists
        props = units.properties.keys()
        props.sort()

        for prop in props: self.propCB.appendItem(prop)
        self.propCB.setCurrentItem(0)

        unit1s = units.properties[props[0]].keys()
        unit1s.sort()
        for unit1 in unit1s: self.unit1CB.appendItem(unit1)
        self.unit1CB.setCurrentItem(0)

        unit2s = units.properties[props[0]][unit1s[0]].keys()
        unit2s.sort()
        for unit2 in unit2s: self.unit2CB.appendItem(unit2)
        self.unit2CB.setCurrentItem(0)


        # remember values for persistence
        self.oldPropSelected = props[0]
        self.oldUnit1Selected = unit1s[0]


        # Action Buttons
        self.appendActionButton('View', self, self.VIEW)
        self.appendActionButton('Reload', self, self.RELOAD)
        self.appendActionButton('Help', self, self.HELP)
        self.appendActionButton( self.DISMISS)

       
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onCmdReload(self, sender, sel, ptr):
        reload(units)
        props = units.properties.keys()
        props.sort()
        self.propCB.clearItems()
        
        for prop in props: self.propCB.appendItem(prop)
        self.propCB.setCurrentItem(0)
        

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onCmdConvert(self, sender, sel, ptr):
        prop = self.propCB.getText()
        value = self.valueTF.getText()
        unit1 = self.unit1CB.getText()
        unit2 = self.unit2CB.getText()

        value2 = convertUnits(value, prop, unit1, unit2)
        self.answer.setText('%.4g'%value2)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onCmdHelp(self, sender, sel, ptr):
        import uti
        absPath = os.path.abspath(__file__)
        absDir  = os.path.dirname(absPath)
        helpUrl = os.path.join(absDir, 'units-conversion-help.html')
        uti.webBrowser.displayURL(helpUrl)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onCmdView(self, sender, sel, ptr):
        import subprocess
        absPath = os.path.abspath(__file__)
        absDir  = os.path.dirname(absPath)
        unitsfile = os.path.join(absDir, 'units.py')
        subprocess.Popen(['notepad.exe',unitsfile])

        
    #----------------------------------------------------------------------
    def processUpdates(self):
        # Keep GUI up-to-date with selections
        prop = self.propCB.getText()
        if prop != self.oldPropSelected:
            unit1s = units.properties[prop].keys()
            unit1s.sort()
            self.unit1CB.clearItems()
            for unit1 in unit1s: self.unit1CB.appendItem(unit1)
            self.unit1CB.setCurrentItem(0)
            self.oldPropSelected = prop

            unit2s = units.properties[prop][unit1].keys()
            unit2s.sort()
            self.unit2CB.clearItems()
            for unit2 in unit2s: self.unit2CB.appendItem(unit2)
            self.unit2CB.setCurrentItem(0)
            self.oldUnit1Selected = unit1

            self.answer.setText('')


        unit1 = self.unit1CB.getText()
        if unit1 != self.oldUnit1Selected:
            unit2s = units.properties[prop][unit1].keys()
            unit2s.sort()
            self.unit2CB.clearItems()
            for unit2 in unit2s: self.unit2CB.appendItem(unit2)
            self.unit2CB.setCurrentItem(0)
            self.oldUnit1Selected = unit1

            self.answer.setText('')


    #----------------------------------------------------------------------



toolset = getAFXApp().getAFXMainWindow().getPluginToolset()

absPath = os.path.abspath(__file__)
absDir  = os.path.dirname(absPath)
helpUrl = os.path.join(absDir, 'units-conversion-help.html')


# Register a GUI plug-in in the Plug-ins menu.

toolset.registerGuiMenuButton(
    object=ConvertForm(toolset), buttonText='Convert Units...',
    kernelInitString='import units',
    version='0.1', author='James Lockley, ABAQUS UK',
    description='Provides a dialog that allows you to convert units from one type to another.\n'+\
    "The conversions descriptions are contained in 'units.py' which users are \n"+\
    "encouraged to edit.\n\n"+\
    "Further conversions can be added by using the format described in Help",
    helpUrl=helpUrl)

