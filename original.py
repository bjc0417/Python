import os
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import * #__all__을 쓰지 않는 이상 모든 모듈을 사용하지는 않는다.
from tkinter import filedialog # sub 모듈이므로 별도로 명시해줘야 한다.
from PIL import Image

root = Tk()

''' 제목 '''
root.title("James's photo cut")

''' ===== ===== ===== ===== ===== ===== ===== 각종 함수 ===== ===== ===== ===== ===== ===== ===== '''
# 파일 추가
def add_file():
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요",\
        # filedialog.askopenfilenames : file 열어주는 창이 뜸
        filetypes=(("PNG 파일", "*.png"),("모든 파일","*.*")),\
        initialdir=r"C:\Users\James\Desktop\PythonWorkspace") 
        # 'r' _ 탈출문자없이 그대로 인식하겠다는 의미
        # 최초에 띄워줄 디렉토리를 명시 _ 최초에 사용자가 지정한 경로를 보여줌
    
    # 사용자가 선택한 파일 목록을 출력
    for file in files:
        list_file.insert(END, file)

# 선택 삭제
def del_file():
    #print(list_file.curselection())

    for index in reversed(list_file.curselection()): # reversed() : list_file안에 있는 값을 거꾸로 반환
        list_file.delete(index)

# 저장 경로 (폴더)
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    # filedialog.askdirectory : folder 열어주는 창이 뜸
    if folder_selected == "" : # 사용자가 취소를 누를 때
        print("폴더 선택 취소")
        return
    #print(folder_selected)
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

# 이미지 통합
def merge_img():
    #print("가로넓이 : ", cmb_width.get())
    #print("간격 : ", cmb_space.get())
    #print("포멧 : ", cmb_format.get())

    try:
        # 가로넓이
        img_width = cmb_width.get()
        if img_width == "원본 유지":
            img_width = -1 # -1 일때는 원본기준으로 유지하라
        else:
            img_width = int(img_width)

        # 간격
        img_space = cmb_space.get()
        if img_space == "좁게":
            img_space = 30
        elif img_space == "보통":
            img_space = 90
        elif img_space == "넓게":
            img_space = 120
        else:
            img_space = 0

        # 포멧
        img_format = cmb_format.get().lower() #PNG, JPG, BMP 값을 가져와서 소문자로 변경
        ##############################################################################

        #print(list_file.get(0, END)) # 모든 파일 목록을 가져오기
        images = [Image.open(x) for x in list_file.get(0, END)]
        
        # 이미지 사이즈 리스트에 넣어 하나씩 처리
        image_sizes = [] # [(width1, height1), (width2, height2), ...]
        if img_width > -1 :
            # width 값 변경
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
                                # width                         height
        else: 
            # 원본 사이즈 사용
            image_sizes = [(x.size[0], x.size[1]) for x in images]

        # 계산식
        # 100 * 60 이미지가 있음 >> width 를 80으로 줄이면 height는?
        # 비례식 
        # 답 : 48
        # x : y = x' : y'
        # xy' = x'y
        # y' = x'y / x

        # 코드에 대입
        # x = width = size[0]    //    y = height = size[1]
        # x' = img_width
        # y' = x'y / x = img_width * size[1] / size[0]

        widths, heights = zip(*(image_sizes))
        #>> widths = (10, 20, 30)
        #>> heights = (10, 20, 30)

        # 최대 넓이, 전체 높이 구하기
        max_width, total_height = max(widths), sum(heights)
        # max() : 입력받은 값들 중에서 최댓값을 반환
        # sum() : 입력받은 값을 모두 더한 값을 반환
        
        # 스케치북 준비
        # 이미지 간격 옵션 적용
        if img_space > 0:
            total_height += (img_space * (len(images) - 1))
        result_img = Image.new("RGB", (max_width, total_height),(255,255,255))
        y_offset = 0 # y 위치
        #for img in images:
        #    result_img.paste(img, (0, y_offset))
        #    y_offset += img.size[1] # height 값 만큼 더해줌

        for idx, img in enumerate(images): # idx 를 쓰려면 enumerate를 써야한다.
            # images 안을 순회하면서, idx 와 img 데이터를 가져온다.
            # width가 원본유자가 아닐 때에는 이미지 크기 조정
            if img_width > -1 :
                img = img.resize(image_sizes[idx])

            result_img.paste(img, (0, y_offset))
            y_offset += (img.size[1] + img_space) # height 값 + 사용자가 지정한 간격

            progress = (idx + 1) / len(images) * 100 #실제 percent 정보 계산
            p_var.set(progress)
            progress_bar.update()

        # 포멧 옵션 처리
        file_name = "james_photo." + img_format

        # 저장 될 경로
        dest_path = os.path.join(txt_dest_path.get(), file_name)
        result_img.save(dest_path)
        msgbox.showinfo("알림", "작업이 완료되었습니다.")
    except Exception as err: # 예외처리
        msgbox.showerror("에러", err)

