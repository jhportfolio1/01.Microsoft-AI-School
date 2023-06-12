import cv2
import numpy as np

#칼만 필터 초기화

#칼만 필터 객체 생성(4:상태벡터크기, 2:측정벡터크기)
kalman = cv2.KalmanFilter(4,2)

#측정행렬설정 : 측정벡터를 상대 벡터로 변환 
kalman.measurementMatrix = np.array([[1,0,0,0],
                                     [0,1,0,0]], np.float32)

#전이행렬설정 : 시간에 따른 상태벡터 변화 나타냄 
kalman.transitionMatrix = np.array([[1,0,1,0],
                                    [0,1,0,1],
                                    [0,0,1,0],
                                    [0,0,0,1]], np.float32)

#프로세스 잡음 공분산을 행렬로 설정 : 시스템 불확실성 모델링
kalman.processNoiseCov = np.array([[1,0,0,0],
                                   [0,1,0,0],
                                   [0,0,1,0],
                                   [0,0,0,1]], np.float32) * 0.05

#칼만 필터 추적
#동영상 파일 읽기
cap = cv2.VideoCapture("gorilla.mp4")
print(cap)

#첫 프레임에서 추적할 객체 선택
ret, frame = cap.read()
print(ret, frame)

#SelectObject 창 만들어서 객체 선택할 수 있게 만듦 
bbox_info = cv2.selectROI("select Object", frame, False, False)
print("box info:", bbox_info)

#객체 추적을 위한 초기 추정 위치 설정
kalman.statePre = np.array([[bbox_info[0]], #객체 X 좌표
                            [bbox_info[1]], #객체 Y 좌표
                            [0], [0]], #나머지 두 요소 초기화 : 객체속도 0으로 추정
                            np.float32)


#칼만 필터 추적
while True:
    #프레임 읽기
    ret, frame = cap.read()
    if not ret:
        break

    #칼만 필터 사용하여 객체 위치 추정
    kalman.correct( #측정값 사용해서 칼만 필터 예측 보정하는 과정
        np.array([  #측정값 
            [np.float32(bbox_info[0] + bbox_info[2] /2)],
            [np.float32(bbox_info[1] + bbox_info[3] /2)]
        ])
    )
    kalman.predict()    #칼만필터 예측단계 수행 : 객체 위치 예측


    #칼만 필터로 추정된 객체 위치 
    predicted_bbox = tuple(map(int, kalman.statePost[:2,0]))    

    #추정된 객체 위치를 사각형으로 표시
    cv2.rectangle(frame, 
                  (predicted_bbox[0] - bbox_info[2] // 2,
                   predicted_bbox[1] - bbox_info[3] //2),
                  (predicted_bbox[0] - bbox_info[2] // 2,
                   predicted_bbox[1] - bbox_info[3] //2),
                  (0,255,0),2)
    
    #프레임 출력
    cv2.imshow("Kalman Filter Tracking", frame)

    #'q'키를 누르면 종료
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

#자원해제
cap.release()
cv2.destroyAllWindows()