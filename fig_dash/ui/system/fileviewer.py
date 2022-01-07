#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import Union
from pathlib import Path
# fig-dash imports.
from fig_dash import FigD
from fig_dash.ui.browser import DebugWebView
from fig_dash.ui.js.webchannel import QWebChannelJS
# PyQt5 imports
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor, QKeySequence
from PyQt5.QtCore import Qt, QSize, QFileInfo, QUrl, QMimeDatabase, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget, QApplication, QErrorMessage, QLabel, QToolBar, QToolButton, QSizePolicy, QFrame, QAction, QActionGroup, QShortcut, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QFileIconProvider
# filweviewer widget.
ViSelectJS = r'''/*! @viselect/vanilla 3.0.0-beta.13 MIT | https://github.com/Simonwep/selection */
const t=(t,e="px")=>"number"==typeof t?t+e:t;function e({style:e},s,i){if("object"==typeof s)for(const[i,o]of Object.entries(s))e[i]=t(o);else void 0!==i&&(e[s]=t(i))}function s(t){return(e,s,i,o={})=>{e instanceof HTMLCollection||e instanceof NodeList?e=Array.from(e):Array.isArray(e)||(e=[e]),Array.isArray(s)||(s=[s]);for(const n of e)for(const e of s)n[t](e,i,{capture:!1,...o});return[e,s,i,o]}}const i=s("addEventListener"),o=s("removeEventListener"),n=t=>{const e=t.touches&&t.touches[0]||t;return{tap:e,x:e.clientX,y:e.clientY,target:e.target}};function r(t){let e=t.path||t.composedPath&&t.composedPath();if(e)return e;let s=t.target.parentElement;for(e=[t.target,s];s=s.parentElement;)e.push(s);return e.push(document,window),e}function h(t,e,s="touch"){switch(s){case"center":{const s=e.left+e.width/2,i=e.top+e.height/2;return s>=t.left&&s<=t.right&&i>=t.top&&i<=t.bottom}case"cover":return e.left>=t.left&&e.top>=t.top&&e.right<=t.right&&e.bottom<=t.bottom;case"touch":return t.right>=e.left&&t.left<=e.right&&t.bottom>=e.top&&t.top<=e.bottom;default:throw new Error(`Unkown intersection mode: ${s}`)}}function c(t,e){const s=t.indexOf(e);~s&&t.splice(s,1)}function a(t,e=document){const s=Array.isArray(t)?t:[t],i=[];for(let t=0,o=s.length;t<o;t++){const o=s[t];"string"==typeof o?i.push(...Array.from(e.querySelectorAll(o))):o instanceof Element&&i.push(o)}return i}const l=()=>matchMedia("(hover: none), (pointer: coarse)").matches,u=(t,e)=>{for(const[s,i]of Object.entries(t)){const o=e[s];t[s]=void 0===o?t[s]:"object"!=typeof o||"object"!=typeof i||null===i||Array.isArray(i)?o:u(i,o)}return t},{abs:d,max:p,min:f,ceil:m}=Math;class SelectionArea extends class{constructor(){this.t=new Map,this.on=this.addEventListener,this.off=this.removeEventListener,this.emit=this.dispatchEvent}addEventListener(t,e){const s=this.t.get(t)||new Set;return this.t.set(t,s),s.add(e),this}removeEventListener(t,e){return this.t.get(t)?.delete(e),this}dispatchEvent(t,...e){let s=!0;for(const i of this.t.get(t)||[])s=!1!==i(...e)&&s;return s}unbindAllListeners(){this.t.clear()}}{constructor(t){super(),this.i={touched:[],stored:[],selected:[],changed:{added:[],removed:[]}},this.o=[],this.h=new DOMRect,this.l={y1:0,x2:0,y2:0,x1:0},this.u=!0,this.p=!0,this.m={x:0,y:0},this.v={x:0,y:0},this.disable=this.g.bind(this,!1),this.enable=this.g,this._=u({selectionAreaClass:"selection-area",selectionContainerClass:void 0,selectables:[],document:window.document,behaviour:{overlap:"invert",intersect:"touch",startThreshold:{x:10,y:10},scrolling:{speedDivider:10,manualSpeed:750,startScrollMargins:{x:0,y:0}}},features:{range:!0,touch:!0,singleTap:{allow:!0,intersect:"native"}},startAreas:["html"],boundaries:["html"],container:"body"},t);for(const t of Object.getOwnPropertyNames(Object.getPrototypeOf(this)))"function"==typeof this[t]&&(this[t]=this[t].bind(this));const{document:s,selectionAreaClass:i,selectionContainerClass:o}=this._;this.S=s.createElement("div"),this.A=s.createElement("div"),this.A.appendChild(this.S),this.S.classList.add(i),o&&this.A.classList.add(o),e(this.S,{willChange:"top, left, bottom, right, width, height",top:0,left:0,position:"fixed"}),e(this.A,{overflow:"hidden",position:"fixed",transform:"translate3d(0, 0, 0)",pointerEvents:"none",zIndex:"1"}),this.T=(t=>{let e,s=-1,i=!1;return{next(...o){e=o,i||(i=!0,s=requestAnimationFrame((()=>{t(...e),i=!1})))},cancel(){cancelAnimationFrame(s),i=!1}}})((t=>{this.L(),this.C(),this.M("move",t),this.j()})),this.enable()}g(t=!0){const{document:e,features:s}=this._,n=t?i:o;n(e,"mousedown",this.k),s.touch&&n(e,"touchstart",this.k,{passive:!1})}k(t,e=!1){const{x:s,y:o,target:c}=n(t),{_:l}=this,{document:u}=this._,d=c.getBoundingClientRect(),p=a(l.startAreas,l.document),f=a(l.boundaries,l.document);this.O=f.find((t=>h(t.getBoundingClientRect(),d)));const m=r(t);if(!this.O||!p.find((t=>m.includes(t)))||!f.find((t=>m.includes(t))))return;if(!e&&!1===this.M("beforestart",t))return;this.l={x1:s,y1:o,x2:0,y2:0};const v=u.scrollingElement||u.body;this.v={x:v.scrollLeft,y:v.scrollTop},this.u=!0,this.clearSelection(!1),i(u,["touchmove","mousemove"],this.R,{passive:!1}),i(u,["mouseup","touchcancel","touchend"],this.$),i(u,"scroll",this.D)}F(t){const{singleTap:{intersect:e},range:s}=this._.features,i=n(t);let o=null;if("native"===e)o=i.target;else if("touch"===e){this.resolveSelectables();const{x:t,y:e}=i;o=this.o.find((s=>{const{right:i,left:o,top:n,bottom:r}=s.getBoundingClientRect();return t<i&&t>o&&e<r&&e>n}))}if(!o)return;for(this.resolveSelectables();!this.o.includes(o);){if(!o.parentElement)return;o=o.parentElement}const{stored:r}=this.i;if(this.M("start",t),t.shiftKey&&r.length&&s){const t=this.q??r[0],[e,s]=4&t.compareDocumentPosition(o)?[o,t]:[t,o],i=[...this.o.filter((t=>4&t.compareDocumentPosition(e)&&2&t.compareDocumentPosition(s))),e,s];this.select(i)}else r.includes(o)&&(1===r.length||t.ctrlKey||r.every((t=>this.i.stored.includes(t))))?this.deselect(o):(this.q=o,this.select(o));this.M("stop",t)}R(t){const{container:s,document:r,features:h,behaviour:{startThreshold:c}}=this._,{x1:u,y1:p}=this.l,{x:f,y:m}=n(t),v=typeof c;if("number"===v&&d(f+m-(u+p))>=c||"object"===v&&d(f-u)>=c.x||d(m-p)>=c.y){if(o(r,["mousemove","touchmove"],this.R,{passive:!1}),!1===this.M("beforedrag",t))return void o(r,["mouseup","touchcancel","touchend"],this.$);i(r,["mousemove","touchmove"],this.H,{passive:!1}),e(this.S,"display","block"),a(s,r)[0].appendChild(this.A),this.resolveSelectables(),this.u=!1,this.W=this.O.getBoundingClientRect(),this.p=this.O.scrollHeight!==this.O.clientHeight||this.O.scrollWidth!==this.O.clientWidth,this.p&&(i(r,"wheel",this.I,{passive:!1}),this.o=this.o.filter((t=>this.O.contains(t)))),this.N(),this.M("start",t),this.H(t)}h.touch&&l()&&t.preventDefault()}N(){const{A:t,O:s,S:i}=this,o=this.W=s.getBoundingClientRect();this.p?(e(t,{top:o.top,left:o.left,width:o.width,height:o.height}),e(i,{marginTop:-o.top,marginLeft:-o.left})):(e(t,{top:0,left:0,width:"100%",height:"100%"}),e(i,{marginTop:0,marginLeft:0}))}H(t){const{x:e,y:s}=n(t),{m:i,l:o,_:r,T:h}=this,{features:c}=r,{speedDivider:a}=r.behaviour.scrolling,u=this.O;if(o.x2=e,o.y2=s,this.p&&(i.y||i.x)){const e=()=>{if(!i.x&&!i.y)return;const{scrollTop:s,scrollLeft:n}=u;i.y&&(u.scrollTop+=m(i.y/a),o.y1-=u.scrollTop-s),i.x&&(u.scrollLeft+=m(i.x/a),o.x1-=u.scrollLeft-n),h.next(t),requestAnimationFrame(e)};requestAnimationFrame(e)}else h.next(t);c.touch&&l()&&t.preventDefault()}D(){const{v:t,_:{document:e}}=this,{scrollTop:s,scrollLeft:i}=e.scrollingElement||e.body;this.l.x1+=t.x-i,this.l.y1+=t.y-s,t.x=i,t.y=s,this.N(),this.T.next(null)}I(t){const{manualSpeed:e}=this._.behaviour.scrolling,s=t.deltaY?t.deltaY>0?1:-1:0,i=t.deltaX?t.deltaX>0?1:-1:0;this.m.y+=s*e,this.m.x+=i*e,this.H(t),t.preventDefault()}L(){const{m:t,l:e,h:s,O:i,W:o,_:n}=this,{scrollTop:r,scrollHeight:h,clientHeight:c,scrollLeft:a,scrollWidth:l,clientWidth:u}=i,m=o,{x1:v,y1:g}=e;let{x2:y,y2:_}=e;const{behaviour:{scrolling:{startScrollMargins:x}}}=n;y<m.left+x.x?(t.x=a?-d(m.left-y+x.x):0,y=y<m.left?m.left:y):y>m.right-x.x?(t.x=l-a-u?d(m.left+m.width-y-x.x):0,y=y>m.right?m.right:y):t.x=0,_<m.top+x.y?(t.y=r?-d(m.top-_+x.y):0,_=_<m.top?m.top:_):_>m.bottom-x.y?(t.y=h-r-c?d(m.top+m.height-_-x.y):0,_=_>m.bottom?m.bottom:_):t.y=0;const b=f(v,y),S=f(g,_),w=p(v,y),A=p(g,_);s.x=b,s.y=S,s.width=w-b,s.height=A-S}j(){const{x:t,y:e,width:s,height:i}=this.h,{style:o}=this.S;o.left=`${t}px`,o.top=`${e}px`,o.width=`${s}px`,o.height=`${i}px`}$(t,s){const{document:i,features:n}=this._,{u:r}=this;o(i,["mousemove","touchmove"],this.R),o(i,["touchmove","mousemove"],this.H),o(i,["mouseup","touchcancel","touchend"],this.$),o(i,"scroll",this.D),t&&r&&n.singleTap.allow?this.F(t):r||s||(this.C(),this.M("stop",t)),this.m.x=0,this.m.y=0,this.p&&o(i,"wheel",this.I,{passive:!0}),this.A.remove(),this.T?.cancel(),e(this.S,"display","none"),this.U()}C(){const{o:t,_:e,i:s,h:i}=this,{stored:o,selected:n,touched:r}=s,{intersect:c,overlap:a}=e.behaviour,l="invert"===a,u=[],d=[],p=[];for(let e=0;e<t.length;e++){const s=t[e];if(h(i,s.getBoundingClientRect(),c)){if(n.includes(s))o.includes(s)&&!r.includes(s)&&r.push(s);else{if(l&&o.includes(s)){p.push(s);continue}d.push(s)}u.push(s)}}l&&d.push(...o.filter((t=>!n.includes(t))));const f="keep"===a;for(let t=0;t<n.length;t++){const e=n[t];u.includes(e)||f&&o.includes(e)||p.push(e)}s.selected=u,s.changed={added:d,removed:p},this.q=u[u.length-1]}M(t,e){return this.emit(t,{event:e,store:this.i,selection:this})}U(){const{_:t,i:e}=this,{selected:s,changed:i,touched:o,stored:n}=e,r=s.filter((t=>!n.includes(t)));switch(t.behaviour.overlap){case"drop":e.stored=[...r,...n.filter((t=>!o.includes(t)))];break;case"invert":e.stored=[...r,...n.filter((t=>!i.removed.includes(t)))];break;case"keep":e.stored=[...n,...s.filter((t=>!n.includes(t)))]}}trigger(t,e=!0){this.k(t,e)}resolveSelectables(){this.o=a(this._.selectables,this._.document)}clearSelection(t=!0){this.i={stored:t?[]:this.i.stored,selected:[],touched:[],changed:{added:[],removed:[]}}}getSelection(){return this.i.stored}getSelectionArea(){return this.S}cancel(t=!1){this.$(null,!t)}destroy(){this.cancel(),this.disable(),this.A.remove(),super.unbindAllListeners()}select(t,e=!1){const{changed:s,selected:i,stored:o}=this.i,n=a(t,this._.document).filter((t=>!i.includes(t)&&!o.includes(t)));return o.push(...n),i.push(...n),s.added.push(...n),!e&&this.M("move",null),n}deselect(t,e=!1){const{selected:s,stored:i,changed:o}=this.i;return!(!s.includes(t)&&!i.includes(t))&&(o.removed.push(t),c(i,t),c(s,t),!e&&this.M("move",null),!0)}}SelectionArea.version="3.0.0-beta.13";export{SelectionArea as default};
//'''# sourceMappingURL=selection.min.js.map

