# -*- coding: utf-8 -*-
from typing import Dict, Text, Any, List, Union, Optional
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action,Tracker 
#from rasa_core_sdk.events import Restarted
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.forms import FormAction
import re
import spacy
import numpy as np
import string



from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType


def Dau(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s
# Tạo Ra các từ sai 
def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)
# Huấn Luyện và dự đoán
def entity_Train(mangEntity):
    mangData=[]
    mangLabel=[]
    for m in range(len(mangEntity)):
        b = Dau(mangEntity[m])
        d = edits1(b)
        c = edits1(mangEntity[m])
        for i_c in c:
            d.add(i_c)
        dt = set(d)
        for i_dt in dt:
            x = nlp(i_dt).vector
            mangData.append(x)
            mangLabel.append(mangEntity[m])

    data = np.array(mangData)
    label = np.array(mangLabel)
    clf = neighbors.KNeighborsClassifier(n_neighbors = 1, p = 2)
    clf.fit(data, label)
    return clf

def entity_predict(mangTest,clf):
    mangT = []
    for t in mangTest:
        T = nlp(t).vector
        mangT.append(T)
    mangTT = np.array(mangT)
    y_pred = clf.predict(mangTT)
    return y_pred

# Tien xu ly
def TienXL(str):
	srt = str.translate(str.maketrans("","",string.punctuation))
	srt = srt.lower()
	srt = srt.replace('  ', ' ')
	srt = srt.strip()
	return srt
# Read data file
def read_file(path):
	import pandas as pd
	xl = pd.ExcelFile(path)
	df = pd.read_excel(xl, 0, header=None)
	mang=[]
	mang2=[]
	max_rows = len(df.iloc[:, 0]) #tong cac dong data
	for i in range(len(df.columns)):
		mang.append(df.at[0, i])
		mang1=[]
		for j in range(1,max_rows):
			mang1.append(df.at[j, i])
		mang2.append(mang1)
	df_data = pd.DataFrame(mang2).T
	df_data.columns = mang
	return df_data
	
CTHV = read_file("excel/DN_CTHV.xlsx")
BoMon = read_file("excel/BoMon.xlsx")
short_BM = read_file("excel/ShortBoMon.xlsx")
BCNK = read_file("excel/BCN.xlsx")
KHMT = read_file("excel/CTDT_KHMT.xlsx")
MMTTT = read_file("excel/CTDT_MMTTT.xlsx")
CNPM = read_file("excel/CTDT_CNPM.xlsx")
THUD = read_file("excel/CTDT_THUD.xlsx")
HTTT = read_file("excel/CTDT_HTTT.xlsx")
CNTT = read_file("excel/CTDT_CNTT.xlsx")
#print(type(CNTT))->dataframe
mangtxt=[]
with open('data/lookup/TenHP.txt','r',encoding='utf-8') as f:
    data = f.read().splitlines()
    mangtxt=data
    f.close()
#print(mangtxt)
#print(CTHV["TenDN"])
#keyCTDT = KHMT.keys()

# Train Entity
#mangData = [CTHV["TenDN"],BoMon["TenBM"],BoMon.keys(),BCNK.keys(),mangtxt,keyCTDT,CNTT["Tên học phần"].dropna(),CNTT.keys()]

dict_CTDT = {
		"khoa học máy tính":[KHMT],
		"công nghệ thông tin":[CNTT],
		"hệ thống thông tin":[HTTT],
		"công nghệ phần mềm":[CNPM],
		"tin học ứng dụng":[THUD],
		"mạng máy tính và truyền thông":[MMTTT]
		}


CTDT = [KHMT,MMTTT,CNPM,CNTT,HTTT,THUD]

#clf_CTDT = [clf_KHMT,clf_MMTTT,clf_CNPM,clf_THUD,clf_HTTT,clf_CNTT]
class ActionRestarted(Action):

	def name(self):
		return "action_restart"

	def run(self, dispatcher, tracker, domain):
		return [SessionStarted()]

class ActionSlotReset(Action): 	
    def name(self): 		
        return 'action_slot_reset' 
	
    def run(self, dispatcher, tracker, domain): 		
        return[AllSlotsReset()]

