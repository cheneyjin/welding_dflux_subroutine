from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class WeldGeom10DB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'WeldGeom 1.0',
            self.OK|self.APPLY|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            

        applyBtn = self.getActionButton(self.ID_CLICKED_APPLY)
        applyBtn.setText('Apply')
            
        HFrame_1 = FXHorizontalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=10, pt=0, pb=0)
        fileName = os.path.join(thisDir, 'multipass.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_1, text='', ic=icon)
        VFrame_1 = FXVerticalFrame(p=HFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=20, pb=0)
        HFrame_2 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        pickHf = FXHorizontalFrame(p=HFrame_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        pickHf.setSelector(99)
        label = FXLabel(p=pickHf, text='    SideEdge1' + ' (None)', ic=None, opts=LAYOUT_CENTER_Y|JUSTIFY_LEFT)
        pickHandler = WeldGeom10DBPickHandler(form, form.SideEdge1Kw, 'Pick one side edge', EDGES, ONE, label)
        icon = afxGetIcon('select', AFX_ICON_SMALL )
        FXButton(p=pickHf, text='\tPick Items in Viewport', ic=icon, tgt=pickHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=1, pb=1)
        AFXTextField(p=HFrame_2, ncols=6, labelText='    LegLength1:', tgt=form.Leg1Kw, sel=0)
        HFrame_3 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        pickHf = FXHorizontalFrame(p=HFrame_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        pickHf.setSelector(99)
        label = FXLabel(p=pickHf, text='    SideEdge2' + ' (None)', ic=None, opts=LAYOUT_CENTER_Y|JUSTIFY_LEFT)
        pickHandler = WeldGeom10DBPickHandler(form, form.SideEdge2Kw, 'Pick the other side edge', EDGES, ONE, label)
        icon = afxGetIcon('select', AFX_ICON_SMALL )
        FXButton(p=pickHf, text='\tPick Items in Viewport', ic=icon, tgt=pickHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=1, pb=1)
        AFXTextField(p=HFrame_3, ncols=6, labelText='    LegLength2:', tgt=form.Leg2Kw, sel=0)
        AFXTextField(p=VFrame_1, ncols=5, labelText='    Reinforcement:', tgt=form.ReinKw, sel=0)
        if isinstance(VFrame_1, FXHorizontalFrame):
            FXVerticalSeparator(p=VFrame_1, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        else:
            FXHorizontalSeparator(p=VFrame_1, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        HFrame_4 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=5, pb=0)
        l = FXLabel(p=HFrame_4, text='    Have Bottom Edge?  ', opts=JUSTIFY_LEFT)
        FXRadioButton(p=HFrame_4, text='Yes', tgt=form.HaveBotKw1, sel=13)
        FXRadioButton(p=HFrame_4, text='No', tgt=form.HaveBotKw1, sel=14)
        pickHf = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        pickHf.setSelector(99)
        self.Botlabel = FXLabel(p=pickHf, text='    BottomEdge' + ' (None)', ic=None, opts=LAYOUT_CENTER_Y|JUSTIFY_LEFT)
        pickHandler = WeldGeom10DBPickHandler(form, form.BotEdgeKw, 'Pick the bottom edges', EDGES, MANY, self.Botlabel)
        icon = afxGetIcon('select', AFX_ICON_SMALL )
        self.Botselect=FXButton(p=pickHf, text='\tPick Items in Viewport', ic=icon, tgt=pickHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=1, pb=1)
        pickHf = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        pickHf.setSelector(99)
        label = FXLabel(p=pickHf, text='    AlongPath   ' + ' (None)', ic=None, opts=LAYOUT_CENTER_Y|JUSTIFY_LEFT)
        pickHandler = WeldGeom10DBPickHandler(form, form.AlongPathKw, 'Pick sweep path', EDGES, MANY, label)
        icon = afxGetIcon('select', AFX_ICON_SMALL )
        FXButton(p=pickHf, text='\tPick Items in Viewport', ic=icon, tgt=pickHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=1, pb=1)
        HFrame_5 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=HFrame_5, ncols=11, labelText='    SetName:', tgt=form.SetNameKw, sel=0)
        btn = AFXColorButton(p=HFrame_5, text='Color:', tgt=form.colorKw, sel=0)

        # add transition
        self.addTransition(form.HaveBotKw1, AFXTransition.EQ,\
            13, self.Botlabel,\
            MKUINT(FXWindow.ID_ENABLE, SEL_COMMAND), None)
        self.addTransition(form.HaveBotKw1, AFXTransition.EQ,\
            13, self.Botselect,\
            MKUINT(FXWindow.ID_ENABLE, SEL_COMMAND), None)

        self.addTransition(form.HaveBotKw1, AFXTransition.EQ,\
            14, self.Botlabel,\
            MKUINT(FXWindow.ID_DISABLE, SEL_COMMAND), None)
        self.addTransition(form.HaveBotKw1, AFXTransition.EQ,\
            14, self.Botselect,\
            MKUINT(FXWindow.ID_DISABLE, SEL_COMMAND), None)
        



###########################################################################
# Class definition
###########################################################################

class WeldGeom10DBPickHandler(AFXProcedure):

        count = 0

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def __init__(self, form, keyword, prompt, entitiesToPick, numberToPick, label):

                self.form = form
                self.keyword = keyword
                self.prompt = prompt
                self.entitiesToPick = entitiesToPick # Enum value
                self.numberToPick = numberToPick # Enum value
                self.label = label
                self.labelText = label.getText()

                AFXProcedure.__init__(self, form.getOwner())

                WeldGeom10DBPickHandler.count += 1
                self.setModeName('WeldGeom10DBPickHandler%d' % (WeldGeom10DBPickHandler.count) )

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def getFirstStep(self):

                return  AFXPickStep(self, self.keyword, self.prompt, 
                    self.entitiesToPick, self.numberToPick, sequenceStyle=ARRAY)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def getNextStep(self, previousStep):

                self.label.setText( self.labelText.replace('None', 'Picked') )
                return None

        def deactivate(self):

            AFXProcedure.deactivate(self)
            if  self.numberToPick == ONE and self.keyword.getValue() and self.keyword.getValue()[0]!='<':
                sendCommand(self.keyword.getSetupCommands() + '\nhighlight(%s)' % self.keyword.getValue() )