# 시작
def start():
    # 각 옵션들 값을 확인
    #print("가로넓이 : ", cmb_width.get())
    #print("간격 : ", cmb_space.get())
    #print("포멧 : ", cmb_format.get())

    # 파일 목록 확인
    if list_file.size() == 0:
        msgbox.showwarning("경고", "이미지 파일을 추가하세요")
        return
    # 저장 경로 확인
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("경고","저장 경로를 선택하세요")
        return

    # 이미지 통합 작업
    merge_img()
''' ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== '''

''' 파일 프레임 (파일 추가, 선택 삭제) '''
file_frame = Frame(root)
file_frame.pack(fill="x", padx=5, pady=5) # fill = "x" x(가로)축으로 쫙 펼쳐라

btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text="파일 추가", command=add_file)
btn_add_file.pack(side="left")

btn_del_file = Button(file_frame, padx=5, pady=5, width=12, text="선택 삭제", command=del_file)
btn_del_file.pack(side="right")

''' 리스트 프레임 '''
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

''' 저장경로 프레임 '''
path_frame = LabelFrame(root, text="저장 경로")
path_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, ipady=4, padx=5, pady=5)
# ipad = inner padding, 높이변경

btn_dest_path = Button(path_frame, text="찾아보기", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

''' 옵션 프레임 '''
frame_option = LabelFrame(root, text="옵션")
frame_option.pack(padx=5, pady=5, ipady=5)

'''1. 가로 넓이 옵션 '''
# 가로넓이 레이블
lbl_width = Label(frame_option, text="가로넓이", width=8)
lbl_width.pack(side="left", padx=5, pady=5)

# 가로넓이 콤보
opt_width = ["원본 유지", "1024", "800", "640"]
cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width, width=10)
cmb_width.current(0)
cmb_width.pack(side="left", padx=5, pady=5)

'''2. 간격 옵션 '''
# 간격 옵션 레이블
lbl_space = Label(frame_option, text="간격", width=8)
lbl_space.pack(side="left", padx=5, pady=5)

# 간격 옵션 콤보
opt_space = ["없음", "좁게", "보통", "넓게"]
cmb_space = ttk.Combobox(frame_option, state="readonly", values=opt_space, width=10)
cmb_space.current(0)
cmb_space.pack(side="left", padx=5, pady=5)

'''3. 파일 포멧 옵션 '''
# 파일 포멧 옵션 레이블
lbl_format = Label(frame_option, text="포멧", width=8)
lbl_format.pack(side="left", padx=5, pady=5)

# 파일 포멧 옵션 콤보
opt_format = ["PNG", "JPG", "BMP"]
cmb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format, width=10)
cmb_format.current(0)
cmb_format.pack(side="left", padx=5, pady=5)

''' 진행상황 Progress Bar '''
frame_progress = LabelFrame(root, text="진행 상황")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5)

''' 실행 프레임 '''
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, text="닫기", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, text="시작", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)







''' 화면 크기 '''
root.resizable(False, False) # x(너비), y(높이) 값 변경 불가 (창크기 변경 불가)

root.mainloop() # 창이 닫히지 않도록 하는 기능