#done
class Action_CTHV(Action):
    def name(self):
        return "action_CTHV"
    def run(self, dispatcher, tracker, domain):
        list_entity=tracker.get_slot("dn")
        print(list_entity)
        if(list_entity != None):
            for j in range(len(CTHV["TenDN"])):
                #print(CTHV["TenDN"][j])
                if(list_entity[0] == TienXL(CTHV["TenDN"][j])):
                    dispatcher.utter_message(CTHV["DN"][j])
        else:
            dispatcher.utter_message("Xin lỗi tôi không hiểu !\n(Ex: Học phần tiên quyết là gì)")
            print("lỗi get Slot dn None")
        return [AllSlotsReset()]
#done
class Action_SoTC(Action):
    def name(self):
        return "action_SoTC"
    def run(self, dispatcher, tracker, domain):
        MHP=tracker.get_slot("MHP")
        print(MHP)
        THP=tracker.get_slot("THP")
        print(THP)
        list_entity=tracker.get_slot("BM")
        print(list_entity)
        if(list_entity != None and MHP == None and THP == None):
            dispatcher.utter_message(list_entity[0] +" có 155 tín chỉ\n")
        if(MHP != None):
            for m in MHP:
                KT = False
                print("188: "+m)
                for bm in CTDT:
                    if(KT==False):
                        for i in range(len(bm["Mã số học phần"])):
                            if(str(bm["Mã số học phần"][i]).lower()== m.lower()):
                                dispatcher.utter_message(m.title()+" có "+str(bm["Số tín chỉ"][i])+" tín chỉ")
                                KT = True
                                break
                    else:
                        break
                if(KT==False):
                    dispatcher.utter_message(m.title()+" không có trong danh sách học phần")
        if(THP != None):
            KT = False
            for m in THP:
                KT = False
                for d in CTDT:
                    if(KT==False):
                        for i in range(len(d["Tên học phần"])):
                            if(m.lower() == str(d["Tên học phần"][i]).lower()):
                                dispatcher.utter_message(m.title()+" có "+str(d["Số tín chỉ"][i]) + " tín chỉ")
                                KT = True
                                break
                    else:
                        break
            if(KT == False):
                dispatcher.utter_message(m.title()+" không có trong danh sách !")
        if(MHP == None and THP == None  and list_entity == None):
            dispatcher.utter_message("Xin lỗi tôi không hiểu !\n(Ex: Số tín chỉ bộ môn công nghệ thông tin)")
            print("lỗi get Slot BM None")
        return [AllSlotsReset()]
#done
class Action_SHKThucHien(Action):
	def name(self):
		return "action_HKThucHien"
		
	def run(self, dispatcher, tracker, domain):
		MHP=tracker.get_slot("MHP")
		print(MHP)
		THP=tracker.get_slot("THP")
		print(THP)
		if(MHP != None):
			for m in MHP:
				KT = False
				for bm in CTDT:
					if(KT==False):
						for i in range(len(bm["Mã số học phần"])):
							if(str(bm["Mã số học phần"][i]).lower()== m.lower()):
								dispatcher.utter_message(m.title()+" được tổ chức ở các HK sau: - "+str(bm["HK thực hiện"][i]))
								KT = True
								break
					else:
						break
				if(KT==False):
					dispatcher.utter_message(m.title()+" không có trong danh sách học phần")
		if(THP != None):
			KT = False
			for m in THP:
				KT = False
				for d in CTDT:
					if(KT==False):
						for i in range(len(d["Tên học phần"])):
							if(m.lower() == str(d["Tên học phần"][i]).lower()):
								dispatcher.utter_message(m.title()+" được tổ chức ở các HK sau: - "+str(d["HK thực hiện"][i]))
								KT = True
								break
					else:
						break
			if(KT == False):
				dispatcher.utter_message(m.title()+" không có trong danh sách !")
		if(MHP == None and THP == None):
			dispatcher.utter_message("Xin lỗi tôi không hiểu !\n(Ex: HK thực hiện của anh văn căn bản 2)")
			print("lỗi get Slot BM None")
		return [AllSlotsReset()]




#done
class Action_ChucVuGV(Action):
    def name(self):
        return "action_ChucVuGV"
		
    def run(self, dispatcher, tracker, domain):
        BM=tracker.get_slot("BM")
        CV=tracker.get_slot("CV")
        print(BM,CV)
        if(BM != None and CV != None):
            for i in BM:
                for j in range(len(BoMon["TenBM"])):
                    if(i == TienXL(BoMon["TenBM"][j])):
                        for k in CV:
                            print("kq phan hoi {}".format(BoMon[k][j]))
                            dispatcher.utter_message(BoMon[k][j])
        else:
            dispatcher.utter_message("Xin lỗi tôi không hiểu!\n(Ex: Trưởng bộ môn khoa học máy tính là ai)")
            print("lỗi get Slot BM None or CV None")
        return [AllSlotsReset()]
