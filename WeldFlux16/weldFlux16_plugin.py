from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class WeldFlux16_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='kernel',
            objectName='T_plain16', registerQuery=False)
        pickedDefault = ''
        self.currentKw = AFXFloatKeyword(self.cmd, 'current', True,150)
        self.volKw = AFXFloatKeyword(self.cmd, 'vol', True,23)
        self.velKw = AFXFloatKeyword(self.cmd, 'vel', True,5)
        self.effKw = AFXFloatKeyword(self.cmd, 'eff', True,0.9)
        if not self.radioButtonGroups.has_key('mtype'):
            self.mtypeKw1 = AFXIntKeyword(None, 'mtypeDummy', True)
            self.mtypeKw2 = AFXStringKeyword(self.cmd, 'mtype', True)
            self.radioButtonGroups['mtype'] = (self.mtypeKw1, self.mtypeKw2, {})
        self.radioButtonGroups['mtype'][2][466] = 'Planar Gauss'
        self.mtypeKw1.setValue(466)
        if not self.radioButtonGroups.has_key('mtype'):
            self.mtypeKw1 = AFXIntKeyword(None, 'mtypeDummy', True)
            self.mtypeKw2 = AFXStringKeyword(self.cmd, 'mtype', True)
            self.radioButtonGroups['mtype'] = (self.mtypeKw1, self.mtypeKw2, {})
        self.radioButtonGroups['mtype'][2][467] = 'Double Ellipsoid'
        if not self.radioButtonGroups.has_key('mtype'):
            self.mtypeKw1 = AFXIntKeyword(None, 'mtypeDummy', True)
            self.mtypeKw2 = AFXStringKeyword(self.cmd, 'mtype', True)
            self.radioButtonGroups['mtype'] = (self.mtypeKw1, self.mtypeKw2, {})
        self.radioButtonGroups['mtype'][2][468] = 'Cone Body'
        self.aKw = AFXFloatKeyword(self.cmd, 'a', True,5)
        self.bKw = AFXFloatKeyword(self.cmd, 'b', True,4)
        self.cKw = AFXFloatKeyword(self.cmd, 'c', True, 3)
        self.a2Kw = AFXFloatKeyword(self.cmd, 'a2', True, 10)
        self.ratioKw = AFXFloatKeyword(self.cmd, 'ratio', True, 0.5)
        if not self.radioButtonGroups.has_key('wtype'):
            self.wtypeKw1 = AFXIntKeyword(None, 'wtypeDummy', True)
            self.wtypeKw2 = AFXStringKeyword(self.cmd, 'wtype', True)
            self.radioButtonGroups['wtype'] = (self.wtypeKw1, self.wtypeKw2, {})
        self.radioButtonGroups['wtype'][2][469] = 'Line'
        self.wtypeKw1.setValue(469)
        if not self.radioButtonGroups.has_key('wtype'):
            self.wtypeKw1 = AFXIntKeyword(None, 'wtypeDummy', True)
            self.wtypeKw2 = AFXStringKeyword(self.cmd, 'wtype', True)
            self.radioButtonGroups['wtype'] = (self.wtypeKw1, self.wtypeKw2, {})
        self.radioButtonGroups['wtype'][2][470] = 'Arc'
        if not self.radioButtonGroups.has_key('wtype'):
            self.wtypeKw1 = AFXIntKeyword(None, 'wtypeDummy', True)
            self.wtypeKw2 = AFXStringKeyword(self.cmd, 'wtype', True)
            self.radioButtonGroups['wtype'] = (self.wtypeKw1, self.wtypeKw2, {})
        self.radioButtonGroups['wtype'][2][471] = 'Free path'
        self.point1Kw1 = AFXObjectKeyword(self.cmd, 'point1', TRUE, pickedDefault)
        self.point2Kw1 = AFXObjectKeyword(self.cmd, 'point2', TRUE, pickedDefault)
        self.point3Kw1 = AFXObjectKeyword(self.cmd, 'point3', TRUE, pickedDefault)
        self.point4Kw1 = AFXObjectKeyword(self.cmd, 'point4', TRUE, pickedDefault)
        self.toepath1Kw= AFXObjectKeyword(self.cmd, 'toepath1', TRUE, pickedDefault)
        self.toepath2Kw= AFXObjectKeyword(self.cmd, 'toepath2', TRUE, pickedDefault)
        self.point1Kw2 = AFXTupleKeyword(self.cmd, 'point1', True,
            3, 3, AFXTUPLE_TYPE_FLOAT)
        self.point2Kw2 = AFXTupleKeyword(self.cmd, 'point2', True,
            3, 3, AFXTUPLE_TYPE_FLOAT)
        self.point3Kw2 = AFXTupleKeyword(self.cmd, 'point3', True,
            3, 3, AFXTUPLE_TYPE_FLOAT)
        self.point3Kw2.setValuesForBlanks('0')
        self.point4Kw2 = AFXTupleKeyword(self.cmd, 'point4', True,
            3, 3, AFXTUPLE_TYPE_FLOAT)
        #self.toepath1Kw2 = AFXTupleKeyword(self.cmd, 'toepath1', True,
        #    3, 3, AFXTUPLE_TYPE_FLOAT)
        #self.toepath2Kw2 = AFXTupleKeyword(self.cmd, 'toepath2', True,
        #    3, 3, AFXTUPLE_TYPE_FLOAT)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import weldFlux16DB
        return weldFlux16DB.WeldFlux16DB(self)

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

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='WeldFlux16', 
    object=WeldFlux16_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    kernelInitString='import T_plain16',
    applicableModules=ALL,
    version='N/A',
    author='N/A',
    description='N/A',
    helpUrl='N/A'
)
