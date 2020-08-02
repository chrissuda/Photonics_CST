'# MWS Version: Version 2018.0 - Oct 26 2017 - ACIS 27.0.2 -

'# length = nm
'# frequency = PHz
'# time = ns
'# frequency range: fmin = 0.14989622899999996 fmax = 0.59958491599999986
'# created = '[VERSION]2018.0|27.0.2|20171026[/VERSION]


'@ use template: FSS, Metamaterial - Unit Cell_1.cfg

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
'set the units
With Units
    .Geometry "nm"
    .Frequency "PHz"
    .Voltage "V"
    .Resistance "Ohm"
    .Inductance "H"
    .TemperatureUnit  "Kelvin"
    .Time "ns"
    .Current "A"
    .Conductance "Siemens"
    .Capacitance "F"
End With
'----------------------------------------------------------------------------
Plot.DrawBox True
With Background
     .Type "Normal"
     .Epsilon "1.0"
     .Mu "1.0"
     .Rho "1.204"
     .ThermalType "Normal"
     .ThermalConductivity "0.026"
     .HeatCapacity "1.005"
     .XminSpace "0.0"
     .XmaxSpace "0.0"
     .YminSpace "0.0"
     .YmaxSpace "0.0"
     .ZminSpace "0.0"
     .ZmaxSpace "0.0"
End With
' define Floquet port boundaries
With FloquetPort
     .Reset
     .SetDialogTheta "0"
     .SetDialogPhi "0"
     .SetSortCode "+beta/pw"
     .SetCustomizedListFlag "False"
     .Port "Zmin"
     .SetNumberOfModesConsidered "2"
     .Port "Zmax"
     .SetNumberOfModesConsidered "2"
End With
MakeSureParameterExists "theta", "0"
SetParameterDescription "theta", "spherical angle of incident plane wave"
MakeSureParameterExists "phi", "0"
SetParameterDescription "phi", "spherical angle of incident plane wave"
' define boundaries, the open boundaries define floquet port
With Boundary
     .Xmin "unit cell"
     .Xmax "unit cell"
     .Ymin "unit cell"
     .Ymax "unit cell"
     .Zmin "expanded open"
     .Zmax "expanded open"
     .Xsymmetry "none"
     .Ysymmetry "none"
     .Zsymmetry "none"
     .XPeriodicShift "0.0"
     .YPeriodicShift "0.0"
     .ZPeriodicShift "0.0"
     .PeriodicUseConstantAngles "False"
     .SetPeriodicBoundaryAngles "theta", "phi"
     .SetPeriodicBoundaryAnglesDirection "inward"
     .UnitCellFitToBoundingBox "True"
     .UnitCellDs1 "0.0"
     .UnitCellDs2 "0.0"
     .UnitCellAngle "90.0"
End With
' set tet mesh as default
With Mesh
     .MeshType "Tetrahedral"
End With
' FD solver excitation with incoming plane wave at Zmax
With FDSolver
     .Reset
     .Stimulation "List", "List"
     .ResetExcitationList
     .AddToExcitationList "Zmax", "TE(0,0);TM(0,0)"
     .LowFrequencyStabilization "False"
End With
'----------------------------------------------------------------------------
'change problem type
ChangeProblemType "Optical"
'set the wavelength range
Solver.WavelengthRange "500", "2000"
CreateResultTemplate( "Optical", "Convert all 1D Results from Frequency To Wavelength", True, "M1DC", "" )
CreateResultTemplate( "Optical", "Calculate Reflectance Transmittance and Absorbance", True, "M1DC", "" )
'----------------------------------------------------------------------------
With MeshSettings
     .SetMeshType "Tet"
     .Set "Version", 1%
End With
With Mesh
     .MeshType "Tetrahedral"
End With
'set the solver type
ChangeSolverType("HF Frequency Domain")

'@ define material: Aluminum

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
With Material
     .Reset
     .Name "Aluminum"
     .Folder ""
