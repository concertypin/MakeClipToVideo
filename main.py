from __future__ import unicode_literals
from typing import List
import os


def MergeVideos(VideoList: List[str], path: str):  # 그냥 리스트로 파일 path 받으면 합치는 무언가
    VideoListPath = os.environ["temp"] + "\\list.txt"
    ListString = ""

    for i in range(len(VideoList)):  # 파일명
        try:
            VideoList[i].index("Transition")
        except:
            FileName = VideoList[i].split("\\")[-1]
            DirName = "\\".join(VideoList[i].split("\\")[:-1])
            # ffmpeg 전처리
            #cmd='ffmpeg -i \"{}\" -n -video_track_timescale 15360 -vcodec copy -acodec copy \"{}\"'
            #cmd = "ffmpeg -use_wallclock_as_timestamps 1 -correct_ts_overflow 0 -n -i \"{}\" \"{}\""
            cmd="ffmpeg -n -i \"{}\" \"{}\" "
            cmd = cmd.format(VideoList[i], DirName + "\\encoded\\" + FileName+".ts")
            with open("C:\\Users\\rophini\\PycharmProjects\\MakeClipToVideo\\log",mode="a",encoding="utf-8") as f:
                f.write("ffmpeg 전처리 cmd\n"+cmd+"\n\n")
            os.system(cmd)
            VideoList[i]=DirName + "\\encoded\\" + FileName+".ts"
        else:
            pass

    # ffmpeg 합치기
    for i in range(len(VideoList)):
        ListString += f'file \'{VideoList[i]}\'\n'
    f = open(VideoListPath, "w")
    f.write(ListString)
    f.close()

    #cmd = f"ffmpeg -fflags +igndts -y -copytb 1 -use_wallclock_as_timestamps 1 -f concat -safe 0 -i \"{VideoListPath}\" -c copy \"{path}\""
    cmd=["copy /b encoded/* tmp.ts",f"ffmpeg -y -i tmp.ts \"{path}\"","del tmp.ts"]
    for i in cmd:
        os.system(i)


def MakeHotclip(CacheDir: str = "clips", VideoCount: int = 10, MaxVideo: int = 10, TwitchID: str = "snow_h",
                path: str = "res.mp4"):
    """
    :param CacheDir:캐시용 폴더를 잡습니다.
    :param VideoCount: 이 조회수를 넘어야지만 다운받아요.
    :param MaxVideo: 최대 클립 수에요.
    :param TwitchID: 트위치 아이디에요.
    :param path: 결과적으로 나올 경로에요.
    :return:
    """

    debug = False
    FastDebug = False
    # 존재하는 디렉터리는 사용 불가능 처리
    try:
        os.listdir(CacheDir)
    except FileNotFoundError:
        pass
    else:
        if (os.listdir(CacheDir) != [] or os.listdir(CacheDir) == ["encoded"]):  # encoded 또는 빈 폴더라면
            if (not ("debug" in os.listdir(CacheDir))):  # debug란 파일이 있으면 디버그 모드, 캐시를 이용함
                print(f"CacheDir(\"{CacheDir}\") 은 존재하면 안 되요!")
                return -1972
            else:
                f = open("clips\\debug", "r")
                debug = True
                if (f.read() == "FastDebug"):
                    FastDebug = True

    # 디렉터리 정리
    BetweenVideos = os.path.abspath("Transition.ts")
    path = os.path.abspath(path)
    if (debug != True):
        try:
            os.mkdir(CacheDir)
        except FileExistsError:
            pass
    os.chdir(CacheDir)

    # 클립 다운
    cmd = f"youtube-dl --max-downloads {MaxVideo} --match-filter \"view_count >= {VideoCount} & duration <= 60\" \"https://www.twitch.tv/{TwitchID}/videos?filter=clips&range=all\""
    if (debug == False):
        os.system(cmd)

    # 병합 전처리
    VideoList = []
    FileList = os.listdir("./")
    try:
        FileList.remove("encoded")
    except:
        os.mkdir("encoded")
    try:
        FileList.remove("debug")
    except:
        pass

    for i in FileList:
        VideoList.append(os.path.abspath(i))
        VideoList.append(BetweenVideos)

    if (debug == True & FastDebug == True):
        VideoList = VideoList[:2]
    else:
        VideoList = VideoList[:len(VideoList) - 1]

    # 병합
    MergeVideos(VideoList, path)

os.system('chcp 65001')
MakeHotclip()
