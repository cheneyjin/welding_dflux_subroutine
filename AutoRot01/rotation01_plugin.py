from abaqusGui import *
from abaqusConstants import ALL
import osutils, os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)
icfile = os.path.join(thisDir,'swap25.png')
ic = afxCreatePNGIcon(icfile)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerKernelMenuButton(
    moduleName = 'rotation01',
    functionName = 'rotation()',
    buttonText='AutoRotation|Rotation01', 
    icon=ic,
    applicableModules=ALL,
    version='N/A',
    author='N/A',
    description='N/A',
    helpUrl='N/A'
)
