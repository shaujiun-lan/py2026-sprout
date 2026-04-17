USAGE = """
Usage:
  {script} [input file] [output file] [deadline timestamp]

Arguments:
  input file:
    輸入檔案，每一行代表一筆紀錄

  output file:
    輸出結果檔案(表格格式)

  deadline timestamp:
    截止時間，格式為 YYYY-MM-DD HH:MM

Example:
  python {script} input.txt output.txt "2026-04-04 12:00"

  input.txt:
    name=Alice, score=80, timestamp=2026-04-10 13:45
    name=Bob, score=35, timestamp=2026-03-31 00:32
    name=Jimmy, score=0, timestamp=2026-03-31 15:17
    name=Thomas, score=100, timestamp=2026-04-05 10:58

  output.txt:
    |   name   | raw score | final score |
    |  Alice   |     80    |       0     |
    |   Bob    |     35    |      35     |
    |  Jimmy   |      0    |       0     |
    |  Thomas  |    100    |      70     |

Note:
  final score = raw score x late ratio
  late ratio:
    - on time        -> 1.0
    - 0 - 1 day late -> 0.7
    - 1 - 3 days     -> 0.4
    - > 3 days       -> 0.0
"""

MAX_NAME_LEN = 10
TIMESTAMP_FMT = "%Y-%m-%d %H:%M"

import sys
from datetime import datetime

def calc_late_ratio(timestamp: datetime, deadline: datetime) -> float:
    ratio = 1.0
    if deadline < timestamp:
        late_seconds = (timestamp - deadline).total_seconds()
        late_days = late_seconds / 86400

        if 0.0 < late_days <= 1.0:
            ratio = 0.7
        elif 1.0 < late_days <= 3.0:
            ratio = 0.4
        else:
            ratio = 0.0
    return ratio

def score_cell(val):
    return f"{val:>3}"

def pr_error(*args, **kargs):
    print("[ERROR] ", *args, file=sys.stderr, **kargs)

def main():
    # 檢查參數數量
    if len(sys.argv) != 4:
        print(USAGE.format(script=sys.argv[0]))
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    deadline_str = sys.argv[3]
    deadline = datetime.strptime(deadline_str, TIMESTAMP_FMT)

    # 開啟檔案
    rf = open(input_file, "r")
    wf = open(output_file, "w")

    # 寫入表格標題列
    wf.write(f"|{'name':^{MAX_NAME_LEN}}"
             f"| raw score "
             f"| final score |\n")

    # 逐行處理輸入檔案
    while True:
        # 讀取一行，去除多餘的空格、換行字元
        line = rf.readline().strip(" \r\n")

        # 讀到檔案尾巴了，離開迴圈
        if len(line) == 0:
            break

        # 解析 input 格式， name=..., score=..., timestamp=...
        name, raw_score_str, timestamp_str = (
            field.split("=")[1]
            for field in line.split(", ")
        )
        raw_score = int(raw_score_str)
        timestamp = datetime.strptime(timestamp_str, TIMESTAMP_FMT)

        # 計算 final score
        late_ratio = calc_late_ratio(timestamp, deadline)
        final_score = int(raw_score * late_ratio)
 
        # 寫入 output file (一列)
        wf.write(f"|{name:^{MAX_NAME_LEN}}"
                 f"|{score_cell(raw_score):^11}"
                 f"|{score_cell(final_score):^13}|\n")

    # 關閉檔案
    rf.close()
    wf.close()


if __name__ == "__main__":
    main()