import struct

import pytest

from bronzebeard import asm


@pytest.mark.parametrize(
    'rd, imm,      code', [
    (0,  0,        0b00000000000000000000000000110111),
    (31, 0,        0b00000000000000000000111110110111),
    (0,  1,        0b00000000000000000001000000110111),
    (0,  0x7ffff,  0b01111111111111111111000000110111),
    (0,  -1,       0b11111111111111111111000000110111),
    (0,  -0x80000, 0b10000000000000000000000000110111),
])
def test_lui(rd, imm, code):
    assert asm.LUI(rd, imm) == code


@pytest.mark.parametrize(
    'rd, imm,      code', [
    (0,  0,        0b00000000000000000000000000010111),
    (31, 0,        0b00000000000000000000111110010111),
    (0,  1,        0b00000000000000000001000000010111),
    (0,  0x7ffff,  0b01111111111111111111000000010111),
    (0,  -1,       0b11111111111111111111000000010111),
    (0,  -0x80000, 0b10000000000000000000000000010111),
])
def test_auipc(rd, imm, code):
    assert asm.AUIPC(rd, imm) == code


@pytest.mark.parametrize(
    'rd, imm,       code', [
    (0,  0,         0b00000000000000000000000001101111),
    (31, 0,         0b00000000000000000000111111101111),
    (0,  2,         0b00000000001000000000000001101111),
    (0,  2046,      0b01111111111000000000000001101111),
    (0,  2048,      0b00000000000100000000000001101111),
    (0,  0x0ff000,  0b00000000000011111111000001101111),
    (0,  0x0ffffe,  0b01111111111111111111000001101111),
    (0,  -2,        0b11111111111111111111000001101111),
    (0,  -0x1000,   0b10000000000011111111000001101111),
    (0,  -0xff800,  0b10000000000100000000000001101111),
    (0,  -0xff802,  0b11111111111000000000000001101111),
    (0,  -0x100000, 0b10000000000000000000000001101111),
])
def test_jal(rd, imm, code):
    assert asm.JAL(rd, imm) == code


@pytest.mark.parametrize(
    'rd, rs1, imm,    code', [
    (0,  0,   0,      0b00000000000000000000000001100111),
    (31, 0,   0,      0b00000000000000000000111111100111),
    (0,  31,  0,      0b00000000000011111000000001100111),
    (31, 31,  0,      0b00000000000011111000111111100111),
    (0,  0,   2,      0b00000000001000000000000001100111),
    (0,  0,   0x7fe,  0b01111111111000000000000001100111),
    (0,  0,   -2,     0b11111111111000000000000001100111),
    (0,  0,   -0x800, 0b10000000000000000000000001100111),
])
def test_jalr(rd, rs1, imm, code):
    assert asm.JALR(rd, rs1, imm) == code


@pytest.mark.parametrize(
    'rs1, rs2, imm,     code', [
    (0,   0,   0,       0b00000000000000000000000001100011),
    (31,  0,   0,       0b00000000000011111000000001100011),
    (0,   31,  0,       0b00000001111100000000000001100011),
    (31,  31,  0,       0b00000001111111111000000001100011),
    (0,   0,   2,       0b00000000000000000000000101100011),
    (0,   0,   0xffe,   0b01111110000000000000111111100011),
    (0,   0,   -2,      0b11111110000000000000111111100011),
    (0,   0,   -0x1000, 0b10000000000000000000000001100011),
])
def test_beq(rs1, rs2, imm, code):
    assert asm.BEQ(rs1, rs2, imm) == code


