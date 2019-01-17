import random

from app.model import Video


if __name__ == "__main__":
    with open("etc/videos.txt", "r") as file:
        for line in file.readlines():
            line = line.replace("\\n", "")
            new_video = Video(name="Video", url=line, status="active",
                              count_success=0, count_fail=0,
                              first_time=random.randint(0, 40),
                              second_time=random.randint(0, 60))
            new_video.save_to_db()
