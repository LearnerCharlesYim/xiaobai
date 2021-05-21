function Banner() {
    this.bannerWidth = 798;
    this.bannerGroup = $('#banner-group');
    this.index = 1;
    this.leftArrow = $('.left-arrow');
    this.rightArrow = $('.right-arrow');
    this.bannerUI = $('#banner-ul');
    this.liList = this.bannerUI.children("li");
    this.bannerCount = this.liList.length;
    this.pageControl = $(".page-control");

}

Banner.prototype.initBanner = function(){
    var self = this;
    var firstBanner = self.liList.eq(0).clone();
    var lastBanner = self.liList.eq(self.bannerCount-1).clone();
    self.bannerUI.append(firstBanner);
    self.bannerUI.prepend(lastBanner);
    self.bannerUI.css({"width":self.bannerWidth*(self.bannerCount+2),"left":-self.bannerWidth});
};

Banner.prototype.initPageControl = function(){
    var self = this;
    for(let i=0;i<self.bannerCount;i++){
        var circle = $("<li></li>");
        self.pageControl.append(circle);
        if(i === 0){
            circle.addClass('active');
        }
    }
    self.pageControl.css({"width":self.bannerCount*12+8*2+16*(self.bannerCount-1)})


};

Banner.prototype.toggleArrow = function(isShow){
    var self = this;
    if(isShow){
        self.leftArrow.show();
        self.rightArrow.show();
    }else{
        self.leftArrow.hide();
        self.rightArrow.hide();
    }
};

Banner.prototype.animate = function(){
    var self = this;
    self.bannerUI.stop().animate({"left":-798*self.index},500);
    var index = self.index;
    if(index === 0){
        index = self.bannerCount-1;
    }else if(index === self.bannerCount+1){
        index = 0;
    }else{
        index = self.index - 1;
    }
    self.pageControl.children('li').eq(index).addClass("active").siblings().removeClass("active");
};


Banner.prototype.loop = function(){
    var self = this;
    self.timer = setInterval(function () {
        if (self.index >= self.bannerCount+1){
            self.bannerUI.css({"left":-self.bannerWidth});
            self.index = 2;
        }else{
            self.index += 1;
        }
        self.animate();
    },2000);
};

Banner.prototype.listenBannerHover = function(){
    var self = this;
    this.bannerGroup.hover(function () {
        // 第一个函数是，把鼠标移动到banner上会执行的函数
        clearInterval(self.timer);
        self.toggleArrow(true);
    },function () {
        // 第二个函数是，把鼠标从banner上移走会执行的函数
        self.loop();
        self.toggleArrow(false);
    })
};

Banner.prototype.listenPageControl = function(){
    var self = this;
    self.pageControl.children("li").each(function (index,obj) {
        $(obj).click(function () {
            self.index = index+1;
            self.animate();
        })
    })

};

Banner.prototype.listenArrowClick = function(){
    var self = this;
    self.leftArrow.click(function () {
        if(self.index === 0){
            self.bannerUI.css({"left":-self.bannerCount*self.bannerWidth});
            self.index = self.bannerCount - 1;
        }else{
            self.index--;
        }
        self.animate();
    });
    self.rightArrow.click(function () {
        if(self.index === self.bannerCount + 1){
            self.bannerUI.css({"left":-self.bannerWidth});
            self.index = 2;
        }else{
            self.index++;
        }
        self.animate();
    })
};


Banner.prototype.run = function () {
    this.initBanner();
    this.initPageControl();
    this.loop();
    this.listenBannerHover();
    this.listenArrowClick();
    this.listenPageControl();
};


$(function () {
    var banner = new Banner();
    banner.run();
});




// 用来处理导航条的
function FrontBase() {}


FrontBase.prototype.run = function () {
    var self = this;
    self.listenAuthBoxHover();
    self.handleNavStatus();
};

FrontBase.prototype.listenAuthBoxHover = function () {
    var authBox = $(".auth-box");
    var userMoreBox = $(".user-more-box");
    authBox.hover(function () {
        userMoreBox.show();
    },function () {
        userMoreBox.hide();
    });
};

$(function () {
    var frontBase = new FrontBase();
    frontBase.run();
});

FrontBase.prototype.handleNavStatus = function () {
    var url = window.location.href;
    var protocol = window.location.protocol;
    var host = window.location.host;

    var domain = protocol + '//' + host;
    var path = url.replace(domain,'');
    var navLis = $(".nav li");
    navLis.each(function (index,element) {
        // js => $(js对象)
        var li = $(element);
        var aTag = li.children("a");
        var href = aTag.attr("href");
        if(href === path){
            li.addClass("active");
            return false;
        }
    });
};


$(function () {
    layui.use(['layer'], function () {
        var $ = layui.jquery
            , layer = layui.layer;
        $('#pub-btn,#subres-btn').click(function () {
            layer.open({
                type: 2,
                title: '发布信息',
                shadeClose: true,
                shade: 0.4,
                area: ['600px', '500px'],
                content: ['/pub_offer/', 'no'], //iframe的url
            });
        });
    });
});