@pytest.mark.parametrize(
    'rs1, rs2, imm,     code', [
    (0,   0,   0,       0b00000000000000000001000001100011),
    (31,  0,   0,       0b00000000000011111001000001100011),
    (0,   31,  0,       0b00000001111100000001000001100011),
    (31,  31,  0,       0b00000001111111111001000001100011),
    (0,   0,   2,       0b00000000000000000001000101100011),
    (0,   0,   0xffe,   0b01111110000000000001111111100011),
    (0,   0,   -2,      0b11111110000000000001111111100011),
    (0,   0,   -0x1000, 0b10000000000000000001000001100011),
])
def test_bne(rs1, rs2, imm, code):
    assert asm.BNE(rs1, rs2, imm) == code


@pytest.mark.parametrize(
    'rs1, rs2, imm,     code', [
    (0,   0,   0,       0b00000000000000000100000001100011),
    (31,  0,   0,       0b00000000000011111100000001100011),
    (0,   31,  0,       0b00000001111100000100000001100011),
    (31,  31,  0,       0b00000001111111111100000001100011),
    (0,   0,   2,       0b00000000000000000100000101100011),
    (0,   0,   0xffe,   0b01111110000000000100111111100011),
    (0,   0,   -2,      0b11111110000000000100111111100011),
    (0,   0,   -0x1000, 0b10000000000000000100000001100011),
])
def test_blt(rs1, rs2, imm, code):
    assert asm.BLT(rs1, rs2, imm) == code


@pytest.mark.parametrize(
    'rs1, rs2, imm,     code', [
    (0,   0,   0,       0b00000000000000000101000001100011),
    (31,  0,   0,       0b00000000000011111101000001100011),
    (0,   31,  0,       0b00000001111100000101000001100011),
    (31,  31,  0,       0b00000001111111111101000001100011),
    (0,   0,   2,       0b00000000000000000101000101100011),
    (0,   0,   0xffe,   0b01111110000000000101111111100011),
    (0,   0,   -2,      0b11111110000000000101111111100011),
    (0,   0,   -0x1000, 0b10000000000000000101000001100011),
])
def test_bge(rs1, rs2, imm, code):
    assert asm.BGE(rs1, rs2, imm) == code


@pytest.mark.parametrize(
    'rs1, rs2, imm,     code', [
    (0,   0,   0,       0b00000000000000000110000001100011),
    (31,  0,   0,       0b00000000000011111110000001100011),
    (0,   31,  0,       0b00000001111100000110000001100011),
    (31,  31,  0,       0b00000001111111111110000001100011),
    (0,   0,   2,       0b00000000000000000110000101100011),
    (0,   0,   0xffe,   0b01111110000000000110111111100011),
    (0,   0,   -2,      0b11111110000000000110111111100011),
    (0,   0,   -0x1000, 0b10000000000000000110000001100011),
])
def test_bltu(rs1, rs2, imm, code):
    assert asm.BLTU(rs1, rs2, imm) == code


@pytest.mark.parametrize(
    'rs1, rs2, imm,     code', [
    (0,   0,   0,       0b00000000000000000111000001100011),
    (31,  0,   0,       0b00000000000011111111000001100011),
    (0,   31,  0,       0b00000001111100000111000001100011),
    (31,  31,  0,       0b00000001111111111111000001100011),
    (0,   0,   2,       0b00000000000000000111000101100011),
    (0,   0,   0xffe,   0b01111110000000000111111111100011),
    (0,   0,   -2,      0b11111110000000000111111111100011),
    (0,   0,   -0x1000, 0b10000000000000000111000001100011),
])
def test_bgeu(rs1, rs2, imm, code):
    assert asm.BGEU(rs1, rs2, imm) == code


@pytest.mark.parametrize(
    'rd, rs1, imm,    code', [
    (0,  0,   0,      0b00000000000000000000000000000011),
    (31, 0,   0,      0b00000000000000000000111110000011),
    (0,  31,  0,      0b00000000000011111000000000000011),
    (31, 31,  0,      0b00000000000011111000111110000011),
    (0,  0,   1,      0b00000000000100000000000000000011),
    (0,  0,   0x7ff,  0b01111111111100000000000000000011),
    (0,  0,   -1,     0b11111111111100000000000000000011),
    (0,  0,   -0x800, 0b10000000000000000000000000000011),
])
def test_lb(rd, rs1, imm, code):
    assert asm.LB(rd, rs1, imm) == code


