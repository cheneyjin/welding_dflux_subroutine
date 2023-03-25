from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class WeldGeom10_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='geom',
            objectName='weldGeom10', registerQuery=False)
        pickedDefault = ''
        self.SideEdge1Kw = AFXObjectKeyword(self.cmd, 'SideEdge1', TRUE, pickedDefault)
        self.Leg1Kw = AFXFloatKeyword(self.cmd, 'Leg1', True, 5)
        self.SideEdge2Kw = AFXObjectKeyword(self.cmd, 'SideEdge2', TRUE, pickedDefault)
        self.Leg2Kw = AFXFloatKeyword(self.cmd, 'Leg2', True, 5)
        self.ReinKw = AFXFloatKeyword(self.cmd, 'Rein', True, 0)
        if not self.radioButtonGroups.has_key('HaveBot'):
            self.HaveBotKw1 = AFXIntKeyword(None, 'HaveBotDummy', True)
            self.HaveBotKw2 = AFXStringKeyword(self.cmd, 'HaveBot', True)
            self.radioButtonGroups['HaveBot'] = (self.HaveBotKw1, self.HaveBotKw2, {})
        self.radioButtonGroups['HaveBot'][2][13] = 'Yes'
        if not self.radioButtonGroups.has_key('HaveBot'):
            self.HaveBotKw1 = AFXIntKeyword(None, 'HaveBotDummy', True)
            self.HaveBotKw2 = AFXStringKeyword(self.cmd, 'HaveBot', True)
            self.radioButtonGroups['HaveBot'] = (self.HaveBotKw1, self.HaveBotKw2, {})
        self.radioButtonGroups['HaveBot'][2][14] = 'No'
        self.HaveBotKw1.setValue(14)
        self.BotEdgeKw = AFXObjectKeyword(self.cmd, 'BotEdge', TRUE, pickedDefault)
        self.AlongPathKw = AFXObjectKeyword(self.cmd, 'AlongPath', TRUE, pickedDefault)
        self.SetNameKw = AFXStringKeyword(self.cmd, 'SetName', True, 'weld1')
        self.colorKw = AFXStringKeyword(self.cmd, 'color', True, '#FF0000')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import weldGeom10DB
        return weldGeom10DB.WeldGeom10DB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        if self.ReinKw.getValue()!=0:
            showAFXErrorDialog(getAFXApp().getAFXMainWindow(),
                    'The reinforcement value can only be set as Zero!\n\
            in the opensource version.\n\
            Contact us to unlock this features!\n\
            Email: Cheneyjin@gmail.com')
            return False
        else:
            return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)
icfile = os.path.join(thisDir,'Geom28.png')
ic = afxCreatePNGIcon(icfile)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='WeldToolkit|WeldGeom10', 
    object=WeldGeom10_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=ic,
    kernelInitString='import weldGeom10',
    applicableModules= ('Part','Property','Mesh'),
    version='1.0',
    author='JINCheng',
    description='N/A',
    helpUrl='N/A'
)
