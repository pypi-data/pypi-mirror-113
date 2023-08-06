import glob
import json
import os
import time
from builtins import staticmethod
from zipfile import ZipFile, is_zipfile

from jinja2 import Template
from ucode.helpers.clog import CLog
from ucode.helpers.misc import dos2unix, findfiles
from ucode.helpers.shell_helper import ShellHelper
from ucode.models.problem import Problem, TestCase


class TestcaseService:
    @staticmethod
    def load_testcases(path: str):
        """

        @param path:    .txt / .zip file for 'ucode' format
                        .zip file / folder for 'cms', 'themis', 'hackerrank'
                        .zip file if format is 'cms',
                        folder if format is 'themis'
        @param format: ucode / cms / themis / hackerrank
        @return:
        """

        path = os.path.abspath(path)
        if not os.path.exists(path):
            CLog.error(f"Path not existed: {path}")
            return None

        if os.path.isfile(path) and not is_zipfile(path):
            CLog.info(f"Loading testcases from single file (ucode format): {path}")
            return TestcaseService.read_ucode_testcases_from_file(path)

        if is_zipfile(path):
            CLog.info(f"Loading testcases from zipfile: {path}")
            with ZipFile(path, 'r') as myzip:
                format, testcase_files = TestcaseService.get_testcase_files_list(path, zip_file=myzip)
                if format == "ucode":
                    inside_archive_file = testcase_files[0]
                    CLog.info(f"Loading testcases (ucode format) from file: {path}\\{inside_archive_file}")
                    return TestcaseService.read_ucode_testcases_from_file(path, inside_archive_file=inside_archive_file)
                else: # format == "themis" / "cms" / "themis" / "hackerrank"
                    return TestcaseService.read_testcases_from_zip_file(path, inside_archive_files=testcase_files)

        else: # test folder
            format, testcase_files = TestcaseService.get_testcase_files_list(path, zip_file=None)
            if format == "ucode":
                test_file = testcase_files[0]
                CLog.info(f"Loading testcases (ucode format) from file: {test_file}")
                return TestcaseService.read_ucode_testcases_from_file(test_file)
            elif format == "themis":
                return TestcaseService.read_themis_testcases_from_folder(path)

        # if format == 'ucode':
        #     return TestcaseService.read_ucode_testcases_from_file(path)
        # elif format == 'themis':
        #     return TestcaseService.read_themis_testcases_from_folder(path)
        # elif format == "cms":
        #     return TestcaseService.read_cms_testcases_from_zip_file(path)
        # else:
        #     CLog.error("Testcase format not supported: " + format)

    @staticmethod
    def get_testcase_files_list(path, zip_file=None):
        if zip_file:
            all_files = zip_file.namelist()
            has_input = has_output = False
            has_folder = False
            for file in all_files:
                if file.startswith("input/"):
                    has_input = True
                if file.startswith("output/"):
                    has_output = True
                if "/" in file:
                    has_folder = True
            if has_input and has_output:
                format = "hackerrank"
                inputs = [f for f in all_files if f.startswith("input/")]
                test_files = []
                for input_file in inputs:
                    output_file = input_file.replace("input", "output").replace(".in", ".out")
                    test_files.append((input_file, output_file))
                print(test_files)
                return format, test_files
            elif has_folder:
                format = "themis"
                test_files = []
                inputs = [f for f in all_files if f.endswith(".inp") or f.endswith(".INP")
                          or f.endswith(".in")  or f.endswith(".IN")]
                for input_file in inputs:
                    if input_file.endswith(".INP"):
                        output_file = input_file[:-4] + ".OUT"
                    elif input_file.endswith(".inp"):
                        output_file = input_file[:-4] + ".out"
                    elif input_file.endswith(".in"):
                        output_file = input_file[:-3] + ".out"
                    else:
                        output_file = input_file[:-3] + ".OUT"
                    test_files.append((input_file, output_file))
                print(test_files)
                return format, test_files
            else:
                format = "cms"
                # format 1: input.xxx & output.xxx
                # format 2: x.in & x.ou
                # format 3: x.in & x.ok
                # format 4: x.in & x.ans
                # format 5: inputxx.inp & inputxx.out
                # format 6: x.inp & x.out
                # format 7: inputxx.txt & inputxx.txt
                test_files = []
                input_files = [f for f in all_files if f.endswith(".inp")]
                if not input_files:
                    input_files = [f for f in all_files if f.endswith(".in")]
                if not input_files:
                    input_files = [f for f in all_files if f.startswith("input")]
                input_files.sort(key=lambda s: int("".join([c for c in s if "0" <= c <= "9"])))
                # print("input files", input_files)
                for input_file in input_files:
                    # print("input files", input_file)
                    if input_file.endswith(".inp"):
                        output_file = input_file.replace(".inp", ".out")
                    elif input_file.startswith("input"):
                        output_file = input_file.replace("input", "output")
                        if output_file not in all_files:
                            output_file = input_file.replace("input", "ouput")
                    else:
                        output_file = input_file.replace(".in", ".ou")
                        if output_file not in all_files:
                            output_file = input_file.replace(".in", ".ok")
                        if output_file not in all_files:
                            output_file = input_file.replace(".in", ".ans")
                        if output_file not in all_files:
                            output_file = input_file.replace(".in", ".out")
                    # CLog.info(f"Reading a testcase in {input_file}, {output_file}")
                    test_files.append((input_file, output_file))
                print(test_files)
                return format, test_files
        else:
            all_files = glob.glob(os.path.join(path, "*"))
            folders = [f for f in all_files if os.path.isdir(f)]
            print("Folder", folders)
            has_input = has_output = False
            has_folder = len(folders) > 0
            for folder in folders:
                if folder.endswith("input"):
                    has_input = True
                if folder.endswith("input"):
                    has_output = True
            if has_input and has_output:
                format = "hackerrank"
                CLog.error(f"Reading hackerrank testcases from folder is not supported yet")
            elif has_folder:
                format = "themis"
            else:
                format = "cms"
                CLog.error(f"Reading CMS testcases from folder is not supported yet")

        if not all_files:
            CLog.error(f"No files found in {path}")
            return None

        if len(all_files) < 2 or "testcases.txt" in all_files:
            format = "ucode"
            return format, all_files

        print(all_files)

        return format, all_files

    @staticmethod
    def read_testcases_from_zip_file(zipfile, inside_archive_files):
        testcases = []
        CLog.info(f"Loading CMS testcases from .zip file `{os.path.abspath(zipfile)}`")

        with ZipFile(zipfile, 'r') as myzip:
            for (input_file, output_file) in inside_archive_files:
                fi = myzip.open(input_file)
                fo = myzip.open(output_file)
                _input = fi.read().decode("utf-8")
                _output = fo.read().decode("utf-8")
                testcases.append(TestCase(input=_input, output=_output))

        CLog.info(f"DONE: {len(testcases)} testcases loaded!")
        return testcases

    @staticmethod
    def read_themis_testcases_from_folder(path):
        testcases = []

        test_folders = glob.glob(os.path.join(path, "Test*"))
        for test_folder in test_folders:
            # test_folder = os.path.abspath(test_folder)
            if not os.path.isdir(test_folder):
                continue
            # print(test_folder)

            input_files = findfiles("*.INP", test_folder)
            output_files = findfiles("*.OUT", test_folder)
            # print(input_files, len(input_files))
            # print(output_files, len(output_files))
            if len(input_files) != 1 or len(output_files) != 1:
                CLog.error(f"Invalid testcase folder `{os.path.abspath(test_folder)}`")
                continue
            input_file = input_files[0]
            output_file = output_files[0]

            # print(input_file, output_file)
            with open(input_file, 'r') as fi:
                _input = fi.read()
            with open(output_file, 'r') as fo:
                _output = fo.read()
            testcases.append(TestCase(input=_input, output=_output))
        return testcases

    @staticmethod
    def read_ucode_testcases_from_file(testcase_file, inside_archive_file=None):
        count = 0
        inputi = ""
        outputi = ""
        is_output = False

        testcases = []
        name = ""
        if inside_archive_file:
            with ZipFile(testcase_file, 'r') as myzip:
                fi = myzip.open(inside_archive_file)
                lines = fi.read().decode("utf-8").split("\n")
        else:
            with open(testcase_file, 'r', encoding="utf-8") as fi:
                lines = fi.readlines()

        for line in lines:
            if line.startswith("###"):

                if count > 0:
                    testcases.append({'input': inputi.rstrip(), 'output': outputi.rstrip(), 'name': name})

                name = line[3:].strip()
                # print("N:", name)
                count += 1

                is_output = False

                inputi = outputi = ""

                continue
            elif line.startswith("---"):
                is_output = True
            else:
                if is_output:
                    outputi += line
                else:
                    inputi += line
        if inputi.rstrip() or outputi.rstrip():
            testcases.append({'input': inputi.rstrip(), 'output': outputi.rstrip(), 'name': name})

        return testcases

    @staticmethod
    def execute(source_code_file: str, _input: str = "", raise_exception=True, timeout=60):
        """

        @param timeout:
        @param raise_exception:
        @param source_code_file:
        @param _input:
        @return: output, compile_time, execute_time
        """

        folder, file_name = os.path.split(source_code_file)
        file_base_name, file_ext = os.path.splitext(file_name)

        if file_ext == ".py":
            compile_needed = False
        else:
            compile_needed = True

        t0 = time.time()
        compile_time = -1

        owd = os.getcwd()
        os.chdir(folder)

        if compile_needed:
            if file_ext != ".cpp":
                CLog.error(f"Language not supported: `{file_ext}`")
                os.chdir(owd)
                return
            compile_cmd = ["C:\\Program Files\\CodeBlocks\\MinGW\\bin\\g++.exe", "-std=c++14",
                           file_name,
                           "-pipe", f"-o{file_base_name}.exe"]
            ShellHelper.execute(compile_cmd, timeout=timeout)
            compile_time = time.time() - t0

        if file_ext == ".py":
            run_cmd = ["python", file_name]
        else:
            run_cmd = [f"{file_base_name}.exe"]

        t0 = time.time()
        output = ShellHelper.execute(run_cmd, input=_input, raise_exception=raise_exception)
        execute_time = time.time() - t0
        os.chdir(owd)
        return output, compile_time, execute_time

    @staticmethod
    def save_testcases(problem_folder, problem: Problem, format="both"):
        """

        @param problem_folder:
        @param problem:
        @param format: ucode | themis | both
        @return:
        """
        template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../dsa/templates')

        if format:
            if format == "ucode" or format == "both":
                CLog.info("Writing testcases in ucode format")
                testcases = problem.testcases
                if testcases:
                    with open(os.path.join(template_path, 'testcases.txt.j2'), encoding="utf-8") as file_:
                        template = Template(file_.read())
                        for i, t in enumerate(testcases):
                            t.name = "Test #%02d" % (i + 1)
                        content = template.render(testcases=testcases)
                        testcase_path = os.path.join(problem_folder, "testcases.txt")
                        f = open(testcase_path, 'w', encoding="utf-8", newline='')
                        f.write(dos2unix(content))
                        f.close()
                        CLog.info(f"Testcases saved to '{testcase_path}'")

                if problem.stock_testcases:
                    with open(os.path.join(template_path, 'testcases.txt.j2'), encoding="utf-8") as file_:
                        template = Template(file_.read())
                        for i, t in enumerate(problem.stock_testcases):
                            t.name = "Test #%02d" % (i + 1)
                        content = template.render(testcases=problem.stock_testcases)
                        testcase_path = os.path.join(problem_folder, "testcases_stock.txt")
                        f = open(testcase_path, 'w', encoding="utf-8", newline='')
                        f.write(dos2unix(content))
                        f.close()
                        CLog.info(f"Testcases saved to '{testcase_path}'")

                if problem.testcases_sample:
                    with open(os.path.join(template_path, 'testcases.txt.j2'), encoding="utf-8") as file_:
                        template = Template(file_.read())
                        for i, t in enumerate(problem.testcases_sample):
                            t.name = "Test #%02d" % (i + 1)
                        content = template.render(testcases=problem.testcases_sample)
                        testcase_path = os.path.join(problem_folder, "testcases_sample.txt")
                        f = open(testcase_path, 'w', encoding="utf-8", newline='')
                        f.write(dos2unix(content))
                        f.close()

    @staticmethod
    def generate_testcases(problem_folder, testcase_count=20,
                           programming_language=None, format=None, overwrite=False):
        """

        @param problem_folder:
        @param testcase_count:
        @param programming_language: py | cpp | pas, None = auto detect
        @param format: ucode | themis | both | None, None --> not save to disk
        @return:
        """
        from ucode.services.dsa.problem_service import ProblemService
        # problem: Problem = ProblemService.load(problem_folder)
        meta, folders = ProblemService.detect_problem_code_in_folder(problem_folder)
        # print(problem)
        print(json.dumps(folders))
        print(json.dumps(folders['solutions']))
        print(json.dumps(folders['test_generators']))
        # return
        input_generator_files = folders['test_generators']
        solution_files = folders['solutions']

        if not input_generator_files:
            CLog.error("No input generator file found!")
            return
        if not solution_files:
            CLog.error("No solution file found!")
            return

        input_generator_file = input_generator_files[0]
        solution_file = solution_files[0]
        if programming_language:
            prefered_generators = [v for v in input_generator_files if v.endswith(programming_language)]
            if prefered_generators:
                input_generator_file = prefered_generators[0]
            else:
                CLog.warn(f"No input generator file found for preferred language `{programming_language}`,"
                          f"Using `{input_generator_file}` instead.")

            prefered_solutions = [v for v in solution_files if v.endswith(programming_language)]
            if prefered_solutions:
                solution_file = prefered_solutions[0]
            else:
                CLog.warn(f"No solution file found for preferred language `{programming_language}`,"
                          f"Using `{input_generator_file}` instead.")

        input_generator_file = os.path.abspath(input_generator_file)
        solution_file = os.path.abspath(solution_file)
        print(input_generator_file, solution_file, sep='\n')

        testcases = []
        for i in range(1, testcase_count + 1):
            _input, input_compile_time, input_time = TestcaseService.execute(input_generator_file, _input=str(i),
                                                                             timeout=180)
            # print("input:", _input)
            _output, compile_time, output_time = TestcaseService.execute(solution_file, _input=_input.strip())

            testcases.append(TestCase(input=_input, output=_output))
            print("Testcase #%02d generated! Input generation compile time: %.2fs, "
                  "input generation running time: %.2fs, solution complie time: %.2f, solution running time: %.2fs"
                  % (i, input_compile_time, input_time, compile_time, output_time))

        if format:
            problem = Problem()
            problem.testcases = testcases
            TestcaseService.save_testcases(problem_folder, problem, format)
        return testcases


