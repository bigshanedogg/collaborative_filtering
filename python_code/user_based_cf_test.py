import user_info_class as um

################################################################
#news_record 객체 사용
news_info1 = {"document_id" : "987654321",
             "press" : "경향",
             "category" : "경제",
             "title" : "비트코인 떡락 가즈아!!",
             "request_time" : "2018-02-01 12:34:56"}

news_info2 = {"document_id" : "432156789",
             "press" : "중앙일보",
             "category" : "경제",
             "title" : "떡락 비트코인 가즈아!!",
             "request_time" : "2018-01-01 12:34:56"}

nr1 = um.news_record(**news_info1)
#nr1.print_news_record()
nr2 = um.news_record(**news_info2)
#nr2.print_news_record()
################################################################

################################################################
#user_status 객체 사용
user_info = {"user_key":"123ha123",
             "gender":"M",
             "birth_year":"1991",
             "location":"경기"}

user1 = um.user_status(**user_info)
user1.set_recommend_service("n")
#user1.print_user_status()
#user1.print_news_record()
user1.add_news_record(nr1)
#user1.print_news_record()
################################################################

################################################################
#user_information_manager 객체 사용
user1_key = "123ha123"
user2_key = "456ah456"
user3_key = "789ha789"
user4_key = "234ah234"
user5_key = "678ha678"

manager = um.user_information_manager("./temp.txt") #두고두고 쓸 파일이니 temp 말고 제대로된 이름으로 저장!
#user_key와 뉴스 열람 정보 등록 전 :
#manager.print_user_record()
#manager.print_user_vector()

#user_key와 뉴스 열람 정보 등록 후 :
manager.update_user_record(user1_key, nr1)
manager.update_user_record(user1_key, nr2)
manager.update_user_record(user2_key, nr1)
manager.update_user_record(user2_key, nr2)
manager.update_user_record(user4_key, nr1)
manager.update_user_record(user5_key, nr2)
manager.update_user_record(user3_key, nr1)
manager.update_user_record(user3_key, nr2)
manager.update_user_record(user4_key, nr1)
manager.update_user_record(user4_key, nr2)
manager.update_user_record(user5_key, nr1)
manager.print_user_record()
manager.print_user_vector()

#특정 유저와 가장 유사한 유저 찾기
#print(manager.get_n_similar_user(user4_key, 2))
#print(manager.user_based_recommendation(user4_key, 2))