@pytest.mark.parametrize(
    'rd, rs1, imm,    code', [
    (0,  0,   0,      0b00000000000000000001000000000011),
    (31, 0,   0,      0b00000000000000000001111110000011),
    (0,  31,  0,      0b00000000000011111001000000000011),
    (31, 31,  0,      0b00000000000011111001111110000011),
    (0,  0,   1,      0b00000000000100000001000000000011),
    (0,  0,   0x7ff,  0b01111111111100000001000000000011),
    (0,  0,   -1,     0b11111111111100000001000000000011),
    (0,  0,   -0x800, 0b10000000000000000001000000000011),
])
def test_lh(rd, rs1, imm, code):
    assert asm.LH(rd, rs1, imm) == code


@pytest.mark.parametrize(
    'rd, rs1, imm,    code', [
    (0,  0,   0,      0b00000000000000000010000000000011),
    (31, 0,   0,      0b00000000000000000010111110000011),
    (0,  31,  0,      0b00000000000011111010000000000011),
    (31, 31,  0,      0b00000000000011111010111110000011),
    (0,  0,   1,      0b00000000000100000010000000000011),
    (0,  0,   0x7ff,  0b01111111111100000010000000000011),
    (0,  0,   -1,     0b11111111111100000010000000000011),
    (0,  0,   -0x800, 0b10000000000000000010000000000011),
])
def test_lw(rd, rs1, imm, code):
    assert asm.LW(rd, rs1, imm) == code


@pytest.mark.parametrize(
    'rd, rs1, imm,    code', [
    (0,  0,   0,      0b00000000000000000100000000000011),
    (31, 0,   0,      0b00000000000000000100111110000011),
    (0,  31,  0,      0b00000000000011111100000000000011),
    (31, 31,  0,      0b00000000000011111100111110000011),
    (0,  0,   1,      0b00000000000100000100000000000011),
    (0,  0,   0x7ff,  0b01111111111100000100000000000011),
    (0,  0,   -1,     0b11111111111100000100000000000011),
    (0,  0,   -0x800, 0b10000000000000000100000000000011),
])
def test_lbu(rd, rs1, imm, code):
    assert asm.LBU(rd, rs1, imm) == code


@pytest.mark.parametrize(
    'rd, rs1, imm,    code', [
    (0,  0,   0,      0b00000000000000000101000000000011),
    (31, 0,   0,      0b00000000000000000101111110000011),
    (0,  31,  0,      0b00000000000011111101000000000011),
    (31, 31,  0,      0b00000000000011111101111110000011),
    (0,  0,   1,      0b00000000000100000101000000000011),
    (0,  0,   0x7ff,  0b01111111111100000101000000000011),
    (0,  0,   -1,     0b11111111111100000101000000000011),
    (0,  0,   -0x800, 0b10000000000000000101000000000011),
])
def test_lhu(rd, rs1, imm, code):
    assert asm.LHU(rd, rs1, imm) == code


@pytest.mark.parametrize(
    'rs1, rs2, imm,   code', [
    (0,   0,   0,     0b00000000000000000000000000100011),
    (31,  0,   0,     0b00000000000011111000000000100011),
    (0,   31,  0,     0b00000001111100000000000000100011),
    (31,  31,  0,     0b00000001111111111000000000100011),
    (0,   0,   1,     0b00000000000000000000000010100011),
    (0,   0,   2047,  0b01111110000000000000111110100011),
    (0,   0,   -1,    0b11111110000000000000111110100011),
    (0,   0,   -2048, 0b10000000000000000000000000100011),
])
def test_sb(rs1, rs2, imm, code):
    assert asm.SB(rs1, rs2, imm) == code


