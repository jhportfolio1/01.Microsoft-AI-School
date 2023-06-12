import cv2

# 동영상 파일 열기
cap = cv2.VideoCapture("gorilla.mp4")

# Shi-Tomasi 코너 검출기 파라미터 설정
feature_params = dict(maxCorners=100,  # 검출할 최대 코너 수
                      qualityLevel=0.3,  # 코너로 간주할 최소 품질
                      minDistance=7,  # 검출된 코너 사이의 최소 거리
                      blockSize=7)  # 코너 검출을 위한 이웃 픽셀 블록 크기

# Lucas-Kanade 광학 흐름 파라미터 설정
lk_params = dict(winSize=(15, 15),  # 특징점 주변 윈도우 크기
                 maxLevel=2,  # 피라미드 레벨 수
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))  # 알고리즘 중지 기준


# 첫 프레임 읽어서 회색조 변환
ret, prev_frame = cap.read()  # 프레임 읽기 성공 여부를 나타내는 변수
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)  # 이전 프레임을 그레이스케일로 변환

# 초기 추적 지점
prev_corners = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)  # 추적할 특징점
prev_points = prev_corners.squeeze()  # 검출된 특징점의 좌표 지정

# 추적 결과 표시용 색상 설정
color = (0, 255, 0)


# 추적기 실행
while True:
    # 다음 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        break

    # 현재 회색조 프레임 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Lucas-Kanade 광학 흐름 계산
    next_points, status, _ = cv2.calcOpticalFlowPyrLK(
        prev_gray, gray, prev_points, None, **lk_params)

    # 추적 결과 표시 (특징점 순회)
    for i, (prev_point, next_point) in enumerate(zip(prev_points, next_points)):
        x1, y1 = prev_point.astype(int)
        x2, y2 = next_point.astype(int)

        cv2.line( #이전-현재 특징점 선으로 연결
                frame, 
                (x1, y1), #이전 특징점 정수형 좌표
                (x2, y2), #현재 특징점 정수형 좌표
                color, 2)
        cv2.circle( #특징점에 원 그리기 
                frame, 
                (x2, y2), 
                3, 
                color, 
                -1)  # 반지름 3, 원 내부 -1

    # 프레임 출력
    cv2.imshow("Feature-based Tracking", frame)

    # 다음 프레임을 위해 변수 업데이트
    prev_gray = gray.copy()  # 이전 프레임의 흑백 이미지 나타냄
    prev_points = next_points  # 이전 프레임 흑백 이미지 복사해서 좌표 업데이트

    # 'q' 키 누르면 종료
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
