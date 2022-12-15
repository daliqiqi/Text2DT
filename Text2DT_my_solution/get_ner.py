import requests

url = "http://10.10.50.150:8014/general_ner/v2"

myobj={
    "text": "患者过去体质一般。无高血压；有糖尿病10余年，详见现病史；无心脏病；无肾病史；无肺结核；无病毒性肝炎；无其他传染病；食物、药物过敏无；无外伤史；无手术史，无输血史；无中毒史；无长期用药史；无可能成瘾药物。疫苗接种史不详。",
    "text_type":"既往史",
    "type":"ner",
    "model": "ACtreeRE",
    "search_type":"exact_search",
    "bio_type": "overlap"
}
x = requests.post(url, json = myobj)
print(x.text)