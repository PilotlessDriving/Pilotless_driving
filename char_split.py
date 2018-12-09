import cv2
import contour_recognition
from time import sleep


def char_preprocess(contour_path):
    img = cv2.imread(contour_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_thre = img_gray
    cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY, img_thre)

    cv2.imshow('threshold', img_thre)
    cv2.waitKey(0)

    cv2.imwrite('./test_pic/thre_res.png', img_thre)

    return img_thre


def char_split(img_thre):
    white = []
    black = []
    height = img_thre.shape[0]
    width = img_thre.shape[1]
    white_max = 0
    black_max = 0
    white_max_counter = 0
    black_max_counter = 0

    for i in range(width):
        s = 0
        t = 0
        for j in range(height):
            if img_thre[j][i] == 255:
                s += 1
            if img_thre[j][i] == 0:
                t += 1
        if s > white_max + 5:
            white_max = s
            white_max_counter = 0
        elif s >= white_max:
            white_max = s
            white_max_counter += 1
        if t > black_max + 5:
            black_max = t
            black_max_counter = 0
        elif t >= black_max:
            black_max = t
            black_max_counter += 1
        white_max = max(white_max, s)
        black_max = max(black_max, t)
        white.append(s)
        black.append(t)
        # print(s)
        # print(t)

    arg = False  # False 白底黑字 True 黑底白字
    print(black_max)
    print(black_max_counter)
    print(white_max)
    print(white_max_counter)
    # sleep(1000)
    if black_max > white_max and black_max_counter > white_max_counter:
        arg = True
    elif white_max < black_max + 5 and black_max_counter > white_max_counter + 5:
        arg = True

    return width, height, white, black, white_max, black_max, arg


def find_end(start_, width, height, white, black, white_max, black_max, arg):
    end_ = start_ + 1
    jug_counter = 0
    for m in range(start_+1, width-1):
        if (black[m] if arg else white[m]) > (0.85 * black_max if arg else 0.85 * white_max):
            end_ = m
            jug_counter += 1
            if jug_counter > 1:
                break

    return end_


def pic_split(src_path):
    img_thre_global = char_preprocess(src_path)
    width_global, height_global, white_global, black_global, white_max_global, black_max_global, arg_global = char_split(img_thre_global)
    n = 1
    start = 1
    end = 2
    char_counter = 0
    while n < width_global - 2:
        n += 1
        if (white_global[n] if arg_global else black_global[n]) > (0.1 * white_max_global if arg_global else 0.1 * black_max_global):
            start = n
            end = find_end(start, width_global, height_global, white_global, black_global, white_max_global, black_max_global, arg_global)
            n = end
            print(arg_global)
            print('start:'+str(start)+' end:'+str(end))
            if end-start > width_global / 14:
                cj = img_thre_global[1:height_global, start:end]
                cv2.namedWindow(str(char_counter))
                cv2.imshow('spilt'+str(char_counter), cj)
                char_counter += 1
                cv2.waitKey(0)


if __name__ == '__main__':
    img_plate_src, img_src = contour_recognition.get_contour('./test_pic/10.jpg')
    pic_split('./test_pic/number_plate.jpg')
    cv2.namedWindow('src_pic')
    cv2.imshow('test', img_src)
    cv2.namedWindow('plate')
    cv2.imshow('plate', img_plate_src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
