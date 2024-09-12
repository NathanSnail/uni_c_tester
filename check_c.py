import os
import re
import subprocess
import sys

ansi = "\033"
red = f"{ansi}[31;4m[-] "
blue = f"{ansi}[96m[*] "
green = f"{ansi}[32m[+] "
reset = f"{ansi}[0m"
if len(sys.argv) < 2:
	print(f"{red}No c file passed{reset}")
	print(f"{blue}Use like: {reset}py check_c.py program.c")
	exit(1)
cpath = sys.argv[1]
source = open("./cases", "r").read()
if source[-1] == "\n":
	source = source[:-1]
cases = re.split(r"(?<!\t)\n\n(?!\t)", source)
failed = []
print(f"{blue}Testing {len(cases)} test case{"s" if len(cases) > 1 else ""}:{reset}")
for n, case in enumerate(cases):
	sections = case.split("\n\n\t\n\n")
	args = sections[0]
	goal = sections[1]
	compilation_code = subprocess.run(
		[
			"gcc",
			"-Wall",
			"-Wextra",
			"-Werror",
			"-Wpedantic",
			"-pedantic-errors",
			"-std=c99",
			cpath,
			"-o",
			"out",
		]
	).returncode
	if compilation_code != 0:
		print(f"{red}Compilation failed")
		exit(1)
	result = subprocess.run(
		["./out"], input=args, encoding="ascii", stdout=subprocess.PIPE
	).stdout
	os.remove("./out")
	if result != goal:
		print(f"{red}Test case {n + 1} failed:{reset}")
		print(f"\n{blue}Got:{reset}")
		print(result)
		print(f"\n{blue}Expected:{reset}")
		print(goal, "\n")
		open("./output", "w").write(result + "\n")
		open("./goal", "w").write(goal + "\n")
		subprocess.run(["diff", "--color", "./output", "./goal"])
		os.remove("./output")
		os.remove("./goal")
		print()
		failed.append(n + 1)
	else:
		print(f"{green}Test case {n + 1} passed!{reset}")

if len(failed) == 0:
	print(f"{green}All test cases passed!{reset}")
elif len(failed) == len(cases):
	print(f"{red}All test cases failed")
else:
	case_list = ", ".join([str(x) for x in failed])
	case_str = f"case{"s" if len(failed) > 1 else ""}"
	print(f"{red}Test {case_str} [{case_list}] failed{reset}")
