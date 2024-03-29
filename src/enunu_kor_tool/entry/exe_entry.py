import shutil
import cli_ui

from enunu_kor_tool import lang

MODULE_DICT = {
    "analysis4vb": {"module": "enunu_kor_tool.analysis4vb.analysis", "func": "cli_ui_main"},
    "g2pk4utau": {"module": "enunu_kor_tool.g2pk4utau.g2pk4utau", "func": "cli_ui_main"},
    "ustx2lab": {"module": "enunu_kor_tool.entry.ustx2lab", "func": "cli_ui_main"},
    "lab2ntlab": {"module": "enunu_kor_tool.entry.lab2ntlab", "func": "cli_ui_main"},
    "check4lab": {"module": "enunu_kor_tool.entry.check4lab", "func": "cli_ui_main"},
}


MODULE_LIST = [
    "analysis4vb",
    "g2pk4utau",
    "ustx2lab",
    "lab2ntlab",
    "check4lab",
]


def cli_ui_main():
    from enunu_kor_tool import version

    global MODULE_LIST

    print()
    print("".center(40, "#"))
    print(f" {version.package_name} ver.{version.version} ".center(40, " "))
    print(f" Dev. Cardroid ".center(40, " "))
    print("".center(40, "#"))
    print()

    try:
        lang.cli_ui_main()  # 언어 설정
        L = lang.get_global_lang()
        print()

        MODULE_DESC_LIST = {
            "analysis4vb": L("analysis4vb (ENUNU 통계)"),
            "g2pk4utau": L("g2pk4utau (한국어 자소 -> 음소 변환기)"),
            "ustx2lab": L("ustx2lab (ustx, ust -> lab 변환기)"),
            "lab2ntlab": L("lab2ntlab (lab 시간 표시 제거)"),
            "check4lab": L("check4lab (ustx, ust <-> lab 일치 여부 검사 모듈) (beta.)"),
        }

        selected_module = cli_ui.ask_choice(L("사용할 모듈을 선택하세요."), choices=MODULE_LIST, func_desc=lambda m: MODULE_DESC_LIST[m], sort=False)

        module_info = MODULE_DICT[selected_module]
        module = __import__(module_info["module"], fromlist=[module_info["module"]])
        func = getattr(module, module_info["func"])

        func()

        print()
    except KeyboardInterrupt:
        print("Done.")


def main():
    import os, sys

    if len(sys.argv) > 1 and sys.argv[1] == "--gen":
        batch_file = (
            "@echo off\n"
            "\n"
            "setlocal\n"
            "set TMP=Temp\n"
            "set TEMP=Temp\n"
            "set LANG_DIR_PATH=.\lang\n"
            "set MECAB_KO_DIC_PATH=.\enunu_kor_tool\mecab\mecab-ko-dic -r .\enunu_kor_tool\mecab\mecabrc\n"
            "enunu_kor_tool\enunu_kor_tool.exe\n"
            "endlocal\n"
            "\n"
            "pause"
        )

        with open(os.path.join("dist", "enunu_kor_tool", "Start.bat"), "w", encoding="utf-8") as f:
            f.write(batch_file)

        os.system(
            (
                "pyinstaller "
                '--add-data="dep_package\mecab;mecab" '
                '--add-data="enunu_kor_tool_python\Lib\site-packages\konlpy;konlpy" '
                '--add-data="dep_package\g2pK\g2pk;g2pk" '
                '--add-data="enunu_kor_tool_python\Lib\site-packages\jamo\data;jamo\data" '
                '--hidden-import="konlpy" '
                '--hidden-import="matplotlib" '
                '--hidden-import="matplotlib.backends.backend_tkagg" '
                '--hidden-import="enunu_kor_tool.analysis4vb" '
                '--hidden-import="enunu_kor_tool.analysis4vb.functions.lab" '
                '--hidden-import="enunu_kor_tool.analysis4vb.functions.ust" '
                '--hidden-import="enunu_kor_tool.g2pk4utau.g2pk4utau" '
                '--hidden-import="enunu_kor_tool.utaupyk._ustx2ust" '
                '--hidden-import="enunu_kor_tool.utaupyk._ust2hts" '
                '--hidden-import="enunu_kor_tool.entry.ustx2lab" '
                '--hidden-import="enunu_kor_tool.entry.lab2ntlab" '
                '--hidden-import="enunu_kor_tool.entry.check4lab" '
                "--clean "
                "--distpath dist\enunu_kor_tool "
                '-n "enunu_kor_tool" '
                "--noconfirm "
                "src\enunu_kor_tool\entry\exe_entry.py"
            )
        )
        shutil.rmtree("build")
        os.remove("enunu_kor_tool.spec")

        return

    cli_ui_main()


if __name__ == "__main__":
    main()
