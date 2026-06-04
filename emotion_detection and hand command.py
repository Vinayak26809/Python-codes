import cv2
import mediapipe as mp
from deepface import DeepFace

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

def is_hand_raised(hand_landmarks):
    if hand_landmarks:
        # Check vertical distance between wrist (0) and middle fingertip (12)
        wrist_y = hand_landmarks.landmark[0].y
        fingertip_y = hand_landmarks.landmark[12].y
        return fingertip_y < wrist_y  # If fingertip is above wrist
    return False

print("Starting... Raise your open hand to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for natural selfie view
    frame = cv2.flip(frame, 1)

    # Emotion Detection
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        cv2.putText(frame, f'Emotion: {emotion}', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    except:
        pass

    # # Hand Detection
    # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # hand_results = hands.process(rgb)

    # if hand_results.multi_hand_landmarks:
    #     for handLms in hand_results.multi_hand_landmarks:
    #         mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
    #         if is_hand_raised(handLms):
    #             cv2.putText(frame, "Hand Detected - Exiting", (30, 100),
    #                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    #             cap.release()
    #             cv2.destroyAllWindows()
    #             exit()

    # Show the frame
    cv2.imshow('Emotion Detection with Hand Quit', frame)

    # Optional: still allow pressing 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
