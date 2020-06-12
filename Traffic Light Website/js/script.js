$(()=>{
	formSwitch();
	enter();
});

enter = ()=>{
	$('.welcome-form button.btn').on('click',(e)=>{
		// e.preventDefault();
		// $('.welcome-form form').preventDefault();
		// window.location.replace('pages/home.html');
	});
}

formSwitch = ()=>{
	$('.welcome-form').on('click','button#regSwitch',()=>{
		$('.sForm#login').css('display','none');
		$('.sForm#register').css('display','block');
	});
	$('.welcome-form').on('click','button#logSwitch',()=>{
		$('.sForm#register').css('display','none');
		$('.sForm#login').css('display','block');
	});
}

validateForm = ()=>{

	var i = document.getElementById("loginEmail");
	var j = document.getElementById("loginPass");

	var status = true;

	
	if(i.value===""){
		i.className += " is-invalid";
		status = false;
	}
	else{
		i.classList.remove("is-invalid");
	}
	if(j.value===""){
		j.className += " is-invalid";
		status = false;
	}
	else{
		j.classList.remove("is-invalid");
	}
	return status;
}


validateFormReg = ()=>{
	var c = document.getElementById("regEmail");
	var e = document.getElementById("regPass");
	var f = document.getElementById("regPass2");

	var g = document.getElementById("register").style.display;

	var status = true;

	if(c.value===""){
		c.className += " is-invalid";
		status = false;
	}
	else{
		c.classList.remove("is-invalid");
	}
	if(e.value===""){
		e.className += " is-invalid";
		status = false;
	}
	else{
		e.classList.remove("is-invalid");
	}
	if(f.value===""){
		f.className += " is-invalid";
		status = false;
	}
	else{
		f.classList.remove("is-invalid");
	}
	if(e.value!=""&&f.value!=""&&e.value!=f.value){
		e.className += " is-invalid";
		f.className += " is-invalid";
		status = false;
	}
	else if(e.value==""||f.value==""){
		status = false;
	}
	else{
		status = true;
	}
	return status;	
}