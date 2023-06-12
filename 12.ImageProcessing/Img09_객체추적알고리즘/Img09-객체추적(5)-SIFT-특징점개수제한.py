
import cv2

#동영상 파일 열기
cap = cv2.VideoCapture("gorilla.mp4")

# SIFT 객체 생성
sift = cv2.SIFT_create(contrastThreshold=0.02)

# 특징점 개수 제한 설정
max_keypoints = 100  #원하는 최대 특징점 개수

while True:
    #프레임 읽기
    ret, frame = cap.read()
    if not ret:
        break
    
    #그레이스케일 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #특징점 검출
    keypoints, descriptors = sift.detectAndCompute(gray, None)

    #특징점 개수 제한 
    if len(keypoints) > max_keypoints:
        keypoints = sorted(keypoints, key=lambda x: -x.response)[:max_keypoints]

    #특징점 그리기
    frame = cv2.drawKeypoints(frame, keypoints, None, 
                              flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    #프레임 출력
    cv2.imshow("SIFT", frame)

    #'q'키 누르면 종료
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# 자원해제
cap.release()
cv2.destroyAllWindows()