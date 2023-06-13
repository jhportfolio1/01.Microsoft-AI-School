import cv2

#이미지 불러오기
img1 = cv2.imread('dubu1.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('dubu2.png', cv2.IMREAD_GRAYSCALE)

#특징점 검출기 생성
orb = cv2.ORB_create()

#특징점 검출 및 디스크립터 계산
keypoints1, descriptors1 = orb.detectAndCompute(img1, None) 
keypoints2, descriptors2 = orb.detectAndCompute(img2, None)

#매칭기 생성
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

#특징점 매칭
matches = bf.match(descriptors1, descriptors2)

#매칭결과 그리기
result = cv2.drawMatches(img1, keypoints1, 
                         img2, keypoints2,
                         matches[:10], None,
                         flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

#매칭결과 출력
cv2.imshow("Matches", result)

#매칭퍼센트 계산
num_matches = len(matches)
mun_good_matches = sum(1 for m in matches if m.distance < 50)   #거리 임계값 적적하게 설정
matching_percent = (num_good_matches / num_matches) * 100

#매핑퍼센트 출력
print("매칭 퍼센트 : %.2f%%" % matching_percent)

cv2.waitkey(0)
cv2.destroyAllWindows()