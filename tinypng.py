# from os.path import dirname
import urllib.request
import base64
import argparse
import os.path

key = "<your api key>"

parser = argparse.ArgumentParser(description="Shrink PNGs with TinyPNG")
parser.add_argument("input", type=argparse.FileType("rb"), help="input PNG")
args = parser.parse_args()

request = urllib.request.Request("https://api.tinypng.com/shrink", args.input.read())

cafile = None
# Uncomment below if you have trouble validating our SSL certificate.
# Download cacert.pem from: http://curl.haxx.se/ca/cacert.pem
# cafile = dirname(__file__) + "/cacert.pem"

auth = base64.b64encode(bytes("api:" + key, "ascii")).decode("ascii")
request.add_header("Authorization", "Basic %s" % auth)

response = urllib.request.urlopen(request, cafile = cafile)
if response.status == 201:
  # Compression was successful, retrieve output from Location header.
  result = urllib.request.urlopen(response.getheader("Location"), cafile = cafile).read()

  # Output name based on input, check for existing one
  outpath = args.input.name
  splitpath = os.path.splitext(outpath)
  counter = 0
  while os.path.isfile(outpath):
    outpath = splitpath[0] + "(" + str(counter) + ")" + splitpath[1]
    counter = counter + 1

  open(outpath, "wb").write(result)
else:
  # Something went wrong! You can parse the JSON body for details.
  print("Compression failed")
