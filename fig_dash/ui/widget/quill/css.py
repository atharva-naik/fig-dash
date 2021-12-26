#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import jinja2

QuillEmojiCSS = r'''#quill-editor{position:relative}.mention{color:#0366d6}.completions{background:#fff;border-radius:2px;box-shadow:2px 2px 2px rgba(0,0,0,.25);list-style:none}.completions,.completions>li{margin:0;padding:0}.completions>li>button{background:none;border:none;box-sizing:border-box;display:block;height:2em;margin:0;padding:.25em .5em;text-align:left;width:100%}.completions>li>button:hover{background:#ddd}.completions>li>button:focus{background:#ddd;outline:none}.completions>li>button>.matched{color:#000;font-weight:700}.completions>li>button>*{vertical-align:middle}.emoji_completions{background:#fff;border:1px solid rgba(0,0,0,.15);border-radius:3px;box-shadow:0 5px 10px rgba(0,0,0,.12);list-style:none;margin:0;padding:6px}.emoji_completions li{display:inline-block;margin:2px 0;padding:0}.emoji_completions li:not(:last-of-type){margin-right:3px}.emoji_completions>li>button{background:#efefef;border:none;border-radius:3px;box-sizing:border-box;display:block;margin:0;padding:3px 2px 6px;text-align:left;width:100%}.emoji_completions>li>button:hover{background:#2d9ee0;color:#fff}.emoji_completions>li>button:focus{background:#2d9ee0;color:#fff;outline:none}.emoji_completions>li>button.emoji-active{background:red;background:#2d9ee0;color:#fff;outline:none}.emoji_completions>li>button>.matched{font-weight:700}.emoji_completions>li>button>*,.ico{vertical-align:middle}.ico{font-size:18px;line-height:0;margin-right:5px}#emoji-palette{border:1px solid rgba(0,0,0,.15);border-radius:3px;box-shadow:0 5px 10px rgba(0,0,0,.12);max-width:250px;position:absolute;z-index:999}.bem{cursor:pointer;display:inline-block;font-size:24px;margin:2px;text-align:center;width:34px}#tab-filters{margin:20px auto 0;width:210px}.emoji-tab{cursor:pointer;display:inline-table;height:100%;min-height:30px;text-align:center;width:30px}#tab-toolbar{background-color:#f7f7f7;border-bottom:1px solid rgba(0,0,0,.15);padding:4px 4px 0}#tab-toolbar ul{margin:0;padding:0}#tab-toolbar .active{border-bottom:3px solid #2ab27b}#tab-panel{background:#fff;display:flex;flex-wrap:wrap;justify-content:center;max-height:220px;overflow-y:scroll;padding:2px}#quill-editor x-contain,contain{background:#fb8;display:block}#quill-editor table{border-collapse:collapse;width:100%}#quill-editor table td{border:1px solid #000;height:25px;padding:5px}.ql-picker.ql-table .ql-picker-label:before,button.ql-table:after{content:"TABLE"}button.ql-contain:after{content:"WRAP"}button.ql-table[value=append-row]:after{content:"ROWS+"}button.ql-table[value=append-col]:after{content:"COLS+"}.ql-contain,.ql-table{margin-right:-15px;width:auto!important}#emoji-close-div{height:100%;left:0;position:fixed;top:0;width:100%}.textarea-emoji-control{height:25px;right:4px;top:10px;width:25px}#textarea-emoji{border:1px solid #66afe9;border:1px solid rgba(0,0,0,.15);border-radius:3px;box-shadow:0 5px 10px rgba(0,0,0,.12);max-width:250px;position:absolute;right:0;z-index:999}.ql-editor{padding-right:26px}.i-activity{background:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="25px" height="25px" viewBox="0 0 40 40"><g fill="none" fill-rule="evenodd"><g fill="%236F6D70"><g transform="translate(7.500000, 7.500000)"><path stroke="%236F6D70" d="M18.02 1.36c5.92 3.02 8.28 10.26 5.26 16.18-2.12 4.17-6.35 6.57-10.73 6.57-1.83 0-3.7-.4-5.45-1.3-5.9-3-8.27-10.22-5.25-16.2C3.97 2.5 8.2.1 12.57.1c1.84 0 3.7.42 5.45 1.3zm4.7 11.44c.1-1.3-.06-2.6-.47-3.87-.13-.38-.27-.75-.43-1.1l-3.42-1.6-1.57-3.4c-.62-.3-1.27-.5-1.92-.68-.7-.18-1.5-.27-2.3-.27-.4 0-.8.02-1.2.06L8.9 4.74l-3.74.43c-.63.68-1.16 1.45-1.6 2.28-.42.84-.72 1.72-.9 2.63l1.84 3.3-.74 3.68c.3.56.66 1.08 1.1 1.58.76.94 1.7 1.7 2.8 2.32l3.7-.74 3.26 1.84c1.13-.23 2.23-.65 3.24-1.26.6-.35 1.2-.77 1.7-1.24l.44-3.74 2.78-2.55.05-.47z" stroke-linecap="round" stroke-linejoin="round"/><polygon points="10.6158689 8.50666885 8.42649168 12.8046921 11.836847 16.2129328 16.1342124 14.0235556 15.3793892 9.26144504"/></g></g></g></svg>')}.i-activity,.i-flags{content:"";height:25px;margin:auto;width:25px}.i-flags{background:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="25px" height="25px" viewBox="0 0 40 40"><g fill="none" fill-rule="evenodd"><g fill="%236F6D70" fill-rule="nonzero"><g transform="translate(9.500000, 8.000000)"><path d="M.5 3.13V23.5c0 .83.68 1.5 1.5 1.5.84 0 1.5-.67 1.5-1.5V3.14c0-.83-.66-1.5-1.5-1.5-.82 0-1.5.67-1.5 1.5z"/><path d="M3.5 11.54c.7-.16 1.44-.22 2.25-.17 1.38.07 2.48.3 5.23 1.04l.55.2c3.02.8 4.77 1 5.96.67v-7.9c-1.7.33-3.8-.07-7.1-1-3.9-1.1-5.7-1.3-6.9-.5v7.7zm7.68-10.1c4.1 1.15 5.7 1.3 6.98.44 1-.66 2.33.05 2.33 1.25v11c0 .5-.3 1-.7 1.26-2.2 1.4-4.6 1.2-9.1 0l-.56-.16c-4.54-1.2-6.15-1.3-7.05-.2-.9 1.06-2.65.42-2.65-.98v-11c0-.4.2-.8.5-1.1C3.4-.24 5.75-.1 11.2 1.4z"/></g></g></g></svg>')}.i-food{background:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="25px" height="25px" viewBox="0 0 40 40"><g fill="none" fill-rule="evenodd"><g fill="%236F6D70"><path fill-rule="nonzero" d="M9.57 28.2c0 .28.22.5.5.5h19.2c.27 0 .5-.22.5-.5v-4.4H9.57v4.4zm23.2-3.06v3.07c0 1.95-1.57 3.5-3.5 3.5h-19.2c-1.93 0-3.5-1.55-3.5-3.5V25c.46.15.96.24 1.47.24h23.78c.33 0 .64-.04.94-.1z"/><path fill-rule="nonzero" d="M6.57 18.2v-3.45c0-3.56 2.9-6.45 6.45-6.45h13.3c3.55 0 6.44 2.9 6.44 6.45v3.45H6.56zm3-1.83h3.6l.4.86c.23.5.73.83 1.3.83.56 0 1.06-.33 1.3-.83l.4-.86h13.2v-1.62c0-1.9-1.56-3.45-3.45-3.45h-13.3c-1.9 0-3.45 1.55-3.45 3.45v1.62z"/><path fill-rule="nonzero" d="M13.23 16.37l.4.86c.24.5.74.83 1.3.83.57 0 1.07-.33 1.3-.83l.4-.86H31.9c2.44 0 4.43 1.98 4.43 4.43 0 2.45-1.98 4.44-4.44 4.44H8.1c-2.44 0-4.43-2-4.43-4.44 0-2.45 1.98-4.43 4.44-4.43h5.14zm-5.12 3c-.8 0-1.42.64-1.42 1.43 0 .8.64 1.44 1.44 1.44h23.8c.8 0 1.43-.64 1.43-1.44 0-.8-.64-1.43-1.44-1.43H18.4c-.83 1.04-2.1 1.7-3.5 1.7-1.37 0-2.65-.66-3.47-1.7H8.1z"/><circle cx="14.6682646" cy="13.75" r="1"/><circle cx="24.6682646" cy="13.75" r="1"/><circle cx="19.6682646" cy="13.75" r="1"/></g></g></svg>')}.i-food,.i-nature{content:"";height:25px;margin:auto;width:25px}.i-nature{background:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="25px" height="25px" viewBox="0 0 40 40"><g fill="none" fill-rule="evenodd"><g fill="%236F6D70" fill-rule="nonzero"><path d="M15.96 18.26L30.86 32c.5.46 1.3.43 1.77-.08.46-.5.43-1.3-.08-1.76l-14.9-13.74c-.5-.46-1.3-.43-1.76.08-.5.5-.5 1.3 0 1.76z"/><path d="M18.17 21.28c-.7-.06-1.3.45-1.35 1.14-.06.7.45 1.3 1.13 1.35l4.96.43c.9.07 1.5-.66 1.4-1.47l-1-5.6c-.1-.7-.74-1.14-1.42-1.02-.67.2-1.12.8-1 1.5l.7 4-3.32-.3z"/><path d="M28.48 28.95c-.38.17-1 .4-1.85.64-2.92.7-6 .9-8.95-.2-5.98-2.17-9.8-8.5-10.54-19.9l-.1-1.4 1.38-.2c14.45-2.08 23.4 7.4 21.33 19.85l-1.9-.3.63 1.43zM10.24 10.77C11.12 20.14 14.2 25 18.7 26.6c2.27.83 4.76.74 7.14.1.4-.12.76-.23 1.07-.35 1.2-9.6-5.4-16.57-16.6-15.58z"/></g></g></svg>')}.i-objects{background:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="25px" height="25px" viewBox="0 0 40 40"><g fill="none" fill-rule="evenodd"><g fill="%236F6D70" fill-rule="nonzero"><path d="M11.04 16.7c0-4.85 4.02-8.76 8.96-8.76 4.94 0 8.96 3.9 8.96 8.76 0 2.54-1.12 4.9-3 6.54v1.87c0 1.28-1.02 2.27-2.26 2.27h-7.37c-1.23 0-2.25-1-2.25-2.22V23.3c-1.9-1.65-3.04-4-3.04-6.58zm11.9 5.82c0-.48.24-.93.63-1.22 1.5-1.08 2.4-2.77 2.4-4.6 0-3.17-2.67-5.76-5.97-5.76s-5.96 2.6-5.96 5.76c0 1.84.9 3.54 2.42 4.62.4.28.62.74.62 1.22v1.8h5.87V22.5z"/><path d="M21.76 28.78c-.22.05-.42.1-.62.13-.5.1-.9.2-1.1.2-.24 0-.62-.04-1.08-.12l-.74-.15-.08-.02v-2.93c0-.83-.68-1.5-1.5-1.5-.83 0-1.5.67-1.5 1.5v4.1c0 .68.44 1.27 1.1 1.45l.38.1.94.23c.3.1.6.15.87.2.62.1 1.16.17 1.6.17.47 0 1.03-.1 1.7-.2l.7-.17.95-.22c.18-.03.32-.1.4-.1.64-.2 1.08-.76 1.08-1.43v-4.1c0-.83-.67-1.5-1.5-1.5-.82 0-1.5.67-1.5 1.5v2.9c-.03 0-.07 0-.1.02z"/></g></g></svg>')}.i-objects,.i-people{content:"";height:25px;margin:auto;width:25px}.i-people{background:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="25px" height="25px" viewBox="0 0 40 40"><g fill="none" fill-rule="evenodd"><g fill="%236F6D70"><path fill-rule="nonzero" d="M20 34c-7.73 0-14-6.27-14-14S12.27 6 20 6s14 6.27 14 14-6.27 14-14 14zm0-3c6.08 0 11-4.92 11-11S26.08 9 20 9 9 13.92 9 20s4.92 11 11 11z"/><circle cx="15.3474348" cy="16.7705459" r="2.34743481"/><circle cx="24.4703784" cy="16.7705459" r="2.34743481"/><path d="M20 27.9c2.7 0 4.88-2.18 4.88-4.88 0-2.7-9.76-2.7-9.76 0S17.3 27.9 20 27.9z"/></g></g></svg>')}.i-symbols{background:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="25px" height="25px" viewBox="0 0 40 40"><g fill="none" fill-rule="evenodd"><g fill="%236F6D70" fill-rule="nonzero"><path d="M15.37 7.95c-4.48 0-8.06 3.9-8.06 8.64 0 3.5 2.2 6.9 5.8 10.3 1.2 1.1 2.5 2.2 3.9 3.1.84.6 1.5 1 1.98 1.3l.27.15.8.5 1.1-.6c.5-.27 1.18-.7 2-1.25 1.34-.9 2.66-1.9 3.9-3 3.57-3.28 5.75-6.8 5.75-10.6 0-4.74-3.6-8.65-8.1-8.65v3.3c2.6 0 4.76 2.4 4.76 5.35 0 2.65-1.72 5.43-4.7 8.13-1.1 1-2.27 1.9-3.5 2.7-.43.3-.83.54-1.17.74-.35-.2-.76-.5-1.2-.83-1.24-.87-2.4-1.83-3.54-2.87-2.95-2.76-4.7-5.5-4.7-7.9 0-2.98 2.2-5.35 4.78-5.35 1.3 0 2.5.6 3.4 1.6L20 14.3l1.25-1.43c.9-1.03 2.1-1.6 3.38-1.6v-3.3c-1.68 0-3.3.56-4.63 1.57-1.34-1-2.95-1.57-4.63-1.57z"/></g></g></svg>')}.i-symbols,.i-travel{content:"";height:25px;margin:auto;width:25px}.i-travel{background:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="25px" height="25px" viewBox="0 0 40 40"><g fill="none" fill-rule="evenodd"><g fill="%236F6D70" fill-rule="nonzero"><path d="M25.46 11.2s-2.67 2.58-3.94 3.95l-10.6-2.13c-.12-.02-.25.04-.3.15l-.8 1.6c-.07.13 0 .3.12.37l7.75 3.88L13.4 24c-.5-.16-1.1-.33-1.66-.3-.3 0-.6.06-.85.25-.3.2-.4.5-.4.9s.1.74.3.98l3.2 3.23c.3.23.7.34 1 .34.4 0 .7-.13.9-.37.2-.23.24-.53.25-.84 0-.6-.15-1.2-.3-1.7l4.97-4.3 3.9 7.76c.06.13.23.2.36.12l1.6-.8c.13-.07.2-.2.17-.3l-2.12-10.6c1.4-1.28 3.95-3.95 3.96-3.96.86-.88 1.4-1.93 1.4-2.87 0-.5-.17-1-.5-1.33-.37-.36-.87-.5-1.38-.5-.95 0-2 .52-2.88 1.4zm2.87-4.4c1.28 0 2.54.44 3.5 1.4.93.93 1.38 2.2 1.38 3.47 0 1.8-.8 3.54-2.2 4.94-.4.5-1.7 1.8-2.8 2.9l1.8 9c.3 1.5-.4 2.9-1.7 3.6l-1.62.8c-1.62.8-3.6.1-4.36-1.4L20 27.1l-.7.6v.62c-.03.92-.28 1.8-.92 2.6-.8 1-1.98 1.5-3.22 1.5-1.03 0-2.12-.37-2.96-1.1l-.16-.14-3.22-3.22-.1-.12c-.75-.83-1.12-1.9-1.12-3 0-1.24.5-2.43 1.48-3.22.8-.6 1.68-.9 2.62-.9h.62l.6-.7-4.27-2.1c-1.65-.8-2.33-2.8-1.52-4.4l.8-1.64c.67-1.3 2.14-2.02 3.57-1.73l9 1.8 1.36-1.33 1.5-1.48c1.42-1.4 3.17-2.27 4.97-2.27z"/></g></g></svg>')}.button-emoji{margin-bottom:-5px}.ql-emojiblot{display:inline-block;vertical-align:text-top}.ap{background-image:url({{ EMOJI_IMAGE }});background-repeat:no-repeat;background-size:820px;box-sizing:border-box;display:inline-flex;font-size:20px;height:20px;line-height:1;margin-top:-3px;overflow:hidden;text-indent:-999px;width:20px}.ap-copyright{background-position:0 0}.ap-registered{background-position:0 -20px}.ap-bangbang{background-position:0 -40px}.ap-interrobang{background-position:0 -60px}.ap-tm{background-position:0 -80px}.ap-information_source{background-position:0 -100px}.ap-left_right_arrow{background-position:0 -120px}.ap-arrow_up_down{background-position:0 -140px}.ap-arrow_upper_left{background-position:0 -160px}.ap-arrow_upper_right{background-position:0 -180px}.ap-arrow_lower_right{background-position:0 -200px}.ap-arrow_lower_left{background-position:0 -220px}.ap-leftwards_arrow_with_hook{background-position:0 -240px}.ap-arrow_right_hook{background-position:0 -260px}.ap-watch{background-position:0 -280px}.ap-hourglass{background-position:0 -300px}.ap-keyboard{background-position:0 -320px}.ap-fast_forward{background-position:0 -360px}.ap-rewind{background-position:0 -380px}.ap-arrow_double_up{background-position:0 -400px}.ap-arrow_double_down{background-position:0 -420px}.ap-black_right_pointing_double_triangle_with_vertical_bar{background-position:0 -440px}.ap-black_left_pointing_double_triangle_with_vertical_bar{background-position:0 -460px}.ap-black_right_pointing_triangle_with_double_vertical_bar{background-position:0 -480px}.ap-alarm_clock{background-position:0 -500px}.ap-stopwatch{background-position:0 -520px}.ap-timer_clock{background-position:0 -540px}.ap-hourglass_flowing_sand{background-position:0 -560px}.ap-double_vertical_bar{background-position:0 -580px}.ap-black_square_for_stop{background-position:0 -600px}.ap-black_circle_for_record{background-position:0 -620px}.ap-m{background-position:0 -640px}.ap-black_small_square{background-position:0 -660px}.ap-white_small_square{background-position:0 -680px}.ap-arrow_forward{background-position:0 -700px}.ap-arrow_backward{background-position:0 -720px}.ap-white_medium_square{background-position:0 -740px}.ap-black_medium_square{background-position:0 -760px}.ap-white_medium_small_square{background-position:0 -780px}.ap-black_medium_small_square{background-position:0 -800px}.ap-sunny{background-position:-20px 0}.ap-cloud{background-position:-20px -20px}.ap-umbrella{background-position:-20px -40px}.ap-snowman{background-position:-20px -60px}.ap-comet{background-position:-20px -80px}.ap-phone,.ap-telephone{background-position:-20px -100px}.ap-ballot_box_with_check{background-position:-20px -120px}.ap-umbrella_with_rain_drops{background-position:-20px -140px}.ap-coffee{background-position:-20px -160px}.ap-shamrock{background-position:-20px -180px}.ap-point_up{background-position:-20px -200px}.ap-skull_and_crossbones{background-position:-20px -320px}.ap-radioactive_sign{background-position:-20px -340px}.ap-biohazard_sign{background-position:-20px -360px}.ap-orthodox_cross{background-position:-20px -380px}.ap-star_and_crescent{background-position:-20px -400px}.ap-peace_symbol{background-position:-20px -420px}.ap-yin_yang{background-position:-20px -440px}.ap-wheel_of_dharma{background-position:-20px -460px}.ap-white_frowning_face{background-position:-20px -480px}.ap-relaxed{background-position:-20px -500px}.ap-aries{background-position:-20px -520px}.ap-taurus{background-position:-20px -540px}.ap-gemini{background-position:-20px -560px}.ap-cancer{background-position:-20px -580px}.ap-leo{background-position:-20px -600px}.ap-virgo{background-position:-20px -620px}.ap-libra{background-position:-20px -640px}.ap-scorpius{background-position:-20px -660px}.ap-sagittarius{background-position:-20px -680px}.ap-capricorn{background-position:-20px -700px}.ap-aquarius{background-position:-20px -720px}.ap-pisces{background-position:-20px -740px}.ap-spades{background-position:-20px -760px}.ap-clubs{background-position:-20px -780px}.ap-hearts{background-position:-20px -800px}.ap-diamonds{background-position:-40px 0}.ap-hotsprings{background-position:-40px -20px}.ap-recycle{background-position:-40px -40px}.ap-wheelchair{background-position:-40px -60px}.ap-hammer_and_pick{background-position:-40px -80px}.ap-anchor{background-position:-40px -100px}.ap-crossed_swords{background-position:-40px -120px}.ap-scales{background-position:-40px -140px}.ap-alembic{background-position:-40px -160px}.ap-gear{background-position:-40px -180px}.ap-atom_symbol{background-position:-40px -200px}.ap-fleur_de_lis{background-position:-40px -220px}.ap-warning{background-position:-40px -240px}.ap-zap{background-position:-40px -260px}.ap-white_circle{background-position:-40px -280px}.ap-black_circle{background-position:-40px -300px}.ap-coffin{background-position:-40px -320px}.ap-funeral_urn{background-position:-40px -340px}.ap-soccer{background-position:-40px -360px}.ap-baseball{background-position:-40px -380px}.ap-snowman_without_snow{background-position:-40px -400px}.ap-partly_sunny{background-position:-40px -420px}.ap-thunder_cloud_and_rain{background-position:-40px -440px}.ap-ophiuchus{background-position:-40px -460px}.ap-pick{background-position:-40px -480px}.ap-helmet_with_white_cross{background-position:-40px -500px}.ap-chains{background-position:-40px -520px}.ap-no_entry{background-position:-40px -540px}.ap-shinto_shrine{background-position:-40px -560px}.ap-church{background-position:-40px -580px}.ap-mountain{background-position:-40px -600px}.ap-beach_umbrella,.ap-umbrella_on_ground{background-position:-40px -620px}.ap-fountain{background-position:-40px -640px}.ap-golf{background-position:-40px -660px}.ap-ferry{background-position:-40px -680px}.ap-boat{background-position:-40px -700px}.ap-skier{background-position:-40px -720px}.ap-ice_skate{background-position:-40px -740px}.ap-person_with_ball{background-position:-40px -760px}.ap-tent{background-position:-60px -60px}.ap-fuelpump{background-position:-60px -80px}.ap-scissors{background-position:-60px -100px}.ap-white_check_mark{background-position:-60px -120px}.ap-airplane{background-position:-60px -140px}.ap-email{background-position:-60px -160px}.ap-fist{background-position:-60px -180px}.ap-hand{background-position:-60px -300px}.ap-v{background-position:-60px -420px}.ap-writing_hand{background-position:-60px -540px}.ap-pencil2{background-position:-60px -660px}.ap-black_nib{background-position:-60px -680px}.ap-heavy_check_mark{background-position:-60px -700px}.ap-heavy_multiplication_x{background-position:-60px -720px}.ap-latin_cross{background-position:-60px -740px}.ap-star_of_david{background-position:-60px -760px}.ap-sparkles{background-position:-60px -780px}.ap-eight_spoked_asterisk{background-position:-60px -800px}.ap-eight_pointed_black_star{background-position:-80px 0}.ap-snowflake{background-position:-80px -20px}.ap-sparkle{background-position:-80px -40px}.ap-x{background-position:-80px -60px}.ap-negative_squared_cross_mark{background-position:-80px -80px}.ap-question{background-position:-80px -100px}.ap-grey_question{background-position:-80px -120px}.ap-grey_exclamation{background-position:-80px -140px}.ap-exclamation{background-position:-80px -160px}.ap-heavy_heart_exclamation_mark_ornament{background-position:-80px -180px}.ap-heart{background-position:-80px -200px}.ap-heavy_plus_sign{background-position:-80px -220px}.ap-heavy_minus_sign{background-position:-80px -240px}.ap-heavy_division_sign{background-position:-80px -260px}.ap-arrow_right{background-position:-80px -280px}.ap-curly_loop{background-position:-80px -300px}.ap-loop{background-position:-80px -320px}.ap-arrow_heading_up{background-position:-80px -340px}.ap-arrow_heading_down{background-position:-80px -360px}.ap-arrow_left{background-position:-80px -380px}.ap-arrow_up{background-position:-80px -400px}.ap-arrow_down{background-position:-80px -420px}.ap-black_large_square{background-position:-80px -440px}.ap-white_large_square{background-position:-80px -460px}.ap-star{background-position:-80px -480px}.ap-o{background-position:-80px -500px}.ap-wavy_dash{background-position:-80px -520px}.ap-part_alternation_mark{background-position:-80px -540px}.ap-congratulations{background-position:-80px -560px}.ap-secret{background-position:-80px -580px}.ap-mahjong{background-position:-80px -600px}.ap-black_joker{background-position:-80px -620px}.ap-a{background-position:-80px -640px}.ap-b{background-position:-80px -660px}.ap-o2{background-position:-80px -680px}.ap-parking{background-position:-80px -700px}.ap-ab{background-position:-80px -720px}.ap-cl{background-position:-80px -740px}.ap-cool{background-position:-80px -760px}.ap-free{background-position:-80px -780px}.ap-id{background-position:-80px -800px}.ap-new{background-position:-100px 0}.ap-ng{background-position:-100px -20px}.ap-ok{background-position:-100px -40px}.ap-sos{background-position:-100px -60px}.ap-up{background-position:-100px -80px}.ap-vs{background-position:-100px -100px}.ap-koko{background-position:-100px -120px}.ap-sa{background-position:-100px -140px}.ap-u7121{background-position:-100px -160px}.ap-u6307{background-position:-100px -180px}.ap-u7981{background-position:-100px -200px}.ap-u7a7a{background-position:-100px -220px}.ap-u5408{background-position:-100px -240px}.ap-u6e80{background-position:-100px -260px}.ap-u6709{background-position:-100px -280px}.ap-u6708{background-position:-100px -300px}.ap-u7533{background-position:-100px -320px}.ap-u5272{background-position:-100px -340px}.ap-u55b6{background-position:-100px -360px}.ap-ideograph_advantage{background-position:-100px -380px}.ap-accept{background-position:-100px -400px}.ap-cyclone{background-position:-100px -420px}.ap-foggy{background-position:-100px -440px}.ap-closed_umbrella{background-position:-100px -460px}.ap-night_with_stars{background-position:-100px -480px}.ap-sunrise_over_mountains{background-position:-100px -500px}.ap-sunrise{background-position:-100px -520px}.ap-city_sunset{background-position:-100px -540px}.ap-city_sunrise{background-position:-100px -560px}.ap-rainbow{background-position:-100px -580px}.ap-bridge_at_night{background-position:-100px -600px}.ap-ocean{background-position:-100px -620px}.ap-volcano{background-position:-100px -640px}.ap-milky_way{background-position:-100px -660px}.ap-earth_africa{background-position:-100px -680px}.ap-earth_americas{background-position:-100px -700px}.ap-earth_asia{background-position:-100px -720px}.ap-globe_with_meridians{background-position:-100px -740px}.ap-new_moon{background-position:-100px -760px}.ap-waxing_crescent_moon{background-position:-100px -780px}.ap-first_quarter_moon{background-position:-100px -800px}.ap-moon{background-position:-120px 0}.ap-full_moon{background-position:-120px -20px}.ap-waning_gibbous_moon{background-position:-120px -40px}.ap-last_quarter_moon{background-position:-120px -60px}.ap-waning_crescent_moon{background-position:-120px -80px}.ap-crescent_moon{background-position:-120px -100px}.ap-new_moon_with_face{background-position:-120px -120px}.ap-first_quarter_moon_with_face{background-position:-120px -140px}.ap-last_quarter_moon_with_face{background-position:-120px -160px}.ap-full_moon_with_face{background-position:-120px -180px}.ap-sun_with_face{background-position:-120px -200px}.ap-star2{background-position:-120px -220px}.ap-stars{background-position:-120px -240px}.ap-thermometer{background-position:-120px -260px}.ap-mostly_sunny{background-position:-120px -280px}.ap-barely_sunny{background-position:-120px -300px}.ap-partly_sunny_rain{background-position:-120px -320px}.ap-rain_cloud{background-position:-120px -340px}.ap-snow_cloud{background-position:-120px -360px}.ap-lightning{background-position:-120px -380px}.ap-tornado{background-position:-120px -400px}.ap-fog{background-position:-120px -420px}.ap-wind_blowing_face{background-position:-120px -440px}.ap-hotdog{background-position:-120px -460px}.ap-taco{background-position:-120px -480px}.ap-burrito{background-position:-120px -500px}.ap-chestnut{background-position:-120px -520px}.ap-seedling{background-position:-120px -540px}.ap-evergreen_tree{background-position:-120px -560px}.ap-deciduous_tree{background-position:-120px -580px}.ap-palm_tree{background-position:-120px -600px}.ap-cactus{background-position:-120px -620px}.ap-hot_pepper{background-position:-120px -640px}.ap-tulip{background-position:-120px -660px}.ap-cherry_blossom{background-position:-120px -680px}.ap-rose{background-position:-120px -700px}.ap-hibiscus{background-position:-120px -720px}.ap-sunflower{background-position:-120px -740px}.ap-blossom{background-position:-120px -760px}.ap-corn{background-position:-120px -780px}.ap-ear_of_rice{background-position:-120px -800px}.ap-herb{background-position:-140px 0}.ap-four_leaf_clover{background-position:-140px -20px}.ap-maple_leaf{background-position:-140px -40px}.ap-fallen_leaf{background-position:-140px -60px}.ap-leaves{background-position:-140px -80px}.ap-mushroom{background-position:-140px -100px}.ap-tomato{background-position:-140px -120px}.ap-eggplant{background-position:-140px -140px}.ap-grapes{background-position:-140px -160px}.ap-melon{background-position:-140px -180px}.ap-watermelon{background-position:-140px -200px}.ap-tangerine{background-position:-140px -220px}.ap-lemon{background-position:-140px -240px}.ap-banana{background-position:-140px -260px}.ap-pineapple{background-position:-140px -280px}.ap-apple{background-position:-140px -300px}.ap-green_apple{background-position:-140px -320px}.ap-pear{background-position:-140px -340px}.ap-peach{background-position:-140px -360px}.ap-cherries{background-position:-140px -380px}.ap-strawberry{background-position:-140px -400px}.ap-hamburger{background-position:-140px -420px}.ap-pizza{background-position:-140px -440px}.ap-meat_on_bone{background-position:-140px -460px}.ap-poultry_leg{background-position:-140px -480px}.ap-rice_cracker{background-position:-140px -500px}.ap-rice_ball{background-position:-140px -520px}.ap-rice{background-position:-140px -540px}.ap-curry{background-position:-140px -560px}.ap-ramen{background-position:-140px -580px}.ap-spaghetti{background-position:-140px -600px}.ap-bread{background-position:-140px -620px}.ap-fries{background-position:-140px -640px}.ap-sweet_potato{background-position:-140px -660px}.ap-dango{background-position:-140px -680px}.ap-oden{background-position:-140px -700px}.ap-sushi{background-position:-140px -720px}.ap-fried_shrimp{background-position:-140px -740px}.ap-fish_cake{background-position:-140px -760px}.ap-icecream{background-position:-140px -780px}.ap-shaved_ice{background-position:-140px -800px}.ap-ice_cream{background-position:-160px 0}.ap-doughnut{background-position:-160px -20px}.ap-cookie{background-position:-160px -40px}.ap-chocolate_bar{background-position:-160px -60px}.ap-candy{background-position:-160px -80px}.ap-lollipop{background-position:-160px -100px}.ap-custard{background-position:-160px -120px}.ap-honey_pot{background-position:-160px -140px}.ap-cake{background-position:-160px -160px}.ap-bento{background-position:-160px -180px}.ap-stew{background-position:-160px -200px}.ap-egg{background-position:-160px -220px}.ap-fork_and_knife{background-position:-160px -240px}.ap-tea{background-position:-160px -260px}.ap-sake{background-position:-160px -280px}.ap-wine_glass{background-position:-160px -300px}.ap-cocktail{background-position:-160px -320px}.ap-tropical_drink{background-position:-160px -340px}.ap-beer{background-position:-160px -360px}.ap-beers{background-position:-160px -380px}.ap-baby_bottle{background-position:-160px -400px}.ap-knife_fork_plate{background-position:-160px -420px}.ap-champagne{background-position:-160px -440px}.ap-popcorn{background-position:-160px -460px}.ap-ribbon{background-position:-160px -480px}.ap-gift{background-position:-160px -500px}.ap-birthday{background-position:-160px -520px}.ap-jack_o_lantern{background-position:-160px -540px}.ap-christmas_tree{background-position:-160px -560px}.ap-santa{background-position:-160px -580px}.ap-fireworks{background-position:-160px -700px}.ap-sparkler{background-position:-160px -720px}.ap-balloon{background-position:-160px -740px}.ap-tada{background-position:-160px -760px}.ap-confetti_ball{background-position:-160px -780px}.ap-tanabata_tree{background-position:-160px -800px}.ap-crossed_flags{background-position:-180px 0}.ap-bamboo{background-position:-180px -20px}.ap-dolls{background-position:-180px -40px}.ap-flags{background-position:-180px -60px}.ap-wind_chime{background-position:-180px -80px}.ap-rice_scene{background-position:-180px -100px}.ap-school_satchel{background-position:-180px -120px}.ap-mortar_board{background-position:-180px -140px}.ap-medal{background-position:-180px -160px}.ap-reminder_ribbon{background-position:-180px -180px}.ap-studio_microphone{background-position:-180px -200px}.ap-level_slider{background-position:-180px -220px}.ap-control_knobs{background-position:-180px -240px}.ap-film_frames{background-position:-180px -260px}.ap-admission_tickets{background-position:-180px -280px}.ap-carousel_horse{background-position:-180px -300px}.ap-ferris_wheel{background-position:-180px -320px}.ap-roller_coaster{background-position:-180px -340px}.ap-fishing_pole_and_fish{background-position:-180px -360px}.ap-microphone{background-position:-180px -380px}.ap-movie_camera{background-position:-180px -400px}.ap-cinema{background-position:-180px -420px}.ap-headphones{background-position:-180px -440px}.ap-art{background-position:-180px -460px}.ap-tophat{background-position:-180px -480px}.ap-circus_tent{background-position:-180px -500px}.ap-ticket{background-position:-180px -520px}.ap-clapper{background-position:-180px -540px}.ap-performing_arts{background-position:-180px -560px}.ap-video_game{background-position:-180px -580px}.ap-dart{background-position:-180px -600px}.ap-slot_machine{background-position:-180px -620px}.ap-8ball{background-position:-180px -640px}.ap-game_die{background-position:-180px -660px}.ap-bowling{background-position:-180px -680px}.ap-flower_playing_cards{background-position:-180px -700px}.ap-musical_note{background-position:-180px -720px}.ap-notes{background-position:-180px -740px}.ap-saxophone{background-position:-180px -760px}.ap-guitar{background-position:-180px -780px}.ap-musical_keyboard{background-position:-180px -800px}.ap-trumpet{background-position:-200px 0}.ap-violin{background-position:-200px -20px}.ap-musical_score{background-position:-200px -40px}.ap-running_shirt_with_sash{background-position:-200px -60px}.ap-tennis{background-position:-200px -80px}.ap-ski{background-position:-200px -100px}.ap-basketball{background-position:-200px -120px}.ap-checkered_flag{background-position:-200px -140px}.ap-snowboarder{background-position:-200px -160px}.ap-runner{background-position:-200px -180px}.ap-surfer{background-position:-200px -300px}.ap-sports_medal{background-position:-200px -420px}.ap-trophy{background-position:-200px -440px}.ap-horse_racing{background-position:-200px -460px}.ap-football{background-position:-200px -480px}.ap-rugby_football{background-position:-200px -500px}.ap-swimmer{background-position:-200px -520px}.ap-weight_lifter{background-position:-200px -640px}.ap-golfer{background-position:-200px -760px}.ap-racing_motorcycle{background-position:-200px -780px}.ap-racing_car{background-position:-200px -800px}.ap-cricket_bat_and_ball{background-position:-220px 0}.ap-volleyball{background-position:-220px -20px}.ap-field_hockey_stick_and_ball{background-position:-220px -40px}.ap-ice_hockey_stick_and_puck{background-position:-220px -60px}.ap-table_tennis_paddle_and_ball{background-position:-220px -80px}.ap-snow_capped_mountain{background-position:-220px -100px}.ap-camping{background-position:-220px -120px}.ap-beach_with_umbrella{background-position:-220px -140px}.ap-building_construction{background-position:-220px -160px}.ap-house_buildings{background-position:-220px -180px}.ap-cityscape{background-position:-220px -200px}.ap-derelict_house_building{background-position:-220px -220px}.ap-classical_building{background-position:-220px -240px}.ap-desert{background-position:-220px -260px}.ap-desert_island{background-position:-220px -280px}.ap-national_park{background-position:-220px -300px}.ap-stadium{background-position:-220px -320px}.ap-house{background-position:-220px -340px}.ap-house_with_garden{background-position:-220px -360px}.ap-office{background-position:-220px -380px}.ap-post_office{background-position:-220px -400px}.ap-european_post_office{background-position:-220px -420px}.ap-hospital{background-position:-220px -440px}.ap-bank{background-position:-220px -460px}.ap-atm{background-position:-220px -480px}.ap-hotel{background-position:-220px -500px}.ap-love_hotel{background-position:-220px -520px}.ap-convenience_store{background-position:-220px -540px}.ap-school{background-position:-220px -560px}.ap-department_store{background-position:-220px -580px}.ap-factory{background-position:-220px -600px}.ap-izakaya_lantern{background-position:-220px -620px}.ap-japanese_castle{background-position:-220px -640px}.ap-european_castle{background-position:-220px -660px}.ap-waving_white_flag{background-position:-220px -680px}.ap-waving_black_flag{background-position:-220px -700px}.ap-rosette{background-position:-220px -720px}.ap-label{background-position:-220px -740px}.ap-badminton_racquet_and_shuttlecock{background-position:-220px -760px}.ap-bow_and_arrow{background-position:-220px -780px}.ap-amphora{background-position:-220px -800px}.ap-skin-tone-2{background-position:-240px 0}.ap-skin-tone-3{background-position:-240px -20px}.ap-skin-tone-4{background-position:-240px -40px}.ap-skin-tone-5{background-position:-240px -60px}.ap-skin-tone-6{background-position:-240px -80px}.ap-rat{background-position:-240px -100px}.ap-mouse2{background-position:-240px -120px}.ap-ox{background-position:-240px -140px}.ap-water_buffalo{background-position:-240px -160px}.ap-cow2{background-position:-240px -180px}.ap-tiger2{background-position:-240px -200px}.ap-leopard{background-position:-240px -220px}.ap-rabbit2{background-position:-240px -240px}.ap-cat2{background-position:-240px -260px}.ap-dragon{background-position:-240px -280px}.ap-crocodile{background-position:-240px -300px}.ap-whale2{background-position:-240px -320px}.ap-snail{background-position:-240px -340px}.ap-snake{background-position:-240px -360px}.ap-racehorse{background-position:-240px -380px}.ap-ram{background-position:-240px -400px}.ap-goat{background-position:-240px -420px}.ap-sheep{background-position:-240px -440px}.ap-monkey{background-position:-240px -460px}.ap-rooster{background-position:-240px -480px}.ap-chicken{background-position:-240px -500px}.ap-dog2{background-position:-240px -520px}.ap-pig2{background-position:-240px -540px}.ap-boar{background-position:-240px -560px}.ap-elephant{background-position:-240px -580px}.ap-octopus{background-position:-240px -600px}.ap-shell{background-position:-240px -620px}.ap-bug{background-position:-240px -640px}.ap-ant{background-position:-240px -660px}.ap-bee{background-position:-240px -680px}.ap-beetle{background-position:-240px -700px}.ap-fish{background-position:-240px -720px}.ap-tropical_fish{background-position:-240px -740px}.ap-blowfish{background-position:-240px -760px}.ap-turtle{background-position:-240px -780px}.ap-hatching_chick{background-position:-240px -800px}.ap-baby_chick{background-position:-260px 0}.ap-hatched_chick{background-position:-260px -20px}.ap-bird{background-position:-260px -40px}.ap-penguin{background-position:-260px -60px}.ap-koala{background-position:-260px -80px}.ap-poodle{background-position:-260px -100px}.ap-dromedary_camel{background-position:-260px -120px}.ap-camel{background-position:-260px -140px}.ap-dolphin{background-position:-260px -160px}.ap-mouse{background-position:-260px -180px}.ap-cow{background-position:-260px -200px}.ap-tiger{background-position:-260px -220px}.ap-rabbit{background-position:-260px -240px}.ap-cat{background-position:-260px -260px}.ap-dragon_face{background-position:-260px -280px}.ap-whale{background-position:-260px -300px}.ap-horse{background-position:-260px -320px}.ap-monkey_face{background-position:-260px -340px}.ap-dog{background-position:-260px -360px}.ap-pig{background-position:-260px -380px}.ap-frog{background-position:-260px -400px}.ap-hamster{background-position:-260px -420px}.ap-wolf{background-position:-260px -440px}.ap-bear{background-position:-260px -460px}.ap-panda_face{background-position:-260px -480px}.ap-pig_nose{background-position:-260px -500px}.ap-feet{background-position:-260px -520px}.ap-chipmunk{background-position:-260px -540px}.ap-eyes{background-position:-260px -560px}.ap-eye{background-position:-260px -580px}.ap-ear{background-position:-260px -600px}.ap-nose{background-position:-260px -720px}.ap-lips{background-position:-280px -20px}.ap-tongue{background-position:-280px -40px}.ap-point_up_2{background-position:-280px -60px}.ap-point_down{background-position:-280px -180px}.ap-point_left{background-position:-280px -300px}.ap-point_right{background-position:-280px -420px}.ap-facepunch{background-position:-280px -540px}.ap-wave{background-position:-280px -660px}.ap-ok_hand{background-position:-280px -780px}.ap-thumbsup{background-position:-300px -80px}.ap--1,.ap-thumbsdown{background-position:-300px -200px}.ap-clap{background-position:-300px -320px}.ap-open_hands{background-position:-300px -440px}.ap-crown{background-position:-300px -560px}.ap-womans_hat{background-position:-300px -580px}.ap-eyeglasses{background-position:-300px -600px}.ap-necktie{background-position:-300px -620px}.ap-shirt{background-position:-300px -640px}.ap-jeans{background-position:-300px -660px}.ap-dress{background-position:-300px -680px}.ap-kimono{background-position:-300px -700px}.ap-bikini{background-position:-300px -720px}.ap-womans_clothes{background-position:-300px -740px}.ap-purse{background-position:-300px -760px}.ap-handbag{background-position:-300px -780px}.ap-pouch{background-position:-300px -800px}.ap-mans_shoe{background-position:-320px 0}.ap-athletic_shoe{background-position:-320px -20px}.ap-high_heel{background-position:-320px -40px}.ap-sandal{background-position:-320px -60px}.ap-boot{background-position:-320px -80px}.ap-footprints{background-position:-320px -100px}.ap-bust_in_silhouette{background-position:-320px -120px}.ap-busts_in_silhouette{background-position:-320px -140px}.ap-boy{background-position:-320px -160px}.ap-girl{background-position:-320px -280px}.ap-man{background-position:-320px -400px}.ap-woman{background-position:-320px -520px}.ap-family{background-position:-320px -640px}.ap-couple{background-position:-320px -660px}.ap-two_men_holding_hands{background-position:-320px -680px}.ap-two_women_holding_hands{background-position:-320px -700px}.ap-cop{background-position:-320px -720px}.ap-dancers{background-position:-340px -20px}.ap-bride_with_veil{background-position:-340px -40px}.ap-person_with_blond_hair{background-position:-340px -160px}.ap-man_with_gua_pi_mao{background-position:-340px -280px}.ap-man_with_turban{background-position:-340px -400px}.ap-older_man{background-position:-340px -520px}.ap-older_woman{background-position:-340px -640px}.ap-baby{background-position:-340px -760px}.ap-construction_worker{background-position:-360px -60px}.ap-princess{background-position:-360px -180px}.ap-japanese_ogre{background-position:-360px -300px}.ap-japanese_goblin{background-position:-360px -320px}.ap-ghost{background-position:-360px -340px}.ap-angel{background-position:-360px -360px}.ap-alien{background-position:-360px -480px}.ap-space_invader{background-position:-360px -500px}.ap-imp{background-position:-360px -520px}.ap-skull{background-position:-360px -540px}.ap-information_desk_person{background-position:-360px -560px}.ap-guardsman{background-position:-360px -680px}.ap-dancer{background-position:-360px -800px}.ap-lipstick{background-position:-380px -100px}.ap-nail_care{background-position:-380px -120px}.ap-massage{background-position:-380px -240px}.ap-haircut{background-position:-380px -360px}.ap-barber{background-position:-380px -480px}.ap-syringe{background-position:-380px -500px}.ap-pill{background-position:-380px -520px}.ap-kiss{background-position:-380px -540px}.ap-love_letter{background-position:-380px -560px}.ap-ring{background-position:-380px -580px}.ap-gem{background-position:-380px -600px}.ap-couplekiss{background-position:-380px -620px}.ap-bouquet{background-position:-380px -640px}.ap-couple_with_heart{background-position:-380px -660px}.ap-wedding{background-position:-380px -680px}.ap-heartbeat{background-position:-380px -700px}.ap-broken_heart{background-position:-380px -720px}.ap-two_hearts{background-position:-380px -740px}.ap-sparkling_heart{background-position:-380px -760px}.ap-heartpulse{background-position:-380px -780px}.ap-cupid{background-position:-380px -800px}.ap-blue_heart{background-position:-400px 0}.ap-green_heart{background-position:-400px -20px}.ap-yellow_heart{background-position:-400px -40px}.ap-purple_heart{background-position:-400px -60px}.ap-gift_heart{background-position:-400px -80px}.ap-revolving_hearts{background-position:-400px -100px}.ap-heart_decoration{background-position:-400px -120px}.ap-diamond_shape_with_a_dot_inside{background-position:-400px -140px}.ap-bulb{background-position:-400px -160px}.ap-anger{background-position:-400px -180px}.ap-bomb{background-position:-400px -200px}.ap-zzz{background-position:-400px -220px}.ap-boom{background-position:-400px -240px}.ap-sweat_drops{background-position:-400px -260px}.ap-droplet{background-position:-400px -280px}.ap-dash{background-position:-400px -300px}.ap-hankey{background-position:-400px -320px}.ap-muscle{background-position:-400px -340px}.ap-dizzy{background-position:-400px -460px}.ap-speech_balloon{background-position:-400px -480px}.ap-thought_balloon{background-position:-400px -500px}.ap-white_flower{background-position:-400px -520px}.ap-100{background-position:-400px -540px}.ap-moneybag{background-position:-400px -560px}.ap-currency_exchange{background-position:-400px -580px}.ap-heavy_dollar_sign{background-position:-400px -600px}.ap-credit_card{background-position:-400px -620px}.ap-yen{background-position:-400px -640px}.ap-dollar{background-position:-400px -660px}.ap-euro{background-position:-400px -680px}.ap-pound{background-position:-400px -700px}.ap-money_with_wings{background-position:-400px -720px}.ap-chart{background-position:-400px -740px}.ap-seat{background-position:-400px -760px}.ap-computer{background-position:-400px -780px}.ap-briefcase{background-position:-400px -800px}.ap-minidisc{background-position:-420px 0}.ap-floppy_disk{background-position:-420px -20px}.ap-cd{background-position:-420px -40px}.ap-dvd{background-position:-420px -60px}.ap-file_folder{background-position:-420px -80px}.ap-open_file_folder{background-position:-420px -100px}.ap-page_with_curl{background-position:-420px -120px}.ap-page_facing_up{background-position:-420px -140px}.ap-date{background-position:-420px -160px}.ap-calendar{background-position:-420px -180px}.ap-card_index{background-position:-420px -200px}.ap-chart_with_upwards_trend{background-position:-420px -220px}.ap-chart_with_downwards_trend{background-position:-420px -240px}.ap-bar_chart{background-position:-420px -260px}.ap-clipboard{background-position:-420px -280px}.ap-pushpin{background-position:-420px -300px}.ap-round_pushpin{background-position:-420px -320px}.ap-paperclip{background-position:-420px -340px}.ap-straight_ruler{background-position:-420px -360px}.ap-triangular_ruler{background-position:-420px -380px}.ap-bookmark_tabs{background-position:-420px -400px}.ap-ledger{background-position:-420px -420px}.ap-notebook{background-position:-420px -440px}.ap-notebook_with_decorative_cover{background-position:-420px -460px}.ap-closed_book{background-position:-420px -480px}.ap-book{background-position:-420px -500px}.ap-green_book{background-position:-420px -520px}.ap-blue_book{background-position:-420px -540px}.ap-orange_book{background-position:-420px -560px}.ap-books{background-position:-420px -580px}.ap-name_badge{background-position:-420px -600px}.ap-scroll{background-position:-420px -620px}.ap-memo{background-position:-420px -640px}.ap-telephone_receiver{background-position:-420px -660px}.ap-pager{background-position:-420px -680px}.ap-fax{background-position:-420px -700px}.ap-satellite_antenna{background-position:-420px -720px}.ap-loudspeaker{background-position:-420px -740px}.ap-mega{background-position:-420px -760px}.ap-outbox_tray{background-position:-420px -780px}.ap-inbox_tray{background-position:-420px -800px}.ap-package{background-position:-440px 0}.ap-e-mail{background-position:-440px -20px}.ap-incoming_envelope{background-position:-440px -40px}.ap-envelope_with_arrow{background-position:-440px -60px}.ap-mailbox_closed{background-position:-440px -80px}.ap-mailbox{background-position:-440px -100px}.ap-mailbox_with_mail{background-position:-440px -120px}.ap-mailbox_with_no_mail{background-position:-440px -140px}.ap-postbox{background-position:-440px -160px}.ap-postal_horn{background-position:-440px -180px}.ap-newspaper{background-position:-440px -200px}.ap-iphone{background-position:-440px -220px}.ap-calling{background-position:-440px -240px}.ap-vibration_mode{background-position:-440px -260px}.ap-mobile_phone_off{background-position:-440px -280px}.ap-no_mobile_phones{background-position:-440px -300px}.ap-signal_strength{background-position:-440px -320px}.ap-camera{background-position:-440px -340px}.ap-camera_with_flash{background-position:-440px -360px}.ap-video_camera{background-position:-440px -380px}.ap-tv{background-position:-440px -400px}.ap-radio{background-position:-440px -420px}.ap-vhs{background-position:-440px -440px}.ap-film_projector{background-position:-440px -460px}.ap-prayer_beads{background-position:-440px -480px}.ap-twisted_rightwards_arrows{background-position:-440px -500px}.ap-repeat{background-position:-440px -520px}.ap-repeat_one{background-position:-440px -540px}.ap-arrows_clockwise{background-position:-440px -560px}.ap-arrows_counterclockwise{background-position:-440px -580px}.ap-low_brightness{background-position:-440px -600px}.ap-high_brightness{background-position:-440px -620px}.ap-mute{background-position:-440px -640px}.ap-speaker{background-position:-440px -660px}.ap-sound{background-position:-440px -680px}.ap-loud_sound{background-position:-440px -700px}.ap-battery{background-position:-440px -720px}.ap-electric_plug{background-position:-440px -740px}.ap-mag{background-position:-440px -760px}.ap-mag_right{background-position:-440px -780px}.ap-lock_with_ink_pen{background-position:-440px -800px}.ap-closed_lock_with_key{background-position:-460px 0}.ap-key{background-position:-460px -20px}.ap-lock{background-position:-460px -40px}.ap-unlock{background-position:-460px -60px}.ap-bell{background-position:-460px -80px}.ap-no_bell{background-position:-460px -100px}.ap-bookmark{background-position:-460px -120px}.ap-link{background-position:-460px -140px}.ap-radio_button{background-position:-460px -160px}.ap-back{background-position:-460px -180px}.ap-end{background-position:-460px -200px}.ap-on{background-position:-460px -220px}.ap-soon{background-position:-460px -240px}.ap-top{background-position:-460px -260px}.ap-underage{background-position:-460px -280px}.ap-keycap_ten{background-position:-460px -300px}.ap-capital_abcd{background-position:-460px -320px}.ap-abcd{background-position:-460px -340px}.ap-1234{background-position:-460px -360px}.ap-symbols{background-position:-460px -380px}.ap-abc{background-position:-460px -400px}.ap-fire{background-position:-460px -420px}.ap-flashlight{background-position:-460px -440px}.ap-wrench{background-position:-460px -460px}.ap-hammer{background-position:-460px -480px}.ap-nut_and_bolt{background-position:-460px -500px}.ap-hocho{background-position:-460px -520px}.ap-gun{background-position:-460px -540px}.ap-microscope{background-position:-460px -560px}.ap-telescope{background-position:-460px -580px}.ap-crystal_ball{background-position:-460px -600px}.ap-six_pointed_star{background-position:-460px -620px}.ap-beginner{background-position:-460px -640px}.ap-trident{background-position:-460px -660px}.ap-black_square_button{background-position:-460px -680px}.ap-white_square_button{background-position:-460px -700px}.ap-red_circle{background-position:-460px -720px}.ap-large_blue_circle{background-position:-460px -740px}.ap-large_orange_diamond{background-position:-460px -760px}.ap-large_blue_diamond{background-position:-460px -780px}.ap-small_orange_diamond{background-position:-460px -800px}.ap-small_blue_diamond{background-position:-480px 0}.ap-small_red_triangle{background-position:-480px -20px}.ap-small_red_triangle_down{background-position:-480px -40px}.ap-arrow_up_small{background-position:-480px -60px}.ap-arrow_down_small{background-position:-480px -80px}.ap-om_symbol{background-position:-480px -100px}.ap-dove_of_peace{background-position:-480px -120px}.ap-kaaba{background-position:-480px -140px}.ap-mosque{background-position:-480px -160px}.ap-synagogue{background-position:-480px -180px}.ap-menorah_with_nine_branches{background-position:-480px -200px}.ap-clock1{background-position:-480px -220px}.ap-clock2{background-position:-480px -240px}.ap-clock3{background-position:-480px -260px}.ap-clock4{background-position:-480px -280px}.ap-clock5{background-position:-480px -300px}.ap-clock6{background-position:-480px -320px}.ap-clock7{background-position:-480px -340px}.ap-clock8{background-position:-480px -360px}.ap-clock9{background-position:-480px -380px}.ap-clock10{background-position:-480px -400px}.ap-clock11{background-position:-480px -420px}.ap-clock12{background-position:-480px -440px}.ap-clock130{background-position:-480px -460px}.ap-clock230{background-position:-480px -480px}.ap-clock330{background-position:-480px -500px}.ap-clock430{background-position:-480px -520px}.ap-clock530{background-position:-480px -540px}.ap-clock630{background-position:-480px -560px}.ap-clock730{background-position:-480px -580px}.ap-clock830{background-position:-480px -600px}.ap-clock930{background-position:-480px -620px}.ap-clock1030{background-position:-480px -640px}.ap-clock1130{background-position:-480px -660px}.ap-clock1230{background-position:-480px -680px}.ap-candle{background-position:-480px -700px}.ap-mantelpiece_clock{background-position:-480px -720px}.ap-hole{background-position:-480px -740px}.ap-man_in_business_suit_levitating{background-position:-480px -760px}.ap-sleuth_or_spy{background-position:-480px -780px}.ap-dark_sunglasses{background-position:-500px -80px}.ap-spider{background-position:-500px -100px}.ap-spider_web{background-position:-500px -120px}.ap-joystick{background-position:-500px -140px}.ap-linked_paperclips{background-position:-500px -160px}.ap-lower_left_ballpoint_pen{background-position:-500px -180px}.ap-lower_left_fountain_pen{background-position:-500px -200px}.ap-lower_left_paintbrush{background-position:-500px -220px}.ap-lower_left_crayon{background-position:-500px -240px}.ap-raised_hand_with_fingers_splayed{background-position:-500px -260px}.ap-middle_finger{background-position:-500px -380px}.ap-spock-hand{background-position:-500px -500px}.ap-desktop_computer{background-position:-500px -620px}.ap-printer{background-position:-500px -640px}.ap-three_button_mouse{background-position:-500px -660px}.ap-trackball{background-position:-500px -680px}.ap-frame_with_picture{background-position:-500px -700px}.ap-card_index_dividers{background-position:-500px -720px}.ap-card_file_box{background-position:-500px -740px}.ap-file_cabinet{background-position:-500px -760px}.ap-wastebasket{background-position:-500px -780px}.ap-spiral_note_pad{background-position:-500px -800px}.ap-spiral_calendar_pad{background-position:-520px 0}.ap-compression{background-position:-520px -20px}.ap-old_key{background-position:-520px -40px}.ap-rolled_up_newspaper{background-position:-520px -60px}.ap-dagger_knife{background-position:-520px -80px}.ap-speaking_head_in_silhouette{background-position:-520px -100px}.ap-left_speech_bubble{background-position:-520px -120px}.ap-right_anger_bubble{background-position:-520px -140px}.ap-ballot_box_with_ballot{background-position:-520px -160px}.ap-world_map{background-position:-520px -180px}.ap-mount_fuji{background-position:-520px -200px}.ap-tokyo_tower{background-position:-520px -220px}.ap-statue_of_liberty{background-position:-520px -240px}.ap-japan{background-position:-520px -260px}.ap-moyai{background-position:-520px -280px}.ap-grinning{background-position:-520px -300px}.ap-grin{background-position:-520px -320px}.ap-joy{background-position:-520px -340px}.ap-smiley{background-position:-520px -360px}.ap-smile{background-position:-520px -380px}.ap-sweat_smile{background-position:-520px -400px}.ap-laughing{background-position:-520px -420px}.ap-innocent{background-position:-520px -440px}.ap-smiling_imp{background-position:-520px -460px}.ap-wink{background-position:-520px -480px}.ap-blush{background-position:-520px -500px}.ap-yum{background-position:-520px -520px}.ap-relieved{background-position:-520px -540px}.ap-heart_eyes{background-position:-520px -560px}.ap-sunglasses{background-position:-520px -580px}.ap-smirk{background-position:-520px -600px}.ap-neutral_face{background-position:-520px -620px}.ap-expressionless{background-position:-520px -640px}.ap-unamused{background-position:-520px -660px}.ap-sweat{background-position:-520px -680px}.ap-pensive{background-position:-520px -700px}.ap-confused{background-position:-520px -720px}.ap-confounded{background-position:-520px -740px}.ap-kissing{background-position:-520px -760px}.ap-kissing_heart{background-position:-520px -780px}.ap-kissing_smiling_eyes{background-position:-520px -800px}.ap-kissing_closed_eyes{background-position:-540px 0}.ap-stuck_out_tongue{background-position:-540px -20px}.ap-stuck_out_tongue_winking_eye{background-position:-540px -40px}.ap-stuck_out_tongue_closed_eyes{background-position:-540px -60px}.ap-disappointed{background-position:-540px -80px}.ap-worried{background-position:-540px -100px}.ap-angry{background-position:-540px -120px}.ap-rage{background-position:-540px -140px}.ap-cry{background-position:-540px -160px}.ap-persevere{background-position:-540px -180px}.ap-triumph{background-position:-540px -200px}.ap-disappointed_relieved{background-position:-540px -220px}.ap-frowning{background-position:-540px -240px}.ap-anguished{background-position:-540px -260px}.ap-fearful{background-position:-540px -280px}.ap-weary{background-position:-540px -300px}.ap-sleepy{background-position:-540px -320px}.ap-tired_face{background-position:-540px -340px}.ap-grimacing{background-position:-540px -360px}.ap-sob{background-position:-540px -380px}.ap-open_mouth{background-position:-540px -400px}.ap-hushed{background-position:-540px -420px}.ap-cold_sweat{background-position:-540px -440px}.ap-scream{background-position:-540px -460px}.ap-astonished{background-position:-540px -480px}.ap-flushed{background-position:-540px -500px}.ap-sleeping{background-position:-540px -520px}.ap-dizzy_face{background-position:-540px -540px}.ap-no_mouth{background-position:-540px -560px}.ap-mask{background-position:-540px -580px}.ap-smile_cat{background-position:-540px -600px}.ap-joy_cat{background-position:-540px -620px}.ap-smiley_cat{background-position:-540px -640px}.ap-heart_eyes_cat{background-position:-540px -660px}.ap-smirk_cat{background-position:-540px -680px}.ap-kissing_cat{background-position:-540px -700px}.ap-pouting_cat{background-position:-540px -720px}.ap-crying_cat_face{background-position:-540px -740px}.ap-scream_cat{background-position:-540px -760px}.ap-slightly_frowning_face{background-position:-540px -780px}.ap-slightly_smiling_face{background-position:-540px -800px}.ap-upside_down_face{background-position:-560px 0}.ap-face_with_rolling_eyes{background-position:-560px -20px}.ap-no_good{background-position:-560px -40px}.ap-ok_woman{background-position:-560px -160px}.ap-bow{background-position:-560px -280px}.ap-see_no_evil{background-position:-560px -400px}.ap-hear_no_evil{background-position:-560px -420px}.ap-speak_no_evil{background-position:-560px -440px}.ap-raising_hand{background-position:-560px -460px}.ap-raised_hands{background-position:-560px -580px}.ap-person_frowning{background-position:-560px -700px}.ap-person_with_pouting_face{background-position:-580px 0}.ap-pray{background-position:-580px -120px}.ap-rocket{background-position:-580px -240px}.ap-helicopter{background-position:-580px -260px}.ap-steam_locomotive{background-position:-580px -280px}.ap-railway_car{background-position:-580px -300px}.ap-bullettrain_side{background-position:-580px -320px}.ap-bullettrain_front{background-position:-580px -340px}.ap-train2{background-position:-580px -360px}.ap-metro{background-position:-580px -380px}.ap-light_rail{background-position:-580px -400px}.ap-station{background-position:-580px -420px}.ap-tram{background-position:-580px -440px}.ap-train{background-position:-580px -460px}.ap-bus{background-position:-580px -480px}.ap-oncoming_bus{background-position:-580px -500px}.ap-trolleybus{background-position:-580px -520px}.ap-busstop{background-position:-580px -540px}.ap-minibus{background-position:-580px -560px}.ap-ambulance{background-position:-580px -580px}.ap-fire_engine{background-position:-580px -600px}.ap-police_car{background-position:-580px -620px}.ap-oncoming_police_car{background-position:-580px -640px}.ap-taxi{background-position:-580px -660px}.ap-oncoming_taxi{background-position:-580px -680px}.ap-car{background-position:-580px -700px}.ap-oncoming_automobile{background-position:-580px -720px}.ap-blue_car{background-position:-580px -740px}.ap-truck{background-position:-580px -760px}.ap-articulated_lorry{background-position:-580px -780px}.ap-tractor{background-position:-580px -800px}.ap-monorail{background-position:-600px 0}.ap-mountain_railway{background-position:-600px -20px}.ap-suspension_railway{background-position:-600px -40px}.ap-mountain_cableway{background-position:-600px -60px}.ap-aerial_tramway{background-position:-600px -80px}.ap-ship{background-position:-600px -100px}.ap-rowboat{background-position:-600px -120px}.ap-speedboat{background-position:-600px -240px}.ap-traffic_light{background-position:-600px -260px}.ap-vertical_traffic_light{background-position:-600px -280px}.ap-construction{background-position:-600px -300px}.ap-rotating_light{background-position:-600px -320px}.ap-triangular_flag_on_post{background-position:-600px -340px}.ap-door{background-position:-600px -360px}.ap-no_entry_sign{background-position:-600px -380px}.ap-smoking{background-position:-600px -400px}.ap-no_smoking{background-position:-600px -420px}.ap-put_litter_in_its_place{background-position:-600px -440px}.ap-do_not_litter{background-position:-600px -460px}.ap-potable_water{background-position:-600px -480px}.ap-non-potable_water{background-position:-600px -500px}.ap-bike{background-position:-600px -520px}.ap-no_bicycles{background-position:-600px -540px}.ap-bicyclist{background-position:-600px -560px}.ap-mountain_bicyclist{background-position:-600px -680px}.ap-walking{background-position:-600px -800px}.ap-no_pedestrians{background-position:-620px -100px}.ap-children_crossing{background-position:-620px -120px}.ap-mens{background-position:-620px -140px}.ap-womens{background-position:-620px -160px}.ap-restroom{background-position:-620px -180px}.ap-baby_symbol{background-position:-620px -200px}.ap-toilet{background-position:-620px -220px}.ap-wc{background-position:-620px -240px}.ap-shower{background-position:-620px -260px}.ap-bath{background-position:-620px -280px}.ap-bathtub{background-position:-620px -400px}.ap-passport_control{background-position:-620px -420px}.ap-customs{background-position:-620px -440px}.ap-baggage_claim{background-position:-620px -460px}.ap-left_luggage{background-position:-620px -480px}.ap-couch_and_lamp{background-position:-620px -500px}.ap-sleeping_accommodation{background-position:-620px -520px}.ap-shopping_bags{background-position:-620px -540px}.ap-bellhop_bell{background-position:-620px -560px}.ap-bed{background-position:-620px -580px}.ap-place_of_worship{background-position:-620px -600px}.ap-hammer_and_wrench{background-position:-620px -620px}.ap-shield{background-position:-620px -640px}.ap-oil_drum{background-position:-620px -660px}.ap-motorway{background-position:-620px -680px}.ap-railway_track{background-position:-620px -700px}.ap-motor_boat{background-position:-620px -720px}.ap-small_airplane{background-position:-620px -740px}.ap-airplane_departure{background-position:-620px -760px}.ap-airplane_arriving{background-position:-620px -780px}.ap-satellite{background-position:-620px -800px}.ap-passenger_ship{background-position:-640px 0}.ap-zipper_mouth_face{background-position:-640px -20px}.ap-money_mouth_face{background-position:-640px -40px}.ap-face_with_thermometer{background-position:-640px -60px}.ap-nerd_face{background-position:-640px -80px}.ap-thinking_face{background-position:-640px -100px}.ap-face_with_head_bandage{background-position:-640px -120px}.ap-robot_face{background-position:-640px -140px}.ap-hugging_face{background-position:-640px -160px}.ap-the_horns{background-position:-640px -180px}.ap-crab{background-position:-640px -300px}.ap-lion_face{background-position:-640px -320px}.ap-scorpion{background-position:-640px -340px}.ap-turkey{background-position:-640px -360px}.ap-unicorn_face{background-position:-640px -380px}.ap-cheese_wedge{background-position:-640px -400px}.ap-hash{background-position:-640px -420px}.ap-keycap_star{background-position:-640px -440px}.ap-zero{background-position:-640px -460px}.ap-one{background-position:-640px -480px}.ap-two{background-position:-640px -500px}.ap-three{background-position:-640px -520px}.ap-four{background-position:-640px -540px}.ap-five{background-position:-640px -560px}.ap-six{background-position:-640px -580px}.ap-seven{background-position:-640px -600px}.ap-eight{background-position:-640px -620px}.ap-nine{background-position:-640px -640px}.ap-flag-ac{background-position:-640px -660px}.ap-flag-ad{background-position:-640px -680px}.ap-flag-ae{background-position:-640px -700px}.ap-flag-af{background-position:-640px -720px}.ap-flag-ag{background-position:-640px -740px}.ap-flag-ai{background-position:-640px -760px}.ap-flag-al{background-position:-640px -780px}.ap-flag-am{background-position:-640px -800px}.ap-flag-ao{background-position:-660px 0}.ap-flag-aq{background-position:-660px -20px}.ap-flag-ar{background-position:-660px -40px}.ap-flag-as{background-position:-660px -60px}.ap-flag-at{background-position:-660px -80px}.ap-flag-au{background-position:-660px -100px}.ap-flag-aw{background-position:-660px -120px}.ap-flag-ax{background-position:-660px -140px}.ap-flag-az{background-position:-660px -160px}.ap-flag-ba{background-position:-660px -180px}.ap-flag-bb{background-position:-660px -200px}.ap-flag-bd{background-position:-660px -220px}.ap-flag-be{background-position:-660px -240px}.ap-flag-bf{background-position:-660px -260px}.ap-flag-bg{background-position:-660px -280px}.ap-flag-bh{background-position:-660px -300px}.ap-flag-bi{background-position:-660px -320px}.ap-flag-bj{background-position:-660px -340px}.ap-flag-bl{background-position:-660px -360px}.ap-flag-bm{background-position:-660px -380px}.ap-flag-bn{background-position:-660px -400px}.ap-flag-bo{background-position:-660px -420px}.ap-flag-bq{background-position:-660px -440px}.ap-flag-br{background-position:-660px -460px}.ap-flag-bs{background-position:-660px -480px}.ap-flag-bt{background-position:-660px -500px}.ap-flag-bv{background-position:-660px -520px}.ap-flag-bw{background-position:-660px -540px}.ap-flag-by{background-position:-660px -560px}.ap-flag-bz{background-position:-660px -580px}.ap-flag-ca{background-position:-660px -600px}.ap-flag-cc{background-position:-660px -620px}.ap-flag-cd{background-position:-660px -640px}.ap-flag-cf{background-position:-660px -660px}.ap-flag-cg{background-position:-660px -680px}.ap-flag-ch{background-position:-660px -700px}.ap-flag-ci{background-position:-660px -720px}.ap-flag-ck{background-position:-660px -740px}.ap-flag-cl{background-position:-660px -760px}.ap-flag-cm{background-position:-660px -780px}.ap-flag-cn{background-position:-660px -800px}.ap-flag-co{background-position:-680px 0}.ap-flag-cp{background-position:-680px -20px}.ap-flag-cr{background-position:-680px -40px}.ap-flag-cu{background-position:-680px -60px}.ap-flag-cv{background-position:-680px -80px}.ap-flag-cw{background-position:-680px -100px}.ap-flag-cx{background-position:-680px -120px}.ap-flag-cy{background-position:-680px -140px}.ap-flag-cz{background-position:-680px -160px}.ap-flag-de{background-position:-680px -180px}.ap-flag-dg{background-position:-680px -200px}.ap-flag-dj{background-position:-680px -220px}.ap-flag-dk{background-position:-680px -240px}.ap-flag-dm{background-position:-680px -260px}.ap-flag-do{background-position:-680px -280px}.ap-flag-dz{background-position:-680px -300px}.ap-flag-ea{background-position:-680px -320px}.ap-flag-ec{background-position:-680px -340px}.ap-flag-ee{background-position:-680px -360px}.ap-flag-eg{background-position:-680px -380px}.ap-flag-eh{background-position:-680px -400px}.ap-flag-er{background-position:-680px -420px}.ap-flag-es{background-position:-680px -440px}.ap-flag-et{background-position:-680px -460px}.ap-flag-eu{background-position:-680px -480px}.ap-flag-fi{background-position:-680px -500px}.ap-flag-fj{background-position:-680px -520px}.ap-flag-fk{background-position:-680px -540px}.ap-flag-fm{background-position:-680px -560px}.ap-flag-fo{background-position:-680px -580px}.ap-flag-fr{background-position:-680px -600px}.ap-flag-ga{background-position:-680px -620px}.ap-flag-gb{background-position:-680px -640px}.ap-flag-gd{background-position:-680px -660px}.ap-flag-ge{background-position:-680px -680px}.ap-flag-gf{background-position:-680px -700px}.ap-flag-gg{background-position:-680px -720px}.ap-flag-gh{background-position:-680px -740px}.ap-flag-gi{background-position:-680px -760px}.ap-flag-gl{background-position:-680px -780px}.ap-flag-gm{background-position:-680px -800px}.ap-flag-gn{background-position:-700px 0}.ap-flag-gp{background-position:-700px -20px}.ap-flag-gq{background-position:-700px -40px}.ap-flag-gr{background-position:-700px -60px}.ap-flag-gs{background-position:-700px -80px}.ap-flag-gt{background-position:-700px -100px}.ap-flag-gu{background-position:-700px -120px}.ap-flag-gw{background-position:-700px -140px}.ap-flag-gy{background-position:-700px -160px}.ap-flag-hk{background-position:-700px -180px}.ap-flag-hm{background-position:-700px -200px}.ap-flag-hn{background-position:-700px -220px}.ap-flag-hr{background-position:-700px -240px}.ap-flag-ht{background-position:-700px -260px}.ap-flag-hu{background-position:-700px -280px}.ap-flag-ic{background-position:-700px -300px}.ap-flag-id{background-position:-700px -320px}.ap-flag-ie{background-position:-700px -340px}.ap-flag-il{background-position:-700px -360px}.ap-flag-im{background-position:-700px -380px}.ap-flag-in{background-position:-700px -400px}.ap-flag-io{background-position:-700px -420px}.ap-flag-iq{background-position:-700px -440px}.ap-flag-ir{background-position:-700px -460px}.ap-flag-is{background-position:-700px -480px}.ap-flag-it{background-position:-700px -500px}.ap-flag-je{background-position:-700px -520px}.ap-flag-jm{background-position:-700px -540px}.ap-flag-jo{background-position:-700px -560px}.ap-flag-jp{background-position:-700px -580px}.ap-flag-ke{background-position:-700px -600px}.ap-flag-kg{background-position:-700px -620px}.ap-flag-kh{background-position:-700px -640px}.ap-flag-ki{background-position:-700px -660px}.ap-flag-km{background-position:-700px -680px}.ap-flag-kn{background-position:-700px -700px}.ap-flag-kp{background-position:-700px -720px}.ap-flag-kr{background-position:-700px -740px}.ap-flag-kw{background-position:-700px -760px}.ap-flag-ky{background-position:-700px -780px}.ap-flag-kz{background-position:-700px -800px}.ap-flag-la{background-position:-720px 0}.ap-flag-lb{background-position:-720px -20px}.ap-flag-lc{background-position:-720px -40px}.ap-flag-li{background-position:-720px -60px}.ap-flag-lk{background-position:-720px -80px}.ap-flag-lr{background-position:-720px -100px}.ap-flag-ls{background-position:-720px -120px}.ap-flag-lt{background-position:-720px -140px}.ap-flag-lu{background-position:-720px -160px}.ap-flag-lv{background-position:-720px -180px}.ap-flag-ly{background-position:-720px -200px}.ap-flag-ma{background-position:-720px -220px}.ap-flag-mc{background-position:-720px -240px}.ap-flag-md{background-position:-720px -260px}.ap-flag-me{background-position:-720px -280px}.ap-flag-mf{background-position:-720px -300px}.ap-flag-mg{background-position:-720px -320px}.ap-flag-mh{background-position:-720px -340px}.ap-flag-mk{background-position:-720px -360px}.ap-flag-ml{background-position:-720px -380px}.ap-flag-mm{background-position:-720px -400px}.ap-flag-mn{background-position:-720px -420px}.ap-flag-mo{background-position:-720px -440px}.ap-flag-mp{background-position:-720px -460px}.ap-flag-mq{background-position:-720px -480px}.ap-flag-mr{background-position:-720px -500px}.ap-flag-ms{background-position:-720px -520px}.ap-flag-mt{background-position:-720px -540px}.ap-flag-mu{background-position:-720px -560px}.ap-flag-mv{background-position:-720px -580px}.ap-flag-mw{background-position:-720px -600px}.ap-flag-mx{background-position:-720px -620px}.ap-flag-my{background-position:-720px -640px}.ap-flag-mz{background-position:-720px -660px}.ap-flag-na{background-position:-720px -680px}.ap-flag-nc{background-position:-720px -700px}.ap-flag-ne{background-position:-720px -720px}.ap-flag-nf{background-position:-720px -740px}.ap-flag-ng{background-position:-720px -760px}.ap-flag-ni{background-position:-720px -780px}.ap-flag-nl{background-position:-720px -800px}.ap-flag-no{background-position:-740px 0}.ap-flag-np{background-position:-740px -20px}.ap-flag-nr{background-position:-740px -40px}.ap-flag-nu{background-position:-740px -60px}.ap-flag-nz{background-position:-740px -80px}.ap-flag-om{background-position:-740px -100px}.ap-flag-pa{background-position:-740px -120px}.ap-flag-pe{background-position:-740px -140px}.ap-flag-pf{background-position:-740px -160px}.ap-flag-pg{background-position:-740px -180px}.ap-flag-ph{background-position:-740px -200px}.ap-flag-pk{background-position:-740px -220px}.ap-flag-pl{background-position:-740px -240px}.ap-flag-pm{background-position:-740px -260px}.ap-flag-pn{background-position:-740px -280px}.ap-flag-pr{background-position:-740px -300px}.ap-flag-ps{background-position:-740px -320px}.ap-flag-pt{background-position:-740px -340px}.ap-flag-pw{background-position:-740px -360px}.ap-flag-py{background-position:-740px -380px}.ap-flag-qa{background-position:-740px -400px}.ap-flag-re{background-position:-740px -420px}.ap-flag-ro{background-position:-740px -440px}.ap-flag-rs{background-position:-740px -460px}.ap-flag-ru{background-position:-740px -480px}.ap-flag-rw{background-position:-740px -500px}.ap-flag-sa{background-position:-740px -520px}.ap-flag-sb{background-position:-740px -540px}.ap-flag-sc{background-position:-740px -560px}.ap-flag-sd{background-position:-740px -580px}.ap-flag-se{background-position:-740px -600px}.ap-flag-sg{background-position:-740px -620px}.ap-flag-sh{background-position:-740px -640px}.ap-flag-si{background-position:-740px -660px}.ap-flag-sj{background-position:-740px -680px}.ap-flag-sk{background-position:-740px -700px}.ap-flag-sl{background-position:-740px -720px}.ap-flag-sm{background-position:-740px -740px}.ap-flag-sn{background-position:-740px -760px}.ap-flag-so{background-position:-740px -780px}.ap-flag-sr{background-position:-740px -800px}.ap-flag-ss{background-position:-760px 0}.ap-flag-st{background-position:-760px -20px}.ap-flag-sv{background-position:-760px -40px}.ap-flag-sx{background-position:-760px -60px}.ap-flag-sy{background-position:-760px -80px}.ap-flag-sz{background-position:-760px -100px}.ap-flag-ta{background-position:-760px -120px}.ap-flag-tc{background-position:-760px -140px}.ap-flag-td{background-position:-760px -160px}.ap-flag-tf{background-position:-760px -180px}.ap-flag-tg{background-position:-760px -200px}.ap-flag-th{background-position:-760px -220px}.ap-flag-tj{background-position:-760px -240px}.ap-flag-tk{background-position:-760px -260px}.ap-flag-tl{background-position:-760px -280px}.ap-flag-tm{background-position:-760px -300px}.ap-flag-tn{background-position:-760px -320px}.ap-flag-to{background-position:-760px -340px}.ap-flag-tr{background-position:-760px -360px}.ap-flag-tt{background-position:-760px -380px}.ap-flag-tv{background-position:-760px -400px}.ap-flag-tw{background-position:-760px -420px}.ap-flag-tz{background-position:-760px -440px}.ap-flag-ua{background-position:-760px -460px}.ap-flag-ug{background-position:-760px -480px}.ap-flag-um{background-position:-760px -500px}.ap-flag-us{background-position:-760px -520px}.ap-flag-uy{background-position:-760px -540px}.ap-flag-uz{background-position:-760px -560px}.ap-flag-va{background-position:-760px -580px}.ap-flag-vc{background-position:-760px -600px}.ap-flag-ve{background-position:-760px -620px}.ap-flag-vg{background-position:-760px -640px}.ap-flag-vi{background-position:-760px -660px}.ap-flag-vn{background-position:-760px -680px}.ap-flag-vu{background-position:-760px -700px}.ap-flag-wf{background-position:-760px -720px}.ap-flag-ws{background-position:-760px -740px}.ap-flag-xk{background-position:-760px -760px}.ap-flag-ye{background-position:-760px -780px}.ap-flag-yt{background-position:-760px -800px}.ap-flag-za{background-position:-780px 0}.ap-flag-zm{background-position:-780px -20px}.ap-flag-zw{background-position:-780px -40px}.ap-man-man-boy{background-position:-780px -60px}.ap-man-man-boy-boy{background-position:-780px -80px}.ap-man-man-girl{background-position:-780px -100px}.ap-man-man-girl-boy{background-position:-780px -120px}.ap-man-man-girl-girl{background-position:-780px -140px}.ap-man-woman-boy-boy{background-position:-780px -160px}.ap-man-woman-girl{background-position:-780px -180px}.ap-man-woman-girl-boy{background-position:-780px -200px}.ap-man-woman-girl-girl{background-position:-780px -220px}.ap-man-heart-man{background-position:-780px -240px}.ap-man-kiss-man{background-position:-780px -260px}.ap-woman-woman-boy{background-position:-780px -280px}.ap-woman-woman-boy-boy{background-position:-780px -300px}.ap-woman-woman-girl{background-position:-780px -320px}.ap-woman-woman-girl-boy{background-position:-780px -340px}.ap-woman-woman-girl-girl{background-position:-780px -360px}.ap-woman-heart-woman{background-position:-780px -380px}.ap-woman-kiss-woman{background-position:-780px -400px}'''

