import sys

sys.path.append("../mini_fuzzer/")

from config import DECREMENT_VALUE, INCREMENT_VALUE
from mutation import (add_random_character, arithmetic_dec, arithmetic_inc,
                      bitflip, byteflip, change_arguments_number,
                      delete_random_character)


def test_bit_byte_flip():
    # 通常の文字列
    test_str = "hello, world"
    assert bitflip(test_str) != test_str
    assert byteflip(test_str)!= test_str
    
    # 空文字
    assert bitflip("") == ""
    assert byteflip("") == ""
    
    # 日本語 and 絵文字
    test_str = "特殊な入力のテスト🌏"
    assert bitflip(test_str) != test_str
    assert byteflip(test_str) != test_str
    
    # 制御文字
    test_str = "Hello\nWorld\t"
    assert bitflip(test_str) != test_str
    assert byteflip(test_str) != test_str

    ## ナル文字
    assert bitflip("\x00") != test_str
    assert byteflip("\x00") != test_str



def test_arithmetic_inc_dec():
    # 整数が与えられた場合
    assert arithmetic_inc("100") == str(100 + INCREMENT_VALUE)
    assert arithmetic_dec("100") == str(100 - DECREMENT_VALUE)
    
    # 数字以外が与えられた場合
    assert arithmetic_inc("hello world") == "hello world"
    assert arithmetic_dec("hello world") == "hello world"

    #浮動小数点数が与えられた場合
    assert arithmetic_inc("15.5") == str(15.5 + INCREMENT_VALUE)
    assert arithmetic_dec("15.5") == str(15.5 - DECREMENT_VALUE)

    #負の値が与えられた場合
    assert arithmetic_inc("-15.5") == str(-15.5 + INCREMENT_VALUE)
    assert arithmetic_dec("-15.5") == str(-15.5 - DECREMENT_VALUE)
    
    #数値だけで構成される文字列
    assert arithmetic_inc("⑤⑥⑦") == "⑤⑥⑦"
    assert arithmetic_dec("⑤⑥⑦") == "⑤⑥⑦"
    assert arithmetic_inc("2²") == "2²"
    assert arithmetic_dec("2²") == "2²"

def test_add_delete_character():
    # 通常の文字列
    assert len(add_random_character("aaaa")) == 5
    assert len(delete_random_character("aaaa")) == 3

    # 空文字
    assert len(add_random_character("")) == 1  
    assert delete_random_character("") == ""
    
    # 日本語 and 絵文字
    test_str = "特殊な入力のテスト🌏"
    assert len(add_random_character(test_str)) == len(test_str) + 1
    assert len(delete_random_character(test_str)) == len(test_str) - 1
    
    # 制御文字
    test_str = "Hello\nWorld\t"
    assert len(add_random_character(test_str)) == len(test_str) + 1
    assert len(delete_random_character(test_str)) == len(test_str) - 1

def test_change_arg_number():
    test_list = ["arg1", "arg2", "arg3"]
    original_len = len(test_list)
    result_len = len(change_arguments_number(test_list))
    assert original_len == result_len or original_len == result_len - 1 or original_len == result_len + 1
    
    #空のリスト
    result = change_arguments_number([])
    assert len(result) == 1


