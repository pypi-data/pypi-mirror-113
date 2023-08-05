"""litcorpt module initialization"""

from tinydb import Query


from .constants import (__version__,
                        __author__,
                        __author_email__,
)

from .main import (corpus,
                   corpus_load,
                   corpus_read,
                   corpus_write,
                   corpus_retrieve,
                   corpus_build_database,
                   corpus_insert_book,
                   book_write,
                   book_read,
                   doc_id,
                   logger,
)

from .epub import read
