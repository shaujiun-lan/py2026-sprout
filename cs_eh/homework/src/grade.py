import subprocess
import tempfile
import os
import sys

python = sys.executable

INPUT_TEST_TIMESTAMP = "2026-04-04 12:00"
INPUT_TEST_TESTCASE = "".join([
    # =====================================================
    # valid + on time (0 days late)
    # =====================================================
    "name=Alice0, score=100, timestamp=2026-04-04 11:59\n",

    # =====================================================
    # valid + on time (exact deadline)
    # =====================================================
    "name=Bob0, score=100, timestamp=2026-04-04 12:00\n",
    
    # =====================================================
    # valid + within 1 day late
    # =====================================================
    "name=Carol0, score=100, timestamp=2026-04-05 11:59\n",
    
    # =====================================================
    # valid + exactly 1 day late boundary
    # =====================================================
    "name=Dave0, score=100, timestamp=2026-04-05 12:00\n",
    
    # =====================================================
    # valid + 1~3 days late
    # =====================================================
    "name=Eve0, score=100, timestamp=2026-04-06 12:00\n",
    
    # =====================================================
    # valid + exactly 3 days late boundary
    # =====================================================
    "name=Frank0, score=100, timestamp=2026-04-07 12:00\n",
    
    # =====================================================
    # valid + > 3 days late
    # =====================================================
    "name=Grace0, score=100, timestamp=2026-04-08 12:01\n",
    
    # =====================================================
    # missing name → skip
    # =====================================================
    "name=, score=100, timestamp=2026-04-05 12:00\n",
    
    # =====================================================
    # invalid score (non-number)
    # =====================================================
    "name=Heidi0, score=abc, timestamp=2026-04-05 12:00\n",
    
    # =====================================================
    # invalid score (too large)
    # =====================================================
    "name=Ivan0, score=200, timestamp=2026-04-05 12:00\n",
    
    # =====================================================
    # invalid score (negative)
    # =====================================================
    "name=Judy0, score=-5, timestamp=2026-04-05 12:00\n",
    
    # =====================================================
    # missing score
    # =====================================================
    "name=Ken0, score=, timestamp=2026-04-05 12:00\n",
    
    # =====================================================
    # invalid timestamp format (wrong format)
    # =====================================================
    "name=Leo0, score=100, timestamp=2026-04-05-12:00\n",
    
    # =====================================================
    # invalid timestamp format (non-date)
    # =====================================================
    "name=Mallory0, score=100, timestamp=bad_time\n",
    
    # =====================================================
    # missing timestamp
    # =====================================================
    "name=Niaj0, score=100, timestamp=\n",
    
    # =====================================================
    # malformed line
    # =====================================================
    "THIS IS BROKEN LINE\n",

    # =====================================================
    # malformed line
    # =====================================================
    "BROKEN LINE HH\n",

    # =====================================================
    # mixed input
    # =====================================================
    "name=Thomas, score=-2, timestamp=\n",

    # =====================================================
    # mixed input
    # =====================================================
    "name=, score=10, timestamp=s\n",
])

INPUT_TEST_ANSWER = "\n".join([
    "|   name   | raw score | final score |",
    "|  Alice0  |    100    |     100     |",
    "|   Bob0   |    100    |     100     |",
    "|  Carol0  |    100    |      70     |",
    "|  Dave0   |    100    |      70     |",
    "|   Eve0   |    100    |      40     |",
    "|  Frank0  |    100    |      40     |",
    "|  Grace0  |    100    |       0     |",
    "|  Heidi0  |      X    |       X     |",
    "|  Ivan0   |      X    |       X     |",
    "|  Judy0   |      X    |       X     |",
    "|   Ken0   |      X    |       X     |",
    "|   Leo0   |    100    |       X     |",
    "| Mallory0 |    100    |       X     |",
    "|  Niaj0   |    100    |       X     |",
    "|  Thomas  |      X    |       X     |",
])

QUIET = False
JUDGE_ERROR_CODE = 52

def judge_print(*args, **kargs):
    if QUIET:
        return
    print(*args, **kargs)

def run(cmd):
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

def show(title, r):
    judge_print("\n====================")
    judge_print(title)
    judge_print("====================")
    judge_print("return code:", r.returncode)
    judge_print("--- stderr ---")
    judge_print(r.stderr.decode().strip())
    judge_print("--- stdout ---")
    judge_print(r.stdout.decode().strip())

def test_file_errors(script):
    judge_print("\n\n######## FILE ERROR TESTS ########")

    is_passed = True

    r = run([python, script, "no_file.txt", "out.txt", "2026-01-01 00:00"])
    show("input file not exist", r)
    is_passed = (is_passed and r.returncode == JUDGE_ERROR_CODE)

    with tempfile.TemporaryDirectory() as tmpi:
        r = run([python, script, tmpi, "out.txt", "2026-01-01 00:00"])
        show("input path is directory", r)
        is_passed = (is_passed and r.returncode == JUDGE_ERROR_CODE)

    with tempfile.TemporaryDirectory() as tmpi, tempfile.TemporaryDirectory() as tmpo:
        input_path = os.path.join(tmpi, "input.txt")
        open(input_path, "w").close()
        r = run([python, script, input_path, tmpo, "2026-01-01 00:00"])
        show("output path is directory", r)
        is_passed = (is_passed and r.returncode == JUDGE_ERROR_CODE)

    no_such_dir = os.path.join("no_such_dir", "out.txt")
    with tempfile.TemporaryDirectory() as tmpi:
        input_path = os.path.join(tmpi, "input.txt")
        open(input_path, "w").close()
        r = run([python, script, input_path, no_such_dir, "2026-01-01 00:00"])
        show("output dir not exist", r)
        is_passed = (is_passed and r.returncode == JUDGE_ERROR_CODE)
    
    return is_passed

def test_input_errors(script):
    judge_print("\n\n######## INPUT ERROR TESTS ########")

    with tempfile.TemporaryDirectory() as tmpd:
        input_path = os.path.join(tmpd, "input.txt")
        output_path = os.path.join(tmpd, "out.txt")

        with open(input_path, "w") as f:
            f.write(INPUT_TEST_TESTCASE)

        r = run([python, script, input_path, output_path, INPUT_TEST_TIMESTAMP])
        show("input error handling", r)

        judge_print("\n--- output file ---")
        with open(output_path, "r") as f:
            output = f.read().strip()
            judge_print(output)
        
        if r.returncode != 0:
            return False
        
        if output != INPUT_TEST_ANSWER:
            return False
    
    return True

# =========================================================
# main
# =========================================================
def main():
    if len(sys.argv) != 2:
        judge_print(f"Usage: python {sys.argv[0]} [your ans.py]")
        sys.exit(1)

    script = sys.argv[1]

    file_test = test_file_errors(script)
    input_test = test_input_errors(script)

    print("\n==============================")
    print("RESULT")
    print("==============================")

    print("File error handling :", "PASS" if file_test else "FAIL")
    print("Input error handling:", "PASS" if input_test else "FAIL")


if __name__ == "__main__":
    main()
