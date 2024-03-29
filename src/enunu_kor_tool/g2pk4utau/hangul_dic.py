# 해당 자소 및 음소는 공식적인 문법이 아닐 수 있습니다. (보기에 더 좋게 설계됨)
# These consonants and phonemes may not be official grammar. (Designed to look better)

from typing import List, Tuple
import regex


## For Verbose
from enunu_kor_tool.g2pk4utau.enum_set import VerboseMode

differ = None


Consonants_LIST = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ", "ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ"]
Vowels_LIST = ["ㅏ", "ㅑ", "ㅓ", "ㅕ", "ㅗ", "ㅛ", "ㅜ", "ㅠ", "ㅡ", "ㅣ", "ㅐ", "ㅒ", "ㅔ", "ㅖ", "ㅘ", "ㅙ", "ㅚ", "ㅝ", "ㅞ", "ㅟ", "ㅢ"]

# \-=+,#/\?:^$.@*"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`'…》

Special_Character_Filter = [
    # " ",
    "\-",
    "=",
    "+",
    ",",
    "#",
    "/",
    "\?",
    ":",
    "^",
    "$",
    ".",
    "@",
    "*",
    '"',
    "※",
    "~",
    "&",
    "%",
    "ㆍ",
    "!",
    "』",
    "\\",
    "‘",
    "|",
    "\(",
    "\)",
    "\[",
    "\]",
    "\<",
    "\>",
    "`",
    "'",
    "…",
    "》",
]


def __get_norm_Special_Character_Filter():
    global Special_Character_Filter
    return [c[-1] if len(c) > 1 else c for c in Special_Character_Filter]


Special_Character_Filter_joined = "".join(Special_Character_Filter)
Special_Character_Filter_norm = __get_norm_Special_Character_Filter()


def clear_Special_Character(text: str) -> str:
    return regex.sub("[" + "".join(Special_Character_Filter) + "]", "", text)


def replace2pre_phn(origin_text: str, verbose: VerboseMode = VerboseMode.NONE) -> Tuple[str, List[Tuple[int, int, str]]]:
    verbose__ = verbose.is_flag(verbose.PREPHN)

    pre_phns = []
    result_str = []

    fter = "[" + "".join(Special_Character_Filter) + "]"

    word_idx = 0
    for char in origin_text:
        if regex.match(fter, char) != None:
            pre_phns.append((len(result_str), word_idx, char))  # 현재 위치, 단어 단위 위치, 문자
        else:
            if char == " ":
                word_idx += 1
            result_str.append(char)

    if verbose__:
        temp_dict = {}
        for idx, word_idx, phn in pre_phns:
            if (phn_space := temp_dict.get(phn)) == None:
                phn_space = []
                temp_dict[phn] = phn_space
            phn_space.append(idx)

        for key, list in temp_dict.items():
            print(f"[\033[1;32m{key}\033[0m] ({len(list)}) : {list}")

        print(f"\033[1;33mLIST\033[0m: {pre_phns}")

    return "".join(result_str), pre_phns


def replace2phn(dic: dict, jamo_text: str, verbose: VerboseMode = VerboseMode.NONE):
    verbose__ = verbose.is_flag(verbose.G2P4UTAU)

    if verbose__:
        before_text = jamo_text
        verbose_result = [(jamo_text, "", "init")]

    for key in dic.keys():
        for pattern, repl in dic[key]:
            jamo_text = regex.sub(pattern, repl, jamo_text)

            if verbose__ and not before_text == jamo_text:
                global differ

                if differ == None:
                    from difflib import Differ

                    differ = Differ()

                highlight = False
                lst = []
                for diff in differ.compare(before_text, jamo_text):
                    if diff[0] == " ":
                        if highlight:
                            lst.append("\033[0m")
                            highlight = False
                        lst.append(diff[2])
                    elif diff[0] == "+":
                        if not highlight:
                            lst.append("\033[1;91m")
                            highlight = True
                        lst.append(diff[2])

                if highlight:
                    lst.append("\033[0m")

                verbose_result.append(("".join(lst), f"{pattern} \033[1;33m->\033[0m {repl}", key))

                before_text = jamo_text

    if verbose__ and len(verbose_result) > 1:
        print("\033[1;96m[g2p4utau Processing]\033[0m")
        for line in verbose_result:
            print("->", line[0], f"        [\033[1;92m{line[2]}\033[0m] ({line[1]})")

    return jamo_text[:-1]


