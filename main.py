import io
import json
from codecs import getencoder, getdecoder, getreader, getwriter, StreamRecoder
from typing import Any, Dict, Hashable, List, Tuple, Generator


def run_loop(stream: List[bytes]) -> Generator[bytearray, None, None]:
    for b in stream:
        yield bytearray(b).lstrip(b" ").lstrip(b"\t")


# Credit https://stackoverflow.com/a/61416215
def join_duplicate_keys(ordered_pairs: List[Tuple[Hashable, Any]]) -> Dict:
    d: Dict = {}
    for k, v in ordered_pairs:
        if k in d:
            if isinstance(d[k], list):
                d[k].append(v)
            else:
                d[k] = [d[k], v]
        else:
            d[k] = v
    return d


def main(file: str) -> bytearray:
    with io.open(file, "rb") as f:
        kv_file = StreamRecoder(
            f,
            getencoder("UTF-16LE"),
            getdecoder("UTF-16LE"),
            getreader("UTF-16LE"),
            getwriter("UTF-16LE"),
        ).readlines()

    final_kv = bytearray()
    final_kv += b"{\r\n"

    for kv in run_loop(kv_file):
        if kv.startswith(b'"'):
            if final_kv.endswith(b'"\r\n'):
                final_kv[-3:] = b'",\r\n'
            elif final_kv.endswith(b"}\r\n"):
                final_kv[-3:] = b"},\r\n"

            if (idx := kv.find(b'"\t\t"')) != -1:
                final_kv += kv[: idx + 1] + b":" + kv[idx + 1 :].replace(b"\t", b" ")
            else:
                final_kv += kv
        elif kv.endswith(b"{\r\n"):

            final_kv[-3:] = b'":\r\n'
            final_kv += kv
        elif kv == b"\r\n":
            continue
        else:
            final_kv += kv

        # print(kv)
    final_kv += b"}\r\n"

    return final_kv


if __name__ == "__main__":
    kv_data = main(".\\data\\items_game.txt")
    json.loads(kv_data, object_pairs_hook=join_duplicate_keys)
    # print(
    #     json.dumps(
    #         json.loads(kv_data, object_pairs_hook=join_duplicate_keys),
    #         indent=4,
    #         sort_keys=True,
    #     )
    # )
