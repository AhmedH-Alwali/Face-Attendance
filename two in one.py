import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# ============================================================
# 1. مقارنة الوجوه الأساسية (Basic Face Comparison)
# ============================================================
def basic_face_comparison():
    """
    يقوم هذا القسم بتحميل صورتين (مثلاً: إيلون ماسك وبل غيتس) واستخراج ترميزات الوجوه،
    مقارنة الوجوه ورسم المستطيل مع عرض النتيجة.
    """
    # تحميل الصور من المجلد ImagesBasic
    imgElon = face_recognition.load_image_file('ImagesBasic/Elon Musk.jpg')
    imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)
    imgTest = face_recognition.load_image_file('ImagesBasic/Bill gates.jpg')
    imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)
    
    # كشف الوجه واستخراج الترميز للصورة الأولى
    faceLoc = face_recognition.face_locations(imgElon)
    if len(faceLoc) == 0:
        print("لم يتم اكتشاف وجه في صورة Elon Musk!")
        return
    faceLoc = faceLoc[0]
    encodeElon = face_recognition.face_encodings(imgElon)[0]
    cv2.rectangle(imgElon, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)
    
    # كشف الوجه واستخراج الترميز للصورة الثانية
    faceLocTest = face_recognition.face_locations(imgTest)
    if len(faceLocTest) == 0:
        print("لم يتم اكتشاف وجه في صورة Bill gates!")
        return
    faceLocTest = faceLocTest[0]
    encodeTest = face_recognition.face_encodings(imgTest)[0]
    cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)
    
    # مقارنة الوجوه وحساب مسافة التشابه
    results = face_recognition.compare_faces([encodeElon], encodeTest)
    faceDis = face_recognition.face_distance([encodeElon], encodeTest)
    print("نتيجة المقارنة:", results, "ومسافة التشابه:", faceDis)
    
    cv2.putText(imgTest, f'{results} {round(faceDis[0],2)}', (50, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    
    # عرض الصور
    cv2.imshow('Elon Musk', imgElon)
    cv2.imshow('Test Image', imgTest)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
import os
import cv2
import face_recognition

def basic_face_comparison():
    # تحقق من وجود الصور المطلوبة
    if not os.path.exists('ImagesBasic/Elon Musk.jpg'):
        print("خطأ: الصورة 'Elon Musk.jpg' غير موجودة في المجلد 'ImagesBasic'.")
        exit()
    if not os.path.exists('ImagesBasic/Bill gates.jpg'):
        print("خطأ: الصورة 'Bill gates.jpg' غير موجودة في المجلد 'ImagesBasic'.")
        exit()

    imgElon = face_recognition.load_image_file('ImagesBasic/Elon Musk.jpg')
    imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)
    
    imgTest = face_recognition.load_image_file('ImagesBasic/Bill gates.jpg')
    imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

    faceLoc = face_recognition.face_locations(imgElon)[0]
    encodeElon = face_recognition.face_encodings(imgElon)[0]
    cv2.rectangle(imgElon, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

    faceLocTest = face_recognition.face_locations(imgTest)[0]
    encodeTest = face_recognition.face_encodings(imgTest)[0]
    cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

    results = face_recognition.compare_faces([encodeElon], encodeTest)
    faceDis = face_recognition.face_distance([encodeElon], encodeTest)

    print(results, faceDis)
    cv2.putText(imgTest, f'{results} {round(faceDis[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Elon Musk', imgElon)
    cv2.imshow('Test Image', imgTest)
    cv2.waitKey(0)

# ============================================================
# 2. نظام الحضور (Attendance System)
# ============================================================

def findEncodings(images):
    """
    تقوم هذه الدالة باستخراج ترميزات الوجوه لكل صورة في القائمة.
    يتم تحويل الصورة إلى نظام RGB ومن ثم استخراج الترميز.
    """
    encodeList = []
    for img in images:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img_rgb)
        if len(encodes) > 0:
            encodeList.append(encodes[0])
        else:
            print("تحذير: لم يتم اكتشاف وجه في إحدى الصور!")
    return encodeList

def markAttendance(name):
    """
    تقوم هذه الدالة بتسجيل اسم الشخص ووقت ظهوره في ملف Attendance.csv
    إذا لم يكن الاسم مسجلاً مسبقاً.
    """
    try:
        with open('Attendance.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.strip().split(',')
                if entry[0]:
                    nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.write(f'\n{name},{dtString}')
    except FileNotFoundError:
        # في حال عدم وجود الملف، يتم إنشاؤه وتسجيل السطر الأول
        with open('Attendance.csv', 'w') as f:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.write(f'{name},{dtString}')

def run_attendance():
    """
    يقوم هذا القسم بتحميل الصور من مجلد ImagesAttendance، استخراج الترميزات،
    ثم بدء كاميرا الويب لمعالجة الوجوه في الزمن الحقيقي. يتم مقارنة الوجوه
    المكتشفة مع الترميزات المعروفة وتسجيل الحضور إذا كانت مسافة التشابه أقل من 0.50.
    """
    # تحديد مسار مجلد الصور والتحقق من وجوده
    path = 'ImagesAttendance'
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"تم إنشاء مجلد '{path}' تلقائيًا. الرجاء إضافة صور للحضور فيه لتشغيل النظام.")
        exit()  # أو يمكن استخدام return للخروج من الدالة

    myList = os.listdir(path)
    if len(myList) == 0:
        print("لا توجد صور للحضور في المجلد 'ImagesAttendance'. الرجاء إضافة صور.")
        exit()
    
    images = []
    classNames = []
    print("الصور الموجودة:", myList)
    for cl in myList:
        curImg = cv2.imread(os.path.join(path, cl))
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print("الأسماء المسجلة:", classNames)
    
    encodeListKnown = findEncodings(images)
    print('استخراج الترميزات اكتمل')
    
    cap = cv2.VideoCapture(0)
    
    while True:
        success, img = cap.read()
        if not success:
            print("فشل قراءة الإطار من كاميرا الويب.")
            break
        
        # تقليص حجم الإطار لتسريع المعالجة
        imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        
        # معالجة كل وجه مكتشف في الإطار
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
    
            # التحقق باستخدام مسافة الترميز لتحديد مدى تشابه الوجه
            if faceDis[matchIndex] < 0.50:
                name = classNames[matchIndex].upper()
                markAttendance(name)
            else:
                name = 'Unknown'
    
            # تحويل الإحداثيات من الصورة المصغرة إلى الصورة الأصلية
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
    
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# ============================================================
# القائمة الرئيسية لتحديد وضع التشغيل
# ============================================================
if __name__ == "__main__":
    print("اختر الوضع:")
    print("1. مقارنة الوجوه الأساسية (Basic Face Comparison)")
    print("2. نظام الحضور (Attendance System)")
    mode = input("أدخل 1 أو 2: ")
    if mode == "1":
        basic_face_comparison()
    elif mode == "2":
        run_attendance()
    else:
        print("اختيار غير صحيح!")
