$(()=>{
	closeButton();
	createButton();
});

createButton = () =>{
	$("div.add-button > button").on("click", e=>{
		$(e.currentTarget).parent().siblings("div.create-new")
		.removeClass("hide")
		.css("display","block");
	});
}

closeButton = ()=>{
	$("div.create-new > div > button:nth-child(1)").on("click",e=>{
		$(e.currentTarget).parent().parent()
		.addClass("hide")
		.css("display","none");
	});
}