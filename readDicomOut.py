import SimpleITK as sitk
import sys

"""if len(sys.argv) < 2:
    print("Usage: DicomImagePrintTags <input_file>")
    sys.exit(1)"""

path="C:\\Users\\jose\\Documents\\MetaDataPython\\08_out"

series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(path)
#print(series_IDs)
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
        print("123" ,reader.GetMetaData(tag))
        