import requests

url = 'http://h5api.m.tmall.com/h5/mtop.alibaba.review.list.for.new.pc.detail/1.0/'
header = {
    'Host': 'h5api.m.tmall.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://detail.tmall.com/',
    'Cookie': 'lid=%E4%B8%8D%E6%9B%BE%E7%9B%B8%E9%81%87%EF%BC%81005009; enc=pRzVNbKJtlbI64jSFbUWgtT7o4Sc33MR8aSrzlpxgmotibPpF8C6vFWV5HJ6GX4fNGc7a4sEV0WUVNBSuv2psA%3D%3D; cna=mQIBHOffplgCAbaVaT9zaaVG; _m_h5_tk=851e3b919fd195a562f991a99c0a28fe_1668964540019; _m_h5_tk_enc=5fce79b290449e5279503b2cb2ad0e49; isg=BMTEtLVye81ix8-BmszH6Q3HlkK23ehH9vl16N5lvA97CWXTB-0F18jvSSHRCiCf; l=eBIA3RTcTc-97V_NBO5CFurza77O1IR48kPzaNbMiInca6_G_U-wzNCU7S7M8dtfgtCe6eKrcdiaydF2JLUd0YNc13fREpZNpxJO.; tfstk=cq2fB9GNqEYb8n0y1qsP701_SGHhas1S2sgzcZNIqdWV2ZE-ksVeL2iTy5YSQcn5.; xlly_s=1; ariaDefaultTheme=default; ariaFixed=true; ariaReadtype=1; ariaoldFixedStatus=false; ariaStatus=false; sgcookie=E100J18jHwQOKbc4vnVQ7n6INLjIYXz%2Fdc48WJVAsxVDANwfUshenMHwP5S7kZKP%2BiWiTQh%2BBDmJnB0Ql0xhqDrvE5eB7x3i9De9bqKE3sghefE%3D; t=b5edb7fc90d3ebea799c9331aa306925; uc3=nk2=0XngSmsSKpj0wwOWSbsC3w%3D%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D&vt3=F8dCvjT9mZ6NMU%2BeDEA%3D&id2=UNJQ7f%2B6tY4GWw%3D%3D; tracknick=%5Cu4E0D%5Cu66FE%5Cu76F8%5Cu9047%5CuFF01005009; uc4=id4=0%40UgXXlMq5mQaj9pTkkCJPMLBsNguQ&nk4=0%4000HLUIMKZA3ZHQYXvMgRDFAsR%2BN3w5%2Fz6KHR; lgc=%5Cu4E0D%5Cu66FE%5Cu76F8%5Cu9047%5CuFF01005009; _tb_token_=efbef137eb357; cookie2=129e8c3184676cd64e21f1995a6b33a4; dnk=bla_ck_sugar; uc1=existShop=false&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&pas=0&cookie21=Vq8l%2BKCLjA%2Bl&cookie14=UoeyBrL4f2piAg%3D%3D&cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D; _l_g_=Ug%3D%3D; unb=3210834116; cookie1=AC5Vp9PTAXaEAtfGbDTJjBuDrCJDOuyuo6Qxie%2B%2Bgbc%3D; login=true; cookie17=UNJQ7f%2B6tY4GWw%3D%3D; _nk_=%5Cu4E0D%5Cu66FE%5Cu76F8%5Cu9047%5CuFF01005009; cancelledSubSites=empty; sg=962; csg=5832ada6',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers',
}
response = requests.get(url=url, headers=header)
print(response)
print(response.text)