@pytest.mark.parametrize(
    'rs1, rs2, imm,   code', [
    (0,   0,   0,     0b00000000000000000001000000100011),
    (31,  0,   0,     0b00000000000011111001000000100011),
    (0,   31,  0,     0b00000001111100000001000000100011),
    (31,  31,  0,     0b00000001111111111001000000100011),
    (0,   0,   1,     0b00000000000000000001000010100011),
    (0,   0,   2047,  0b01111110000000000001111110100011),
    (0,   0,   -1,    0b11111110000000000001111110100011),
    (0,   0,   -2048, 0b10000000000000000001000000100011),
])
def test_sh(rs1, rs2, imm, code):
    assert asm.SH(rs1, rs2, imm) == code


@pytest.mark.parametrize(
    'rs1, rs2, imm,   code', [
    (0,   0,   0,     0b00000000000000000010000000100011),
    (31,  0,   0,     0b00000000000011111010000000100011),
    (0,   31,  0,     0b00000001111100000010000000100011),
    (31,  31,  0,     0b00000001111111111010000000100011),
    (0,   0,   1,     0b00000000000000000010000010100011),
    (0,   0,   2047,  0b01111110000000000010111110100011),
    (0,   0,   -1,    0b11111110000000000010111110100011),
    (0,   0,   -2048, 0b10000000000000000010000000100011),
])
def test_sw(rs1, rs2, imm, code):
    assert asm.SW(rs1, rs2, imm) == code


@pytest.mark.parametrize(
    'rd, rs1, imm,    code', [
    (0,  0,   0,      0b00000000000000000000000000010011),
    (31, 0,   0,      0b00000000000000000000111110010011),
    (0,  31,  0,      0b00000000000011111000000000010011),
    (31, 31,  0,      0b00000000000011111000111110010011),
    (0,  0,   1,      0b00000000000100000000000000010011),
    (0,  0,   0x7ff,  0b01111111111100000000000000010011),
    (0,  0,   -1,     0b11111111111100000000000000010011),
    (0,  0,   -0x800, 0b10000000000000000000000000010011),
])
def test_addi(rd, rs1, imm, code):
    assert asm.ADDI(rd, rs1, imm) == code


@pytest.mark.parametrize(
    'rd, rs1, imm,    code', [
    (0,  0,   0,      0b00000000000000000010000000010011),
    (31, 0,   0,      0b00000000000000000010111110010011),
    (0,  31,  0,      0b00000000000011111010000000010011),
    (31, 31,  0,      0b00000000000011111010111110010011),
    (0,  0,   1,      0b00000000000100000010000000010011),
    (0,  0,   0x7ff,  0b01111111111100000010000000010011),
    (0,  0,   -1,     0b11111111111100000010000000010011),
    (0,  0,   -0x800, 0b10000000000000000010000000010011),
])
def test_slti(rd, rs1, imm, code):
    assert asm.SLTI(rd, rs1, imm) == code


@pytest.mark.parametrize(
    'rd, rs1, imm,    code', [
    (0,  0,   0,      0b00000000000000000011000000010011),
    (31, 0,   0,      0b00000000000000000011111110010011),
    (0,  31,  0,      0b00000000000011111011000000010011),
    (31, 31,  0,      0b00000000000011111011111110010011),
    (0,  0,   1,      0b00000000000100000011000000010011),
    (0,  0,   0x7ff,  0b01111111111100000011000000010011),
    (0,  0,   -1,     0b11111111111100000011000000010011),
    (0,  0,   -0x800, 0b10000000000000000011000000010011),
])
def test_sltiu(rd, rs1, imm, code):
    assert asm.SLTIU(rd, rs1, imm) == code


