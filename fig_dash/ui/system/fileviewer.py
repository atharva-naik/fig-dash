#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# the fig-dash fileviewer is known as the "orchard".
from genericpath import isfile
import os
from sys import meta_path
import jinja2
import socket
import getpass
from pathlib import Path
from typing import Union, Tuple
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.utils import h_format_mem
from fig_dash.ui.browser import DebugWebView
from fig_dash.api.js.system import SystemHandler
from fig_dash.ui.js.webchannel import QWebChannelJS
from fig_dash.api.system.file.applications import MimeTypeDefaults, DesktopFile
# PyQt5 imports
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor, QKeySequence, QFontDatabase
from PyQt5.QtCore import Qt, QSize, QFileInfo, QUrl, QMimeDatabase, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QErrorMessage, QLabel, QLineEdit, QToolBar, QMenu, QToolButton, QSizePolicy, QFrame, QAction, QActionGroup, QShortcut, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QFileIconProvider, QSlider, QComboBox, QCompleter, QDirModel
# filweviewer widget.
ViSelectJS = r'''/*! @viselect/vanilla 3.0.0-beta.13 MIT | https://github.com/Simonwep/selection */
const t=(t,e="px")=>"number"==typeof t?t+e:t;function e({style:e},s,i){if("object"==typeof s)for(const[i,o]of Object.entries(s))e[i]=t(o);else void 0!==i&&(e[s]=t(i))}function s(t){return(e,s,i,o={})=>{e instanceof HTMLCollection||e instanceof NodeList?e=Array.from(e):Array.isArray(e)||(e=[e]),Array.isArray(s)||(s=[s]);for(const n of e)for(const e of s)n[t](e,i,{capture:!1,...o});return[e,s,i,o]}}const i=s("addEventListener"),o=s("removeEventListener"),n=t=>{const e=t.touches&&t.touches[0]||t;return{tap:e,x:e.clientX,y:e.clientY,target:e.target}};function r(t){let e=t.path||t.composedPath&&t.composedPath();if(e)return e;let s=t.target.parentElement;for(e=[t.target,s];s=s.parentElement;)e.push(s);return e.push(document,window),e}function h(t,e,s="touch"){switch(s){case"center":{const s=e.left+e.width/2,i=e.top+e.height/2;return s>=t.left&&s<=t.right&&i>=t.top&&i<=t.bottom}case"cover":return e.left>=t.left&&e.top>=t.top&&e.right<=t.right&&e.bottom<=t.bottom;case"touch":return t.right>=e.left&&t.left<=e.right&&t.bottom>=e.top&&t.top<=e.bottom;default:throw new Error(`Unkown intersection mode: ${s}`)}}function c(t,e){const s=t.indexOf(e);~s&&t.splice(s,1)}function a(t,e=document){const s=Array.isArray(t)?t:[t],i=[];for(let t=0,o=s.length;t<o;t++){const o=s[t];"string"==typeof o?i.push(...Array.from(e.querySelectorAll(o))):o instanceof Element&&i.push(o)}return i}const l=()=>matchMedia("(hover: none), (pointer: coarse)").matches,u=(t,e)=>{for(const[s,i]of Object.entries(t)){const o=e[s];t[s]=void 0===o?t[s]:"object"!=typeof o||"object"!=typeof i||null===i||Array.isArray(i)?o:u(i,o)}return t},{abs:d,max:p,min:f,ceil:m}=Math;class SelectionArea extends class{constructor(){this.t=new Map,this.on=this.addEventListener,this.off=this.removeEventListener,this.emit=this.dispatchEvent}addEventListener(t,e){const s=this.t.get(t)||new Set;return this.t.set(t,s),s.add(e),this}removeEventListener(t,e){return this.t.get(t)?.delete(e),this}dispatchEvent(t,...e){let s=!0;for(const i of this.t.get(t)||[])s=!1!==i(...e)&&s;return s}unbindAllListeners(){this.t.clear()}}{constructor(t){super(),this.i={touched:[],stored:[],selected:[],changed:{added:[],removed:[]}},this.o=[],this.h=new DOMRect,this.l={y1:0,x2:0,y2:0,x1:0},this.u=!0,this.p=!0,this.m={x:0,y:0},this.v={x:0,y:0},this.disable=this.g.bind(this,!1),this.enable=this.g,this._=u({selectionAreaClass:"selection-area",selectionContainerClass:void 0,selectables:[],document:window.document,behaviour:{overlap:"invert",intersect:"touch",startThreshold:{x:10,y:10},scrolling:{speedDivider:10,manualSpeed:750,startScrollMargins:{x:0,y:0}}},features:{range:!0,touch:!0,singleTap:{allow:!0,intersect:"native"}},startAreas:["html"],boundaries:["html"],container:"body"},t);for(const t of Object.getOwnPropertyNames(Object.getPrototypeOf(this)))"function"==typeof this[t]&&(this[t]=this[t].bind(this));const{document:s,selectionAreaClass:i,selectionContainerClass:o}=this._;this.S=s.createElement("div"),this.A=s.createElement("div"),this.A.appendChild(this.S),this.S.classList.add(i),o&&this.A.classList.add(o),e(this.S,{willChange:"top, left, bottom, right, width, height",top:0,left:0,position:"fixed"}),e(this.A,{overflow:"hidden",position:"fixed",transform:"translate3d(0, 0, 0)",pointerEvents:"none",zIndex:"1"}),this.T=(t=>{let e,s=-1,i=!1;return{next(...o){e=o,i||(i=!0,s=requestAnimationFrame((()=>{t(...e),i=!1})))},cancel(){cancelAnimationFrame(s),i=!1}}})((t=>{this.L(),this.C(),this.M("move",t),this.j()})),this.enable()}g(t=!0){const{document:e,features:s}=this._,n=t?i:o;n(e,"mousedown",this.k),s.touch&&n(e,"touchstart",this.k,{passive:!1})}k(t,e=!1){const{x:s,y:o,target:c}=n(t),{_:l}=this,{document:u}=this._,d=c.getBoundingClientRect(),p=a(l.startAreas,l.document),f=a(l.boundaries,l.document);this.O=f.find((t=>h(t.getBoundingClientRect(),d)));const m=r(t);if(!this.O||!p.find((t=>m.includes(t)))||!f.find((t=>m.includes(t))))return;if(!e&&!1===this.M("beforestart",t))return;this.l={x1:s,y1:o,x2:0,y2:0};const v=u.scrollingElement||u.body;this.v={x:v.scrollLeft,y:v.scrollTop},this.u=!0,this.clearSelection(!1),i(u,["touchmove","mousemove"],this.R,{passive:!1}),i(u,["mouseup","touchcancel","touchend"],this.$),i(u,"scroll",this.D)}F(t){const{singleTap:{intersect:e},range:s}=this._.features,i=n(t);let o=null;if("native"===e)o=i.target;else if("touch"===e){this.resolveSelectables();const{x:t,y:e}=i;o=this.o.find((s=>{const{right:i,left:o,top:n,bottom:r}=s.getBoundingClientRect();return t<i&&t>o&&e<r&&e>n}))}if(!o)return;for(this.resolveSelectables();!this.o.includes(o);){if(!o.parentElement)return;o=o.parentElement}const{stored:r}=this.i;if(this.M("start",t),t.shiftKey&&r.length&&s){const t=this.q??r[0],[e,s]=4&t.compareDocumentPosition(o)?[o,t]:[t,o],i=[...this.o.filter((t=>4&t.compareDocumentPosition(e)&&2&t.compareDocumentPosition(s))),e,s];this.select(i)}else r.includes(o)&&(1===r.length||t.ctrlKey||r.every((t=>this.i.stored.includes(t))))?this.deselect(o):(this.q=o,this.select(o));this.M("stop",t)}R(t){const{container:s,document:r,features:h,behaviour:{startThreshold:c}}=this._,{x1:u,y1:p}=this.l,{x:f,y:m}=n(t),v=typeof c;if("number"===v&&d(f+m-(u+p))>=c||"object"===v&&d(f-u)>=c.x||d(m-p)>=c.y){if(o(r,["mousemove","touchmove"],this.R,{passive:!1}),!1===this.M("beforedrag",t))return void o(r,["mouseup","touchcancel","touchend"],this.$);i(r,["mousemove","touchmove"],this.H,{passive:!1}),e(this.S,"display","block"),a(s,r)[0].appendChild(this.A),this.resolveSelectables(),this.u=!1,this.W=this.O.getBoundingClientRect(),this.p=this.O.scrollHeight!==this.O.clientHeight||this.O.scrollWidth!==this.O.clientWidth,this.p&&(i(r,"wheel",this.I,{passive:!1}),this.o=this.o.filter((t=>this.O.contains(t)))),this.N(),this.M("start",t),this.H(t)}h.touch&&l()&&t.preventDefault()}N(){const{A:t,O:s,S:i}=this,o=this.W=s.getBoundingClientRect();this.p?(e(t,{top:o.top,left:o.left,width:o.width,height:o.height}),e(i,{marginTop:-o.top,marginLeft:-o.left})):(e(t,{top:0,left:0,width:"100%",height:"100%"}),e(i,{marginTop:0,marginLeft:0}))}H(t){const{x:e,y:s}=n(t),{m:i,l:o,_:r,T:h}=this,{features:c}=r,{speedDivider:a}=r.behaviour.scrolling,u=this.O;if(o.x2=e,o.y2=s,this.p&&(i.y||i.x)){const e=()=>{if(!i.x&&!i.y)return;const{scrollTop:s,scrollLeft:n}=u;i.y&&(u.scrollTop+=m(i.y/a),o.y1-=u.scrollTop-s),i.x&&(u.scrollLeft+=m(i.x/a),o.x1-=u.scrollLeft-n),h.next(t),requestAnimationFrame(e)};requestAnimationFrame(e)}else h.next(t);c.touch&&l()&&t.preventDefault()}D(){const{v:t,_:{document:e}}=this,{scrollTop:s,scrollLeft:i}=e.scrollingElement||e.body;this.l.x1+=t.x-i,this.l.y1+=t.y-s,t.x=i,t.y=s,this.N(),this.T.next(null)}I(t){const{manualSpeed:e}=this._.behaviour.scrolling,s=t.deltaY?t.deltaY>0?1:-1:0,i=t.deltaX?t.deltaX>0?1:-1:0;this.m.y+=s*e,this.m.x+=i*e,this.H(t),t.preventDefault()}L(){const{m:t,l:e,h:s,O:i,W:o,_:n}=this,{scrollTop:r,scrollHeight:h,clientHeight:c,scrollLeft:a,scrollWidth:l,clientWidth:u}=i,m=o,{x1:v,y1:g}=e;let{x2:y,y2:_}=e;const{behaviour:{scrolling:{startScrollMargins:x}}}=n;y<m.left+x.x?(t.x=a?-d(m.left-y+x.x):0,y=y<m.left?m.left:y):y>m.right-x.x?(t.x=l-a-u?d(m.left+m.width-y-x.x):0,y=y>m.right?m.right:y):t.x=0,_<m.top+x.y?(t.y=r?-d(m.top-_+x.y):0,_=_<m.top?m.top:_):_>m.bottom-x.y?(t.y=h-r-c?d(m.top+m.height-_-x.y):0,_=_>m.bottom?m.bottom:_):t.y=0;const b=f(v,y),S=f(g,_),w=p(v,y),A=p(g,_);s.x=b,s.y=S,s.width=w-b,s.height=A-S}j(){const{x:t,y:e,width:s,height:i}=this.h,{style:o}=this.S;o.left=`${t}px`,o.top=`${e}px`,o.width=`${s}px`,o.height=`${i}px`}$(t,s){const{document:i,features:n}=this._,{u:r}=this;o(i,["mousemove","touchmove"],this.R),o(i,["touchmove","mousemove"],this.H),o(i,["mouseup","touchcancel","touchend"],this.$),o(i,"scroll",this.D),t&&r&&n.singleTap.allow?this.F(t):r||s||(this.C(),this.M("stop",t)),this.m.x=0,this.m.y=0,this.p&&o(i,"wheel",this.I,{passive:!0}),this.A.remove(),this.T?.cancel(),e(this.S,"display","none"),this.U()}C(){const{o:t,_:e,i:s,h:i}=this,{stored:o,selected:n,touched:r}=s,{intersect:c,overlap:a}=e.behaviour,l="invert"===a,u=[],d=[],p=[];for(let e=0;e<t.length;e++){const s=t[e];if(h(i,s.getBoundingClientRect(),c)){if(n.includes(s))o.includes(s)&&!r.includes(s)&&r.push(s);else{if(l&&o.includes(s)){p.push(s);continue}d.push(s)}u.push(s)}}l&&d.push(...o.filter((t=>!n.includes(t))));const f="keep"===a;for(let t=0;t<n.length;t++){const e=n[t];u.includes(e)||f&&o.includes(e)||p.push(e)}s.selected=u,s.changed={added:d,removed:p},this.q=u[u.length-1]}M(t,e){return this.emit(t,{event:e,store:this.i,selection:this})}U(){const{_:t,i:e}=this,{selected:s,changed:i,touched:o,stored:n}=e,r=s.filter((t=>!n.includes(t)));switch(t.behaviour.overlap){case"drop":e.stored=[...r,...n.filter((t=>!o.includes(t)))];break;case"invert":e.stored=[...r,...n.filter((t=>!i.removed.includes(t)))];break;case"keep":e.stored=[...n,...s.filter((t=>!n.includes(t)))]}}trigger(t,e=!0){this.k(t,e)}resolveSelectables(){this.o=a(this._.selectables,this._.document)}clearSelection(t=!0){this.i={stored:t?[]:this.i.stored,selected:[],touched:[],changed:{added:[],removed:[]}}}getSelection(){return this.i.stored}getSelectionArea(){return this.S}cancel(t=!1){this.$(null,!t)}destroy(){this.cancel(),this.disable(),this.A.remove(),super.unbindAllListeners()}select(t,e=!1){const{changed:s,selected:i,stored:o}=this.i,n=a(t,this._.document).filter((t=>!i.includes(t)&&!o.includes(t)));return o.push(...n),i.push(...n),s.added.push(...n),!e&&this.M("move",null),n}deselect(t,e=!1){const{selected:s,stored:i,changed:o}=this.i;return!(!s.includes(t)&&!i.includes(t))&&(o.removed.push(t),c(i,t),c(s,t),!e&&this.M("move",null),!0)}}SelectionArea.version="3.0.0-beta.13";export{SelectionArea as default};
//'''# sourceMappingURL=selection.min.js.map

