$(document).ready(function(){
	$("#menu ul li a img").hover(function(){
		// console.log($(this).attr('src').split('_')[0] + '.png');
		$(this).attr('src', $(this).attr('src').split('_')[0] + '.png');
	},function(){
		 // console.log($(this).attr('src').split('.png')[0] + '_b.png');
		$(this).attr('src', $(this).attr('src').split('.png')[0] + '_b.png');
	});

	$("#menu_right a").on('click', function(){
		switch($(this).attr('href')){
			case "#ajouterSujet":
				$("#ajoutAnnonce").show();
				$(this).attr("href", "#ajouterSujet_1");
				break;
			case "#ajouterSujet_1":
				$("#ajoutAnnonce").hide();
				$(this).attr("href", "#ajouterSujet");
				break;
		}
	});

	$(".title span").on('click', function(){
		$("#" + $(this).attr('rel')).hide();
		
	});
});