@pytest.mark.parametrize(
    'rd, rs1, imm,    code', [
    (0,  0,   0,      0b00000000000000000100000000010011),
    (31, 0,   0,      0b00000000000000000100111110010011),
    (0,  31,  0,      0b00000000000011111100000000010011),
    (31, 31,  0,      0b00000000000011111100111110010011),
    (0,  0,   1,      0b00000000000100000100000000010011),
    (0,  0,   0x7ff,  0b01111111111100000100000000010011),
    (0,  0,   -1,     0b11111111111100000100000000010011),
    (0,  0,   -0x800, 0b10000000000000000100000000010011),
])
def test_xori(rd, rs1, imm, code):
    assert asm.XORI(rd, rs1, imm) == code


@pytest.mark.parametrize(
    'rd, rs1, imm,    code', [
    (0,  0,   0,      0b00000000000000000110000000010011),
    (31, 0,   0,      0b00000000000000000110111110010011),
    (0,  31,  0,      0b00000000000011111110000000010011),
    (31, 31,  0,      0b00000000000011111110111110010011),
    (0,  0,   1,      0b00000000000100000110000000010011),
    (0,  0,   0x7ff,  0b01111111111100000110000000010011),
    (0,  0,   -1,     0b11111111111100000110000000010011),
    (0,  0,   -0x800, 0b10000000000000000110000000010011),
])
def test_ori(rd, rs1, imm, code):
    assert asm.ORI(rd, rs1, imm) == code


@pytest.mark.parametrize(
    'rd, rs1, imm,    code', [
    (0,  0,   0,      0b00000000000000000111000000010011),
    (31, 0,   0,      0b00000000000000000111111110010011),
    (0,  31,  0,      0b00000000000011111111000000010011),
    (31, 31,  0,      0b00000000000011111111111110010011),
    (0,  0,   1,      0b00000000000100000111000000010011),
    (0,  0,   0x7ff,  0b01111111111100000111000000010011),
    (0,  0,   -1,     0b11111111111100000111000000010011),
    (0,  0,   -0x800, 0b10000000000000000111000000010011),
])
def test_andi(rd, rs1, imm, code):
    assert asm.ANDI(rd, rs1, imm) == code


@pytest.mark.parametrize(
    'rd, rs1, rs2, code', [
    (0,  0,   0,   0b00000000000000000001000000010011),
    (31, 0,   0,   0b00000000000000000001111110010011),
    (0,  31,  0,   0b00000000000011111001000000010011),
    (31, 31,  0,   0b00000000000011111001111110010011),
    (0,  0,   31,  0b00000001111100000001000000010011),
    (31, 0,   31,  0b00000001111100000001111110010011),
    (0,  31,  31,  0b00000001111111111001000000010011),
    (31, 31,  31,  0b00000001111111111001111110010011),
])
def test_slli(rd, rs1, rs2, code):
    assert asm.SLLI(rd, rs1, rs2) == code


@pytest.mark.parametrize(
    'rd, rs1, rs2, code', [
    (0,  0,   0,   0b00000000000000000101000000010011),
    (31, 0,   0,   0b00000000000000000101111110010011),
    (0,  31,  0,   0b00000000000011111101000000010011),
    (31, 31,  0,   0b00000000000011111101111110010011),
    (0,  0,   31,  0b00000001111100000101000000010011),
    (31, 0,   31,  0b00000001111100000101111110010011),
    (0,  31,  31,  0b00000001111111111101000000010011),
    (31, 31,  31,  0b00000001111111111101111110010011),
])
def test_srli(rd, rs1, rs2, code):
    assert asm.SRLI(rd, rs1, rs2) == code


@pytest.mark.parametrize(
    'rd, rs1, rs2, code', [
    (0,  0,   0,   0b01000000000000000101000000010011),
    (31, 0,   0,   0b01000000000000000101111110010011),
    (0,  31,  0,   0b01000000000011111101000000010011),
    (31, 31,  0,   0b01000000000011111101111110010011),
    (0,  0,   31,  0b01000001111100000101000000010011),
    (31, 0,   31,  0b01000001111100000101111110010011),
    (0,  31,  31,  0b01000001111111111101000000010011),
    (31, 31,  31,  0b01000001111111111101111110010011),
])
def test_srai(rd, rs1, rs2, code):
    assert asm.SRAI(rd, rs1, rs2) == code