#done
class Action_GioiThieuBoMon(Action):
    def name(self):
        return "action_GioiThieuBoMon"
		
    def run(self, dispatcher, tracker, domain):
        BM=tracker.get_slot("BM")
        print(BM)
        if(BM != None):
            for i in BM:
                print("294 "+i)
                for j in range(len(BoMon["TenBM"])):
                    if(i == TienXL(BoMon["TenBM"][j]) or i== TienXL(short_BM["TenBM"][j])):
                        dispatcher.utter_message(i.title()+":\n"+BoMon["GioiThieu"][j])
        else:
            dispatcher.utter_message("Xin lỗi tôi không hiểu!\n(Để biết về bộ môn vui lòng hỏi: Giới thiệu về bộ môn khoa học máy tính)")
            print("lỗi get Slot BM None")
        return [AllSlotsReset()]
#done
class Action_BanChuNhiemKhoa(Action):
	def name(self):
		return "action_BanChuNhiemKhoa"
		
	def run(self, dispatcher, tracker, domain):
		BCN=tracker.get_slot("BCN")
		print(BCN)
		if(BCN != None):
			for i in BCN:
				dispatcher.utter_message(i.title()+":\n"+BCNK[i][0])
		else:
			dispatcher.utter_message("Xin lỗi tôi không hiểu!\n(Ex: Trưởng khoa là ai)")
			print("lỗi get Slot BCN None")
		return [AllSlotsReset()]
#done
class Action_MaHP(Action):
	def name(self):
		return "action_MaHP"
		
	def run(self, dispatcher, tracker, domain):
		MHP=tracker.get_slot("MHP")
		print(MHP)
		THP=tracker.get_slot("THP")
		print(THP)
		if(MHP != None):
			for m in MHP:
				KT = False
				for bm in CTDT:
					if(KT==False):
						for i in range(len(bm["Mã số học phần"])):
							if(str(bm["Mã số học phần"][i]).lower()==m.lower()):
								dispatcher.utter_message(m.title()+" là học phần "+bm["Tên học phần"][i])
								KT = True
								break
					else:
						break
				if(KT==False):
					dispatcher.utter_message(m.title()+" không có trong danh sách học phần")

		elif(THP != None):
			KT = False
			for m in THP:
				KT = False
				for d in CTDT:
					if(KT==False):
						for i in range(len(d["Tên học phần"])):
							if(m.lower() == str(d["Tên học phần"][i]).lower()):
								dispatcher.utter_message(m.title()+" Có mã học phần là: "+d["Mã số học phần"][i])
								KT = True
								break
					else:
						break
			if(KT == False):
				dispatcher.utter_message(m.title()+" không có trong danh sách !")

		else:
			dispatcher.utter_message("Xin lỗi tôi không hiểu!\n(Ex: CT179 là học phần gì)")
			print("lỗi get Slot NHP None")
		return [AllSlotsReset()]


