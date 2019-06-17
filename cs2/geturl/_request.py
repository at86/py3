# coding:utf-8
import os
import time

import demjson
import requests
import logging

import re
import wx


from pypac import PACSession, get_pac
from pypac.parser import PACFile

# atdo from url
# pac = get_pac(url='http://txp-01.tencent.com/proxy_ngn.pac?ip=192.168.72.1;192.168.88.1;192.168.56.1;192.168.1.102;&pc=watsenwang-NB1&ver=5.0.73.142')
# atdo from file
pac = PACFile(open('d:/tool/proxy_ngn.pac').read())
session = PACSession(pac)

# requests.sessions=session
# requests.Session()

# atdo this use no proxy
# r = requests.get('http://www.baidu.com')
# r = requests.get('http://10.240.138.145:8080/consume_progress_monitor.htm?topic=sng_hrtx_qd_call_session_report_ex_online&consumerGroup=t_sng_crm_b_sng_hrtx_qd_call_session_report_ex_online_cg_php_api_extcdr_push_001',timeout=2)

# atdo this use auto pac file like ie pac file
# r = session.get('http://10.240.138.145:8080/consume_progress_monitor.htm?topic=sng_hrtx_qd_call_session_report_ex_online&consumerGroup=t_sng_crm_b_sng_hrtx_qd_call_session_report_ex_online_cg_php_api_extcdr_push_001',timeout=2)
# print(r.status_code,r.text)

logging.basicConfig()

# response = requests.get('https://www.baidu.com')
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

# atdo this use proxy
# ip_address = 'web-proxy.tencent.com'
# ip_port = 8080
# ip_url_next = '://' + ip_address + ':' + str(ip_port)
# proxies = {'http': 'http' + ip_url_next, 'https': 'https' + ip_url_next}
# proxies = {}
# url = 'http://10.240.138.145:8080/consume_progress_monitor.htm?topic=sng_hrtx_qd_call_session_report_ex_online&consumerGroup=t_sng_crm_b_sng_hrtx_qd_call_session_report_ex_online_cg_php_api_extcdr_push_001'
# r = requests.get(url, headers=header, proxies=proxies, timeout=3)

# html = r.text
# print len(html), html.__len__()
# matchs = re.findall(r'value={.*}', html)
# if matchs.__len__() > 0:
#     # fstr =  matchs[0].encode("latin-1")
#     fstr = matchs[0]
#     # still: 'Unknown identifier', u'value'
#     # fstr =fstr[fstr.find('value='):]
#     fstr = fstr.replace('value=', '')
#     print fstr
#     obj = demjson.decode(fstr)
#     consumed = obj['consumed']
#     produced = obj['produced']
#     queues = obj['queues']
#     producedAll = 0
#     consumedAll = 0
#     fstr = ''
#     for i in range(0, consumed.__len__()):
#         producedAll += produced[i]
#         consumedAll += consumed[i]
#         a = produced[i] - consumed[i]
#         fstr += 'queueid-' + str(queues[i]) + ': 待消费数 ' + str(a) + '; 生产 ' + format(produced[i],',') + '; 消费 ' + format(consumed[i],',')+"\n"
#         print i
#     print fstr


class TabPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        # colors = ["red", "blue", "gray", "yellow", "green"]
        # self.SetBackgroundColour(random.choice(colors))

        # btn = wx.Button(self, label="Press Me"+str(random.randint(1,10)))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.tarea = wx.TextCtrl(self, -1, u'',
                                 style=(wx.TE_MULTILINE | wx.TE_RICH))
        # | wx.SUNKEN_BORDER
        # | wx.TE_NO_VSCROLL
        # | wx.AUTO_SCROLL | wx.TE_DONTWRAP
        # | wx.AUTO_SCROLL #atdo no this style
        self.tarea.SetInsertionPoint(0)
        self.tarea.Bind(wx.EVT_KEY_UP, self.OnSelectAll)

        sizer.Add(self.tarea,
                  1,  # make vertically stretchable
                  wx.EXPAND  # make horizontally stretchable
                  # | wx.ALL,  # and make border all around
                  )
        self.SetSizer(sizer)

    # 自定义 多行文本框  全选
    def OnSelectAll(self, event):
        if event.GetKeyCode() == 65 and event.ControlDown():
            self.tarea.SelectAll()


