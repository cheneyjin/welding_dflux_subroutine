from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class AMFlux10_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='kernel',
            objectName='AMFlux10', registerQuery=False)
        pickedDefault = ''
        self.powerKw = AFXFloatKeyword(self.cmd, 'power', True,1000)
        self.velKw = AFXFloatKeyword(self.cmd, 'vel', True,10)
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
        self.aKw = AFXFloatKeyword(self.cmd, 'a', True,1)
        self.bKw = AFXFloatKeyword(self.cmd, 'b', True,1)
        self.cKw = AFXFloatKeyword(self.cmd, 'c', True, 0.5)
        self.a2Kw = AFXFloatKeyword(self.cmd, 'a2', True, 2)
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
        self.point1Kw1 = AFXObjectKeyword(self.cmd, 'point1', TRUE, pickedDefault)
        self.point2Kw1 = AFXObjectKeyword(self.cmd, 'point2', TRUE, pickedDefault)
        self.point3Kw1 = AFXObjectKeyword(self.cmd, 'point3', TRUE, pickedDefault)
        self.point4Kw1 = AFXObjectKeyword(self.cmd, 'point4', TRUE, pickedDefault)
        self.point1Kw2 = AFXTupleKeyword(self.cmd, 'point1', True,
            3, 3, AFXTUPLE_TYPE_FLOAT)
        self.point2Kw2 = AFXTupleKeyword(self.cmd, 'point2', True,
            3, 3, AFXTUPLE_TYPE_FLOAT)
        self.point3Kw2 = AFXTupleKeyword(self.cmd, 'point3', True,
            3, 3, AFXTUPLE_TYPE_FLOAT)
        self.point3Kw2.setValuesForBlanks('0')
        self.point4Kw2 = AFXTupleKeyword(self.cmd, 'point4', True,
            3, 3, AFXTUPLE_TYPE_FLOAT)
        #self.EnAMKw = AFXBoolKeyword(self.cmd, 'EnAM', AFXBoolKeyword.TRUE_FALSE, True, False)
        self.PreStepNameKw = AFXStringKeyword(self.cmd, 'PreStepName', True, 'remove')
        self.FirstAMstepKw = AFXStringKeyword(self.cmd, 'FirstAMstep', True, 'AM1')
        self.CurrentPassKw = AFXStringKeyword(self.cmd, 'CurrentPass', True, 'weld1')
        self.LengthKw = AFXFloatKeyword(self.cmd, 'Length', True, 10)
        self.SpaceKw = AFXFloatKeyword(self.cmd, 'Space', True, 0.2)
        self.LayersKw = AFXIntKeyword(self.cmd, 'Layers', True, 2)
        self.ElesKw = AFXIntKeyword(self.cmd, 'Eles', True, 8)
        self.BEleKw = AFXIntKeyword(self.cmd, 'BEle', True, 1)
        if not self.radioButtonGroups.has_key('Eltype'):
            self.EltypeKw1 = AFXIntKeyword(None, 'EltypeDummy', True)
            self.EltypeKw2 = AFXStringKeyword(self.cmd, 'Eltype', True)
            self.radioButtonGroups['Eltype'] = (self.EltypeKw1, self.EltypeKw2, {})
        self.radioButtonGroups['Eltype'][2][471] = 'Box'
        self.EltypeKw1.setValue(471)
        if not self.radioButtonGroups.has_key('Eltype'):
            self.EltypeKw1 = AFXIntKeyword(None, 'EltypeDummy', True)
            self.EltypeKw2 = AFXStringKeyword(self.cmd, 'Eltype', True)
            self.radioButtonGroups['Eltype'] = (self.EltypeKw1, self.EltypeKw2, {})
        self.radioButtonGroups['Eltype'][2][472] = 'Label'
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import AMFlux10DB
        return AMFlux10DB.AMFlux10DB(self)

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
    buttonText='AMFlux10', 
    object=AMFlux10_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    kernelInitString='import AMFlux10',
    applicableModules=ALL,
    version='N/A',
    author='N/A',
    description='N/A',
    helpUrl='N/A'
)
