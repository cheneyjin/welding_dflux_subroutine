from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class AMFlux10DB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'AMFlux 1.0',
            self.APPLY|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            
        applyBtn = self.getActionButton(self.ID_CLICKED_APPLY)
        applyBtn.setText('Pass+1')
            
        TabBook_1 = FXTabBook(p=self, tgt=None, sel=0,
            opts=TABBOOK_NORMAL,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)
        tabItem = FXTabItem(p=TabBook_1, text='Heat Input', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_1 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        HFrame_1 = FXHorizontalFrame(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_1 = FXGroupBox(p=HFrame_1, text='Process Settings', opts=FRAME_GROOVE)
        VAligner_1 = AFXVerticalAligner(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VAligner_1, ncols=10, labelText='Power (W):', tgt=form.powerKw, sel=0)
        AFXTextField(p=VAligner_1, ncols=10, labelText='Vel.(mm/s):', tgt=form.velKw, sel=0)
        AFXTextField(p=VAligner_1, ncols=10, labelText='Efficiency:', tgt=form.effKw, sel=0)
        fileName = os.path.join(thisDir, 'contours.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_1, text='', ic=icon)
        tabItem = FXTabItem(p=TabBook_1, text='Model Data', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_3 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        HFrame_2 = FXHorizontalFrame(p=TabItem_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        VFrame_3 = FXVerticalFrame(p=HFrame_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_2 = FXGroupBox(p=VFrame_3, text='Model Type', opts=FRAME_GROOVE)
        FXRadioButton(p=GroupBox_2, text='Planar Gauss', tgt=form.mtypeKw1, sel=466)
        FXRadioButton(p=GroupBox_2, text='Double Ellipsoid', tgt=form.mtypeKw1, sel=467)
        FXRadioButton(p=GroupBox_2, text='Cone Body', tgt=form.mtypeKw1, sel=468)
        GroupBox_3 = FXGroupBox(p=VFrame_3, text='Model Parameters', opts=FRAME_GROOVE)
        VAligner_2 = AFXVerticalAligner(p=GroupBox_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        #add trasition
        self.Texta = AFXTextField(p=VAligner_2, ncols=10, labelText='a:', tgt=form.aKw, sel=0)
        self.Textb = AFXTextField(p=VAligner_2, ncols=10, labelText='b:', tgt=form.bKw, sel=0)
        self.Textc = AFXTextField(p=VAligner_2, ncols=10, labelText='c:', tgt=form.cKw, sel=0)
        self.Texta2 = AFXTextField(p=VAligner_2, ncols=10, labelText='a2:', tgt=form.a2Kw, sel=0)
        self.Textr = AFXTextField(p=VAligner_2, ncols=10, labelText='Ratio:', tgt=form.ratioKw, sel=0)

        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            466, self.Textc,\
            MKUINT(FXWindow.ID_DISABLE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            466, self.Texta2,\
            MKUINT(FXWindow.ID_DISABLE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            466, self.Textr,\
            MKUINT(FXWindow.ID_DISABLE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            467, self.Textc,\
            MKUINT(FXWindow.ID_ENABLE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            467, self.Texta2,\
            MKUINT(FXWindow.ID_ENABLE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            467, self.Textr,\
            MKUINT(FXWindow.ID_ENABLE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            468, self.Textc,\
            MKUINT(FXWindow.ID_ENABLE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            468, self.Texta2,\
            MKUINT(FXWindow.ID_DISABLE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            468, self.Textr,\
            MKUINT(FXWindow.ID_DISABLE, SEL_COMMAND), None)

        guassfile = os.path.join(thisDir, 'Gauss.png')
        doublefile= os.path.join(thisDir, 'double.png')
        conefile=os.path.join(thisDir, 'cone.png')
        self.guass = afxCreatePNGIcon(guassfile)
        self.double = afxCreatePNGIcon(doublefile)
        self.cone = afxCreatePNGIcon(conefile)

        self.pic1=FXLabel(p=HFrame_2, text='', ic=self.guass)
        self.pic2=FXLabel(p=HFrame_2, text='', ic=self.double)
        self.pic2.hide()
        self.pic3=FXLabel(p=HFrame_2, text='', ic=self.cone)
        self.pic3.hide()

        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            466, self.pic1,\
            MKUINT(FXWindow.ID_SHOW, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            466, self.pic2,\
            MKUINT(FXWindow.ID_HIDE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            466, self.pic3,\
            MKUINT(FXWindow.ID_HIDE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            467, self.pic1,\
            MKUINT(FXWindow.ID_HIDE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            467, self.pic2,\
            MKUINT(FXWindow.ID_SHOW, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            467, self.pic3,\
            MKUINT(FXWindow.ID_HIDE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            468, self.pic1,\
            MKUINT(FXWindow.ID_HIDE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            468, self.pic2,\
            MKUINT(FXWindow.ID_HIDE, SEL_COMMAND), None)
        self.addTransition(form.mtypeKw1, AFXTransition.EQ,\
            468, self.pic3,\
            MKUINT(FXWindow.ID_SHOW, SEL_COMMAND), None)

        tabItem = FXTabItem(p=TabBook_1, text='Weld Path', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_2 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        HFrame_3 = FXHorizontalFrame(p=TabItem_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=2, pb=5)
        l = FXLabel(p=HFrame_3, text='Type:  ', opts=JUSTIFY_LEFT)
        FXRadioButton(p=HFrame_3, text='Line', tgt=form.wtypeKw1, sel=469)
        FXRadioButton(p=HFrame_3, text='Arc', tgt=form.wtypeKw1, sel=470)
        HFrame_4 = FXHorizontalFrame(p=TabItem_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_4 = FXGroupBox(p=HFrame_4, text='Path Definition', opts=FRAME_GROOVE)
        VAligner_4 = AFXVerticalAligner(p=GroupBox_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        pickHf = FXHorizontalFrame(p=VAligner_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        pickHf.setSelector(99)
        label = FXLabel(p=pickHf, text='Start Point:    ' + ' (None) ', ic=None, opts=LAYOUT_CENTER_Y|JUSTIFY_LEFT)
        pickHandler = AMFlux10DBPickHandler(form, form.point1Kw1, form.point1Kw2,'Pick the start point', NODES|DATUM_POINTS, ONE,3, label)
        icon = afxGetIcon('select', AFX_ICON_SMALL )
        FXButton(p=pickHf, text='\tPick Items in Viewport', ic=icon, tgt=pickHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=1, pb=1)
        pickHf = FXHorizontalFrame(p=VAligner_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        pickHf.setSelector(99)
        label = FXLabel(p=pickHf, text='Along Point:  ' + ' (None) ', ic=None, opts=LAYOUT_CENTER_Y|JUSTIFY_LEFT)
        pickHandler = AMFlux10DBPickHandler(form, form.point2Kw1,form.point2Kw2, 'Pick a point on weld line', NODES|DATUM_POINTS, ONE, 3,label)
        icon = afxGetIcon('select', AFX_ICON_SMALL )
        FXButton(p=pickHf, text='\tPick Items in Viewport', ic=icon, tgt=pickHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=1, pb=1)
        pickHf = FXHorizontalFrame(p=VAligner_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        pickHf.setSelector(99)
        self.p2Label = FXLabel(p=pickHf, text='Along Point2:' + ' (None) ', ic=None, opts=LAYOUT_CENTER_Y|JUSTIFY_LEFT)
        pickHandler = AMFlux10DBPickHandler(form, form.point3Kw1,form.point3Kw2, 'Pick anothe point on weld line', NODES|DATUM_POINTS, ONE,4, self.p2Label)
        icon = afxGetIcon('select', AFX_ICON_SMALL )
        self.AP2=FXButton(p=pickHf, text='\tPick Items in Viewport', ic=icon, tgt=pickHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=1, pb=1)
        pickHf = FXHorizontalFrame(p=VAligner_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        pickHf.setSelector(99)
        label = FXLabel(p=pickHf, text='Toe Point:     ' + ' (None) ', ic=None, opts=LAYOUT_CENTER_Y|JUSTIFY_LEFT)
        pickHandler = AMFlux10DBPickHandler(form, form.point4Kw1,form.point4Kw2, 'Pick a point on weld toe', NODES|DATUM_POINTS, ONE, 2,label)
        icon = afxGetIcon('select', AFX_ICON_SMALL )
        FXButton(p=pickHf, text='\tPick Items in Viewport', ic=icon, tgt=pickHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=1, pb=1)

        linefile = os.path.join(thisDir, 'track.png')
        arcfile = os.path.join(thisDir, 'arc.png')
        self.line = afxCreatePNGIcon(linefile)
        self.arc = afxCreatePNGIcon(arcfile)
        
        self.trpic1 = FXLabel(p=HFrame_4, text='', ic=self.line)
        self.trpic2 = FXLabel(p=HFrame_4, text='', ic=self.arc)
        self.trpic2.hide()

        # show pic
        self.addTransition(form.wtypeKw1, AFXTransition.EQ,\
            469, self.trpic1,\
            MKUINT(FXWindow.ID_SHOW, SEL_COMMAND), None)
        self.addTransition(form.wtypeKw1, AFXTransition.EQ,\
            469, self.trpic2,\
            MKUINT(FXWindow.ID_HIDE, SEL_COMMAND), None)

        self.addTransition(form.wtypeKw1, AFXTransition.EQ,\
            470, self.trpic1,\
            MKUINT(FXWindow.ID_HIDE, SEL_COMMAND), None)
        self.addTransition(form.wtypeKw1, AFXTransition.EQ,\
            470, self.trpic2,\
            MKUINT(FXWindow.ID_SHOW, SEL_COMMAND), None)

        # show Lable,Button
        self.addTransition(form.wtypeKw1, AFXTransition.EQ,\
            469, self.p2Label,\
            MKUINT(FXWindow.ID_DISABLE, SEL_COMMAND), None)
        self.addTransition(form.wtypeKw1, AFXTransition.EQ,\
            469, self.AP2,\
            MKUINT(FXWindow.ID_DISABLE, SEL_COMMAND), None)

        self.addTransition(form.wtypeKw1, AFXTransition.EQ,\
            470, self.p2Label,\
            MKUINT(FXWindow.ID_ENABLE, SEL_COMMAND), None)
        self.addTransition(form.wtypeKw1, AFXTransition.EQ,\
            470, self.AP2,\
            MKUINT(FXWindow.ID_ENABLE, SEL_COMMAND), None)
        
        tabItem = FXTabItem(p=TabBook_1, text='A.M. Model', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_4 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        HFrame_3 = FXHorizontalFrame(p=TabItem_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        #FXCheckButton(p=HFrame_3, text='Enable A.M. Processing', tgt=form.EnAMKw, sel=0)
        #HFrame_4 = FXHorizontalFrame(p=HFrame_3, opts=0, x=0, y=0, w=0, h=0,
        #    pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_3, text='Activate elements by:', opts=JUSTIFY_LEFT)
        FXRadioButton(p=HFrame_3, text='Box', tgt=form.EltypeKw1, sel=471)
        FXRadioButton(p=HFrame_3, text='Label', tgt=form.EltypeKw1, sel=472)

        HFrame_4 = FXHorizontalFrame(p=TabItem_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        VFrame_1 = FXVerticalFrame(p=HFrame_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0) 
        
        
        GroupBox_3 = FXGroupBox(p=VFrame_1, text='Settings:', opts=FRAME_GROOVE)
        VAligner_4 = AFXVerticalAligner(p=GroupBox_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        self.PreName=AFXTextField(p=VAligner_4, ncols=10, labelText='PreStepName:', tgt=form.PreStepNameKw, sel=0)
        self.FirstName=AFXTextField(p=VAligner_4, ncols=10, labelText='FirstA.M.Step:', tgt=form.FirstAMstepKw, sel=0)
        self.Current=AFXTextField(p=VAligner_4, ncols=10, labelText='CurrentPass:', tgt=form.CurrentPassKw, sel=0)
        self.Length=AFXTextField(p=VAligner_4, ncols=10, labelText='PassLength(mm):', tgt=form.LengthKw, sel=0)
        self.Layers=AFXTextField(p=VAligner_4, ncols=10, labelText='LayersPerInc:', tgt=form.LayersKw, sel=0)
        self.Space=AFXTextField(p=VAligner_4, ncols=10, labelText='LayerLength(mm):', tgt=form.SpaceKw, sel=0)
        self.Eles=AFXTextField(p=VAligner_4, ncols=10, labelText='ElesPerLayer:', tgt=form.ElesKw, sel=0)
        self.BEle=AFXTextField(p=VAligner_4, ncols=10, labelText='BeginEleLabel:', tgt=form.BEleKw, sel=0)
        fileName = os.path.join(thisDir, 'AM.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_4, text='', ic=icon)
        ## add transition Enable
        self.addTransition(form.EltypeKw1,AFXTransition.EQ,\
                472,self.BEle,\
                MKUINT(FXWindow.ID_ENABLE, SEL_COMMAND), None)
        self.addTransition(form.EltypeKw1,AFXTransition.EQ,\
                472,self.Eles,\
                MKUINT(FXWindow.ID_ENABLE, SEL_COMMAND), None)
        ## add disable
        self.addTransition(form.EltypeKw1,AFXTransition.EQ,\
                471,self.BEle,\
                MKUINT(FXWindow.ID_DISABLE, SEL_COMMAND), None)
        self.addTransition(form.EltypeKw1,AFXTransition.EQ,\
                471,self.Eles,\
                MKUINT(FXWindow.ID_DISABLE, SEL_COMMAND), None)
        self.addTransition(form.EltypeKw1,AFXTransition.EQ,\
                472,self.Space,\
                MKUINT(FXWindow.ID_DISABLE, SEL_COMMAND), None)
###########################################################################
# Class definition
###########################################################################

class AMFlux10DBPickHandler(AFXProcedure):

        count = 0

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def __init__(self, form, keyword1,keyword2, prompt, entitiesToPick, numberToPick, highlightLevel, label):

                self.form = form
                self.keyword1 = keyword1
                self.keyword2 = keyword2
                self.prompt = prompt
                self.entitiesToPick = entitiesToPick # Enum value
                self.numberToPick = numberToPick # Enum value
                self.label = label
                self.labelText = label.getText()
                self.highlightLevel = highlightLevel

                AFXProcedure.__init__(self, form.getOwner())

                AMFlux10DBPickHandler.count += 1
                self.setModeName('AMFlux10DBPickHandler%d' % (AMFlux10DBPickHandler.count) )

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def getFirstStep(self):
                #self.keyword.setValueToDefault(True)
                step = AFXPickStep(self, self.keyword1, self.prompt, 
                    self.entitiesToPick, self.numberToPick, self.highlightLevel, sequenceStyle=TUPLE)
                step.addPointKeyIn(self.keyword2)
                return  step

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def getNextStep(self, previousStep):

                self.label.setText( self.labelText.replace('None', 'Picked') )
                return None
