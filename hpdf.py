# premature optimisation is the root of all evil

from flask import Flask,request,abort,redirect,url_for,jsonify,send_file,render_template,make_response
import requests,json


app=Flask(__name__)


@app.route('/')
def greet():
	return 'Hello World - Arun'
	

@app.route('/authors/')
def authors():
	au=requests.get('https://jsonplaceholder.typicode.com/users')
	req=json.loads(au.text)
	authResp={}
	for i in req:
		id=i['id']
		name=i['name']
		authResp[id]=name
	newdictkeys=authResp.keys()
	postResp={}
	for i in newdictkeys:
		postResp.setdefault(i,[])
	po=requests.get('https://jsonplaceholder.typicode.com/posts')
	req=json.loads(po.text)
	for i in req:
		userid=i['userId']
		postid=i['id']
		postIds=postResp[userid]
		if postIds==None:
			continue
		postIds.append(postid)
		postResp[userid]=postIds
	iter=0
	for i in newdictkeys:
		postCheck=postResp[i]
		postCheck=list(set(postCheck))
		postCount=len(postCheck)
		postResp[i]=postCount
		iter+=1
	resp={}
	for i in newdictkeys:
		respKey=authResp[i]
		respValue=postResp[i]
		resp[respKey]=respValue
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
	if (name or age) == None: 
		print type(name)
		print type(age)
		return 'cookies missing'
	else:
		return name + ' is ' + age + ' old'
	

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
