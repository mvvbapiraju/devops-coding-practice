import os, sys, subprocess, glob

def py_compile_all():
    py_files = glob.glob("Barclays/exercises/**/solution.py", recursive=True)
    for p in py_files:
        subprocess.check_call([sys.executable, "-m", "py_compile", p])
    print(f"Compiled {len(py_files)} solution files.")

def smoke_runs():
    code1 = 'from Barclays.exercises._01_log_slo_gate.solution import slo_breaches\nrows=[("2026-01-07T09:00:01Z","auth","OK",210),("2026-01-07T09:02:50Z","auth","ERROR",1300)]\nprint(slo_breaches(rows,300,250,0.01))'
    subprocess.check_call([sys.executable, "-c", code1])

    code2 = 'from Barclays.exercises._02_ci_secret_linter.solution import lint_ci_yaml\ny="""build:\n  script:\n    - echo $GITHUB_TOKEN\n"""\nprint(lint_ci_yaml(y))'
    subprocess.check_call([sys.executable, "-c", code2])

    code4 = 'from Barclays.exercises._04_blue_green_cutover.solution import propose_cutover\nevents=[("2026-01-07T09:00:00Z","green",True,0.001,180),("2026-01-07T09:10:01Z","green",True,0.001,180)]\nprint(propose_cutover(events,10,0.01,250,0.99))'
    subprocess.check_call([sys.executable, "-c", code4])

if __name__ == "__main__":
    py_compile_all()
    smoke_runs()
    print("CI smoke OK")