FileViewerStyle = r'''
::-webkit-scrollbar {
    width: 0.5em;
    height: 0.55em;
    background: transparent;
}

::-webkit-scrollbar-corner {
    display: none;
}

:root {
    --c-text: #42445a;
    --c-primary: #337bff;
    --c-primary-accent: #5084e2;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html,
body {
    height: 100%;
}

body {
    color: {{ FONT_COLOR }};
    font-weight: bold;
    background: rgb(72,72,72);
    background: linear-gradient(-45deg, rgba(72,72,72,1) 30%, rgba(41,41,41,1) 60%);
    font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji;
    /* backdrop-filter: blur(10px); */
    backdrop-filter: brightness(30%) blur(2px);
    background-image: url('{{ BACKGROUND_IMAGE }}');
    background-position: center;
}

*::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}
*::-webkit-scrollbar-track:hover {
    background: rgba(29, 29, 29, 0.4);
}    
*::-webkit-scrollbar-track {
    /* background-color: rgba(235, 235, 235, 0.8); */
    background: linear-gradient(0deg, rgba(235,95,52,0.8) 0%, rgba(235,204,52,1) 94%);
}
*::-webkit-scrollbar-thumb {
    background-color: #292929;
}
*::-webkit-scrollbar-thumb:hover {
    background: rgb(235,95,52);
    background: linear-gradient(0deg, rgba(235,95,52,1) 40%, rgba(235,204,52,1) 94%);
}
*::-webkit-scrollbar-corner {
    background-color: transparent;
    /* background: rgba(235, 235, 235, 0.1); */
}

header {
    text-align: center;
    font-size: 2.5em;
    padding: 1.2em 0 0.5em 0;
}

header h1 {
    font-size: 1em;
    font-weight: normal;
    color: var(--c-text);
}

header a {
    display: inline-flex;
    align-items: center;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.3em;
    color: white;
    margin-top: 5vh;
    padding: 0.75em 1.25em;
    transition: 0.3s all;
    background: var(--c-primary);
    border-radius: 50em;
    box-shadow: 0 1px 5px var(--c-primary-accent);
}

header a svg {
    width: 24px;
    height: 24px;
    margin-right: 0.75rem;
}

header a:hover {
    filter: brightness(1.1);
    box-shadow: 0 2px 8px var(--c-primary-accent);
}

h2 {
    margin-bottom: 0.75em;
    font-weight: 400;
    text-align: center;
    color: var(--c-text);
}

main {
    width: 100%;
    /* max-width: 50em; */
    /* margin: 1.5em auto; */
    /* padding-bottom: 10rem; */
}

main section.demo .info {
    text-align: center;
    /* margin: 0em 0 2em 0; */
    line-height: 2em;
    color: var(--c-text);
}

main .boxes {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    border: 2px solid rgba(66, 68, 90, 0.075);
    border-radius: 0.15em;
    padding: 1em 0;
    user-select: none;
    word-wrap: break-word;
}

main .boxes.green,
main .boxes.blue {
    margin-bottom: 0em;
}

main .boxes.red {
    display: grid;
    grid-template-columns: repeat(28, 1fr);
    grid-gap: 0.4em;
    align-items: flex-start;
    justify-content: flex-start;
    max-height: 25em;
    overflow: auto;
    padding: 0.5em;
    margin-bottom: 3em;
}

main .boxes.red > div {
    margin: 0;
}

main .boxes::after {
    display: block;
    content: '';
    clear: both;
}

main .boxes div {
    width: 6.5em;
    height:fit-content;
    /* height: 5em; */
    margin: 0.2em;
    margin-left: 0.75em;
    margin-right: 0.75em;
    border-radius: 0.2em;
    /* background: rgba(66, 68, 90, 0.075);
    background: transparent; 
    border: 2px solid transparent; */
    cursor: pointer;
}

main .boxes.green div.selected {
    color: #292929;
    font-weight: bold;
    background: linear-gradient(45deg, rgba(235,95,52,0.6) 40%, rgba(235,204,52,0.6) 94%);
    background-color: rgba(255, 0, 0, 0.45);
    /* background: hsl(100, 80%, 65%);
       border: 2px solid rgba(235, 95, 52, 0.075); */
}

/* main .boxes.green div.selected.item_name {
    background: hsl(100, 80%, 65%);
    border: 2px solid rgba(0, 0, 0, 0.075);
} */

main .boxes.blue div.selected {
    background: hsl(150, 80%, 65%);
    border: 2px solid rgba(0, 0, 0, 0.075);
}

img {
    display block;
    mix-blend-mode: multiply;
}

main .boxes.red div.selected {
    background: hsl(200, 80%, 65%);
    border: 2px solid rgba(0, 0, 0, 0.075);
}

.selection-area {
    background: rgba(46, 115, 252, 0.11);
    border: 1px solid rgba(98, 155, 255, 0.85);
    border-radius: 0.15em;
}

main section.demo .info p {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
}

.key {
    display: inline-block;
    font-weight: bold;
    text-transform: uppercase;
    color: var(--c-primary);
    font-size: 10px;
    line-height: 1em;
    padding: 0.25em 0.4em 0.2em 0.4em;
    margin: 0 0.5em -4px;
    border: 1px solid var(--c-primary);
    border-bottom: 3px solid var(--c-primary);
    border-radius: 2px;
}'''

