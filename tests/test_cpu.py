from mock import patch
from unittest import TestCase

from chip8.cpu import CPU
from chip8.display import Display

class CPUTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.display = Display(height=32, width=64, scale=10)
        self.cpu = CPU(None, None, display=self.display)

    def test_init_expect_all_setup_correctly(self):
        cpu = CPU(None, None, None)

        self.assertIsNotNone(cpu)
        self.assertEqual(cpu.memory[0], 0xf0)
        self.assertEqual(cpu.pc, 0x200)
        self.assertIs(cpu.paused, False)

    @patch('chip8.cpu.CPU.fetch_instruction')
    @patch('chip8.cpu.CPU.run_instruction')
    def test_cycle_given_paused_expect_fetch_and_run_not_called(self, mock_run, mock_fetch):
        self.cpu.paused = True
        self.cpu.cycle()

        mock_fetch.assert_not_called()
        mock_run.assert_not_called()

    def test_fetch_instruction_expect_correct_opcode_fetched(self):
        self.cpu.memory[0x200] = 0xff
        self.cpu.memory[0x201] = 0xff
        opcode = self.cpu.fetch_instruction()

        self.assertEqual(opcode, 0xffff)

    @patch('chip8.display.Display.clear_display')
    def test_run_instruction_00e0_expect_correct(self, mock_clear_display):
        self.cpu.memory[0x200] = 0x00
        self.cpu.memory[0x201] = 0xe0
        self.cpu.cycle()

        self.assertEqual(self.cpu.pc, 0x202)
        mock_clear_display.assert_called_once()
