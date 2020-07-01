from googletrans import Translator


def get_i18_text(origin, src='en', dest='zh-cn'):
    gt = Translator(service_urls=['translate.google.cn'])
    res = gt.translate(origin, src=src, dest=dest)
    if isinstance(origin, str):
        res = res.text
    elif isinstance(origin, list):
        res = [i.text for i in res]

    return res
