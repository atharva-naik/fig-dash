#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import Union
from pathlib import Path
# fig-dash imports.
from fig_dash import FigD
from fig_dash.ui.browser import DebugWebView
# PyQt5 imports
from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QToolBar, QToolButton, QSizePolicy, QAction, QActionGroup, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
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

::-webkit-scrollbar-thumb {
    background: #afafaf;
    border-radius: 0.2em;
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
    background: #ebedf7;
    font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji;
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
}

main .boxes.green,
main .boxes.blue {
    margin-bottom: 3em;
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
    height: 3em;
    width: 3em;
    margin: 0.2em;
    background: rgba(66, 68, 90, 0.075);
    border: 2px solid transparent;
    border-radius: 0.15em;
    cursor: pointer;
}

main .boxes.green div.selected {
    background: hsl(100, 80%, 65%);
    border: 2px solid rgba(0, 0, 0, 0.075);
}

main .boxes.blue div.selected {
    background: hsl(150, 80%, 65%);
    border: 2px solid rgba(0, 0, 0, 0.075);
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
{{ FILEVIEWER_JS }}
var fileViewerItemNames = {{}} 
[
    ['.boxes.green', {{ NUM_ITEMS }}]
].forEach(([selector, items]) => {
    const container = document.querySelector(selector);
    console.error(items);
    for (let i = 0; i < items; i++) {
        var divElement = document.createElement('div');
        // console.error(divElement)
        container.appendChild(divElement);
    }
});

const selection = new SelectionArea({
    selectables: ['.boxes > div'],
    boundaries: ['.boxes']
}).on('start', ({store, event}) => {
    if (!event.ctrlKey && !event.metaKey) {

        for (const el of store.stored) {
            el.classList.remove('selected');
        }

        selection.clearSelection();
    }
}).on('move', ({store: {changed: {added, removed}}}) => {
    for (const el of added) {
        el.classList.add('selected');
    }

    for (const el of removed) {
        el.classList.remove('selected');
    }
});'''

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
        <link rel="icon" href="favicon.png"/>
        <link rel="fluid-icon" href="favicon.png"/>
        <link rel="apple-touch-icon" href="favicon.png"/>
        <link href="favicon.png" rel="icon"/>
        <link href="favicon.png" rel="apple-touch-icon"/>

        <!-- CSS / JS -->
        <style>{{ FILEVIEWER_CSS }}</style>
    </head>

    <body>
        <main>
            <section class="demo">
                <section class="boxes green"></section>
            </section>
        </main>

        <script type="module">{{ FILEVIEWER_MJS }}</script>
    </body>
</html>''')
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
            layout.addWidget(btn, 0, Qt.AlignCenter)
        layout.addStretch(1)
        btnGroup.setLayout(layout)

        return btnGroup

    def initBtn(self, **args):
        btn = QToolButton(self)
        tip = args.get("tip", "a tip")
        icon = args.get("icon")
        icon = os.path.join("system/fileviewer", icon)
        size = args.get("size", (23,23))
        btn.setIcon(FigD.Icon(icon))
        btn.setIconSize(QSize(*size))
        btn.setToolTip(tip)
        btn.setStyleSheet('''
        QToolButton {
            color: #fff;
            border: 0px;
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
            icon="connect_to_server.png",
            size=(45,45),
            tip="connect to a server",
        )
        self.layout.addWidget(self.creationWidget)
        self.layout.addWidget(self.connectToServerBtn)


class FileViewerPathGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerPathGroup, self).__init__(parent, "Path")
        # just to convert to VBox Layout.
        self.pathWidget = QWidget()
        self.pathLayout = QVBoxLayout()
        self.pathLayout.setContentsMargins(0, 0, 0, 0)
        self.pathLayout.setSpacing(0)
        self.pathWidget.setLayout(self.pathLayout)
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
        # move to view
        # self.hideExtBtn =  self.initBtn(
        #     icon="hide_extension.svg",
        #     size=(20,20)
        # )
        self.pathLayout.addWidget(self.copyPathBtn)
        self.pathLayout.addWidget(self.copyNameBtn)
        self.pathLayout.addWidget(self.copyUrlBtn)
        self.pathLayout.addStretch(1)
        self.layout.addStretch(1)
        self.layout.addWidget(self.pathWidget)
        self.layout.addStretch(1)


class FileViewerEditGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerEditGroup, self).__init__(parent, "Edit")
        self.editWidget = QWidget() 
        self.editLayout = QVBoxLayout()
        self.editLayout.setContentsMargins(0, 0, 0, 0)
        # undo, redo, rename
        self.renameGroup = self.initBtnGroup([
            {"icon": "undo.png", "size": (23,23), "tip": "undo rename"},
            {"icon": "rename.svg", "size": (23,23), "tip": "rename file/folder"},
            {"icon": "redo.png", "size": (23,23) , "tip": "redo rename"},
        ])
        # cut, copy, paste
        self.moveGroup = self.initBtnGroup([
            {"icon": "cut.png", "size": (23,23), "tip": "cut selected item"},
            {"icon": "copy.svg", "size": (23,23), "tip": "copy selected items"},
            {"icon": "paste.png", "size": (23,23), "tip": "paste selected items from the clipboard"},
        ])
        # make link, release link, move to trash
        self.linkGroup = self.initBtnGroup([
            {"icon": "link.svg", "size": (23,23)},
            {"icon": "unlink.svg", "size": (23,23), "tip": "move selected item(s) to trash"},
            {"icon": "trash.svg", "size": (23,23), "tip": "move selected item(s) to trash"},
        ])
        self.editLayout.addWidget(self.renameGroup)
        self.editLayout.addWidget(self.moveGroup)
        self.editLayout.addWidget(self.linkGroup)
        self.editLayout.addStretch(1)
        self.editWidget.setLayout(self.editLayout)
        self.layout.addStretch(1)
        self.layout.addWidget(self.editWidget)
        self.layout.addStretch(1)    


class FileViewerViewGroup(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerViewGroup, self).__init__(parent, "View")
        self.viewWidget = QWidget() 
        self.viewLayout = QVBoxLayout()
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.layoutGroup = self.initBtnGroup(
            {"icon": "tileview.svg", "size": (25,25), "tip": "tile view"},
            {"icon": "listview.svg", "size": (25,25), "tip": "list view"},
            {"icon": "treeview.svg", "size": (25,25), "tip": "tree view"},
        )        
        self.viewLayout.addWidget(self.linkGroup)
        self.viewLayout.addStretch(1)
        self.viewWidget.setLayout(self.viewLayout)
        self.layout.addStretch(1)
        self.layout.addWidget(self.viewWidget)
        self.layout.addStretch(1)    
# class FileViewerOpenGroup(QWidget):
# class FileViewerMoveGroup(QWidget):
# class FileViewerPropGroup(QWidget):
# class FileViewerShareGroup(QWidget):
# class FileViewerFilterGroup(QWidget):
# class FileViewerUtilsGroup(QWidget): compression, file conversion (for images, videos,document formats etc.)
# class FileViewerSelectGroup(QWidget):
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
        self.layout.addWidget(self.filegroup)
        self.layout.addWidget(self.pathgroup)
        self.layout.addWidget(self.editgroup)
        self.layout.addStretch(1)
        self.setLayout(self.layout)


class FileViewerWidget(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None,
                 zoom_factor: float=1.35):
        super(FileViewerWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.webview = DebugWebView()
        self.zoom_factor = zoom_factor
        self.menu = FileViewerMenu()
        self.menu.setMaximumHeight(110)
        self.layout.addWidget(self.menu)
        self.layout.addWidget(self.webview.devToolsBtn)
        self.layout.addWidget(self.webview.splitter)
        self.setLayout(self.layout)
        self.webview.urlChanged.connect(self.onUrlChange)
        self.setStyleSheet('''background: #292929; color: #fff;''')

    def build(self, folder: str=os.path.expanduser("~")):
        self.folder = Path(folder)
        listed = os.listdir(self.folder)
        self.params = {
            "FOLDER": self.folder.name,
            "FILEVIEWER_JS": ViSelectJS,
            "FILEVIEWER_MJS": FileViewerMJS,
            "FILEVIEWER_CSS": FileViewerStyle,
            "PARENT_FOLDER": self.folder.parent.name,
            "NUM_ITEMS": len(listed),
        }
        self.viewer_html = jinja2.Template(
            FileViewerHtml.render(**self.params)
        ).render(**self.params)
        render_url = FigD.createTempUrl(self.viewer_html)
        self.webview.load(render_url)

    def onUrlChange(self):
        self.webview.setZoomFactor(self.zoom_factor)
        self.webview.loadFinished.connect(self.webview.loadDevTools)

    def saveScreenshot(self, path):
        with open(path, "w") as f:
            f.write(self.viewer_html)


def test_fileviewer():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    fileviewer = FileViewerWidget()
    fileviewer.build()
    fileviewer.saveScreenshot("fileviewer.html")
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