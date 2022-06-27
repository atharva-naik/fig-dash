print("fig_dash::ui::js::fileviewer")
import jinja2

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
/* *::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}
*::-webkit-scrollbar-track:hover {
    background: rgba(29, 29, 29, 0.4);
}    
*::-webkit-scrollbar-track {
    background-color: rgba(235, 235, 235, 0.8);
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
    background: rgba(235, 235, 235, 0.1);
} */

*::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}
*::-webkit-scrollbar-track {
    background-color: #292929;
}
*::-webkit-scrollbar-thumb {
    background: {{ CSS_GRAD }};
}
*::-webkit-scrollbar-corner {
    background: rgba(235, 235, 235, 0.5);
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

main .boxes.green div.selected img{
    filter: blur(1px);
}
main .boxes.green div.selected span{
    color: #292929;
    border-radius: 2px;
    border: 1px solid #0a4c70;
    background: rgba(105, 191, 238, 150);
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
var fileViewerMimeTypes = {{ FILEVIEWER_MIMETYPES }};
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
    <img id="thumbnail_${fileViewerPaths[i]}" data-mimetype="${fileViewerMimeTypes[i]}" class="icon" src="${fileViewerIcons[i]}" width="40px;"/>
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
            try {
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    var eventHandler = channel.objects.eventHandler;
                    eventHandler.sendOpenRequest(file_item_id);
                });
            }
            catch (err) {
                console.log(err);
                console.log(file_item_id);
                window.location.href = `/ui/system/fileviewer?path=${file_item_id}`;
            }
        })
        divElement.addEventListener('contextmenu', function(event) {
            // event.preventDefault(); // disable regular contextmenu.
            // event.preventDefault();
            // var file_item = this;
            /* new QWebChannel(qt.webChannelTransport, function(channel) {
                var eventHandler = channel.objects.eventHandler;
                eventHandler.triggerContextMenu(file_item.id);
            });
            console.log(event); */
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


        <title>{{ FOLDER }}</title>

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