# -*- coding: utf-8 -*-
from __future__ import absolute_import

__license__   = 'GPL v3'
__copyright__ = '2021, Jim Miller'
__docformat__ = 'restructuredtext en'

import logging
logger = logging.getLogger(__name__)

import sys, re, os, traceback
from collections import defaultdict
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED, BadZipFile
from xml.dom.minidom import parseString
import collections
#from datetime import datetime

# py2 vs py3 transition
from .six import ensure_text, text_type as unicode
from .six import string_types as basestring
from . import exceptions
from io import BytesIO

import json
import bs4

from .htmlcleanup import stripHTML

class TransCache(object):

    def __init__(self,inpath=None):
        self.lastupdated = None

        self.storycache={
            'stories':{},
            'files':{},
            }

        if inpath:
            self.add_inputs(inpath)

    def get_stories(self):
        return self.storycache['stories']

    def get_story_urls(self):
        return self.get_stories().keys()

    def get_story(self,url):
        ## basic dict structure, not a class in anticipation of
        ## passing to calibre BG.
        return self.get_stories()[url]

    def write_json(self,outpath):
        with open(outpath,'w') as outfile:
            json.dump(self.storycache, outfile,
                      sort_keys=True, indent=2, separators=(',', ':'))

    # accept path & recurse
    def add_inputs(self,inpath):
        # logger.debug("add_inputs:%s"%inpath)
        if os.path.isdir(inpath):
            with os.scandir(inpath) as scandir:
                for f in scandir:
                    # logger.debug("add_inputs:scandir%s"%f)
                    if os.path.isdir(f):
                        self.add_inputs(f)
                    else:
                        self.add_input(f)
        else:
            self.add_input(inpath)

    # individual file.
    def add_input(self,infile):
        # logger.debug("add_input:%s"%infile.name)

        ## Will need a mechanism here to choose different Trans
        ## classes, if more ever show up.

        ## XXX compare timestamp of file to self.lastupdated.
        ## XXX record files & timestamps if ever allow updating
        ## XXX All proc'ed in memory at once at this point.

        try:
            transclass = TransWebToEpub(infile)
            # kept as primatives for json saving
            transdata = transclass.get_trans_data()
            storyUrl = transdata['metadata']['storyUrl']

            stories = self.get_stories()
            if storyUrl not in stories:
                stories[storyUrl]=transdata
            else:
                # logger.debug("\n\nmerge\n\n")
                existing = stories[storyUrl]
                ## if newer, update metadata.
                isnewer = transdata['filetimestamp'] > existing['filetimestamp']
                if isnewer:
                    ## check for continuing existence of filepath?
                    existing['filetimestamp']=transdata['filetimestamp']
                    existing['metadata']=transdata['metadata']
                    existing['chapters_order']=transdata['chapters_order']
                existing_chaps = existing['chapters']
                ## older file might still have chapters newer one doesn't.
                for co in transdata['chapters_order']:
                    c = transdata['chapters'][co]
                    if c['href'] is None: # not in file, skip.
                        continue
                    # doesn't exist, or has no href, or is newer, use this one
                    if c['chapurl'] not in existing_chaps or existing_chaps[c['chapurl']]['href'] is None or isnewer:
                        existing_chaps[c['chapurl']] = c


        except exceptions.TransFileUnsupported as e:
            logger.error("File (%s) is not supported:%s"%(infile.name,e))

    def make_transcache(self):
        pass

class TransFile(object):
    def __init__(self,filepath):
        ##
        self.filepath = os.path.abspath(filepath)
        self.filetimestamp = os.path.getmtime(filepath)
        self.rawinfo = None
        self.metadata = {}
        # index by chapter url, order by chapter order
        self.chapters = {}
        self.chapters_order = []

    def set_metadata(self,key,val):
        self.metadata[key]=val

    def get_metadata(self,key,default=None):
        return self.metadata.get(key,default)

    def set_chapter(self,url,item):
        self.chapters[url]=item
        self.chapters_order.append(url)

    def check_supported(self):
        raise exceptions.TransFileUnsupported('File is given is unsupported')

    def get_trans_data(self):
        return {
            ## make filepath (& timestamp?) a list?
            # 'filepath':self.filepath,
            'filetimestamp':self.filetimestamp,
            'rawinfo':self.rawinfo,
            'metadata':self.metadata,
            'chapters':self.chapters,
            'chapters_order':self.chapters_order,
            }