if __name__ == "__main__":
    # folder = "D:\\projects\\ucode\\dsa-thematic-problems\\de_thi_hsg\\hanoi_2020_2021_thcs\\p4_itable"
    # # folder = "../../../problems/p4_itable"
    # T = TestcaseService.generate_testcases(problem_folder=folder, format="ucode",
    #                                        programming_language="cpp",
    #                                        testcase_count=10)
    # print("testcases:", len(T))

    # testcase_file = "D:\\projects\\freecontest\\beginner\\Beginner Free Contest 11 (01-09-2019)" \
    #                 "\\Bộ test (01-09-2019)\\AVERAGE.zip"
    # testcase_file = r"D:\projects\ucode\ucode-cli\ucode\services\testcase\sample_testcases\sample_testcases.zip"
    # testcase_file = r"D:\projects\ucode\ucode-cli\ucode\services\testcase\sample_testcases\ucode\testcases.txt"
    # testcase_file = r"D:\projects\ucode\ucode-cli\ucode\services\testcase\sample_testcases\ucode\testcases.zip"
    # testcase_file = r"D:\projects\ucode\ucode-cli\ucode\services\testcase\sample_testcases\ucode"
    # testcase_file = r"D:\projects\ucode\ucode-cli\ucode\services\testcase\sample_testcases\themis\sample_testcases.zip"
    # testcase_file = r"D:\projects\ucode\ucode-cli\ucode\services\testcase\sample_testcases\themis"
    testcase_file = r"D:\projects\ucode\ucode-cli\ucode\services\testcase\sample_testcases\hackerrank\testcases_hackerrank.zip"
    # testcase_file = r"D:\projects\ucode\ucode-cli\ucode\services\testcase\sample_testcases\cms\BANK.zip"
    testcases = TestcaseService.load_testcases(testcase_file)
    print(testcases)
    print(len(testcases))
    print(testcases[0])