def run():
    try:

        app = wx.App()
        fframe = wx.Frame(parent=None, id=wx.ID_ANY, title='process of watsen', size=(880, 680))

        # panel = wx.Panel(fframe)
        # notebook = wx.Notebook(panel)
        notebook = wx.Notebook(fframe)
        # tabOne = TabPanel(notebook)
        # notebook.AddPage(tabOne, "Tab 1")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(notebook, 1, wx.EXPAND, 0)


        # panel.SetSizer(sizer2)

        def tabGetData(tab, url):
            # tab.tarea.ShowPosition(0)
            tab.tarea.Hide()
            tab.tarea.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False))
            tab.tarea.SetDefaultStyle(wx.TextAttr(wx.RED))
            # atdo in corp this proxy set ok
            # r = requests.get(url, headers=header, proxies=proxies, timeout=3)
            # r = requests.get(url, headers=header, timeout=3)
            r = session.get(url, headers=header, timeout=3)
            # print len(r.text), r.text.__len__()
            matchs = re.findall(r'value={.*}', r.text)
            tab.tarea.SetInsertionPoint(0)
            # tab.tarea.AppendText(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" =============\n")
            tab.tarea.WriteText(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " =============\n")
            tab.tarea.SetDefaultStyle(wx.TextAttr(wx.BLACK))
            if matchs.__len__() > 0:
                # fstr =  matchs[0].encode("latin-1")
                fstr = matchs[0]
                # still: 'Unknown identifier', u'value'
                # fstr =fstr[fstr.find('value='):]
                fstr = fstr.replace('value=', '')
                # print fstr
                data = demjson.decode(fstr)
                consumed = data['consumed']
                produced = data['produced']
                queues = data['queues']
                producedAll = 0
                consumedAll = 0
                fstr = ''
                for i in range(0, consumed.__len__()):
                    producedAll += produced[i]
                    consumedAll += consumed[i]
                    a = produced[i] - consumed[i]
                    fstr += 'queueid-' + str(queues[i]) + \
                            ': 待消费数 ' + str(a) + '; 生产 ' + \
                            format(produced[i], ',') + '; 消费 ' + \
                            format(consumed[i], ',') + "\n"
                fstr += '生产总数：' + format(producedAll, ',') + "\n"
                fstr += '消费总数：' + format(consumedAll, ',') + "\n"
                fstr += '待消费总数：' + format(producedAll - consumedAll, ',') + "\n\n"
                # print fstr
                # tab.tarea.SetLabelText(fstr)
                # tab.tarea.AppendText(fstr)
                tab.tarea.WriteText(fstr)
            else:
                # tab.tarea.AppendText(r.text)
                tab.tarea.WriteText(r.text)
            # tab.tarea.ShowPosition(tab.tarea.GetLastPosition())
            tab.tarea.ShowPosition(0)
            tab.tarea.Show()


        def newpageParse(event, url, label):
            btn = event.GetEventObject()
            tab = None
            if not hasattr(btn, 'fpage'):
                tab = TabPanel(notebook)
                # notebook.AddPage(new_tab, "Tab %s" % self.tab_num)
                notebook.AddPage(tab, label, select=True)
                # obj['fpage'] = notebook.GetSelection() #this will not as dynamic attr
                btn.fpage = notebook.GetSelection()
                btn.ftab = tab
                # print tab.tarea.IsMultiLine()
                tabGetData(tab, url)
            else:
                notebook.SetSelection(btn.fpage)
                tab = btn.ftab
                # atdo not this whole call, but apendText() in this call, and setPositon(0)
                # wx.FutureCall(1000,tabGetData,tab,url)
                # return
                tabGetData(tab, url)


        def tabUrl(url, label):
            btn2 = wx.Button(fframe, id=wx.ID_ANY, label=label, style=wx.WANTS_CHARS)
            # btn2.Bind(wx.EVT_BUTTON, self.btnClickNewProcess)
            #  lambda evt, mark=i : self.OnMenusClick(evt,mark)
            # btn_click = lambda evt, p : self.btnClickNewProcess(evt, p) # atdo can't do like this, pass lambda as event handler
            btn2.Bind(wx.EVT_BUTTON, lambda evt, url=url, label=label: newpageParse(evt, url, label))
            sizer1.Add(btn2, 1, wx.ALIGN_LEFT, 0)  # |wx.EXPAND


        # url = 'https://www.baidu.com'
        # r = requests.get(url, headers=header, proxies=proxies, timeout=3)
        # html = r.text
        # print html

        # fdir = os.path.split(os.path.realpath(__file__))[0]
        # urls = open()
        fdir = os.path.abspath(os.path.join(os.getcwd(), '../..'))
        ffile = os.path.abspath(os.path.join(fdir, './wx/watsen/urls.js'))
        urls = open(ffile).read()
        urls = urls[urls.find('['):]
        urls = demjson.decode(urls)

        for i in urls:
            url = i['url']
            # print url.find('consume_progress_monitor.htm')
            if url.find('consume_progress_monitor.htm') > -1:
                label = i['label']
                tabUrl(url, label)

        sizer.Add(sizer1)
        sizer.Add(sizer2, 1, wx.EXPAND, 0)
        fframe.SetSizer(sizer)
        fframe.Show()
        app.MainLoop()
        wx.Exit()

    except Exception as e:
        # print("fail of: %s" % ip_address)
        logging.error('3333.', exc_info=e)

    # import urllib2
    # response = urllib2.urlopen('http://www.baidu.com/')
    # html = response.read()
    # print html

run()
