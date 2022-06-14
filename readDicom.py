import SimpleITK as sitk
import sys

"""if len(sys.argv) < 2:
    print("Usage: DicomImagePrintTags <input_file>")
    sys.exit(1)"""

path="C:\\Users\\jose\\Documents\\MetaDataPython\\08"

series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(path)
print(series_IDs)
if not series_IDs:
    print("ERROR: given directory \""+path+"\" does not contain a DICOM series.")
    sys.exit(1)
series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(path, series_IDs[0])

reader = sitk.ImageFileReader()

tag = "0010|0010"
value = ""

for i, file_name in enumerate(series_file_names):
    reader.SetFileName(file_name)
    reader.LoadPrivateTagsOn()

    try:
        reader.ReadImageInformation()
    except:
        print(path, "has no image information")

    if reader.HasMetaDataKey(tag):
        #print(reader.GetMetaData(tag))
        pass

        #modkey = input("Modify: ")
        #print(str(reader.HasMetaDataKey[modkey]))

    """for k in reader.GetMetaDataKeys():
        v = reader.GetMetaData(k)
        print(f"({k}) = = \"{v}\"")"""

series_reader = sitk.ImageSeriesReader()
series_reader.SetFileNames(series_file_names)
series_reader.MetaDataDictionaryArrayUpdateOn()
series_reader.LoadPrivateTagsOn()
image3D = series_reader.Execute()

writer = sitk.ImageFileWriter()
writer.KeepOriginalImageUIDOn()

for i in range(image3D.GetDepth()):
    image_slice = image3D[:,:,i]
    
    if series_reader.HasMetaDataKey(i, tag):
        print(reader.GetMetaData(tag))
        image_slice.SetMetaData(tag, value)
    
    writer.SetFileName(".\\08_out\\"+str(i)+'.dcm')
    writer.Execute(image_slice)
sys.exit( 0 )