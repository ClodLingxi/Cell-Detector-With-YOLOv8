import cv2
import os


def pic_pre_handle(pic_path='./output_blocks/'):

    PIC_LOCATION = pic_path

    for root, dirs, files in os.walk(PIC_LOCATION):
        for file in files:
            image = cv2.imread(os.path.join(root, file))

            height, width = image.shape[:2]

            block_size = 640

            output_dir = file
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            num_blocks_x = width // block_size
            num_blocks_y = height // block_size

            block_id = 0
            for y in range(num_blocks_y):
                for x in range(num_blocks_x):
                    start_x = x * block_size
                    start_y = y * block_size
                    end_x = start_x + block_size
                    end_y = start_y + block_size

                    # 裁剪图像块
                    block = image[start_y:end_y, start_x:end_x]

                    # 保存块
                    block_filename = os.path.join(output_dir, f'block_{block_id}.jpg')
                    cv2.imwrite(block_filename, block)
                    block_id += 1

            # 处理图像右边和下边可能的剩余部分
            if width % block_size != 0:
                for y in range(num_blocks_y):
                    start_x = num_blocks_x * block_size
                    start_y = y * block_size
                    end_x = width
                    end_y = start_y + block_size
                    block = image[start_y:end_y, start_x:end_x]
                    block_filename = os.path.join(output_dir, f'block_{block_id}.jpg')
                    cv2.imwrite(block_filename, block)
                    block_id += 1

            if height % block_size != 0:
                for x in range(num_blocks_x):
                    start_x = x * block_size
                    start_y = num_blocks_y * block_size
                    end_x = start_x + block_size
                    end_y = height
                    block = image[start_y:end_y, start_x:end_x]
                    block_filename = os.path.join(output_dir, f'block_{block_id}.jpg')
                    cv2.imwrite(block_filename, block)
                    block_id += 1

            if width % block_size != 0 and height % block_size != 0:
                start_x = num_blocks_x * block_size
                start_y = num_blocks_y * block_size
                block = image[start_y:height, start_x:width]
                block_filename = os.path.join(output_dir, f'block_{block_id}.jpg')
                cv2.imwrite(block_filename, block)
