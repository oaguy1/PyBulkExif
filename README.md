# PyBulkExif

## Main Program
```
usage: PyBulkExif [-h] {read,edit} ...

A TUI Python tool to bulk edit Exif photo data

positional arguments:
  {read,edit}
    read       Read Exif metadata and print to STDOUT
    edit       Bulk edit Exif data on images

options:
  -h, --help   show this help message and exit

Please file all bugs on GitHub
```

## Read
```
usage: PyBulkExif read [-h] images_dir

positional arguments:
  images_dir  Path to the directory containing the images to read Exif data from

options:
  -h, --help  show this help message and exit
```

## Edit
```
usage: PyBulkExif edit [-h] -E EXIF_DATA images_dir

positional arguments:
  images_dir            Path to the directory containing the images to have their Exif data set

options:
  -h, --help            show this help message and exit
  -E, --exif_data EXIF_DATA
                        Path to the YAML file containing the Exif data to be written
```
