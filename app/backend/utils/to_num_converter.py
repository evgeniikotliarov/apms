class ToNum:
    def to_num(self, str_num: str):
        if not (str_num.__class__ is str):
            return str_num
        if '.' in str_num:
            return self.to_float(str_num)
        else:
            return self.to_int(str_num)

    def to_int(self, str_num):
        if str_num[0] == '0' and str_num.__len__() > 1:
            return self.to_int(str_num[1:])
        return int(str_num)

    def to_float(self, str_num):
        if str_num[0] == '0' and str_num.__len__() > 1 and str_num[1] != '.':
            return self.to_float(str_num[1:])
        return float(str_num)
