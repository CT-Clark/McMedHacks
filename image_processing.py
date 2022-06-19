from email import contentmanager
import os
import shutil
import pydicom
import glob
import numpy as np

project_dir = "Intro_to_image_processing"

list_dcm_path = glob.glob("Intro_to_image_processing/*.dcm")
print(f"My list contains {len(list_dcm_path)} elements. These are the 5 first: ")
for i in range(5):
    print(list_dcm_path[i])

my_dcm_file = pydicom.dcmread(list_dcm_path[0])
print(my_dcm_file)
print()

from pydicom.tag import Tag

# all of these tags are equivalent
t1 = Tag(0x00100010)
t2 = Tag(0x10,0x10)
t3 = Tag((0x10,0x10))
t4 = Tag("PatientName")
print(t1)
print(type(t1))
print(t1==t2, t2==t3, t3==t4)

print(my_dcm_file[0x10,0x10]) # Returns the whole DataElement
print(my_dcm_file.PatientName) # Returns the value
print(my_dcm_file[0x10,0x10].value) # Returns the value as well

print("As 'my_dcm_file[0x10,0x10]' is a DataElement, we can look at all its components:")
print(f"Value Multiplicity: {my_dcm_file[0x10,0x10].VM}")
print(f"Value Representation: {my_dcm_file[0x10,0x10].VR}")
print(f"Tag: {my_dcm_file[0x10,0x10].tag}")
print(f"Value: {my_dcm_file[0x10,0x10].value}\n")

print(type(my_dcm_file[0x10,0x10]))
print("==============")
print(my_dcm_file[0x10,0x10])
print()
# DataElement can contain sequences
print(type(my_dcm_file[0x0012, 0x0064]))
print("==========")
print(my_dcm_file[0x0012, 0x0064])
print()
# If we take the first element of this sequence we get another dataset
print(type(my_dcm_file[0x0012, 0x0064][0]))
print("==========")
print(my_dcm_file[0x0012, 0x0064][0])
print()

#Important tags
print(f"Storage object: {my_dcm_file.SOPClassUID.name}")
print(f"Image modality: {my_dcm_file.Modality}")
print(f"Image ID: {my_dcm_file.SOPInstanceUID.name}")
print(f"Treatment site: {my_dcm_file.BodyPartExamined}")
print(f"Image position: {my_dcm_file.ImagePositionPatient}")
print(f"Image height: {my_dcm_file.Rows}")
print(f"Image width: {my_dcm_file.Columns}")
print(f"Image spacings: {my_dcm_file.PixelSpacing}")
print()

# Can list DICOM into a dictionary
keywords = my_dcm_file.dir()
dic = dict()
for key in keywords:
    dic[key] = my_dcm_file[key]

# But then you will have to do it recursively because of the sequences
# objects that contain datasets
print(my_dcm_file[0x0012, 0x0064])

for key in keywords:
    print(key)

print()

print(my_dcm_file.PixelData)
print("==========")
print(type(my_dcm_file.PixelData))
print("==========")
print(my_dcm_file[0x7fe0, 0x0010])
print()

print(type(my_dcm_file.pixel_array))
print("==========")
print(my_dcm_file.pixel_array)
print("==========")
print(np.all(my_dcm_file.pixel_array==my_dcm_file[0x7fe0, 0x0010].value))
print()

print(my_dcm_file[0x7fe0, 0x0010].value) # Same as PixelData
print()

# Black pixels are not 0s. You might need to rescape your pixel array
print("To rescale your image from pixel values to Hounsfield Unit you can use the intercept " +
    f"({my_dcm_file.RescaleIntercept}) and the slope ({my_dcm_file.RescaleSlope}) present in the DICOM file")

import matplotlib.pyplot as plt

plt.figure(figsize=(15,10))
plt.imshow(my_dcm_file.pixel_array, cmap=plt.cm.bone)
plt.colorbar()
plt.title("My first opened CT image")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.show()

# Be careful on the axis dimensions (0 doesn't start at the same corner for both axis)
temp = my_dcm_file.pixel_array.copy()
temp[:200] = 18
plt.imshow(temp, cmap=plt.cm.bone)
plt.colorbar()
plt.title("My first opened CT image")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.show()

