"""
뭐 써야 하지
"""
from __future__ import unicode_literals

import os

from moviepy.editor import VideoFileClip, concatenate_videoclips

"""
def ClipDownload(url, FormatCode=None, path=None):  # 그냥 유튭 클립 다운로드하는 무언가
    import os

    if (FormatCode is None):
        if (path is not None):
            os.system(f"youtube-dl \"{url}\" -o \"{path}\"")
        else:
            os.system(f"youtube-dl \"{url}\"")
    else:
        if (path is not None):
            os.system(f"youtube-dl \"{url}\" -o \"{path}\" -f {FormatCode}")
        else:
            os.system(f"youtube-dl \"{url}\" -f {FormatCode}")
"""


def MergeVideos(VideoList, path):  # 그냥 리스트로 파일 path 받으면 합치는 무언가
    try:
        UseableList = []
        for i in VideoList:
            UseableList.append(VideoFileClip(i))
        final_clip = concatenate_videoclips(UseableList) #todo 뭔가 트렌지션 부분이 깨지는 오류
        final_clip.write_videofile(path)
    except:
        #코덱 에러
        UseableList = []
        cmd="ffmpeg -n -i \"{}\" \"{}\""
        for i in VideoList:
            os.system(cmd.format(i,i+".mp4"))
            UseableList.append(VideoFileClip(i+".mp4"))
        final_clip = concatenate_videoclips(UseableList)
        final_clip.write_videofile(path)


def MakeHotclip(CacheDir="clips", VideoCount=10, MaxVideo=10,TwitchID="snow_h",path="res.mp4"):
    """
    :param CacheDir:캐시용 폴더를 잡습니다.
    :param VideoCount: 이 조회수를 넘어야지만 다운받아요.
    :param MaxVideo: 최대 클립 수에요.
    :param TwitchID: 트위치 아이디에요.
    :param path: 결과적으로 나올 경로에요.
    :return:
    """

    debug=False
    # 존재하는 디렉터리는 사용 불가능 처리
    try:
        os.listdir(CacheDir)
    except FileNotFoundError:
        pass
    else:
        if(os.listdir(CacheDir)!=[]):
            if (not ("debug" in os.listdir(CacheDir))):  # debug란 파일이 있으면 디버그 모드, 캐시를 이용함
                print(f"CacheDir(\"{CacheDir}\") 은 존재하면 안 되요!")
                return -1972
            else:
                debug=True

    # 디렉터리 정리
    BetweenVideos = os.path.abspath("Transition.mp4")
    path=os.path.abspath(path)
    if(debug!=True):
        try:
            os.mkdir(CacheDir)
        except FileExistsError:
            pass
    os.chdir(CacheDir)

    # 클립 다운
    cmd = f"youtube-dl --max-downloads {MaxVideo} --match-filter \"view_count >= {VideoCount} & duration <= 60\" \"https://www.twitch.tv/{TwitchID}/videos?filter=clips&range=all\""
    if(debug==False):
        os.system(cmd)

    # 병합 전처리
    VideoList = []
    FileList = os.listdir("./")
    for i in FileList:
        VideoList.append(i)
        VideoList.append(BetweenVideos)

    if(debug==True):
        VideoList = VideoList[:2]

    # 병합
    MergeVideos(VideoList,path)
MakeHotclip()