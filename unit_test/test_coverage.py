import sys
from unittest.mock import mock_open, patch

import pytest

sys.path.append("../mini_fuzzer/")

from mini_fuzzer.coverage import get_excutable_line, get_executed_line

sample1_gcov_data = [
    " -: 0:Source:sample1.cpp\n",
    " -: 0:Graph:sample1.gcno\n",
    " -: 0:Data:sample1.gcda\n",
    " -: 0:Runs:1\n",
    " -: 0:Programs:1\n",
    " 1: 1:int main() {\n",
    " 1: 2:  int a = 0;\n",
    " -: 3:  // comment\n",
    " 1: 4:  return a;\n",
    " -: 5:}\n"
]

sample2_gcov_data = [
    " -: 0:Source:sample2.c\n",
    " -: 0:Graph:sample2.gcno\n",
    " -: 0:Data:sample2.gcda\n",
    " -: 0:Runs:1\n",
    " -: 0:Programs:1\n",
    " 1: 1:int main() {\n",
    " 1: 2: int num = 1 \n" 
    " 1: 3: if((num % 2) == 0)\n",
    "#####: 4: printf(\"%d is odd\", num);\n",
    " -: 5:  else {    \n "
    " 1: 6:    printf(\"%d is odd\", num);\n",                   
    " -: 7:  }\n",
    " -: 8:}\n"
]


@pytest.fixture
def mock_files():
    sample1_gcov_str = "".join(sample1_gcov_data)
    sample2_gcov_str = "".join(sample2_gcov_data)
    
    m = mock_open()
    m.side_effect = [mock_open(read_data=sample1_gcov_str).return_value,
                     mock_open(read_data=sample2_gcov_str).return_value]
    with patch("mini_fuzzer.coverage.open", m) as mock_file:
        yield mock_file

@pytest.fixture
def mock_find_files():
    with patch("mini_fuzzer.coverage.find_files", return_value=["sample1.cpp.gcov", "sample2.cpp.gcov"]) as mock_find:
        yield mock_find

def test_get_executable_line(mock_files, mock_find_files):
    assert get_excutable_line() == 8

def test_get_executab_line(mock_files, mock_find_files):
    assert get_executed_line() == 7

