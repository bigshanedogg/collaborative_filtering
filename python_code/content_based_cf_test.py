import content_based_cf as cb

searcher = cb.news_searcher("temp2.txt") #두고두고 유지할 파일이니 파일 경로는 이쁘게!
searcher.add_new_document([1,2,3,4,5]) #1,2,3,4,5는 document_id 대신 테스트용으로 입력한 id

temp = searcher.get_similar_document(1,2) #특정 document_id가 주어졌을 때 이와 가장 유사한 document 반환 (content-based 추천)
print(temp)

search_query = "문재인 대통령 평창 북한"
temp2 = searcher.search_news_document(search_query, 1)
print(temp2)

search_query2 = "삼성전자 이재용 부회장"
temp3 = searcher.search_news_document(search_query2, 1)
print(temp3)

#print(searcher.dtm_index)
#print(searcher.dtm_list)