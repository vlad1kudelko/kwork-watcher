import main_1_parser

def test__parser_info_stay():
    arr = [
        ('Осталось: 1 ч. 49 мин.',      '0 01:49:00'),
        ('Осталось: 2 д. 6 ч.',         '2 06:00:00'),
        ('Осталось: 1 д. 23 ч.',        '1 23:00:00'),
        ('Осталось: 2 д.',              '2 00:00:00'),
        ('Осталось: 21 ч. 36 мин.',     '0 21:36:00'),
        ('Осталось: 53 мин.',           '0 00:53:00'),
        ('Осталось: 4 ч. 9 мин.',       '0 04:09:00'),
        ('Осталось: 11 ч. 6 мин.',      '0 11:06:00'),
        ('Осталось: 11 ч.',             '0 11:00:00'),
        ('Осталось: 3 мин.',            '0 00:03:00'),
        ('Осталось: 20 сек.',           '0 00:00:20'),
        ('Осталось: 2 ч.',              '0 02:00:00'),
    ]
    assert main_1_parser.parser_info_stay([  ]) == None
    assert main_1_parser.parser_info_stay(['']) == None
    for item in arr:
        assert main_1_parser.parser_info_stay([ '', item[0] ]) == item[1]
        assert main_1_parser.parser_info_stay([   item[0]   ]) == item[1]
        assert main_1_parser.parser_info_stay([ item[0], '' ]) == item[1]