FileViewerMJS = r'''
// import SelectionArea from 'https://cdn.jsdelivr.net/npm/@viselect/vanilla/lib/viselect.esm.js';
var fileViewerItems = {{ FILEVIEWER_ITEMS }};
var fileViewerIcons = {{ FILEVIEWER_ICONS }};
var fileViewerPaths = {{ FILEVIEWER_PATHS }};
var fileHiddenFlags = {{ HIDDEN_FLAG_LIST }};
{{ FILEVIEWER_JS }}

[
    ['.boxes.green', {{ NUM_ITEMS }}]
].forEach(([selector, items]) => {
    const container = document.querySelector(selector);
    // console.error(items);
    for (let i = 0; i < items; i++) {
        var divElement = document.createElement('div');
        // console.error(fileHiddenFlags[i]);
        divElement.id = `${fileViewerPaths[i]}`;
        var hiddenFileFlag = document.createAttribute('data-filehidden');
        hiddenFileFlag.value = fileHiddenFlags[i];
        divElement.setAttributeNode(hiddenFileFlag)
        divElement.className = "file_item";
        divElement.style.textAlign = 'center';
        divElement.innerHTML = `<img class="icon" src="${fileViewerIcons[i]}" width="40px;"/><br><span class="item_name" style="text-align: center; font-size: 13px;">${fileViewerItems[i]}</div>`
        divElement.onclick = function() {
            // console.error(this.id);
            var file_item_id = this.id;
            new QWebChannel(qt.webChannelTransport, function(channel) {
                var clickHandler = channel.objects.clickHandler;
                clickHandler.sendClickedItem(file_item_id);
            });
        }
        if (fileHiddenFlags[i] == "1") {
            divElement.style.display = "none";
        }
        container.appendChild(divElement);
    }
});

const filesSelection = new SelectionArea({
    selectables: ['.boxes > div'],
    boundaries: ['.boxes']
}).on('start', ({store, event}) => {
    if (!event.ctrlKey && !event.metaKey) {

        for (const el of store.stored) {
            el.classList.remove('selected');
            // el.getElementsByClassName['icon'][0].classList.remove('selected');
        }

        filesSelection.clearSelection();
    }
}).on('move', ({store: {changed: {added, removed}}}) => {
    for (const el of added) {
        el.classList.add('selected');
        // el.getElementsByClassName['icon'][0].classList.add('selected');
    }

    for (const el of removed) {
        el.classList.remove('selected');
        // el.getElementsByClassName['icon'][0].classList.remove('selected');
    }
});'''

