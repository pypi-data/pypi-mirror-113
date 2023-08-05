try:
    import improvmxpy as a
except ImportError:
    import os

    os.system("pip3 install improvmxpy")
else:
    pass
finally:
    import os
    import improvmxpy as a

    a.SetUp(os.getenv("testtoken"))
    try:
        a.Account().GetAccountDetail()
        print("Publishing to pypi")
        exit(0)
    except a.TokenError:
        print("TOKEN IS WRONG OR NOT FOUND")
        exit(1)
    except a.ServerError:
        print("SERVER ERROR COUNT THAT IT IS WORKING")
        exit(0)