FileViewerStyle = r'''
/* @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap'); */
/* @import url('https://fonts.googleapis.com/css2?family=Moon+Dance&display=swap'); */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro&display=swap');

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
    font-family: 'Noto Sans', cursive;
    background-color: rgb(72,72,72);
    background-color: linear-gradient(-45deg, rgba(72,72,72,1) 30%, rgba(41,41,41,1) 60%);
    /* backdrop-filter: blur(10px); */
    background-image: url('{{ BACKGROUND_IMAGE }}');
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
    background-attachment: fixed;
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

footer {
    position: fixed;
    bottom: 0;
    width: 100%
}

main {
    width: 100%;
    backdrop-filter: blur(2px) brightness(50%);
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
    justify-content: left;
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
    padding-top: 0.5em;
    padding-bottom: 0.5em;
    margin-left: 0em;
    margin-right: 1.5em;
    border-radius: 0.2em;
    /* background: rgba(66, 68, 90, 0.075);
    background: transparent; 
    border: 2px solid transparent; */
    cursor: pointer;
}

main .boxes.green div.selected {
    color: #292929;
    background: linear-gradient(45deg, rgba(20,126,184,0.6) 40%, rgba(105,191,238,0.6) 94%);
    background-color: rgba(255,0,0,0.45);
    /* background: linear-gradient(45deg, rgba(235,95,52,0.6) 40%, rgba(235,204,52,0.6) 94%);
    background-color: rgba(255, 0, 0, 0.45); */
    /* background: hsl(100, 80%, 65%);
       border: 2px solid rgba(235, 95, 52, 0.075); */
}

.slider {
    -webkit-appearance: none;
    width: 100%;
    border-radius: 4px;
    height: 5px;
    /* border: 1px solid #bdc3c7; */
    background-color: rgb(238,238,238);
background: radial-gradient(circle, rgba(238,238,238,1) 21%, rgba(187,187,187,1) 50%, rgba(238,238,238,1) 81%);; 
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  background-color: #ecf0f1;
  border: 1px solid #bdc3c7;
  width: 14px;
  height: 14px;
  border-radius: 7px;
  cursor: pointer;
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

.style-panel {
    text-align: center; 
    font-size: 13px; 
    color: white; 
    display: flex; 
    justify-content: center;
    background-color: rgba(29, 29, 29, 0.8);
    backdrop-filter: blur(3px);
}

.attribute-panel {
    width: 140px; 
    height: 50px;
    float: left;  
    margin: 10px;
    font-family: 'Be Vietnam Pro', sans-serif;
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

// drag and drop callbacks.
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
        // divElement.style.cursor = 'move';
        
        // drag and drop events.
        divElement.draggable = true;
        divElement.addEventListener('dragstart', function(event){
            // console.log(this.id);
            this.style.cursor = "move";
            event.dataTransfer.setData("text", this.id);
        })
        divElement.addEventListener('drop', function(event){
            event.preventDefault();
            var path = event.dataTransfer.getData("text");
            console.log(`Dragged ${path} into ${this.id}`);
        })
        divElement.addEventListener('dragover', function(event){
            event.preventDefault();
            console.log("drag over");
            this.style.cursor = "pointer";
        })
        
        divElement.innerHTML = `
    <img id="thumbnail_${fileViewerPaths[i]}" class="icon" src="${fileViewerIcons[i]}" width="40px;"/>
    <br>
    <span class="item_name" style="overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; text-align: center; font-size: 13px;">${fileViewerItems[i]}</span>`
        divElement.onclick = function() {
            // console.error(this.id);
            var file_item_id = this.id;
            new QWebChannel(qt.webChannelTransport, function(channel) {
                var eventHandler = channel.objects.eventHandler;
                eventHandler.sendClickedItem(file_item_id);
            });
        }
        divElement.addEventListener("dblclick", function() {
            var file_item_id = this.id;
            new QWebChannel(qt.webChannelTransport, function(channel) {
                var eventHandler = channel.objects.eventHandler;
                eventHandler.sendOpenRequest(file_item_id);
            });
        })
        divElement.addEventListener('contextmenu', function(event) {
            // event.preventDefault(); // disable regular contextmenu.
            event.preventDefault();
            var file_item = this;
            new QWebChannel(qt.webChannelTransport, function(channel) {
                var eventHandler = channel.objects.eventHandler;
                eventHandler.triggerContextMenu(file_item.id);
            });
            console.log(event);
            // file_item.dispatchEvent(new CustomEvent('contextmenu'));
        });
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
// create file item.
function itemDrag(event) {
    console.log(event.target.id);
    event.dataTransfer.setData("text", event.target.id);
}
function enableItemDrop(event) {
    event.preventDefault();
}
function itemDrop(element, event) {
    event.preventDefault();
    var data = event.dataTransfer.getData("text");
    console.error(`Dragged ${data} into ${element.id}`);
    // event.target.appendChild(document.getElementById(data));
}

class OrchardAppearance {
    constructor() {
        var body = document.getElementsByTagName("main")[0]; // document.getElementByTagName();
        this.style = window.getComputedStyle(body);
    }
    get(attr) {
        var body = document.getElementsByTagName("main")[0];
        this.style = window.getComputedStyle(body);
        
        return this.style.getPropertyValue(attr);
    }
    set(attr, value) {
        document.getElementsByTagName("main")[0].style.setProperty(attr, value);
    }
    setFilter(filter, val) {
        var filter_str = this.get('backdrop-filter');
        var all_filters = filter_str.split(" ");
        var filter_exists = false
        for (let i=0; i<all_filters.length; i++) {
            if (all_filters[i].startsWith(filter)) {
                all_filters[i] = `${filter}(${val})`;
                filter_exists = true;
            }   
        }
        if (filter_exists == false) {
            all_filters.push(`${filter}(${val})`);
        }
        filter_str = all_filters.join(" ");
        this.set('backdrop-filter', filter_str);
    }
    setGrayScale(val) {
        this.setFilter('grayscale', val);
    }
    setContrast(val) {
        this.setFilter('contrast', val);
    }
    setInvert(val) {
        this.setFilter('invert', val);
    }
    setOpacity(val) {
        this.setFilter('opacity', val);
    }
    setSaturate(val) {
        this.setFilter('saturate', val);
    }
    setBlurRadius(radius) {
        var filter_str = this.get('backdrop-filter');
        var all_filters = filter_str.split(" ");
        var filter_exists = false
        for (let i=0; i<all_filters.length; i++) {
            if (all_filters[i].startsWith('blur')) {
                all_filters[i] = `blur(${radius}px)`;
                filter_exists = true;
            }   
        }
        if (filter_exists == false) {
            all_filters.push(`blur(${radius}px)`);
        }
        filter_str = all_filters.join(" ");
        this.set('backdrop-filter', filter_str);
    }
    // backdrop-filter: hue-rotate(120deg);
    // backdrop-filter: drop-shadow(4px 4px 10px blue);
    setBrightness(val) {
        this.setFilter('brightness', val);
    }
    setSepia(val) {
        this.setFilter('sepia', val);
    }
}
let oa = new OrchardAppearance();

function selectItemById(id) {
    selectedItem = document.getElementById(id);
    selectedItem.classList.add("selected");
}

function createItem(path, name, icon, hidden) {
    var item = document.createElement('div');
    item.id = path;
    console.log(`creating item: ${name} at ${path}, icon=${icon}`)
    var hiddenFileFlag = document.createAttribute('data-filehidden');
    hiddenFileFlag.value = hidden;
    item.setAttributeNode(hiddenFileFlag)
    item.className = "file_item";
    item.style.textAlign = 'center';
    item.innerHTML = `
    <img class="icon" src="${icon}" width="40px" max-height="40px"/>
    <br>
    <span class="item_name" style="text-align: center; font-size: 14px;">${name}</span>`
    item.onclick = function() {
        var file_item_id = this.id;
        new QWebChannel(qt.webChannelTransport, function(channel) {
            var eventHandler = channel.objects.eventHandler;
            eventHandler.sendClickedItem(file_item_id);
        });
    }
    item.addEventListener("dblclick", function() {
        var file_item_id = this.id;
        new QWebChannel(qt.webChannelTransport, function(channel) {
            var eventHandler = channel.objects.eventHandler;
            eventHandler.sendOpenRequest(file_item_id);
        });
    })
    if (hidden == "1") {
        item.style.display = "none";
    }
    return item;
}
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

// this function is the callback triggered on an item rename event
function handleItemRename(event) {
    // specifically handle enter key.
    if (event.keyCode === 13) { 
        // console.log(`${selectedItemElement.id} renamed to ${selectedItemSpan.innerText}`);
        new QWebChannel(qt.webChannelTransport, function(channel) {
            var eventHandler = channel.objects.eventHandler;
            var id = selectedItemElement.id;
            var newName = selectedItemSpan.innerText;
            eventHandler.triggerRename(id, newName);
        });
        event.preventDefault();
        selectedItemSpan.style.backgroundColor = "";
        selectedItemSpan.style.color = "";
        selectedItemSpan.setAttribute('contenteditable', 'false');
        // make span uneditable
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

        <!-- CSS / JS -->
        <style>{{ FILEVIEWER_CSS }}</style>
    </head>

    <body>
        <main>
            <section class="demo">
                <section id="orchard" class="boxes green"></section>
            </section>
            <br><br><br><br>
            <br><br><br><br>
            <br><br><br><br>
            <br><br><br><br>
            <br><br><br><br>
        </main>
        <script>{{ WEBCHANNEL_JS }}</script>
        <script>{{ FIG_DESKTOP_NOTIF_JS }}</script>
        <script>{{ FIG_FILE_MANAGER_JS }}</script>
        <script>{{ FILEVIEWER_CJS }}</script>
        <script type="module">{{ FILEVIEWER_MJS }}</script>
        <footer>
            <div class="style-panel" id="background_style_panel_1">
                <div class="attribute-panel">
                    <span>gray scale</span><br>
                    <input type="range" min="1" max="100" value="0" class="slider" onchange="oa.setGrayScale(this.value/100)">
                </div>
                <div class="attribute-panel">
                    <span>contrast</span><br>
                    <input type="range" min="1" max="100" value="100" class="slider" onchange="oa.setContrast(this.value/100)">
                </div>
                <div class="attribute-panel">
                    <span>invert</span><br>
                    <input type="range" min="1" max="100" value="0" class="slider" onchange="oa.setInvert(this.value/100)">
                </div>
                <div class="attribute-panel">
                    <span>opacity</span><br>
                    <input type="range" min="1" max="100" value="100" class="slider" onchange="oa.setOpacity(this.value/100)">
                </div>
                <br>
                <div class="attribute-panel">
                    <span>saturation</span><br>
                    <input type="range" min="1" max="100" value="100" class="slider" onchange="oa.setSaturate(this.value/100)">
                </div>
                <div class="attribute-panel">
                    <span>blur radius</span><br>
                    <input type="range" min="1" max="30" value="2" class="slider" onchange="oa.setBlurRadius(this.value)">
                </div>
                <div class="attribute-panel">
                    <span>brightness</span><br>
                    <input type="range" min="1" max="100" value="50" class="slider" onchange="oa.setBrightness(this.value/100)">
                </div>
                <div class="attribute-panel">
                    <span>sepia</span><br>
                    <input type="range" min="1" max="100" value="0" class="slider" onchange="oa.setSepia(this.value/100)">
                </div>
            </div>
        </footer>
    </body>
</html>''')
class EventHandler(QObject):
    def __init__(self, fileviewer):
        super(EventHandler, self).__init__()
        self.fileviewer = fileviewer

    @pyqtSlot(str)
    def sendClickedItem(self, path: str):
        # print(f"selected path {path}")
        self.fileviewer.updateSelection(path)

    @pyqtSlot(str)
    def sendOpenRequest(self, path: str):
        # print(f"opened path {path}")
        self.fileviewer.open(path)

    @pyqtSlot(str)
    def triggerContextMenu(self, path: str):
        # self.fileviewer.webview.menu = self.fileviewer.webview.itemMenu
        print(f"context menu triggered for {path}")

    @pyqtSlot(str, str)
    def triggerRename(self, id: str, new_name: str):
        new_name = new_name.strip()
        self.fileviewer.renameItem(id, new_name)
        