@pytest.mark.parametrize(
    'rd, rs1, rs2, code', [
    (0,  0,   0,   0b00000000000000000000000000110011),
    (31, 0,   0,   0b00000000000000000000111110110011),
    (0,  31,  0,   0b00000000000011111000000000110011),
    (31, 31,  0,   0b00000000000011111000111110110011),
    (0,  0,   31,  0b00000001111100000000000000110011),
    (31, 0,   31,  0b00000001111100000000111110110011),
    (0,  31,  31,  0b00000001111111111000000000110011),
    (31, 31,  31,  0b00000001111111111000111110110011),
])
def test_add(rd, rs1, rs2, code):
    assert asm.ADD(rd, rs1, rs2) == code


@pytest.mark.parametrize(
    'rd, rs1, rs2, code', [
    (0,  0,   0,   0b01000000000000000000000000110011),
    (31, 0,   0,   0b01000000000000000000111110110011),
    (0,  31,  0,   0b01000000000011111000000000110011),
    (31, 31,  0,   0b01000000000011111000111110110011),
    (0,  0,   31,  0b01000001111100000000000000110011),
    (31, 0,   31,  0b01000001111100000000111110110011),
    (0,  31,  31,  0b01000001111111111000000000110011),
    (31, 31,  31,  0b01000001111111111000111110110011),
])
def test_sub(rd, rs1, rs2, code):
    assert asm.SUB(rd, rs1, rs2) == code


@pytest.mark.parametrize(
    'rd, rs1, rs2, code', [
    (0,  0,   0,   0b00000000000000000001000000110011),
    (31, 0,   0,   0b00000000000000000001111110110011),
    (0,  31,  0,   0b00000000000011111001000000110011),
    (31, 31,  0,   0b00000000000011111001111110110011),
    (0,  0,   31,  0b00000001111100000001000000110011),
    (31, 0,   31,  0b00000001111100000001111110110011),
    (0,  31,  31,  0b00000001111111111001000000110011),
    (31, 31,  31,  0b00000001111111111001111110110011),
])
def test_sll(rd, rs1, rs2, code):
    assert asm.SLL(rd, rs1, rs2) == code


@pytest.mark.parametrize(
    'rd, rs1, rs2, code', [
    (0,  0,   0,   0b00000000000000000010000000110011),
    (31, 0,   0,   0b00000000000000000010111110110011),
    (0,  31,  0,   0b00000000000011111010000000110011),
    (31, 31,  0,   0b00000000000011111010111110110011),
    (0,  0,   31,  0b00000001111100000010000000110011),
    (31, 0,   31,  0b00000001111100000010111110110011),
    (0,  31,  31,  0b00000001111111111010000000110011),
    (31, 31,  31,  0b00000001111111111010111110110011),
])
def test_slt(rd, rs1, rs2, code):
    assert asm.SLT(rd, rs1, rs2) == code


@pytest.mark.parametrize(
    'rd, rs1, rs2, code', [
    (0,  0,   0,   0b00000000000000000011000000110011),
    (31, 0,   0,   0b00000000000000000011111110110011),
    (0,  31,  0,   0b00000000000011111011000000110011),
    (31, 31,  0,   0b00000000000011111011111110110011),
    (0,  0,   31,  0b00000001111100000011000000110011),
    (31, 0,   31,  0b00000001111100000011111110110011),
    (0,  31,  31,  0b00000001111111111011000000110011),
    (31, 31,  31,  0b00000001111111111011111110110011),
])
def test_sltu(rd, rs1, rs2, code):
    assert asm.SLTU(rd, rs1, rs2) == code


