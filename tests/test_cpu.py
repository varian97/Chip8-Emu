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
        self.assertIsNotNone(self.cpu)
        self.assertEqual(self.cpu.memory[0], 0xf0)
        self.assertEqual(self.cpu.pc, 0x200)
        self.assertIs(self.cpu.paused, False)

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

    def test_run_instruction_00ee_expect_correct(self):
        self.cpu.memory[0x200] = 0x00
        self.cpu.memory[0x201] = 0xee
        self.cpu.stack.append(0xff)
        self.cpu.cycle()

        self.assertEqual(self.cpu.pc, 0xff)
        self.assertEqual(len(self.cpu.stack), 0)

    def test_run_instruction_1nnn_expect_correct(self):
        self.cpu.memory[0x200] = 0x10
        self.cpu.memory[0x201] = 0x11
        self.cpu.cycle()

        self.assertEqual(self.cpu.pc, 0x11)

    def test_run_instruction_2nnn_expect_correct(self):
        initial_pc = self.cpu.pc
        self.cpu.memory[0x200] = 0x20
        self.cpu.memory[0x201] = 0x11
        self.cpu.cycle()

        self.assertEqual(self.cpu.pc, 0x11)
        self.assertEqual(len(self.cpu.stack), 1)
        self.assertEqual(self.cpu.stack[-1], initial_pc)

    def test_run_instruction_3xkk_expect_correct(self):
        self.cpu.memory[0x200] = 0x30
        self.cpu.memory[0x201] = 0x11
        self.cpu.v[0] = 0x11
        self.cpu.cycle()

        self.assertEqual(self.cpu.pc, 0x204)

        self.cpu.memory[0x204] = 0x30
        self.cpu.memory[0x205] = 0x11
        self.cpu.v[0] = 0x10
        self.cpu.cycle()

        self.assertEqual(self.cpu.pc, 0x206)

    def test_run_instruction_4xkk_expect_correct(self):
        self.cpu.memory[0x200] = 0x40
        self.cpu.memory[0x201] = 0x11
        self.cpu.v[0] = 0x11
        self.cpu.cycle()

        self.assertEqual(self.cpu.pc, 0x202)

        self.cpu.memory[0x202] = 0x40
        self.cpu.memory[0x203] = 0x11
        self.cpu.v[0] = 0x10
        self.cpu.cycle()

        self.assertEqual(self.cpu.pc, 0x206)

    def test_run_instruction_5xy0_expect_correct(self):
        self.cpu.memory[0x200] = 0x50
        self.cpu.memory[0x201] = 0x10
        self.cpu.v[0] = 0x11
        self.cpu.v[1] = 0x11
        self.cpu.cycle()

        self.assertEqual(self.cpu.pc, 0x204)

        self.cpu.memory[0x204] = 0x50
        self.cpu.memory[0x205] = 0x10
        self.cpu.v[0] = 0x10
        self.cpu.v[1] = 0x11
        self.cpu.cycle()

        self.assertEqual(self.cpu.pc, 0x206)

    def test_run_instruction_6xkk_expect_correct(self):
        self.cpu.memory[0x200] = 0x60
        self.cpu.memory[0x201] = 0xff
        self.cpu.cycle()

        self.assertEqual(self.cpu.v[0], 0xff)
        self.assertEqual(self.cpu.pc, 0x202)

    def test_run_instruction_7xkk_expect_correct(self):
        self.cpu.memory[0x200] = 0x70
        self.cpu.memory[0x201] = 0xff
        self.cpu.cycle()

        self.assertEqual(self.cpu.v[0], 0xff)
        self.assertEqual(self.cpu.pc, 0x202)

    def test_run_instruction_8xy0_expect_correct(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x10
        self.cpu.v[0] = 0x01
        self.cpu.v[1] = 0x02
        self.cpu.cycle()

        self.assertEqual(self.cpu.v[0], 0x02)
        self.assertEqual(self.cpu.pc, 0x202)

    def test_run_instruction_8xy1_expect_correct(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x11
        self.cpu.v[0] = 0x01
        self.cpu.v[1] = 0x02
        self.cpu.cycle()

        self.assertEqual(self.cpu.v[0], 0x03)
        self.assertEqual(self.cpu.pc, 0x202)

    def test_run_instruction_8xy2_expect_correct(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x12
        self.cpu.v[0] = 0x01
        self.cpu.v[1] = 0x03
        self.cpu.cycle()

        self.assertEqual(self.cpu.v[0], 0x01)
        self.assertEqual(self.cpu.pc, 0x202)

    def test_run_instruction_8xy3_expect_correct(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x13
        self.cpu.v[0] = 0x01
        self.cpu.v[1] = 0x03
        self.cpu.cycle()

        self.assertEqual(self.cpu.v[0], 0x02)
        self.assertEqual(self.cpu.pc, 0x202)

    def test_run_instruction_8xy4_expect_correct(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x14
        self.cpu.v[0] = 0x01
        self.cpu.v[1] = 0x03
        self.cpu.cycle()

        self.assertEqual(self.cpu.v[0], 0x04)
        self.assertEqual(self.cpu.v[15], 0)
        self.assertEqual(self.cpu.pc, 0x202)

        self.cpu.memory[0x202] = 0x80
        self.cpu.memory[0x203] = 0x14
        self.cpu.v[0] = 0xff
        self.cpu.v[1] = 0x01
        self.cpu.cycle()

        self.assertEqual(self.cpu.v[0], 0)
        self.assertEqual(self.cpu.v[15], 1)
        self.assertEqual(self.cpu.pc, 0x204)

    def test_run_instruction_8xy5_expect_correct(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x15
        self.cpu.v[0] = 0x03
        self.cpu.v[1] = 0x01
        self.cpu.cycle()

        self.assertEqual(self.cpu.v[0], 0x02)
        self.assertEqual(self.cpu.v[15], 1)
        self.assertEqual(self.cpu.pc, 0x202)

        self.cpu.memory[0x202] = 0x80
        self.cpu.memory[0x203] = 0x15
        self.cpu.v[0] = 0x01
        self.cpu.v[1] = 0x03
        self.cpu.cycle()

        self.assertEqual(self.cpu.v[0], 0xfe)
        self.assertEqual(self.cpu.v[15], 0)
        self.assertEqual(self.cpu.pc, 0x204)
