#!/usr/bin/python
#
# Created: 
#    Kuang Yaming.
# Last Modified: 
#    4 Mar. 2011
# 
import os
import sys
import getopt
def Usage():
	print('SepBuild.py [-v] [SourceDir] DestDir')

opts,args = getopt.getopt(sys.argv[1:], 'vh', ['verbose', 'help'])

# Turn off verbose by default
verbose = 0

for opt,arg in opts:
	if opt in ('-h', '--help'):
		Usage()
	if opt in ('-v', '--verbose'):
		print ('Verbose mode enabled')
		verbose = 1

if len(args)==0:
	Usage()
if len(args)==1:
	srcdir = os.getcwd()
	dstdir = os.path.realpath(args[0])
else:
 	srcdir = os.path.realpath(args[0])
 	dstdir = os.path.realpath(args[1])

if verbose:
	print('Linking %(str1)s to %(str2)s ...'%{"str1":srcdir, "str2":dstdir}) 

if not os.path.isdir(srcdir):
	print('Error: src argument:%(str1)s is not a directory'%{"str1":srcdir})
	Usage()
if os.path.abspath(srcdir) == os.path.abspath(dstdir):
	print('Error: source and destination dir are the same')
	Usage()

if os.path.exists(dstdir):
	print('dest dir:%(str1)s already exists.'%{"str1":dstdir})
else:
	os.makedirs(dstdir)

dstlinked = dstdir + '/.py2link'
os.chdir(srcdir)
# find all the files under srcdir and store full path to dstlinked (file: .py2link);
# Only store full path of files, dirs alone will NOT be stored.
os.system("find %s \! -type d  -print | sort > %s 2>&1" % (srcdir, dstlinked))

def ProcessFile(srcfile, dstfile):
	if os.path.exists(dstfile):
		if os.path.islink(dstfile):
			# dstfile is a link
			linkTarget = os.path.realpath(dstfile)
			if os.path.islink(srcfile):
				# srcfile is also a link
				srclinkTgt = os.readlink(srcfile)
				dstlinkTgt = os.readlink(dstfile)
				if srclinkTgt != dstlinkTgt:
					# re-set dstfile to the real link of srcfile
					print('Correcting link: %(str1)s'%{"str1":dstfile})
					os.unlink(dstfile)
					os.symlink(srclinkTgt, dstfile)
		else:
			# blow away file and replace by link
			print('removing file: %(str1)s'%{"str1":dstfile})
			savefname = '%(str1).%(str2)s'%{"str1":dstfile, "str2":"p4link"}
			print('file %(str1)s was not a link. Moving file out of way to %(str2)s'%{"str1":dstfile, "str2":savefname})
			os.rename(dstfile, savefname)
			os.symlink(srcfile, dstfile)
	else:
		# no previous file, just create link directly
		link_srcfile = srcfile
		if os.path.islink(srcfile):
			link_srcfile = os.readlink(srcfile)
		os.symlink(link_srcfile, dstfile)


def ProcessDir(srcdir, dstdir):
    # fpy2link has all the stuff to link ...
	fpy2link = open(dstlinked, 'r')
	entries = fpy2link.readlines()

	for entry in entries:
		last4chars = entry[len(entry)-5:len(entry)-1]
		if last4chars == '.swp': #skip file with *.swp
			print('Skip linking file: %(str1)s'%{"str1":entry})
			continue
		srcfile = entry.replace('\n', '')
		dstfile = srcfile.replace(srcdir, dstdir)
		thedstdir = os.path.dirname(dstfile)
		if not os.path.isdir(thedstdir):
            # Make the dir if not exist yet.
			os.makedirs(thedstdir)

		ProcessFile(srcfile, dstfile)
	fpy2link.close()

ProcessDir(srcdir, dstdir)
