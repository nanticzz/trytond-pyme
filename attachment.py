# This file is part of the pyme module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from ...config import CONFIG
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
import os
__all__ = ['Attachment']
__metaclass__ = PoolMeta


class Attachment:
    __name__ = 'ir.attachment'

    @classmethod
    def delete(cls, attachments):
        cursor = Transaction().cursor
        db_name = cursor.dbname
        base_path = os.path.join(CONFIG['data_path'], db_name)
        archives = []
        for attachment in attachments:
            archive = attachment.digest
            collision = attachment.collision
            directory = os.path.join(base_path, archive[0:2], archive[2:4])
            if collision:
                archive += '-' + str(collision)
            archives.append('%s/%s' % (directory, archive))
        super(Attachment, cls).delete(attachments)
        for archive in archives:
            os.unlink(archive)
            try:
                directories = ('/'.join(archive.split('/')[0:-1]),
                    '/'.join(archive.split('/')[0:-2]))
                map(os.rmdir, directories)
            except OSError:
                pass