import SimpleITK as sitk
import sys

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkCylinderSource

from myshow import *
from convertir import *
from convertir2 import *

"""if len(sys.argv) < 2:
    print("Usage: DicomImagePrintTags <input_file>")
    sys.exit(1)"""

path="C:\\Users\\josec\\OneDrive\\Desktop\\dam2\\metadatapython\\MetaDataPython\\08"

series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(path)#la primera funcion lee la imagen de la serie y la segunda coge todas la seriesIDS del DICOM data set
print(series_IDs)
if not series_IDs:
    print("ERROR: given directory \""+path+"\" does not contain a DICOM series.")
    sys.exit(1)
series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(path, series_IDs[0])#lee la imagen de la serie y la segunda recoge todos las series de los nombres de los archivos
reader = sitk.ImageFileReader()

#Son tags del paciente que queremos anonimizar
tag1 = "0010|0010"
tag2 = "0010|0020"
tag3 = "0010|0030"
tag4 = "0010|0040"
tag5 = "0010|1010"
tag6 = "0012|0062"
tag7 = "0012|0063"
value = ""
# i el contador y el file_name nos coge el nombre del archivo y series_file_names es la ruta del archivo
for i, file_name in enumerate(series_file_names):#Enumerador nos agrega un contador a un iterable y lo devuelve 
    reader.SetFileName(file_name)#Se utiliza para establecer el nombre del archivo antes de leer o escribir la imagen
    reader.LoadPrivateTagsOn()#Carga los tags

    try:
        reader.ReadImageInformation()#Funcion lee la informacion 
    except:
        print(path, "has no image information")#Aqui es donde lee la ruta del fichero y lee los ficheros 

    if reader.HasMetaDataKey(tag1):# Aqui es donde comprobamos que hemos si hay un identificar si hay un objeto
        #print(reader.GetMetaData(tag))
        pass


series_reader = sitk.ImageSeriesReader()
series_reader.SetFileNames(series_file_names)
series_reader.MetaDataDictionaryArrayUpdateOn()
series_reader.LoadPrivateTagsOn()#Carga los tags
image3D = series_reader.Execute()

writer = sitk.ImageFileWriter()
writer.KeepOriginalImageUIDOn()
print(image3D.GetDepth()) #Cantidad de imagenes
print(image3D.GetSize()) # Numero de cubos que existen y cantidad de imagenes que hay

vtk_img = sitk2vtk(image3D) #llamamos a la funcion sitk2vtk que nos convierte vtk(image3D)
print(vtk_img) #Y que nos imprima sus datos
print(type(vtk_img))#<class 'vtkmodules.vtkCommonDataModel.vtkImageData'>


#vtk_delaunay = delaunay3d(vtk_img)
#print(vtk_delaunay)
#print(type(vtk_delaunay))

#vtk_hole = holeFilter(vtk_img)
#print(vtk_hole)
#print(type(vtk_hole))

vtk_3d = MarchingCubes(vtk_img, 282)
print(vtk_3d) #Y que nos imprima sus datos
print(type(vtk_3d))#<class 'vtkmodules.vtkCommonDataModel.vtkPolyData'>


vtk_smooth = smooth3d(vtk_3d)
print(vtk_smooth)
print(type(vtk_smooth))

vtk_filter = sizeFilter(vtk_smooth)
print(vtk_filter)
print(type(vtk_filter))

vtk_depth = depth3d(vtk_filter)
print(vtk_depth)
print(type(vtk_depth))


vtk_clean = cleanFilter(vtk_depth)
print(vtk_clean)
print(type(vtk_clean))

vtk_normals = normals3d(vtk_clean)
print(vtk_normals)
print(type(vtk_normals))

#vtk_surface = surfaceFilter(vtk_normals)
#print(vtk_surface)
#print(type(vtk_surface))

#visualize_poly(poly)
writer = vtk.vtkSTLWriter()
writer.SetInputData(vtk_normals)
print(vtk_normals)
writer.SetFileName('dicomSmooth.stl')
writer.Update()


 ## Read and show STL
 # Read and display for verification
reader = vtk.vtkSTLReader()
reader.SetFileName('dicomSmooth.stl')
reader.Update()

jpegfile = "bones.jpg"

# Read the image data from a file
reader2 = vtk.vtkJPEGReader()
reader2.SetFileName(jpegfile)

# Create texture object
texture = vtk.vtkTexture()

if vtk.VTK_MAJOR_VERSION <= 5:
    texture.SetInput(reader2.GetOutput())
else:
    texture.SetInputConnection(reader2.GetOutputPort())


# Map texture coordinates
map_to_sphere = vtk.vtkTextureMapToSphere()
if vtk.VTK_MAJOR_VERSION <= 5:
    map_to_sphere.SetInput(reader.GetOutput())
else:
    map_to_sphere.SetInputConnection(reader.GetOutputPort())
map_to_sphere.PreventSeamOn()


#PolyDataMapper
mapper = vtk.vtkPolyDataMapper()

if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(map_to_sphere.GetOutput())
else:
    mapper.SetInputConnection(map_to_sphere.GetOutputPort())

# Create a sphere
cylinderSource = vtkCylinderSource()
cylinderSource.SetRadius(2.0)
cylinderSource.SetHeight(150.0)
cylinderSource.SetResolution(6)
cylinderSource.Update()

jpegfile2 = "screw.jpg"

# Read the image data from a file
reader3 = vtk.vtkJPEGReader()
reader3.SetFileName(jpegfile2)

# Create texture object
texture2 = vtk.vtkTexture()


if vtk.VTK_MAJOR_VERSION <= 5:
    texture2.SetInput(reader3.GetOutput())
