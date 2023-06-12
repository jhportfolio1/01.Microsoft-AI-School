import cv2

#추적할 객체의 위치정보 저장 변수
tracking_window = None

#추적할 객체의 히스토그램 저장할 변수
roi_hist = None

#평균 이동 알고리즘 수렴 기준 설정
#EPS : 수렴조건 - 이전위치와 현재위치의 이동 벡터크기 최소 변경값
#COUNT : 수렴조건 - 최대반복횟수 (10:10번반복후 수렴안하면 알고리즘 정지 / 1:수렴조건판단최소값)
trem_cri = (cv2.TERM_CRITERIA_EPS | cv2.TermCriteria_COUNT, 10, 1)  


#동영상 파일 열기
cap = cv2.VideoCapture("slow_traffic_small.mp4")

#첫 프레임에서 추적할 객체 선택
ret, frame = cap.read()
x, y, w, h = cv2.selectROI("selectObject", frame, False, False)
#print("선택한 박스 좌표 : ", x, y, w, h)

#선택한 좌표와 너비 사용해 해당 객체 추출하여 roi변수에 저장
roi = frame[y:y+h, x:x+w]

# 이미지를 HSV로 변환 : 색상(Hue), 채도(Saturation), 명도(Value)로 이루어짐 
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# 이미지 채널에서 히스토그램 계산에서 roi_hist에 저장
roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0,100])

# 히스토그램을 0-255 사이 범위로 정규화하여 값 조정
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

#추적할 객체의 초기 윈도우 좌표 및 크기 설정(이후 객체 위치 업데이트에 사용)
track_window = (x, y, w, h)

#결과확인
#cv2.imshow('roi test', roi)
#cv2.waitKey(0)

#평균 이동 추적(Mean Shift Tracking)
while True:
    #프레임 읽기
    ret, frame = cap.read()
    if not ret:
        break

    #추적할 객체의 히스토그램 역투영 계산
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0,100], 1)

    # 평균 이동 알고리즘 통해 객체 위치 추정
    ret, track_window = cv2.meanShift(dst, track_window, trem_cri)

    # 추적결과를 사각형으로 표시
    x, y, w, h = track_window
    print(x, y, w, h)
    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

    # 프레임 출력 
    cv2.imshow("Mean Shift Tracking", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# 자원해제
cap.release()
cv2.destroyAllWindows()
