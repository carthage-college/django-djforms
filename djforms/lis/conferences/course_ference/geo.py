from pygeocoder import Geocoder
results = Geocoder.geocode("2001 alford park drive, kenosha wi, 53150")
print(results[0].coordinates)
