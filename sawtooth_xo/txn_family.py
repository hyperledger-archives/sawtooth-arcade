# Copyright 2016 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

import logging

from journal import transaction, global_store_manager
from journal.messages import transaction_message

from sawtooth_xo.xo_exceptions import XoException

LOGGER = logging.getLogger(__name__)


def _register_transaction_types(ledger):
    ledger.register_message_handler(
        XoTransactionMessage,
        transaction_message.transaction_message_handler)
    ledger.add_transaction_store(XoTransaction)


class XoTransactionMessage(transaction_message.TransactionMessage):
    MessageType = "/Xo/Transaction"

    def __init__(self, minfo=None):
        if minfo is None:
            minfo = {}

        super(XoTransactionMessage, self).__init__(minfo)

        tinfo = minfo.get('Transaction', {})
        self.Transaction = XoTransaction(tinfo)


class XoTransaction(transaction.Transaction):
    TransactionTypeName = '/XoTransaction'
    TransactionStoreType = global_store_manager.KeyValueStore
    MessageType = XoTransactionMessage

    def __init__(self, minfo=None):
        if minfo is None:
            minfo = {}

        super(XoTransaction, self).__init__(minfo)

        LOGGER.debug("minfo: %s", repr(minfo))
        self._name = minfo['Name'] if 'Name' in minfo else None
        self._action = minfo['Action'] if 'Action' in minfo else None
        self._space = minfo['Space'] if 'Space' in minfo else None

    def __str__(self):
        LOGGER.error("XoTransaction __str__ not implemented")
        return "XoTransaction"

    def is_valid(self, store):
        try:
            self.check_valid(store)
        except XoException as e:
            LOGGER.debug('invalid transaction (%s): %s', str(e), str(self))
            return False

        return True

    def check_valid(self, store):
        if not super(XoTransaction, self).is_valid(store):
            raise XoException("invalid transaction")

        LOGGER.debug('checking %s', str(self))

        raise XoException('XoTransaction.check_valid is not implemented')

    def apply(self, store):
        LOGGER.debug('apply %s', str(self))
        LOGGER.error('XoTransaction.apply is not implemented')

    def dump(self):
        result = super(XoTransaction, self).dump()

        result['Action'] = self._action
        result['Name'] = self._name
        if self._space is not None:
            result['Space'] = self._space

        return result
