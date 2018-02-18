import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class news_record :
    '''
    사용자가 특정 뉴스를 조회한 기록을 저장하는 class (열람한 뉴스의 document_id / press / category / title / request_time을 저장한다.)
    '''
    def __init__(self, **news_info) :
        self.document_id = news_info["document_id"]
        self.press = news_info["press"]
        self.category = news_info["category"]
        self.title = news_info["title"]
        self.request_time = news_info["request_time"]


    def print_news_record(self):
        '''
        news_record 객체의 값을 print하는 함수
        :return: None
        '''
        print("document_id: ", self.document_id,
              "\npress: ", self.press,
              "\ncategory: ", self.category,
              "\ntitle: ", self.title,
              "\nrequest_time: ", self.request_time)


class user_status :
    '''
    사용자의 정보를 저장하는 class (사용자의 user_key, 성별, 생년, 지역, 열람한 뉴스 목록, 서비스 제공을 위한 파라미터 정보를 저장한다.)
    '''
    def __init__(self, **user_info):
        '''
        사용자 정보를 담고 있는 user_status 객체 생성
        :param user_info: user_info: document_id, gender, birth_year, location을 key로 가지는 dictionary 
        '''
        self.user_key = user_info["user_key"]
        self.gender = user_info["gender"]
        self.birth_year = user_info["birth_year"]
        self.location = user_info["location"]
        self.news_record_list = []
        self.recommend_service = "Y"
        self.remove_seen_news = "Y"


    def update_user_status(self, **user_info):
        '''
        저장된 사용자의 user_key, 성별, 생년, 지역 정보를 변경한다.
        :param user_info: document_id, gender, birth_year, location을 key로 가지는 dictionary 
        :return: None
        '''
        self.user_key = user_info["user_key"]
        self.gender = user_info["gender"]
        self.birth_year = user_info["birth_year"]
        self.location = user_info["location"]


    def set_recommend_service(self, flag):
        '''
        사용자의 추천 서비스 이용 여부 정보를 변경한다. 지정된 것 외의 문자를 입력하면 에러 발생
        :param flag: "y", "Y", "n", "N" 중 한가지로 길이 1의 문자열.
        :return: None
        '''
        if flag.upper()=="Y" :
            self.recommend_service = flag.upper()
        elif flag.upper()=="N" :
            self.recommend_service = flag.upper()
        else :
            raise "Wrong parameter input. Parameter should be 'Y' or 'N'."


    def set_remove_seen_news(self, flag):
        '''
        사용자의 열람한 뉴스를 목록에서 제거할지 여부 정보를 변경한다. 지정된 것 외의 문자를 입력하면 에러 발생
        :param flag: "y", "Y", "n", "N" 중 한가지로 길이 1의 문자열.
        :return: None
        '''
        if flag.upper()=="Y" :
            self.remove_seen_news = flag.upper()
        elif flag.upper()=="N" :
            self.remove_seen_news = flag.upper()
        else :
            raise "Wrong parameter input. Parameter should be 'Y' or 'N'."


    def add_news_record(self, news_record_instnace):
        '''
        열람한 뉴스 정보를 담고 있는 news_record 객체를 사용자의 news_record_list에 추가한다.
        :param news_record_instnace: 뉴스 정보를 담고 있는 news_record 객체
        :return: None
        '''
        self.news_record_list.append(news_record_instnace)


    def print_user_status(self):
        '''
        사용자의 정보를 담고 있는 user_status의 내역을 출력한다.
        :return: None 
        '''
        print("Printing", self.user_key, "user_status.")
        print("=" * 40)
        print("user_key: ", self.user_key,
              "\ngender: ", self.gender,
              "\nbirth_year: ", self.birth_year,
              "\nlocation: ", self.location,
              "\nrecommend_service: ", self.recommend_service,
              "\nremove_seen_news: ", self.remove_seen_news)
        print("="*40)


    def print_news_record(self):
        '''
        사용자가 열람한 뉴스 목록의 세부 사항을 출력한다.
        :return: None
        '''
        print("Printing",len(self.news_record_list),"news_record by latest order.")
        print("=" * 40)
        for i,news in enumerate(self.news_record_list) :
            print("news %d:" %(i+1))
            print("\tdocument_id: ", news.document_id,
                  "\n\tpress: ", news.press,
                  "\n\tcategory: ", news.category,
                  "\n\ttitle: ", news.title,
                  "\n\trequest_time: ",news.request_time)
        print("=" * 40)