fileviewer_searchbar_style = jinja2.Template('''
QLineEdit {
    border: 0px;
    font-size: 17px;
    font-family: 'Be Vietnam Pro', sans-serif;
    padding-top: 3px;
    padding-bottom: 3px;
    color: #fff; /* #ad3700; */
    /* background: qlineargradient(x1 : 1, y1 : 0, x2 : 0, y2: 0, stop: 0 #828282, stop: 0.5 #eee, stop: 1 #828282); */
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
    border-radius: {{ BORDER_RADIUS }};
}
QLabel {
    font-size: 16px;
}''')
class FileViewerSearchBar(QLineEdit):
    def __init__(self, parent: Union[QWidget, None]=None):
        super(FileViewerSearchBar, self).__init__(parent)
        # search action.
        self.searchAction = QAction()
        self.searchAction.setIcon(FigD.Icon("system/fileviewer/search.svg"))
        self.addAction(self.searchAction, self.LeadingPosition)
        # match case.
        self.caseAction = QAction()
        self.caseAction.setIcon(
            FigD.Icon("system/fileviewer/case.svg")
        )
        self.addAction(self.caseAction, self.TrailingPosition)
        # self.matchWholeAction.setIcon(
        #     FigD.Icon("system/fileviewer/match_whole.svg")
        # )
        # match prefix.
        self.prefixAction = QAction()
        self.prefixAction.setIcon(
            FigD.Icon("system/fileviewer/prefix.svg")
        )
        self.addAction(self.prefixAction, self.TrailingPosition)
        # match suffix.
        self.suffixAction = QAction()
        self.suffixAction.setIcon(
            FigD.Icon("system/fileviewer/suffix.svg")
        )
        self.addAction(self.suffixAction, self.TrailingPosition)
        # match contains.
        self.containsAction = QAction()
        self.containsAction.setIcon(
            FigD.Icon("system/fileviewer/match_contains.svg")
        )
        self.addAction(self.containsAction, self.TrailingPosition)
        self.setStyleSheet(fileviewer_searchbar_style.render(
            BORDER_RADIUS=16,
        ))
        self.setFixedHeight(28)
        self.setClearButtonEnabled(True)
        self.returnPressed.connect(self.search)
        # completion for search.
        self.completer = QCompleter()
        self.completer.setModel(QDirModel(self.completer))
        self.completer.popup().setStyleSheet("""font-family: 'Be Vietnam Pro', sans-serif; color: #fff; background: #000; border: 0px;""")
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        # self.completer.setCompletionMode(QCompleter.PopupCompletion)
        # self.completer.setFilterMode(Qt.MatchContains)
        self.setCompleter(self.completer)

    def search(self):
        pass
        # print("searched")

