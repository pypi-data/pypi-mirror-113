import os
import glob
from typing import Dict, Sequence

def get_versions(pattern, sep='-', num_prefix=2) -> Dict[str, Sequence[int]]:
    """获取指定目录下的版本数组
    Args:
        pattern: glob路径模板
        sep: 程序名与版本的分隔符
        num_prefix: 文件后缀数目
    Returns:
        多个版本号的数组，每个版本号由一组整数表示
    """
    versions = {}
    for fp in glob.glob(pattern):
        arr = os.path.basename(fp).split(sep)[1].split('.')[:-num_prefix]
        versions[fp] = [int(i) for i in arr]
        # versions.append([int(i) for i in arr])
    return versions

def get_latest_index(versions: Sequence[Sequence[int]]) -> int:
    """
    Args:
        versions: 多个版本号的数组，每个版本号由一组整数表示
    Return:
        最新版本在versions中的索引
    """
    max_index = len(versions[0]) - 1
    
    def _recursive(used: Sequence[int], i: int) -> int:
        """
        Args:
            used: 索引数组，在versions的子集里面查找
            i: 在每个version的第i个元素里面比较
        Return:
            最新版本在versions中的索引
        Exceptions:
            存在多个最新版本时会报错
        """
        maxv = -1
        _versions = []
        _index = []
        for vidx,version in enumerate(versions):
            if vidx not in used or version[i] < maxv:
                continue
            if version[i] > maxv:
                maxv = version[i]
                _versions = [version]
                _index = [vidx]
            elif version[i] == maxv:
                _versions.append(version)
                _index.append(vidx)

        if len(_versions) == 1:
            return _index[0]
        else:
            if i == max_index:
                raise Exception('Multiple latest versions!')
            return _recursive(_index, i + 1)

    return _recursive(list(range(len(versions))), 0)

def get_latest_file(pattern, *args, **kwargs):
    data = get_versions(pattern, *args, **kwargs)
    files = []
    versions = []
    for k, v in data.items():
        files.append(k)
        versions.append(v)

    max_index = get_latest_index(versions)
    max_file = files[max_index]

    return max_file