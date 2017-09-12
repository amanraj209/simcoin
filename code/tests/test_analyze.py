from unittest import TestCase
from mock import patch
from mock import mock_open
import config
from parse import TxStats
from parse import CheckingMempoolLogLine
from parse import TickLogLine
from parse import RPCExceptionLogLine
from parse import ExceptionLogLine
from analyze import Analyzer
from mock import Mock


class TestAnalyze(TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_create_mempool_snapshots_csv(self, m_open):
        mempool_snapshots = [
            CheckingMempoolLogLine('timestamp', 'node-1', 45, 36)
        ]

        context = Mock()
        context.mempool_snapshots = mempool_snapshots
        context.general_infos = {'tag': 'test'}
        analyzer = Analyzer(context)
        analyzer.create_mempool_snapshots_csv()

        m_open.assert_called_with(config.mempool_snapshots_csv, 'w')
        handle = m_open()
        self.assertEqual(handle.write.call_count, 2)
        self.assertEqual(handle.write.call_args_list[0][0][0], 'timestamp;node;txs;inputs\r\n')
        self.assertEqual(handle.write.call_args_list[1][0][0], 'timestamp;node-1;45;36\r\n')

    @patch('builtins.open', new_callable=mock_open)
    def test_create_tick_infos(self, m_open):
        tick_infos = [
            TickLogLine('timestamp', 12.12, 45)
        ]

        context = Mock()
        context.tick_infos = tick_infos
        context.general_infos = {'tag': 'test'}
        analyzer = Analyzer(context)
        analyzer.create_tick_infos_csv()

        m_open.assert_called_with(config.tick_infos_csv, 'w')
        handle = m_open()
        self.assertEqual(handle.write.call_count, 2)
        self.assertEqual(handle.write.call_args_list[0][0][0], 'timestamp;start;duration\r\n')
        self.assertEqual(handle.write.call_args_list[1][0][0], 'timestamp;12.12;45\r\n')

    @patch('builtins.open', new_callable=mock_open)
    def test_create_rpc_exceptions(self, m_open):
        rpc_exceptions = [
            RPCExceptionLogLine('timestamp', 'node-1', 'some_method', 'some_exception')
        ]

        context = Mock()
        context.rpc_exceptions = rpc_exceptions
        context.general_infos = {'tag': 'test'}
        analyzer = Analyzer(context)
        analyzer.create_rpc_exceptions_csv()

        m_open.assert_called_with(config.rpc_exceptions_csv, 'w')
        handle = m_open()
        self.assertEqual(handle.write.call_count, 2)
        self.assertEqual(handle.write.call_args_list[0][0][0], 'timestamp;node;method;exception\r\n')
        self.assertEqual(handle.write.call_args_list[1][0][0], 'timestamp;node-1;some_method;some_exception\r\n')