else:
    texture2.SetInputConnection(reader3.GetOutputPort())

# Map texture coordinates
map_to_sphere2 = vtk.vtkTextureMapToSphere()
if vtk.VTK_MAJOR_VERSION <= 5:
    map_to_sphere2.SetInput(cylinderSource.GetOutput())
else:
    map_to_sphere2.SetInputConnection(cylinderSource.GetOutputPort())
map_to_sphere2.PreventSeamOn()

#PolyDataMapper
mapper2 = vtk.vtkPolyDataMapper()

if vtk.VTK_MAJOR_VERSION <= 5:
    mapper2.SetInput(map_to_sphere2.GetOutput())
else:
    mapper2.SetInputConnection(map_to_sphere2.GetOutputPort())


colors = vtk.vtkNamedColors()
actor2 = vtk.vtkActor()
actor2.SetMapper(mapper2)
actor2.SetTexture(texture2)
actor2.GetProperty().SetOpacity(0.99)
actor2.SetPosition(-2,-100,-340)
actor2.RotateX(-8)
  

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.SetTexture(texture)
actor.GetProperty().SetRoughness(0.0)
actor.GetProperty().SetOpacity(0.998)
actor.GetProperty().SetSpecular(0.2)
actor.GetProperty().SetInterpolationToFlat()


#actor.GetProperty().LightingOff()
#actor.GetProperty().SetSpecularPower(50)
#actor.GetProperty().SetOcclusionStrength(1.0)
#actor.GetProperty().SetColor(colors.GetColor3d('Bisque'))

    # Create a rendering window and renderer

ren = vtk.vtkRenderer()
ren.SetBackground(colors.GetColor3d("Silver"))
#ren.SetUseDepthPeelingForVolumes(True)
#ren.SetUseDepthPeeling(False)




renWin = vtk.vtkRenderWindow()
renWin.SetWindowName("DICOM EN 3D")
#renWin.SetAlphaBitPlanes(True)
#renWin.SetMultiSamples(4)
renWin.AddRenderer(ren)


    # Create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
 
    # Assign actor to the renderer
#ren.AddActor(actor)
ren.AddActor(actor2)
ren.AddActor(actor)

 
    # Enable user interface interactor
iren.Initialize()

renWin.Render()

print(ren.GetLastRenderingUsedDepthPeeling())
if (ren.GetLastRenderingUsedDepthPeeling()):
    print("depth peeling was used")
else:
    print("depth peeling was not used (alpha blending instead)")


iren.Start()






for i in range(image3D.GetDepth()): #Bucle for dentro del rango de las imagenes
    
    image_slice = image3D[:,::,i] #indicamos que recorra todas las imagenes en 3D

    image_slice = sitk.BinaryThreshold(image_slice, lowerThreshold=400, upperThreshold=1800, insideValue=1, outsideValue=0)#Filtro blanco y negro
    image_slice = sitk.BinaryFillhole(image_slice, fullyConnected=False, foregroundValue=1.0)#Rellena agujeros de la imagen
    image_slice = sitk.BinaryMorphologicalClosing(image_slice, (10,20), foregroundValue=1.0, safeBorder=True)#Mejora el relleno del objeto
    image_slice = sitk.BinaryGrindPeak(image_slice, fullyConnected=False, foregroundValue=1.0, backgroundValue=1)#Quita objetos que no estan conectados
    image_slice = sitk.CurvatureFlow(image_slice, timeStep=0.05, numberOfIterations=5) #Mejora la curvatura de la columna
    

    #image_slice = sitk.BinaryReconstructionByDilation(image_slice, image_slice, backgroundValue=0.0, foregroundValue=1.0, fullyConnected=False) 
    #image_slice = sitk.BinaryClosingByReconstruction(image_slice, (20,20), foregroundValue=1.0, fullyConnected=False)
    #image_slice = sitk.BinaryMinMaxCurvatureFlow(image_slice, timeStep=0.05, numberOfIterations=5, stencilRadius=2, threshold=0)
    #image_slice = sitk.BoxMean(image_slice, (5,1)) 
    
    #llamamos a la funcion myshow
    myshow(image_slice)



        #anonimiza los datos del paciente?
if series_reader.HasMetaDataKey(i, tag1):
    print(reader.GetMetaData(tag1))
    image_slice.SetMetaData(tag1, value)

    series_reader.HasMetaDataKey(i, tag2)
    print(reader.GetMetaData(tag2))
    image_slice.SetMetaData(tag2, value)
    
    series_reader.HasMetaDataKey(i, tag3)
    print(reader.GetMetaData(tag3))
    image_slice.SetMetaData(tag3, value)
    
    series_reader.HasMetaDataKey(i, tag4)
    print(reader.GetMetaData(tag4))
    image_slice.SetMetaData(tag4, value)

    series_reader.HasMetaDataKey(i, tag5)
    print(reader.GetMetaData(tag5))
    image_slice.SetMetaData(tag5, value)

    series_reader.HasMetaDataKey(i, tag6)
    print(reader.GetMetaData(tag6))
    image_slice.SetMetaData(tag6, value)

    series_reader.HasMetaDataKey(i, tag7)
    print(reader.GetMetaData(tag7))
    image_slice.SetMetaData(tag7, value)
      
   
    writer.SetFileName(".\\08_out2\\"+str(i)+'.dcm')#Creamos la carpeta y con el nuevo nombre y por ultimo el fichero DICOM
    

    
    writer.Execute(image_slice)#Aqui nos escribe la image_slice 



  
    
   
    
    sys.exit(0)#Salida limpia sin ningun problema y si es exit(1) significa cuando hay errores el programa se sale
        