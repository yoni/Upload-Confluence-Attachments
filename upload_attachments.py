#!/usr/bin/python
# Facilities for creating a results page on the wiki, retrieving one, and uploading PNG attachments. 

import sys
import os
import re
import fnmatch

from xmlrpclib import Server, Binary

import argparse

parser = argparse.ArgumentParser(description='Upload attachments to confluence page.')

parser.add_argument("-s", "--server_url",
                      required=True,
                      help="confluence server xmlrpc url. e.g. https://some_confluence_site.com/rpc/xmlrpc")
parser.add_argument("-k", "--space_key",
                      required=True,
                      help="confluence space key.")
parser.add_argument("-u", "--user",
                      required=True,
                      help="confluence user name")
parser.add_argument("-p", "--page",
                      required=True,
                      help="confluence page title")
parser.add_argument("-f", "--file_path",
                      required=True,
                      help="Upload attachments from this path")
parser.add_argument("-r", "--regex",
                      required=True,
                      help="file name regex to match against. e.g. *.png")
parser.add_argument("-t", "--content_type",
                      required=True,
                      help="content type to set for upload. e.g. image/png")
parser.add_argument("-d", "--dry_run",
                      default=False,
                      const=True,
                      nargs="?",
                      help="find the page and print out the file names to upload, but don't actually upload.")

args = parser.parse_args()

print "Uploading images from %s to page: '%s'" % (args.file_path, args.page)

if args.dry_run:
  print "DRY RUN. Not actually uploading files." 

def get_token(server):
  import getpass
  password = getpass.getpass(prompt="Confluence Password: ")
  token = server.confluence1.login(args.user, password)
  return token

server = Server(args.server_url)
token = get_token(server)

def create_page():
  pagedata = {"title":args.page, "content":"Results", "space":args.space_key}
  page = server.confluence1.storePage(token, pagedata);
  print "Created a page:"
  return page

def upload_attachment(page, filename):
  attachment = {}
  attachment['fileName'] = os.path.basename(filename)
  attachment['contentType'] = content_type

  data = open(filename, 'rb').read()

  server.confluence2.addAttachment(token, page['id'], attachment, Binary(data))

page = server.confluence1.getPage(token, args.space_key, args.page)

for filename in os.listdir(args.file_path):
  if fnmatch.fnmatch(filename, args.regex):
    path = os.path.join(args.file_path, filename)
    print("Uploading %s" % path)
    if not args.dry_run:
       upload_attachment(page, path)