@pytest.mark.parametrize(
    'rd, rs1, rs2, code', [
    (0,  0,   0,   0b00000000000000000100000000110011),
    (31, 0,   0,   0b00000000000000000100111110110011),
    (0,  31,  0,   0b00000000000011111100000000110011),
    (31, 31,  0,   0b00000000000011111100111110110011),
    (0,  0,   31,  0b00000001111100000100000000110011),
    (31, 0,   31,  0b00000001111100000100111110110011),
    (0,  31,  31,  0b00000001111111111100000000110011),
    (31, 31,  31,  0b00000001111111111100111110110011),
])
def test_xor(rd, rs1, rs2, code):
    assert asm.XOR(rd, rs1, rs2) == code


@pytest.mark.parametrize(
    'rd, rs1, rs2, code', [
    (0,  0,   0,   0b00000000000000000101000000110011),
    (31, 0,   0,   0b00000000000000000101111110110011),
    (0,  31,  0,   0b00000000000011111101000000110011),
    (31, 31,  0,   0b00000000000011111101111110110011),
    (0,  0,   31,  0b00000001111100000101000000110011),
    (31, 0,   31,  0b00000001111100000101111110110011),
    (0,  31,  31,  0b00000001111111111101000000110011),
    (31, 31,  31,  0b00000001111111111101111110110011),
])
def test_srl(rd, rs1, rs2, code):
    assert asm.SRL(rd, rs1, rs2) == code


@pytest.mark.parametrize(
    'rd, rs1, rs2, code', [
    (0,  0,   0,   0b01000000000000000101000000110011),
    (31, 0,   0,   0b01000000000000000101111110110011),
    (0,  31,  0,   0b01000000000011111101000000110011),
    (31, 31,  0,   0b01000000000011111101111110110011),
    (0,  0,   31,  0b01000001111100000101000000110011),
    (31, 0,   31,  0b01000001111100000101111110110011),
    (0,  31,  31,  0b01000001111111111101000000110011),
    (31, 31,  31,  0b01000001111111111101111110110011),
])
def test_sra(rd, rs1, rs2, code):
    assert asm.SRA(rd, rs1, rs2) == code


@pytest.mark.parametrize(
    'rd, rs1, rs2, code', [
    (0,  0,   0,   0b00000000000000000110000000110011),
    (31, 0,   0,   0b00000000000000000110111110110011),
    (0,  31,  0,   0b00000000000011111110000000110011),
    (31, 31,  0,   0b00000000000011111110111110110011),
    (0,  0,   31,  0b00000001111100000110000000110011),
    (31, 0,   31,  0b00000001111100000110111110110011),
    (0,  31,  31,  0b00000001111111111110000000110011),
    (31, 31,  31,  0b00000001111111111110111110110011),
])
def test_or(rd, rs1, rs2, code):
    assert asm.OR(rd, rs1, rs2) == code


@pytest.mark.parametrize(
    'rd, rs1, rs2, code', [
    (0,  0,   0,   0b00000000000000000111000000110011),
    (31, 0,   0,   0b00000000000000000111111110110011),
    (0,  31,  0,   0b00000000000011111111000000110011),
    (31, 31,  0,   0b00000000000011111111111110110011),
    (0,  0,   31,  0b00000001111100000111000000110011),
    (31, 0,   31,  0b00000001111100000111111110110011),
    (0,  31,  31,  0b00000001111111111111000000110011),
    (31, 31,  31,  0b00000001111111111111111110110011),
])
def test_and(rd, rs1, rs2, code):
    assert asm.AND(rd, rs1, rs2) == code


@pytest.mark.parametrize(
    'succ,   pred,   code', [
    (0b0000, 0b0000, 0b00000000000000000000000000001111),
    (0b0000, 0b1111, 0b00001111000000000000000000001111),
    (0b1111, 0b0000, 0b00000000111100000000000000001111),
    (0b1111, 0b1111, 0b00001111111100000000000000001111),
])
def test_fence(succ, pred, code):
    assert asm.FENCE(succ, pred) == code


