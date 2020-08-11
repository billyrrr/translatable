import main

if __name__ == "__main__":
    import os

    path = './'
    files = os.listdir(path)

    files_txt = [i for i in files if i.endswith('.md') and not i.endswith('.zh.md')]
    for file_path in files_txt:
        with open(path+file_path, 'r') as f:
            ss = f.read()
            # import requests
            # res = requests.post(
            # 'http://127.0.0.1:8080/translate',
            # data=ss.encode('utf-8'), headers={
            #     'content-type': 'text/plain'
            # })
            # zh_s = res.content.decode('utf-8')
            zh_s = main.change(ss)
            # print(res.text)
            p = path + file_path[:-3] + '.zh.md'
            with open(p, 'w') as out:
                out.write(zh_s)
                out.close()
            f.close()