QuillSnowCSS = r'''
/*!
 * Quill Editor v1.3.6
 * https://quilljs.com/
 * Copyright (c) 2014, Jason Chen
 * Copyright (c) 2013, salesforce.com
 */
.ql-container {
  box-sizing: border-box;
  font-family: Helvetica, Arial, sans-serif;
  font-size: 13px;
  height: 100%;
  margin: 0px;
  position: relative;
}
.ql-container.ql-disabled .ql-tooltip {
  visibility: hidden;
}
.ql-container.ql-disabled .ql-editor ul[data-checked] > li::before {
  pointer-events: none;
}
.ql-clipboard {
  left: -100000px;
  height: 1px;
  overflow-y: hidden;
  position: absolute;
  top: 50%;
}
.ql-clipboard p {
  margin: 0;
  padding: 0;
}
.ql-editor {
  box-sizing: border-box;
  line-height: 1.42;
  height: 100%;
  outline: none;
  overflow-y: auto;
  padding: 12px 15px;
  tab-size: 4;
  -moz-tab-size: 4;
  text-align: left;
  white-space: pre-wrap;
  word-wrap: break-word;
}
.ql-editor > * {
  cursor: text;
}
.ql-editor p,
.ql-editor ol,
.ql-editor ul,
.ql-editor pre,
.ql-editor blockquote,
.ql-editor h1,
.ql-editor h2,
.ql-editor h3,
.ql-editor h4,
.ql-editor h5,
.ql-editor h6 {
  margin: 0;
  padding: 0;
  counter-reset: list-1 list-2 list-3 list-4 list-5 list-6 list-7 list-8 list-9;
}
.ql-editor ol,
.ql-editor ul {
  padding-left: 1.5em;
}
.ql-editor ol > li,
.ql-editor ul > li {
  list-style-type: none;
}
.ql-editor ul > li::before {
  content: '\2022';
}
.ql-editor ul[data-checked=true],
.ql-editor ul[data-checked=false] {
  pointer-events: none;
}
.ql-editor ul[data-checked=true] > li *,
.ql-editor ul[data-checked=false] > li * {
  pointer-events: all;
}
.ql-editor ul[data-checked=true] > li::before,
.ql-editor ul[data-checked=false] > li::before {
  color: #777;
  cursor: pointer;
  pointer-events: all;
}
.ql-editor ul[data-checked=true] > li::before {
  content: '\2611';
}
.ql-editor ul[data-checked=false] > li::before {
  content: '\2610';
}
.ql-editor li::before {
  display: inline-block;
  white-space: nowrap;
  width: 1.2em;
}
.ql-editor li:not(.ql-direction-rtl)::before {
  margin-left: -1.5em;
  margin-right: 0.3em;
  text-align: right;
}
.ql-editor li.ql-direction-rtl::before {
  margin-left: 0.3em;
  margin-right: -1.5em;
}
.ql-editor ol li:not(.ql-direction-rtl),
.ql-editor ul li:not(.ql-direction-rtl) {
  padding-left: 1.5em;
}
.ql-editor ol li.ql-direction-rtl,
.ql-editor ul li.ql-direction-rtl {
  padding-right: 1.5em;
}
.ql-editor ol li {
  counter-reset: list-1 list-2 list-3 list-4 list-5 list-6 list-7 list-8 list-9;
  counter-increment: list-0;
}
.ql-editor ol li:before {
  content: counter(list-0, decimal) '. ';
}
.ql-editor ol li.ql-indent-1 {
  counter-increment: list-1;
}
.ql-editor ol li.ql-indent-1:before {
  content: counter(list-1, lower-alpha) '. ';
}
.ql-editor ol li.ql-indent-1 {
  counter-reset: list-2 list-3 list-4 list-5 list-6 list-7 list-8 list-9;
}
.ql-editor ol li.ql-indent-2 {
  counter-increment: list-2;
}
.ql-editor ol li.ql-indent-2:before {
  content: counter(list-2, lower-roman) '. ';
}
.ql-editor ol li.ql-indent-2 {
  counter-reset: list-3 list-4 list-5 list-6 list-7 list-8 list-9;
}
.ql-editor ol li.ql-indent-3 {
  counter-increment: list-3;
}
.ql-editor ol li.ql-indent-3:before {
  content: counter(list-3, decimal) '. ';
}
.ql-editor ol li.ql-indent-3 {
  counter-reset: list-4 list-5 list-6 list-7 list-8 list-9;
}
.ql-editor ol li.ql-indent-4 {
  counter-increment: list-4;
}
.ql-editor ol li.ql-indent-4:before {
  content: counter(list-4, lower-alpha) '. ';
}
.ql-editor ol li.ql-indent-4 {
  counter-reset: list-5 list-6 list-7 list-8 list-9;
}
.ql-editor ol li.ql-indent-5 {
  counter-increment: list-5;
}
.ql-editor ol li.ql-indent-5:before {
  content: counter(list-5, lower-roman) '. ';
}
.ql-editor ol li.ql-indent-5 {
  counter-reset: list-6 list-7 list-8 list-9;
}
.ql-editor ol li.ql-indent-6 {
  counter-increment: list-6;
}
.ql-editor ol li.ql-indent-6:before {
  content: counter(list-6, decimal) '. ';
}
.ql-editor ol li.ql-indent-6 {
  counter-reset: list-7 list-8 list-9;
}
.ql-editor ol li.ql-indent-7 {
  counter-increment: list-7;
}
.ql-editor ol li.ql-indent-7:before {
  content: counter(list-7, lower-alpha) '. ';
}
.ql-editor ol li.ql-indent-7 {
  counter-reset: list-8 list-9;
}
.ql-editor ol li.ql-indent-8 {
  counter-increment: list-8;
}
.ql-editor ol li.ql-indent-8:before {
  content: counter(list-8, lower-roman) '. ';
}
.ql-editor ol li.ql-indent-8 {
  counter-reset: list-9;
}
.ql-editor ol li.ql-indent-9 {
  counter-increment: list-9;
}
.ql-editor ol li.ql-indent-9:before {
  content: counter(list-9, decimal) '. ';
}
.ql-editor .ql-indent-1:not(.ql-direction-rtl) {
  padding-left: 3em;
}
.ql-editor li.ql-indent-1:not(.ql-direction-rtl) {
  padding-left: 4.5em;
}
.ql-editor .ql-indent-1.ql-direction-rtl.ql-align-right {
  padding-right: 3em;
}
.ql-editor li.ql-indent-1.ql-direction-rtl.ql-align-right {
  padding-right: 4.5em;
}
.ql-editor .ql-indent-2:not(.ql-direction-rtl) {
  padding-left: 6em;
}
.ql-editor li.ql-indent-2:not(.ql-direction-rtl) {
  padding-left: 7.5em;
}
.ql-editor .ql-indent-2.ql-direction-rtl.ql-align-right {
  padding-right: 6em;
}
.ql-editor li.ql-indent-2.ql-direction-rtl.ql-align-right {
  padding-right: 7.5em;
}
.ql-editor .ql-indent-3:not(.ql-direction-rtl) {
  padding-left: 9em;
}
.ql-editor li.ql-indent-3:not(.ql-direction-rtl) {
  padding-left: 10.5em;
}
.ql-editor .ql-indent-3.ql-direction-rtl.ql-align-right {
  padding-right: 9em;
}
.ql-editor li.ql-indent-3.ql-direction-rtl.ql-align-right {
  padding-right: 10.5em;
}
.ql-editor .ql-indent-4:not(.ql-direction-rtl) {
  padding-left: 12em;
}
.ql-editor li.ql-indent-4:not(.ql-direction-rtl) {
  padding-left: 13.5em;
}
.ql-editor .ql-indent-4.ql-direction-rtl.ql-align-right {
  padding-right: 12em;
}
.ql-editor li.ql-indent-4.ql-direction-rtl.ql-align-right {
  padding-right: 13.5em;
}
.ql-editor .ql-indent-5:not(.ql-direction-rtl) {
  padding-left: 15em;
}
.ql-editor li.ql-indent-5:not(.ql-direction-rtl) {
  padding-left: 16.5em;
}
.ql-editor .ql-indent-5.ql-direction-rtl.ql-align-right {
  padding-right: 15em;
}
.ql-editor li.ql-indent-5.ql-direction-rtl.ql-align-right {
  padding-right: 16.5em;
}
.ql-editor .ql-indent-6:not(.ql-direction-rtl) {
  padding-left: 18em;
}
.ql-editor li.ql-indent-6:not(.ql-direction-rtl) {
  padding-left: 19.5em;
}
.ql-editor .ql-indent-6.ql-direction-rtl.ql-align-right {
  padding-right: 18em;
}
.ql-editor li.ql-indent-6.ql-direction-rtl.ql-align-right {
  padding-right: 19.5em;
}
.ql-editor .ql-indent-7:not(.ql-direction-rtl) {
  padding-left: 21em;
}
.ql-editor li.ql-indent-7:not(.ql-direction-rtl) {
  padding-left: 22.5em;
}
.ql-editor .ql-indent-7.ql-direction-rtl.ql-align-right {
  padding-right: 21em;
}
.ql-editor li.ql-indent-7.ql-direction-rtl.ql-align-right {
  padding-right: 22.5em;
}
.ql-editor .ql-indent-8:not(.ql-direction-rtl) {
  padding-left: 24em;
}
.ql-editor li.ql-indent-8:not(.ql-direction-rtl) {
  padding-left: 25.5em;
}
.ql-editor .ql-indent-8.ql-direction-rtl.ql-align-right {
  padding-right: 24em;
}
.ql-editor li.ql-indent-8.ql-direction-rtl.ql-align-right {
  padding-right: 25.5em;
}
.ql-editor .ql-indent-9:not(.ql-direction-rtl) {
  padding-left: 27em;
}
.ql-editor li.ql-indent-9:not(.ql-direction-rtl) {
  padding-left: 28.5em;
}
.ql-editor .ql-indent-9.ql-direction-rtl.ql-align-right {
  padding-right: 27em;
}
.ql-editor li.ql-indent-9.ql-direction-rtl.ql-align-right {
  padding-right: 28.5em;
}
.ql-editor .ql-video {
  display: block;
  max-width: 100%;
}
.ql-editor .ql-video.ql-align-center {
  margin: 0 auto;
}
.ql-editor .ql-video.ql-align-right {
  margin: 0 0 0 auto;
}
.ql-editor .ql-bg-black {
  background-color: #000;
}
.ql-editor .ql-bg-red {
  background-color: #e60000;
}
.ql-editor .ql-bg-orange {
  background-color: #f90;
}
.ql-editor .ql-bg-yellow {
  background-color: #ff0;
}
.ql-editor .ql-bg-green {
  background-color: #008a00;
}
.ql-editor .ql-bg-blue {
  background-color: #06c;
}
.ql-editor .ql-bg-purple {
  background-color: #93f;
}
.ql-editor .ql-color-white {
  color: #fff;
}
.ql-editor .ql-color-red {
  color: #e60000;
}
.ql-editor .ql-color-orange {
  color: #f90;
}
.ql-editor .ql-color-yellow {
  color: #ff0;
}
.ql-editor .ql-color-green {
  color: #008a00;
}
.ql-editor .ql-color-blue {
  color: #06c;
}
.ql-editor .ql-color-purple {
  color: #93f;
}
.ql-editor .ql-font-serif {
  font-family: Georgia, Times New Roman, serif;
}
.ql-editor .ql-font-monospace {
  font-family: Monaco, Courier New, monospace;
}
.ql-editor .ql-size-small {
  font-size: 0.75em;
}
.ql-editor .ql-size-large {
  font-size: 1.5em;
}
.ql-editor .ql-size-huge {
  font-size: 2.5em;
}
.ql-editor .ql-direction-rtl {
  direction: rtl;
  text-align: inherit;
}
.ql-editor .ql-align-center {
  text-align: center;
}
.ql-editor .ql-align-justify {
  text-align: justify;
}
.ql-editor .ql-align-right {
  text-align: right;
}
.ql-editor.ql-blank::before {
  color: rgba(0,0,0,0.6);
  content: attr(data-placeholder);
  font-style: italic;
  left: 15px;
  pointer-events: none;
  position: absolute;
  right: 15px;
}
.ql-snow.ql-toolbar:after,
.ql-snow .ql-toolbar:after {
  clear: both;
  content: '';
  display: table;
}
.ql-snow.ql-toolbar button,
.ql-snow .ql-toolbar button {
  background: none;
  border: none;
  cursor: pointer;
  display: inline-block;
  float: left;
  height: 24px;
  padding: 3px 5px;
  width: 28px;
}
.ql-snow.ql-toolbar button svg,
.ql-snow .ql-toolbar button svg {
  float: left;
  height: 100%;
}
.ql-snow.ql-toolbar button:active:hover,
.ql-snow .ql-toolbar button:active:hover {
  outline: none;
}
.ql-snow.ql-toolbar input.ql-image[type=file],
.ql-snow .ql-toolbar input.ql-image[type=file] {
  display: none;
}
.ql-snow.ql-toolbar button:hover,
.ql-snow .ql-toolbar button:hover,
.ql-snow.ql-toolbar button:focus,
.ql-snow .ql-toolbar button:focus,
.ql-snow.ql-toolbar button.ql-active,
.ql-snow .ql-toolbar button.ql-active,
.ql-snow.ql-toolbar .ql-picker-label:hover,
.ql-snow .ql-toolbar .ql-picker-label:hover,
.ql-snow.ql-toolbar .ql-picker-label.ql-active,
.ql-snow .ql-toolbar .ql-picker-label.ql-active,
.ql-snow.ql-toolbar .ql-picker-item:hover,
.ql-snow .ql-toolbar .ql-picker-item:hover,
.ql-snow.ql-toolbar .ql-picker-item.ql-selected,
.ql-snow .ql-toolbar .ql-picker-item.ql-selected {
  color: #06c;
}
.ql-snow.ql-toolbar button:hover .ql-fill,
.ql-snow .ql-toolbar button:hover .ql-fill,
.ql-snow.ql-toolbar button:focus .ql-fill,
.ql-snow .ql-toolbar button:focus .ql-fill,
.ql-snow.ql-toolbar button.ql-active .ql-fill,
.ql-snow .ql-toolbar button.ql-active .ql-fill,
.ql-snow.ql-toolbar .ql-picker-label:hover .ql-fill,
.ql-snow .ql-toolbar .ql-picker-label:hover .ql-fill,
.ql-snow.ql-toolbar .ql-picker-label.ql-active .ql-fill,
.ql-snow .ql-toolbar .ql-picker-label.ql-active .ql-fill,
.ql-snow.ql-toolbar .ql-picker-item:hover .ql-fill,
.ql-snow .ql-toolbar .ql-picker-item:hover .ql-fill,
.ql-snow.ql-toolbar .ql-picker-item.ql-selected .ql-fill,
.ql-snow .ql-toolbar .ql-picker-item.ql-selected .ql-fill,
.ql-snow.ql-toolbar button:hover .ql-stroke.ql-fill,
.ql-snow .ql-toolbar button:hover .ql-stroke.ql-fill,
.ql-snow.ql-toolbar button:focus .ql-stroke.ql-fill,
.ql-snow .ql-toolbar button:focus .ql-stroke.ql-fill,
.ql-snow.ql-toolbar button.ql-active .ql-stroke.ql-fill,
.ql-snow .ql-toolbar button.ql-active .ql-stroke.ql-fill,
.ql-snow.ql-toolbar .ql-picker-label:hover .ql-stroke.ql-fill,
.ql-snow .ql-toolbar .ql-picker-label:hover .ql-stroke.ql-fill,
.ql-snow.ql-toolbar .ql-picker-label.ql-active .ql-stroke.ql-fill,
.ql-snow .ql-toolbar .ql-picker-label.ql-active .ql-stroke.ql-fill,
.ql-snow.ql-toolbar .ql-picker-item:hover .ql-stroke.ql-fill,
.ql-snow .ql-toolbar .ql-picker-item:hover .ql-stroke.ql-fill,
.ql-snow.ql-toolbar .ql-picker-item.ql-selected .ql-stroke.ql-fill,
.ql-snow .ql-toolbar .ql-picker-item.ql-selected .ql-stroke.ql-fill {
  fill: #06c;
}
.ql-snow.ql-toolbar button:hover .ql-stroke,
.ql-snow .ql-toolbar button:hover .ql-stroke,
.ql-snow.ql-toolbar button:focus .ql-stroke,
.ql-snow .ql-toolbar button:focus .ql-stroke,
.ql-snow.ql-toolbar button.ql-active .ql-stroke,
.ql-snow .ql-toolbar button.ql-active .ql-stroke,
.ql-snow.ql-toolbar .ql-picker-label:hover .ql-stroke,
.ql-snow .ql-toolbar .ql-picker-label:hover .ql-stroke,
.ql-snow.ql-toolbar .ql-picker-label.ql-active .ql-stroke,
.ql-snow .ql-toolbar .ql-picker-label.ql-active .ql-stroke,
.ql-snow.ql-toolbar .ql-picker-item:hover .ql-stroke,
.ql-snow .ql-toolbar .ql-picker-item:hover .ql-stroke,
.ql-snow.ql-toolbar .ql-picker-item.ql-selected .ql-stroke,
.ql-snow .ql-toolbar .ql-picker-item.ql-selected .ql-stroke,
.ql-snow.ql-toolbar button:hover .ql-stroke-miter,
.ql-snow .ql-toolbar button:hover .ql-stroke-miter,
.ql-snow.ql-toolbar button:focus .ql-stroke-miter,
.ql-snow .ql-toolbar button:focus .ql-stroke-miter,
.ql-snow.ql-toolbar button.ql-active .ql-stroke-miter,
.ql-snow .ql-toolbar button.ql-active .ql-stroke-miter,
.ql-snow.ql-toolbar .ql-picker-label:hover .ql-stroke-miter,
.ql-snow .ql-toolbar .ql-picker-label:hover .ql-stroke-miter,
.ql-snow.ql-toolbar .ql-picker-label.ql-active .ql-stroke-miter,
.ql-snow .ql-toolbar .ql-picker-label.ql-active .ql-stroke-miter,
.ql-snow.ql-toolbar .ql-picker-item:hover .ql-stroke-miter,
.ql-snow .ql-toolbar .ql-picker-item:hover .ql-stroke-miter,
.ql-snow.ql-toolbar .ql-picker-item.ql-selected .ql-stroke-miter,
.ql-snow .ql-toolbar .ql-picker-item.ql-selected .ql-stroke-miter {
  stroke: #06c;
}
@media (pointer: coarse) {
  .ql-snow.ql-toolbar button:hover:not(.ql-active),
  .ql-snow .ql-toolbar button:hover:not(.ql-active) {
    color: #444;
  }
  .ql-snow.ql-toolbar button:hover:not(.ql-active) .ql-fill,
  .ql-snow .ql-toolbar button:hover:not(.ql-active) .ql-fill,
  .ql-snow.ql-toolbar button:hover:not(.ql-active) .ql-stroke.ql-fill,
  .ql-snow .ql-toolbar button:hover:not(.ql-active) .ql-stroke.ql-fill {
    fill: #444;
  }
  .ql-snow.ql-toolbar button:hover:not(.ql-active) .ql-stroke,
  .ql-snow .ql-toolbar button:hover:not(.ql-active) .ql-stroke,
  .ql-snow.ql-toolbar button:hover:not(.ql-active) .ql-stroke-miter,
  .ql-snow .ql-toolbar button:hover:not(.ql-active) .ql-stroke-miter {
    stroke: #444;
  }
}
.ql-snow {
  box-sizing: border-box;
}
.ql-snow * {
  box-sizing: border-box;
}
.ql-snow .ql-hidden {
  display: none;
}
.ql-snow .ql-out-bottom,
.ql-snow .ql-out-top {
  visibility: hidden;
}
.ql-snow .ql-tooltip {
  position: absolute;
  transform: translateY(10px);
}
.ql-snow .ql-tooltip a {
  cursor: pointer;
  text-decoration: none;
}
.ql-snow .ql-tooltip.ql-flip {
  transform: translateY(-10px);
}
.ql-snow .ql-formats {
  display: inline-block;
  vertical-align: middle;
}
.ql-snow .ql-formats:after {
  clear: both;
  content: '';
  display: table;
}
.ql-snow .ql-stroke {
  fill: none;
  stroke: #444;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 2;
}
.ql-snow .ql-stroke-miter {
  fill: none;
  stroke: #444;
  stroke-miterlimit: 10;
  stroke-width: 2;
}
.ql-snow .ql-fill,
.ql-snow .ql-stroke.ql-fill {
  fill: #444;
}
.ql-snow .ql-empty {
  fill: none;
}
.ql-snow .ql-even {
  fill-rule: evenodd;
}
.ql-snow .ql-thin,
.ql-snow .ql-stroke.ql-thin {
  stroke-width: 1;
}
.ql-snow .ql-transparent {
  opacity: 0.4;
}
.ql-snow .ql-direction svg:last-child {
  display: none;
}
.ql-snow .ql-direction.ql-active svg:last-child {
  display: inline;
}
.ql-snow .ql-direction.ql-active svg:first-child {
  display: none;
}
.ql-snow .ql-editor h1 {
  font-size: 2em;
}
.ql-snow .ql-editor h2 {
  font-size: 1.5em;
}
.ql-snow .ql-editor h3 {
  font-size: 1.17em;
}
.ql-snow .ql-editor h4 {
  font-size: 1em;
}
.ql-snow .ql-editor h5 {
  font-size: 0.83em;
}
.ql-snow .ql-editor h6 {
  font-size: 0.67em;
}
.ql-snow .ql-editor a {
  text-decoration: underline;
}
.ql-snow .ql-editor blockquote {
  border-left: 4px solid #ccc;
  margin-bottom: 5px;
  margin-top: 5px;
  padding-left: 16px;
}
.ql-snow .ql-editor code,
.ql-snow .ql-editor pre {
  background-color: #f0f0f0;
  border-radius: 3px;
}
.ql-snow .ql-editor pre {
  white-space: pre-wrap;
  margin-bottom: 5px;
  margin-top: 5px;
  padding: 5px 10px;
}
.ql-snow .ql-editor code {
  font-size: 85%;
  padding: 2px 4px;
}
.ql-snow .ql-editor pre.ql-syntax {
  background-color: #23241f;
  color: #f8f8f2;
  overflow: visible;
}
.ql-snow .ql-editor img {
  max-width: 100%;
}
.ql-snow .ql-picker {
  color: #444;
  display: inline-block;
  float: left;
  font-size: 14px;
  font-weight: 500;
  height: 24px;
  position: relative;
  vertical-align: middle;
}
.ql-snow .ql-picker-label {
  cursor: pointer;
  display: inline-block;
  height: 100%;
  padding-left: 8px;
  padding-right: 2px;
  position: relative;
  width: 100%;
}
.ql-snow .ql-picker-label::before {
  display: inline-block;
  line-height: 22px;
}
.ql-snow .ql-picker-options {
  background-color: #fff;
  display: none;
  min-width: 100%;
  padding: 4px 8px;
  position: absolute;
  white-space: nowrap;
}
.ql-snow .ql-picker-options .ql-picker-item {
  cursor: pointer;
  display: block;
  padding-bottom: 5px;
  padding-top: 5px;
}
.ql-snow .ql-picker.ql-expanded .ql-picker-label {
  color: #ccc;
  z-index: 2;
}
.ql-snow .ql-picker.ql-expanded .ql-picker-label .ql-fill {
  fill: #ccc;
}
.ql-snow .ql-picker.ql-expanded .ql-picker-label .ql-stroke {
  stroke: #ccc;
}
.ql-snow .ql-picker.ql-expanded .ql-picker-options {
  display: block;
  margin-top: -1px;
  top: 100%;
  z-index: 1;
}
.ql-snow .ql-color-picker,
.ql-snow .ql-icon-picker {
  width: 28px;
}
.ql-snow .ql-color-picker .ql-picker-label,
.ql-snow .ql-icon-picker .ql-picker-label {
  padding: 2px 4px;
}
.ql-snow .ql-color-picker .ql-picker-label svg,
.ql-snow .ql-icon-picker .ql-picker-label svg {
  right: 4px;
}
.ql-snow .ql-icon-picker .ql-picker-options {
  padding: 4px 0px;
}
.ql-snow .ql-icon-picker .ql-picker-item {
  height: 24px;
  width: 24px;
  padding: 2px 4px;
}
.ql-snow .ql-color-picker .ql-picker-options {
  padding: 3px 5px;
  width: 152px;
}
.ql-snow .ql-color-picker .ql-picker-item {
  border: 1px solid transparent;
  float: left;
  height: 16px;
  margin: 2px;
  padding: 0px;
  width: 16px;
}
.ql-snow .ql-picker:not(.ql-color-picker):not(.ql-icon-picker) svg {
  position: absolute;
  margin-top: -9px;
  right: 0;
  top: 50%;
  width: 18px;
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-label]:not([data-label=''])::before,
.ql-snow .ql-picker.ql-font .ql-picker-label[data-label]:not([data-label=''])::before,
.ql-snow .ql-picker.ql-size .ql-picker-label[data-label]:not([data-label=''])::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-label]:not([data-label=''])::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-label]:not([data-label=''])::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-label]:not([data-label=''])::before {
  content: attr(data-label);
}
.ql-snow .ql-picker.ql-header {
  width: 98px;
}
.ql-snow .ql-picker.ql-header .ql-picker-label::before,
.ql-snow .ql-picker.ql-header .ql-picker-item::before {
  content: 'Normal';
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="1"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="1"]::before {
  content: 'Heading 1';
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="2"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="2"]::before {
  content: 'Heading 2';
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="3"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="3"]::before {
  content: 'Heading 3';
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="4"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="4"]::before {
  content: 'Heading 4';
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="5"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="5"]::before {
  content: 'Heading 5';
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="6"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="6"]::before {
  content: 'Heading 6';
}
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="1"]::before {
  font-size: 2em;
}
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="2"]::before {
  font-size: 1.5em;
}
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="3"]::before {
  font-size: 1.17em;
}
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="4"]::before {
  font-size: 1em;
}
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="5"]::before {
  font-size: 0.83em;
}
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="6"]::before {
  font-size: 0.67em;
}
.ql-snow .ql-picker.ql-font {
  width: 108px;
}
.ql-snow .ql-picker.ql-font .ql-picker-label::before,
.ql-snow .ql-picker.ql-font .ql-picker-item::before {
  content: 'Sans Serif';
}
.ql-snow .ql-picker.ql-font .ql-picker-label[data-value=serif]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value=serif]::before {
  content: 'Serif';
}
.ql-snow .ql-picker.ql-font .ql-picker-label[data-value=monospace]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value=monospace]::before {
  content: 'Monospace';
}
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value=serif]::before {
  font-family: Georgia, Times New Roman, serif;
}
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value=monospace]::before {
  font-family: Monaco, Courier New, monospace;
}
.ql-snow .ql-picker.ql-size {
  width: 98px;
}
.ql-snow .ql-picker.ql-size .ql-picker-label::before,
.ql-snow .ql-picker.ql-size .ql-picker-item::before {
  content: 'Normal';
}
.ql-snow .ql-picker.ql-size .ql-picker-label[data-value=small]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value=small]::before {
  content: 'Small';
}
.ql-snow .ql-picker.ql-size .ql-picker-label[data-value=large]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value=large]::before {
  content: 'Large';
}
.ql-snow .ql-picker.ql-size .ql-picker-label[data-value=huge]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value=huge]::before {
  content: 'Huge';
}
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value=small]::before {
  font-size: 10px;
}
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value=large]::before {
  font-size: 18px;
}
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value=huge]::before {
  font-size: 32px;
}
.ql-snow .ql-color-picker.ql-background .ql-picker-item {
  background-color: #fff;
}
.ql-snow .ql-color-picker.ql-color .ql-picker-item {
  background-color: #000;
}
.ql-toolbar.ql-snow {
  border: 1px solid #ccc;
  box-sizing: border-box;
  font-family: 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;
  padding: 8px;
}
.ql-toolbar.ql-snow .ql-formats {
  margin-right: 15px;
}
.ql-toolbar.ql-snow .ql-picker-label {
  border: 1px solid transparent;
}
.ql-toolbar.ql-snow .ql-picker-options {
  border: 1px solid transparent;
  box-shadow: rgba(0,0,0,0.2) 0 2px 8px;
}
.ql-toolbar.ql-snow .ql-picker.ql-expanded .ql-picker-label {
  border-color: #ccc;
}
.ql-toolbar.ql-snow .ql-picker.ql-expanded .ql-picker-options {
  border-color: #ccc;
}
.ql-toolbar.ql-snow .ql-color-picker .ql-picker-item.ql-selected,
.ql-toolbar.ql-snow .ql-color-picker .ql-picker-item:hover {
  border-color: #000;
}
.ql-toolbar.ql-snow + .ql-container.ql-snow {
  border-top: 0px;
}
.ql-snow .ql-tooltip {
  background-color: #fff;
  border: 1px solid #ccc;
  box-shadow: 0px 0px 5px #ddd;
  color: #444;
  padding: 5px 12px;
  white-space: nowrap;
}
.ql-snow .ql-tooltip::before {
  content: "Visit URL:";
  line-height: 26px;
  margin-right: 8px;
}
.ql-snow .ql-tooltip input[type=text] {
  display: none;
  border: 1px solid #ccc;
  font-size: 13px;
  height: 26px;
  margin: 0px;
  padding: 3px 5px;
  width: 170px;
}
.ql-snow .ql-tooltip a.ql-preview {
  display: inline-block;
  max-width: 200px;
  overflow-x: hidden;
  text-overflow: ellipsis;
  vertical-align: top;
}
.ql-snow .ql-tooltip a.ql-action::after {
  border-right: 1px solid #ccc;
  content: 'Edit';
  margin-left: 16px;
  padding-right: 8px;
}
.ql-snow .ql-tooltip a.ql-remove::before {
  content: 'Remove';
  margin-left: 8px;
}
.ql-snow .ql-tooltip a {
  line-height: 26px;
}
.ql-snow .ql-tooltip.ql-editing a.ql-preview,
.ql-snow .ql-tooltip.ql-editing a.ql-remove {
  display: none;
}
.ql-snow .ql-tooltip.ql-editing input[type=text] {
  display: inline-block;
}
.ql-snow .ql-tooltip.ql-editing a.ql-action::after {
  border-right: 0px;
  content: 'Save';
  padding-right: 0px;
}
.ql-snow .ql-tooltip[data-mode=link]::before {
  content: "Enter link:";
}
.ql-snow .ql-tooltip[data-mode=formula]::before {
  content: "Enter formula:";
}
.ql-snow .ql-tooltip[data-mode=video]::before {
  content: "Enter video:";
}
.ql-snow a {
  color: #06c;
}
.ql-container.ql-snow {
  border: 1px solid #ccc;
}'''