def test_ecall():
    assert asm.ECALL() == 0b00000000000000000000000001110011


def test_ebreak():
    assert asm.EBREAK() == 0b00000000000100000000000001110011


@pytest.mark.parametrize(
    'source,           expected', [
    ('lui   x0 0',     asm.LUI('x0', 0)),
    ('auipc x0 0',     asm.AUIPC('x0', 0)),
    ('jal   x0 0',     asm.JAL('x0', 0)),
    ('jalr  x0 x1 0',  asm.JALR('x0', 'x1', 0)),
    ('beq   x0 x1 0',  asm.BEQ('x0', 'x1', 0)),
    ('bne   x0 x1 0',  asm.BNE('x0', 'x1', 0)),
    ('blt   x0 x1 0',  asm.BLT('x0', 'x1', 0)),
    ('bge   x0 x1 0',  asm.BGE('x0', 'x1', 0)),
    ('bltu  x0 x1 0',  asm.BLTU('x0', 'x1', 0)),
    ('bgeu  x0 x1 0',  asm.BGEU('x0', 'x1', 0)),
    ('lb    x0 x1 0',  asm.LB('x0', 'x1', 0)),
    ('lh    x0 x1 0',  asm.LH('x0', 'x1', 0)),
    ('lw    x0 x1 0',  asm.LW('x0', 'x1', 0)),
    ('lbu   x0 x1 0',  asm.LBU('x0', 'x1', 0)),
    ('lhu   x0 x1 0',  asm.LHU('x0', 'x1', 0)),
    ('sb    x0 x1 0',  asm.SB('x0', 'x1', 0)),
    ('sh    x0 x1 0',  asm.SH('x0', 'x1', 0)),
    ('sw    x0 x1 0',  asm.SW('x0', 'x1', 0)),
    ('addi  x0 x1 0',  asm.ADDI('x0', 'x1', 0)),
    ('slti  x0 x1 0',  asm.SLTI('x0', 'x1', 0)),
    ('sltiu x0 x1 0',  asm.SLTIU('x0', 'x1', 0)),
    ('xori  x0 x1 0',  asm.XORI('x0', 'x1', 0)),
    ('ori   x0 x1 0',  asm.ORI('x0', 'x1', 0)),
    ('andi  x0 x1 0',  asm.ANDI('x0', 'x1', 0)),
    ('slli  x0 x1 0',  asm.SLLI('x0', 'x1', 0)),
    ('srli  x0 x1 0',  asm.SRLI('x0', 'x1', 0)),
    ('srai  x0 x1 0',  asm.SRAI('x0', 'x1', 0)),
    ('add   x0 x1 x2', asm.ADD('x0', 'x1', 'x2')),
    ('sub   x0 x1 x2', asm.SUB('x0', 'x1', 'x2')),
    ('sll   x0 x1 x2', asm.SLL('x0', 'x1', 'x2')),
    ('slt   x0 x1 x2', asm.SLT('x0', 'x1', 'x2')),
    ('sltu  x0 x1 x2', asm.SLTU('x0', 'x1', 'x2')),
    ('xor   x0 x1 x2', asm.XOR('x0', 'x1', 'x2')),
    ('srl   x0 x1 x2', asm.SRL('x0', 'x1', 'x2')),
    ('sra   x0 x1 x2', asm.SRA('x0', 'x1', 'x2')),
    ('or    x0 x1 x2', asm.OR('x0', 'x1', 'x2')),
    ('and   x0 x1 x2', asm.AND('x0', 'x1', 'x2')),
    ('fence 0xf 0xf',  asm.FENCE(0b1111, 0b1111)),
    ('ecall',          asm.ECALL()),
    ('ebreak',         asm.EBREAK()),
])
def test_assemble_base_i(source, expected):
    binary = asm.assemble(source)
    target = struct.pack('<I', expected)
    assert binary == target
