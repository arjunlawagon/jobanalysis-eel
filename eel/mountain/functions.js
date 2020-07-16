response = ""

function pythonlink(bau, prj) {
    alert("triggering python mainprocess")
	eel.mainprocess(bau,prj)(setresult)
}

function setresult(resp) {
	alert("response received from python : " + resp)
	response = resp
//	if response == "00"
    eel.dummy("dummy input parm")(makeAlert)
	eel.getStep("bau")(makeAlert)
}

function makeAlert(resp){
    alert("getStep response = " + resp)
}

function processResponse(func, resp){
    if func == "getStep"
}