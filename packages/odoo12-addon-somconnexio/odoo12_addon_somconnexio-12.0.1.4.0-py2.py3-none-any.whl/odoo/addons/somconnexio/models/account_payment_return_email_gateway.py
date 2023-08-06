from odoo import models
from odoo.exceptions import UserError
import logging
import re
_logger = logging.getLogger(__name__)


class AccountPaymentReturnEmailGateway(models.Model):
    _name = 'account.payment.return.gateway'
    _inherit = 'mail.thread'

    def message_new(self, msg_dict, custom_values=None):
        import_model = self.env['payment.return.import']
        return_model = self.env['payment.return']
        journal_model = self.env['account.journal']
        thread = super().message_new(msg_dict, custom_values)
        if 'attachments' in msg_dict:
            attach_bytes = msg_dict['attachments'][0][1]
            pattern = re.compile(r'filename=".*?".*\n\n(.*?)\n-+', re.DOTALL)
            attach_bytes = pattern.search(attach_bytes)[1].strip()
            return_file = attach_bytes.encode('ascii')
            journal = journal_model.search([('code', '=', 'REM')])
            bank_return_id = import_model.create(
                dict(
                    data_file=return_file,
                    journal_id=journal.id,
                    match_after_import=False
                )
            )
            result = bank_return_id.import_file()
            payment_return = return_model.browse(result['res_id'])
            payment_return.action_confirm()
        else:
            raise UserError('Missing attachment in Payment Return email')
        return thread