.FrqType "static"
.Type "Normal"
.SetMaterialUnit "Hz", "mm"
.Epsilon "1"
.Mu "1.0"
.Kappa "3.56e+007"
.TanD "0.0"
.TanDFreq "0.0"
.TanDGiven "False"
.TanDModel "ConstTanD"
.KappaM "0"
.TanDM "0.0"
.TanDMFreq "0.0"
.TanDMGiven "False"
.TanDMModel "ConstTanD"
.DispModelEps "None"
.DispModelMu "None"
.DispersiveFittingSchemeEps "General 1st"
.DispersiveFittingSchemeMu "General 1st"
.UseGeneralDispersionEps "False"
.UseGeneralDispersionMu "False"
.FrqType "all"
.Type "Lossy metal"
.MaterialUnit "Frequency", "GHz"
.MaterialUnit "Geometry", "mm"
.MaterialUnit "Time", "s"
.MaterialUnit "Temperature", "Kelvin"
.Mu "1.0"
.Sigma "3.56e+007"
.Rho "2700.0"
.ThermalType "Normal"
.ThermalConductivity "237.0"
.HeatCapacity "0.9"
.MetabolicRate "0"
.BloodFlow "0"
.VoxelConvection "0"
.MechanicsType "Isotropic"
.YoungsModulus "69"
.PoissonsRatio "0.33"
.ThermalExpansionRate "23"
.ReferenceCoordSystem "Global"
.CoordSystemType "Cartesian"
.NLAnisotropy "False"
.NLAStackingFactor "1"
.NLADirectionX "1"
.NLADirectionY "0"
.NLADirectionZ "0"
.Colour "1", "1", "0"
.Wireframe "False"
.Reflection "False"
.Allowoutline "True"
.Transparentoutline "False"
.Transparency "0"
.Create
End With

'@ new component: component1

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Component.New "component1"

'@ define brick: component1:BOTTOM

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
With Brick
     .Reset 
     .Name "BOTTOM" 
     .Component "component1" 
     .Material "Aluminum" 
     .Xrange "-w/2", "w/2" 
     .Yrange "-w/2", "w/2" 
     .Zrange "0", "h" 
     .Create
End With

'@ pick face

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Pick.PickFaceFromId "component1:BOTTOM", "1"

'@ align wcs with face

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
WCS.AlignWCSWithSelected "Face"

'@ define material: Paper

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
With Material
     .Reset
     .Name "Paper"
     .Folder ""
.FrqType "all"
.Type "Normal"
.SetMaterialUnit "GHz", "mm"
.Epsilon "2.31"
.Mu "1"
.Kappa "0"
.TanD "0.0"
.TanDFreq "0.0"
.TanDGiven "False"
.TanDModel "ConstTanD"
.KappaM "0"
.TanDM "0.0"
.TanDMFreq "0.0"
.TanDMGiven "False"
.TanDMModel "ConstTanD"
.DispModelEps "None"
.DispModelMu "None"
.DispersiveFittingSchemeEps "General 1st"
.DispersiveFittingSchemeMu "General 1st"
.UseGeneralDispersionEps "False"
.UseGeneralDispersionMu "False"
.Rho "800"
.ThermalType "Normal"
.ThermalConductivity "0.05"
.HeatCapacity "1.4"
.Colour "1", "0", "0"
.Wireframe "False"
.Transparency "0"
.Create
End With

'@ define brick: component1:middle

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
With Brick
     .Reset 
     .Name "middle" 
     .Component "component1" 
     .Material "Paper" 
     .Xrange "-w/2", "w/2" 
     .Yrange "-w/2", "w/2" 
     .Zrange "0", "h/2" 
     .Create
End With

'@ pick face

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Pick.PickFaceFromId "component1:middle", "1"

'@ define torus: component1:top

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
With Torus 
     .Reset 
     .Name "top" 
     .Component "component1" 
     .Material "Paper" 
     .OuterRadius "w/2" 
     .InnerRadius "w/4" 
     .Axis "z" 
     .Xcenter "0" 
     .Ycenter "0" 
     .Zcenter "h/2" 
     .Segments "0" 
     .Create 
End With

'@ clear picks

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Pick.ClearAllPicks

'@ delete shape: component1:top

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Solid.Delete "component1:top"

'@ pick face

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Pick.PickFaceFromId "component1:middle", "1"

