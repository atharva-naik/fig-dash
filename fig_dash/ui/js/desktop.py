print("fig_dash::ui::js::desktop")
import jinja2

DesktopDockCSS = jinja2.Template(r"""
*,
html,
body {
	margin: 0;
	padding: 0;
	height: 100%;
	font-family: "San Francisco";
}

@font-face {
	font-family: "San Francisco";
  font-weight: 400;
  src: url("https://applesocial.s3.amazonaws.com/assets/styles/fonts/sanfrancisco/sanfranciscodisplay-regular-webfont.woff");
}

@font-face {
	font-family: "San Francisco";
  font-weight: 800;
  src: url("https://applesocial.s3.amazonaws.com/assets/styles/fonts/sanfrancisco/sanfranciscodisplay-bold-webfont.woff");
}

body {
	background: url({{ DESKTOP_BACKGROUND }});
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center center;
  background-attachment: fixed;  
}

/* Now all the acrylic layer is just only one class! */
.acrylic {
	/* Parent background + Gaussian blur */
	backdrop-filter: blur(5px);
	-webkit-backdrop-filter: blur(5px);
  
	/* Exclusion blend */
	background-blend-mode: exclusion;
  
	/* Color/tint overlay + Opacity */
	background: rgba(255, 255, 255, .6);
  
	/* Tiled noise texture */
	background-image: url(data:image/png;base64,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);
  }

.menu-bar {
	width: 100%;
	height: 24px;
	position: absolute;
	top: 0;
	left: 0;
	display: flex;
	align-items: center;
	justify-content: space-between;
	background: rgba(23, 23, 23, 0.8);
	box-shadow: 0px 0px 20px 5px #000;
}

.menu-bar .left {
	display: flex;
	align-items: center;
	justify-content: space-evenly;
	width: auto;
	margin-left: 20px;
}

.menu-bar .left .apple-logo {
	transform: scale(0.7);
}

.menu-bar .left .menus {
	height: 100%;
	display: flex;
	align-items: center;
	margin-left: 15px;
	color: rgba(255, 255, 255, 0.95);
	font-size: 12px;
  font-family: Be Vietnam Pro;
}

.menu-bar .left .active {
	font-weight: bold;
	color: #fff !important;
}

.menu-bar .right {
	display: flex;
	align-items: center;
	justify-content: space-evenly;
	width: 500px;
	margin-right: 20px;
}

.menu-bar .right .vol {
	transform: scale(0.6);
	margin-right: -10px;
}

.menu-bar .right .menu-time {
	height: 100%;
	width: auto;
	display: flex;
	align-items: center;
	justify-content: center;
	color: #fff;
  font-size: 14px;
  vertical-align: middle;
}

.menu-bar .right .menu-ico {
	height: 100%;
	width: 10px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.menu-bar .right .menu-ico .control-center {
	-webkit-filter: invert(100%);
	filter: invert(100%);
	transform: scale(0.5);
}

.menu-bar .right .menu-ico .siri {
	transform: scale(0.7);
	object-fit: fill;
}

.menu-bar .right .menu-ico i {
	display: contents;
	font-size: 16px;
	color: #fff;
	filter: drop-shadow(10px, 10px, 10px, white);
}

.dock {
	width: 100%;
	height: 60px;
	border-radius: 16px;
	display: flex;
	justify-content: center;
	position: absolute;
	bottom: 15px;
	left: 50%;
	transform: translateX(-50%);
}

.dock .dock-container {
	padding: 3px;
	width: auto;
	height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 16px;
	background: transparent;
	background: rgba(23, 23, 23, 0.7);
	backdrop-filter: blur(20px);
	border: 1px solid rgba(255, 255, 255, 0.3);
	position: fixed;
	perspective: 65px;
	box-shadow: 0px 0px 20px 5px #000;
}

.dock .dock-container::after{
	content: "";
	border-radius: 0px;
	position: absolute;
	left: 0px;
	bottom: -10px;
	width: 100%;
	height: 100%;
	backdrop-filter: blur(20px);
	background: rgba(23, 23, 23, 0.8);
	z-index: -1;
	transform-style: preserve-3d;
	transform: rotateX(25deg);
	
}

.dock .dock-container .li-bin {
	padding: 0px 6px 0px 6px;
    margin-left: 20px;
	border-left: 1.5px solid rgba(255, 255, 255, 0.4);
}

.dock .dock-container .li-2::after {
	position: absolute;
	width: 5px;
	height: 5px;
	border-radius: 50%;
	background: rgba(255, 255, 255, 0.5);
	content: "";
	bottom: 2px;
    transform: none;
}

.dock .dock-container li {
	list-style: none;
	display: flex;
	align-items: center;
	justify-content: center;
	width: 50px;
	height: 50px;
	vertical-align: bottom;
	transition: 0.2s;
	transform-origin: 50% 100%;
}

.dock .dock-container li:hover {
	margin: 0px 13px 0px 13px;
}

.dock .dock-container li .name {
	position: absolute;
	top: -70px;
	background: rgba(0, 0, 0, 0.5);
	color: rgba(255, 255, 255, 0.9);
	height: 10px;
	padding: 10px 15px;
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 5px;
	visibility: hidden;
}

.dock .dock-container li .name::after {
	content: "";
	position: absolute;
	bottom: -10px;
	width: 0;
	height: 0;
	backdrop-filter: blur(13px);
	-webkit-backdrop-filter: blur(13px);
	border-left: 10px solid transparent;
	border-right: 10px solid transparent;
	border-top: 10px solid rgba(0, 0, 0, 0.5);
}

.dock .dock-container li .ico {
	width: 100%;
	height: 100%;
	object-fit: cover;
	transition: 0.2s;
    transform: rotateX(-5deg);
	-webkit-box-reflect: below 2px -webkit-gradient(linear, left top, left bottom, from(transparent), color-stop(0.7, transparent), to(rgba(255, 255, 255, 0.5)));
        /* reflection is supported by webkit only */
	-webkit-transition: all 0.3s;
	-webkit-transform-origin: 50% 100%;
}

.dock .dock-container li .ico-bin {
	width: 94% !important;
	height: 94% !important;
	object-fit: cover;
	transition: 0.2s;
}

.dock .dock-container li .ico-bin:hover {
	margin-left: 10px;
}

.li-1:hover .name {
	visibility: visible !important;
}

.li-2:hover .name {
	visibility: visible !important;
}

.li-3:hover .name {
	visibility: visible !important;
}

.li-4:hover .name {
	visibility: visible !important;
}

.li-5:hover .name {
	visibility: visible !important;
}

.li-6:hover .name {
	visibility: visible !important;
}

.li-7:hover .name {
	visibility: visible !important;
}

.li-8:hover .name {
	visibility: visible !important;
}

.li-9:hover .name {
	visibility: visible !important;
}

.li-10:hover .name {
	visibility: visible !important;
}

.li-11:hover .name {
	visibility: visible !important;
}

.li-12:hover .name {
	visibility: visible !important;
}

.li-13:hover .name {
	visibility: visible !important;
}

.li-14:hover .name {
	visibility: visible !important;
}

.li-15:hover .name {
	visibility: visible !important;
}""")

