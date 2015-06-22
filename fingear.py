import cherrypy
import random

class gear(object):
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def index(self, m=None, ng1=None, ng2=None, inp2=None):
        # 將標準答案存入 answer session 對應區
        theanswer = random.randint(1, 100)
        thecount = 0
        # 將答案與計算次數變數存進 session 對應變數
        cherrypy.session['answer'] = theanswer
        cherrypy.session['count'] = thecount
        # 印出讓使用者輸入的超文件表單
        outstring = self.menuLink()
        outstring += '''<br />'''
        outstring += '''
    <!DOCTYPE html> 
    <html>
    <title>
    期末齒輪 -單人
    </title>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.0-20150301-090019/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">


    <form method=\"post\" action=\"dogear\">
        <legend>輸入條件</legend>

        齒數1:<br />
        <input type=\"text\" name=\"ng1\" value="10"><br />
        齒數2:<br />
        <input type=\"text\" name=\"ng2\" value="10"><br />
        模數:<br />
        <input type=\"text\" name=\"m\" value="10"><br />
        壓力角(>33時會有錯誤):<br />
        <input type=\"text\" name=\"inp2\" value="30"><br />
        <input type=\"submit\" value=\"畫圖!!\">
        <input type=\"reset\" value=\"重填\">
    </form>
    <hr>
    <!-- 以下在網頁內嵌 Brython 程式 -->
    <script type="text/python">
    from browser import document, alert

    def echo(ev):
        alert(document["zone"].value)

    # 將文件中名稱為 mybutton 的物件, 透過 click 事件與 echo 函式 bind 在一起
    document['mybutton'].bind('click',echo)
    </script>

    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    from math import *

    # 準備在 id="plotarea" 的 canvas 中繪圖
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")

    def create_line(x1, y1, x2, y2, width=3, fill="red"):
    ctx.beginPath()
    ctx.lineWidth = width
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.strokeStyle = fill
    ctx.stroke()

    # 導入數學函式後, 圓周率為 pi
    # deg 為角度轉為徑度的轉換因子
    deg = pi/180.

    # 以下分別為正齒輪繪圖與主 tkinter 畫布繪圖

    # 定義一個繪正齒輪的繪圖函式
    # midx 為齒輪圓心 x 座標
    # midy 為齒輪圓心 y 座標
    # rp 為節圓半徑, n 為齒數
    def gear(midx, midy, rp, n, 顏色):
    # 將角度轉換因子設為全域變數
    global deg
    # 齒輪漸開線分成 15 線段繪製
    imax = 15
    # 在輸入的畫布上繪製直線, 由圓心到節圓 y 軸頂點畫一直線
    create_line(midx, midy, midx, midy-rp)
    # 畫出 rp 圓, 畫圓函式尚未定義
    #create_oval(midx-rp, midy-rp, midx+rp, midy+rp, width=2)
    # a 為模數 (代表公制中齒的大小), 模數為節圓直徑(稱為節徑)除以齒數
    # 模數也就是齒冠大小
    a=2*rp/n
    # d 為齒根大小, 為模數的 1.157 或 1.25倍, 這裡採 1.25 倍
    d=2.5*rp/n
    # ra 為齒輪的外圍半徑
    ra=rp+a
    print("ra:", ra)
    # 畫出 ra 圓, 畫圓函式尚未定義
    #create_oval(midx-ra, midy-ra, midx+ra, midy+ra, width=1)
    # rb 則為齒輪的基圓半徑
    # 基圓為漸開線長齒之基準圓
    rb=rp*cos(20*deg)
    print("rp:", rp)
    print("rb:", rb)
    # 畫出 rb 圓 (基圓), 畫圓函式尚未定義
    #create_oval(midx-rb, midy-rb, midx+rb, midy+rb, width=1)
    # rd 為齒根圓半徑
    rd=rp-d
    # 當 rd 大於 rb 時
    print("rd:", rd)
    # 畫出 rd 圓 (齒根圓), 畫圓函式尚未定義
    #create_oval(midx-rd, midy-rd, midx+rd, midy+rd, width=1)
    # dr 則為基圓到齒頂圓半徑分成 imax 段後的每段半徑增量大小
    # 將圓弧分成 imax 段來繪製漸開線
    dr=(ra-rb)/imax
    # tan(20*deg)-20*deg 為漸開線函數
    sigma=pi/(2*n)+tan(20*deg)-20*deg
    for j in range(n):
        ang=-2.*j*pi/n+sigma
        ang2=2.*j*pi/n+sigma
        lxd=midx+rd*sin(ang2-2.*pi/n)
        lyd=midy-rd*cos(ang2-2.*pi/n)
        #for(i=0;i<=imax;i++):
        for i in range(imax+1):
            r=rb+i*dr
            theta=sqrt((r*r)/(rb*rb)-1.)
            alpha=theta-atan(theta)
            xpt=r*sin(alpha-ang)
            ypt=r*cos(alpha-ang)
            xd=rd*sin(-ang)
            yd=rd*cos(-ang)
            # i=0 時, 繪線起點由齒根圓上的點, 作為起點
            if(i==0):
                last_x = midx+xd
                last_y = midy-yd
            # 由左側齒根圓作為起點, 除第一點 (xd,yd) 齒根圓上的起點外, 其餘的 (xpt,ypt)則為漸開線上的分段點
            create_line((midx+xpt),(midy-ypt),(last_x),(last_y),fill=顏色)
            # 最後一點, 則為齒頂圓
            if(i==imax):
                lfx=midx+xpt
                lfy=midy-ypt
            last_x = midx+xpt
            last_y = midy-ypt
        # the line from last end of dedendum point to the recent
        # end of dedendum point
        # lxd 為齒根圓上的左側 x 座標, lyd 則為 y 座標
        # 下列為齒根圓上用來近似圓弧的直線
        create_line((lxd),(lyd),(midx+xd),(midy-yd),fill=顏色)
        #for(i=0;i<=imax;i++):
        for i in range(imax+1):
            r=rb+i*dr
            theta=sqrt((r*r)/(rb*rb)-1.)
            alpha=theta-atan(theta)
            xpt=r*sin(ang2-alpha)
            ypt=r*cos(ang2-alpha)
            xd=rd*sin(ang2)
            yd=rd*cos(ang2)
            # i=0 時, 繪線起點由齒根圓上的點, 作為起點
            if(i==0):
                last_x = midx+xd
                last_y = midy-yd
            # 由右側齒根圓作為起點, 除第一點 (xd,yd) 齒根圓上的起點外, 其餘的 (xpt,ypt)則為漸開線上的分段點
            create_line((midx+xpt),(midy-ypt),(last_x),(last_y),fill=顏色)
            # 最後一點, 則為齒頂圓
            if(i==imax):
                rfx=midx+xpt
                rfy=midy-ypt
            last_x = midx+xpt
            last_y = midy-ypt
        # lfx 為齒頂圓上的左側 x 座標, lfy 則為 y 座標
        # 下列為齒頂圓上用來近似圓弧的直線
        create_line(lfx,lfy,rfx,rfy,fill=顏色)

    gear(400,400,300,41,"blue")
    </script>
    <canvas id="plotarea" width="800" height="800"></canvas>
    </body>
    </html>
    '''

        return outstring
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def index2(self, m=None, ng1=None, ng2=None, ng3=None, ng4=None, inp2=None):
        # 將標準答案存入 answer session 對應區
        theanswer = random.randint(1, 100)
        thecount = 0
        # 將答案與計算次數變數存進 session 對應變數
        cherrypy.session['answer'] = theanswer
        cherrypy.session['count'] = thecount
        # 印出讓使用者輸入的超文件表單
        outstring = self.menuLink()
        outstring += '''<br />'''
        outstring += '''
    <!DOCTYPE html> 
    <html>
    <title>
    期末齒輪 -協同
    </title>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.0-20150301-090019/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">

    <form method=\"post\" action=\"dogears\">
        <legend>輸入條件</legend>

        齒數1:<br />
        <input type=\"text\" name=\"ng1\" value="10"><br />
        齒數2:<br />
        <input type=\"text\" name=\"ng2\" value="10"><br />
        齒數3:<br />
        <input type=\"text\" name=\"ng3\" value="10"><br />
        齒數4:<br />
        <input type=\"text\" name=\"ng4\" value="10"><br />
        模數:<br />
        <input type=\"text\" name=\"m\" value="10"><br />
        壓力角(>33時會有錯誤):<br />
        <input type=\"text\" name=\"inp2\" value="30"><br />
        <input type=\"submit\" value=\"畫圖!!\">
        <input type=\"reset\" value=\"重填\">
    </form>
    </body>
    </html>
    '''

        return outstring

    @cherrypy.expose
    def dogear(self, m=None, ng1=None, ng2=None, inp2=None):
        outString = ""
        outString += self.menuLink()
        outString += '''<br />'''
        outString +="藍色，齒數1:"+ng1
        outString += "<br />"
        outString +="黑色，齒數2:"+ng2
        outString += "<br />"
        outString +="模數:"+m
        outString += "<br />"
        outString +="壓力角:"+inp2
        outString += "<br />"
        outString += '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">

    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    from math import *
    # 請注意, 這裡導入位於 Lib/site-packages 目錄下的 spur.py 檔案
    import spur

    # 準備在 id="plotarea" 的 canvas 中繪圖
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")
    # 以下利用 spur.py 程式進行繪圖, 接下來的協同設計運算必須要配合使用者的需求進行設計運算與繪圖
    # 其中並將工作分配給其他組員建立類似 spur.py 的相關零件繪圖模組
    # midx, midy 為齒輪圓心座標, rp 為節圓半徑, n 為齒數, pa 為壓力角, color 為線的顏色
    # Gear(midx, midy, rp, n=20, pa=20, color="black"):
    # 模數決定齒的尺寸大小, 囓合齒輪組必須有相同的模數與壓力角
    # 壓力角 pa 單位為角度
    pa = '''+str(inp2)+'''

    # m 為模數
    m = '''+str(m)+'''

    # 齒輪齒數
    n_g1 = '''+str(ng1)+'''
    n_g2 = '''+str(ng2)+'''



    # 計算兩齒輪的節圓半徑
    rp_g1 = m*n_g1/2
    rp_g2 = m*n_g2/2


    # 繪圖齒輪的圓心座標,假設排列成水平, 表示各齒輪圓心 y 座標相同
    x_g1 = 100
    y_g1 = 200

    x_g2 = x_g1
    y_g2 = y_g1 - rp_g1 - rp_g2



    #齒輪嚙合的旋轉角
    # 將第1齒輪順時鐘轉 90 度
    th1 = 0

    # 將第2齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    th2 = pi-pi/n_g2

    # 將第3齒輪逆時鐘轉 90 度之後, 再往回轉第2齒輪定位帶動轉角, 然後再逆時鐘多轉一齒, 以便與第2齒輪進行囓合
    # 第1個 -pi/2 為將原先垂直的第3齒輪定位線逆時鐘旋轉 90 度
    # -pi/n_g3 則是第3齒與第2齒定位線重合後, 必須再逆時鐘多轉一齒的轉角, 以便進行囓合
    # (pi+pi/n_g2)*n_g2/n_g3 則是第2齒原定位線為順時鐘轉動 90 度, 
    # pi+pi/n_g2 為第2齒輪從順時鐘轉 90 度之後, 必須配合目前的標記線所作的齒輪 2 轉動角度, 要轉換到齒輪3 的轉動角度
    # 必須乘上兩齒輪齒數的比例, 若齒輪2 大, 則齒輪3 會轉動較快
    # 但是第2齒輪為了與第1齒輪囓合, 已經距離定位線, 多轉了 180 度, 再加上第2齒輪的一齒角度, 因為要帶動第3齒輪定位, 
    # 這個修正角度必須要再配合第2齒與第3齒的轉速比加以轉換成第3齒輪的轉角, 因此乘上 n_g2/n_g3




    # 使用 ctx.save() 與 ctx.restore() 以確保各齒輪以相對座標進行旋轉繪圖
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g1,y_g1)
    ctx.rotate(th1)
    # put it back
    ctx.translate(-x_g1,-y_g1)
    spur.Spur(ctx).Gear(x_g1,y_g1,rp_g1,n_g1, pa, "blue")
    ctx.restore()

    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g2,y_g2)
    # rotate to engage
    ctx.rotate(th2)
    # put it back
    ctx.translate(-x_g2,-y_g2)
    spur.Spur(ctx).Gear(x_g2,y_g2,rp_g2,n_g2, pa, "black")
    ctx.restore()

    # 假如第3齒也要進行囓合, 又該如何進行繪圖?



    </script>
    <canvas id="plotarea" width="2800" height="1200"></canvas>
    </body>
    </html>
    '''
        return outString


    @cherrypy.expose
    def dogears(self, m=None, ng1=None, ng2=None, ng3=None, ng4=None, inp2=None):
        outString = ""
        outString += self.menuLink()
        outString += '''<br />'''
        outString +="藍色，齒數1:"+ng1
        outString += "<br />"
        outString +="黑色，齒數2:"+ng2
        outString += "<br />"
        outString +="紅色，齒數3:"+ng3
        outString += "<br />"
        outString +="紫色，齒數4:"+ng4
        outString += "<br />"
        outString +="模數:"+m
        outString += "<br />"
        outString +="壓力角:"+inp2
        outString += "<br />"
        outString += '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">

    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    from math import *
    # 請注意, 這裡導入位於 Lib/site-packages 目錄下的 spur.py 檔案
    import spur

    # 準備在 id="plotarea" 的 canvas 中繪圖
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")
    # 以下利用 spur.py 程式進行繪圖, 接下來的協同設計運算必須要配合使用者的需求進行設計運算與繪圖
    # 其中並將工作分配給其他組員建立類似 spur.py 的相關零件繪圖模組
    # midx, midy 為齒輪圓心座標, rp 為節圓半徑, n 為齒數, pa 為壓力角, color 為線的顏色
    # Gear(midx, midy, rp, n=20, pa=20, color="black"):
    # 模數決定齒的尺寸大小, 囓合齒輪組必須有相同的模數與壓力角
    # 壓力角 pa 單位為角度
    pa = '''+str(inp2)+'''

    # m 為模數
    m = '''+str(m)+'''

    # 齒輪齒數
    n_g1 = '''+str(ng1)+'''
    n_g2 = '''+str(ng2)+'''
    n_g3 = '''+str(ng3)+'''
    n_g4 = '''+str(ng4)+'''



    # 計算兩齒輪的節圓半徑
    rp_g1 = m*n_g1/2
    rp_g2 = m*n_g2/2
    rp_g3 = m*n_g3/2
    rp_g4 = m*n_g4/2


    # 繪圖齒輪的圓心座標,假設排列成水平, 表示各齒輪圓心 y 座標相同
    x_g1 = 100
    y_g1 = 200

    x_g2 = x_g1
    y_g2 = y_g1 - rp_g1 - rp_g2

    x_g3 = x_g1 +rp_g1 +rp_g3
    y_g3 = y_g1

    x_g4 = x_g3
    y_g4 = y_g3 +rp_g3 +rp_g4


    #齒輪嚙合的旋轉角
    # 將第1齒輪順時鐘轉 90 度
    th1 = 0

    # 將第2齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    th2 = pi-pi/n_g2

    # 將第3齒輪逆時鐘轉 90 度之後, 再往回轉第2齒輪定位帶動轉角, 然後再逆時鐘多轉一齒, 以便與第2齒輪進行囓合
    # 第1個 -pi/2 為將原先垂直的第3齒輪定位線逆時鐘旋轉 90 度
    # -pi/n_g3 則是第3齒與第2齒定位線重合後, 必須再逆時鐘多轉一齒的轉角, 以便進行囓合
    # (pi+pi/n_g2)*n_g2/n_g3 則是第2齒原定位線為順時鐘轉動 90 度, 
    # pi+pi/n_g2 為第2齒輪從順時鐘轉 90 度之後, 必須配合目前的標記線所作的齒輪 2 轉動角度, 要轉換到齒輪3 的轉動角度
    # 必須乘上兩齒輪齒數的比例, 若齒輪2 大, 則齒輪3 會轉動較快
    # 但是第2齒輪為了與第1齒輪囓合, 已經距離定位線, 多轉了 180 度, 再加上第2齒輪的一齒角度, 因為要帶動第3齒輪定位, 
    # 這個修正角度必須要再配合第2齒與第3齒的轉速比加以轉換成第3齒輪的轉角, 因此乘上 n_g2/n_g3
    th3 = -pi/2 +pi/n_g3  +pi/2*(n_g1/n_g3)

    th4 = pi/n_g4 -(th3+pi)*(n_g3/n_g4)




    # 使用 ctx.save() 與 ctx.restore() 以確保各齒輪以相對座標進行旋轉繪圖
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g1,y_g1)
    ctx.rotate(th1)
    # put it back
    ctx.translate(-x_g1,-y_g1)
    spur.Spur(ctx).Gear(x_g1,y_g1,rp_g1,n_g1, pa, "blue")
    ctx.restore()

    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g2,y_g2)
    # rotate to engage
    ctx.rotate(th2)
    # put it back
    ctx.translate(-x_g2,-y_g2)
    spur.Spur(ctx).Gear(x_g2,y_g2,rp_g2,n_g2, pa, "black")
    ctx.restore()

    # 假如第3齒也要進行囓合, 又該如何進行繪圖?

    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g3,y_g3)
    # rotate to engage
    ctx.rotate(th3)
    # put it back
    ctx.translate(-x_g3,-y_g3)
    spur.Spur(ctx).Gear(x_g3,y_g3,rp_g3,n_g3, pa, "red")
    ctx.restore()

    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g4,y_g4)
    # rotate to engage
    ctx.rotate(th4)
    # put it back
    ctx.translate(-x_g4,-y_g4)
    spur.Spur(ctx).Gear(x_g4,y_g4,rp_g4,n_g4, pa, "purple")
    ctx.restore()


    </script>
    <canvas id="plotarea" width="2800" height="1200"></canvas>
    </body>
    </html>
    '''
        return outString


    @cherrypy.expose
    def menuLink(self):
        return '''
        <br />
        <a href=\"index\">期末齒輪 -單人(首頁)</a>
        <a href=\"index2">期末齒輪 -協同</a>
        <br />
        '''
