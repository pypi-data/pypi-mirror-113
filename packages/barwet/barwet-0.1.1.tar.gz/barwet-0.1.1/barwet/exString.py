def auto_as(obj):
    if isinstance(obj, str):
        if obj.lower() == 'false':
            return False
        elif obj.lower() == 'true':
            return True
        else:
            try:
                _f = float(obj)
            except ValueError:
                # 不可转化为数值的字符串
                return obj
            else:
                try:
                    _i = int(obj)
                except ValueError:
                    # 可转化为浮点数但不能转化为整数的字符串
                    return _f
                else:
                    if _f == _i:
                        # 可转化为整数的字符串
                        return _i
                    else:
                        return _f

def to_multilines(text: str, ncols=20, eng=False):
    if eng:
        return text
    else:
        fmt_text = []
        index = 0
        while index < len(text):
            subtext = text[index:index+ncols]
            fmt_text.append(subtext)
            index += ncols
        fmt_text = '\n'.join(fmt_text)
        return fmt_text


if __name__ == '__main__':
    print(to_multilines('导入的项目名称，该名称将会直接作为项目名称保存到数据库。数据目录下必须存在以该名称命令的数据目录才能导入该项目的数据，请在导入前核对数据目录下的项目名称'))