FileViewerCustomJS = r'''
// hide hidden files.
function hideHiddenFiles() {
    var items = document.getElementsByClassName("file_item");
    N = items.length;
    for (let i=0; i<N; i++) {
        item = items[i]
        if (item.getAttribute("data-filehidden") == "1") {
            item.style.display = "none";
        }
    }
}
// show hidden files.
function showHiddenFiles() {
    var items = document.getElementsByClassName("file_item");
    N = items.length;
    for (let i=0; i<N; i++) {
        item = items[i]
        if (item.getAttribute("data-filehidden") == "1") {
            item.style.display = "";
        }
    }
}

// this javascript function is to clear all selections.
function clearSelectedItems() {
    selItems = document.getElementsByClassName("selected file_item");
    N = selItems.length
    var selItemIds = []
    for (let i=0; i<N; i++) {
        selItemIds.push(selItems[i].id);
    }
    for (let i=0; i<N; i++) {
        item = document.getElementById(selItemIds[i]);
        item.classList.remove('selected');
    }
}
function invertSelectedItems() {
    items = document.getElementsByClassName("file_item");
    N = items.length
    for (let i=0; i<N; i++) {
        classList = items[i].classList;
        if (classList.contains("selected")) {
            items[i].classList.remove('selected');
        }
        else {
            items[i].classList.add('selected');
        }
    }    
}
// select all file items.
function selectAllItems() {
    items = document.getElementsByClassName("file_item");
    N = items.length
    for (let i=0; i<N; i++) {
        items[i].classList.add('selected');
    }
}'''

FileViewerHtml = jinja2.Template(r'''
<!DOCTYPE HTML>
<html lang="en">
    <head>
        <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <meta charset="UTF-8">

        <!-- Chrome, Firefox OS and Opera -->
        <meta name="theme-color" content="#57D5E3"/>

        <!-- Windows Phone -->
        <meta name="msapplication-navbutton-color" content="#57D5E3"/>

        <!-- iOS Safari -->
        <meta name="apple-mobile-web-app-status-bar-style" content="#57D5E3"/>


        <title>Selection JS</title>

        <!-- Icons -->
        <!-- <link rel="icon" href="favicon.png"/>
        <link rel="fluid-icon" href="favicon.png"/>
        <link rel="apple-touch-icon" href="favicon.png"/>
        <link href="favicon.png" rel="icon"/>
        <link href="favicon.png" rel="apple-touch-icon"/> -->

        <!-- CSS / JS -->
        <style>{{ FILEVIEWER_CSS }}</style>
    </head>

    <body>
        <main>
            <section class="demo">
                <section class="boxes green"></section>
            </section>
        </main>
        <script>{{ WEBCHANNEL_JS }}</script>
        <script>{{ FILEVIEWER_CJS }}</script>
        <script type="module">{{ FILEVIEWER_MJS }}</script>
    </body>
</html>''')
class ClickEventHandler(QObject):
    def __init__(self, fileviewer):
        super(ClickEventHandler, self).__init__()
        self.fileviewer = fileviewer

    @pyqtSlot(str)
    def sendClickedItem(self, path):
        # id = int(id.replace("item", ""))
        if self.fileviewer.selected_item == path:
            # print(id)
            # item = self.fileviewer.loaded_file_items[]
            self.fileviewer.open(path)  
        else:
            self.fileviewer.updateSelection(path)
        

