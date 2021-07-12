import traceback
import pandas as pd

from WeiboUserScrapy import WeiboUserScrapy as WUS

class getLows:
    def __init__(self):
        self.userID_list = [] # 用户id列表
        self.run()

    def getuserID(self):
        """获取用户列表"""
        try:
            file_name = 'comment/hj/hebing.csv'
            df = pd.read_csv(file_name, header=0)
            userURL = df.values[:, 1]
            for user in userURL:
                #print(user)
                self.userID_list.append(user.split(r'/')[-1])

        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def run(self):
        self.getuserID()
        for userID in self.userID_list[0:]:
            WUS(user_id=int(userID), filter=0)


if __name__ == '__main__':
    getLows()
    print(0)