'@ define torus: component1:top

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
With Torus 
     .Reset 
     .Name "top" 
     .Component "component1" 
     .Material "Aluminum" 
     .OuterRadius "w/2" 
     .InnerRadius "w/4" 
     .Axis "z" 
     .Xcenter "0" 
     .Ycenter "0" 
     .Zcenter "3.5" 
     .Segments "0" 
     .Create 
End With

'@ delete shape: component1:top

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Solid.Delete "component1:top"

'@ pick face

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Pick.PickFaceFromId "component1:middle", "1"

'@ define torus: component1:top

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
With Torus 
     .Reset 
     .Name "top" 
     .Component "component1" 
     .Material "Aluminum" 
     .OuterRadius "w/2" 
     .InnerRadius "w/4" 
     .Axis "z" 
     .Xcenter "-2.2" 
     .Ycenter "-1.6" 
     .Zcenter "0" 
     .Segments "0" 
     .Create 
End With

'@ delete shape: component1:top

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Solid.Delete "component1:top"

'@ pick face

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Pick.PickFaceFromId "component1:middle", "1"

'@ define torus: component1:solid1

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
With Torus 
     .Reset 
     .Name "solid1" 
     .Component "component1" 
     .Material "Paper" 
     .OuterRadius "w/2" 
     .InnerRadius "w/4" 
     .Axis "z" 
     .Xcenter "1" 
     .Ycenter "1" 
     .Zcenter "0" 
     .Segments "0" 
     .Create 
End With

'@ delete shape: component1:solid1

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Solid.Delete "component1:solid1"

'@ pick face

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Pick.PickFaceFromId "component1:middle", "1"

'@ define torus: component1:solid1

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
With Torus 
     .Reset 
     .Name "solid1" 
     .Component "component1" 
     .Material "Aluminum" 
     .OuterRadius "w/2" 
     .InnerRadius "w/4" 
     .Axis "z" 
     .Xcenter "0" 
     .Ycenter "0" 
     .Zcenter "h/2" 
     .Segments "0" 
     .Create 
End With

'@ clear picks

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Pick.ClearAllPicks

'@ switch bounding box

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Plot.DrawBox "False"

'@ change solver type

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
ChangeSolverType "HF Frequency Domain"

