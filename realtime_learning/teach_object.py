import cv2
import os
import time

def teach_object(object_name: str, save_dir: str = "data/custom_dataset", cam_index: int = 0):
    """
    使用摄像头拍摄图像并保存为特定类别的训练样本。

    参数:
        object_name (str): 物体名称，如“桌子”
        save_dir (str): 保存数据的根目录
        cam_index (int): 摄像头索引，默认0
    """

    # 创建目标目录
    object_dir = os.path.join(save_dir, object_name)
    os.makedirs(object_dir, exist_ok=True)

    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print("❌ 摄像头无法打开")
        return

    print(f"📷 开始捕捉 '{object_name}'，按 't' 保存当前帧，按 'q' 退出")
    img_count = len(os.listdir(object_dir))

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ 读取摄像头画面失败")
            break

        # 显示窗口
        cv2.imshow(f"Teaching: {object_name}", frame)
        key = cv2.waitKey(1)

        if key == ord('t'):
            img_name = f"img_{int(time.time())}.jpg"
            img_path = os.path.join(object_dir, img_name)
            cv2.imwrite(img_path, frame)
            img_count += 1
            print(f"✅ 已保存 {img_name}（总共 {img_count} 张）")

        elif key == ord('q'):
            print("🛑 退出教学模式")
            break

    cap.release()
    cv2.destroyAllWindows()