class FileViewerWebView(DebugWebView):
    '''fileviewer web view'''
    def contextMenuEvent(self, event):
        '''redefine the context menu.'''
        self.menu = self.page().createStandardContextMenu()
        self.menu.clear()
        self.menu.setStyleSheet("background: #292929; color: #fff;")
        self.menu.addAction("New Folder")
        self.menu.addAction("New File")
        self.menu.addSeparator()
        self.menu.addAction("Restore Missing Files...")
        self.menu.addAction("Open in Terminal")
        self.menu.addSeparator()
        self.menu.addAction("Paste")
        self.menu.addSeparator()
        self.menu.addAction("Properties")
        self.menu.popup(event.globalPos())


class  FileViewerGroup(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None,
                 name: str="Widget Group"):
        super(FileViewerGroup, self).__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(0)
        self.group = QWidget()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setSpacing(2)
        self.group.setLayout(self.layout)
        layout.addWidget(self.Label(name))
        layout.addWidget(self.group)
        layout.addStretch(1)
        self.setLayout(layout)

    def Label(self, name):
        name = QLabel(name)
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet('''
        QLabel {
            border: 0px;
            padding: 6px;
            color: #eb5f34;
            font-size: 16px;
            background: transparent;
        }''')
        return name

    def initBtnGroup(self, btn_args):
        btnGroup = QWidget()
        btnGroup.btns = []
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        btnGroup.setLayout(layout)
        btnGroup.setStyleSheet('''
        QWidget {
            color: #fff;
            border: 0px;
            background: transparent;
        }''')
        layout.addStretch(1)
        for args in btn_args:
            btn = self.initBtn(**args)
            btnGroup.btns.append(btn)
            layout.addWidget(btn, 0, Qt.AlignCenter)
        layout.addStretch(1)
        btnGroup.setLayout(layout)

        return btnGroup

    def initBtn(self, **args):
        btn = QToolButton(self)
        tip = args.get("tip", "a tip")
        size = args.get("size", (23,23))
        if "icon" in args:
            icon = os.path.join("system/fileviewer", args["icon"])
            btn.setIcon(FigD.Icon(icon))
        elif "text" in args:
            btn.setText(args["text"])
        btn.setIconSize(QSize(*size))
        btn.setToolTip(tip)
        btn.setStatusTip(tip)
        btn.setStyleSheet('''
        QToolButton {
            color: #fff;
            border: 0px;
            font-size: 14px;
            background: transparent;
        }
        QToolButton:hover {
            color: #292929;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34);
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }''')

        return btn 


class FileViewerFileGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerFileGroup, self).__init__(parent, "File")
        # file creation widget.
        self.creationWidget = QWidget()
        self.creationLayout = QVBoxLayout()
        self.creationLayout.setContentsMargins(0, 0, 0, 0)
        self.creationWidget.setLayout(self.creationLayout)
        self.newFileBtn =  self.initBtn(
            icon="new_file.svg",
            size=(30,30),
            tip="create a new file",
        )
        self.newFolderBtn =  self.initBtn(
            icon="new_folder.svg",
            size=(30,30),
            tip="create a new folder",
        )
        self.creationLayout.addWidget(self.newFileBtn)
        self.creationLayout.addWidget(self.newFolderBtn)
        self.creationLayout.addStretch(1)
        # connect to server.
        self.connectToServerBtn = self.initBtn(
            icon="connect_to_server.svg",
            size=(45,45),
            tip="connect to a server",
        )
        self.layout.addWidget(self.creationWidget)
        self.layout.addWidget(self.connectToServerBtn)


class FileViewerPathGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerPathGroup, self).__init__(parent, "Path")
        # just to convert to VBox Layout.
        # path copying tools.
        self.pathWidget = QWidget()
        self.pathLayout = QVBoxLayout()
        self.pathLayout.setContentsMargins(0, 0, 0, 0)
        self.pathLayout.setSpacing(0)
        self.pathWidget.setLayout(self.pathLayout)
        # path navigation tools.
        self.navWidget = QWidget()
        self.navLayout = QVBoxLayout()
        self.navLayout.setContentsMargins(0, 0, 0, 0)
        self.navLayout.setSpacing(0)
        self.navWidget.setLayout(self.navLayout)
        # buttons.
        self.backPathBtn = self.initBtn(
            icon="back_path.png",
            size=(25,25),
            tip="go back to parent folder",
        )
        self.copyPathBtn =  self.initBtn(
            icon="copy_filepath.png",
            size=(25,25),
            tip="copy filepath",
        )
        self.copyNameBtn = self.initBtn(
            icon="copy_filename.svg",
            size=(25,25),
            tip="copy filename",
        )
        self.copyUrlBtn =  self.initBtn(
            icon="copy_as_url.png",
            size=(25,25),
            tip="copy file path as url",
        )
        self.extBtn = self.initBtn(
            text=".ext", size=(25,25),
            tip="copy extension of file",
        )
        # move to view
        # self.hideExtBtn =  self.initBtn(
        #     icon="hide_extension.svg",
        #     size=(20,20)
        # )
        self.pathLayout.addWidget(self.copyPathBtn)
        self.pathLayout.addWidget(self.copyNameBtn)
        self.pathLayout.addWidget(self.copyUrlBtn)
        self.pathLayout.addStretch(1)

        self.navLayout.addStretch(1)
        self.navLayout.addWidget(self.backPathBtn)
        self.navLayout.addWidget(self.extBtn)
        
        self.layout.addStretch(1)
        self.layout.addWidget(self.pathWidget)
        self.layout.addWidget(self.navWidget)
        self.layout.addStretch(1)

    def updateExt(self, ext: str):
        '''update extension layout.'''
        self.extBtn.setText(ext)

    def connectWidget(self, widget):
        self.backPathBtn.clicked.connect(widget.openParent)
        self.copyUrlBtn.clicked.connect(widget.copyUrlToClipboard)
        self.copyNameBtn.clicked.connect(widget.copyNameToClipboard)
        self.copyPathBtn.clicked.connect(widget.copyPathToClipboard)
        self.extBtn.clicked.connect(
            lambda: widget.copyToClipboard(self.extBtn.text())
        )


class FileViewerEditGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerEditGroup, self).__init__(parent, "Edit")
        self.editWidget = QWidget() 
        self.editLayout = QVBoxLayout()
        self.editLayout.setContentsMargins(0, 0, 0, 0)
        # undo, redo, rename
        self.renameGroup = self.initBtnGroup([
            {"icon": "undo.png", "size": (20,20), "tip": "undo rename"},
            {"icon": "rename.svg", "size": (20,20), "tip": "rename file/folder"},
            {"icon": "redo.png", "size": (20,20) , "tip": "redo rename"},
        ])
        # cut, copy, paste
        self.moveGroup = self.initBtnGroup([
            {"icon": "cut.png", "size": (20,20), "tip": "cut selected item"},
            {"icon": "copy.svg", "size": (20,20), "tip": "copy selected items"},
            {"icon": "paste.png", "size": (20,20), "tip": "paste selected items from the clipboard"},
        ])
        # make link, release link, move to trash
        self.linkGroup = self.initBtnGroup([
            {"icon": "link.svg", "size": (20,20)},
            {"icon": "unlink.svg", "size": (20,20), "tip": "move selected item(s) to trash"},
            {"icon": "trash.svg", "size": (30,30), "tip": "move selected item(s) to trash"},
        ])
        self.editLayout.addWidget(self.renameGroup)
        self.editLayout.addWidget(self.moveGroup)
        self.editLayout.addWidget(self.linkGroup)
        self.editLayout.addStretch(1)
        self.editWidget.setLayout(self.editLayout)
        self.layout.addStretch(1)
        self.layout.addWidget(self.editWidget)
        self.layout.addStretch(1)    


class FileViewerViewGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerViewGroup, self).__init__(parent, "View")
        self.viewWidget = QWidget() 
        self.viewLayout = QVBoxLayout()
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        # layout of file items
        self.layoutGroup = self.initBtnGroup([
            {"icon": "tileview.svg", "size": (25,25), "tip": "tile view"},
            {"icon": "listview.svg", "size": (25,25), "tip": "list view"},
            {"icon": "treeview.svg", "size": (25,25), "tip": "tree view"},
        ])
        # hidden files, folder bar visibility, side bar visibility, search bar visibility.
        self.visibilityGroup = self.initBtnGroup([
            {"icon": "toggle_hidden_files.png", "size": (23,23), "tip": "toggle visibility of hidden files"},
            {"icon": "toggle_folderbar.svg", "size": (30,30), "tip": "toggle visibility of folder bar"},
            {"icon": "toggle_searchbar.svg", "size": (23,23), "tip": "toggle visibility of search bar"},
            {"icon": "toggle_sidebar.svg", "size": (23,23), "tip": "toggle visibility of sidebar"},
        ])
        self.hiddenFilesBtn = self.visibilityGroup.btns[0]
        self.folderbarBtn = self.visibilityGroup.btns[1]
        self.searchbarBtn = self.visibilityGroup.btns[2]
        self.sidebarBtn = self.visibilityGroup.btns[3]
        self.arrangeGroup = self.initBtnGroup([
            {"icon": "sidebar_left.svg", "size": (20,20), "tip": "sidebar to the left"},
            {"icon": "sidebar_right.svg", "size": (20,20), "tip": "sidebar to the right"},
        ])     
        self.viewLayout.addWidget(self.layoutGroup)
        self.viewLayout.addWidget(self.visibilityGroup)
        self.viewLayout.addWidget(self.arrangeGroup)
        self.viewLayout.addStretch(1)
        self.viewWidget.setLayout(self.viewLayout)
        self.layout.addStretch(1)
        self.layout.addWidget(self.viewWidget)
        self.layout.addStretch(1)    

    def connectWidget(self, widget):
        self.widget = widget
        self.folderbarBtn.clicked.connect(
            widget.folderbar.toggle
        )
        self.hiddenFilesBtn.clicked.connect(
            widget.toggleHiddenFiles
        )


class FileViewerSelectGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerSelectGroup, self).__init__(parent, "Select")
        self.selectionWidget = QWidget() 
        self.selectionLayout = QVBoxLayout()
        self.selectionLayout.setContentsMargins(0, 0, 0, 0)
    
        self.selectionGroup = self.initBtnGroup([
            {"icon": "clear_selection.png", "size": (25,25), "tip": "clear current selection"},
            {"icon": "select_all.png", "size": (25,25), "tip": "select all items"},
            {"icon": "invert_selection.png", "size": (25,25), "tip": "invert selected items"},
        ])
        self.clearBtn = self.selectionGroup.btns[0]
        self.selectAllBtn = self.selectionGroup.btns[1]
        self.invertBtn = self.selectionGroup.btns[2]
        self.selectionLayout.addWidget(self.selectionGroup)
        self.selectionLayout.addStretch(1)
        self.selectionWidget.setLayout(self.selectionLayout)

        self.layout.addStretch(1)
        self.layout.addWidget(self.selectionWidget)
        self.layout.addStretch(1)    

    def connectWidget(self, widget):
        self.widget = widget
        self.clearBtn.clicked.connect(widget.clearSelection)
        self.selectAllBtn.clicked.connect(widget.selectAll)
        self.invertBtn.clicked.connect(widget.invertSelection)
# class FileViewerOpenGroup(QWidget):
# class FileViewerMoveGroup(QWidget):
# class FileViewerPropGroup(QWidget):
# class FileViewerShareGroup(QWidget):
# class FileViewerFilterGroup(QWidget):
# class FileViewerUtilsGroup(QWidget): encryption, compression, file conversion (for images, videos,document formats etc.)

