# Copyright (c) 2022 cardroid

import os, re
from glob import glob

import yaml
from tqdm import tqdm
from yaml import loader

from enunu_kor_tool import utils


class FullLoader(loader.Reader, loader.Scanner, loader.Parser, loader.Composer, loader.FullConstructor, loader.Resolver):
    def __init__(self, stream):

        loader.Reader.__init__(self, stream)
        loader.Scanner.__init__(self)
        loader.Parser.__init__(self)
        loader.Composer.__init__(self)
        loader.FullConstructor.__init__(self)
        loader.Resolver.__init__(self)

        for key, reg in loader.Resolver.yaml_implicit_resolvers.items():
            reg_n = []
            for in_reg in reg:
                in_reg = list(in_reg)
                if in_reg[0] == "tag:yaml.org,2002:bool":
                    in_reg[1] = re.compile(
                        r"""^(?:YES|NO|TRUE|FALSE|ON|OFF)$""",
                        re.X,
                    )
                reg_n.append(tuple(in_reg))
            loader.Resolver.yaml_implicit_resolvers[key] = reg_n


class Ustx2Ust_Converter:
    def __init__(self, path, encoding="cp932") -> None:
        try:
            with open(path, mode="r", encoding=encoding) as f:
                self.ustx = yaml.load(f, Loader=FullLoader)
        except UnicodeDecodeError:
            try:
                with open(path, mode="r", encoding="utf-8") as f:
                    self.ustx = yaml.load(f, Loader=FullLoader)
            except UnicodeDecodeError:
                with open(path, mode="r", encoding="utf-8_sig") as f:
                    self.ustx = yaml.load(f, Loader=FullLoader)

    def save_ust(self, path: str, flag: str = "", encoding: str = "utf-8"):
        part_index = 0

        project = self.ustx

        tempo = project.get("bpm")
        if "tempos" in project:
            tempos = project["tempos"]

            for t in tempos:
                if t["position"] == part_index:
                    tempo = t["bpm"]
                    break

        assert tempo != None, "Unable to get tempo value."

        project_body = project["voice_parts"][part_index]

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as ust:
            # Header
            ust.write("[#SETTING]\n")
            ust.write(f"Tempo={tempo}\n")
            ust.write("Tracks=1\n")
            ust.write(f"Charset={encoding}\n")
            ust.write(f"Project={project_body['name']}.ust\n")
            ust.write(f"CacheDir={project_body['name']}.cache\n")
            ust.write("Mode2=True\n")

            # Body
            position = 0
            idx = 0
            for note in project_body["notes"]:
                current_pos = note["position"]
                current_dur = note["duration"]
                if position < current_pos:
                    ust.write(f"[#{str(idx).zfill(4)}]\n")
                    ust.write(f"Length={current_pos - position}\n")
                    ust.write("NoteNum=60\n")
                    ust.write("Lyric=R\n")
                    ust.write(f"Flags={flag}\n")
                    # ust.write("PreUtterance=\n")

                    idx += 1

                ust.write(f"[#{str(idx).zfill(4)}]\n")
                ust.write(f"Length={current_dur}\n")
                ust.write(f"NoteNum={note['tone']}\n")
                ust.write(f"Lyric={note['lyric']}\n")
                ust.write(f"Flags={flag}\n")
                # ust.write("PreUtterance=\n")

                idx += 1
                position = current_pos + current_dur

            # Footer

            ust.write(f"[#TRACKEND]\n")

    def __repr__(self) -> str:
        # result = ""

        # for k, v in self.ustx:
        #     result += f"{k} = {v}"

        return str(self.ustx)

    def __str__(self) -> str:
        return self.__repr__()


def ustx2ust(db_root, out_dir, flag=""):
    target_files = glob(f"{db_root}/**/*.ustx", recursive=True)
    if len(target_files) != 0:
        os.makedirs(out_dir, exist_ok=True)
        print(f"Converting ustx files")
        for path in tqdm(target_files):
            if os.path.basename(path).endswith("-autosave"):
                continue
            converter = Ustx2Ust_Converter(path)
            name, ext = os.path.splitext(os.path.basename(path))
            converter.save_ust(os.path.join(out_dir, f"{name}.ust"), flag)


import shutil
from sys import argv


def ustx2ust_main(path_config_yaml):
    with open(path_config_yaml, "r") as fy:
        config = yaml.load(fy, Loader=yaml.FullLoader)
    db_root = os.path.expanduser(config["stage0"]["db_root"]).strip('"')
    out_dir = os.path.join(db_root, "ust_auto_exp")

    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)

    ustx2ust(db_root, out_dir)


if __name__ == "__main__":
    ustx2ust_main(argv[1].strip('"'))
