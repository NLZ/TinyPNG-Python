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

  # Rename original file
  orig_path = args.input.name
  rename_path = orig_path
  args.input.close()  

  while True:
    try:
      rename_path_split = os.path.splitext(rename_path)
      rename_path = rename_path_split[0] + "_orig" + rename_path_split[1]
      os.rename(orig_path, rename_path)
      break
    except FileExistsError:
      print("File exist")

  # Name the new one as the original
  open(orig_path, "wb").write(result)

else:
  # Something went wrong! You can parse the JSON body for details.
  print("Compression failed")
  input("Press enter to continue")
