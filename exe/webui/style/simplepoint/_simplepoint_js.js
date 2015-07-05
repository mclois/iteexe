var myTheme = {
    init : function(){
		var ie_v = $exe.isIE();
		if (ie_v && ie_v<8) return false;
        setTimeout(function(){
            $(window).resize(function() {
                myTheme.reset();
            });
        },1000);
		var tit = $exe_i18n.menu+" ("+$exe_i18n.hide.toLowerCase()+")";
        var l = $('<p id="nav-toggler"><a href="#" onclick="myTheme.toggleMenu(this)" class="hide-nav" id="toggle-nav" title="'+tit+'"><span>'+$exe_i18n.menu+'</span></a></p>');
        $("#siteNav").before(l);
        var url = window.location.href;
        url = url.split("?");
        if (url.length>1){
            if (url[1].indexOf("nav=false")!=-1) {
                myTheme.hideMenu();
            }
        }
		// Enable keyboard
		document.onkeydown = myTheme.checkKey;
        // License icon
        $("#packageLicense").css("cursor","pointer").click(function(){
            window.open($("A",this).attr("href"));
        });
    },
	isLightboxOpen : function(){
		if (typeof($.prettyPhoto)!='undefined' && $(".pp_pic_holder").css("display")=="block") return true;
		return false;
	},
	checkKey : function(e){
		// if ($(window).width()<750) return false;
		// Links
		var p = $("#topPagination");
		var k = $("#toggle-nav").attr("class");
		var url;
		// Previous
		var prevURL = "";
		var prevLnk = $(".prev",p);
		if (prevLnk.length==1) prevURL = prevLnk.attr("href");
		// Previous
		var nextURL = "";
		var nextLnk = $(".next",p);
		if (nextLnk.length==1) nextURL = nextLnk.attr("href");		
		
		// Actions
		var x = e || window.event;
		if (x.keyCode=='38') {
			// up arrow
			url = "index.html";
			if (k=="show-nav") url += "?nav=false";
			window.location=url;
		} else if (x.keyCode=='40') {
			// down arrow
			var lis = $("#siteNav a");
			url = lis.eq(lis.length-1).attr("href");
			if (k=="show-nav") url += "?nav=false";
			window.location=url;
		} else if (x.keyCode=='37') {
			// left arrow
			if (prevURL!="" && !myTheme.isLightboxOpen()) window.location=prevURL;
		} else if (x.keyCode=='32' || x.keyCode=='39') {
			// space bar or right arrow
			if (nextURL!="" && !myTheme.isLightboxOpen()) window.location=nextURL;
		} else if (x.keyCode=='77') {
			// m
			if (k=="show-nav") myTheme.toggleMenu();
			else myTheme.hideMenu();
		}
		
	},
    hideMenu : function(){
        $("#siteNav").hide();
        $(document.body).addClass("no-nav");
        myTheme.params("add");
		var tit = $exe_i18n.menu+" ("+$exe_i18n.show.toLowerCase()+")";
        $("#toggle-nav").attr("class","show-nav").attr("title",tit);
    },
    toggleMenu : function(e){
        if (typeof(myTheme.isToggling)=='undefined') myTheme.isToggling = false;
        if (myTheme.isToggling) return false;
        
        var l = $("#toggle-nav");
        
        if (!e && $(window).width()<900 && l.css("display")!='none') return false; // No reset in mobile view
        if (!e) {
            var tit = $exe_i18n.menu+" ("+$exe_i18n.show.toLowerCase()+")";
            l.attr("class","show-nav").attr("title",tit); // Reset
        }
        
        myTheme.isToggling = true;
        
        if (l.attr("class")=='hide-nav') {  
			var tit = $exe_i18n.menu+" ("+$exe_i18n.show.toLowerCase()+")";
            l.attr("class","show-nav").attr("title",tit);
            $("#siteFooter").hide();
			$("#siteNav").slideUp(400,function(){
                $(document.body).addClass("no-nav");
                $("#siteFooter").show();
                myTheme.isToggling = false;
            }); 
            myTheme.params("add");
        } else {
            var tit = $exe_i18n.menu+" ("+$exe_i18n.hide.toLowerCase()+")";
			l.attr("class","hide-nav").attr("title",tit);
            $(document.body).removeClass("no-nav");
			$("#siteNav").slideDown(400,function(){
                myTheme.isToggling = false;
            });
            myTheme.params("delete");            
        }
        
    },
    param : function(e,act) {
        if (act=="add") {
            var ref = e.href;
            var con = "?";
            if (ref.indexOf(".html?")!=-1) con = "&";
            var param = "nav=false";
            if (ref.indexOf(param)==-1) {
                ref += con+param;
                e.href = ref;                    
            }            
        } else {
            // This will remove all params
            var ref = e.href;
            ref = ref.split("?");
            e.href = ref[0];
        }
    },
    params : function(act){
        $("A",".pagination").each(function(){
            myTheme.param(this,act);
        });
    },
    reset : function() {
        myTheme.toggleMenu();        
    }    
}

$(function(){
    var c = document.body.className;
    var f = document.getElementById("siteFooter");
    if (c.indexOf("exe-authoring-page")==0) {
        if (!f) $("BODY").append("<div id='siteFooter'></div>");
    } else {
        if (!f) $("#content").append("<div id='siteFooter'></div>");
        if (c=='exe-web-site js') {
            myTheme.init();
        }     
    }
});