class user_information_manager:
    '''
    모든 사용자의 뉴스 열람 내역을 2d matrix 형태의 pandas DataFrame으로 저장 및 관리하기 위한 객체.
    정보는 pickle을 이용해 객체 생성시 입력한 path에 저장되며, 이전 path와 다르면 이전 정보를 관리할 수 없기 때문에 고정해야 한다. (백업 용도 제외)
    '''
    def __init__(self, path):
        '''
        저장된 파일이 없으면 빈 파일을 새로 만들어 저장하고, 저장된 파일이 있다면 불러온다.
        :param path: 정보를 저장할 파일의 위치 및 파일명.txt 
        '''
        self.path = path
        self.user_record = None #사용자의 press, category별 열람 횟수를 frequency table로 저장한다
        self.user_vector = None #user_record를 사용자별로 총합 1의 0~1사이의 실수들로 정규화한다.
        try:
            with open(self.path, mode="rb") as fp:
                self.user_record = pickle.load(fp)
                self.regularize_user_record()
                print("User_record file has been loaded successfully.")
        except:
            print("There is no existing user data.")
            with open(self.path, mode="wb") as fp:
                self.user_record = pd.DataFrame(data=None)
                pickle.dump(self.user_record, fp)
            print("Empty data file was created.")


    def is_user_record_empty(self):
        '''
        user_record가 빈 파일인지 아닌지 boolean 값으로 반환하는 함수
        :return: boolean
        '''
        if len(self.user_record) == 0:
            return True
        else:
            return False


    def is_user_vector_empty(self):
        '''
        user_vector가 빈 파일인지 아닌지 boolean 값으로 반환하는 함수
        :return: boolean
        '''

        if len(self.user_vector) == 0:
            return True
        else:
            return False


    def update_user_record_file(self):
        '''
        변경된 user_record 내역을 파일에 업데이트하여 저장하는 함수.
        :return: None 
        '''
        with open(self.path, mode="wb") as fp:
            pickle.dump(self.user_record, fp)
            print("User_record file has been updated successfully.")


    def is_new_user(self, user_key):
        '''
        입력한 user_key가 정보에 저장된 사용자의 user_key인지 아닌지 boolean으로 반환하는 함수 
        :param user_key: 
        :return: boolean 
        '''
        if user_key not in self.user_record.index:
            return True
        else:
            return False


    def is_new_press(self, news_record_instance):
        '''
        등록하는 news_record 객체의 press가 이미 등록되었는지 아닌지 boolean으로 반환하는 함수
        :param news_record_instance: 사용자가 열람한 뉴스를 저장하는 news_record 객체
        :return: boolean 
        '''
        if news_record_instance.press not in self.user_record.columns.values:
            return True
        else:
            return False


    def is_new_category(self, news_record_instance):
        '''
        등록하는 news_record 객체의 category가 이미 등록되었는지 아닌지 boolean으로 반환하는 함수
        :param news_record_instance: 사용자가 열람한 뉴스를 저장하는 news_record 객체
        :return: boolean
        '''
        if news_record_instance.category not in self.user_record.columns.values:
            return True
        else:
            return False


    def update_user_news_record_list(self, user_key, news_record_instance):
        # 해당 user_key의 user_status 객체를 불러와서 news_record_instance를 업데이트한다.
        # user_status 객체의 클래스 메소드인 add_news_record(news_record_instance)를 이용한다.
        pass


    def get_document_by_userkey(self, user_key):
        # user_key를 인자로 받아서, 해당 유저가 조회한 뉴스한 뉴스의 document_id (최신순으로 정렬된) 리스트를 반환한다.
        pass


    def update_user_record(self, user_key, news_record_instance):
        '''
        사용자가 news를 열람하면 해당 정보를 user_status에 반영한다.
        사용자가 news를 열람하면 해당 정보를 user_record와 user_vector에 반영하여 파일에 업데이트한다.
        :param user_key: 새로운 뉴스를 열람한 사용자의 user_key
        :param news_record_instance: 사용자가 열람한 뉴스 정보를 담는 news_record 객체
        :return: None
        '''
        if self.is_user_record_empty():
            self.user_record = pd.DataFrame(data={news_record_instance.press: 1, news_record_instance.category: 1},
                                            index=[user_key])
            print("New user", user_key, "has been registered.")
            print("New press", news_record_instance.press, "has been registered.")
            print("New category", news_record_instance.category, "has been registered.")
        else:
            if self.is_new_user(user_key):  # 기존 레코드에 해당 user_key가 존재하지 않으면 새로 추가
                temp = pd.DataFrame([[0] * self.user_record.shape[1]], index=[user_key])
                temp.columns = self.user_record.columns
                self.user_record = self.user_record.append(temp)
                print("New user", user_key, "has been registered.")

            # user_key가 user_record에 존재한다는 조건하에
            if self.is_new_press(news_record_instance):
                # 해당 press가 존재하지 않다면, 0인 값으로 열을 추가하고, [user_key, press]에 +1
                self.user_record[news_record_instance.press] = 0
                self.user_record.loc[user_key, news_record_instance.press] += 1
                print("New press", news_record_instance.press, "has been registered.")
            else:  # 해당 press가 user_record column에 있다면 [user_key, press]에 +1
                self.user_record.loc[user_key, news_record_instance.press] += 1

            if self.is_new_category(news_record_instance):
                # 해당 category가 존재하지 않다면, 0인 값으로 열을 추가하고, [user_key, category]에 +1
                self.user_record[news_record_instance.category] = 0
                self.user_record.loc[user_key, news_record_instance.category] += 1
                print("New category", news_record_instance.category, "has been registered.")
            else:  # 해당 category가 user_record column에 있다면 [user_key, category]에 +1
                self.user_record.loc[user_key, news_record_instance.category] += 1

        self.regularize_user_record()
        # 작업 완료 후 파일 업데이트
        self.update_user_record_file()
        # 작업 완료 후 user_news_record_list 업데이트
        self.update_user_news_record_list(user_key, news_record_instance)


    def regularize_user_record(self):
        '''
        user_record를 정규화하여 user_vector에 반영한다.
        :return: 
        '''
        df_temp = self.user_record.copy()
        values_np = np.array(self.user_record.iloc[:, :], dtype=float)
        df_temp.iloc[:, :] = values_np / np.reshape(np.sum(values_np, axis=1), [values_np.shape[0], -1])
        self.user_vector = df_temp


    def get_n_similar_user(self, user_key, n):
        '''
        해당 user_key를 가진 사용자와 가장 유사한 뉴스 열람 패턴을 보이는 n명의 사용자를 반환한다.
        :param user_key: 특정 사용자의 user_key
        :param n: 찾고자하는 유사한 사용자의 수 n
        :return: 가장 유사한 n명의 사용자의 user_key를 원소로 갖는 list
        '''
        if self.is_new_user(user_key):
            print("User", user_key, "is unregistered user.")
            return None
        else:
            similarity_matrix = cosine_similarity(self.user_vector)
            user_index = self.user_vector.index.get_loc(user_key)
            similarity_vector = similarity_matrix[user_index, :]
            top_n_index = np.argsort(similarity_vector)[-2:-(2 + n):-1]
            top_n_user = self.user_vector.index[top_n_index]
            return list(top_n_user)


    def user_based_recommendation(self, user_key, n):
        '''
        가장 유사한 상위 n명의 유저가 조회한 news를 빈도수 순으로 정렬하고 그 중에서 상위 5개의 기사의 document_id를 반환한다.
        :param user_key: 찾고자하는 대상의 user_key, 즉 추천해줄 대상 (string)
        :param n: 상위 유저의 수 n (integer)
        :return: 상위 5개의 document_id를 원소로 갖는 리스트 (list)
        '''
        top_n_user = self.get_n_similar_user(user_key, n)  # n명의 가장 유사한 유저를 탐색
        recommendation_dic_ub = []
        if top_n_user == None:
            return None
        for user in top_n_user:
            document_list = self.get_document_by_userkey(user)
            for document_id in document_list:
                if document_id in recommendation_dic_ub:
                    recommendation_dic_ub[document_id] += 1
                else:
                    recommendation_dic_ub[document_id] = 1

        recommendation_list_ub = sorted(recommendation_dic_ub, key=lambda k: recommendation_dic_ub[k], reverse=True)
        return recommendation_list_ub[:5]  # 빈도수별로 count해서 상위 5개의 뉴스 기사 반환


    def print_user_record(self):
        '''
        user_record를 출력한다.
        :return: None
        '''
        if self.is_user_record_empty():
            print("There is no saved user record.")
        else:
            print("Printing", self.user_record.shape[0], "users record.")
            print("=" * 40)
            print(self.user_record)
            print("=" * 40)

    def print_user_vector(self):
        '''
        user_vector를 출력한다.
        :return: None
        '''
        if self.is_user_vector_empty():
            print("There is no saved user vector.")
        else:
            print("Printing", self.user_vector.shape[0], "users regularized record.")
            print("=" * 40)
            print(self.user_vector)
            print("=" * 40)