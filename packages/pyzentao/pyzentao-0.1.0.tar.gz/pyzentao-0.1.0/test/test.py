# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2021-07-15
#


from pyzentao import Zentao


if "__main__" == __name__:
    zentao = Zentao({
        # zentao root url
        "url": "http://0.0.0.0:20080/zentao",
        "version": "15",

        # authentication
        "username": "admin",
        "password": "Lton2008@",
    })

    print(">" * 30)
    print(
        zentao.user_task(
            userID=1,
            type="finishedBy"
        )
    )
    print("<" * 30)

# end
