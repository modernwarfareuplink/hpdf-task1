# premature optimisation is the root of all evil
import time
from flask import Flask,request,abort,redirect,url_for,jsonify,send_file,render_template,make_response
import requests,json


app=Flask(__name__)


@app.route('/')
def greet():
	return 'Hello World - Arun'
	

@app.route('/authors/')
def authors():
	#s=time.time()
	au=requests.get('https://jsonplaceholder.typicode.com/users')
	req=json.loads(au.text)
	authResp={}
	for i in req:
		id=i['id']
		name=i['name']
		#print type(id),type(name)
		authResp[id]=name
	#return jsonify(authResp)
	newdictkeys=authResp.keys()
	postResp={}
	for i in newdictkeys:
		postResp.setdefault(i,[])
	#return jsonify(authResp,postResp)
	po=requests.get('https://jsonplaceholder.typicode.com/posts')
	req=json.loads(po.text)
	for i in req:
		userid=i['userId']
		postid=i['id']
		postIds=postResp[userid]
		if postIds==None:
			continue
		#print postIds,postResp[userid] ###place matters
		postIds.append(postid)
		#print postIds,postResp[userid]
		postResp[userid]=postIds #array property must be noted
	iter=0
	for i in newdictkeys:
		postCheck=postResp[i]
		postCheck=list(set(postCheck))
		postCount=len(postCheck)
		postResp[i]=postCount
		iter+=1
	#return jsonify(authResp,postResp)
	resp={}
	for i in newdictkeys:
		respKey=authResp[i]
		respValue=postResp[i]
		resp[respKey]=respValue
	#t=time.time()
	#print t-s  //to check the time taken for returning a request
	#return jsonify(resp)
	return render_template('authPost.html',res=resp,authors=resp.keys())


@app.route('/setcookie/')
def setcookie():
	resp=make_response('cookies are set')
	resp.set_cookie('name','Arun')
	resp.set_cookie('age','21')
	return resp


@app.route('/getcookies/')
def getcookie():
	name=request.cookies.get('name')
	age=request.cookies.get('age')
	if (name or age) == None: #operator precedence
		print type(name)
		print type(age)
		return 'cookies missing'
	else:
		return name + ' is ' + age + ' yr old'
	

@app.route('/robots.txt/')
def deny():
	abort(403)
	return 'deny'


@app.route('/htm/')
@app.route('/html/')
def html(): 
	return render_template('welcome.html'),403


@app.route('/img/')
@app.route('/image/')
def image(): 
	return send_file('meghaAkashHigh.jpg',mimetype='image/gif')


@app.route('/input/',methods=['GET','POST'])
def input():
	if request.method=='GET':
		return render_template('input.html')
	elif request.method=='POST':
		log=request.form['log']
		if log=='':
			return render_template('input.html')
		print log
		return render_template('logged.html',log=log)

		
#easter egg	
@app.route('/love/')
def love():
	return redirect(url_for('image'))

		
@app.errorhandler(404)
def err(error):
	return "url mismatch, may be a typo"



if __name__ == '__main__':
	app.run(debug=True,port=8080)
