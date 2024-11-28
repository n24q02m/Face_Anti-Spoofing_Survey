import cv2
import pandas as pd

def get_video_properties(video_path):
    """
    Hàm lấy thông tin kỹ thuật của video.
    Trả về Series pandas chứa width, height, fps, frame_count, duration.
    """
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps else 0
        cap.release()
        return pd.Series({
            'width': width,
            'height': height,
            'fps': fps,
            'frame_count': frame_count,
            'duration': duration
        })
    else:
        return pd.Series({
            'width': None,
            'height': None,
            'fps': None,
            'frame_count': None,
            'duration': None
        })

def get_frames(video_path):
    """
    Hàm lấy khung hình đầu tiên và giữa của video.
    Trả về tuple (frame1, frame2).
    """
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # Lấy khung hình đầu tiên
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret1, frame1 = cap.read()
        # Lấy khung hình giữa
        cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames // 2)
        ret2, frame2 = cap.read()
        cap.release()
        return (frame1 if ret1 else None, frame2 if ret2 else None)
    else:
        return (None, None)

def calculate_motion(video_path):
    """
    Hàm tính toán mức độ chuyển động trong video.
    Trả về giá trị trung bình của sự khác biệt giữa các khung hình.
    """
    cap = cv2.VideoCapture(video_path)
    frame_diffs = []
    if cap.isOpened():
        ret, prev_frame = cap.read()
        if not ret:
            cap.release()
            return 0
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        while True:
            ret, curr_frame = cap.read()
            if not ret:
                break
            curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
            frame_diff = cv2.absdiff(curr_gray, prev_gray)
            mean_diff = frame_diff.mean()
            frame_diffs.append(mean_diff)
            prev_gray = curr_gray
        cap.release()
        avg_motion = sum(frame_diffs) / len(frame_diffs) if frame_diffs else 0
        return avg_motion
    else:
        return 0