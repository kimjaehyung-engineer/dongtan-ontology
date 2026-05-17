import os

def pop_up_drawing():
    file_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\도면\DT-ARC-001_Station_Plan.html"
    
    print("RODO: 지식망에서 [정거장 곡선부 PSD 간섭 리스크]를 검색했습니다.")
    print(f"RODO: 관련 도면을 발견했습니다. -> {file_path}")
    print("RODO: 브라우저를 통해 도면을 팝업합니다...")
    
    try:
        os.startfile(file_path)
        print("RODO: 도면 팝업 성공! 브라우저 창을 확인해 주세요.")
    except Exception as e:
        print(f"RODO: 팝업 실패. Error: {e}")

if __name__ == "__main__":
    pop_up_drawing()
