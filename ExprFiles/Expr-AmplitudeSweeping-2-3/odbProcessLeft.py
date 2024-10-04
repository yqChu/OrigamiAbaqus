from abaqus import *
from abaqusConstants import *
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()

session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=186.546569824219, 
    height=132.183700561523)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
for amp_id in range(10):
    o1 = session.openOdb(
    name=f'C:/Research/Nonreciprocity/OrigamiAbaqus/ExprFiles/Expr-AmplitudeSweeping-2-3/LeftLoadFreq=200Amp={amp_id+1}hor_num=5.odb'
    )
    odb = session.odbs[f'C:/Research/Nonreciprocity/OrigamiAbaqus/ExprFiles/Expr-AmplitudeSweeping-2-3/LeftLoadFreq=200Amp={amp_id+1}hor_num=5.odb']
    xy1 = xyPlot.XYDataFromHistory(odb=odb,
                outputVariableName='Spatial displacement: U2 PI: PART-126-1 Node 1',
                steps=('Step-1', ), suppressQuery=True, __linkedVpName__='Viewport: 1')
    x0 = session.xyDataObjects['_temp_1']
    session.writeXYReport(
        fileName=f'C:/Research/Nonreciprocity/OrigamiAbaqus/PostProcess/Expr-2-3-f=200-AmplitudeSweeping/LeftLoadDispFreq=200Amp={amp_id+1}hor_num=5.txt', 
        xyData=(x0, ))
    del session.xyDataObjects['_temp_1']
    xy2 = xyPlot.XYDataFromHistory(odb=odb,
                outputVariableName='Spatial velocity: V2 PI: PART-126-1 Node 1',
                steps=('Step-1', ), suppressQuery=True, __linkedVpName__='Viewport: 1')
    x0 = session.xyDataObjects['_temp_1']
    session.writeXYReport(
        fileName=f'C:/Research/Nonreciprocity/OrigamiAbaqus/PostProcess/Expr-2-3-f=200-AmplitudeSweeping/LeftLoadVelFreq=200Amp={amp_id+1}hor_num=5.txt',
        xyData=(x0, ))
    del session.xyDataObjects['_temp_1']

    o1 = session.openOdb(
    name=f'C:/Research/Nonreciprocity/OrigamiAbaqus/ExprFiles/Expr-AmplitudeSweeping-2-3/RightLoadFreq=200Amp={amp_id+1}hor_num=5.odb'
    )
    odb = session.odbs[f'C:/Research/Nonreciprocity/OrigamiAbaqus/ExprFiles/Expr-AmplitudeSweeping-2-3/RightLoadFreq=200Amp={amp_id+1}hor_num=5.odb']
    xy1 = xyPlot.XYDataFromHistory(odb=odb,
                outputVariableName='Spatial displacement: U2 PI: PART-9-1 Node 5',
                steps=('Step-1', ), suppressQuery=True, __linkedVpName__='Viewport: 1')
    x0 = session.xyDataObjects['_temp_1']
    session.writeXYReport(
        fileName=f'C:/Research/Nonreciprocity/OrigamiAbaqus/PostProcess/Expr-2-3-f=200-AmplitudeSweeping/RightLoadDispFreq=200Amp={amp_id+1}hor_num=5.txt', 
        xyData=(x0, ))
    del session.xyDataObjects['_temp_1']
    xy2 = xyPlot.XYDataFromHistory(odb=odb,
                outputVariableName='Spatial velocity: V2 PI: PART-9-1 Node 5',
                steps=('Step-1', ), suppressQuery=True, __linkedVpName__='Viewport: 1')
    x0 = session.xyDataObjects['_temp_1']
    session.writeXYReport(
        fileName=f'C:/Research/Nonreciprocity/OrigamiAbaqus/PostProcess/Expr-2-3-f=200-AmplitudeSweeping/RightLoadVelFreq=200Amp={amp_id+1}hor_num=5.txt',
        xyData=(x0, ))
    del session.xyDataObjects['_temp_1']