'''
class HPTQ_Form(FormAction):
	def name(self) -> Text:
		return "HPTQ_form"

	@staticmethod
	def required_slots(tracker: Tracker) -> List[Text]:
		return ["BM"]
	def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
		return {"BM": self.from_entity(entity="BM")
				}

	@staticmethod
	def BM_db() -> List[Text]:

		return ["khoa học máy tính",
				"công nghệ thông tin",
				"hệ thống thông tin",
				"công nghệ phần mềm",
				"mạng máy tính và truyền thông",
				"tin học ứng dụng"]

	@staticmethod
	def is_int(string: Text) -> bool:

		try:
			int(string)
			return True
		except ValueError:
			return False

	def validate_BM(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:
		print(value)
		BM = tracker.get_slot("BM")
		print(BM)
		print(type(BM))
		BM = entity_predict(BM,clf_BoMon)
		print(BM)
		value = BM[0]
		print(value)
		if value in self.BM_db():
			return {"BM": value}
		else:
			dispatcher.utter_template("utter_wrong_BM", tracker)
			return {"BM": None}


	def submit(
	    self,
	    dispatcher: CollectingDispatcher,
	    tracker: Tracker,
	    domain: Dict[Text, Any],
	) -> List[Dict]:

		entityTrueBM=tracker.get_slot("BM")
		THP=tracker.get_slot("THP")
		MHP=tracker.get_slot("MHP")
		HPKey=tracker.get_slot("dn")
		print("Trc khi dự đoán THP:",THP)
		print("Trc khi dự đoán: HPKey",HPKey)
		print("Ma Hoc Phan: ",MHP)
		if(THP != None and HPKey != None):
			for k in dict_CTDT.keys():
				if(k == entityTrueBM):
					entityTrueTHP =entity_predict(THP,dict_CTDT[entityTrueBM][1])
					print("Sau khi dự đoán THP:",entityTrueTHP)
					entityTrueHPKey =entity_predict(HPKey,clf_Key)
					print("sau khi dự đoán HPKey:",entityTrueHPKey)
					for i in entityTrueTHP:
						for j in range(len(dict_CTDT[entityTrueBM][0]["Tên học phần"])):
							if(i==TienXL(str(dict_CTDT[entityTrueBM][0]["Tên học phần"][j]))):
								for x in entityTrueHPKey:
									for y in dict_CTDT[entityTrueBM][0].keys():
										if(x == TienXL(y)):
											if(str(dict_CTDT[entityTrueBM][0][y][j])=="nan"):
												dispatcher.utter_message(y.title()+ " của " +dict_CTDT[entityTrueBM][0]["Tên học phần"][j]+": Không có")
											else:
												dispatcher.utter_message(y.title()+" của "+dict_CTDT[entityTrueBM][0]["Tên học phần"][j]+": "+ str(dict_CTDT[entityTrueBM][0][y][j]))		
		if(MHP != None and HPKey != None):
			for k in dict_CTDT.keys():
				if(k == entityTrueBM):
					entityTrueTHP = MHP
					print("Sau khi dự đoán THP:",entityTrueTHP)
					entityTrueHPKey =entity_predict(HPKey,clf_Key)
					print("sau khi dự đoán HPKey:",entityTrueHPKey)
					for i in entityTrueTHP:
						KT = False
						for j in range(len(dict_CTDT[entityTrueBM][0]["Mã số học phần"])):
							if(i==TienXL(str(dict_CTDT[entityTrueBM][0]["Mã số học phần"][j]))):
								for x in entityTrueHPKey:
									for y in dict_CTDT[entityTrueBM][0].keys():
										if(x == TienXL(y)):
											if(str(dict_CTDT[entityTrueBM][0][y][j])=="nan"):
												dispatcher.utter_message(y.title()+ " của " +dict_CTDT[entityTrueBM][0]["Mã số học phần"][j]+": Không có")
											else:
												dispatcher.utter_message(y.title()+" của "+dict_CTDT[entityTrueBM][0]["Mã số học phần"][j]+": "+ str(dict_CTDT[entityTrueBM][0][y][j]))
											KT = True
						if(KT==False):	
							dispatcher.utter_message(i.upper()+" không có trong chương trình đào tạo "+ entityTrueBM.title())

		if((MHP == None and THP == None) or (HPKey == None and THP == None) or (HPKey == None and MHP == None)):
			dispatcher.utter_message("Xin lỗi tôi không xác định được ý định và tên học phần.\n(Ex: Học phần tiên quyết của Anh văn căn bản 2 là gì)")
			print("lỗi get Slot NHP None HPKey None")
		return [AllSlotsReset()]
'''