def get_phn_dictionary(labeling_mode: bool = True):

    ##### 전처리 #####
    pre_regex_list = [
        # 종성 'ㄹ'과 초성 'ㄹ'이 만날 경우 둘 다 'l'로 발음
        (r"ㄹ(\s*)ㄹ", r"L\1 l "),
        # 모음 뒤, 'ㅎ' 앞의 'ㄹ'
        (r"ㄹ(\s*)ㅎ", r"RR\1 "),
        # 모음과 모음 사이 'ㄹ'
        (r"(?<=[ㅏ-ㅣ]\s*)ㄹ(?=\s*[ㅏ-ㅣ])", r"r "),
        # 'ㄹ'뒤의 'ㅅ'은 'ㅆ'으로 발음
        # (r"(ㄹ\s*)ㅅ", r"\1ss "),
    ]

    # if labeling_mode:
    #     pre_regex_list.append((r"(?<=ㄱ)(\s*)ㅆ", r"\1K ss "))
    #     pre_regex_list.append((r"(?<=ㅂ)(\s*)ㅆ", r"\1P ss "))
    # else:
    #     pre_regex_list.append((r"(?<=ㄱ\s*)ㅆ", r"Kss "))
    #     pre_regex_list.append((r"(?<=ㅂ\s*)ㅆ", r"Pss "))

    ########
    # 초성 #
    ########
    lead_consonants_process_regex_list = [
        (r"ㄱ(?=\s*([ㅏ-ㅣ]))", r"g "),
        (r"ㄴ(?=\s*([ㅏ-ㅣ]))", r"n "),
        (r"ㄷ(?=\s*([ㅏ-ㅣ]))", r"d "),
        (r"ㄹ(?=\s*([ㅏ-ㅣ]))", r"r "),
        (r"ㅁ(?=\s*([ㅏ-ㅣ]))", r"m "),
        (r"ㅂ(?=\s*([ㅏ-ㅣ]))", r"b "),
        (r"ㅅ(?=\s*([ㅏ-ㅣ]))", r"s "),
        # 초성에서 소리 없음
        (r"ㅇ(?=\s*([ㅏ-ㅣ]))", r""),
        (r"ㅈ(?=\s*([ㅏ-ㅣ]))", r"j "),
        (r"ㅊ(?=\s*([ㅏ-ㅣ]))", r"ch "),
        (r"ㅋ(?=\s*([ㅏ-ㅣ]))", r"k "),
        (r"ㅌ(?=\s*([ㅏ-ㅣ]))", r"t "),
        (r"ㅍ(?=\s*([ㅏ-ㅣ]))", r"p "),
        (r"ㅎ(?=\s*([ㅏ-ㅣ]))", r"h "),
        # UTAU에서 통용되는 표기는 'gg'이지만 외국 사용자들의 접근성을 위해 'kk'로 표기
        (r"ㄲ(?=\s*([ㅏ-ㅣ]))", r"kk "),
        # UTAU에서 통용되는 표기는 'dd'이지만 외국 사용자들의 접근성을 위해 'tt'로 표기
        (r"ㄸ(?=\s*([ㅏ-ㅣ]))", r"tt "),
        # UTAU에서 통용되는 표기는 'bb'이지만 외국 사용자들의 접근성을 위해 'pp'로 표기
        (r"ㅃ(?=\s*([ㅏ-ㅣ]))", r"pp "),
        (r"ㅆ(?=\s*([ㅏ-ㅣ]))", r"ss "),
        (r"ㅉ(?=\s*([ㅏ-ㅣ]))", r"jj "),
    ]

    ########
    # 중성 #
    ########
    vowels_process_regex_list = [
        (r"ㅏ", r"a "),
        (r"ㅓ", r"eo "),
        (r"ㅗ", r"o "),
        (r"ㅜ", r"u "),
        (r"ㅡ", r"eu "),
        (r"ㅣ", r"i "),
        (r"ㅔ", r"e "),
        (r"ㅐ", r"e "),
    ]

    if labeling_mode:
        vowels_process_regex_list.append((r"ㅑ", r"y a "))
        vowels_process_regex_list.append((r"ㅕ", r"y eo "))
        vowels_process_regex_list.append((r"ㅛ", r"y o "))
        vowels_process_regex_list.append((r"ㅠ", r"y u "))
        vowels_process_regex_list.append((r"ㅖ", r"y e "))
        vowels_process_regex_list.append((r"ㅒ", r"y e "))
        vowels_process_regex_list.append((r"ㅘ", r"w a "))
        vowels_process_regex_list.append((r"ㅚ", r"w e "))
        vowels_process_regex_list.append((r"ㅞ", r"w e "))
        vowels_process_regex_list.append((r"ㅙ", r"w e "))
        # UTAU에서는 사용되지 않지만 상황에 따라 'i'발음을 원순모음화 시 발생
        vowels_process_regex_list.append((r"ㅟ", r"w i "))
        # UTAU에서는 사용되지 않지만 상황에 따라 'e'발음을 원순모음화 시 발생
        vowels_process_regex_list.append((r"ㅝ", r"w eo "))
        # 라벨링을 할 때는 'eu i'로 구분
        vowels_process_regex_list.append((r"ㅢ", r"eu i "))
    else:
        vowels_process_regex_list.append((r"ㅑ", r"ya "))
        vowels_process_regex_list.append((r"ㅕ", r"yeo "))
        vowels_process_regex_list.append((r"ㅛ", r"yo "))
        vowels_process_regex_list.append((r"ㅠ", r"yu "))
        vowels_process_regex_list.append((r"ㅖ", r"ye "))
        vowels_process_regex_list.append((r"ㅒ", r"ye "))
        vowels_process_regex_list.append((r"ㅘ", r"wa "))
        vowels_process_regex_list.append((r"ㅚ", r"we "))
        vowels_process_regex_list.append((r"ㅞ", r"we "))
        vowels_process_regex_list.append((r"ㅙ", r"we "))
        # UTAU에서는 사용되지 않지만 상황에 따라 'i'발음을 원순모음화 시 발생
        vowels_process_regex_list.append((r"ㅟ", r"wi "))
        # UTAU에서는 사용되지 않지만 상황에 따라 'e'발음을 원순모음화 시 발생
        vowels_process_regex_list.append((r"ㅝ", r"weo "))
        vowels_process_regex_list.append((r"ㅢ", r"eui "))

    ########
    # 종성 #
    ########
    tail_consonants_process_regex_list = [
        # 음절 끝소리 규칙
        (r"ㄲ", r"ㄱ"),
        (r"ㅋ", r"ㄱ"),
        (r"ㅌ", r"ㄷ"),
        (r"ㅅ", r"ㄷ"),
        (r"ㅆ", r"ㄷ"),
        (r"ㅈ", r"ㄷ"),
        (r"ㅊ", r"ㄷ"),
        (r"ㅎ", r"ㄷ"),
        (r"ㅍ", r"ㅂ"),
        # 악, 앜, 앆... 등에 쓰이는 받침
        (r"ㄱ", r"K "),
        # 앋, 앗, 앚, 앛, 앝, 앟, 았 ... 등에 쓰이는 받침
        (r"ㄷ", r"T "),
        # 압, 앞 ... 등에 쓰이는 받침
        (r"ㅂ", r"P "),
        # # 안 ... 등에 쓰이는 받침
        (r"ㄴ", r"N "),
        # # 알 ... 등에 쓰이는 받침
        (r"ㄹ", r"L "),
        # # 암 ... 등에 쓰이는 받침
        (r"ㅁ", r"M "),
        # 앙 ... 등에 쓰이는 받침 (유성 받침, 초성에서 발음이 없음)
        (r"ㅇ", r"NG "),
    ]

    ##### 후처리 #####
    post_regex_list = [
        # 쌍자음인 'ss' 앞 받침 'T' 제거
        (r"T(\s*)ss", r"\1ss"),
    ]

    result_dic = {
        "Pre": pre_regex_list,
        "Lead Consonants": lead_consonants_process_regex_list,
        "Vowels": vowels_process_regex_list,
        "Tail Consonants": tail_consonants_process_regex_list,
        "Post": post_regex_list,
    }

    return result_dic