'@ define frequency domain solver parameters

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Mesh.SetCreator "High Frequency" 
With FDSolver
     .Reset 
     .SetMethod "Tetrahedral", "General purpose" 
     .OrderTet "Second" 
     .OrderSrf "First" 
     .Stimulation "List", "List" 
     .ResetExcitationList 
     .AddToExcitationList "Zmax", "TE(0,0);TM(0,0)" 
     .AutoNormImpedance "False" 
     .NormingImpedance "50" 
     .ModesOnly "False" 
     .ConsiderPortLossesTet "True" 
     .SetShieldAllPorts "False" 
     .AccuracyHex "1e-6" 
     .AccuracyTet "1e-4" 
     .AccuracySrf "1e-3" 
     .LimitIterations "False" 
     .MaxIterations "0" 
     .SetCalcBlockExcitationsInParallel "True", "True", "" 
     .StoreAllResults "False" 
     .StoreResultsInCache "False" 
     .UseHelmholtzEquation "True" 
     .LowFrequencyStabilization "False" 
     .Type "Auto" 
     .MeshAdaptionHex "False" 
     .MeshAdaptionTet "True" 
     .AcceleratedRestart "True" 
     .FreqDistAdaptMode "Distributed" 
     .NewIterativeSolver "True" 
     .TDCompatibleMaterials "False" 
     .ExtrudeOpenBC "False" 
     .SetOpenBCTypeHex "Default" 
     .SetOpenBCTypeTet "Default" 
     .AddMonitorSamples "True" 
     .CalcStatBField "False" 
     .CalcPowerLoss "True" 
     .CalcPowerLossPerComponent "False" 
     .StoreSolutionCoefficients "True" 
     .UseDoublePrecision "False" 
     .UseDoublePrecision_ML "True" 
     .MixedOrderSrf "False" 
     .MixedOrderTet "False" 
     .PreconditionerAccuracyIntEq "0.15" 
     .MLFMMAccuracy "Default" 
     .MinMLFMMBoxSize "0.3" 
     .UseCFIEForCPECIntEq "True" 
     .UseFastRCSSweepIntEq "false" 
     .UseSensitivityAnalysis "False" 
     .RemoveAllStopCriteria "Hex"
     .AddStopCriterion "All S-Parameters", "0.01", "2", "Hex", "True"
     .AddStopCriterion "Reflection S-Parameters", "0.01", "2", "Hex", "False"
     .AddStopCriterion "Transmission S-Parameters", "0.01", "2", "Hex", "False"
     .RemoveAllStopCriteria "Tet"
     .AddStopCriterion "All S-Parameters", "0.01", "2", "Tet", "True"
     .AddStopCriterion "Reflection S-Parameters", "0.01", "2", "Tet", "False"
     .AddStopCriterion "Transmission S-Parameters", "0.01", "2", "Tet", "False"
     .AddStopCriterion "All Probes", "0.05", "2", "Tet", "True"
     .RemoveAllStopCriteria "Srf"
     .AddStopCriterion "All S-Parameters", "0.01", "2", "Srf", "True"
     .AddStopCriterion "Reflection S-Parameters", "0.01", "2", "Srf", "False"
     .AddStopCriterion "Transmission S-Parameters", "0.01", "2", "Srf", "False"
     .SweepMinimumSamples "3" 
     .SetNumberOfResultDataSamples "1001" 
     .SetResultDataSamplingMode "Automatic" 
     .SweepWeightEvanescent "1.0" 
     .AccuracyROM "1e-4" 
     .AddSampleInterval "", "", "1", "Automatic", "True" 
     .AddSampleInterval "", "", "", "Automatic", "False" 
     .MPIParallelization "False"
     .UseDistributedComputing "False"
     .NetworkComputingStrategy "RunRemote"
     .NetworkComputingJobCount "3"
     .UseParallelization "True"
     .MaxCPUs "96"
     .MaximumNumberOfCPUDevices "2"
End With
With IESolver
     .Reset 
     .UseFastFrequencySweep "True" 
     .UseIEGroundPlane "False" 
     .SetRealGroundMaterialName "" 
     .CalcFarFieldInRealGround "False" 
     .RealGroundModelType "Auto" 
     .PreconditionerType "Auto" 
     .ExtendThinWireModelByWireNubs "False" 
End With
With IESolver
     .SetFMMFFCalcStopLevel "0" 
     .SetFMMFFCalcNumInterpPoints "6" 
     .UseFMMFarfieldCalc "True" 
     .SetCFIEAlpha "0.500000" 
     .LowFrequencyStabilization "False" 
     .LowFrequencyStabilizationML "True" 
     .Multilayer "False" 
     .SetiMoMACC_I "0.0001" 
     .SetiMoMACC_M "0.0001" 
     .DeembedExternalPorts "True" 
     .SetOpenBC_XY "True" 
     .OldRCSSweepDefintion "False" 
     .SetAccuracySetting "Custom" 
     .CalculateSParaforFieldsources "True" 
     .ModeTrackingCMA "True" 
     .NumberOfModesCMA "3" 
     .StartFrequencyCMA "-1.0" 
     .SetAccuracySettingCMA "Default" 
     .FrequencySamplesCMA "0" 
     .SetMemSettingCMA "Auto" 
End With

'@ change solver type

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
ChangeSolverType "HF Frequency Domain" 

'@ execute macro: Solver\F-Solver\FD-TET - Reference Impedance Settings

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
Dim bTET_FD_Impedance As Boolean
bTET_FD_Impedance = False

	FDSolver.SetUseImpLineImpedanceAsReference bTET_FD_Impedance


'@ set parametersweep options

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
With ParameterSweep
    .SetSimulationType "Frequency" 
End With 


'@ add parsweep sequence: Sequence 1

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
With ParameterSweep
     .AddSequence "Sequence 1" 
End With


'@ add parsweep parameter: Sequence 1:h

'[VERSION]2018.0|27.0.2|20171026[/VERSION]
With ParameterSweep
     .AddParameter_Linear "Sequence 1", "h", "3", "10", "7" 
End With


