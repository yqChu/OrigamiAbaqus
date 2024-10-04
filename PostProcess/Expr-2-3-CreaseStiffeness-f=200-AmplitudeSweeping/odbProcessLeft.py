from abaqus import *
from abaqusConstants import *
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()

session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=186.546569824219, 
    height=132.183700561523)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
for hor_num_id in range(3,4):
    for amp_id in range(10):
        o1 = session.openOdb(
        name=f'C:/Research/Nonreciprocity/OrigamiAbaqus/ExprFiles/Expr-AmplitudeSweeping-SameCS-hor_num={hor_num_id+1}/LeftLoadFreq=200Amp={amp_id+1}hor_num={hor_num_id+1}.odb'
        )
        odb = session.odbs[f'C:/Research/Nonreciprocity/OrigamiAbaqus/ExprFiles/Expr-AmplitudeSweeping-SameCS-hor_num={hor_num_id+1}/LeftLoadFreq=200Amp={amp_id+1}hor_num={hor_num_id+1}.odb']
        xy1 = xyPlot.XYDataFromHistory(odb=odb,
                    outputVariableName='Spatial displacement: U2 PI: PART-126-1 Node 1',
                    steps=('Step-1', ), suppressQuery=True, __linkedVpName__='Viewport: 1')
        x0 = session.xyDataObjects['_temp_1']
        session.writeXYReport(
            fileName=f'C:/Research/Nonreciprocity/OrigamiAbaqus/PostProcess/Expr-2-3-CreaseStiffeness-f=200-AmplitudeSweeping/LeftLoadDispFreq=200Amp={amp_id+1}hor_num={hor_num_id+1}.txt', 
            xyData=(x0, ))
        del session.xyDataObjects['_temp_1']
        xy2 = xyPlot.XYDataFromHistory(odb=odb,
                    outputVariableName='Spatial velocity: V2 PI: PART-126-1 Node 1',
                    steps=('Step-1', ), suppressQuery=True, __linkedVpName__='Viewport: 1')
        x0 = session.xyDataObjects['_temp_1']
        session.writeXYReport(
            fileName=f'C:/Research/Nonreciprocity/OrigamiAbaqus/PostProcess/Expr-2-3-CreaseStiffeness-f=200-AmplitudeSweeping/LeftLoadVelFreq=200Amp={amp_id+1}hor_num={hor_num_id+1}.txt',
            xyData=(x0, ))
        del session.xyDataObjects['_temp_1']

        o1 = session.openOdb(
        name=f'C:/Research/Nonreciprocity/OrigamiAbaqus/ExprFiles/Expr-AmplitudeSweeping-SameCS-hor_num={hor_num_id+1}/RightLoadFreq=200Amp={amp_id+1}hor_num={hor_num_id+1}.odb'
        )
        odb = session.odbs[f'C:/Research/Nonreciprocity/OrigamiAbaqus/ExprFiles/Expr-AmplitudeSweeping-SameCS-hor_num={hor_num_id+1}/RightLoadFreq=200Amp={amp_id+1}hor_num={hor_num_id+1}.odb']
        xy1 = xyPlot.XYDataFromHistory(odb=odb,
                    outputVariableName=f'Spatial displacement: U2 PI: PART-9-1 Node {hor_num_id+1}',
                    steps=('Step-1', ), suppressQuery=True, __linkedVpName__='Viewport: 1')
        x0 = session.xyDataObjects['_temp_1']
        session.writeXYReport(
            fileName=f'C:/Research/Nonreciprocity/OrigamiAbaqus/PostProcess/Expr-2-3-CreaseStiffeness-f=200-AmplitudeSweeping/RightLoadDispFreq=200Amp={amp_id+1}hor_num={hor_num_id+1}.txt', 
            xyData=(x0, ))
        del session.xyDataObjects['_temp_1']
        xy2 = xyPlot.XYDataFromHistory(odb=odb,
                    outputVariableName=f'Spatial velocity: V2 PI: PART-9-1 Node {hor_num_id+1}',
                    steps=('Step-1', ), suppressQuery=True, __linkedVpName__='Viewport: 1')
        x0 = session.xyDataObjects['_temp_1']
        session.writeXYReport(
            fileName=f'C:/Research/Nonreciprocity/OrigamiAbaqus/PostProcess/Expr-2-3-CreaseStiffeness-f=200-AmplitudeSweeping/RightLoadVelFreq=200Amp={amp_id+1}hor_num={hor_num_id+1}.txt',
            xyData=(x0, ))
        del session.xyDataObjects['_temp_1']