class EpubManifestItem(dict):
    def __init__(self,href,id=None,toc=None,
                 data=None,chapurl=None,
                 epubpath=None):
        self['href']=href
        self['id']=id
        self['toc']=toc
        self['chapurl']=chapurl
        self['epubpath']=epubpath

class TransFromEpub(TransFile):
    def __init__(self,filepath):
        super().__init__(filepath)
        try:
            self.read_epub(filepath)
        except BadZipFile:
            exceptions.TransFileUnsupported('File is given is not(or bad) zip file')

    # mostly to shorten the calls.
    def get_tags(self,node,tag):
        # returns Node[]
        return node.getElementsByTagName(tag)

    def get_tag(self,node,tag):
        # returns Node
        return self.get_tags(node,tag)[0]

    def get_tag_string(self,node,tag):
        # returns string
        return self.get_node_string(self.get_tag(node,tag))

    def get_node_string(self,node):
        # returns string
        return ensure_text(node.firstChild.data)

    def read_epub(self,filepath):
        # works equally well with filepath as a path or a blob
        with ZipFile(filepath, 'r') as self.epub:
            epub = self.epub

            ## Find the .opf file.
            container = epub.read("META-INF/container.xml")
            containerdom = parseString(container)
            rootfilenodelist = self.get_tags(containerdom,"rootfile")
            rootfilename = rootfilenodelist[0].getAttribute("full-path")
            ## Save the path to the .opf file--hrefs inside it are relative to it.
            relpath = get_path_part(rootfilename)

            self.containdom = contentdom = parseString(epub.read(rootfilename))

            # logger.debug(contentdom.toprettyxml())

            ## sources list of (URL,id) tuples.
            self.sources = []
            self.firstmetadom = firstmetadom = self.get_tag(contentdom,"metadata")
            for src in self.get_tags(firstmetadom,"dc:source"):
                self.sources.append((self.get_node_string(src),src.getAttribute('id')))

            # logger.debug(self.sources)

            ##manifest 'list' of EpubManifestItem(href,id,TOC text) tuples
            self.manifest = collections.OrderedDict()
            self.tocdom = None
            # spin through the manifest--only place there are item tags.
            for item in self.get_tags(contentdom,"item"):
                filehref=relpath+item.getAttribute("href")
                ## content files
                if( item.getAttribute("media-type") == "application/xhtml+xml" ):
                    manitem = EpubManifestItem(filehref,item.getAttribute("id"))
                    self.manifest[manitem['href']]=manitem
                ## toc.ncx
                if( item.getAttribute("media-type") == "application/x-dtbncx+xml" ):
                    self.tocdom = parseString(epub.read(filehref))
            for contenttag in self.get_tags(self.tocdom,"content"):
                href=relpath+contenttag.getAttribute('src')
                if href in self.manifest:
                    self.manifest[href]['toc']=self.get_tag_string(
                        self.get_tag(contenttag.parentNode,'navLabel'),'text')
                    # logger.debug(self.manifest[href])
            # logger.debug(self.tocdom.toprettyxml())

            # check if supported file.  raises exception if not.  After
            # sources recorded to be able to check against source.
            self.check_supported()

            self.parse_title()
            self.parse_authors()

            self.parse_metadata()
            self.parse_chapters()

    def parse_title(self):
        self.set_metadata('title',
                          self.get_tag_string(self.firstmetadom,
                                              "dc:title"))

    def parse_authors(self):
        authors=[]
        # <dc:creator opf:file-as="Kaiimei" opf:role="aut">Kaiimei</dc:creator>
        # <dc:creator id="creator">Kaiimei</dc:creator>
        for c in self.get_tags(self.firstmetadom,"dc:creator"):
            if c.getAttribute('id') == 'creator' or c.getAttribute('opf:role') == 'aut':
                authors.append(self.get_node_string(c))
        self.set_metadata('author',authors)

