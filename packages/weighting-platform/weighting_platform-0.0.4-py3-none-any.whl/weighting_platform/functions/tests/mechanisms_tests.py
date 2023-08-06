import unittest
import threading
import time
import datetime
from weighting_platform.functions import mechanisms
from weighting_platform.tests import test_objects


class MechanismsTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MechanismsTest, self).__init__(*args, **kwargs)
        self.qsb = test_objects.test_qsb
        self.weight_splitter = test_objects.weightsplitter_test
        self.weight_splitter.start()

    def test_close_gate_mechanism_normal(self):
        time.sleep(2)
        self.weight_splitter.set_manual_value(manual_value='10000')
        time.sleep(1)
        main_thread = threading.Thread(target=mechanisms.close_barrier_after_round,
                                       args=(self.qsb, self.weight_splitter, 'internal'))
        main_thread.start()
        time.sleep(3)
        self.weight_splitter.set_manual_value(manual_value='0')
        time.sleep(3)
        self.qsb.lock_point('INTERNAL_PHOTOCELL')
        time.sleep(5)
        self.qsb.normal_point('INTERNAL_PHOTOCELL')
        time.sleep(10)
        self.assertTrue(not main_thread.is_alive())

    def test_close_gate_mechanism_block(self):
        time.sleep(2)
        self.weight_splitter.set_manual_value(manual_value='10000')
        time.sleep(1)
        main_thread = threading.Thread(target=mechanisms.close_barrier_after_round,
                                       args=(self.qsb, self.weight_splitter, 'internal'))
        main_thread.start()
        time.sleep(3)
        self.weight_splitter.set_manual_value(manual_value='0')
        time.sleep(4)
        self.qsb.lock_point('INTERNAL_PHOTOCELL')
        time.sleep(5)
        self.qsb.normal_point('INTERNAL_PHOTOCELL')
        time.sleep(2)
        self.qsb.lock_point('INTERNAL_PHOTOCELL')
        time.sleep(6)
        self.assertTrue(main_thread.is_alive())

    def test_close_gate_mechanism_block_deblock(self):
        time.sleep(2)
        self.weight_splitter.set_manual_value(manual_value='10000')
        time.sleep(1)
        main_thread = threading.Thread(
            target=mechanisms.close_barrier_after_round,
            args=(self.qsb, self.weight_splitter, 'internal'))
        main_thread.start()
        time.sleep(3)
        self.weight_splitter.set_manual_value(manual_value='0')
        time.sleep(4)
        self.qsb.lock_point('INTERNAL_PHOTOCELL')
        time.sleep(5)
        self.qsb.normal_point('INTERNAL_PHOTOCELL')
        time.sleep(2)
        self.qsb.lock_point('INTERNAL_PHOTOCELL')
        self.qsb.normal_point('INTERNAL_PHOTOCELL')
        time.sleep(2)
        self.qsb.lock_point('INTERNAL_PHOTOCELL')
        self.qsb.normal_point('INTERNAL_PHOTOCELL')
        time.sleep(2)
        self.qsb.lock_point('INTERNAL_PHOTOCELL')
        self.qsb.normal_point('INTERNAL_PHOTOCELL')
        time.sleep(2)
        self.qsb.lock_point('INTERNAL_PHOTOCELL')
        self.qsb.normal_point('INTERNAL_PHOTOCELL')
        time.sleep(2)
        self.qsb.lock_point('INTERNAL_PHOTOCELL')
        self.qsb.normal_point('INTERNAL_PHOTOCELL')
        time.sleep(6)
        self.assertTrue(not main_thread.is_alive())

    def test_close_both_gates(self):
        mechanisms.open_both_gates(self.qsb)
        external_gate_status = self.qsb.get_point_state('EXTERNAL_GATE')
        internal_gate_status = self.qsb.get_point_state('INTERNAL_GATE')
        self.assertEqual(external_gate_status, self.qsb.get_unlock_state_str())
        self.assertEqual(internal_gate_status, self.qsb.get_unlock_state_str())
        mechanisms.close_both_gates(self.qsb)
        external_gate_status = self.qsb.get_point_state('EXTERNAL_GATE')
        internal_gate_status = self.qsb.get_point_state('INTERNAL_GATE')
        self.assertEqual(external_gate_status, self.qsb.get_lock_state_str())
        self.assertEqual(internal_gate_status, self.qsb.get_lock_state_str())


if __name__ == '__main__':
    unittest.main()

