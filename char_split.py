import cv2
import contour_recognition
from time import sleep


def char_preprocess(contour_path):
    img = cv2.imread(contour_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_thre = img_gray
    cv2.threshold(img_gray, 140, 255, cv2.THRESH_BINARY, img_thre)

    # cv2.imshow('threshold', img_thre)
    # cv2.waitKey(0)

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

    arg = True  # False 白底黑字 True 黑底白字

    return width, height, white, black, white_max, black_max, arg


def find_end(start_, width, height, white, black, white_max, black_max, arg, times, cc_in):
    end_ = start_ + 1
    jug_counter = 0
    for m in range(start_+1, width-1):
        if (black[m] if arg else white[m]) > ((0.95 - 0.01*times) * black_max if arg else (0.95 - 0.01*times) * white_max):
            end_ = m
            jug_counter += 1
            if end_ - start_ > width / 10:
                break
    if end_ - start_ > width / 50 and cc_in <7:
        print('getin1')

        return end_
    else:
        print('get2')
        return start_
    # return end_
    # print('/:'+str((end_-start_)/width))
    # return end_


def pic_split(src_path):
    time_total = 0
    cj_list_last = []
    char_counter_max = 0
    while True:
        img_thre_global = char_preprocess(src_path)
        width_global, height_global, white_global, black_global, white_max_global, black_max_global, arg_global = char_split(img_thre_global)
        n = 1
        start = 1
        end = 2
        char_counter = 0
        cj_list = []
        while n < width_global - 2:
            n += 1
            if (white_global[n] if arg_global else black_global[n]) > (0.1 * white_max_global if arg_global else 0.1 * black_max_global):
                start = n
                end = find_end(start, width_global, height_global, white_global, black_global, white_max_global, black_max_global, arg_global, time_total, char_counter)
                n = end
                # print(arg_global)
                # print('start:'+str(start)+' end:'+str(end))
                if end != start:
                    cj = img_thre_global[1:height_global, start:end]
                    # cv2.namedWindow(str(char_counter))
                    # cv2.imshow('spilt'+str(char_counter), cj)
                    char_counter += 1
                    # cv2.waitKey(0)
                    cj_list.append(cj)
                # else:
                #     pass
        print(char_counter)
        if char_counter > 6:
            # print(1)
            break
        elif char_counter < char_counter_max:
            # print(2)
            cj_list = cj_list_last
            break
        else:
            # print(3)
            cj_list_last = cj_list
            char_counter_max = char_counter
        time_total += 1
    for cj in cj_list:
        cv2.imshow('split', cj)
        cv2.waitKey(0)


if __name__ == '__main__':
    img_plate_src, img_src = contour_recognition.get_contour('./test_pic/4.jpg')
    pic_split('./test_pic/number_plate.jpg')
    cv2.namedWindow('src_pic')
    cv2.imshow('test', img_src)
    cv2.namedWindow('plate')
    cv2.imshow('plate', img_plate_src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
