import urllib2
from BeautifulSoup import *
from urlparse import urljoin
from pysqlite2 import dbapi2 as sqlite

ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])


class crawler:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)
    
    def __del__(self):
        self.con.close()
        
    def dbcommit(self):
        self.con.commit()
        
    # Get an entry id, and insert it into db if it don't exist
    def getentryid(self, table, field, value):
        cur = self.con.execute('select rowid from %s where %s = "%s"' % (table, field, value))
        res = cur.fetchone()
        if res is None:
            cur = self.con.execute('insert into %s (%s) values ("%s")' % (table, field, value))
            return cur.lastrowid
        return res[0]
    
    # Create an index for each page
    def addtoindex(self, url, soup):
        if self.isindexed(url):
            return
        print 'Indexing %s' % url
        
        text = self.gettextonly(soup)
        words = self.separatewords(text)
        
        urlid = self.getentryid('urllist', 'url', url)
        
        # Link each word to this url
        for id, word in enumerate(words):
            if word in ignorewords:
                continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute('insert into wordlocation(urlid, wordid, location) values (%d, %d, %d)' % (urlid, wordid, id))
        
    # No tags
    def gettextonly(self, soup):
        v = soup.string
        if v is None:
            resulttext = ''
            c = soup.contents
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        return v.strip()
        
    # Separate the words by any non-whitespace character
    def separatewords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']
        
    def isindexed(self, url):
        u = self.con.execute('select rowid from urllist where url = "%s"' % url).fetchone()
        if u is not None:
            v = self.con.execute('select * from wordlocation where urlid = %d' % u[0]).fetchone()
            return v is not None
        return False
        
    def addlinkref(self, urlFrom, urlTo, linkText):
        pass
        
    # Starting with a list of pages, 
    # do a breadth first search to the given depth, indexing pages as we go
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                except:
                    print 'Could not open %s' % page
                    continue
                soup = BeautifulSoup(c.read())
                self.addtoindex(page, soup)
                
                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1:
                            continue
                        url = url.split('#')[0]    # remove location portion
                        if url[0:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText = self.gettextonly(link)
                        self.addlinkref(page, url, linkText)
                self.dbcommit()
            pages = newpages
        
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        
        self.dbcommit()
        

class searcher:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)
        
    def __del__(self):
        self.con.close()
        
    def getmatchrows(self, query):
        fieldlist = 'w0.urlid'
        tablelist = ''
        clauselist = ''
        wordids = []
        
        words = query.split(' ')
        tablenumber = 0
        
        for word in words:
            wordrow = self.con.execute("select rowid from wordlist where word = '%s'" % word).fetchone()
            if wordrow is not None:
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenumber > 0:
                    tablelist += ', '
                    clauselist += ' and '
                    clauselist += 'w%d.urlid = w%d.urlid and ' % (tablenumber-1, tablenumber)
                fieldlist += ', w%d.location' % tablenumber
                tablelist += 'wordlocation w%d' % tablenumber
                clauselist += 'w%d.wordid = %d' % (tablenumber, wordid)
                tablenumber += 1
                
        fullquery = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
        cur = self.con.execute(fullquery)
        rows = [row for row in cur]
        
        return rows, wordids
    
        
if __name__ == '__main__':
    pagelist = ['http://www.baidu.com']
    crawler = crawler('searchindex.db')
    crawler.crawl(pagelist)
