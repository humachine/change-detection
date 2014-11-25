from tifffile import TiffFile
import sys
path_to_file=str(sys.argv[1])
print path_to_file
for page in TiffFile(path_to_file):
    for tag in page.tags.values():
        print tag.name, tag.code, tag.dtype, tag.count, tag.value
