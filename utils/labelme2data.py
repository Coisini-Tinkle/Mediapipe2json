import json
import numpy as np

label_index_array=np.array(
    [
        "L_WRIST",
        "L_THUMB_CMC",
        "L_THUMB_MCP",
        "L_THUMB_IP",
        "L_THUMB_TIP",
        "L_INDEX_FINGER_MCP",
        "L_INDEX_FINGER_PIP",
        "L_INDEX_FINGER_DIP",
        "L_INDEX_FINGER_TIP",
        "L_MIDDLE_FINGER_MCP",
        "L_MIDDLE_FINGER_PIP",
        "L_MIDDLE_FINGER_DIP",
        "L_MIDDLE_FINGER_TIP",
        "L_RING_FINGER_MCP",
        "L_RING_FINGER_PIP",
        "L_RING_FINGER_DIP",
        "L_RING_FINGER_TIP",
        "L_PINKY_MCP",
        "L_PINKY_PIP",
        "L_PINKY_DIP",
        "L_PINKY_TIP",
        "R_WRIST",
        "R_THUMB_CMC",
        "R_THUMB_MCP",
        "R_THUMB_IP",
        "R_THUMB_TIP",
        "R_INDEX_FINGER_MCP",
        "R_INDEX_FINGER_PIP",
        "R_INDEX_FINGER_DIP",
        "R_INDEX_FINGER_TIP",
        "R_MIDDLE_FINGER_MCP",
        "R_MIDDLE_FINGER_PIP",
        "R_MIDDLE_FINGER_DIP",
        "R_MIDDLE_FINGER_TIP",
        "R_RING_FINGER_MCP",
        "R_RING_FINGER_PIP",
        "R_RING_FINGER_DIP",
        "R_RING_FINGER_TIP",
        "R_PINKY_MCP",
        "R_PINKY_PIP",
        "R_PINKY_DIP",
        "R_PINKY_TIP"
    ]
)

def labelme2owndata(labelme_json_file,output_json_folder,index:int):
    """This is function is used to convert labelme's result json file to standard json file(refer to readme.md)

    Args:
        labelme_json_file (str): the path of labelme's result json file
        output_json_folder (str): the folder to save output
        index (int): the index of json file ,which is equal to the index of image
    """
    with open(labelme_json_file) as f:
        json_data=json.load(f)

    left_hand_array=np.zeros((21,2))
    right_hand_array=np.zeros((21,2))
    w,h=json_data['imageWidth'],json_data['imageHeight']
    data=json_data['shapes']
    for d in data:#42个点的遍历
        flag=np.where(label_index_array==d['label'])[0][0]
        if flag<=20:
            # print(d['points'][0][0])
            # print(d['points'][0][1])
            left_hand_array[flag][0]=d['points'][0][0]/w
            left_hand_array[flag][1]=d['points'][0][1]/h
        else:
            right_hand_array[flag-21][0]=d['points'][0][0]/w
            right_hand_array[flag-21][1]=d['points'][0][1]/h

    #json格式标准
    json_standard= \
        {
        "image_id":index,
        "image_info":
            {
                "w":w,
                "h":h
            },
        "keypoints": []
    }
    for hand in ["left","right"]:
        if ~(np.any(eval(hand + "_hand_array")))==False:
            json_standard['keypoints'].append(
                {
                    "hand_keypoints": eval(hand + "_hand_array").tolist(),
                    "hand_score":1,
                    "hand_type":hand
                }
            )

    with open(output_json_folder+f"/{index:0>4d}.json","w") as f:
        json.dump(json_standard,f)


    print("A json has been created!")

def json_change_left_right(json_file_folder,index:int):
    """Change the left and right hand information in the specified json file

    Args:
        json_file_folder (str): the folder of json files
        index (int): the index of json file which is equal to the index of image
    """
    index_str = '{:0>4d}'.format(index)
    with open(json_file_folder+f"/{index_str}.json") as f:
        json_data=json.load(f)
    for i in range(len(json_data['keypoints'])):
        if json_data['keypoints'][i]['hand_type']=="left":
            json_data['keypoints'][i]['hand_type']="right"
        elif json_data['keypoints'][i]['hand_type']=="right":
            json_data['keypoints'][i]['hand_type']="left"
    with open(json_file_folder+f"{index_str}.json","w") as ff:
        json.dump(json_data,ff)

def handtype_case_conversion(json_file):
    """Change the handtype in particular json file

    Args:
        json_file (str): the path of json file
    """
    with open(json_file) as f:
        data=json.load(f)
    for key in data['keypoints']:
        if key['hand_type'] in ["Left","left"]:
            key['hand_type']="Right"
        elif key['hand_type'] in ["Right","right"]:
            key['hand_type']="Left"
    with open(json_file,"w") as d:
        json.dump(data,d)

if __name__=='__main__':
    labelme2owndata(
        labelme_json_file=r"F:/Code/Mediapipe2json/labelme/oringinal_labelme_json/2880.json",
        output_json_folder=r"F:/Code/Mediapipe2json/",
        index=2880
    )
    # json_change_left_right(json_file_folder=r"F:\Code\Mediapipe2json\output\labelmejson",index=1596)
    # handtype_case_conversion(json_file=r"C:/Users/ZhangYao/Desktop/0001.json")
    print("This main function is just for debug!")