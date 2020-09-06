import requests
import json


def send_single_sms(apikey, code, mobile):
    '''
    发送单条短信
    :param apikey:
    :param code:
    :param mobile:
    :return:
    '''

    url = 'https://sms.yunpian.com/v2/sms/single_send.json'
    text = f'【程序猿的世界】您的验证码是{code}。如非本人操作，请忽略本短信'
    res = requests.post(url, data={
        'apikey': apikey,
        'mobile': mobile,
        'text': text
    })
    return json.loads(res.text)


if __name__ == '__main__':
    res = send_single_sms('d30347d2fb9248760b754137eb312e59', '123456', "17602151484")
    import json
    res_json = json.loads(res.text)
    code = res_json['code']
    msg = res_json['msg']
    if code == 0:
        print('发送成功')
        print(res.text)
    else:
        print('发送失败{}'.format(msg))