class FileViewerStatus(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None, 
                 webview: Union[DebugWebView, None]=None):
        super(FileViewerStatus, self).__init__(parent)    
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.webview = webview
        self.layout.setSpacing(5)    
        self.selected = self.initBtn(icon="file.svg", text=" selected: None") # name of seelcted item.
        self.num_items = self.initBtn(icon="item.png", text="(contains 0 items)") # number of items in selected item 
        self.file_size = self.initBtn(icon="storage.svg", text=" 0kB") # size of selected item
        self.breakdown = QLabel("0 items (0 files, 0 folders, 0 hidden)")
        # self.user = self.initBtn(icon="user.svg", text=" "+getpass.getuser())
        self.hostname = self.initBtn(icon="server.svg", text=f" {socket.gethostname()}@{getpass.getuser()}")
        self.owner = self.initBtn(icon="owner.svg", text=" <user>")
        self.group = self.initBtn(icon="group.svg", text=" <group>")
        self.permissions = self.initBtn(icon="permissions.svg", text="[RWX]")
        self.symlink = self.initBtn(icon=None, text=None)
        self.shortcut = self.initBtn(icon=None, text=None)
        # add widgets.
        self.layout.addWidget(self.breakdown)
        # self.layout.addWidget(self.user)
        self.layout.addWidget(self.hostname)
        self.layout.addStretch(1)
        self.layout.addWidget(self.selected)
        self.layout.addWidget(self.num_items)
        self.layout.addWidget(self.file_size)
        self.layout.addWidget(self.owner)
        self.layout.addWidget(self.group)
        self.layout.addWidget(self.permissions)
        self.layout.addWidget(self.symlink)
        self.layout.addWidget(self.shortcut)
        # set layout and style
        self.setLayout(self.layout)
        self.setObjectName("CodeMirrorStatus")
        self.setStyleSheet('''
        QWidget#CodeMirrorStatus {
            color: #6e6e6e;
            border: 0px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-size: 16px;
            background: transparent;
        }
        QLabel {
            color: #6e6e6e;
            border: 0px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-size: 16px;
            background: transparent;
        }''')
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def updateSelected(self, **data):
        size = data.get("size", 0)
        icon = data.get("icon", "")
        name = data.get("name", "")
        items = data.get("items", 0)
        
        owner = data.get("owner")
        group = data.get("group")
        last_read = data.get("last_read")
        permissions = data.get("permissions")
        last_modified = data.get("last_modified")
        meta_change_time = data.get("meta_change_time")
        
        shortcut = data.get("shortcut", False)
        symbolic = data.get("symbolic", False)
        if symbolic:
            print("is a symlink")
            self.symlink.setIcon(FigD.Icon("system/fileviewer/symlink.svg"))
        if shortcut:
            print("is a shortcut")
            self.shortcut.setIcon(FigD.Icon("system/fileviewer/shortcut.png"))

        self.selected.setText(f" selected: {name}")
        self.file_size.setText(f" {size}")
        self.permissions.setText(f" {permissions}")
        self.owner.setText(f" {owner}")
        self.group.setText(f" {group}")
        # self.last_read.setText()
        # self.last_modified.setText()
        # self.

        if icon != "":
            self.selected.setIcon(QIcon(icon))
        if items != 0:
            self.num_items.setText(f"(contains {items} items)")
        else:
            self.num_items.setText("")

    def updateBreakdown(self, **data):
        items = data.get("items", 0)
        files = data.get("files", 0)
        hidden = data.get("hidden", 0)
        folders = data.get("folders", 0)
        self.breakdown.setText(f"{items} items ({files} files, {folders} folders, {hidden} hidden)")

    def initBtn(self, icon=None, text=None):
        btn = QToolButton(self)
        if icon: 
            icon = os.path.join("system/fileviewer", icon)
            btn.setIcon(FigD.Icon(icon))
        if text: btn.setText(text)
        btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        btn.setStyleSheet("background: #292929; color: #fff;")
        btn.setStyleSheet('''
        QToolButton {
            color: #6e6e6e;
            border: 0px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-size: 16px;
            background: transparent;
        }
        QToolButton:hover {
            border: 0px;
            background: rgba(0, 0, 0, 0.5);
        }''')

        return btn


class FileViewerWebView(DebugWebView):
    '''fileviewer web view'''
    def __init__(self):
        super(FileViewerWebView, self).__init__()
        self.orchardMenu = QMenu()
        self.orchardMenu.setStyleSheet("background: #292929; color: #fff;")
        self.orchardMenu.addAction("New Folder")
        self.orchardMenu.addAction("New File")
        self.orchardMenu.addSeparator()
        self.orchardMenu.addAction("Restore Missing Files...")
        self.orchardMenu.addAction("Open in Terminal")
        self.orchardMenu.addSeparator()
        self.orchardMenu.addAction("Paste")
        self.orchardMenu.addSeparator()
        self.orchardMenu.addAction("Properties")

        self.itemMenu = QMenu()
        self.itemMenu.setStyleSheet("background: #292929; color: #fff;")
        self.itemMenu.addAction("Open")
        self.itemMenu.addAction("Open With")
        self.itemMenu.addSeparator()
        self.itemMenu.addAction("Cut")
        self.itemMenu.addAction("Copy")

    def dragEnterEvent(self, e):
        e.ignore()
    # def itemContextMenuEvent(self, event):
    #     '''show item specific context menu (for the selected item)'''
    #     self.itemMenu.popup(event.globalPos())
    def contextMenuEvent(self, event):
        '''show the orchared context menu (not specific to a selected item)'''
        # print(dir(event))
        self.orchardMenu.popup(event.globalPos())

    def connectWidget(self, widget):
        self.widget = widget
        # New folder action.
        self.orchardMenu.actions()[0].triggered.connect(
            lambda: widget.createDialogue(item_type="folder")
        )
        # New file action.
        self.orchardMenu.actions()[1].triggered.connect(
            lambda: widget.createDialogue(item_type="file")
        )

    def initiateRenameForId(self, id: str):
        '''make the span displaying the item_name editanle for the selected item'''
        code = f'''selectedItemElement = document.getElementById('{id}');
selectedItemSpan = selectedItemElement.getElementsByClassName('item_name')[0];
// selectedItemSpan
selectedItemSpan.setAttribute('contenteditable', 'true');
selectedItemSpan.style.backgroundColor = "white";
selectedItemSpan.style.color = "black";
selectedItemSpan.focus()
document.execCommand('selectAll', false, null);
document.getSelection().collapseToEnd();
selectedItemSpan.addEventListener('keypress', handleItemRename);
'''        
        # print(code)
        self.page().runJavaScript(code)

    def createItem(self, path: str, name: str, 
                  icon: str, hidden: bool=False):
        '''
        Create a file item from arguments:
        path (or id of the div): the exact file location.
        name: the displayed file name.
        icon: the icon for the file item.
        hidden: whether the file is hidden or displayed.
        '''
        hidden = 1 if hidden else 0
        code = f'''
        var newItemDivElement = createItem('{path}', '{name}', '{icon}', {hidden}); // create the new file item.
        orchard.prepend(newItemDivElement); // add the new file item to the green boxes section which is marked by the 'orchard' id.
        '''
        self.page().runJavaScript(code)

#eb5f34
class FileViewerBtn(QToolButton):
    '''File viewer button'''
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(FileViewerBtn, self).__init__(parent)
        tip = args.get("tip", "a tip")
        size = args.get("size", (23,23))
        self.hover_response = "background"
        if "icon" in args:
            self.inactive_icon = os.path.join("system/fileviewer", args["icon"])
            stem, ext = os.path.splitext(Path(args["icon"]))
            active_icon = f"{stem}_active{ext}"
            self.active_icon = os.path.join("system/fileviewer", active_icon)
            if os.path.exists(FigD.icon(self.active_icon)):
                self.hover_response = "foreground"
            self.setIcon(FigD.Icon(self.inactive_icon))
        elif "text" in args:
            self.setText(args["text"])
        self.setIconSize(QSize(*size))
        self.setToolTip(tip)
        self.setStatusTip(tip)
        if self.hover_response == "background":
            self.setStyleSheet('''
            QToolButton {
                color: #fff;
                border: 0px;
                font-size: 14px;
                background: transparent;
            }
            QToolButton:hover {
                color: #292929;
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #147eb8, stop : 0.3 #69bfee, stop: 0.9 #338fc0);
            }
            QToolTip {
                color: #fff;
                border: 0px;
                background: #000;
            }''')
        else:
            self.setStyleSheet('''
            QToolButton {
                color: #fff;
                border: 0px;
                font-size: 14px;
                background: transparent;
            }
            QToolTip {
                color: #fff;
                border: 0px;
                background: #000;
            }''')

    def leaveEvent(self, event):
        if self.hover_response == "foreground":
            self.setIcon(FigD.Icon(self.inactive_icon))
        super(FileViewerBtn, self).leaveEvent(event)

    def enterEvent(self, event):
        if self.hover_response == "foreground":
            self.setIcon(FigD.Icon(self.active_icon))
        super(FileViewerBtn, self).enterEvent(event)


class FileViewerGroup(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None,
                 name: str="Widget Group"):
        super(FileViewerGroup, self).__init__(parent)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(0)
        self.group = QWidget()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setSpacing(2)
        self.group.setLayout(self.layout)
        layout.addStretch(1)
        layout.addWidget(self.group)
        layout.addWidget(self.Label(name))
        self.setLayout(layout)

    def Label(self, name):
        name = QLabel(name)
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet('''
        QLabel {
            border: 0px;
            border-right: 1px;
            padding: 6px;
            color: #69bfee;
            font-size: 16px;
            font-family: 'Be Vietnam Pro', sans-serif;
            background: transparent;
        }''')
        return name

    def initBtnGroup(self, btn_args, 
                     orient="horizontal", 
                     alignment_flag=None,
                     spacing=None):
        btnGroup = QWidget()
        btnGroup.btns = []
        if orient == "horizontal":
            layout = QHBoxLayout()
        elif orient == "vertical":
            layout = QVBoxLayout()
        if spacing is not None:
            # print("setting spacing")
            layout.setSpacing(spacing)
        layout.setContentsMargins(0, 0, 0, 0)
        btnGroup.layout = layout
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
            if alignment_flag is None:
                layout.addWidget(btn, 0, Qt.AlignCenter)
            else:
                layout.addWidget(btn, 0, alignment_flag)
        layout.addStretch(1)
        btnGroup.setLayout(layout)

        return btnGroup

    def initBtn(self, **args):
        return FileViewerBtn(self, **args)
        # btn = QToolButton(self)
        # tip = args.get("tip", "a tip")
        # size = args.get("size", (23,23))
        # if "icon" in args:
        #     icon = os.path.join("system/fileviewer", args["icon"])
        #     btn.setIcon(FigD.Icon(icon))
        # elif "text" in args:
        #     btn.setText(args["text"])
        # btn.setIconSize(QSize(*size))
        # btn.setToolTip(tip)
        # btn.setStatusTip(tip)
        # btn.setStyleSheet('''
        # QToolButton {
        #     color: #fff;
        #     border: 0px;
        #     font-size: 14px;
        #     background: transparent;
        # }
        # QToolButton:hover {
        #     color: #292929;
        #     background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34);
        # }
        # QToolTip {
        #     color: #fff;
        #     border: 0px;
        #     background: #000;
        # }''')

        # return btn 