# class FileViewerMiscGroup(QWidget): note, bookmark
# class FileViewerVCSGroup(QWidget):
# class FileViewerBackupGroup(QWidget):
class FileViewerMenu(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerMenu, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.filegroup = FileViewerFileGroup()
        self.pathgroup = FileViewerPathGroup()
        self.editgroup = FileViewerEditGroup()
        self.viewgroup = FileViewerViewGroup()
        self.selectgroup = FileViewerSelectGroup()
        self.layout.addWidget(self.filegroup)
        self.layout.addWidget(self.addSeparator(20))
        self.layout.addWidget(self.pathgroup)
        self.layout.addWidget(self.addSeparator(20))
        self.layout.addWidget(self.editgroup)
        self.layout.addWidget(self.addSeparator(20))
        self.layout.addWidget(self.viewgroup)
        self.layout.addWidget(self.addSeparator(20))
        self.layout.addWidget(self.selectgroup)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def addSeparator(self, width: Union[None, int]=None):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet('''background: transparent;''')
        sep.setLineWidth(1)
        sep.setMaximumHeight(90)
        if width: sep.setFixedWidth(width)
        return sep

    def connectWidget(self, widget):
        self.viewgroup.connectWidget(widget)
        self.pathgroup.connectWidget(widget)
        self.selectgroup.connectWidget(widget)


class FileViewerFolderBar(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerFolderBar, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        self.path = ""
        self.setLayout(self.layout)
        self.setObjectName("FileViewerFolderBar")
        self.selectedIndex = 0 
        self.folderBtns = []
        self.folderBtnStyle = '''
        QToolButton {
            color: #fff;
            border: 0px;
            font-size: 17px;
            font-weight: bold;
            padding-top: 4px;
            padding-bottom: 4px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
        }
        QToolButton:hover {
            color: #292929;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34);
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }'''
        self.folderBtnSelStyle = '''
        QToolButton {
            border: 0px;
            color: #292929;
            font-size: 17px;
            font-weight: bold;
            padding-top: 4px;
            padding-bottom: 4px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34);
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }'''

    def toggle(self):
        print("toggling folderbar visibility")
        if self.isVisible():
            self.hide()
        else: self.show()

    def __len__(self):
        return len(self.folderBtns)

    def clear(self):
        '''clear all the folder buttons on the folder bar.'''
        for i in reversed(range(len(self))): 
            print(i)
            self.layout.itemAt(i).widget().setParent(None)

    def getSubPaths(self, path):
        sub_paths = []
        path = Path(path)
        while str(path) != "/":
            sub_paths.append((str(path)))
            path = path.parent

        return ["/"]+sub_paths[::-1]

    def setPath(self, path):
        if self.path.startswith(path):
            for i, sub_path in enumerate(self.getSubPaths(path)):
                if sub_path == path: break
            self.folderBtns[self.selectedIndex].setStyleSheet(self.folderBtnStyle)
            self.folderBtns[i].setStyleSheet(self.folderBtnSelStyle)
            self.selectedIndex = i
            return
        # clear layout
        self.clear()
        # change the recorded deepest path till now.
        self.path = path
        path = Path(path)
        self.folderBtns = []
        
        items = []
        while str(path) != "/":
            items.append((str(path.name), str(path)))
            path = path.parent
        items.append(("/", "/"))
        # items = items[::-1]
        self.selectedIndex = len(items)-1
        for name, path in items:
            btn = self.initFolderBtn(name, path)
            self.layout.insertWidget(0, btn)
            self.folderBtns.append(btn)
        
        self.folderBtns = self.folderBtns[::-1]
        self.folderBtns[-1].setStyleSheet(self.folderBtnSelStyle)
        self.layout.addStretch(1)

    def connectWidget(self, widget):
        self.widget = widget

    def initFolderBtn(self, name, full_path):
        btn = QToolButton(self)
        tip = f"got to {full_path}"
        btn.setToolTip(tip)
        btn.setText(name)
        if self.widget:
            btn.clicked.connect(
                lambda: self.widget.open(full_path)
            )
        btn.setStyleSheet(self.folderBtnStyle)

        return btn 


class FileViewerWidget(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None,
                 zoom_factor: float=1.35, **args):
        super(FileViewerWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.webview = FileViewerWebView()
        self.zoom_factor = zoom_factor
        self.menu = FileViewerMenu()
        self.menu.setMaximumHeight(130)
        self.font_color = args.get("font_color", '#fff')
        # data
        self.background_image = QUrl.fromLocalFile(
            args.get("background")
        ).toString()
        self.icon_provider = QFileIconProvider()
        self.mime_database = QMimeDatabase()
        self.loaded_file_items = []
        self.browsing_history = []
        self.selected_item = None
        self.hidden_visible = False
        # handle click events (using click handler)
        self.channel = QWebChannel()
        self.clickHandler = ClickEventHandler(fileviewer=self)
        self.channel.registerObject("clickHandler", self.clickHandler)
        self.webview.page().setWebChannel(self.channel)
        self.folderbar = FileViewerFolderBar()
        self.folderbar.setMaximumHeight(30)
        # clipboard access.
        self.clipboard = args.get("clipboard")
        # shortcuts.
        self.CtrlA = QShortcut(QKeySequence("Ctrl+A"), self)
        self.CtrlA.activated.connect(self.selectAll)
        # add widgets to layout.
        self.layout.addWidget(self.menu)
        self.layout.addWidget(self.folderbar)
        self.layout.addWidget(self.webview.devToolsBtn)
        self.layout.addWidget(self.webview.splitter)
        self.setLayout(self.layout)
        self.webview.urlChanged.connect(self.onUrlChange)
        self.setStyleSheet('''background: transparent; border: 0px; color: #fff;''')
        self.menu.connectWidget(self)
        self.folderbar.connectWidget(self)

    def toggleHiddenFiles(self):
        if self.hidden_visible:
            self.hidden_visible = False
            self.webview.page().runJavaScript('hideHiddenFiles();')
        else:
            self.hidden_visible = True
            self.webview.page().runJavaScript('showHiddenFiles();')
        
    def openParent(self):
        path = str(self.folder.parent)
        self.open(path)

    def callXdgOpen(self, path: str):
        '''call xdg-open for the appropriate mimetype.'''
        mimetype = self.mime_database.mimeTypeForFile(path).name()
        print(f"{path}: calling xdg-open for {mimetype} files")

    def listFiles(self, path: str, **args):
        listed_and_full_paths_files = []
        listed_and_full_paths_folders = []
        # hidden files are marked by a 0
        # sort in reverse order or not
        reverse = args.get("reverse", False)
        for file in os.listdir(path):
            # if hidden == False and file.startswith("."):
            #     continue
            full_path = os.path.join(path, file) 
            if os.path.isdir(full_path):
                listed_and_full_paths_folders.append((
                    file, 1 if file.startswith(".") else 0, 
                    os.path.join(path, file)
                ))
            else:
                listed_and_full_paths_files.append((
                    file, 1 if file.startswith(".") else 0, 
                    os.path.join(path, file)
                ))
        listed_and_full_paths_folders = sorted(
            listed_and_full_paths_folders, 
            key=lambda x: x[0].lower(), 
            reverse=reverse,
        )
        listed_and_full_paths_files = sorted(
            listed_and_full_paths_files, 
            key=lambda x: x[0].lower(), 
            reverse=reverse,
        )
        listed_and_full_paths = listed_and_full_paths_folders + listed_and_full_paths_files
        listed = [i for i,_,_ in listed_and_full_paths]
        full_paths = [i for _,_,i in listed_and_full_paths]
        hidden_flag_list = [i for _,i,_ in listed_and_full_paths]

        return listed, full_paths, hidden_flag_list

    def errorDialog(self, msg):
        self.error_dialog = QErrorMessage()
        self.error_dialog.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.error_dialog.showMessage(msg)
        # print(msg)
    def open(self, folder: str=os.path.expanduser("~")):
        '''open a file/folder location.'''
        # call xdg-open if a file is clicked instead of a folder.
        if os.path.isfile(folder): 
            self.callXdgOpen(folder)
            return
        # might be a device or something.
        if not os.path.isdir(folder): return
        # check if the user has permission to view folder
        try:
            os.scandir(folder)
        except PermissionError as e:
            self.errorDialog(str(e))
            return
        self.folder = Path(folder)
        self.folderbar.setPath(folder)  
        self.browsing_history.append(folder)
        listed, full_paths, hidden_flag_list = self.listFiles(folder)
        
        for path in full_paths:
            self.loaded_file_items.append({
                "path": path, 
                "mimetype": self.mime_database.mimeTypeForFile(path).name(),
                "info": QFileInfo(path),
            })   
        icons = [
            (self.icon_provider.icon(QFileInfo(path)).name(), 
             self.mime_database.mimeTypeForFile(path).name(),
             path) for path in full_paths
        ]
        icon_theme_devices_path = "/usr/share/icons/Humanity/devices/48"
        icon_theme_places_path = "/usr/share/icons/Humanity/places/64"
        icon_theme_mimes_path = "/usr/share/icons/Humanity/mimes/48"
        # if os.path.exists(icon_theme_places_path):
        icon_paths = []
        for name, mimetype, full_path in icons:
            if name == "":
                name = "text-plain"
            if mimetype.startswith("image/"):
                path = full_path
                icon_paths.append(QUrl.fromLocalFile(path).toString())
            else:
                path = os.path.join(
                    icon_theme_mimes_path, 
                    name+".svg"
                )
                if os.path.exists(path): 
                    icon_paths.append(QUrl.fromLocalFile(path).toString())
                    continue
                path = os.path.join(
                    icon_theme_places_path, 
                    name+".svg"
                )
                if os.path.exists(path): 
                    icon_paths.append(QUrl.fromLocalFile(path).toString())
                    continue
                path = os.path.join(
                    icon_theme_devices_path, 
                    name+".svg"
                )    
                if os.path.exists(path): 
                    icon_paths.append(QUrl.fromLocalFile(path).toString())
                    continue
                path = "default.svg"
                icon_paths.append(QUrl.fromLocalFile(path).toString())     
        def chunk_string(string, k=12):
            result = []
            for i in range(0, len(string), k):
                result.append(string[i:i+k])

            return result

        def format_listed(prelisted):
            listed = []
            for rec in prelisted:
                # rec = "_<br>".join(rec.split("_"))
                # rec = "<br>".join(chunk_string(rec))
                listed.append(rec)

            return listed         
        # print(icons)
        self.params = {
            "FOLDER": self.folder.name,
            "FONT_COLOR": self.font_color,
            "WEBCHANNEL_JS": QWebChannelJS,
            "FILEVIEWER_JS": ViSelectJS,
            "FILEVIEWER_MJS": FileViewerMJS,
            "FILEVIEWER_CSS": FileViewerStyle,
            "FILEVIEWER_CJS": FileViewerCustomJS,
            "PARENT_FOLDER": self.folder.parent.name,
            "FILEVIEWER_ICONS": icon_paths,
            "FILEVIEWER_PATHS": full_paths,
            "FILEVIEWER_ITEMS": format_listed(listed),
            "BACKGROUND_IMAGE": self.background_image,
            "HIDDEN_FLAG_LIST": hidden_flag_list,
            "NUM_ITEMS": len(listed),
        }
        self.viewer_html = jinja2.Template(
            FileViewerHtml.render(**self.params)
        ).render(**self.params)
        render_url = FigD.createTempUrl(self.viewer_html)
        self.webview.load(render_url)

    def updateSelection(self, item):
        '''update widget state when currently selected item is changed'''
        self.selected_item = item
        # print(os.path.splitext(item))
        _, file_ext = os.path.splitext(item)
        if file_ext == "":
            file_ext = ".ext"
        # print(file_ext)
        self.menu.pathgroup.updateExt(file_ext)

    def onUrlChange(self):
        self.webview.setZoomFactor(self.zoom_factor)
        self.webview.loadFinished.connect(self.webview.loadDevTools)

    def copyUrlToClipboard(self):
        if self.clipboard and self.selected_item:
            url = QUrl.fromLocalFile(self.selected_item).toString()
            self.clipboard.setText(url)
            print(f"copied {url} to clipboard")    

    def copyPathToClipboard(self):
        if self.clipboard and self.selected_item:
            self.clipboard.setText(self.selected_item)
            print(f"copied {self.selected_item} to clipboard")

    def copyNameToClipboard(self):
        if self.clipboard and self.selected_item:
            name = Path(self.selected_item).name
            self.clipboard.setText(name)
            print(f"copied {name} to clipboard")            

    @pyqtSlot()
    def selectAll(self):
        '''select all items.'''
        # print("selected all items")
        self.webview.page().runJavaScript('selectAllItems();')

    def invertSelection(self):
        '''invert selected items.'''
        self.webview.page().runJavaScript('invertSelectedItems();')

    def clearSelection(self):
        '''clear selected items.'''
        self.webview.page().runJavaScript('clearSelectedItems();')

    def copyToClipboard(self, text):
        if self.clipboard:
            self.clipboard.setText(text)
            print(f"copied {text} to clipboard")

    def saveScreenshot(self, path):
        with open(path, "w") as f:
            f.write(self.viewer_html)


def test_fileviewer():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    fileviewer = FileViewerWidget(
        clipboard=app.clipboard(),
        background="/home/atharva/Pictures/Wallpapers/anime/beautiful-crowded-city.jpg",
        font_color="#fff",
    )
    fileviewer.open()
    # fileviewer.saveScreenshot("fileviewer.html")
    fileviewer.show()
    app.exec()


if __name__ == '__main__':
    test_fileviewer()

#a33817 (dark) #323150
#eb5f34 (deep) #4d4c78
#bd5f42 (medium) #64639c
#db8b72 (dull) #8a87b2
#e0a494 (light) #c8c2e9
#f2e3df (very light) #dfdafd