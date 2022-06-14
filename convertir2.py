
import vtk


def MarchingCubes(image,threshold):
    '''
    http://www.vtk.org/Wiki/VTK/Examples/Cxx/Modelling/ExtractLargestIsosurface 
    '''
    mc = vtk.vtkMarchingCubes()
    mc.SetInputData(image)
    mc.ComputeNormalsOn()
    mc.SetValue(0, threshold)
    mc.Update()

    # To remain largest region
    confilter = vtk.vtkPolyDataConnectivityFilter()
    confilter.SetInputData(mc.GetOutput())
    confilter.SetExtractionModeToLargestRegion()
    confilter.Update()

    return confilter.GetOutput()

def sizeFilter(vtk_fitler):

    reduceData = vtk.vtkDecimatePro()
    reduceData.SetInputData(vtk_fitler)
    reduceData.SetTargetReduction(0.60)
    #reduceData.AttributeErrorMetricOn()
    reduceData.PreserveTopologyOn()
    #reduceData.VolumePreservationOff()
    reduceData.Update()

 
    return reduceData.GetOutput()

def smooth3d(vtk_smooth):
    
    smoothFilter = vtk.vtkWindowedSincPolyDataFilter()
    smoothFilter.SetInputData(vtk_smooth)
    smoothFilter.BoundarySmoothingOn()
    smoothFilter.FeatureEdgeSmoothingOn()
    smoothFilter.SetFeatureAngle(120.0)
    smoothFilter.SetPassBand(0.001)
    smoothFilter.SetNumberOfIterations(10)
    smoothFilter.NonManifoldSmoothingOn()
    smoothFilter.NormalizeCoordinatesOn()
    smoothFilter.Update()

    return smoothFilter.GetOutput()

def normals3d(vtk_normals):

    normalsFilter = vtk.vtkPolyDataNormals()
    normalsFilter.SetComputeCellNormals(1)
    normalsFilter.SetInputData(vtk_normals)
    normalsFilter.SplittingOff()
    normalsFilter.Update()


    return normalsFilter.GetOutput()


def depth3d(vtk_depth):
    camera = vtk.vtkCamera()
    depthFilter = vtk.vtkDepthSortPolyData()
    depthFilter.SetInputData(vtk_depth)
    depthFilter.SetDepthSortModeToFirstPoint()
    depthFilter.SortScalarsOn()
    #depthFilter.SetVector(150,-51,-250)
    depthFilter.SetDirection(75)
    depthFilter.SetDepthSortMode(100)
    depthFilter.SetCamera(camera)
    depthFilter.Update()


    return depthFilter.GetOutput()

def surfaceFilter(vtk_surface):
    alg = vtk.vtkFeatureEdges()
    alg.FeatureEdgesOff()
    alg.BoundaryEdgesOn()
    alg.NonManifoldEdgesOn()
    alg.SetInputDataObject(vtk_surface)
    alg.Update()



    return alg.GetOutput().GetNumberOfCells() < 1



def cleanFilter(vtk_clean):
    cFilter = vtk.vtkCleanPolyData()
    cFilter.SetInputData(vtk_clean)
    cFilter.Update()


    return cFilter.GetOutput()


def holeFilter(vtk_hole):

    resliceFilter = vtk.vtkImageReslice()
    resliceFilter.SetInputData(vtk_hole)
    resliceFilter.SetOutputSpacing(0.5, 0.5, 0.5)
    resliceFilter.SetInterpolationModeToCubic()
    resliceFilter.Update()

    return resliceFilter.GetOutput()



def delaunay3d(vtk_delaunay):
    dFilter = vtk.vtkImageData()
    dFilter.SetInputConnection(vtk_delaunay.GetImageData())
    dFilter.Update()

    return dFilter.GetOutput()
        
  
    """ 

    gauss = vtk.vtkImageGaussianSmooth()
    gauss.SetInputData(vtk_smooth)
    gauss.SetStandardDeviation(3.0,3.0,3.0)
    gauss.SetDimensionality(2)
    gauss.SetRadiusFactor(0.3)
    gauss.Update()
        
 
    """

    """ 
    smoothFilter = vtk.vtkWindowedSincPolyDataFilter()
    smoothFilter.SetInputData(mc.GetOutput())
    smoothFilter.SetNumberOfIterations(20)
    smoothFilter.SetPassBand(0.3)
    smoothFilter.SetFeatureAngle(180)
    smoothFilter.SetEdgeAngle(180)
    smoothFilter.Update()
    print(smoothFilter)
    print(type(smoothFilter))
    """

    """ 
    resliceFilter = vtk.vtkImageReslice()
    resliceFilter.SetInputData(image)
    resliceFilter.SetOutputSpacing(0.5, 0.5, 0.5)
    resliceFilter.SetInterpolationModeToCubic()
    print(resliceFilter)
    print(type(resliceFilter))
    resliceFilter.Update()
    """
    
    """ 
    smoothFilter = vtk.vtkSmoothPolyDataFilter()
    smoothFilter.SetInputData(mc.GetOutput())
    smoothFilter.SetNumberOfIterations(20)
    smoothFilter.SetRelaxationFactor(5)
    #smoothFilter.FeatureEdgeSmoothingOff()
    smoothFilter.FeatureEdgeSmoothingOn()
    smoothFilter.BoundarySmoothingOn()
    #smoothFilter.BoundarySmoothingOff()
    smoothFilter.Update()
    """
   
    

    
    