# backdrop-filter: drop-shadow(4px 4px 10px blue);
# backdrop-filter: hue-rotate(120deg);
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
            size=(40,40),
            tip="connect to a server",
        )
        self.linkGroup = self.initBtnGroup([
            {"icon": "link.svg", "size": (20,20)},
            {"icon": "unlink.svg", "size": (20,20), "tip": "move selected item(s) to trash"},
        ])
        self.linkNServer = QWidget()
        self.linkNServerLayout = QVBoxLayout()
        self.linkNServerLayout.setContentsMargins(0, 0, 0, 0)
        self.linkNServer.setLayout(self.linkNServerLayout)
        self.linkNServerLayout.addWidget(self.connectToServerBtn)
        self.linkNServerLayout.addWidget(self.linkGroup)
        self.layout.addWidget(self.creationWidget)
        self.layout.addWidget(self.linkNServer)

    def connectWidget(self, widget):
        self.widget = widget
        # self.newFileBtn.clicked.connect(widget.createFile)
        self.newFolderBtn.clicked.connect(
            lambda: widget.createDialogue(item_type="folder")
        )
        self.newFileBtn.clicked.connect(
            lambda: widget.createDialogue(item_type="file")
        )


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
            icon="back.svg",
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
            icon="copy_as_url.svg",
            size=(25,25),
            tip="copy file path as url",
        )
        self.stemBtn = self.initBtn(
            text="stem", size=(25,25),
            tip="copy file name without extension",
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
        self.navLayout.addWidget(self.stemBtn)
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
        self.editWidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding) 
        self.editLayout = QVBoxLayout()
        self.editLayout.setContentsMargins(0, 0, 0, 0)
        # undo, redo, rename
        self.renameGroup = self.initBtnGroup([
            {"icon": "undo.svg", "size": (25,25), "tip": "undo rename"},
            {"icon": "rename.svg", "size": (25,25), "tip": "rename file/folder"},
            {"icon": "redo.svg", "size": (25,25) , "tip": "redo rename"},
        ])
        self.undoBtn = self.renameGroup.btns[0]
        self.renameBtn = self.renameGroup.btns[1]
        self.redoBtn = self.renameGroup.btns[2]
        # cut, copy, paste
        self.moveGroup = self.initBtnGroup([
            {"icon": "cut.png", "size": (28,28), "tip": "cut selected item"},
            {"icon": "copy.svg", "size": (35,35), "tip": "copy selected items"},
            {"icon": "paste.png", "size": (37,37), "tip": "paste selected items from the clipboard"},
        ])
        # make link, release link, move to trash
        self.linkGroup = self.initBtnGroup([
            # {"icon": "link.svg", "size": (20,20)},
            # {"icon": "unlink.svg", "size": (20,20), "tip": "move selected item(s) to trash"},
            {"icon": "trash.svg", "size": (40,40), "tip": "move selected item(s) to trash"},
        ], orient="vertical")
        # self.sortWidget = QWidget()
        # self.editLayout.addStretch(1)
        self.editLayout.addWidget(self.renameGroup)
        self.editLayout.addWidget(self.moveGroup)
        # self.editLayout.addStretch(1)
        self.editWidget.setLayout(self.editLayout)
        self.layout.addStretch(1)
        self.layout.addWidget(self.editWidget)
        self.layout.addWidget(self.linkGroup)
        self.layout.addStretch(1)    

    def connectWidget(self, widget):
        self.widget = widget
        self.renameBtn.clicked.connect(widget.renameDialog)


class FileViewerViewGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerViewGroup, self).__init__(parent, "View")
        self.viewWidget = QWidget() 
        self.viewLayout = QVBoxLayout()
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        # layout of file items
        self.layoutGroup = self.initBtnGroup([
            {"icon": "gridview.svg", "size": (25,25), "tip": "tile view"},
            {"icon": "list_view.svg", "size": (20,20), "tip": "list view"},
            {"icon": "treelistview.svg", "size": (20,20), "tip": "tree view"},
            {"icon": "toggle_hidden_files.png", "size": (23,23), "tip": "toggle visibility of hidden files"},
        ])
        # hidden files, folder bar visibility, side bar visibility, search bar visibility.
        self.visibilityGroup = self.initBtnGroup([
            {"icon": "toggle_folderbar.svg", "size": (35,35), "tip": "toggle visibility of folder bar"},
            {"icon": "toggle_searchbar.svg", "size": (27,27), "tip": "toggle visibility of search bar"},
            {"icon": "toggle_sidebar.svg", "size": (27,27), "tip": "toggle visibility of sidebar"},
        ])
        self.hiddenFilesBtn = self.layoutGroup.btns[-1]
        self.folderbarBtn = self.visibilityGroup.btns[0]
        self.searchbarBtn = self.visibilityGroup.btns[1]
        self.sidebarBtn = self.visibilityGroup.btns[2]
        self.arrangeGroup = self.initBtnGroup([
            {"icon": "sidebar_left.svg", "size": (25,25), "tip": "sidebar to the left"},
            {"icon": "sidebar_right.svg", "size": (25,25), "tip": "sidebar to the right"},
        ], orient="vertical", spacing=0)     
        self.viewLayout.addStretch(1)
        self.viewLayout.addWidget(self.layoutGroup)
        self.viewLayout.addWidget(self.visibilityGroup)
        # self.viewLayout.addWidget(self.arrangeGroup)
        self.viewWidget.setLayout(self.viewLayout)
        # self.layout.addStretch(1)
        self.layout.addWidget(self.viewWidget)
        self.layout.addWidget(self.arrangeGroup)
        # self.layout.addStretch(1)    
    def connectWidget(self, widget):
        self.widget = widget
        self.folderbarBtn.clicked.connect(
            widget.folderbar.toggle
        )
        self.sidebarBtn.clicked.connect(
            widget.sidebar.toggle
        )

        self.hiddenFilesBtn.clicked.connect(
            widget.toggleHiddenFiles
        )


class FileViewerSelectGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerSelectGroup, self).__init__(parent, "Select")
        # self.selectionWidget = QWidget() 
        # self.selectionLayout = QVBoxLayout()
        # self.selectionLayout.setContentsMargins(0, 0, 0, 0)
        # self.selectionLayout.setSpacing(0)
        self.selectionGroup1 = self.initBtnGroup([
            {"icon": "clear_selection.png", "size": (30,30), "tip": "clear current selection", "icon_size": (30,30)},
            {"icon": "select_all.png", "size": (30,30), "tip": "select all items", "icon_size": (30,30)},
        ], orient="vertical", spacing=0)
        self.selectionGroup2 = self.initBtnGroup([
            {"icon": "invert_selection.png", "size": (30,30), "tip": "invert selected items", "icon_size": (30,30)},
        ], orient="vertical", spacing=0)
        self.clearBtn = self.selectionGroup1.btns[0]
        self.selectAllBtn = self.selectionGroup1.btns[1]
        self.invertBtn = self.selectionGroup2.btns[0]
        self.layout.addWidget(self.selectionGroup1)
        self.layout.addWidget(self.selectionGroup2, 0, Qt.AlignCenter | Qt.AlignBottom)
        # self.selectionLayout.addWidget(self.selectionGroup)
        # self.selectionLayout.addStretch(1)
        # self.selectionWidget.setLayout(self.selectionLayout)
        # self.layout.addStretch(1)
        # self.layout.addWidget(self.selectionWidget)
        # self.layout.addStretch(1)    
    def connectWidget(self, widget):
        self.widget = widget
        self.clearBtn.clicked.connect(widget.clearSelection)
        self.selectAllBtn.clicked.connect(widget.selectAll)
        self.invertBtn.clicked.connect(widget.invertSelection)


class XdgOpenDropdown(QComboBox):
    '''Dropdown of available applications for opening file of particular type.'''
    def __init__(self, mimetype: str):
        super(XdgOpenDropdown, self).__init__()
        self.setEditable(True)
        self.lineEdit().setAlignment(Qt.AlignCenter)
        self.lineEdit().textChanged.connect(self.adjustCursor)
        self.mime_to_apps = MimeTypeDefaults()
        self.populate(mimetype)
        self.currentIndexChanged.connect(self.selChanged)
        self.setStyleSheet("background: #292929; color: #69bfee; font-size: 15px; text-align: left;")

    def adjustCursor(self):
        '''adjust cursor to the starting position.'''
        self.lineEdit().setCursorPosition(0)

    def connectWidget(self, widget: QWidget):
        self.widget = widget
        self.clearBtn.clicked.connect(widget.clearSelection)
        self.selectAllBtn.clicked.connect(widget.selectAll)
        self.invertBtn.clicked.connect(widget.invertSelection)

    def getAppsList(self, mimetype: str):
        '''get list of apps available for a given mimetype.'''
        apps = self.mime_to_apps(mimetype)
        # print(mimetype)
        self.desktop_files = []
        app_names = []
        for app in apps:
            desktop_file = DesktopFile(app)
            # desktop_file.read()
            self.desktop_files.append(desktop_file)
            # print(desktop_file)
            app_names.append(desktop_file.app_name)

        return app_names

    def xdgOpen(self, file: str):
        '''use xdg-open on a specific file'''
        os.system(f"xdg-open {file}")

    def gtkLaunch(self, app: str, file: str=""):
        '''do a gtk launch of a specific application with or without a specific file.'''
        # os.system(f"gtk-launch {app} '{file}'")
        # print(f"gtk-launch {app} '{file}'")

    def open(self, file):
        i = self.currentIndex()
        self.gtkLaunch(self.apps[i], file)

    def populate(self, mimetype: str):
        # clear combox box.
        # get list of available apps.
        self.clear()
        self.apps = self.getAppsList(mimetype)
        for app in self.apps:
            self.addItem(app)

    def selChanged(self, index: int):
        '''selected application (for xdg-open) is changed.'''
        # print(index, self.apps)
        appSelected = self.apps[index]
        # print(appSelected)

class FileViewerOpenGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerOpenGroup, self).__init__(parent, "Open")
        self.xdgOpenWidget = self.initXdgOpenWidget()
        # opener widget.
        self.openerGroup = self.initBtnGroup([
            {"icon": "terminal.svg", "size":(40,40),
            'tip': "open in terminal"},
            {"icon": "browser.svg", "size":(40,40),
            'tip': "open in browser"},
        ], orient="vertical", spacing=0)
        self.terminalBtn = self.openerGroup.btns[0]
        self.browserBtn = self.openerGroup.btns[1]

        self.layout.addStretch(1)
        self.layout.addWidget(self.xdgOpenWidget)
        self.layout.addWidget(self.openerGroup)
        self.layout.addStretch(1)   

    def updateMimeBtn(self, mimetype: str, 
                      icon: QIcon, path: str):
        self.mimeBtn.setText(mimetype)
        # self.mimeBtn.setToolTip(tip)
        # self.mimeBtn.setStatusTip(tip)
        self.mimeBtn.setIcon(QIcon(icon))
        self.mimeBtn.setIconSize(QSize(35,35))
        self.appDropdown.populate(mimetype)
        self.mimeBtn.clicked.connect(lambda: self.appDropdown.open(path))

    def initXdgOpenWidget(self):
        '''change xdg-open settings.'''
        xdgOpenWidget = QWidget() 
        xdgOpenLayout = QVBoxLayout()
        xdgOpenLayout.setContentsMargins(0, 0, 0, 0)
        xdgOpenLayout.setSpacing(0)
        # # open with label.
        # label = QLabel("Open With")
        # label.setStyleSheet('''
        # QLabel {
        #     color: #ccc;
        #     border: 0px;
        #     padding: 2px;
        #     font-size: 13px;
        #     font-weight: bold;
        #     font-family: 'Be Vietnam Pro', sans-serif;
        #     background: transparent;
        # }''')
        tip = "open selected file with selected app"
        icon = os.path.join(
            "system/fileviewer", 
            "file.svg"
        )
        self.mimeBtn = QToolButton()
        self.mimeBtn.setToolTip(tip)
        self.mimeBtn.setStatusTip(tip)
        self.mimeBtn.setText("text/plain")
        self.mimeBtn.setIcon(FigD.Icon(icon))
        self.mimeBtn.setIconSize(QSize(35,35))
        self.mimeBtn.setStyleSheet('''
        QToolButton {
            color: #fff;
            border: 0px;
            font-size: 14px;
            font-family: 'Be Vietnam Pro', sans-serif;
            background: transparent;
        }
        QToolButton:hover {
            color: #292929;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #147eb8, stop : 0.3 #69bfee, stop: 0.9 #338fc0);
        }''')
        self.mimeBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # app selection dropdown.
        self.appDropdown = XdgOpenDropdown("text/plain")
        self.appDropdown.setFixedWidth(130)
        self.appDropdown.setFixedHeight(22)
        # self.mimeBtn.clicked.connect(
        #     lambda: os.system(f"gtk-launch {} {self.selected_item}")
        # )
        xdgOpenLayout.addWidget(self.mimeBtn, 0, Qt.AlignCenter)
        # xdgOpenLayout.addWidget(label, 0, Qt.AlignCenter)
        xdgOpenLayout.addWidget(self.appDropdown)
        xdgOpenWidget.setLayout(xdgOpenLayout)

        return xdgOpenWidget

class FileViewerShareGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerShareGroup, self).__init__(parent, "Share")
        # QR, devices, bluetooth, email, copy to clipboard (contents)
        # twitter, reddit, facebook, youtube, instagram
        self.nativeGroup1 = self.initBtnGroup([
            {"icon": "devices.svg", "size":(18,18),
            'tip': "share to linked devices"},
            {"icon": "bluetooth.svg", "size":(18,18),
            'tip': "share using bluetooth"},
            {"icon": "qr.svg", "size":(18,18),
            'tip': "create qr code for file"},
        ], orient="vertical", spacing=5)
        self.nativeGroup2 = self.initBtnGroup([
            {"icon": "email.svg", "size":(25,25),
            'tip': "share file as email attachment"},
            {"icon": "copy_content.svg", "size":(25,25),
            'tip': "copy file contents to clipboard"}
        ], orient="vertical", spacing=15)
        self.appsGroup1 = self.initBtnGroup([
            {"icon": "youtube.png", "size":(28,28),
            'tip': "share video on youtube"},
            {"icon": "twitter.png", "size":(35,35),
            'tip': "share on twitter"},
            {"icon": "reddit.png", "size":(32,32),
            'tip': "share on reddit"},
        ])
        self.appsGroup2 = self.initBtnGroup([
            {"icon": "facebook.png", "size":(32,32),
            'tip': "share on facebook"},
            {"icon": "instagram.png", "size":(32,32),
            'tip': "share image on instagram"},
            {"icon": "whatsapp.png", "size":(32,32),
            'tip': "share video on youtube"},
        ])
        self.shareWidget = QWidget()
        self.shareLayout = QVBoxLayout()
        # self.shareLayout.setSpacing(0)
        self.shareLayout.setContentsMargins(0,0,0,0)
        self.shareLayout.addWidget(self.appsGroup1)
        self.shareLayout.addWidget(self.appsGroup2)
        self.shareWidget.setLayout(self.shareLayout)

        self.layout.addStretch(1)
        self.layout.addWidget(self.nativeGroup1)
        self.layout.addWidget(self.nativeGroup2)
        self.layout.addWidget(self.shareWidget)
        self.layout.addStretch(1)   
# class FileViewerPropGroup(QWidget):
# class FileViewerFilterGroup(QWidget):
# class FileViewerUtilsGroup(QWidget): encryption, compression, file conversion (for images, videos,document formats etc.)

# class FileViewerMiscGroup(QWidget): note, bookmark
# class FileViewerVCSGroup(QWidget):
# class FileViewerBackupGroup(QWidget):


class AppearanceSlider(QWidget):
    def __init__(self, icon: str="", orient: str="horizontal", 
                 initial_value: float=1, tip: str=""):
        super(AppearanceSlider, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLineEdit()
        self.label.setText(str(initial_value))
        self.label.returnPressed.connect(self.setSliderByLabel)
        self.slider = QSlider()
        if orient == "vertical":
            self.slider.setOrientation(Qt.Vertical)
        else:
            self.slider.setOrientation(Qt.Horizontal)
        self.icon = QLabel()
        path = FigD.icon(
            os.path.join("system/fileviewer", icon)
        )
        self.slider.setMaximumWidth(50)
        self.slider.valueChanged.connect(self.sliderAction)
        pixmap = QPixmap(path)
        if icon.endswith(".png"):
            pixmap = pixmap.scaled(
                QSize(20,20), 
                aspectRatioMode=Qt.KeepAspectRatio,
                transformMode=Qt.SmoothTransformation,
            )
        # pixmap = pixmap.scaled(QSize(20,20))
        self.icon.setPixmap(pixmap)
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.label)
        self.label.setMaximumWidth(30)
        self.label.setStyleSheet('''
        QLineEdit {
            color: #eb5f34;
            font-size: 14px;
        }''')
        self.js_func  = None
        self.setToolTip(tip)
        self.setStatusTip(tip)
        self.setLayout(self.layout)

    def connectWidget(self, js_func):
        '''connect JS functionality'''
        self.js_func = js_func

    def sliderAction(self, value):
        self.label.setText(f"{1+value:.0f}")
        if self.js_func:
            self.js_func()

    def setSliderByLabel(self):
        '''set slider value when return is pressed in the line edit.'''
        try: value = int(self.label.text())
        except ValueError: value = 0
        self.slider.setValue(value)
# oa.set('backdrop-filter', 'brightness(0.3) sepia(0.7)')
# oa.setBrightness(0.5)
class FileViewerAppearanceGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerAppearanceGroup, self).__init__(parent, "Appearance")
        VBox = QWidget()
        HBox = QWidget()
        Box3 = QWidget()
        VBox.setStyleSheet("background: rgba(29, 29, 29, 0.7); border: 0px;")
        HBox.setStyleSheet("background: rgba(29, 29, 29, 0.7); border: 0px;")
        Box3.setStyleSheet("background: rgba(29, 29, 29, 0.7); border: 0px;")
        HLayout = QVBoxLayout()
        HLayout.setContentsMargins(0, 0, 0, 0)
        VLayout = QVBoxLayout()
        VLayout.setContentsMargins(0, 0, 0, 0)
        Layout3 = QVBoxLayout()
        Layout3.setContentsMargins(0, 0, 0, 0)
        self.brightnessSlider = AppearanceSlider(
            icon="brightness.svg",
            tip="set background brightness",
        )
        self.blurRadiusSlider = AppearanceSlider(
            icon="blur.svg",
            tip="set background blur radius",
        )
        self.contrastSlider = AppearanceSlider(
            icon="contrast.svg",
            tip="set background contrast",
        )
        self.hueRotateSlider = AppearanceSlider(
            icon="hue.png",
            tip="set hue rotation",
        )
        self.grayScaleSlider = AppearanceSlider(
            icon="grayscale.png",
            tip="set gray scale amount",
        )
        self.saturateSlider = AppearanceSlider(
            icon="saturation.png",
            tip="set background saturation",
        )
        self.invertSlider = AppearanceSlider(
            icon="invert.svg",
            tip="invert background image color scheme",
        )
        self.opacitySlider = AppearanceSlider(
            icon="opacity.svg",
            tip="set background opacity",
        )
        self.sepiaSlider = AppearanceSlider(
            icon="sepia.png",
            tip="apply sepia filter",
        )
        self.backgroundImageBtn = self.initBtn(
            icon="background-image.png",
            tip="change background image"
        )
        # horizontal sliders box.
        VLayout.addWidget(self.brightnessSlider)
        VLayout.addWidget(self.blurRadiusSlider)
        VLayout.addWidget(self.contrastSlider)
        VLayout.addWidget(self.invertSlider)
        VBox.setLayout(VLayout)
        # vertical sliders box.
        HLayout.addWidget(self.hueRotateSlider)
        HLayout.addWidget(self.grayScaleSlider)
        HLayout.addWidget(self.opacitySlider)
        HLayout.addWidget(self.sepiaSlider)
        HBox.setLayout(HLayout)
        # 3rd vertical box.
        Layout3.addWidget(self.backgroundImageBtn, 0, Qt.AlignCenter)
        Layout3.addWidget(self.saturateSlider)
        Box3.setLayout(Layout3)

        self.layout.addStretch(1)
        self.layout.addWidget(VBox)
        self.layout.addWidget(HBox)
        self.layout.addWidget(Box3)
        self.layout.addStretch(1)

    def initBtn(self, icon: str, tip: str=""):
        btn = QToolButton(self)
        btn.setIconSize(QSize(30,30))
        path = os.path.join(
            "system/fileviewer", icon
        )
        btn.setIcon(FigD.Icon(path))
        # btn.setText("background\nimage")
        btn.setStyleSheet('''
        QToolButton {
            color: #fff;
            border: 0px;
            font-size: 12px;
            background: transparent;
        }
        QToolButton:hover {
            color: #292929;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34);
        }''')
        # btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btn.setToolTip(tip)
        btn.setStatusTip(tip)

        return btn

    def connectWidget(self, widget):
        self.widget = widget

