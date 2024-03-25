import os
from typing import List
from ninja import NinjaAPI, Schema
from core.models import T_Feed
from lxml import etree
from django.conf import settings

greader = NinjaAPI()

class T_FeedSchema(Schema):
    id: str
    title: str
    url: str
    
    # language: str
    # status: str
    # modified: str

    @staticmethod
    def resolve_id(t_feed: T_Feed):
        return t_feed.sid
    
    @staticmethod
    def resolve_title(t_feed: T_Feed):
        return t_feed.o_feed.name

    @staticmethod
    def resolve_url(t_feed: T_Feed):
        return t_feed.o_feed.feed_url

class EntrySchema(Schema):
    id: str  
    title: str
    link: str
    published: str
    updated: str
    summary: str
    content: str
    author: str


@greader.get('/reader/api/0/subscription', response=List[T_FeedSchema])
def list_feeds(request):
    feeds = T_Feed.objects.filter(status=True).exclude(o_feed__name='Loading') #o_feed可能会因为网络问题导致失败，所以不能作为条件
    return feeds

@greader.get('/feeds/{feed_id}/entries', response=List[EntrySchema])  
def feed_entries(request, feed_id: str):
    file_path = os.path.join(settings.DATA_FOLDER, 'feeds', feed_id + '.xml')
    if not os.path.exists(file_path):
        return []

    parser = etree.XMLParser(ns_clean=True, recover=True)
    tree = etree.parse(file_path, parser=parser)
    root = tree.getroot()

    entries = []
    for entry in root.xpath('//atom:entry', namespaces={'atom': 'http://www.w3.org/2005/Atom'}):
        entry_id = entry.xpath('./atom:id/text()', namespaces={'atom': 'http://www.w3.org/2005/Atom'})[0]
        title = entry.xpath('./atom:title/text()', namespaces={'atom': 'http://www.w3.org/2005/Atom'})[0]
        summary = entry.xpath('./atom:summary/text()', namespaces={'atom': 'http://www.w3.org/2005/Atom'})
        content = entry.xpath('./atom:content/text()', namespaces={'atom': 'http://www.w3.org/2005/Atom'})
        updated = entry.xpath('./atom:updated/text()', namespaces={'atom': 'http://www.w3.org/2005/Atom'})
        published = entry.xpath('./atom:published/text()', namespaces={'atom': 'http://www.w3.org/2005/Atom'})
        author = entry.xpath('./atom:author/atom:name/text()', namespaces={'atom': 'http://www.w3.org/2005/Atom'})
        link = entry.xpath('./atom:link/@href', namespaces={'atom': 'http://www.w3.org/2005/Atom'})[0]
        
        entries.append(EntrySchema(
            id=entry_id,
            title=title,
            link=link,
            summary=summary[0] if summary else '',
            content=content[0] if content else '',
            updated=updated[0] if updated else '',
            published=published[0] if published else '',
            author=author[0] if author else ''
        ))

    return entries

@greader.get("/hello")
def hello(request):
    return "Hello world"

