import skimage.io

import io, json, codecs

from IPython.display import Image



# Read image into scimage package

img = skimage.io.imread(sample_data_file_name)

skimage.io.imsave('original.png', img)



# Display original image

display(Image(filename='original.png',width=800, height=800))



from osgeo import gdal, osr

import numpy

from skimage.segmentation import felzenszwalb

from skimage.segmentation import mark_boundaries

from skimage.measure import regionprops

import csv



# Prepare result structure

result = {

    "trees": []

}



# Open image with gdal

ds = gdal.Open(sample_data_file_name)

xoff, a, b, yoff, d, e = ds.GetGeoTransform()



# Get projection information from source image

ds_proj = ds.GetProjectionRef()

ds_srs = osr.SpatialReference(ds_proj)



# Get the source image's geographic coordinate system (the 'GEOGCS' node of ds_srs)

geogcs = ds_srs.CloneGeogCS()



# Set up a transformation between projected coordinates (x, y) & geographic coordinates (lat, lon)

transform = osr.CoordinateTransformation(ds_srs, geogcs)



# Convert multi-channel image it into red, green and blueb[, alpha] channels

red, green, blue = numpy.rollaxis(numpy.array(img), axis=-1)

alpha = 0







# Mask: threshold + stops canny detecting image boundary edges

mask = blue > 240

mask1 = red < 90

mask2 = green < 200



# Create mask for edge detection

skimage.io.imsave('mask.png', mask * 255)

skimage.io.imsave('mask1.png', mask1 * 255)

skimage.io.imsave('mask2.png', mask2 * 255)





# Use Felzenszwalb algo to find segements

segments_fz = felzenszwalb(numpy.dstack((mask, mask1, mask2)),

                               scale=3700,

                               sigma=2,

                               min_size=4)









# Build labeled mask to show where trees were dectected

segmented_img = mark_boundaries(numpy.dstack((mask, mask1, mask2)), segments_fz)

skimage.io.imsave('mask_labeled.png', segmented_img)

segmented_img1 = mark_boundaries(mask1, segments_fz)

skimage.io.imsave('mask_labeled1.png', segmented_img1)

segmented_img2 = mark_boundaries(mask2, segments_fz)

skimage.io.imsave('mask_labeled2.png', segmented_img2)



# Count trees and save image of each tree clipped from masked image

k=0



for idx, tree in enumerate(regionprops(segments_fz)):



    # If area matches that of a stanard tree, count it

    if (tree.area >= 2 and tree.area <= 100):



        # Incrment count

        k+=1



        # Create tree thumbnail

        x, y = (int(numpy.average([tree.bbox[0],

                                tree.bbox[2]])),

                                int(numpy.average([tree.bbox[1],

                                tree.bbox[3]])))

        sx, ex = max(x - 35, 0), min(x + 35, img.shape[0] - 1)

        sy, ey = max(y - 35, 0), min(y + 35, img.shape[1] - 1)

        img_tree = img[sx:ex, sy:ey]

        skimage.io.imsave('tree-id_' + str(idx + 1) + '-count_' + str(k) +'.png', img_tree)



        # Get global coordinates from pixel x, y coords

        projected_x = a * y + b * x + xoff

        projected_y = d * y + e * x + yoff



        # Transform from projected x, y to geographic lat, lng

        (lat, lng, elev) = transform.TransformPoint(projected_x, projected_y)
        # Add tree to results cluster

        result["trees"].append({

            "id": idx + 1,

            "tree_count": k,

            "lat": lat,

            "lng": lng

        })
