import cv2

#동영상 파일 열기
cap = cv2.VideoCapture("vtest.")

#ORB 객체 생성
orb = cv2.ORB_create()

while True:
    #프레임 읽기
    ret, frame = cap.read()
    if not ret:
        break
    
    #그레이스케일로 변환 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #특징점 검출
    keypoints = orb.detect(gray, None)

    #특징점 그리기
    frame = cv2.drawKeypoints(frame, keypoints, None, color=(0,255,0), flags=0)

    #프레임 출력
    cv2.imshow("ORB", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()