class TransWebToEpub(TransFromEpub):
    def __init__(self,filepath):
        super().__init__(filepath)

    def is_webtoepub(self):
        # <dc:contributor opf:role="bkp">[https://github.com/dteviot/WebToEpub] (ver. 0.0.0.125)</dc:contributor>
        # <dc:contributor id="packingTool">[https://github.com/dteviot/WebToEpub] (ver. 0.0.0.125)</dc:contributor>
        for c in self.get_tags(self.firstmetadom,"dc:contributor"):
            if( (c.getAttribute('id') == 'packingTool' or
                 c.getAttribute('opf:role') == 'bkp')
                and 'WebToEpub' in self.get_node_string(c) ):
                return True
        return False

    def check_supported(self):
        # only fanfiction.net right now.
        if not self.is_webtoepub():
            raise exceptions.TransFileUnsupported('File is given is not WebToEpub epub')
        if 'fanfiction.net' not in self.sources[0][0]:
            raise exceptions.TransFileUnsupported('Only fanfiction.net WebToEpub epub supported')
        if 'OEBPS/Text/0000_Information.xhtml' not in self.manifest:
            raise exceptions.TransFileUnsupported('WebToEpub epub must have Information page')

    def parse_metadata(self):
        ## only supporting ffnet right now.  Could someday push more
        ## of this into the adapter maybe.

        ## only minimal metadata here: storyUrl, numChapters.

        # https://www.fanfiction.net/s/13278343/3/The-Timeless-Vault-HP-travel
        url = self.sources[0][0]
        self.set_metadata('storyId',url.split('/',)[4])
        self.set_metadata('storyUrl','https://www.fanfiction.net/s/'+
                          self.get_metadata('storyId')+'/1/')

        self.rawinfo = ensure_text(self.epub.read('OEBPS/Text/0000_Information.xhtml'))
        data = stripHTML(self.rawinfo)
        # logger.debug(data)
        # Chapters: 27 - Words: 198,260
        pre='Chapters: '
        post=' - Words:'
        numC = data[data.index(pre)+len(pre):data.index(post)+1]
        self.set_metadata('numChapters',numC)
        # logger.debug("\n\n"+self.get_metadata('numChapters')+"\n\n")

    def parse_chapters(self):
        ## WTE includes chapters URLs in dc:source's, but I want to
        ## make sure they are correctly associated with file name
        ## (from manifest) and chapter title(aka toc) from toc.ncx

        # make a hash of URL->id
        srcs = {}
        for s in self.sources:
            url = re.sub(r'^(https://www.fanfiction.net/s/\d+/\d+/).*$',r'\1',s[0])
            id = s[1][3:] # remove leading 'id.'
            srcs[url]=id

        # make a hash of id->EpubManifestItem
        manifest = {}
        for k in self.manifest.keys():
            m = self.manifest[k]
            manifest[m['id']] = m

        # logger.debug(srcs)
        urlpref = 'https://www.fanfiction.net/s/'+self.get_metadata('storyId')+'/'
        for i in range(1,1+int(self.get_metadata('numChapters'))):
            url = "%s%s/"%(urlpref,i)
            id = srcs.get(url,None)
            m = None
            try:
                m = manifest[srcs[url]]
                m['epubpath'] = self.filepath
            except KeyError:
                pass
            ## WTE puts a chapter dc:source to the info page, don't include it.
            if m is None or m['href'] == "OEBPS/Text/0000_Information.xhtml":
                m = EpubManifestItem(None)
            m['chapurl'] = url
            self.set_chapter(url,m)

def pretty_json(o):
    return json.dumps(o, sort_keys=True, indent=2, separators=(',', ':'))

def get_path_part(n):
    relpath = os.path.dirname(n)
    if( len(relpath) > 0 ):
        relpath=relpath+"/"
    return relpath

def make_soup(data):
    '''
    Convenience method for getting a bs4 soup.
    '''

    ## html5lib handles <noscript> oddly.  See:
    ## https://bugs.launchpad.net/beautifulsoup/+bug/1277464
    ## This should 'hide' and restore <noscript> tags.
    data = data.replace("noscript>","fff_hide_noscript>")

    ## soup and re-soup because BS4/html5lib is more forgiving of
    ## incorrectly nested tags that way.
    soup = bs4.BeautifulSoup(data,'html5lib')
    soup = bs4.BeautifulSoup(unicode(soup),'html5lib')

    for ns in soup.find_all('fff_hide_noscript'):
        ns.name = 'noscript'

    return soup

def get_epub_file(epubpath,filehref):
    data = None
    with ZipFile(epubpath, 'r') as epub:
        data = ensure_text(epub.read(filehref))
        logger.debug("Found %s in %s"%(filehref,epubpath))
    return data
