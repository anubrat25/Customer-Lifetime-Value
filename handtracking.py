import cv2
import mediapipe as mdp
cap = cv2.VideoCapture(0)
hand_det = mdp.solutions.hands.Hands()
drawing_utils = mdp.solutions.drawing_utils
indexy = 0
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    op = hand_det.process(rgb_frame)
    hands = op.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark           
    cv2.imshow('Virtual Mouse', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
cap.release()
cap.destroyAllWindows()