# TGB-Osborn-VR

This repository contains code samples used to curate the dataset for the repository of TGB Osborn (Koonamore) Vegetation Reserve, Photopoint Data  (https://portal.tern.org.au/metadata/TERN/05f37d50-935e-4a0a-b45e-cb1b606ce476)

## Ecoimages - add species data to the metadata of the published image

The images were published with the species data, based the published CSV file.
The code used to add the species information to the XMP metadata of the image, in included in the jupyter notebook `add_species_to_image.ipynb`

This code has been setup to run against the photo in the `photos` folder, resulting in a new, enhanced, image with the inclusion of the species information.

## Filenames – standardise image names

The script in the python file `Standardise_filenames_and_update_excel_file_list.py` copies the original image files into a new directory and standardises filenames to the format `photopointID_yyyymmdd_seqX.jpg`, removing film numbers, spaces (replacing with underscores), and temporary duplication markers (e.g. `_a`, `_b`), while updating the associated Excel file.

## Excel list – generate list of originals

The script in the python file `Create_filename_list_excel.py` creates an Excel file listing all `.jpg` images in a source directory and its subfolders, providing a record of all the filenames.

## Metadata – match images to records

The script in the python file `Insert_modified_filenames_into_metadata_excel_doc_in_seq_matching_date_pp.py` links the final image filenames to the metadata Excel file by matching photopoint ID and date (`YYYYMMDD` or `YYYYMM` if the day is unknown), filling up to four photo slots per entry, and saving the results to a new output file.
