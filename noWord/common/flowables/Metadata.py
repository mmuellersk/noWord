from reportlab.platypus import Flowable



# This class is a trick to define ALL pdf metadata. Some are settable from the docTemplate
# like author, subject etc, but creator and producer would always be set to the default
# "ReportLab PDF Library - www.reportlab.com" string.


class Metadata(Flowable):
    def __init__(self, title="", author="", subject="", keywords="", creator="", producer=""):
        Flowable.__init__(self)
        self.title = title
        self.author = author
        self.subject = subject
        self.keywords = keywords
        self.creator = creator
        self.producer = producer

    def draw(self):
        infos = self.canv._doc.info
        infos.title = self.title
        infos.author = self.author
        infos.subject = self.subject
        infos.keywords = self.keywords
        infos.creator = self.creator
        infos.producer = self.producer
        return

    def __str__(self):
        return self.__repr__(self)

    def __repr__(self):
        str = 'noWord.%s (\n' % 'Metadata'
        str += 'title: %s,\n' % self.title
        str += 'author: %s,\n' % self.author
        str += 'subject: %s,\n' % self.subject
        str += 'keywords: %s,\n' % self.keywords
        str += 'creator: %s,\n' % self.creator
        str += 'producer: %s\n' % self.producer
        str += ') noWord.#%s ' % 'Metadata'
        return str