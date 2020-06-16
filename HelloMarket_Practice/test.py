import re

params = {'삼성':'1','애플':'2','엘지':'3'}
print(params[].key)
model_x = ['팝니다','(충전기 포함)','♡전문매장♡','판매합니다','단품','헬로페이','가성비굿~!','[당일배송]','정상해지','스마트폰','판매','미개봉','완박스']
model ='아이폰6팝니다'
if model != None:
    for i in range(0,len(model_x)):
        model = model.replace(model_x[i],'')
    print(model)
 


con = 'CONTENT: 100프로 각각 직접 찍어 실사진으로만 판매하고 있어요   갤럭시s9 64 기가 입니다 무잔상 S급 입니다 사진 확인해주세요 정상해지된 공기계로 초기화도 완료해두었어요 유심만 끼워 사용 하심되요  확정기변  25%할인 모두 적용가능기기 입니다  최초통신사 lg(lg kt sk 다 사용가능) 최초통화일 2019.1.3 케이스 충전기 필름 드리고 청라내 배달가능  멀면 택배 퀵 가능   01020580201'
f_regex = re.compile('\d{3}\S+\d{4}\S+\d{4}|\d{3}\s+\d{4}\s+\d{4}|\d{11}')

regex = re.compile('\d{11}')


phone = re.search(f_regex, con)

print(phone)

phone = re.search(regex, con)
print(phone)