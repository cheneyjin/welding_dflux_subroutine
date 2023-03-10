from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class AutoRot01DB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'AutoRot0.1_settings',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        VFrame_1 = FXVerticalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        ComboBox_1 = AFXComboBox(p=VFrame_1, ncols=0, nvis=1, text='Rotation axis:  ', tgt=form.axisKw, sel=0)
        ComboBox_1.setMaxVisible(10)
        ComboBox_1.appendItem(text='X-axis')
        ComboBox_1.appendItem(text='Y-axis')
        ComboBox_1.appendItem(text='Z-axis')
        slider = AFXSlider(VFrame_1, form.speedKw, 0, 
            AFXSLIDER_INSIDE_BAR|LAYOUT_FIX_WIDTH, 0,0,200,0)
        slider.setTitleLabelText('Speed')
        slider.setTitleLabelJustify(JUSTIFY_CENTER_X)
        slider.setMinLabelText('Slow')
        slider.setMaxLabelText('Fast')
        slider.setDecimalPlaces(1)
        slider.setRange(5, 10)