"""


		if(entityTrueBM == "khoa học máy tính"):
			entityTrueTHP =entity_predict(THP,clf_KHMT)
			print("Sau khi dự đoán THP:",entityTrueTHP)
			entityTrueHPKey =entity_predict(HPKey,clf_KHMT)
			print("sau khi dự đoán HPKey:",entityTrueHPKey)
			for i in entityTrueTHP:
				for j in range(len(KHMT["Tên học phần"])):
					if(i==TienXL(str(KHMT["Tên học phần"][j]))):
						for x in entityTrueHPKey:
							for y in KHMT.keys():
								if(x == TienXL(y)):
									if(str(KHMT[y][j])=="nan"):
										dispatcher.utter_message(y.title()+ " của " +KHMT["Tên học phần"][j]+":\n- Không có")
									else:
										dispatcher.utter_message(y.title()+" của "+KHMT["Tên học phần"][j]+":\n- "+ str(KHMT[y][j]))
		
		if(entityTrueBM == "hệ thống thông tin"):
			entityTrueTHP =entity_predict(THP,clf_HTTT)
			print(entityTrueTHP)
			entityTrueHPKey =entity_predict(HPKey,clf_HTTT)
			print("Tên định nghĩa: ",entityTrueHPKey)
			for i in entityTrueTHP:
				for j in range(len(HTTT["Tên học phần"])):
					if(i==TienXL(str(HTTT["Tên học phần"][j]))):
						for x in entityTrueHPKey:
							for y in HTTT.keys():
								if(x == TienXL(y)):
									if(str(HTTT[y][j])=="nan"):
										dispatcher.utter_message(y.title()+" của "+HTTT["Tên học phần"][j]+":\nKhông có")
									else:
										dispatcher.utter_message(y.title()+" của "+HTTT["Tên học phần"][j]+":\n"+ str(HTTT[y][j]))

		if(entityTrueBM == "công nghệ thông tin"):
			entityTrueTHP =entity_predict(THP,clf_CNTT)
			print(entityTrueTHP)
			entityTrueHPKey =entity_predict(HPKey,clf_CNTT)
			print("Tên định nghĩa: ",entityTrueHPKey)
			for i in entityTrueTHP:
				for j in range(len(CNTT["Tên học phần"])):
					if(i==TienXL(str(CNTT["Tên học phần"][j]))):
						for x in entityTrueHPKey:
							for y in CNTT.keys():
								if(x == TienXL(y)):
									if(str(CNTT[y][j])=="nan"):
										dispatcher.utter_message(y.title()+" của "+CNTT["Tên học phần"][j]+":\nKhông có")
									else:
										dispatcher.utter_message(y.title()+" của "+CNTT["Tên học phần"][j]+":\n"+ str(CNTT[y][j]))

		if(entityTrueBM == "công nghệ phần mềm"):
			entityTrueTHP =entity_predict(THP,clf_CNPM)
			print(entityTrueTHP)
			entityTrueHPKey =entity_predict(HPKey,clf_CNPM)
			print("Tên định nghĩa: ",entityTrueHPKey)
			for i in entityTrueTHP:
				for j in range(len(CNPM["Tên học phần"])):
					if(i==TienXL(str(CNPM["Tên học phần"][j]))):
						for x in entityTrueHPKey:
							for y in CNPM.keys():
								if(x == TienXL(y)):
									if(str(CNPM[y][j])=="nan"):
										dispatcher.utter_message(y.title()+" của "+CNPM["Tên học phần"][j]+":\nKhông có")
									else:
										dispatcher.utter_message(y.title()+" của "+CNPM["Tên học phần"][j]+":\n"+ str(CNPM[y][j]))

		if(entityTrueBM == "tin học ứng dụng"):
			entityTrueTHP =entity_predict(THP,clf_THUD)
			print(entityTrueTHP)
			entityTrueHPKey =entity_predict(HPKey,clf_THUD)
			print("Tên định nghĩa: ",entityTrueHPKey)
			for i in entityTrueTHP:
				for j in range(len(THUD["Tên học phần"])):
					if(i==TienXL(str(THUD["Tên học phần"][j]))):
						for x in entityTrueHPKey:
							for y in THUD.keys():
								if(x == TienXL(y)):
									if(str(THUD[y][j])=="nan"):
										dispatcher.utter_message(y.title()+" của "+THUD["Tên học phần"][j]+":\nKhông có")
									else:
										dispatcher.utter_message(y.title()+" của "+THUD["Tên học phần"][j]+":\n"+ str(THUD[y][j]))

		if(entityTrueBM == "mạng máy tính và truyền thông"):
			entityTrueTHP =entity_predict(THP,clf_MMTTT)
			print(entityTrueTHP)
			entityTrueHPKey =entity_predict(HPKey,clf_MMTTT)
			print("Tên định nghĩa: ",entityTrueHPKey)
			for i in entityTrueTHP:
				for j in range(len(MMTTT["Tên học phần"])):
					if(i==TienXL(str(MMTTT["Tên học phần"][j]))):
						for x in entityTrueHPKey:
							for y in MMTTT.keys():
								if(x == TienXL(y)):
									if(str(MMTTT[y][j])=="nan"):
										dispatcher.utter_message(y.title()+" của "+MMTTT["Tên học phần"][j]+":\nKhông có")
									else:
										dispatcher.utter_message(y.title()+" của "+MMTTT["Tên học phần"][j]+":\n"+ str(MMTTT[y][j]))
		"""
