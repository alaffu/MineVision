import subprocess #a
import cv2 as cv

# purpose of this code is to check the files in ~/vision_training then check
# each file to find the biggest n number in it, for example img_1, img 99 it
# should return 99 so when  we do the vision training no files get overwritten


def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def biggest_number(split_list, debug_mode=None):
    split_list2 = []

    for i in range(len(split_list)):
        x = split_list[i].splitlines()
        split_list2.append(x)

    if debug_mode:
        print("this is split_list2\n", split_list2)

    for i in range(len(split_list2)):
        larg = 0

        for x in (split_list2):
            if is_number(x[0]):
                x = int(x[0])
                if x > larg:
                    print(x)
                    larg = x

    return larg


def screenshot_vision(img, key_negative='d', key_positive='f'):
    key = cv.waitKey(1)
    big_n = biggest_number(negative_list)

    write = str('img_{}'.format(big_n + 1))

    if key == ord(key_positive):
        cv.imwrite('positive/{}.jpg'.format(write), img)

    if key == ord(key_negative):
        cv.imwrite('positive/{}.jpg'.format(write), img)


def ls_files(path_files):

    list_files = subprocess.run(['ls {}'.format(path_files)],
                                capture_output=True,
                                text=True,
                                shell=True)  # security problem using shell=True

    return list_files


# it will ls on negative's folders and put the output into negative_list
path_negative = '~/Documents/minecraft_bot2/vision_training/negative'
negative_list = ls_files(path_negative)
negative_list = negative_list.stdout.split("_")

# find the biggest number on the title of the files example: img_1, img_99 it
# will return 99
big_n = biggest_number(negative_list)

print("this is the biggest number " + str(big_n))
