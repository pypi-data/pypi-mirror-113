# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from nereid.helpers import send_file, url_for
#from nereid.helpers import url_for
#from flask import send_file
from nereid.contrib.sitemap import SitemapIndex
from tempfile import NamedTemporaryFile
import io


class SitemapIndexPrio(SitemapIndex):
    '''
    nereid/contrib/sitemap.py
      - Extended implementation to get different priorities assigned to the
        index file names
    '''
    def __init__(self, model, domain, priorities=[0.5],
            cache_timeout=60 * 60 * 24):
        '''
        - Use the additional keyword argument priority
        - Allow to concatenate indexes for several priorities
        '''
        self.model = model
        self.domain = domain
        print('prio',domain)
        self.priorities = priorities
        self.cache_timeout = cache_timeout

    def render(self):
        with io.BytesIO() as tmp_file:
            data = '<?xml version="1.0" encoding="UTF-8"?>\n'
            data += '<sitemapindex '
            data += 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            print(self.page_count)
            method = '%s.sitemap' % self.model.__name__
            for page in range(1, self.page_count + 1):
                for priority in self.priorities:
                    data += ('<sitemap><loc>%s</loc></sitemap>\n'
                        % url_for(method, page=page,
                            priority=str(priority), _external=True))
            data += '</sitemapindex>'

            tmp_file.write(data.encode())
            mimetype = 'application/xml'
            # Workaround to avoid closed file error
            # https://stackoverflow.com/questions/58197454/using-bytesio-and-flask-send-file
            # Remove with flask 2.0
            tmp_file.seek(0)
            return send_file(io.BytesIO(tmp_file.read()),
                cache_timeout=self.cache_timeout,
                mimetype=mimetype)
            #attachment_filename='index.xml')

    def wrender(self):
        with io.BytesIO() as tmp_file:
            tmp_file.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode())
            tmp_file.write('<sitemapindex '.encode())
            tmp_file.write(
                'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'.encode()
            )
            print(self.page_count)
            method = '%s.sitemap' % self.model.__name__
            for page in range(1, self.page_count + 1):
                for priority in self.priorities:
                    loc = ('<sitemap><loc>%s</loc></sitemap>\n'
                        % url_for(method, page=page,
                            priority=str(priority), _external=True))
                    tmp_file.write(loc.encode())
            tmp_file.write('</sitemapindex>'.encode())
            #print(dir(tmp_file))
            #w = FileWrapper(tmp_file)
            #print(tmp_file.file.buffer)
            #import time
            #time.sleep(1)
            mimetype = 'application/xml'
            tmp_file.seek(0)
            return send_file(io.BytesIO(tmp_file.read()),
                cache_timeout=self.cache_timeout,
                mimetype=mimetype)
            #attachment_filename='index.xml')

    def xrender(self):
        with NamedTemporaryFile(suffix=".xml", mode="w") as tmp_file:
            tmp_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            tmp_file.write('<sitemapindex ')
            tmp_file.write(
                'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            )
            print(self.page_count)
            method = '%s.sitemap' % self.model.__name__
            for page in range(1, self.page_count + 1):
                for priority in self.priorities:
                    tmp_file.write('<sitemap><loc>%s</loc></sitemap>\n'
                        % url_for(method, page=page,
                            priority=str(priority), _external=True))
            tmp_file.write('</sitemapindex>')
            print(tmp_file.name)
            print(dir(tmp_file.file))
            print(tmp_file.file.buffer)
            import time
            #time.sleep(1)
            return send_file(tmp_file.name, cache_timeout=self.cache_timeout)
