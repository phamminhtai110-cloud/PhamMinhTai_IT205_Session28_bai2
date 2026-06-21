from abc import ABC, abstractmethod


class BaseLesson(ABC):

    platform_name = "Rikkei Academy LMS"
    base_completion_points = 10

    def __init__(self, lesson_code, title):
        self.__duration_minutes = 0
        self.lesson_code = lesson_code
        self.title = title.strip().upper()

    @property
    def duration_minutes(self):
        return self.__duration_minutes

    def add_duration(self, minutes):
        if minutes <= 0:
            raise ValueError("Invalid duration")
        self.__duration_minutes += minutes

    @abstractmethod
    def calculate_completion_score(self):
        pass

    @abstractmethod
    def update_content(self, new_data):
        pass

    def __add__(self, other):
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes + other.duration_minutes

    def __lt__(self, other):
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes < other.duration_minutes

    @staticmethod
    def validate_lesson_code(code):
        return isinstance(code, str) and code.startswith("LMS") and len(code) == 10

    @classmethod
    def update_base_points(cls, value):
        cls.base_completion_points = value


class VideoLesson(BaseLesson):

    def __init__(self, lesson_code, title, video_quality):
        super().__init__(lesson_code, title)
        self.video_quality = video_quality
        self.view_count = 0

    def calculate_completion_score(self):
        return self.base_completion_points + self.duration_minutes * 0.5

    def update_content(self, new_data):
        self.video_quality = new_data

    def play_video(self):
        self.view_count += 1


class CodingChallenge(BaseLesson):

    def __init__(self, lesson_code, title, number_of_testcases, difficulty_multiplier):
        super().__init__(lesson_code, title)
        self.number_of_testcases = number_of_testcases
        self.difficulty_multiplier = difficulty_multiplier

    def calculate_completion_score(self):
        return (
            self.base_completion_points *
            self.number_of_testcases *
            self.difficulty_multiplier
        )

    def update_content(self, new_data):
        if new_data <= 0:
            raise ValueError("Invalid testcase")
        self.number_of_testcases = new_data


class HybridAssessment(VideoLesson, CodingChallenge):

    def __init__(
        self,
        lesson_code,
        title,
        video_quality,
        number_of_testcases,
        difficulty_multiplier
    ):
        VideoLesson.__init__(
            self,
            lesson_code,
            title,
            video_quality
        )

        self.number_of_testcases = number_of_testcases
        self.difficulty_multiplier = difficulty_multiplier

    def calculate_completion_score(self):

        video_score = (
            self.base_completion_points
            +
            self.duration_minutes * 0.5
        )

        code_score = (
            self.number_of_testcases
            *
            self.difficulty_multiplier
        )

        return video_score + code_score


class AWSS3StorageService:

    def upload_lesson(self, lesson):
        print(
            "AWS upload:",
            lesson.lesson_code
        )


class GoogleCloudStorageService:

    def upload_lesson(self, lesson):
        print(
            "Google upload:",
            lesson.lesson_code
        )


def sync_to_cloud(service, lesson):

    try:
        service.upload_lesson(lesson)

    except AttributeError:
        print("Invalid cloud service")


lessons = []
current_lesson = None


def menu():

    global current_lesson

    while True:

        print("""
===== RIKKEI LMS =====
1. Create lesson
2. Show lesson MRO
3. Update lesson
4. Calculate score
5. Compare lesson
6. Upload cloud
7. Exit
""")

        choice = input("Choice: ")


        if choice == "1":

            print("1.Video 2.Code 3.Hybrid")
            t = input("Type: ")

            code = input("Code: ")
            title = input("Title: ")


            if not BaseLesson.validate_lesson_code(code):
                print("Invalid code")
                continue


            if t == "1":

                obj = VideoLesson(
                    code,
                    title,
                    "1080p"
                )

            elif t == "2":

                obj = CodingChallenge(
                    code,
                    title,
                    5,
                    1.5
                )

            else:

                obj = HybridAssessment(
                    code,
                    title,
                    "1080p",
                    5,
                    1.5
                )


            obj.add_duration(45)

            lessons.append(obj)
            current_lesson = obj

            print("Created")


        elif choice == "2":

            if current_lesson:

                print(
                    type(current_lesson).__name__
                )

                print(
                    type(current_lesson).mro()
                )


        elif choice == "3":

            if current_lesson:

                if hasattr(
                    current_lesson,
                    "play_video"
                ):
                    current_lesson.play_video()

                print("Updated")


        elif choice == "4":

            if current_lesson:
                print(
                    current_lesson.calculate_completion_score()
                )


        elif choice == "5":

            if len(lessons) > 1:

                other = lessons[1]

                print(
                    current_lesson + other
                )

                print(
                    current_lesson < other
                )


        elif choice == "6":

            if current_lesson:

                service = AWSS3StorageService()

                sync_to_cloud(
                    service,
                    current_lesson
                )


        elif choice == "7":
            break


menu()