# don't need class FileViewerMoveGroup(QWidget):
class FileViewerMenu(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerMenu, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # direct access to mime database and icon provider.
        self.mime_database = QMimeDatabase()
        self.icon_provider = QFileIconProvider()

        self.filegroup = FileViewerFileGroup()
        self.pathgroup = FileViewerPathGroup()
        self.editgroup = FileViewerEditGroup()
        self.viewgroup = FileViewerViewGroup()
        self.opengroup = FileViewerOpenGroup()
        self.sharegroup = FileViewerShareGroup()
        self.selectgroup = FileViewerSelectGroup()
        # self.appearancegroup = FileViewerAppearanceGroup()
        self.layout.addWidget(self.filegroup)
        self.layout.addWidget(self.addSeparator(10))
        self.layout.addWidget(self.pathgroup)
        self.layout.addWidget(self.addSeparator(10))
        self.layout.addWidget(self.editgroup)
        self.layout.addWidget(self.addSeparator(10))
        self.layout.addWidget(self.selectgroup)
        self.layout.addWidget(self.addSeparator(10))
        self.layout.addWidget(self.viewgroup)
        self.layout.addWidget(self.addSeparator(10))
        self.layout.addWidget(self.opengroup)
        self.layout.addWidget(self.addSeparator(10))
        self.layout.addWidget(self.sharegroup)

        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def addSeparator(self, width: Union[None, int]=None):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet('''background: #292929;''')
        sep.setLineWidth(1)
        # sep.setMaximumHeight(90)
        if width: 
            sep.setFixedWidth(width)
        return sep

    def connectWidget(self, widget):
        self.filegroup.connectWidget(widget)
        self.editgroup.connectWidget(widget)
        self.viewgroup.connectWidget(widget)
        self.pathgroup.connectWidget(widget)
        # self.opengroup.connectWidget(widget)
        self.selectgroup.connectWidget(widget)
        # self.appearancegroup.connectWidget(widget)

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
            font-family: 'Be Vietnam Pro', sans-serif;
            padding-top: 4px;
            padding-bottom: 4px;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1)); */
        }
        QToolButton:hover {
            color: #292929;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #147eb8, stop : 0.3 #69bfee, stop: 0.9 #338fc0);
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
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
            font-family: 'Be Vietnam Pro', sans-serif;
            padding-top: 4px;
            padding-bottom: 4px;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #147eb8, stop : 0.3 #69bfee, stop: 0.9 #338fc0);
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


class FileViewerShortcutBtn(QToolButton):
    '''File viewer shortcut button.'''
    def __init__(self, parent: Union[None, QWidget]=None, 
                 text: str="", icon: str="", path: str="",
                 size: Tuple[int, int]=(25,25),
                 tip: str=""):
        super(FileViewerShortcutBtn, self).__init__(parent)
        self.btnStyle = '''
        QToolButton {
            color: #fff;
            border: 0px;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            padding-top: 0px;
            padding-bottom: 0px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
        }
        QToolButton:hover {
            color: #292929;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #147eb8, stop : 0.3 #69bfee, stop: 0.9 #338fc0);
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }'''
        if text is None:
            text = Path(path).name
        self.setStyleSheet(self.btnStyle)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setIcon(FigD.Icon(
            os.path.join("system/fileviewer", icon)
        ))
        self.setIconSize(QSize(*size))
        self.setText(3*" "+text)
        self.setToolTip(tip)
        self.setStatusTip(tip)
        self.path = path
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
    def connectWidget(self, widget):
        self.widget = widget
        self.clicked.connect(self.onClick)

    def onClick(self):
        self.widget.open(self.path)


class FileViewerSideBar(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerSideBar, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        # shortcuts.
        self.shortcutBtns = []
        # bookmarks.
        self.bookmarkBtns = []
        home = os.path.expanduser("~")
        self.layout.setSpacing(5)
        self.recentBtn = self.initShortcutBtn(
            path=os.path.join(home, "Recent"),
            icon="recent.svg",
            tip=f"recently opened files",
            text="Recent",
        )
        self.homeBtn = self.initShortcutBtn(
            path=home,
            icon="home.svg",
            tip=f"open home folder ({home})",
            text="Home",
        )
        self.desktopBtn = self.initShortcutBtn(
            path=os.path.join(home, "Desktop"),
            icon="desktop.svg",
            tip="open desktop",
        )
        self.downloadsBtn = self.initShortcutBtn(
            path=os.path.join(home, "Downloads"),
            icon="downloads.svg",
            tip="open downloads",
        )
        self.documentsBtn = self.initShortcutBtn(
            path=os.path.join(home, "Documents"),
            icon="document.svg",
            tip="open documents folder",
        )
        self.musicBtn = self.initShortcutBtn(
            path=os.path.join(home, "Music"),
            icon="music.svg",
            tip="open music folder",
        )
        self.picturesBtn = self.initShortcutBtn(
            path=os.path.join(home, "Pictures"),
            icon="pictures.svg",
            tip="open pictures folder",
        )
        self.templatesBtn = self.initShortcutBtn(
            path=os.path.join(home, "Templates"),
            icon="templates.svg",
            tip="open templates folder",
        )
        # add buttons to layout.
        self.layout.addWidget(self.recentBtn)
        self.layout.addWidget(self.homeBtn)
        self.layout.addWidget(self.desktopBtn)
        self.layout.addWidget(self.documentsBtn)
        self.layout.addWidget(self.downloadsBtn)
        self.layout.addWidget(self.musicBtn)
        self.layout.addWidget(self.picturesBtn)
        self.layout.addWidget(self.templatesBtn)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def toggle(self):
        print("toggling folderbar visibility")
        if self.isVisible():
            self.hide()
        else: self.show()

    def addSeparator(self):
        pass

    def initShortcutBtn(self, path: str, 
                        icon: str, tip: str, 
                        text: Union[None, str]=None,
                        size: Tuple[int, int]=(25,25)):
        btn = FileViewerShortcutBtn(
            self, path=path, icon=icon,
            text=text, size=size, tip=tip,
        )
        self.shortcutBtns.append(btn)

        return btn
    # def initFavBtn(self, *args):
    #     pass
    # def initBookmarkBtn(self, path):
    #     name = Path(path).name
    #     btn = QToolButton(self)
    #     btn.setText(name)
    #     btn.setIcon(FigD.Icon("system/fileviewer/folder.svg"))
    #     btn.setToolTip(f"{path}")
    #     btn.setStyleSheet(self.btnStyle)
    #     btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
    #     btn.path = path
    #     self.bookmarkBtns.append(btn)

    #     return btn
    def connectWidget(self, widget):
        self.widget = widget
        for btn in self.shortcutBtns:
            btn.connectWidget(widget)


class FileViewerKeyPressSearch(QLineEdit):
    def __init__(self):
        super(FileViewerKeyPressSearch, self).__init__()
        self.setStyleSheet("""
        QLineEdit {
            color: #000;
            background: #fff;
        }""")
        self.h, self.w = 30, 100
        self.setFixedWidth(self.w)
        self.setFixedHeight(self.h)

    def showPanel(self, parent, w: int, h: int):
        self.setParent(parent)
        self.move(w-self.w, h-self.h)
        self.setFocus()
        self.show()

    def connectWidget(self, widget):
        self.widget = widget
        self.textChanged.connect(self.widget.searchByFileName)


class FileViewerWidget(QMainWindow):
    def __init__(self, parent: Union[None, QWidget]=None,
                 zoom_factor: float=1.35, **args):
        super(FileViewerWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.webview = FileViewerWebView()
        self.browser = self.webview
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
        self.showItemContextMenu = False
        self.loaded_file_items = []
        self.browsing_history = []
        self.selected_item = None
        self.hidden_visible = False
        # handle click events (using click handler)
        self.channel = QWebChannel()
        self.eventHandler = EventHandler(fileviewer=self)
        self.channel.registerObject("eventHandler", self.eventHandler)
        self.systemHandler = SystemHandler()
        self.systemHandler.connectChannel(self.channel)
        self.webview.page().setWebChannel(self.channel)
        
        self.folderbar = FileViewerFolderBar()
        self.folderbar.setFixedHeight(34)
        self.sidebar = FileViewerSideBar()
        self.sidebar.hide()
        # searchbar.
        self.searchbar = FileViewerSearchBar()
        # self.searchbar.setParent(self.webview)
        self.searchbar.setMinimumWidth(800)
        self.searchbar.setFixedHeight(34)
        # self.searchbar.setMaximumHeight(20)
        self.searchbar.move(0,0)
        # statusbar.
        self.statusbar = FileViewerStatus(self, self.webview)
        # clipboard access.
        self.clipboard = args.get("clipboard")
        
        # # shortcuts.
        self.SelectAll = QShortcut(QKeySequence.SelectAll, self)
        self.SelectAll.activated.connect(self.selectAll)
        # self.SelectAll.setEnabled(False)
    
        # add the dev tools button to the view group.
        self.menu.viewgroup.arrangeGroup.layout.insertWidget(1, self.webview.devToolsBtn)
        # self.menu.viewgroup.arrangeGroup.layout.insertWidget(1, self.webview.pyDevToolsBtn)
        # self.layout.addWidget(self.webview.devToolsBtn)
        # add widgets to layout.
        self.layout.insertWidget(0, self.webview.splitter, 0)
        self.layout.insertWidget(0, self.searchbar, 0, Qt.AlignCenter)
        self.layout.insertWidget(0, self.folderbar, 0)
        self.layout.insertWidget(0, self.menu, 0)
        # self.layout.addStretch(1)

        self.webview.splitter.insertWidget(0, self.sidebar)
        self.webview.splitter.setSizes([200, 600, 200])
        self.webview.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.keypress_search = FileViewerKeyPressSearch()
        self.keypress_search.connectWidget(self)
        self.keypress_search.hide()

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet('''background: transparent; border: 0px; color: #fff;''')        
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.webview.urlChanged.connect(self.onUrlChange)
        
        self.menu.connectWidget(self)
        self.folderbar.connectWidget(self)
        self.webview.connectWidget(self)
        self.sidebar.connectWidget(self)
        # connect Esc key shortcut to Esc handler.
        self.webview.Esc.setEnabled(False)
        self.EscKey = QShortcut(QKeySequence("Esc"), self)
        self.EscKey.activated.connect(self.EscHandler)

    def EscHandler(self):
        '''handle ESC key'''
        if self.webview.searchPanel.isVisible():
            self.webview.searchPanel.closePanel()
        elif self.keypress_search.isVisible():
            self.keypress_search.hide()
        else: self.clearSelection()

    def toggleHiddenFiles(self):
        if self.hidden_visible:
            self.hidden_visible = False
            self.webview.page().runJavaScript('hideHiddenFiles();')
        else:
            self.hidden_visible = True
            self.webview.page().runJavaScript('showHiddenFiles();')
        
    def searchByFileName(self):
        '''search by top level filenames in the currently opened folder only, and scroll it into view. (this search is case insensitive)'''
        query = self.keypress_search.text()
        selIndex = None
        for i, filename in enumerate(self.listed_filenames):
            filename = filename.lower()
            if filename.startswith(query): selIndex = i
        if selIndex is not None:
            id = self.listed_full_paths[selIndex]
            self.highlightItem(id)
            self.scrollToItem(id)

    def openParent(self):
        path = str(self.folder.parent)
        self.open(path)

    def callXdgOpen(self, path: str):
        '''call xdg-open for the appropriate mimetype.'''
        mimetype = self.mime_database.mimeTypeForFile(path).name()
        print(f"{path}: calling xdg-open for {mimetype} files")
        url = QUrl.fromLocalFile(path).toString()
        os.system(f"xdg-open {url}")

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

    def getIcon(self, path):
        name = self.icon_provider.icon(QFileInfo(path)).name()
        # print(name)
        # paths where mimetype icons may be found.
        icon_theme_devices_path = "/usr/share/icons/breeze/devices/48"
        icon_theme_places_path = "/usr/share/icons/breeze/places/64"
        icon_theme_mimes_path = "/usr/share/icons/breeze/mimetypes/32"
        Path = os.path.join(icon_theme_devices_path, name+".svg")
        if os.path.exists(Path): return Path
        Path = os.path.join(icon_theme_places_path, name+".svg")
        if os.path.exists(Path): return Path
        Path = os.path.join(icon_theme_mimes_path, name+".svg")
        if os.path.exists(Path): return Path

        return path

    def errorDialog(self, msg):
        self.error_dialog = QErrorMessage()
        self.error_dialog.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.error_dialog.showMessage(msg)
        # print(msg)
    def createDialogue(self, item_type="file"):
        if item_type == "folder": 
            path = self.createFolder()
            icon = "file:///usr/share/icons/breeze/places/64/inode-directory.svg"
            # file icon: file:///usr/share/icons/Humanity/mimes/48/text-plain.svg
        elif item_type == "file": 
            path = self.createFile()
            icon = "file:///usr/share/icons/breeze/mimetypes/32/text-plain.svg"
            # folder icon: file:///usr/share/icons/Humanity/places/64/inode-directory.svg
        name = Path(path).name
        self.webview.createItem(path, name, icon, hidden=False) 

    def renameDialog(self, path: Union[str, None]=None):
        '''rename file item, by creating an editable field.'''
        if path is None: path = self.selected_item
        if self.selected_item:
            self.webview.initiateRenameForId(self.selected_item)

    def renameItem(self, id: str, new_name: str):
        parent = Path(id).parent
        new_name = os.path.join(parent, new_name)
        print(f"renaming {id} to {new_name}")
        os.rename(id, new_name)

    def createFile(self):
        '''create a new empty file'''
        i = 1
        while True:
            path = os.path.join(self.folder, f"Untitled File {i}")
            if not os.path.exists(path): break
            else: i += 1
        print(f"\x1b[32;1mcreated new file: {path}\x1b[0m")
        open(path, "w")

        return path

    def createFolder(self):
        '''create a new empty folder'''
        i = 1
        while True:
            try:
                path = os.  path.join(
                    self.folder, 
                    f"Untitled Folder {i}"
                )
                os.mkdir(path)
                break
            except FileExistsError:
                i += 1
        print(f"\x1b[32;1mcreated new folder: {path}\x1b[0m")

        return path

    def open(self, folder: str="~"):
        '''open a file/folder location.'''
        try:
            print(self.dash_window)
            i = self.dash_window.tabs.currentIndex()
            self.dash_window.tabs.setTabText(i, folder)
        except AttributeError:
            print("FileViewerWidget: \x1b[31;1mnot connected to a DashWindow\x1b[0m")
        # expand user.
        folder = os.path.expanduser(folder) 
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
            print("\x1b[31;1mfileviewer.open\x1b[0m", e)
            self.errorDialog(str(e))
            return
        self.folder = Path(folder)
        self.folderbar.setPath(folder)  
        self.browsing_history.append(folder)
        listed, full_paths, hidden_flag_list = self.listFiles(folder)
        # populate content for searching.
        self.listed_filenames = listed
        self.listed_full_paths = full_paths
        self.listed_hidden_files = hidden_flag_list
        file_count = 0
        folder_count = 0 
        hidden_count = 0
        for path in full_paths:
            if os.path.isdir(path):
                folder_count += 1
            elif os.path.isfile(path):
                file_count += 1
        for value in hidden_flag_list:
            if value == False: continue
            hidden_count += 1
        # get number of items, folder, files and hidden
        self.statusbar.updateBreakdown(
            files=file_count,
            items=len(self.listed_filenames),
            hidden=hidden_count,
            folders=folder_count,
        )

        for path in full_paths:
            self.loaded_file_items.append({
                "path": path, 
                "mimetype": self.mime_database.mimeTypeForFile(path).name(),
                "info": QFileInfo(path),
            }) 
        humanity_to_breeze_map = {
            "video": "video-mp4",
        }  
        icons = []
        for path in full_paths:
            iconPath = humanity_to_breeze_map.get(
                self.icon_provider.icon(
                    QFileInfo(path)
                ).name(),
                self.icon_provider.icon(
                    QFileInfo(path)
                ).name()
            ) 
            icons.append((
                iconPath,
                self.mime_database.mimeTypeForFile(path).name(),
                path
            ))
        # icons = [
        #     (iconPath, 
        #      self.mime_database.mimeTypeForFile(path).name(),
        #      path) for path in full_paths
        # ]
        icon_theme_devices_path = "/usr/share/icons/breeze/devices/48"
        icon_theme_places_path = "/usr/share/icons/breeze/places/64"
        icon_theme_mimes_path = "/usr/share/icons/breeze/mimetypes/32"
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
                path = "/usr/share/icons/breeze/mimetypes/32/text-plain.svg"
                icon_paths.append(QUrl.fromLocalFile(path).toString())     
        # def chunk_string(string, k=12):
        #     result = []
        #     for i in range(0, len(string), k):
        #         result.append(string[i:i+k])

        #     return result
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
        self.params.update(self.systemHandler.js_sources)
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
        icon = self.getIcon(item)
        mimetype = self.mime_database.mimeTypeForFile(item).name()
        self.menu.pathgroup.updateExt(file_ext)
        self.menu.opengroup.updateMimeBtn(
            mimetype=mimetype, 
            icon=icon, path=item
        )
        file_info = QFileInfo(item)
        name = file_info.fileName()
        if file_info.isDir():
            items = len(os.listdir(item)) 
        else: items = 0
        size = h_format_mem(file_info.size())
        # .strftime("%b, %m %d %Y %H:%M:%S")
        group = file_info.group()
        owner = file_info.owner()
        shortcut = file_info.isShortcut()
        symbolic = file_info.isSymbolicLink()
        r_permission = file_info.isReadable()
        w_permission = file_info.isWritable()
        x_permission = file_info.isExecutable()
        permissions = "["
        if r_permission:
            permissions += "R"
        if w_permission:
            permissions += "W"
        if x_permission:
            permissions += "X"
        permissions += "]"

        last_read = file_info.lastRead().toPyDateTime()
        last_modified = file_info.lastModified().toPyDateTime()
        meta_change_time = file_info.metadataChangeTime().toPyDateTime()
        # print(last_read, last_modified, group, owner, 
        #       meta_change_time, permissions)
        self.statusbar.updateSelected(
            shortcut=shortcut, symbolic=symbolic,
            items=items, name=name, icon=icon, 
            size=size, permissions=permissions,
            meta_change_time=meta_change_time,
            last_read=last_read, owner=owner,
            last_modified=last_modified,
            group=group,
        )

    def keyPressEvent(self, event):
        # print(event.key()) # print("opened keypress search")
        try:
            letter = chr(event.key())
            self.keypress_search.showPanel(
                parent=self, 
                w=self.width(),
                h=self.height(),
            )
            self.keypress_search.setText(letter.lower())
            # print("changed focus")
        except (TypeError, ValueError) as e:
            print("\x1b[31;1mfileviewer.keyPressEvent\x1b[0m", e)
            # fail silently.
        super(FileViewerWidget, self).keyPressEvent(event)

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

    def reload(self):
        '''refresh the webview'''
        self.webview.reload()

    def scrollToItem(self, id: str):
        '''scroll item into view by id.'''
        code = f"document.getElementById('{id}').scrollIntoView()"
        self.webview.page().runJavaScript(code)

    def invertSelection(self):
        '''invert selected items.'''
        self.webview.page().runJavaScript('invertSelectedItems();')

    def highlightItem(self, id: str):
        '''select a specific item by id'''
        self.clearSelection()
        self.webview.page().runJavaScript(f"selectItemById('{id}')")

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

    def connectWindow(self, window):
        print("FileViewerWidget: \x1b[32;1mconnected to DashWindow\x1b[0m")
        self.dash_window = window


def test_fileviewer():
    import sys
    import platform
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    fileviewer = FileViewerWidget(
        clipboard=app.clipboard(),
        background="/home/atharva/Pictures/Wallpapers/3339083.jpg",
        font_color="#fff",
    )
    fileviewer.setStyleSheet("background: tranparent; border: 0px;")
    QFontDatabase.addApplicationFont(
        FigD.font("BeVietnamPro-Regular.ttf")
    )
    fileviewer.open("~")
    fileviewer.setGeometry(200, 200, 800, 600)
    fileviewer.setWindowFlags(Qt.WindowStaysOnTopHint)
    if platform.system() == "Linux":
        fileviewer.setWindowIcon(FigD.Icon("system/fileviewer/logo.svg"))
        app.setWindowIcon(FigD.Icon("system/fileviewer/logo.svg"))
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
# https://towardsdatascience.com/a-friendly-introduction-to-siamese-networks-85ab17522942#:~:text=A%20Siamese%20Neural%20Network%20is%20a%20class%20of%20neural%20network%20architectures%20that%20contain
# https://towardsdatascience.com/case-study-2-an-unsupervised-neural-attention-model-for-aspect-extraction-1c2c97b1380a#:~:text=All%20reviews-,are,-available%20as%20a