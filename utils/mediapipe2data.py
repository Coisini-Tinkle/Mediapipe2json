import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import json
import cv2
import os

def mediaPipe_result2json(image_file, json_file, image_id, num_hands=5):
    """Input an image file ,use mediapipe hand model to detect the keypoints of hand, 
    then convert the result to a standard json file.(Please refer to readme.md)

    Args:
        image_file (str): image file path
        json_file (str): the path to save json file
        image_id (int): the index of image
        num_hands (int, optional): the maximum number of hands in one image. Defaults to 5.
    """
    # Create a HandLandmarker object.
    base_options = python.BaseOptions(model_asset_path='model/hand_landmarker.task')
    options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=num_hands)
    detector = vision.HandLandmarker.create_from_options(options)

    # Load the input image.
    image = mp.Image.create_from_file(image_file)
    w, h = image.width, image.height

    # Detect hands in the input image.
    detection_result = detector.detect(image)

    # Convert detection_result to a dictionary and save as a JSON file.
    detected_num_hand = len(detection_result.handedness)

    # hand_list = []
    keypoints_dict_list = []

    for i in range(detected_num_hand):
        temp = []
        # only x ,y
        for j in range(21):
            temp2 = detection_result.hand_landmarks[i][j]
            temp2 = [temp2.x, temp2.y]
            temp.append(temp2)

        # hand_list.append(temp)
        keypoints_dict_list.append(
            {
                "hand_keypoints": temp,
                "hand_score": detection_result.handedness[i][0].score,
                "hand_type": detection_result.handedness[i][0].category_name
            }
        )

    data = {
        "image_id": image_id,
        "image_info":
            {
                "w": w,
                "h": h
            },
        "keypoints": keypoints_dict_list
    }

    with open(json_file+f"{image_id:0>8d}.json","w") as f:
        json.dump(data,f)
        print("A json file has been created!")


def json_visualize(json_file, image_file, image_output, image_id):
    img = cv2.imread(image_file)
    with open(json_file) as f:
        data = json.load(f)
        width = data['image_info']['w']
        height = data['image_info']['h']
        hands = data['keypoints']
        hands_num = len(hands)
        for hand_order in range(hands_num):
            hand_kpts = hands[hand_order]['hand_keypoints']
            for point_order in range(21):
                point_x = int(hand_kpts[point_order][0]*width)
                point_y = int(hand_kpts[point_order][1]*height)
                cv2.circle(img,(point_x, point_y), 5, (255,0,0), 1)
    # cv2.namedWindow('hhh')
    # cv2.imshow('hhh',img)
    cv2.imwrite(image_output+f'{image_id:0>4d}.png',img)
    # cv2.waitKey(0)
    print('A image file has been created!')


def json_visualize2(json_file,image_file,image_output,image_id):
    """Input a json file and visualize it.

    Args:
        image_file (str): image file path
        json_file (str): json file path
        image_id (int): the index of image
    """
    left_color1 = (255,165,0)
    left_color2 = (255,0,0)
    left_color3 = (128,0,128)
    left_color4 = (0,255,255)
    left_color5 = (255,105,180)
    right_color1 = (0,255,0)
    right_color2 = (0,0,255)
    right_color3 = (204,255,0)
    right_color4 = (139,0,0)
    right_color5 = (0,191,255)
    black_color = (0,0,0)
    white_color = (224,224,224)
    hands_connections = (
        ((0,1),(1,2),(2,3),(3,4)),
        ((0,5),(5,6),(6,7),(7,8)),
        ((0,9),(9,10),(10,11),(11,12)),
        ((0,13),(13,14),(14,15),(15,16)),
        ((0,17),(17,18),(18,19),(19,20))
    )
    left_color = (left_color1,left_color2,left_color3,left_color4,left_color5)
    right_color = (right_color1,right_color2,right_color3,right_color4,right_color5)

    img = cv2.imread(image_file)
    with open(json_file) as f:
        data = json.load(f)
        width = data['image_info']['w']
        height = data['image_info']['h']
        hands = data['keypoints']
        hands_num = len(hands)
        for hand_order in range(hands_num):
            if hands[hand_order]['hand_type'] == 'Right':
                hand_color = right_color
            else:
                hand_color = left_color
            hand_kpts = hands[hand_order]['hand_keypoints']
            for i in range(len(hands_connections)):
                color = hand_color[i]
                for connection in hands_connections[i]:
                    start_index = connection[0]
                    end_index = connection[1]
                    start_point = hand_kpts[start_index]
                    end_point = hand_kpts[end_index]
                    start_x = int(start_point[0]*width)
                    start_y = int(start_point[1]*height)
                    end_x = int(end_point[0]*width)
                    end_y = int(end_point[1]*height)
                    cv2.line(img,(start_x,start_y),(end_x,end_y),color,2)
            for point in hand_kpts:
                cv2.circle(img,(int(point[0]*width),int(point[1]*height)),3,black_color,2)
                cv2.circle(img,(int(point[0]*width),int(point[1]*height)),2,white_color,2)
            point_text = hand_kpts[0]
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,hands[hand_order]['hand_type'],(int(point_text[0]*width),int(point_text[1]*height)),font, 0.5, (0, 255, 255), 1)


    cv2.imwrite(image_output + f'{image_id:0>4d}.png', img)
    print('A image file has been created!')

if __name__ == '__main__':
    # mediaPipe_result2json(image_file=r"image/000007.jpg", json_file=r"outputjson/", image_id=1)
    # json_visualize(json_file=r"outputjson/00000001.json",image_file=r"image/000007.jpg",image_output=r'outputimg/',image_id=1)
    # json_visualize2(json_file=r"outputjson/00000001.json",image_file=r"image/images/0001.png",image_output=r'test_try/',image_id=1)
    pass