DesktopHtml = jinja2.Template(r"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
        <!-- font awesome-->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css" integrity="sha512-KfkfwYDsLkIlwQp6LFnl8zNdLGxu9YAA1QvwINks4PhcElQSvqcyVLLD9aMhXd13uQjoXtEKNosOWaZqXgel0g==" crossorigin="anonymous" referrerpolicy="no-referrer" />
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <!-- Chrome, Firefox OS and Opera -->
        <meta name="theme-color" content="#57D5E3"/>
        <!-- Windows Phone -->
        <meta name="msapplication-navbutton-color" content="#57D5E3"/>
        <!-- iOS Safari -->
        <meta name="apple-mobile-web-app-status-bar-style" content="#57D5E3"/>
        <title>Desktop {{ DESKTOP_INDEX }} {{ DEKSTOP_NUM_NOTIFS }}</title>
        <!-- CSS / JS -->
        <style>
            {{ FILEVIEWER_CSS }}
            {{ DESKTOP_DOCK_CSS }}
            .file_container {
                border: none;
                outline: none;
                max-height: 650px;
                overflow-y: scroll; 
                font-family: 'Be Vietnam Pro';
            }
            .file_container::-webkit-scrollbar {
                display: none;
            }
        </style>
    </head>
    <body>
      <div class="menu-bar acrylic">
        <div class="left">
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Apple_logo_white.svg/1010px-Apple_logo_white.svg.png" class="apple-logo" alt="">
          <span class="menus active">Finder</span>
          <span class="menus">File</span>
          <span class="menus">Edit</span>
          <span class="menus">View</span>
          <span class="menus">Go</span>
          <span class="menus">Window</span>
          <span class="menus">Help</span>
        </div>
        <div class="right">
          <div class="menu-ico">
            <i class="fas fa-wifi"></i>
          </div>      
          <div class="menu-ico">
            <i class="fab fa-bluetooth-b"></i>
          </div>
          <div class="menu-ico">
            <i class="fas fa-battery-half"></i>
          </div>
          <div class="menu-ico">
            <span id="battery_level" style="font-size: 13px; vertical-align: middle; margin-top: 7px;">100</span>
          </div>
          <div class="menu-ico">
            <img src="https://freepngimg.com/download/united_states/76187-sound-information-united-business-states-address-email.png" alt="" class="vol">
          </div>
          <div class="menu-ico">
            <span id="battery_level" style="font-size: 13px; vertical-align: middle; margin-top: 7px;">100</span>
          </div>
          <div class="menu-ico">
            <i class="fas fa-search"></i>
          </div>
          <div class="menu-ico" onclick="triggerClipboard(this)">
            <i class="fa-regular fa-clipboard"></i>
          </div>
          <div class="menu-ico">
            <img src="https://eshop.macsales.com/blog/wp-content/uploads/2021/03/control-center-icon.png" alt="" class="control-center">
          </div>
          <div class="menu-ico">
            <img src="https://upload.wikimedia.org/wikipedia/en/8/8e/AppleSiriIcon2017.png" alt="" class="siri">
          </div>
      
          <div id="desktop-datetime" class="menu-time">
            <img id="calendar" style="height: 18px; margin-top: 3px; margin-bottom: 3px; margin-right: 5px;" src="{{ DESKTOP_CALENDAR_ICON }}"/><span id="date" style="vertical-align: middle; margin-top: 7px;"></span>&nbsp;&nbsp;<img id="timeOfDay" style="margin-bottom: 2px; margin-right: 5px;" src="{{ DESKTOP_CLOCK_TIME_OF_DAY }}" height="18"/><span id="time" style="vertical-align: middle; margin-top: 7px; float: left; width: 80px;"></span>
          </div>
        </div>
      </div>
      <br>
      <br>
      <div class="file_container">{{ EMBEDDED_FILE_VIEWER }}</div>
      <div class="dock">
        <div class="dock-container acrylic">
          <li class="li-1">
            <div class="name">Finder</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f70853981255cc36b3a37af_finder.png" alt="">
          </li>
          <li class="li-2">
            <div class="name">Siri</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f70853ff3bafbac60495771_siri.png" alt="">
          </li>
          <li class="li-3">
            <div class="name">LaunchPad</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f70853943597517f128b9b4_launchpad.png" alt="">
          </li>
          <li class="li-4">
            <div class="name">Contacts</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f70853743597518c528b9b3_contacts.png" alt="">
          </li>
          <li class="li-5">
            <div class="name">Notes</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f70853c849ec3735b52cef9_notes.png" alt="">
          </li>
          <li class="li-6">
            <div class="name">Reminders</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f70853d44d99641ce69afeb_reminders.png" alt="">
          </li>
          <li class="li-7">
            <div class="name">Photos</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f70853c55558a2e1192ee09_photos.png" alt="">
          </li>
          <li class="li-8">
            <div class="name">Messages</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f70853a55558a68e192ee08_messages.png" alt="">
          </li>
          <li class="li-9">
            <div class="name">FaceTime</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f708537f18e2cb27247c904_facetime.png" alt="">
          </li>
          <li class="li-10">
            <div class="name">Music</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f70853ba0782d6ff2aca6b3_music.png" alt="">
          </li>
          <li class="li-11">
            <div class="name">Podcasts</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f70853cc718ba9ede6888f9_podcasts.png" alt="">
          </li>
          <li class="li-12">
            <div class="name">TV</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f708540dd82638d7b8eda70_tv.png" alt="">
          </li>
          <li class="li-12">
            <div class="name">App Store</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f70853270b5e2ccfd795b49_appstore.png" alt="">
          </li>
          <li class="li-14">
            <div class="name">Safari</div>
            <img class="ico" src="https://uploads-ssl.webflow.com/5f7081c044fb7b3321ac260e/5f70853ddd826358438eda6d_safari.png" alt="">
          </li>
          <li class="li-bin li-15">
            <div class="name">Bin</div>
            <img class="ico ico-bin" src="https://findicons.com/files/icons/569/longhorn_objects/128/trash.png" alt="">
          </li>
      
        </div>
      </div>
      <script>{{ WEBCHANNEL_JS }}</script>
      <script>
        function triggerClipboard(el) {
          // console.log("triggering clipboard on click recieved by "+`${el}`);
          var rect = el.getBoundingClientRect();
          console.log(rect.top, rect.right, rect.bottom, rect.left);
          new QWebChannel(qt.webChannelTransport, function(channel) {
            channel.objects.desktopHandler.triggerClipboard(
              rect.top, rect.right, 
              rect.bottom, rect.left,
            );
          });
        }
        var icons = document.querySelectorAll(".ico");
        var length = icons.length;

        icons.forEach((item, index) => {
          item.addEventListener("mouseover", (e) => {
            focus(e.target, index);
          });
          item.addEventListener("mouseleave", (e) => {
            icons.forEach((item) => {
              item.style.transform = "scale(1)  translateY(0px)";
            });
          });
        });

        var focus = (elem, index) => {
          var previous = index - 1;
          var previous1 = index - 2;
          var next = index + 1;
          var next2 = index + 2;

          if (previous == -1) {
            console.log("first element");
            elem.style.transform = "scale(1.5)  translateY(-10px)";
          } else if (next == icons.length) {
            elem.style.transform = "scale(1.5)  translateY(-10px)";
            console.log("last element");
          } else {
            elem.style.transform = "scale(1.5)  translateY(-10px)";
            console.log(icons);
            icons[previous].style.transform = "scale(1.2) translateY(-6px)";
            icons[previous1].style.transform = "scale(1.1)";
            icons[next].style.transform = "scale(1.2) translateY(-6px)";
            icons[next2].style.transform = "scale(1.1)";
          }
        };
      </script>
    </body>
</html>""")