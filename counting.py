import cv2
import matplotlib.pyplot as plt
import numpy as np

MIN_AREA = 2000
MAX_AREA = 50000

def experiment_hsv(img_rgb):
    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)

    H, S, V = cv2.split(hsv)

    cv2.imwrite("output/steps/01_hue.png", H)
    cv2.imwrite("output/steps/02_saturation.png", S)
    cv2.imwrite("output/steps/03_value.png", V)

    plt.figure(figsize=(15,4))

    plt.subplot(131)
    plt.hist(H.ravel(), bins=256)
    plt.title("Histogram Hue")

    plt.subplot(132)
    plt.hist(S.ravel(), bins=256)
    plt.title("Histogram Saturation")

    plt.subplot(133)
    plt.hist(V.ravel(), bins=256)
    plt.title("Histogram Value")

    plt.tight_layout()

    plt.savefig("output/steps/04_histogram_hsv.png")

    plt.close()

    _, mask_h = cv2.threshold(H, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    _, mask_s = cv2.threshold(S, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    _, mask_v = cv2.threshold(V, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.imwrite("output/steps/05_hue_mask.png", mask_h)
    cv2.imwrite("output/steps/06_saturation_mask.png", mask_s)
    cv2.imwrite("output/steps/07_value_mask.png", mask_v)

    mask = cv2.inRange(hsv, (0, 0, 120), (180, 80, 255))

    cv2.imwrite("output/steps/08_hsv_segmentation.png", mask)

    kernel = np.ones((5, 5), np.uint8)

    mask_clean = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite("output/steps/09_hsv_morphology.png", mask_clean)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask_clean)

    result = img_rgb.copy()

    count = 0

    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]

        if MIN_AREA < area < MAX_AREA:
            count += 1

            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]

            cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 3)

    cv2.imwrite(
        "output/steps/10_hsv_bounding_box.png", cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    )

    cv2.imwrite("output/result.png", cv2.cvtColor(result, cv2.COLOR_RGB2BGR))

    return count

def experiment_edge(img_rgb):
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    cv2.imwrite("output/steps/11_grayscale.png",gray)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    cv2.imwrite("output/steps/12_blur.png", blur)

    edges = cv2.Canny(blur, 50, 150)

    cv2.imwrite("output/steps/13_canny.png", edges)

    kernel = np.ones((3,3), np.uint8)

    dilated = cv2.dilate(edges, kernel, iterations=1)

    cv2.imwrite("output/steps/14_dilation.png", dilated)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    result = img_rgb.copy()

    count = 0

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if MIN_AREA < area < MAX_AREA:

            count += 1

            x, y, w, h = cv2.boundingRect(cnt)

            cv2.rectangle(result, (x, y), (x+w, y+h), (255, 0, 0), 3)

    cv2.imwrite(
        "output/steps/15_edge_bounding_box.png", cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    )

    return count

def experiment_threshold(img_rgb):
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    cv2.imwrite("output/steps/16_gray_threshold.png", gray)

    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.imwrite("output/steps/17_otsu_threshold.png", thresh)

    kernel = np.ones((5, 5), np.uint8)

    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    cv2.imwrite("output/steps/18_opening.png", opened)

    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite("output/steps/19_closing.png", closed)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(closed)

    result = img_rgb.copy()

    count = 0

    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]

        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]

        aspect = w / h

        if MIN_AREA < area < MAX_AREA and 0.3 < aspect < 3:
            count += 1

            cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 3)

    cv2.imwrite(
        "output/steps/20_threshold_bounding_box.png", cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    )

    return count

if __name__ == "__main__":
    img = cv2.imread("input/parking.jpg")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    cv2.imwrite("output/steps/00_original.png", img)

    hsv_count = experiment_hsv(img_rgb)
    edge_count = experiment_edge(img_rgb)
    threshold_count = experiment_threshold(img_rgb)

    print("Jumlah Mobil Terdeteksi oleh Pendekatan:")
    print("HSV = ", hsv_count)
    print("Edge = ", edge_count)
    print("Threshold = ", threshold_count)
