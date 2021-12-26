#!/usr/bin/env python3
# -*- coding: utf-8 -*-
QuillEmojiJS = r'''
!function(e,o){"object"==typeof exports&&"object"==typeof module?module.exports=o(require("quill")):"function"==typeof define&&define.amd?define(["quill"],o):"object"==typeof exports?exports.QuillEmoji=o(require("quill")):e.QuillEmoji=o(e.Quill)}(window,function(a){return function(a){var r={};function c(e){if(r[e])return r[e].exports;var o=r[e]={i:e,l:!1,exports:{}};return a[e].call(o.exports,o,o.exports,c),o.l=!0,o.exports}return c.m=a,c.c=r,c.d=function(e,o,a){c.o(e,o)||Object.defineProperty(e,o,{enumerable:!0,get:a})},c.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},c.t=function(o,e){if(1&e&&(o=c(o)),8&e)return o;if(4&e&&"object"==typeof o&&o&&o.__esModule)return o;var a=Object.create(null);if(c.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:o}),2&e&&"string"!=typeof o)for(var r in o)c.d(a,r,function(e){return o[e]}.bind(null,r));return a},c.n=function(e){var o=e&&e.__esModule?function(){return e.default}:function(){return e};return c.d(o,"a",o),o},c.o=function(e,o){return Object.prototype.hasOwnProperty.call(e,o)},c.p="",c(c.s=3)}([function(e,o){e.exports=a},function(e,o,a){var r;r=function(){return function(a){var r={};function c(e){if(r[e])return r[e].exports;var o=r[e]={i:e,l:!1,exports:{}};return a[e].call(o.exports,o,o.exports,c),o.l=!0,o.exports}return c.m=a,c.c=r,c.d=function(e,o,a){c.o(e,o)||Object.defineProperty(e,o,{enumerable:!0,get:a})},c.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},c.t=function(o,e){if(1&e&&(o=c(o)),8&e)return o;if(4&e&&"object"==typeof o&&o&&o.__esModule)return o;var a=Object.create(null);if(c.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:o}),2&e&&"string"!=typeof o)for(var r in o)c.d(a,r,function(e){return o[e]}.bind(null,r));return a},c.n=function(e){var o=e&&e.__esModule?function(){return e.default}:function(){return e};return c.d(o,"a",o),o},c.o=function(e,o){return Object.prototype.hasOwnProperty.call(e,o)},c.p="",c(c.s="./src/index.js")}({"./src/bitap/bitap_matched_indices.js":function(e,o){e.exports=function(){for(var e=0<arguments.length&&void 0!==arguments[0]?arguments[0]:[],o=1<arguments.length&&void 0!==arguments[1]?arguments[1]:1,a=[],r=-1,c=-1,n=0,d=e.length;n<d;n+=1){var i=e[n];i&&-1===r?r=n:i||-1===r||(o<=(c=n-1)-r+1&&a.push([r,c]),r=-1)}return e[n-1]&&o<=n-r&&a.push([r,n-1]),a}},"./src/bitap/bitap_pattern_alphabet.js":function(e,o){e.exports=function(e){for(var o={},a=e.length,r=0;r<a;r+=1)o[e.charAt(r)]=0;for(var c=0;c<a;c+=1)o[e.charAt(c)]|=1<<a-c-1;return o}},"./src/bitap/bitap_regex_search.js":function(e,o){var _=/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g;e.exports=function(e,o){var a=2<arguments.length&&void 0!==arguments[2]?arguments[2]:/ +/g,r=new RegExp(o.replace(_,"\\$&").replace(a,"|")),c=e.match(r),n=!!c,d=[];if(n)for(var i=0,m=c.length;i<m;i+=1){var t=c[i];d.push([e.indexOf(t),t.length-1])}return{score:n?.5:1,isMatch:n,matchedIndices:d}}},"./src/bitap/bitap_score.js":function(e,o){e.exports=function(e,o){var a=o.errors,r=void 0===a?0:a,c=o.currentLocation,n=void 0===c?0:c,d=o.expectedLocation,i=void 0===d?0:d,m=o.distance,t=void 0===m?100:m,_=r/e.length,l=Math.abs(i-n);return t?_+l/t:l?1:_}},"./src/bitap/bitap_search.js":function(e,o,a){var I=a("./src/bitap/bitap_score.js"),B=a("./src/bitap/bitap_matched_indices.js");e.exports=function(e,o,a,r){for(var c=r.location,n=void 0===c?0:c,d=r.distance,i=void 0===d?100:d,m=r.threshold,t=void 0===m?.6:m,_=r.findAllMatches,l=void 0!==_&&_,s=r.minMatchCharLength,f=void 0===s?1:s,g=n,u=e.length,h=t,y=e.indexOf(o,g),j=o.length,p=[],b=0;b<u;b+=1)p[b]=0;if(-1!==y){var v=I(o,{errors:0,currentLocation:y,expectedLocation:g,distance:i});if(h=Math.min(v,h),-1!==(y=e.lastIndexOf(o,g+j))){var k=I(o,{errors:0,currentLocation:y,expectedLocation:g,distance:i});h=Math.min(k,h)}}y=-1;for(var w=[],x=1,S=j+u,q=1<<j-1,E=0;E<j;E+=1){for(var C=0,L=S;C<L;){I(o,{errors:E,currentLocation:g+L,expectedLocation:g,distance:i})<=h?C=L:S=L,L=Math.floor((S-C)/2+C)}S=L;var O=Math.max(1,g-L+1),M=l?u:Math.min(g+L,u)+j,z=Array(M+2);z[M+1]=(1<<E)-1;for(var T=M;O<=T;T-=1){var P=T-1,A=a[e.charAt(P)];if(A&&(p[P]=1),z[T]=(z[T+1]<<1|1)&A,0!==E&&(z[T]|=(w[T+1]|w[T])<<1|1|w[T+1]),z[T]&q&&(x=I(o,{errors:E,currentLocation:P,expectedLocation:g,distance:i}))<=h){if(h=x,(y=P)<=g)break;O=Math.max(1,2*g-y)}}if(h<I(o,{errors:E+1,currentLocation:g,expectedLocation:g,distance:i}))break;w=z}return{isMatch:0<=y,score:0===x?.001:x,matchedIndices:B(p,f)}}},"./src/bitap/index.js":function(e,o,a){function r(e,o){for(var a=0;a<o.length;a++){var r=o[a];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}var _=a("./src/bitap/bitap_regex_search.js"),l=a("./src/bitap/bitap_search.js"),p=a("./src/bitap/bitap_pattern_alphabet.js"),c=function(){function j(e,o){var a=o.location,r=void 0===a?0:a,c=o.distance,n=void 0===c?100:c,d=o.threshold,i=void 0===d?.6:d,m=o.maxPatternLength,t=void 0===m?32:m,_=o.isCaseSensitive,l=void 0!==_&&_,s=o.tokenSeparator,f=void 0===s?/ +/g:s,g=o.findAllMatches,u=void 0!==g&&g,h=o.minMatchCharLength,y=void 0===h?1:h;!function(e,o){if(!(e instanceof o))throw new TypeError("Cannot call a class as a function")}(this,j),this.options={location:r,distance:n,threshold:i,maxPatternLength:t,isCaseSensitive:l,tokenSeparator:f,findAllMatches:u,minMatchCharLength:y},this.pattern=this.options.isCaseSensitive?e:e.toLowerCase(),this.pattern.length<=t&&(this.patternAlphabet=p(this.pattern))}var e,o,a;return e=j,(o=[{key:"search",value:function(e){if(this.options.isCaseSensitive||(e=e.toLowerCase()),this.pattern===e)return{isMatch:!0,score:0,matchedIndices:[[0,e.length-1]]};var o=this.options,a=o.maxPatternLength,r=o.tokenSeparator;if(this.pattern.length>a)return _(e,this.pattern,r);var c=this.options,n=c.location,d=c.distance,i=c.threshold,m=c.findAllMatches,t=c.minMatchCharLength;return l(e,this.pattern,this.patternAlphabet,{location:n,distance:d,threshold:i,findAllMatches:m,minMatchCharLength:t})}}])&&r(e.prototype,o),a&&r(e,a),j}();e.exports=c},"./src/helpers/deep_value.js":function(e,o,a){var _=a("./src/helpers/is_array.js");e.exports=function(e,o){return function e(o,a,r){if(a){var c=a.indexOf("."),n=a,d=null;-1!==c&&(n=a.slice(0,c),d=a.slice(c+1));var i=o[n];if(null!=i)if(d||"string"!=typeof i&&"number"!=typeof i)if(_(i))for(var m=0,t=i.length;m<t;m+=1)e(i[m],d,r);else d&&e(i,d,r);else r.push(i.toString())}else r.push(o);return r}(e,o,[])}},"./src/helpers/is_array.js":function(e,o){e.exports=function(e){return Array.isArray?Array.isArray(e):"[object Array]"===Object.prototype.toString.call(e)}},"./src/index.js":function(e,o,a){function _(e){return(_="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function r(e,o){for(var a=0;a<o.length;a++){var r=o[a];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}var n=a("./src/bitap/index.js"),R=a("./src/helpers/deep_value.js"),I=a("./src/helpers/is_array.js"),c=function(){function H(e,o){var a=o.location,r=void 0===a?0:a,c=o.distance,n=void 0===c?100:c,d=o.threshold,i=void 0===d?.6:d,m=o.maxPatternLength,t=void 0===m?32:m,_=o.caseSensitive,l=void 0!==_&&_,s=o.tokenSeparator,f=void 0===s?/ +/g:s,g=o.findAllMatches,u=void 0!==g&&g,h=o.minMatchCharLength,y=void 0===h?1:h,j=o.id,p=void 0===j?null:j,b=o.keys,v=void 0===b?[]:b,k=o.shouldSort,w=void 0===k||k,x=o.getFn,S=void 0===x?R:x,q=o.sortFn,E=void 0===q?function(e,o){return e.score-o.score}:q,C=o.tokenize,L=void 0!==C&&C,O=o.matchAllTokens,M=void 0!==O&&O,z=o.includeMatches,T=void 0!==z&&z,P=o.includeScore,A=void 0!==P&&P,I=o.verbose,B=void 0!==I&&I;!function(e,o){if(!(e instanceof o))throw new TypeError("Cannot call a class as a function")}(this,H),this.options={location:r,distance:n,threshold:i,maxPatternLength:t,isCaseSensitive:l,tokenSeparator:f,findAllMatches:u,minMatchCharLength:y,id:p,keys:v,includeMatches:T,includeScore:A,shouldSort:w,getFn:S,sortFn:E,verbose:B,tokenize:L,matchAllTokens:M},this.setCollection(e)}var e,o,a;return e=H,(o=[{key:"setCollection",value:function(e){return this.list=e}},{key:"search",value:function(e){var o=1<arguments.length&&void 0!==arguments[1]?arguments[1]:{limit:!1};this._log('---------\nSearch pattern: "'.concat(e,'"'));var a=this._prepareSearchers(e),r=a.tokenSearchers,c=a.fullSearcher,n=this._search(r,c),d=n.weights,i=n.results;return this._computeScore(d,i),this.options.shouldSort&&this._sort(i),o.limit&&"number"==typeof o.limit&&(i=i.slice(0,o.limit)),this._format(i)}},{key:"_prepareSearchers",value:function(){var e=0<arguments.length&&void 0!==arguments[0]?arguments[0]:"",o=[];if(this.options.tokenize)for(var a=e.split(this.options.tokenSeparator),r=0,c=a.length;r<c;r+=1)o.push(new n(a[r],this.options));return{tokenSearchers:o,fullSearcher:new n(e,this.options)}}},{key:"_search",value:function(){var e=0<arguments.length&&void 0!==arguments[0]?arguments[0]:[],o=1<arguments.length?arguments[1]:void 0,a=this.list,r={},c=[];if("string"==typeof a[0]){for(var n=0,d=a.length;n<d;n+=1)this._analyze({key:"",value:a[n],record:n,index:n},{resultMap:r,results:c,tokenSearchers:e,fullSearcher:o});return{weights:null,results:c}}for(var i={},m=0,t=a.length;m<t;m+=1)for(var _=a[m],l=0,s=this.options.keys.length;l<s;l+=1){var f=this.options.keys[l];if("string"!=typeof f){if(i[f.name]={weight:1-f.weight||1},f.weight<=0||1<f.weight)throw new Error("Key weight has to be > 0 and <= 1");f=f.name}else i[f]={weight:1};this._analyze({key:f,value:this.options.getFn(_,f),record:_,index:m},{resultMap:r,results:c,tokenSearchers:e,fullSearcher:o})}return{weights:i,results:c}}},{key:"_analyze",value:function(e,o){var a=e.key,r=e.arrayIndex,c=void 0===r?-1:r,n=e.value,d=e.record,i=e.index,m=o.tokenSearchers,t=void 0===m?[]:m,_=o.fullSearcher,l=void 0===_?[]:_,s=o.resultMap,f=void 0===s?{}:s,g=o.results,u=void 0===g?[]:g;if(null!=n){var h=!1,y=-1,j=0;if("string"==typeof n){this._log("\nKey: ".concat(""===a?"-":a));var p=l.search(n);if(this._log('Full text: "'.concat(n,'", score: ').concat(p.score)),this.options.tokenize){for(var b=n.split(this.options.tokenSeparator),v=[],k=0;k<t.length;k+=1){var w=t[k];this._log('\nPattern: "'.concat(w.pattern,'"'));for(var x=!1,S=0;S<b.length;S+=1){var q=b[S],E=w.search(q),C={};E.isMatch?(C[q]=E.score,x=h=!0,v.push(E.score)):(C[q]=1,this.options.matchAllTokens||v.push(1)),this._log('Token: "'.concat(q,'", score: ').concat(C[q]))}x&&(j+=1)}y=v[0];for(var L=v.length,O=1;O<L;O+=1)y+=v[O];y/=L,this._log("Token score average:",y)}var M=p.score;-1<y&&(M=(M+y)/2),this._log("Score average:",M);var z=!this.options.tokenize||!this.options.matchAllTokens||j>=t.length;if(this._log("\nCheck Matches: ".concat(z)),(h||p.isMatch)&&z){var T=f[i];T?T.output.push({key:a,arrayIndex:c,value:n,score:M,matchedIndices:p.matchedIndices}):(f[i]={item:d,output:[{key:a,arrayIndex:c,value:n,score:M,matchedIndices:p.matchedIndices}]},u.push(f[i]))}}else if(I(n))for(var P=0,A=n.length;P<A;P+=1)this._analyze({key:a,arrayIndex:P,value:n[P],record:d,index:i},{resultMap:f,results:u,tokenSearchers:t,fullSearcher:l})}}},{key:"_computeScore",value:function(e,o){this._log("\n\nComputing score:\n");for(var a=0,r=o.length;a<r;a+=1){for(var c=o[a].output,n=c.length,d=1,i=1,m=0;m<n;m+=1){var t=e?e[c[m].key].weight:1,_=(1===t?c[m].score:c[m].score||.001)*t;1!==t?i=Math.min(i,_):d*=c[m].nScore=_}o[a].score=1===i?d:i,this._log(o[a])}}},{key:"_sort",value:function(e){this._log("\n\nSorting...."),e.sort(this.options.sortFn)}},{key:"_format",value:function(e){var o=[];if(this.options.verbose){var a=[];this._log("\n\nOutput:\n\n",JSON.stringify(e,function(e,o){if("object"===_(o)&&null!==o){if(-1!==a.indexOf(o))return;a.push(o)}return o})),a=null}var r=[];this.options.includeMatches&&r.push(function(e,o){var a=e.output;o.matches=[];for(var r=0,c=a.length;r<c;r+=1){var n=a[r];if(0!==n.matchedIndices.length){var d={indices:n.matchedIndices,value:n.value};n.key&&(d.key=n.key),n.hasOwnProperty("arrayIndex")&&-1<n.arrayIndex&&(d.arrayIndex=n.arrayIndex),o.matches.push(d)}}}),this.options.includeScore&&r.push(function(e,o){o.score=e.score});for(var c=0,n=e.length;c<n;c+=1){var d=e[c];if(this.options.id&&(d.item=this.options.getFn(d.item,this.options.id)[0]),r.length){for(var i={item:d.item},m=0,t=r.length;m<t;m+=1)r[m](d,i);o.push(i)}else o.push(d.item)}return o}},{key:"_log",value:function(){var e;this.options.verbose&&(e=console).log.apply(e,arguments)}}])&&r(e.prototype,o),a&&r(e,a),H}();e.exports=c}})},e.exports=r()},function(e,o,a){},function(e,o,a){"use strict";a.r(o);var r=a(0),m=a.n(r),c=[{name:"100",unicode:"1f4af",shortname:":100:",code_decimal:"&#128175;",category:"s",emoji_order:"2119"},{name:"1234",unicode:"1f522",shortname:":1234:",code_decimal:"&#128290;",category:"s",emoji_order:"2122"},{name:"grinning",unicode:"1f600",shortname:":grinning:",code_decimal:"&#128512;",category:"p",emoji_order:"1"},{name:"grin",unicode:"1f601",shortname:":grin:",code_decimal:"&#128513;",category:"p",emoji_order:"2"},{name:"joy",unicode:"1f602",shortname:":joy:",code_decimal:"&#128514;",category:"p",emoji_order:"3"},{name:"smiley",unicode:"1f603",shortname:":smiley:",code_decimal:"&#128515;",category:"p",emoji_order:"5"},{name:"smile",unicode:"1f604",shortname:":smile:",code_decimal:"&#128516;",category:"p",emoji_order:"6"},{name:"sweat_smile",unicode:"1f605",shortname:":sweat_smile:",code_decimal:"&#128517;",category:"p",emoji_order:"7"},{name:"laughing",unicode:"1f606",shortname:":laughing:",code_decimal:"&#128518;",category:"p",emoji_order:"8"},{name:"wink",unicode:"1f609",shortname:":wink:",code_decimal:"&#128521;",category:"p",emoji_order:"9"},{name:"blush",unicode:"1f60a",shortname:":blush:",code_decimal:"&#128522;",category:"p",emoji_order:"10"},{name:"yum",unicode:"1f60b",shortname:":yum:",code_decimal:"&#128523;",category:"p",emoji_order:"11"},{name:"sunglasses",unicode:"1f60e",shortname:":sunglasses:",code_decimal:"&#128526;",category:"p",emoji_order:"12"},{name:"heart_eyes",unicode:"1f60d",shortname:":heart_eyes:",code_decimal:"&#128525;",category:"p",emoji_order:"13"},{name:"kissing_heart",unicode:"1f618",shortname:":kissing_heart:",code_decimal:"&#128536;",category:"p",emoji_order:"14"},{name:"kissing",unicode:"1f617",shortname:":kissing:",code_decimal:"&#128535;",category:"p",emoji_order:"15"},{name:"kissing_smiling_eyes",unicode:"1f619",shortname:":kissing_smiling_eyes:",code_decimal:"&#128537;",category:"p",emoji_order:"16"},{name:"kissing_closed_eyes",unicode:"1f61a",shortname:":kissing_closed_eyes:",code_decimal:"&#128538;",category:"p",emoji_order:"17"},{name:"slightly_smiling_face",unicode:"1f642",shortname:":slight_smile:",code_decimal:"&#128578;",category:"p",emoji_order:"19"},{name:"hugging_face",unicode:"1f917",shortname:":hugging:",code_decimal:"&#129303;",category:"p",emoji_order:"20"},{name:"thinking_face",unicode:"1f914",shortname:":thinking:",code_decimal:"&#129300;",category:"p",emoji_order:"21"},{name:"neutral_face",unicode:"1f610",shortname:":neutral_face:",code_decimal:"&#128528;",category:"p",emoji_order:"22"},{name:"expressionless",unicode:"1f611",shortname:":expressionless:",code_decimal:"&#128529;",category:"p",emoji_order:"23"},{name:"no_mouth",unicode:"1f636",shortname:":no_mouth:",code_decimal:"&#128566;",category:"p",emoji_order:"24"},{name:"face_with_rolling_eyes",unicode:"1f644",shortname:":rolling_eyes:",code_decimal:"&#128580;",category:"p",emoji_order:"25"},{name:"smirk",unicode:"1f60f",shortname:":smirk:",code_decimal:"&#128527;",category:"p",emoji_order:"26"},{name:"persevere",unicode:"1f623",shortname:":persevere:",code_decimal:"&#128547;",category:"p",emoji_order:"27"},{name:"disappointed_relieved",unicode:"1f625",shortname:":disappointed_relieved:",code_decimal:"&#128549;",category:"p",emoji_order:"28"},{name:"open_mouth",unicode:"1f62e",shortname:":open_mouth:",code_decimal:"&#128558;",category:"p",emoji_order:"29"},{name:"zipper_mouth_face",unicode:"1f910",shortname:":zipper_mouth:",code_decimal:"&#129296;",category:"p",emoji_order:"30"},{name:"hushed",unicode:"1f62f",shortname:":hushed:",code_decimal:"&#128559;",category:"p",emoji_order:"31"},{name:"sleepy",unicode:"1f62a",shortname:":sleepy:",code_decimal:"&#128554;",category:"p",emoji_order:"32"},{name:"tired_face",unicode:"1f62b",shortname:":tired_face:",code_decimal:"&#128555;",category:"p",emoji_order:"33"},{name:"sleeping",unicode:"1f634",shortname:":sleeping:",code_decimal:"&#128564;",category:"p",emoji_order:"34"},{name:"relieved",unicode:"1f60c",shortname:":relieved:",code_decimal:"&#128524;",category:"p",emoji_order:"35"},{name:"nerd_face",unicode:"1f913",shortname:":nerd:",code_decimal:"&#129299;",category:"p",emoji_order:"36"},{name:"stuck_out_tongue",unicode:"1f61b",shortname:":stuck_out_tongue:",code_decimal:"&#128539;",category:"p",emoji_order:"37"},{name:"stuck_out_tongue_winking_eye",unicode:"1f61c",shortname:":stuck_out_tongue_winking_eye:",code_decimal:"&#128540;",category:"p",emoji_order:"38"},{name:"stuck_out_tongue_closed_eyes",unicode:"1f61d",shortname:":stuck_out_tongue_closed_eyes:",code_decimal:"&#128541;",category:"p",emoji_order:"39"},{name:"unamused",unicode:"1f612",shortname:":unamused:",code_decimal:"&#128530;",category:"p",emoji_order:"41"},{name:"sweat",unicode:"1f613",shortname:":sweat:",code_decimal:"&#128531;",category:"p",emoji_order:"42"},{name:"pensive",unicode:"1f614",shortname:":pensive:",code_decimal:"&#128532;",category:"p",emoji_order:"43"},{name:"confused",unicode:"1f615",shortname:":confused:",code_decimal:"&#128533;",category:"p",emoji_order:"44"},{name:"upside_down_face",unicode:"1f643",shortname:":upside_down:",code_decimal:"&#128579;",category:"p",emoji_order:"45"},{name:"money_mouth_face",unicode:"1f911",shortname:":money_mouth:",code_decimal:"&#129297;",category:"p",emoji_order:"46"},{name:"astonished",unicode:"1f632",shortname:":astonished:",code_decimal:"&#128562;",category:"p",emoji_order:"47"},{name:"slightly_frowning_face",unicode:"1f641",shortname:":slight_frown:",code_decimal:"&#128577;",category:"p",emoji_order:"49"},{name:"confounded",unicode:"1f616",shortname:":confounded:",code_decimal:"&#128534;",category:"p",emoji_order:"50"},{name:"disappointed",unicode:"1f61e",shortname:":disappointed:",code_decimal:"&#128542;",category:"p",emoji_order:"51"},{name:"worried",unicode:"1f61f",shortname:":worried:",code_decimal:"&#128543;",category:"p",emoji_order:"52"},{name:"triumph",unicode:"1f624",shortname:":triumph:",code_decimal:"&#128548;",category:"p",emoji_order:"53"},{name:"cry",unicode:"1f622",shortname:":cry:",code_decimal:"&#128546;",category:"p",emoji_order:"54"},{name:"sob",unicode:"1f62d",shortname:":sob:",code_decimal:"&#128557;",category:"p",emoji_order:"55"},{name:"frowning",unicode:"1f626",shortname:":frowning:",code_decimal:"&#128550;",category:"p",emoji_order:"56"},{name:"anguished",unicode:"1f627",shortname:":anguished:",code_decimal:"&#128551;",category:"p",emoji_order:"57"},{name:"fearful",unicode:"1f628",shortname:":fearful:",code_decimal:"&#128552;",category:"p",emoji_order:"58"},{name:"weary",unicode:"1f629",shortname:":weary:",code_decimal:"&#128553;",category:"p",emoji_order:"59"},{name:"grimacing",unicode:"1f62c",shortname:":grimacing:",code_decimal:"&#128556;",category:"p",emoji_order:"60"},{name:"cold_sweat",unicode:"1f630",shortname:":cold_sweat:",code_decimal:"&#128560;",category:"p",emoji_order:"61"},{name:"scream",unicode:"1f631",shortname:":scream:",code_decimal:"&#128561;",category:"p",emoji_order:"62"},{name:"flushed",unicode:"1f633",shortname:":flushed:",code_decimal:"&#128563;",category:"p",emoji_order:"63"},{name:"dizzy_face",unicode:"1f635",shortname:":dizzy_face:",code_decimal:"&#128565;",category:"p",emoji_order:"64"},{name:"rage",unicode:"1f621",shortname:":rage:",code_decimal:"&#128545;",category:"p",emoji_order:"65"},{name:"angry",unicode:"1f620",shortname:":angry:",code_decimal:"&#128544;",category:"p",emoji_order:"66"},{name:"innocent",unicode:"1f607",shortname:":innocent:",code_decimal:"&#128519;",category:"p",emoji_order:"67"},{name:"mask",unicode:"1f637",shortname:":mask:",code_decimal:"&#128567;",category:"p",emoji_order:"71"},{name:"face_with_thermometer",unicode:"1f912",shortname:":thermometer_face:",code_decimal:"&#129298;",category:"p",emoji_order:"72"},{name:"face_with_head_bandage",unicode:"1f915",shortname:":head_bandage:",code_decimal:"&#129301;",category:"p",emoji_order:"73"},{name:"smiling_imp",unicode:"1f608",shortname:":smiling_imp:",code_decimal:"&#128520;",category:"p",emoji_order:"76"},{name:"imp",unicode:"1f47f",shortname:":imp:",code_decimal:"&#128127;",category:"p",emoji_order:"77"},{name:"japanese_ogre",unicode:"1f479",shortname:":japanese_ogre:",code_decimal:"&#128121;",category:"p",emoji_order:"78"},{name:"japanese_goblin",unicode:"1f47a",shortname:":japanese_goblin:",code_decimal:"&#128122;",category:"p",emoji_order:"79"},{name:"skull",unicode:"1f480",shortname:":skull:",code_decimal:"&#128128;",category:"p",emoji_order:"80"},{name:"skull_and_crossbones",unicode:"2620",shortname:":skull_crossbones:",code_decimal:"&#9760;",category:"o",emoji_order:"81"},{name:"ghost",unicode:"1f47b",shortname:":ghost:",code_decimal:"&#128123;",category:"p",emoji_order:"82"},{name:"alien",unicode:"1f47d",shortname:":alien:",code_decimal:"&#128125;",category:"p",emoji_order:"83"},{name:"space_invader",unicode:"1f47e",shortname:":space_invader:",code_decimal:"&#128126;",category:"a",emoji_order:"84"},{name:"robot_face",unicode:"1f916",shortname:":robot:",code_decimal:"&#129302;",category:"p",emoji_order:"85"},{name:"hankey",unicode:"1f4a9",shortname:":poop:",code_decimal:"&#128169;",category:"p",emoji_order:"86"},{name:"smiley_cat",unicode:"1f63a",shortname:":smiley_cat:",code_decimal:"&#128570;",category:"p",emoji_order:"87"},{name:"smile_cat",unicode:"1f638",shortname:":smile_cat:",code_decimal:"&#128568;",category:"p",emoji_order:"88"},{name:"joy_cat",unicode:"1f639",shortname:":joy_cat:",code_decimal:"&#128569;",category:"p",emoji_order:"89"},{name:"heart_eyes_cat",unicode:"1f63b",shortname:":heart_eyes_cat:",code_decimal:"&#128571;",category:"p",emoji_order:"90"},{name:"smirk_cat",unicode:"1f63c",shortname:":smirk_cat:",code_decimal:"&#128572;",category:"p",emoji_order:"91"},{name:"kissing_cat",unicode:"1f63d",shortname:":kissing_cat:",code_decimal:"&#128573;",category:"p",emoji_order:"92"},{name:"scream_cat",unicode:"1f640",shortname:":scream_cat:",code_decimal:"&#128576;",category:"p",emoji_order:"93"},{name:"crying_cat_face",unicode:"1f63f",shortname:":crying_cat_face:",code_decimal:"&#128575;",category:"p",emoji_order:"94"},{name:"pouting_cat",unicode:"1f63e",shortname:":pouting_cat:",code_decimal:"&#128574;",category:"p",emoji_order:"95"},{name:"see_no_evil",unicode:"1f648",shortname:":see_no_evil:",code_decimal:"&#128584;",category:"n",emoji_order:"96"},{name:"hear_no_evil",unicode:"1f649",shortname:":hear_no_evil:",code_decimal:"&#128585;",category:"n",emoji_order:"97"},{name:"speak_no_evil",unicode:"1f64a",shortname:":speak_no_evil:",code_decimal:"&#128586;",category:"n",emoji_order:"98"},{name:"boy",unicode:"1f466",shortname:":boy:",code_decimal:"&#128102;",category:"p",emoji_order:"99"},{name:"girl",unicode:"1f467",shortname:":girl:",code_decimal:"&#128103;",category:"p",emoji_order:"105"},{name:"man",unicode:"1f468",shortname:":man:",code_decimal:"&#128104;",category:"p",emoji_order:"111"},{name:"woman",unicode:"1f469",shortname:":woman:",code_decimal:"&#128105;",category:"p",emoji_order:"117"},{name:"older_man",unicode:"1f474",shortname:":older_man:",code_decimal:"&#128116;",category:"p",emoji_order:"123"},{name:"older_woman",unicode:"1f475",shortname:":older_woman:",code_decimal:"&#128117;",category:"p",emoji_order:"129"},{name:"baby",unicode:"1f476",shortname:":baby:",code_decimal:"&#128118;",category:"p",emoji_order:"135"},{name:"angel",unicode:"1f47c",shortname:":angel:",code_decimal:"&#128124;",category:"p",emoji_order:"141"},{name:"cop",unicode:"1f46e",shortname:":cop:",code_decimal:"&#128110;",category:"p",emoji_order:"339"},{name:"sleuth_or_spy",unicode:"1f575",shortname:":spy:",code_decimal:"&#128373;",category:"p",emoji_order:"357"},{name:"guardsman",unicode:"1f482",shortname:":guardsman:",code_decimal:"&#128130;",category:"p",emoji_order:"375"},{name:"construction_worker",unicode:"1f477",shortname:":construction_worker:",code_decimal:"&#128119;",category:"p",emoji_order:"393"},{name:"man_with_turban",unicode:"1f473",shortname:":man_with_turban:",code_decimal:"&#128115;",category:"p",emoji_order:"411"},{name:"person_with_blond_hair",unicode:"1f471",shortname:":person_with_blond_hair:",code_decimal:"&#128113;",category:"p",emoji_order:"429"},{name:"santa",unicode:"1f385",shortname:":santa:",code_decimal:"&#127877;",category:"p",emoji_order:"447"},{name:"princess",unicode:"1f478",shortname:":princess:",code_decimal:"&#128120;",category:"p",emoji_order:"459"},{name:"bride_with_veil",unicode:"1f470",shortname:":bride_with_veil:",code_decimal:"&#128112;",category:"p",emoji_order:"471"},{name:"man_with_gua_pi_mao",unicode:"1f472",shortname:":man_with_gua_pi_mao:",code_decimal:"&#128114;",category:"p",emoji_order:"489"},{name:"person_frowning",unicode:"1f64d",shortname:":person_frowning:",code_decimal:"&#128589;",category:"p",emoji_order:"495"},{name:"person_with_pouting_face",unicode:"1f64e",shortname:":person_with_pouting_face:",code_decimal:"&#128590;",category:"p",emoji_order:"513"},{name:"no_good",unicode:"1f645",shortname:":no_good:",code_decimal:"&#128581;",category:"p",emoji_order:"531"},{name:"ok_woman",unicode:"1f646",shortname:":ok_woman:",code_decimal:"&#128582;",category:"p",emoji_order:"549"},{name:"information_desk_person",unicode:"1f481",shortname:":information_desk_person:",code_decimal:"&#128129;",category:"p",emoji_order:"567"},{name:"raising_hand",unicode:"1f64b",shortname:":raising_hand:",code_decimal:"&#128587;",category:"p",emoji_order:"585"},{name:"bow",unicode:"1f647",shortname:":bow:",code_decimal:"&#128583;",category:"p",emoji_order:"603"},{name:"massage",unicode:"1f486",shortname:":massage:",code_decimal:"&#128134;",category:"p",emoji_order:"657"},{name:"haircut",unicode:"1f487",shortname:":haircut:",code_decimal:"&#128135;",category:"p",emoji_order:"675"},{name:"walking",unicode:"1f6b6",shortname:":walking:",code_decimal:"&#128694;",category:"p",emoji_order:"693"},{name:"runner",unicode:"1f3c3",shortname:":runner:",code_decimal:"&#127939;",category:"p",emoji_order:"711"},{name:"dancer",unicode:"1f483",shortname:":dancer:",code_decimal:"&#128131;",category:"p",emoji_order:"729"},{name:"dancers",unicode:"1f46f",shortname:":dancers:",code_decimal:"&#128111;",category:"p",emoji_order:"741"},{name:"man_in_business_suit_levitating",unicode:"1f574",shortname:":levitate:",code_decimal:"&#128372;",category:"a",emoji_order:"759"},{name:"speaking_head_in_silhouette",unicode:"1f5e3",shortname:":speaking_head:",code_decimal:"&#128483;",category:"p",emoji_order:"765"},{name:"bust_in_silhouette",unicode:"1f464",shortname:":bust_in_silhouette:",code_decimal:"&#128100;",category:"p",emoji_order:"766"},{name:"busts_in_silhouette",unicode:"1f465",shortname:":busts_in_silhouette:",code_decimal:"&#128101;",category:"p",emoji_order:"767"},{name:"horse_racing",unicode:"1f3c7",shortname:":horse_racing:",code_decimal:"&#127943;",category:"a",emoji_order:"769"},{name:"skier",unicode:"26f7",shortname:":skier:",code_decimal:"&#9975;",category:"a",emoji_order:"775"},{name:"snowboarder",unicode:"1f3c2",shortname:":snowboarder:",code_decimal:"&#127938;",category:"a",emoji_order:"776"},{name:"golfer",unicode:"1f3cc",shortname:":golfer:",code_decimal:"&#127948;",category:"a",emoji_order:"782"},{name:"surfer",unicode:"1f3c4",shortname:":surfer:",code_decimal:"&#127940;",category:"a",emoji_order:"800"},{name:"rowboat",unicode:"1f6a3",shortname:":rowboat:",code_decimal:"&#128675;",category:"a",emoji_order:"818"},{name:"swimmer",unicode:"1f3ca",shortname:":swimmer:",code_decimal:"&#127946;",category:"a",emoji_order:"836"},{name:"person_with_ball",unicode:"26f9",shortname:":basketball_player:",code_decimal:"&#9977;",category:"a",emoji_order:"854"},{name:"weight_lifter",unicode:"1f3cb",shortname:":lifter:",code_decimal:"&#127947;",category:"a",emoji_order:"872"},{name:"bicyclist",unicode:"1f6b4",shortname:":bicyclist:",code_decimal:"&#128692;",category:"a",emoji_order:"890"},{name:"mountain_bicyclist",unicode:"1f6b5",shortname:":mountain_bicyclist:",code_decimal:"&#128693;",category:"a",emoji_order:"908"},{name:"racing_car",unicode:"1f3ce",shortname:":race_car:",code_decimal:"&#127950;",category:"t",emoji_order:"926"},{name:"racing_motorcycle",unicode:"1f3cd",shortname:":motorcycle:",code_decimal:"&#127949;",category:"t",emoji_order:"927"},{name:"couple",unicode:"1f46b",shortname:":couple:",code_decimal:"&#128107;",category:"p",emoji_order:"1018"},{name:"two_men_holding_hands",unicode:"1f46c",shortname:":two_men_holding_hands:",code_decimal:"&#128108;",category:"p",emoji_order:"1024"},{name:"two_women_holding_hands",unicode:"1f46d",shortname:":two_women_holding_hands:",code_decimal:"&#128109;",category:"p",emoji_order:"1030"},{name:"couplekiss",unicode:"1f48f",shortname:":couplekiss:",code_decimal:"&#128143;",category:"p",emoji_order:"1036"},{name:"couple_with_heart",unicode:"1f491",shortname:":couple_with_heart:",code_decimal:"&#128145;",category:"p",emoji_order:"1040"},{name:"family",unicode:"1f46a",shortname:":family:",code_decimal:"&#128106;",category:"p",emoji_order:"1044"},{name:"muscle",unicode:"1f4aa",shortname:":muscle:",code_decimal:"&#128170;",category:"p",emoji_order:"1080"},{name:"point_left",unicode:"1f448",shortname:":point_left:",code_decimal:"&#128072;",category:"p",emoji_order:"1092"},{name:"point_right",unicode:"1f449",shortname:":point_right:",code_decimal:"&#128073;",category:"p",emoji_order:"1098"},{name:"point_up",unicode:"261d",shortname:":point_up:",code_decimal:"&#9757;",category:"p",emoji_order:"1104"},{name:"point_up_2",unicode:"1f446",shortname:":point_up_2:",code_decimal:"&#128070;",category:"p",emoji_order:"1110"},{name:"middle_finger",unicode:"1f595",shortname:":middle_finger:",code_decimal:"&#128405;",category:"p",emoji_order:"1116"},{name:"point_down",unicode:"1f447",shortname:":point_down:",code_decimal:"&#128071;",category:"p",emoji_order:"1122"},{name:"v",unicode:"270c",shortname:":v:",code_decimal:"&#9996;",category:"p",emoji_order:"1128"},{name:"the_horns",unicode:"1f918",shortname:":metal_tone2:",code_decimal:"&#129304;",category:"p",emoji_order:"1146"},{name:"raised_hand_with_fingers_splayed",unicode:"1f590",shortname:":hand_splayed:",code_decimal:"&#128400;",category:"p",emoji_order:"1158"},{name:"ok_hand",unicode:"1f44c",shortname:":ok_hand:",code_decimal:"&#128076;",category:"p",emoji_order:"1170"},{name:"thumbsup",unicode:"1f44d",shortname:":thumbsup:",code_decimal:"&#128077;",category:"p",emoji_order:"1176"},{name:"thumbsdown",unicode:"1f44e",shortname:":thumbsdown:",code_decimal:"&#128078;",category:"p",emoji_order:"1182"},{name:"fist",unicode:"270a",shortname:":fist:",code_decimal:"&#9994;",category:"p",emoji_order:"1188"},{name:"facepunch",unicode:"1f44a",shortname:":punch:",code_decimal:"&#128074;",category:"p",emoji_order:"1194"},{name:"wave",unicode:"1f44b",shortname:":wave:",code_decimal:"&#128075;",category:"p",emoji_order:"1218"},{name:"clap",unicode:"1f44f",shortname:":clap:",code_decimal:"&#128079;",category:"p",emoji_order:"1224"},{name:"writing_hand",unicode:"270d",shortname:":writing_hand:",code_decimal:"&#9997;",category:"p",emoji_order:"1230"},{name:"open_hands",unicode:"1f450",shortname:":open_hands:",code_decimal:"&#128080;",category:"p",emoji_order:"1236"},{name:"raised_hands",unicode:"1f64c",shortname:":raised_hands:",code_decimal:"&#128588;",category:"p",emoji_order:"1242"},{name:"pray",unicode:"1f64f",shortname:":pray:",code_decimal:"&#128591;",category:"p",emoji_order:"1248"},{name:"nail_care",unicode:"1f485",shortname:":nail_care:",code_decimal:"&#128133;",category:"p",emoji_order:"1260"},{name:"ear",unicode:"1f442",shortname:":ear:",code_decimal:"&#128066;",category:"p",emoji_order:"1266"},{name:"nose",unicode:"1f443",shortname:":nose:",code_decimal:"&#128067;",category:"p",emoji_order:"1272"},{name:"footprints",unicode:"1f463",shortname:":footprints:",code_decimal:"&#128099;",category:"p",emoji_order:"1278"},{name:"eyes",unicode:"1f440",shortname:":eyes:",code_decimal:"&#128064;",category:"p",emoji_order:"1279"},{name:"eye",unicode:"1f441",shortname:":eye:",code_decimal:"&#128065;",category:"p",emoji_order:"1280"},{name:"tongue",unicode:"1f445",shortname:":tongue:",code_decimal:"&#128069;",category:"p",emoji_order:"1282"},{name:"lips",unicode:"1f444",shortname:":lips:",code_decimal:"&#128068;",category:"p",emoji_order:"1283"},{name:"kiss",unicode:"1f48b",shortname:":kiss:",code_decimal:"&#128139;",category:"p",emoji_order:"1284"},{name:"cupid",unicode:"1f498",shortname:":cupid:",code_decimal:"&#128152;",category:"s",emoji_order:"1285"},{name:"heart",unicode:"2764",shortname:":heart:",code_decimal:"&#10084;",category:"s",emoji_order:"1286"},{name:"heartbeat",unicode:"1f493",shortname:":heartbeat:",code_decimal:"&#128147;",category:"s",emoji_order:"1287"},{name:"broken_heart",unicode:"1f494",shortname:":broken_heart:",code_decimal:"&#128148;",category:"s",emoji_order:"1288"},{name:"two_hearts",unicode:"1f495",shortname:":two_hearts:",code_decimal:"&#128149;",category:"s",emoji_order:"1289"},{name:"sparkling_heart",unicode:"1f496",shortname:":sparkling_heart:",code_decimal:"&#128150;",category:"s",emoji_order:"1290"},{name:"heartpulse",unicode:"1f497",shortname:":heartpulse:",code_decimal:"&#128151;",category:"s",emoji_order:"1291"},{name:"blue_heart",unicode:"1f499",shortname:":blue_heart:",code_decimal:"&#128153;",category:"s",emoji_order:"1292"},{name:"green_heart",unicode:"1f49a",shortname:":green_heart:",code_decimal:"&#128154;",category:"s",emoji_order:"1293"},{name:"yellow_heart",unicode:"1f49b",shortname:":yellow_heart:",code_decimal:"&#128155;",category:"s",emoji_order:"1294"},{name:"purple_heart",unicode:"1f49c",shortname:":purple_heart:",code_decimal:"&#128156;",category:"s",emoji_order:"1295"},{name:"gift_heart",unicode:"1f49d",shortname:":gift_heart:",code_decimal:"&#128157;",category:"s",emoji_order:"1297"},{name:"revolving_hearts",unicode:"1f49e",shortname:":revolving_hearts:",code_decimal:"&#128158;",category:"s",emoji_order:"1298"},{name:"heart_decoration",unicode:"1f49f",shortname:":heart_decoration:",code_decimal:"&#128159;",category:"s",emoji_order:"1299"},{name:"heart_exclamation",unicode:"2763",shortname:":heart_exclamation:",code_decimal:"&#10083;",category:"s",emoji_order:"1300"},{name:"love_letter",unicode:"1f48c",shortname:":love_letter:",code_decimal:"&#128140;",category:"o",emoji_order:"1301"},{name:"zzz",unicode:"1f4a4",shortname:":zzz:",code_decimal:"&#128164;",category:"p",emoji_order:"1302"},{name:"anger",unicode:"1f4a2",shortname:":anger:",code_decimal:"&#128162;",category:"s",emoji_order:"1303"},{name:"bomb",unicode:"1f4a3",shortname:":bomb:",code_decimal:"&#128163;",category:"o",emoji_order:"1304"},{name:"boom",unicode:"1f4a5",shortname:":boom:",code_decimal:"&#128165;",category:"s",emoji_order:"1305"},{name:"sweat_drops",unicode:"1f4a6",shortname:":sweat_drops:",code_decimal:"&#128166;",category:"n",emoji_order:"1306"},{name:"dash",unicode:"1f4a8",shortname:":dash:",code_decimal:"&#128168;",category:"n",emoji_order:"1307"},{name:"dizzy",unicode:"1f4ab",shortname:":dizzy:",code_decimal:"&#128171;",category:"s",emoji_order:"1308"},{name:"speech_balloon",unicode:"1f4ac",shortname:":speech_balloon:",code_decimal:"&#128172;",category:"s",emoji_order:"1309"},{name:"left_speech_bubble",unicode:"1f5e8",shortname:":speech_left:",code_decimal:"&#128488;",category:"s",emoji_order:"1310"},{name:"right_anger_bubble",unicode:"1f5ef",shortname:":anger_right:",code_decimal:"&#128495;",category:"s",emoji_order:"1311"},{name:"thought_balloon",unicode:"1f4ad",shortname:":thought_balloon:",code_decimal:"&#128173;",category:"s",emoji_order:"1312"},{name:"hole",unicode:"1f573",shortname:":hole:",code_decimal:"&#128371;",category:"o",emoji_order:"1313"},{name:"eyeglasses",unicode:"1f453",shortname:":eyeglasses:",code_decimal:"&#128083;",category:"p",emoji_order:"1314"},{name:"dark_sunglasses",unicode:"1f576",shortname:":dark_sunglasses:",code_decimal:"&#128374;",category:"p",emoji_order:"1315"},{name:"necktie",unicode:"1f454",shortname:":necktie:",code_decimal:"&#128084;",category:"p",emoji_order:"1316"},{name:"shirt",unicode:"1f455",shortname:":shirt:",code_decimal:"&#128085;",category:"p",emoji_order:"1317"},{name:"jeans",unicode:"1f456",shortname:":jeans:",code_decimal:"&#128086;",category:"p",emoji_order:"1318"},{name:"dress",unicode:"1f457",shortname:":dress:",code_decimal:"&#128087;",category:"p",emoji_order:"1319"},{name:"kimono",unicode:"1f458",shortname:":kimono:",code_decimal:"&#128088;",category:"p",emoji_order:"1320"},{name:"bikini",unicode:"1f459",shortname:":bikini:",code_decimal:"&#128089;",category:"p",emoji_order:"1321"},{name:"womans_clothes",unicode:"1f45a",shortname:":womans_clothes:",code_decimal:"&#128090;",category:"p",emoji_order:"1322"},{name:"purse",unicode:"1f45b",shortname:":purse:",code_decimal:"&#128091;",category:"p",emoji_order:"1323"},{name:"handbag",unicode:"1f45c",shortname:":handbag:",code_decimal:"&#128092;",category:"p",emoji_order:"1324"},{name:"pouch",unicode:"1f45d",shortname:":pouch:",code_decimal:"&#128093;",category:"p",emoji_order:"1325"},{name:"shopping_bags",unicode:"1f6cd",shortname:":shopping_bags:",code_decimal:"&#128717;",category:"o",emoji_order:"1326"},{name:"school_satchel",unicode:"1f392",shortname:":school_satchel:",code_decimal:"&#127890;",category:"p",emoji_order:"1327"},{name:"mans_shoe",unicode:"1f45e",shortname:":mans_shoe:",code_decimal:"&#128094;",category:"p",emoji_order:"1328"},{name:"athletic_shoe",unicode:"1f45f",shortname:":athletic_shoe:",code_decimal:"&#128095;",category:"p",emoji_order:"1329"},{name:"high_heel",unicode:"1f460",shortname:":high_heel:",code_decimal:"&#128096;",category:"p",emoji_order:"1330"},{name:"sandal",unicode:"1f461",shortname:":sandal:",code_decimal:"&#128097;",category:"p",emoji_order:"1331"},{name:"boot",unicode:"1f462",shortname:":boot:",code_decimal:"&#128098;",category:"p",emoji_order:"1332"},{name:"crown",unicode:"1f451",shortname:":crown:",code_decimal:"&#128081;",category:"p",emoji_order:"1333"},{name:"womans_hat",unicode:"1f452",shortname:":womans_hat:",code_decimal:"&#128082;",category:"p",emoji_order:"1334"},{name:"tophat",unicode:"1f3a9",shortname:":tophat:",code_decimal:"&#127913;",category:"p",emoji_order:"1335"},{name:"mortar_board",unicode:"1f393",shortname:":mortar_board:",code_decimal:"&#127891;",category:"p",emoji_order:"1336"},{name:"helmet_with_white_cross",unicode:"26d1",shortname:":helmet_with_cross:",code_decimal:"&#9937;",category:"p",emoji_order:"1337"},{name:"prayer_beads",unicode:"1f4ff",shortname:":prayer_beads:",code_decimal:"&#128255;",category:"o",emoji_order:"1338"},{name:"lipstick",unicode:"1f484",shortname:":lipstick:",code_decimal:"&#128132;",category:"p",emoji_order:"1339"},{name:"ring",unicode:"1f48d",shortname:":ring:",code_decimal:"&#128141;",category:"p",emoji_order:"1340"},{name:"gem",unicode:"1f48e",shortname:":gem:",code_decimal:"&#128142;",category:"o",emoji_order:"1341"},{name:"monkey_face",unicode:"1f435",shortname:":monkey_face:",code_decimal:"&#128053;",category:"n",emoji_order:"1342"},{name:"monkey",unicode:"1f412",shortname:":monkey:",code_decimal:"&#128018;",category:"n",emoji_order:"1343"},{name:"dog",unicode:"1f436",shortname:":dog:",code_decimal:"&#128054;",category:"n",emoji_order:"1345"},{name:"dog2",unicode:"1f415",shortname:":dog2:",code_decimal:"&#128021;",category:"n",emoji_order:"1346"},{name:"poodle",unicode:"1f429",shortname:":poodle:",code_decimal:"&#128041;",category:"n",emoji_order:"1347"},{name:"wolf",unicode:"1f43a",shortname:":wolf:",code_decimal:"&#128058;",category:"n",emoji_order:"1348"},{name:"cat",unicode:"1f431",shortname:":cat:",code_decimal:"&#128049;",category:"n",emoji_order:"1350"},{name:"cat2",unicode:"1f408",shortname:":cat2:",code_decimal:"&#128008;",category:"n",emoji_order:"1351"},{name:"lion_face",unicode:"1f981",shortname:":lion_face:",code_decimal:"&#129409;",category:"n",emoji_order:"1352"},{name:"tiger",unicode:"1f42f",shortname:":tiger:",code_decimal:"&#128047;",category:"n",emoji_order:"1353"},{name:"tiger2",unicode:"1f405",shortname:":tiger2:",code_decimal:"&#128005;",category:"n",emoji_order:"1354"},{name:"leopard",unicode:"1f406",shortname:":leopard:",code_decimal:"&#128006;",category:"n",emoji_order:"1355"},{name:"horse",unicode:"1f434",shortname:":horse:",code_decimal:"&#128052;",category:"n",emoji_order:"1356"},{name:"racehorse",unicode:"1f40e",shortname:":racehorse:",code_decimal:"&#128014;",category:"n",emoji_order:"1357"},{name:"unicorn_face",unicode:"1f984",shortname:":unicorn:",code_decimal:"&#129412;",category:"n",emoji_order:"1359"},{name:"cow",unicode:"1f42e",shortname:":cow:",code_decimal:"&#128046;",category:"n",emoji_order:"1360"},{name:"ox",unicode:"1f402",shortname:":ox:",code_decimal:"&#128002;",category:"n",emoji_order:"1361"},{name:"water_buffalo",unicode:"1f403",shortname:":water_buffalo:",code_decimal:"&#128003;",category:"n",emoji_order:"1362"},{name:"cow2",unicode:"1f404",shortname:":cow2:",code_decimal:"&#128004;",category:"n",emoji_order:"1363"},{name:"pig",unicode:"1f437",shortname:":pig:",code_decimal:"&#128055;",category:"n",emoji_order:"1364"},{name:"pig2",unicode:"1f416",shortname:":pig2:",code_decimal:"&#128022;",category:"n",emoji_order:"1365"},{name:"boar",unicode:"1f417",shortname:":boar:",code_decimal:"&#128023;",category:"n",emoji_order:"1366"},{name:"pig_nose",unicode:"1f43d",shortname:":pig_nose:",code_decimal:"&#128061;",category:"n",emoji_order:"1367"},{name:"ram",unicode:"1f40f",shortname:":ram:",code_decimal:"&#128015;",category:"n",emoji_order:"1368"},{name:"sheep",unicode:"1f411",shortname:":sheep:",code_decimal:"&#128017;",category:"n",emoji_order:"1369"},{name:"goat",unicode:"1f410",shortname:":goat:",code_decimal:"&#128016;",category:"n",emoji_order:"1370"},{name:"dromedary_camel",unicode:"1f42a",shortname:":dromedary_camel:",code_decimal:"&#128042;",category:"n",emoji_order:"1371"},{name:"camel",unicode:"1f42b",shortname:":camel:",code_decimal:"&#128043;",category:"n",emoji_order:"1372"},{name:"elephant",unicode:"1f418",shortname:":elephant:",code_decimal:"&#128024;",category:"n",emoji_order:"1373"},{name:"mouse",unicode:"1f42d",shortname:":mouse:",code_decimal:"&#128045;",category:"n",emoji_order:"1375"},{name:"mouse2",unicode:"1f401",shortname:":mouse2:",code_decimal:"&#128001;",category:"n",emoji_order:"1376"},{name:"rat",unicode:"1f400",shortname:":rat:",code_decimal:"&#128000;",category:"n",emoji_order:"1377"},{name:"hamster",unicode:"1f439",shortname:":hamster:",code_decimal:"&#128057;",category:"n",emoji_order:"1378"},{name:"rabbit",unicode:"1f430",shortname:":rabbit:",code_decimal:"&#128048;",category:"n",emoji_order:"1379"},{name:"rabbit2",unicode:"1f407",shortname:":rabbit2:",code_decimal:"&#128007;",category:"n",emoji_order:"1380"},{name:"chipmunk",unicode:"1f43f",shortname:":chipmunk:",code_decimal:"&#128063;",category:"n",emoji_order:"1381"},{name:"bear",unicode:"1f43b",shortname:":bear:",code_decimal:"&#128059;",category:"n",emoji_order:"1383"},{name:"koala",unicode:"1f428",shortname:":koala:",code_decimal:"&#128040;",category:"n",emoji_order:"1384"},{name:"panda_face",unicode:"1f43c",shortname:":panda_face:",code_decimal:"&#128060;",category:"n",emoji_order:"1385"},{name:"feet",unicode:"1f43e",shortname:":feet:",code_decimal:"&#128062;",category:"n",emoji_order:"1386"},{name:"turkey",unicode:"1f983",shortname:":turkey:",code_decimal:"&#129411;",category:"n",emoji_order:"1387"},{name:"chicken",unicode:"1f414",shortname:":chicken:",code_decimal:"&#128020;",category:"n",emoji_order:"1388"},{name:"rooster",unicode:"1f413",shortname:":rooster:",code_decimal:"&#128019;",category:"n",emoji_order:"1389"},{name:"hatching_chick",unicode:"1f423",shortname:":hatching_chick:",code_decimal:"&#128035;",category:"n",emoji_order:"1390"},{name:"baby_chick",unicode:"1f424",shortname:":baby_chick:",code_decimal:"&#128036;",category:"n",emoji_order:"1391"},{name:"hatched_chick",unicode:"1f425",shortname:":hatched_chick:",code_decimal:"&#128037;",category:"n",emoji_order:"1392"},{name:"bird",unicode:"1f426",shortname:":bird:",code_decimal:"&#128038;",category:"n",emoji_order:"1393"},{name:"penguin",unicode:"1f427",shortname:":penguin:",code_decimal:"&#128039;",category:"n",emoji_order:"1394"},{name:"dove_of_peace",unicode:"1f54a",shortname:":dove:",code_decimal:"&#128330;",category:"n",emoji_order:"1395"},{name:"frog",unicode:"1f438",shortname:":frog:",code_decimal:"&#128056;",category:"n",emoji_order:"1399"},{name:"crocodile",unicode:"1f40a",shortname:":crocodile:",code_decimal:"&#128010;",category:"n",emoji_order:"1400"},{name:"turtle",unicode:"1f422",shortname:":turtle:",code_decimal:"&#128034;",category:"n",emoji_order:"1401"},{name:"snake",unicode:"1f40d",shortname:":snake:",code_decimal:"&#128013;",category:"n",emoji_order:"1403"},{name:"dragon_face",unicode:"1f432",shortname:":dragon_face:",code_decimal:"&#128050;",category:"n",emoji_order:"1404"},{name:"dragon",unicode:"1f409",shortname:":dragon:",code_decimal:"&#128009;",category:"n",emoji_order:"1405"},{name:"whale",unicode:"1f433",shortname:":whale:",code_decimal:"&#128051;",category:"n",emoji_order:"1406"},{name:"whale2",unicode:"1f40b",shortname:":whale2:",code_decimal:"&#128011;",category:"n",emoji_order:"1407"},{name:"dolphin",unicode:"1f42c",shortname:":dolphin:",code_decimal:"&#128044;",category:"n",emoji_order:"1408"},{name:"fish",unicode:"1f41f",shortname:":fish:",code_decimal:"&#128031;",category:"n",emoji_order:"1409"},{name:"tropical_fish",unicode:"1f420",shortname:":tropical_fish:",code_decimal:"&#128032;",category:"n",emoji_order:"1410"},{name:"blowfish",unicode:"1f421",shortname:":blowfish:",code_decimal:"&#128033;",category:"n",emoji_order:"1411"},{name:"octopus",unicode:"1f419",shortname:":octopus:",code_decimal:"&#128025;",category:"n",emoji_order:"1413"},{name:"shell",unicode:"1f41a",shortname:":shell:",code_decimal:"&#128026;",category:"n",emoji_order:"1414"},{name:"crab",unicode:"1f980",shortname:":crab:",code_decimal:"&#129408;",category:"n",emoji_order:"1415"},{name:"snail",unicode:"1f40c",shortname:":snail:",code_decimal:"&#128012;",category:"n",emoji_order:"1419"},{name:"bug",unicode:"1f41b",shortname:":bug:",code_decimal:"&#128027;",category:"n",emoji_order:"1420"},{name:"ant",unicode:"1f41c",shortname:":ant:",code_decimal:"&#128028;",category:"n",emoji_order:"1421"},{name:"bee",unicode:"1f41d",shortname:":bee:",code_decimal:"&#128029;",category:"n",emoji_order:"1422"},{name:"beetle",unicode:"1f41e",shortname:":beetle:",code_decimal:"&#128030;",category:"n",emoji_order:"1423"},{name:"spider",unicode:"1f577",shortname:":spider:",code_decimal:"&#128375;",category:"n",emoji_order:"1424"},{name:"spider_web",unicode:"1f578",shortname:":spider_web:",code_decimal:"&#128376;",category:"n",emoji_order:"1425"},{name:"scorpion",unicode:"1f982",shortname:":scorpion:",code_decimal:"&#129410;",category:"n",emoji_order:"1426"},{name:"bouquet",unicode:"1f490",shortname:":bouquet:",code_decimal:"&#128144;",category:"n",emoji_order:"1427"},{name:"cherry_blossom",unicode:"1f338",shortname:":cherry_blossom:",code_decimal:"&#127800;",category:"n",emoji_order:"1428"},{name:"white_flower",unicode:"1f4ae",shortname:":white_flower:",code_decimal:"&#128174;",category:"s",emoji_order:"1429"},{name:"rosette",unicode:"1f3f5",shortname:":rosette:",code_decimal:"&#127989;",category:"n",emoji_order:"1430"},{name:"rose",unicode:"1f339",shortname:":rose:",code_decimal:"&#127801;",category:"n",emoji_order:"1431"},{name:"hibiscus",unicode:"1f33a",shortname:":hibiscus:",code_decimal:"&#127802;",category:"n",emoji_order:"1433"},{name:"sunflower",unicode:"1f33b",shortname:":sunflower:",code_decimal:"&#127803;",category:"n",emoji_order:"1434"},{name:"blossom",unicode:"1f33c",shortname:":blossom:",code_decimal:"&#127804;",category:"n",emoji_order:"1435"},{name:"tulip",unicode:"1f337",shortname:":tulip:",code_decimal:"&#127799;",category:"n",emoji_order:"1436"},{name:"seedling",unicode:"1f331",shortname:":seedling:",code_decimal:"&#127793;",category:"n",emoji_order:"1437"},{name:"evergreen_tree",unicode:"1f332",shortname:":evergreen_tree:",code_decimal:"&#127794;",category:"n",emoji_order:"1438"},{name:"deciduous_tree",unicode:"1f333",shortname:":deciduous_tree:",code_decimal:"&#127795;",category:"n",emoji_order:"1439"},{name:"palm_tree",unicode:"1f334",shortname:":palm_tree:",code_decimal:"&#127796;",category:"n",emoji_order:"1440"},{name:"cactus",unicode:"1f335",shortname:":cactus:",code_decimal:"&#127797;",category:"n",emoji_order:"1441"},{name:"ear_of_rice",unicode:"1f33e",shortname:":ear_of_rice:",code_decimal:"&#127806;",category:"n",emoji_order:"1442"},{name:"herb",unicode:"1f33f",shortname:":herb:",code_decimal:"&#127807;",category:"n",emoji_order:"1443"},{name:"shamrock",unicode:"2618",shortname:":shamrock:",code_decimal:"&#9752;",category:"n",emoji_order:"1444"},{name:"four_leaf_clover",unicode:"1f340",shortname:":four_leaf_clover:",code_decimal:"&#127808;",category:"n",emoji_order:"1445"},{name:"maple_leaf",unicode:"1f341",shortname:":maple_leaf:",code_decimal:"&#127809;",category:"n",emoji_order:"1446"},{name:"fallen_leaf",unicode:"1f342",shortname:":fallen_leaf:",code_decimal:"&#127810;",category:"n",emoji_order:"1447"},{name:"leaves",unicode:"1f343",shortname:":leaves:",code_decimal:"&#127811;",category:"n",emoji_order:"1448"},{name:"grapes",unicode:"1f347",shortname:":grapes:",code_decimal:"&#127815;",category:"d",emoji_order:"1449"},{name:"melon",unicode:"1f348",shortname:":melon:",code_decimal:"&#127816;",category:"d",emoji_order:"1450"},{name:"watermelon",unicode:"1f349",shortname:":watermelon:",code_decimal:"&#127817;",category:"d",emoji_order:"1451"},{name:"tangerine",unicode:"1f34a",shortname:":tangerine:",code_decimal:"&#127818;",category:"d",emoji_order:"1452"},{name:"lemon",unicode:"1f34b",shortname:":lemon:",code_decimal:"&#127819;",category:"d",emoji_order:"1453"},{name:"banana",unicode:"1f34c",shortname:":banana:",code_decimal:"&#127820;",category:"d",emoji_order:"1454"},{name:"pineapple",unicode:"1f34d",shortname:":pineapple:",code_decimal:"&#127821;",category:"d",emoji_order:"1455"},{name:"apple",unicode:"1f34e",shortname:":apple:",code_decimal:"&#127822;",category:"d",emoji_order:"1456"},{name:"green_apple",unicode:"1f34f",shortname:":green_apple:",code_decimal:"&#127823;",category:"d",emoji_order:"1457"},{name:"pear",unicode:"1f350",shortname:":pear:",code_decimal:"&#127824;",category:"d",emoji_order:"1458"},{name:"peach",unicode:"1f351",shortname:":peach:",code_decimal:"&#127825;",category:"d",emoji_order:"1459"},{name:"cherries",unicode:"1f352",shortname:":cherries:",code_decimal:"&#127826;",category:"d",emoji_order:"1460"},{name:"strawberry",unicode:"1f353",shortname:":strawberry:",code_decimal:"&#127827;",category:"d",emoji_order:"1461"},{name:"tomato",unicode:"1f345",shortname:":tomato:",code_decimal:"&#127813;",category:"d",emoji_order:"1463"},{name:"eggplant",unicode:"1f346",shortname:":eggplant:",code_decimal:"&#127814;",category:"d",emoji_order:"1465"},{name:"corn",unicode:"1f33d",shortname:":corn:",code_decimal:"&#127805;",category:"d",emoji_order:"1468"},{name:"hot_pepper",unicode:"1f336",shortname:":hot_pepper:",code_decimal:"&#127798;",category:"d",emoji_order:"1469"},{name:"mushroom",unicode:"1f344",shortname:":mushroom:",code_decimal:"&#127812;",category:"n",emoji_order:"1471"},{name:"chestnut",unicode:"1f330",shortname:":chestnut:",code_decimal:"&#127792;",category:"n",emoji_order:"1473"},{name:"bread",unicode:"1f35e",shortname:":bread:",code_decimal:"&#127838;",category:"d",emoji_order:"1474"},{name:"cheese_wedge",unicode:"1f9c0",shortname:":cheese:",code_decimal:"&#129472;",category:"d",emoji_order:"1478"},{name:"meat_on_bone",unicode:"1f356",shortname:":meat_on_bone:",code_decimal:"&#127830;",category:"d",emoji_order:"1479"},{name:"poultry_leg",unicode:"1f357",shortname:":poultry_leg:",code_decimal:"&#127831;",category:"d",emoji_order:"1480"},{name:"hamburger",unicode:"1f354",shortname:":hamburger:",code_decimal:"&#127828;",category:"d",emoji_order:"1482"},{name:"fries",unicode:"1f35f",shortname:":fries:",code_decimal:"&#127839;",category:"d",emoji_order:"1483"},{name:"pizza",unicode:"1f355",shortname:":pizza:",code_decimal:"&#127829;",category:"d",emoji_order:"1484"},{name:"hotdog",unicode:"1f32d",shortname:":hotdog:",code_decimal:"&#127789;",category:"d",emoji_order:"1485"},{name:"taco",unicode:"1f32e",shortname:":taco:",code_decimal:"&#127790;",category:"d",emoji_order:"1486"},{name:"burrito",unicode:"1f32f",shortname:":burrito:",code_decimal:"&#127791;",category:"d",emoji_order:"1487"},{name:"egg",unicode:"1f95a",shortname:":egg:",code_decimal:"&#129370;",category:"d",emoji_order:"1489"},{name:"stew",unicode:"1f372",shortname:":stew:",code_decimal:"&#127858;",category:"d",emoji_order:"1492"},{name:"popcorn",unicode:"1f37f",shortname:":popcorn:",code_decimal:"&#127871;",category:"d",emoji_order:"1494"},{name:"bento",unicode:"1f371",shortname:":bento:",code_decimal:"&#127857;",category:"d",emoji_order:"1495"},{name:"rice_cracker",unicode:"1f358",shortname:":rice_cracker:",code_decimal:"&#127832;",category:"d",emoji_order:"1496"},{name:"rice_ball",unicode:"1f359",shortname:":rice_ball:",code_decimal:"&#127833;",category:"d",emoji_order:"1497"},{name:"rice",unicode:"1f35a",shortname:":rice:",code_decimal:"&#127834;",category:"d",emoji_order:"1498"},{name:"curry",unicode:"1f35b",shortname:":curry:",code_decimal:"&#127835;",category:"d",emoji_order:"1499"},{name:"ramen",unicode:"1f35c",shortname:":ramen:",code_decimal:"&#127836;",category:"d",emoji_order:"1500"},{name:"spaghetti",unicode:"1f35d",shortname:":spaghetti:",code_decimal:"&#127837;",category:"d",emoji_order:"1501"},{name:"sweet_potato",unicode:"1f360",shortname:":sweet_potato:",code_decimal:"&#127840;",category:"d",emoji_order:"1502"},{name:"oden",unicode:"1f362",shortname:":oden:",code_decimal:"&#127842;",category:"d",emoji_order:"1503"},{name:"sushi",unicode:"1f363",shortname:":sushi:",code_decimal:"&#127843;",category:"d",emoji_order:"1504"},{name:"fried_shrimp",unicode:"1f364",shortname:":fried_shrimp:",code_decimal:"&#127844;",category:"d",emoji_order:"1505"},{name:"fish_cake",unicode:"1f365",shortname:":fish_cake:",code_decimal:"&#127845;",category:"d",emoji_order:"1506"},{name:"dango",unicode:"1f361",shortname:":dango:",code_decimal:"&#127841;",category:"d",emoji_order:"1507"},{name:"icecream",unicode:"1f366",shortname:":icecream:",code_decimal:"&#127846;",category:"d",emoji_order:"1508"},{name:"shaved_ice",unicode:"1f367",shortname:":shaved_ice:",code_decimal:"&#127847;",category:"d",emoji_order:"1509"},{name:"ice_cream",unicode:"1f368",shortname:":ice_cream:",code_decimal:"&#127848;",category:"d",emoji_order:"1510"},{name:"doughnut",unicode:"1f369",shortname:":doughnut:",code_decimal:"&#127849;",category:"d",emoji_order:"1511"},{name:"cookie",unicode:"1f36a",shortname:":cookie:",code_decimal:"&#127850;",category:"d",emoji_order:"1512"},{name:"birthday",unicode:"1f382",shortname:":birthday:",code_decimal:"&#127874;",category:"d",emoji_order:"1513"},{name:"cake",unicode:"1f370",shortname:":cake:",code_decimal:"&#127856;",category:"d",emoji_order:"1514"},{name:"chocolate_bar",unicode:"1f36b",shortname:":chocolate_bar:",code_decimal:"&#127851;",category:"d",emoji_order:"1515"},{name:"candy",unicode:"1f36c",shortname:":candy:",code_decimal:"&#127852;",category:"d",emoji_order:"1516"},{name:"lollipop",unicode:"1f36d",shortname:":lollipop:",code_decimal:"&#127853;",category:"d",emoji_order:"1517"},{name:"custard",unicode:"1f36e",shortname:":custard:",code_decimal:"&#127854;",category:"d",emoji_order:"1518"},{name:"honey_pot",unicode:"1f36f",shortname:":honey_pot:",code_decimal:"&#127855;",category:"d",emoji_order:"1519"},{name:"baby_bottle",unicode:"1f37c",shortname:":baby_bottle:",code_decimal:"&#127868;",category:"d",emoji_order:"1520"},{name:"coffee",unicode:"2615",shortname:":coffee:",code_decimal:"&#9749;",category:"d",emoji_order:"1522"},{name:"tea",unicode:"1f375",shortname:":tea:",code_decimal:"&#127861;",category:"d",emoji_order:"1523"},{name:"sake",unicode:"1f376",shortname:":sake:",code_decimal:"&#127862;",category:"d",emoji_order:"1524"},{name:"champagne",unicode:"1f37e",shortname:":champagne:",code_decimal:"&#127870;",category:"d",emoji_order:"1525"},{name:"wine_glass",unicode:"1f377",shortname:":wine_glass:",code_decimal:"&#127863;",category:"d",emoji_order:"1526"},{name:"cocktail",unicode:"1f378",shortname:":cocktail:",code_decimal:"&#127864;",category:"d",emoji_order:"1527"},{name:"tropical_drink",unicode:"1f379",shortname:":tropical_drink:",code_decimal:"&#127865;",category:"d",emoji_order:"1528"},{name:"beer",unicode:"1f37a",shortname:":beer:",code_decimal:"&#127866;",category:"d",emoji_order:"1529"},{name:"beers",unicode:"1f37b",shortname:":beers:",code_decimal:"&#127867;",category:"d",emoji_order:"1530"},{name:"knife_fork_plate",unicode:"1f37d",shortname:":fork_knife_plate:",code_decimal:"&#127869;",category:"d",emoji_order:"1533"},{name:"fork_and_knife",unicode:"1f374",shortname:":fork_and_knife:",code_decimal:"&#127860;",category:"d",emoji_order:"1534"},{name:"amphora",unicode:"1f3fa",shortname:":amphora:",code_decimal:"&#127994;",category:"o",emoji_order:"1537"},{name:"earth_africa",unicode:"1f30d",shortname:":earth_africa:",code_decimal:"&#127757;",category:"n",emoji_order:"1538"},{name:"earth_americas",unicode:"1f30e",shortname:":earth_americas:",code_decimal:"&#127758;",category:"n",emoji_order:"1539"},{name:"earth_asia",unicode:"1f30f",shortname:":earth_asia:",code_decimal:"&#127759;",category:"n",emoji_order:"1540"},{name:"globe_with_meridians",unicode:"1f310",shortname:":globe_with_meridians:",code_decimal:"&#127760;",category:"s",emoji_order:"1541"},{name:"world_map",unicode:"1f5fa",shortname:":map:",code_decimal:"&#128506;",category:"o",emoji_order:"1542"},{name:"japan",unicode:"1f5fe",shortname:":japan:",code_decimal:"&#128510;",category:"t",emoji_order:"1543"},{name:"snow_capped_mountain",unicode:"1f3d4",shortname:":mountain_snow:",code_decimal:"&#127956;",category:"t",emoji_order:"1544"},{name:"mountain",unicode:"26f0",shortname:":mountain:",code_decimal:"&#9968;",category:"t",emoji_order:"1545"},{name:"volcano",unicode:"1f30b",shortname:":volcano:",code_decimal:"&#127755;",category:"t",emoji_order:"1546"},{name:"mount_fuji",unicode:"1f5fb",shortname:":mount_fuji:",code_decimal:"&#128507;",category:"t",emoji_order:"1547"},{name:"camping",unicode:"1f3d5",shortname:":camping:",code_decimal:"&#127957;",category:"t",emoji_order:"1548"},{name:"beach_with_umbrella",unicode:"1f3d6",shortname:":beach:",code_decimal:"&#127958;",category:"t",emoji_order:"1549"},{name:"desert",unicode:"1f3dc",shortname:":desert:",code_decimal:"&#127964;",category:"t",emoji_order:"1550"},{name:"desert_island",unicode:"1f3dd",shortname:":island:",code_decimal:"&#127965;",category:"t",emoji_order:"1551"},{name:"national_park",unicode:"1f3de",shortname:":park:",code_decimal:"&#127966;",category:"t",emoji_order:"1552"},{name:"stadium",unicode:"1f3df",shortname:":stadium:",code_decimal:"&#127967;",category:"t",emoji_order:"1553"},{name:"classical_building",unicode:"1f3db",shortname:":classical_building:",code_decimal:"&#127963;",category:"t",emoji_order:"1554"},{name:"building_construction",unicode:"1f3d7",shortname:":construction_site:",code_decimal:"&#127959;",category:"t",emoji_order:"1555"},{name:"house_buildings",unicode:"1f3d8",shortname:":homes:",code_decimal:"&#127960;",category:"t",emoji_order:"1556"},{name:"cityscape",unicode:"1f3d9",shortname:":cityscape:",code_decimal:"&#127961;",category:"t",emoji_order:"1557"},{name:"derelict_house_building",unicode:"1f3da",shortname:":house_abandoned:",code_decimal:"&#127962;",category:"t",emoji_order:"1558"},{name:"house",unicode:"1f3e0",shortname:":house:",code_decimal:"&#127968;",category:"t",emoji_order:"1559"},{name:"house_with_garden",unicode:"1f3e1",shortname:":house_with_garden:",code_decimal:"&#127969;",category:"t",emoji_order:"1560"},{name:"office",unicode:"1f3e2",shortname:":office:",code_decimal:"&#127970;",category:"t",emoji_order:"1561"},{name:"post_office",unicode:"1f3e3",shortname:":post_office:",code_decimal:"&#127971;",category:"t",emoji_order:"1562"},{name:"european_post_office",unicode:"1f3e4",shortname:":european_post_office:",code_decimal:"&#127972;",category:"t",emoji_order:"1563"},{name:"hospital",unicode:"1f3e5",shortname:":hospital:",code_decimal:"&#127973;",category:"t",emoji_order:"1564"},{name:"bank",unicode:"1f3e6",shortname:":bank:",code_decimal:"&#127974;",category:"t",emoji_order:"1565"},{name:"hotel",unicode:"1f3e8",shortname:":hotel:",code_decimal:"&#127976;",category:"t",emoji_order:"1566"},{name:"love_hotel",unicode:"1f3e9",shortname:":love_hotel:",code_decimal:"&#127977;",category:"t",emoji_order:"1567"},{name:"convenience_store",unicode:"1f3ea",shortname:":convenience_store:",code_decimal:"&#127978;",category:"t",emoji_order:"1568"},{name:"school",unicode:"1f3eb",shortname:":school:",code_decimal:"&#127979;",category:"t",emoji_order:"1569"},{name:"department_store",unicode:"1f3ec",shortname:":department_store:",code_decimal:"&#127980;",category:"t",emoji_order:"1570"},{name:"factory",unicode:"1f3ed",shortname:":factory:",code_decimal:"&#127981;",category:"t",emoji_order:"1571"},{name:"japanese_castle",unicode:"1f3ef",shortname:":japanese_castle:",code_decimal:"&#127983;",category:"t",emoji_order:"1572"},{name:"european_castle",unicode:"1f3f0",shortname:":european_castle:",code_decimal:"&#127984;",category:"t",emoji_order:"1573"},{name:"wedding",unicode:"1f492",shortname:":wedding:",code_decimal:"&#128146;",category:"t",emoji_order:"1574"},{name:"tokyo_tower",unicode:"1f5fc",shortname:":tokyo_tower:",code_decimal:"&#128508;",category:"t",emoji_order:"1575"},{name:"statue_of_liberty",unicode:"1f5fd",shortname:":statue_of_liberty:",code_decimal:"&#128509;",category:"t",emoji_order:"1576"},{name:"church",unicode:"26ea",shortname:":church:",code_decimal:"&#9962;",category:"t",emoji_order:"1577"},{name:"mosque",unicode:"1f54c",shortname:":mosque:",code_decimal:"&#128332;",category:"t",emoji_order:"1578"},{name:"synagogue",unicode:"1f54d",shortname:":synagogue:",code_decimal:"&#128333;",category:"t",emoji_order:"1579"},{name:"shinto_shrine",unicode:"26e9",shortname:":shinto_shrine:",code_decimal:"&#9961;",category:"t",emoji_order:"1580"},{name:"kaaba",unicode:"1f54b",shortname:":kaaba:",code_decimal:"&#128331;",category:"t",emoji_order:"1581"},{name:"fountain",unicode:"26f2",shortname:":fountain:",code_decimal:"&#9970;",category:"t",emoji_order:"1582"},{name:"tent",unicode:"26fa",shortname:":tent:",code_decimal:"&#9978;",category:"t",emoji_order:"1583"},{name:"foggy",unicode:"1f301",shortname:":foggy:",code_decimal:"&#127745;",category:"t",emoji_order:"1584"},{name:"night_with_stars",unicode:"1f303",shortname:":night_with_stars:",code_decimal:"&#127747;",category:"t",emoji_order:"1585"},{name:"sunrise_over_mountains",unicode:"1f304",shortname:":sunrise_over_mountains:",code_decimal:"&#127748;",category:"t",emoji_order:"1586"},{name:"sunrise",unicode:"1f305",shortname:":sunrise:",code_decimal:"&#127749;",category:"t",emoji_order:"1587"},{name:"city_sunset",unicode:"1f307",shortname:":city_sunset:",code_decimal:"&#127751;",category:"t",emoji_order:"1589"},{name:"bridge_at_night",unicode:"1f309",shortname:":bridge_at_night:",code_decimal:"&#127753;",category:"t",emoji_order:"1590"},{name:"hotsprings",unicode:"2668",shortname:":hotsprings:",code_decimal:"&#9832;",category:"s",emoji_order:"1591"},{name:"milky_way",unicode:"1f30c",shortname:":milky_way:",code_decimal:"&#127756;",category:"t",emoji_order:"1592"},{name:"carousel_horse",unicode:"1f3a0",shortname:":carousel_horse:",code_decimal:"&#127904;",category:"t",emoji_order:"1593"},{name:"ferris_wheel",unicode:"1f3a1",shortname:":ferris_wheel:",code_decimal:"&#127905;",category:"t",emoji_order:"1594"},{name:"roller_coaster",unicode:"1f3a2",shortname:":roller_coaster:",code_decimal:"&#127906;",category:"t",emoji_order:"1595"},{name:"barber",unicode:"1f488",shortname:":barber:",code_decimal:"&#128136;",category:"o",emoji_order:"1596"},{name:"circus_tent",unicode:"1f3aa",shortname:":circus_tent:",code_decimal:"&#127914;",category:"a",emoji_order:"1597"},{name:"performing_arts",unicode:"1f3ad",shortname:":performing_arts:",code_decimal:"&#127917;",category:"a",emoji_order:"1598"},{name:"frame_with_picture",unicode:"1f5bc",shortname:":frame_photo:",code_decimal:"&#128444;",category:"o",emoji_order:"1599"},{name:"art",unicode:"1f3a8",shortname:":art:",code_decimal:"&#127912;",category:"a",emoji_order:"1600"},{name:"slot_machine",unicode:"1f3b0",shortname:":slot_machine:",code_decimal:"&#127920;",category:"a",emoji_order:"1601"},{name:"steam_locomotive",unicode:"1f682",shortname:":steam_locomotive:",code_decimal:"&#128642;",category:"t",emoji_order:"1602"},{name:"railway_car",unicode:"1f683",shortname:":railway_car:",code_decimal:"&#128643;",category:"t",emoji_order:"1603"},{name:"bullettrain_side",unicode:"1f684",shortname:":bullettrain_side:",code_decimal:"&#128644;",category:"t",emoji_order:"1604"},{name:"bullettrain_front",unicode:"1f685",shortname:":bullettrain_front:",code_decimal:"&#128645;",category:"t",emoji_order:"1605"},{name:"train2",unicode:"1f686",shortname:":train2:",code_decimal:"&#128646;",category:"t",emoji_order:"1606"},{name:"metro",unicode:"1f687",shortname:":metro:",code_decimal:"&#128647;",category:"t",emoji_order:"1607"},{name:"light_rail",unicode:"1f688",shortname:":light_rail:",code_decimal:"&#128648;",category:"t",emoji_order:"1608"},{name:"station",unicode:"1f689",shortname:":station:",code_decimal:"&#128649;",category:"t",emoji_order:"1609"},{name:"tram",unicode:"1f68a",shortname:":tram:",code_decimal:"&#128650;",category:"t",emoji_order:"1610"},{name:"monorail",unicode:"1f69d",shortname:":monorail:",code_decimal:"&#128669;",category:"t",emoji_order:"1611"},{name:"mountain_railway",unicode:"1f69e",shortname:":mountain_railway:",code_decimal:"&#128670;",category:"t",emoji_order:"1612"},{name:"train",unicode:"1f68b",shortname:":train:",code_decimal:"&#128651;",category:"t",emoji_order:"1613"},{name:"bus",unicode:"1f68c",shortname:":bus:",code_decimal:"&#128652;",category:"t",emoji_order:"1614"},{name:"oncoming_bus",unicode:"1f68d",shortname:":oncoming_bus:",code_decimal:"&#128653;",category:"t",emoji_order:"1615"},{name:"trolleybus",unicode:"1f68e",shortname:":trolleybus:",code_decimal:"&#128654;",category:"t",emoji_order:"1616"},{name:"minibus",unicode:"1f690",shortname:":minibus:",code_decimal:"&#128656;",category:"t",emoji_order:"1617"},{name:"ambulance",unicode:"1f691",shortname:":ambulance:",code_decimal:"&#128657;",category:"t",emoji_order:"1618"},{name:"fire_engine",unicode:"1f692",shortname:":fire_engine:",code_decimal:"&#128658;",category:"t",emoji_order:"1619"},{name:"police_car",unicode:"1f693",shortname:":police_car:",code_decimal:"&#128659;",category:"t",emoji_order:"1620"},{name:"oncoming_police_car",unicode:"1f694",shortname:":oncoming_police_car:",code_decimal:"&#128660;",category:"t",emoji_order:"1621"},{name:"taxi",unicode:"1f695",shortname:":taxi:",code_decimal:"&#128661;",category:"t",emoji_order:"1622"},{name:"oncoming_taxi",unicode:"1f696",shortname:":oncoming_taxi:",code_decimal:"&#128662;",category:"t",emoji_order:"1623"},{name:"car",unicode:"1f697",shortname:":red_car:",code_decimal:"&#128663;",category:"t",emoji_order:"1624"},{name:"oncoming_automobile",unicode:"1f698",shortname:":oncoming_automobile:",code_decimal:"&#128664;",category:"t",emoji_order:"1625"},{name:"blue_car",unicode:"1f699",shortname:":blue_car:",code_decimal:"&#128665;",category:"t",emoji_order:"1626"},{name:"truck",unicode:"1f69a",shortname:":truck:",code_decimal:"&#128666;",category:"t",emoji_order:"1627"},{name:"articulated_lorry",unicode:"1f69b",shortname:":articulated_lorry:",code_decimal:"&#128667;",category:"t",emoji_order:"1628"},{name:"tractor",unicode:"1f69c",shortname:":tractor:",code_decimal:"&#128668;",category:"t",emoji_order:"1629"},{name:"bike",unicode:"1f6b2",shortname:":bike:",code_decimal:"&#128690;",category:"t",emoji_order:"1630"},{name:"busstop",unicode:"1f68f",shortname:":busstop:",code_decimal:"&#128655;",category:"t",emoji_order:"1633"},{name:"motorway",unicode:"1f6e3",shortname:":motorway:",code_decimal:"&#128739;",category:"t",emoji_order:"1634"},{name:"railway_track",unicode:"1f6e4",shortname:":railway_track:",code_decimal:"&#128740;",category:"t",emoji_order:"1635"},{name:"fuelpump",unicode:"26fd",shortname:":fuelpump:",code_decimal:"&#9981;",category:"t",emoji_order:"1636"},{name:"rotating_light",unicode:"1f6a8",shortname:":rotating_light:",code_decimal:"&#128680;",category:"t",emoji_order:"1637"},{name:"traffic_light",unicode:"1f6a5",shortname:":traffic_light:",code_decimal:"&#128677;",category:"t",emoji_order:"1638"},{name:"vertical_traffic_light",unicode:"1f6a6",shortname:":vertical_traffic_light:",code_decimal:"&#128678;",category:"t",emoji_order:"1639"},{name:"construction",unicode:"1f6a7",shortname:":construction:",code_decimal:"&#128679;",category:"t",emoji_order:"1640"},{name:"octagonal_sign",unicode:"1f6d1",shortname:":octagonal_sign:",code_decimal:"&#128721;",category:"s",emoji_order:"1641"},{name:"anchor",unicode:"2693",shortname:":anchor:",code_decimal:"&#9875;",category:"t",emoji_order:"1642"},{name:"boat",unicode:"26f5",shortname:":sailboat:",code_decimal:"&#9973;",category:"t",emoji_order:"1643"},{name:"speedboat",unicode:"1f6a4",shortname:":speedboat:",code_decimal:"&#128676;",category:"t",emoji_order:"1645"},{name:"passenger_ship",unicode:"1f6f3",shortname:":cruise_ship:",code_decimal:"&#128755;",category:"t",emoji_order:"1646"},{name:"ferry",unicode:"26f4",shortname:":ferry:",code_decimal:"&#9972;",category:"t",emoji_order:"1647"},{name:"motor_boat",unicode:"1f6e5",shortname:":motorboat:",code_decimal:"&#128741;",category:"t",emoji_order:"1648"},{name:"ship",unicode:"1f6a2",shortname:":ship:",code_decimal:"&#128674;",category:"t",emoji_order:"1649"},{name:"airplane",unicode:"2708",shortname:":airplane:",code_decimal:"&#9992;",category:"t",emoji_order:"1650"},{name:"small_airplane",unicode:"1f6e9",shortname:":airplane_small:",code_decimal:"&#128745;",category:"t",emoji_order:"1651"},{name:"airplane_departure",unicode:"1f6eb",shortname:":airplane_departure:",code_decimal:"&#128747;",category:"t",emoji_order:"1652"},{name:"airplane_arriving",unicode:"1f6ec",shortname:":airplane_arriving:",code_decimal:"&#128748;",category:"t",emoji_order:"1653"},{name:"seat",unicode:"1f4ba",shortname:":seat:",code_decimal:"&#128186;",category:"t",emoji_order:"1654"},{name:"helicopter",unicode:"1f681",shortname:":helicopter:",code_decimal:"&#128641;",category:"t",emoji_order:"1655"},{name:"suspension_railway",unicode:"1f69f",shortname:":suspension_railway:",code_decimal:"&#128671;",category:"t",emoji_order:"1656"},{name:"mountain_cableway",unicode:"1f6a0",shortname:":mountain_cableway:",code_decimal:"&#128672;",category:"t",emoji_order:"1657"},{name:"aerial_tramway",unicode:"1f6a1",shortname:":aerial_tramway:",code_decimal:"&#128673;",category:"t",emoji_order:"1658"},{name:"rocket",unicode:"1f680",shortname:":rocket:",code_decimal:"&#128640;",category:"t",emoji_order:"1659"},{name:"satellite",unicode:"1f6f0",shortname:":satellite_orbital:",code_decimal:"&#128752;",category:"t",emoji_order:"1660"},{name:"bellhop_bell",unicode:"1f6ce",shortname:":bellhop:",code_decimal:"&#128718;",category:"o",emoji_order:"1661"},{name:"door",unicode:"1f6aa",shortname:":door:",code_decimal:"&#128682;",category:"o",emoji_order:"1662"},{name:"sleeping_accommodation",unicode:"1f6cc",shortname:":sleeping_accommodation:",code_decimal:"&#128716;",category:"o",emoji_order:"1663"},{name:"bed",unicode:"1f6cf",shortname:":bed:",code_decimal:"&#128719;",category:"o",emoji_order:"1669"},{name:"couch_and_lamp",unicode:"1f6cb",shortname:":couch:",code_decimal:"&#128715;",category:"o",emoji_order:"1670"},{name:"toilet",unicode:"1f6bd",shortname:":toilet:",code_decimal:"&#128701;",category:"o",emoji_order:"1671"},{name:"shower",unicode:"1f6bf",shortname:":shower:",code_decimal:"&#128703;",category:"o",emoji_order:"1672"},{name:"bath",unicode:"1f6c0",shortname:":bath:",code_decimal:"&#128704;",category:"a",emoji_order:"1673"},{name:"bathtub",unicode:"1f6c1",shortname:":bathtub:",code_decimal:"&#128705;",category:"o",emoji_order:"1679"},{name:"hourglass",unicode:"231b",shortname:":hourglass:",code_decimal:"&#8987;",category:"o",emoji_order:"1680"},{name:"hourglass_flowing_sand",unicode:"23f3",shortname:":hourglass_flowing_sand:",code_decimal:"&#9203;",category:"o",emoji_order:"1681"},{name:"watch",unicode:"231a",shortname:":watch:",code_decimal:"&#8986;",category:"o",emoji_order:"1682"},{name:"alarm_clock",unicode:"23f0",shortname:":alarm_clock:",code_decimal:"&#9200;",category:"o",emoji_order:"1683"},{name:"stopwatch",unicode:"23f1",shortname:":stopwatch:",code_decimal:"&#9201;",category:"o",emoji_order:"1684"},{name:"timer_clock",unicode:"23f2",shortname:":timer:",code_decimal:"&#9202;",category:"o",emoji_order:"1685"},{name:"mantelpiece_clock",unicode:"1f570",shortname:":clock:",code_decimal:"&#128368;",category:"o",emoji_order:"1686"},{name:"clock12",unicode:"1f55b",shortname:":clock12:",code_decimal:"&#128347;",category:"s",emoji_order:"1687"},{name:"clock1230",unicode:"1f567",shortname:":clock1230:",code_decimal:"&#128359;",category:"s",emoji_order:"1688"},{name:"clock1",unicode:"1f550",shortname:":clock1:",code_decimal:"&#128336;",category:"s",emoji_order:"1689"},{name:"clock130",unicode:"1f55c",shortname:":clock130:",code_decimal:"&#128348;",category:"s",emoji_order:"1690"},{name:"clock2",unicode:"1f551",shortname:":clock2:",code_decimal:"&#128337;",category:"s",emoji_order:"1691"},{name:"clock230",unicode:"1f55d",shortname:":clock230:",code_decimal:"&#128349;",category:"s",emoji_order:"1692"},{name:"clock3",unicode:"1f552",shortname:":clock3:",code_decimal:"&#128338;",category:"s",emoji_order:"1693"},{name:"clock330",unicode:"1f55e",shortname:":clock330:",code_decimal:"&#128350;",category:"s",emoji_order:"1694"},{name:"clock4",unicode:"1f553",shortname:":clock4:",code_decimal:"&#128339;",category:"s",emoji_order:"1695"},{name:"clock430",unicode:"1f55f",shortname:":clock430:",code_decimal:"&#128351;",category:"s",emoji_order:"1696"},{name:"clock5",unicode:"1f554",shortname:":clock5:",code_decimal:"&#128340;",category:"s",emoji_order:"1697"},{name:"clock530",unicode:"1f560",shortname:":clock530:",code_decimal:"&#128352;",category:"s",emoji_order:"1698"},{name:"clock6",unicode:"1f555",shortname:":clock6:",code_decimal:"&#128341;",category:"s",emoji_order:"1699"},{name:"clock630",unicode:"1f561",shortname:":clock630:",code_decimal:"&#128353;",category:"s",emoji_order:"1700"},{name:"clock7",unicode:"1f556",shortname:":clock7:",code_decimal:"&#128342;",category:"s",emoji_order:"1701"},{name:"clock730",unicode:"1f562",shortname:":clock730:",code_decimal:"&#128354;",category:"s",emoji_order:"1702"},{name:"clock8",unicode:"1f557",shortname:":clock8:",code_decimal:"&#128343;",category:"s",emoji_order:"1703"},{name:"clock830",unicode:"1f563",shortname:":clock830:",code_decimal:"&#128355;",category:"s",emoji_order:"1704"},{name:"clock9",unicode:"1f558",shortname:":clock9:",code_decimal:"&#128344;",category:"s",emoji_order:"1705"},{name:"clock930",unicode:"1f564",shortname:":clock930:",code_decimal:"&#128356;",category:"s",emoji_order:"1706"},{name:"clock10",unicode:"1f559",shortname:":clock10:",code_decimal:"&#128345;",category:"s",emoji_order:"1707"},{name:"clock1030",unicode:"1f565",shortname:":clock1030:",code_decimal:"&#128357;",category:"s",emoji_order:"1708"},{name:"clock11",unicode:"1f55a",shortname:":clock11:",code_decimal:"&#128346;",category:"s",emoji_order:"1709"},{name:"clock1130",unicode:"1f566",shortname:":clock1130:",code_decimal:"&#128358;",category:"s",emoji_order:"1710"},{name:"new_moon",unicode:"1f311",shortname:":new_moon:",code_decimal:"&#127761;",category:"n",emoji_order:"1711"},{name:"waxing_crescent_moon",unicode:"1f312",shortname:":waxing_crescent_moon:",code_decimal:"&#127762;",category:"n",emoji_order:"1712"},{name:"first_quarter_moon",unicode:"1f313",shortname:":first_quarter_moon:",code_decimal:"&#127763;",category:"n",emoji_order:"1713"},{name:"full_moon",unicode:"1f315",shortname:":full_moon:",code_decimal:"&#127765;",category:"n",emoji_order:"1715"},{name:"waning_gibbous_moon",unicode:"1f316",shortname:":waning_gibbous_moon:",code_decimal:"&#127766;",category:"n",emoji_order:"1716"},{name:"last_quarter_moon",unicode:"1f317",shortname:":last_quarter_moon:",code_decimal:"&#127767;",category:"n",emoji_order:"1717"},{name:"waning_crescent_moon",unicode:"1f318",shortname:":waning_crescent_moon:",code_decimal:"&#127768;",category:"n",emoji_order:"1718"},{name:"crescent_moon",unicode:"1f319",shortname:":crescent_moon:",code_decimal:"&#127769;",category:"n",emoji_order:"1719"},{name:"new_moon_with_face",unicode:"1f31a",shortname:":new_moon_with_face:",code_decimal:"&#127770;",category:"n",emoji_order:"1720"},{name:"first_quarter_moon_with_face",unicode:"1f31b",shortname:":first_quarter_moon_with_face:",code_decimal:"&#127771;",category:"n",emoji_order:"1721"},{name:"last_quarter_moon_with_face",unicode:"1f31c",shortname:":last_quarter_moon_with_face:",code_decimal:"&#127772;",category:"n",emoji_order:"1722"},{name:"thermometer",unicode:"1f321",shortname:":thermometer:",code_decimal:"&#127777;",category:"o",emoji_order:"1723"},{name:"sunny",unicode:"2600",shortname:":sunny:",code_decimal:"&#9728;",category:"n",emoji_order:"1724"},{name:"full_moon_with_face",unicode:"1f31d",shortname:":full_moon_with_face:",code_decimal:"&#127773;",category:"n",emoji_order:"1725"},{name:"sun_with_face",unicode:"1f31e",shortname:":sun_with_face:",code_decimal:"&#127774;",category:"n",emoji_order:"1726"},{name:"star",unicode:"2b50",shortname:":star:",code_decimal:"&#11088;",category:"n",emoji_order:"1727"},{name:"star2",unicode:"1f31f",shortname:":star2:",code_decimal:"&#127775;",category:"n",emoji_order:"1728"},{name:"stars",unicode:"1f320",shortname:":stars:",code_decimal:"&#127776;",category:"t",emoji_order:"1729"},{name:"cloud",unicode:"2601",shortname:":cloud:",code_decimal:"&#9729;",category:"n",emoji_order:"1730"},{name:"partly_sunny",unicode:"26c5",shortname:":partly_sunny:",code_decimal:"&#9925;",category:"n",emoji_order:"1731"},{name:"thunder_cloud_and_rain",unicode:"26c8",shortname:":thunder_cloud_rain:",code_decimal:"&#9928;",category:"n",emoji_order:"1732"},{name:"rain_cloud",unicode:"1f327",shortname:":cloud_rain:",code_decimal:"&#127783;",category:"n",emoji_order:"1736"},{name:"snow_cloud",unicode:"1f328",shortname:":cloud_snow:",code_decimal:"&#127784;",category:"n",emoji_order:"1737"},{name:"fog",unicode:"1f32b",shortname:":fog:",code_decimal:"&#127787;",category:"n",emoji_order:"1740"},{name:"wind_blowing_face",unicode:"1f32c",shortname:":wind_blowing_face:",code_decimal:"&#127788;",category:"n",emoji_order:"1741"},{name:"cyclone",unicode:"1f300",shortname:":cyclone:",code_decimal:"&#127744;",category:"s",emoji_order:"1742"},{name:"rainbow",unicode:"1f308",shortname:":rainbow:",code_decimal:"&#127752;",category:"t",emoji_order:"1743"},{name:"closed_umbrella",unicode:"1f302",shortname:":closed_umbrella:",code_decimal:"&#127746;",category:"p",emoji_order:"1744"},{name:"umbrella",unicode:"2602",shortname:":umbrella2:",code_decimal:"&#9730;",category:"n",emoji_order:"1745"},{name:"umbrella_with_rain_drops",unicode:"2614",shortname:":umbrella:",code_decimal:"&#9748;",category:"n",emoji_order:"1746"},{name:"beach_umbrella",unicode:"26f1",shortname:":beach_umbrella:",code_decimal:"&#9969;",category:"o",emoji_order:"1747"},{name:"zap",unicode:"26a1",shortname:":zap:",code_decimal:"&#9889;",category:"n",emoji_order:"1748"},{name:"snowflake",unicode:"2744",shortname:":snowflake:",code_decimal:"&#10052;",category:"n",emoji_order:"1749"},{name:"snowman",unicode:"2603",shortname:":snowman2:",code_decimal:"&#9731;",category:"n",emoji_order:"1750"},{name:"snowman_without_snow",unicode:"26c4",shortname:":snowman:",code_decimal:"&#9924;",category:"n",emoji_order:"1751"},{name:"comet",unicode:"2604",shortname:":comet:",code_decimal:"&#9732;",category:"n",emoji_order:"1752"},{name:"fire",unicode:"1f525",shortname:":fire:",code_decimal:"&#128293;",category:"n",emoji_order:"1753"},{name:"droplet",unicode:"1f4a7",shortname:":droplet:",code_decimal:"&#128167;",category:"n",emoji_order:"1754"},{name:"ocean",unicode:"1f30a",shortname:":ocean:",code_decimal:"&#127754;",category:"n",emoji_order:"1755"},{name:"jack_o_lantern",unicode:"1f383",shortname:":jack_o_lantern:",code_decimal:"&#127875;",category:"n",emoji_order:"1756"},{name:"christmas_tree",unicode:"1f384",shortname:":christmas_tree:",code_decimal:"&#127876;",category:"n",emoji_order:"1757"},{name:"fireworks",unicode:"1f386",shortname:":fireworks:",code_decimal:"&#127878;",category:"t",emoji_order:"1758"},{name:"sparkler",unicode:"1f387",shortname:":sparkler:",code_decimal:"&#127879;",category:"t",emoji_order:"1759"},{name:"sparkles",unicode:"2728",shortname:":sparkles:",code_decimal:"&#10024;",category:"n",emoji_order:"1760"},{name:"balloon",unicode:"1f388",shortname:":balloon:",code_decimal:"&#127880;",category:"o",emoji_order:"1761"},{name:"tada",unicode:"1f389",shortname:":tada:",code_decimal:"&#127881;",category:"o",emoji_order:"1762"},{name:"confetti_ball",unicode:"1f38a",shortname:":confetti_ball:",code_decimal:"&#127882;",category:"o",emoji_order:"1763"},{name:"tanabata_tree",unicode:"1f38b",shortname:":tanabata_tree:",code_decimal:"&#127883;",category:"n",emoji_order:"1764"},{name:"bamboo",unicode:"1f38d",shortname:":bamboo:",code_decimal:"&#127885;",category:"n",emoji_order:"1765"},{name:"dolls",unicode:"1f38e",shortname:":dolls:",code_decimal:"&#127886;",category:"o",emoji_order:"1766"},{name:"f",unicode:"1f38f",shortname:":flags:",code_decimal:"&#127887;",category:"o",emoji_order:"1767"},{name:"wind_chime",unicode:"1f390",shortname:":wind_chime:",code_decimal:"&#127888;",category:"o",emoji_order:"1768"},{name:"rice_scene",unicode:"1f391",shortname:":rice_scene:",code_decimal:"&#127889;",category:"t",emoji_order:"1769"},{name:"ribbon",unicode:"1f380",shortname:":ribbon:",code_decimal:"&#127872;",category:"o",emoji_order:"1770"},{name:"gift",unicode:"1f381",shortname:":gift:",code_decimal:"&#127873;",category:"o",emoji_order:"1771"},{name:"reminder_ribbon",unicode:"1f397",shortname:":reminder_ribbon:",code_decimal:"&#127895;",category:"a",emoji_order:"1772"},{name:"admission_tickets",unicode:"1f39f",shortname:":tickets:",code_decimal:"&#127903;",category:"a",emoji_order:"1773"},{name:"ticket",unicode:"1f3ab",shortname:":ticket:",code_decimal:"&#127915;",category:"a",emoji_order:"1774"},{name:"medal",unicode:"1f396",shortname:":military_medal:",code_decimal:"&#127894;",category:"a",emoji_order:"1775"},{name:"trophy",unicode:"1f3c6",shortname:":trophy:",code_decimal:"&#127942;",category:"a",emoji_order:"1776"},{name:"sports_medal",unicode:"1f3c5",shortname:":medal:",code_decimal:"&#127941;",category:"a",emoji_order:"1777"},{name:"soccer",unicode:"26bd",shortname:":soccer:",code_decimal:"&#9917;",category:"a",emoji_order:"1781"},{name:"baseball",unicode:"26be",shortname:":baseball:",code_decimal:"&#9918;",category:"a",emoji_order:"1782"},{name:"basketball",unicode:"1f3c0",shortname:":basketball:",code_decimal:"&#127936;",category:"a",emoji_order:"1783"},{name:"volleyball",unicode:"1f3d0",shortname:":volleyball:",code_decimal:"&#127952;",category:"a",emoji_order:"1784"},{name:"football",unicode:"1f3c8",shortname:":football:",code_decimal:"&#127944;",category:"a",emoji_order:"1785"},{name:"rugby_football",unicode:"1f3c9",shortname:":rugby_football:",code_decimal:"&#127945;",category:"a",emoji_order:"1786"},{name:"tennis",unicode:"1f3be",shortname:":tennis:",code_decimal:"&#127934;",category:"a",emoji_order:"1787"},{name:"8ball",unicode:"1f3b1",shortname:":8ball:",code_decimal:"&#127921;",category:"a",emoji_order:"1788"},{name:"bowling",unicode:"1f3b3",shortname:":bowling:",code_decimal:"&#127923;",category:"a",emoji_order:"1789"},{name:"cricket_bat_and_ball",unicode:"1f3cf",shortname:":cricket_game:",code_decimal:"&#127951;",category:"a",emoji_order:"1790"},{name:"field_hockey_stick_and_ball",unicode:"1f3d1",shortname:":field_hockey:",code_decimal:"&#127953;",category:"a",emoji_order:"1791"},{name:"ice_hockey_stick_and_puck",unicode:"1f3d2",shortname:":hockey:",code_decimal:"&#127954;",category:"a",emoji_order:"1792"},{name:"table_tennis_paddle_and_ball",unicode:"1f3d3",shortname:":ping_pong:",code_decimal:"&#127955;",category:"a",emoji_order:"1793"},{name:"badminton_racquet_and_shuttlecock",unicode:"1f3f8",shortname:":badminton:",code_decimal:"&#127992;",category:"a",emoji_order:"1794"},{name:"dart",unicode:"1f3af",shortname:":dart:",code_decimal:"&#127919;",category:"a",emoji_order:"1798"},{name:"golf",unicode:"26f3",shortname:":golf:",code_decimal:"&#9971;",category:"a",emoji_order:"1799"},{name:"ice_skate",unicode:"26f8",shortname:":ice_skate:",code_decimal:"&#9976;",category:"a",emoji_order:"1800"},{name:"fishing_pole_and_fish",unicode:"1f3a3",shortname:":fishing_pole_and_fish:",code_decimal:"&#127907;",category:"a",emoji_order:"1801"},{name:"running_shirt_with_sash",unicode:"1f3bd",shortname:":running_shirt_with_sash:",code_decimal:"&#127933;",category:"a",emoji_order:"1802"},{name:"ski",unicode:"1f3bf",shortname:":ski:",code_decimal:"&#127935;",category:"a",emoji_order:"1803"},{name:"video_game",unicode:"1f3ae",shortname:":video_game:",code_decimal:"&#127918;",category:"a",emoji_order:"1804"},{name:"joystick",unicode:"1f579",shortname:":joystick:",code_decimal:"&#128377;",category:"o",emoji_order:"1805"},{name:"game_die",unicode:"1f3b2",shortname:":game_die:",code_decimal:"&#127922;",category:"a",emoji_order:"1806"},{name:"spades",unicode:"2660",shortname:":spades:",code_decimal:"&spades;",category:"s",emoji_order:"1807"},{name:"hearts",unicode:"2665",shortname:":hearts:",code_decimal:"&hearts;",category:"s",emoji_order:"1808"},{name:"diamonds",unicode:"2666",shortname:":diamonds:",code_decimal:"&diams;",category:"s",emoji_order:"1809"},{name:"clubs",unicode:"2663",shortname:":clubs:",code_decimal:"&clubs;",category:"s",emoji_order:"1810"},{name:"black_joker",unicode:"1f0cf",shortname:":black_joker:",code_decimal:"&#127183;",category:"s",emoji_order:"1811"},{name:"mahjong",unicode:"1f004",shortname:":mahjong:",code_decimal:"&#126980;",category:"s",emoji_order:"1812"},{name:"flower_playing_cards",unicode:"1f3b4",shortname:":flower_playing_cards:",code_decimal:"&#127924;",category:"s",emoji_order:"1813"},{name:"mute",unicode:"1f507",shortname:":mute:",code_decimal:"&#128263;",category:"s",emoji_order:"1814"},{name:"speaker",unicode:"1f508",shortname:":speaker:",code_decimal:"&#128264;",category:"s",emoji_order:"1815"},{name:"sound",unicode:"1f509",shortname:":sound:",code_decimal:"&#128265;",category:"s",emoji_order:"1816"},{name:"loud_sound",unicode:"1f50a",shortname:":loud_sound:",code_decimal:"&#128266;",category:"s",emoji_order:"1817"},{name:"loudspeaker",unicode:"1f4e2",shortname:":loudspeaker:",code_decimal:"&#128226;",category:"s",emoji_order:"1818"},{name:"mega",unicode:"1f4e3",shortname:":mega:",code_decimal:"&#128227;",category:"s",emoji_order:"1819"},{name:"postal_horn",unicode:"1f4ef",shortname:":postal_horn:",code_decimal:"&#128239;",category:"o",emoji_order:"1820"},{name:"bell",unicode:"1f514",shortname:":bell:",code_decimal:"&#128276;",category:"s",emoji_order:"1821"},{name:"no_bell",unicode:"1f515",shortname:":no_bell:",code_decimal:"&#128277;",category:"s",emoji_order:"1822"},{name:"musical_score",unicode:"1f3bc",shortname:":musical_score:",code_decimal:"&#127932;",category:"a",emoji_order:"1823"},{name:"musical_note",unicode:"1f3b5",shortname:":musical_note:",code_decimal:"&#127925;",category:"s",emoji_order:"1824"},{name:"notes",unicode:"1f3b6",shortname:":notes:",code_decimal:"&#127926;",category:"s",emoji_order:"1825"},{name:"studio_microphone",unicode:"1f399",shortname:":microphone2:",code_decimal:"&#127897;",category:"o",emoji_order:"1826"},{name:"level_slider",unicode:"1f39a",shortname:":level_slider:",code_decimal:"&#127898;",category:"o",emoji_order:"1827"},{name:"control_knobs",unicode:"1f39b",shortname:":control_knobs:",code_decimal:"&#127899;",category:"o",emoji_order:"1828"},{name:"microphone",unicode:"1f3a4",shortname:":microphone:",code_decimal:"&#127908;",category:"a",emoji_order:"1829"},{name:"headphones",unicode:"1f3a7",shortname:":headphones:",code_decimal:"&#127911;",category:"a",emoji_order:"1830"},{name:"radio",unicode:"1f4fb",shortname:":radio:",code_decimal:"&#128251;",category:"o",emoji_order:"1831"},{name:"saxophone",unicode:"1f3b7",shortname:":saxophone:",code_decimal:"&#127927;",category:"a",emoji_order:"1832"},{name:"guitar",unicode:"1f3b8",shortname:":guitar:",code_decimal:"&#127928;",category:"a",emoji_order:"1833"},{name:"musical_keyboard",unicode:"1f3b9",shortname:":musical_keyboard:",code_decimal:"&#127929;",category:"a",emoji_order:"1834"},{name:"trumpet",unicode:"1f3ba",shortname:":trumpet:",code_decimal:"&#127930;",category:"a",emoji_order:"1835"},{name:"violin",unicode:"1f3bb",shortname:":violin:",code_decimal:"&#127931;",category:"a",emoji_order:"1836"},{name:"iphone",unicode:"1f4f1",shortname:":iphone:",code_decimal:"&#128241;",category:"o",emoji_order:"1838"},{name:"calling",unicode:"1f4f2",shortname:":calling:",code_decimal:"&#128242;",category:"o",emoji_order:"1839"},{name:"telephone",unicode:"260e",shortname:":telephone:",code_decimal:"&#9742;",category:"o",emoji_order:"1840"},{name:"telephone_receiver",unicode:"1f4de",shortname:":telephone_receiver:",code_decimal:"&#128222;",category:"o",emoji_order:"1841"},{name:"pager",unicode:"1f4df",shortname:":pager:",code_decimal:"&#128223;",category:"o",emoji_order:"1842"},{name:"fax",unicode:"1f4e0",shortname:":fax:",code_decimal:"&#128224;",category:"o",emoji_order:"1843"},{name:"battery",unicode:"1f50b",shortname:":battery:",code_decimal:"&#128267;",category:"o",emoji_order:"1844"},{name:"electric_plug",unicode:"1f50c",shortname:":electric_plug:",code_decimal:"&#128268;",category:"o",emoji_order:"1845"},{name:"computer",unicode:"1f4bb",shortname:":computer:",code_decimal:"&#128187;",category:"o",emoji_order:"1846"},{name:"desktop_computer",unicode:"1f5a5",shortname:":desktop:",code_decimal:"&#128421;",category:"o",emoji_order:"1847"},{name:"printer",unicode:"1f5a8",shortname:":printer:",code_decimal:"&#128424;",category:"o",emoji_order:"1848"},{name:"keyboard",unicode:"2328",shortname:":keyboard:",code_decimal:"&#9000;",category:"o",emoji_order:"1849"},{name:"three_button_mouse",unicode:"1f5b1",shortname:":mouse_three_button:",code_decimal:"&#128433;",category:"o",emoji_order:"1850"},{name:"trackball",unicode:"1f5b2",shortname:":trackball:",code_decimal:"&#128434;",category:"o",emoji_order:"1851"},{name:"minidisc",unicode:"1f4bd",shortname:":minidisc:",code_decimal:"&#128189;",category:"o",emoji_order:"1852"},{name:"floppy_disk",unicode:"1f4be",shortname:":floppy_disk:",code_decimal:"&#128190;",category:"o",emoji_order:"1853"},{name:"cd",unicode:"1f4bf",shortname:":cd:",code_decimal:"&#128191;",category:"o",emoji_order:"1854"},{name:"dvd",unicode:"1f4c0",shortname:":dvd:",code_decimal:"&#128192;",category:"o",emoji_order:"1855"},{name:"movie_camera",unicode:"1f3a5",shortname:":movie_camera:",code_decimal:"&#127909;",category:"o",emoji_order:"1856"},{name:"film_frames",unicode:"1f39e",shortname:":film_frames:",code_decimal:"&#127902;",category:"o",emoji_order:"1857"},{name:"film_projector",unicode:"1f4fd",shortname:":projector:",code_decimal:"&#128253;",category:"o",emoji_order:"1858"},{name:"clapper",unicode:"1f3ac",shortname:":clapper:",code_decimal:"&#127916;",category:"a",emoji_order:"1859"},{name:"tv",unicode:"1f4fa",shortname:":tv:",code_decimal:"&#128250;",category:"o",emoji_order:"1860"},{name:"camera",unicode:"1f4f7",shortname:":camera:",code_decimal:"&#128247;",category:"o",emoji_order:"1861"},{name:"camera_with_flash",unicode:"1f4f8",shortname:":camera_with_flash:",code_decimal:"&#128248;",category:"o",emoji_order:"1862"},{name:"video_camera",unicode:"1f4f9",shortname:":video_camera:",code_decimal:"&#128249;",category:"o",emoji_order:"1863"},{name:"vhs",unicode:"1f4fc",shortname:":vhs:",code_decimal:"&#128252;",category:"o",emoji_order:"1864"},{name:"mag",unicode:"1f50d",shortname:":mag:",code_decimal:"&#128269;",category:"o",emoji_order:"1865"},{name:"mag_right",unicode:"1f50e",shortname:":mag_right:",code_decimal:"&#128270;",category:"o",emoji_order:"1866"},{name:"microscope",unicode:"1f52c",shortname:":microscope:",code_decimal:"&#128300;",category:"o",emoji_order:"1867"},{name:"telescope",unicode:"1f52d",shortname:":telescope:",code_decimal:"&#128301;",category:"o",emoji_order:"1868"},{name:"satellite_antenna",unicode:"1f4e1",shortname:":satellite:",code_decimal:"&#128225;",category:"o",emoji_order:"1869"},{name:"candle",unicode:"1f56f",shortname:":candle:",code_decimal:"&#128367;",category:"o",emoji_order:"1870"},{name:"bulb",unicode:"1f4a1",shortname:":bulb:",code_decimal:"&#128161;",category:"o",emoji_order:"1871"},{name:"flashlight",unicode:"1f526",shortname:":flashlight:",code_decimal:"&#128294;",category:"o",emoji_order:"1872"},{name:"izakaya_lantern",unicode:"1f3ee",shortname:":izakaya_lantern:",code_decimal:"&#127982;",category:"o",emoji_order:"1873"},{name:"notebook_with_decorative_cover",unicode:"1f4d4",shortname:":notebook_with_decorative_cover:",code_decimal:"&#128212;",category:"o",emoji_order:"1874"},{name:"closed_book",unicode:"1f4d5",shortname:":closed_book:",code_decimal:"&#128213;",category:"o",emoji_order:"1875"},{name:"book",unicode:"1f4d6",shortname:":book:",code_decimal:"&#128214;",category:"o",emoji_order:"1876"},{name:"green_book",unicode:"1f4d7",shortname:":green_book:",code_decimal:"&#128215;",category:"o",emoji_order:"1877"},{name:"blue_book",unicode:"1f4d8",shortname:":blue_book:",code_decimal:"&#128216;",category:"o",emoji_order:"1878"},{name:"orange_book",unicode:"1f4d9",shortname:":orange_book:",code_decimal:"&#128217;",category:"o",emoji_order:"1879"},{name:"books",unicode:"1f4da",shortname:":books:",code_decimal:"&#128218;",category:"o",emoji_order:"1880"},{name:"notebook",unicode:"1f4d3",shortname:":notebook:",code_decimal:"&#128211;",category:"o",emoji_order:"1881"},{name:"ledger",unicode:"1f4d2",shortname:":ledger:",code_decimal:"&#128210;",category:"o",emoji_order:"1882"},{name:"page_with_curl",unicode:"1f4c3",shortname:":page_with_curl:",code_decimal:"&#128195;",category:"o",emoji_order:"1883"},{name:"scroll",unicode:"1f4dc",shortname:":scroll:",code_decimal:"&#128220;",category:"o",emoji_order:"1884"},{name:"page_facing_up",unicode:"1f4c4",shortname:":page_facing_up:",code_decimal:"&#128196;",category:"o",emoji_order:"1885"},{name:"newspaper",unicode:"1f4f0",shortname:":newspaper:",code_decimal:"&#128240;",category:"o",emoji_order:"1886"},{name:"rolled_up_newspaper",unicode:"1f5de",shortname:":newspaper2:",code_decimal:"&#128478;",category:"o",emoji_order:"1887"},{name:"bookmark_tabs",unicode:"1f4d1",shortname:":bookmark_tabs:",code_decimal:"&#128209;",category:"o",emoji_order:"1888"},{name:"bookmark",unicode:"1f516",shortname:":bookmark:",code_decimal:"&#128278;",category:"o",emoji_order:"1889"},{name:"label",unicode:"1f3f7",shortname:":label:",code_decimal:"&#127991;",category:"o",emoji_order:"1890"},{name:"moneybag",unicode:"1f4b0",shortname:":moneybag:",code_decimal:"&#128176;",category:"o",emoji_order:"1891"},{name:"yen",unicode:"1f4b4",shortname:":yen:",code_decimal:"&#128180;",category:"o",emoji_order:"1892"},{name:"dollar",unicode:"1f4b5",shortname:":dollar:",code_decimal:"&#128181;",category:"o",emoji_order:"1893"},{name:"euro",unicode:"1f4b6",shortname:":euro:",code_decimal:"&#128182;",category:"o",emoji_order:"1894"},{name:"pound",unicode:"1f4b7",shortname:":pound:",code_decimal:"&#128183;",category:"o",emoji_order:"1895"},{name:"money_with_wings",unicode:"1f4b8",shortname:":money_with_wings:",code_decimal:"&#128184;",category:"o",emoji_order:"1896"},{name:"credit_card",unicode:"1f4b3",shortname:":credit_card:",code_decimal:"&#128179;",category:"o",emoji_order:"1897"},{name:"chart",unicode:"1f4b9",shortname:":chart:",code_decimal:"&#128185;",category:"s",emoji_order:"1898"},{name:"currency_exchange",unicode:"1f4b1",shortname:":currency_exchange:",code_decimal:"&#128177;",category:"s",emoji_order:"1899"},{name:"heavy_dollar_sign",unicode:"1f4b2",shortname:":heavy_dollar_sign:",code_decimal:"&#128178;",category:"s",emoji_order:"1900"},{name:"e-mail",unicode:"1f4e7",shortname:":e-mail:",code_decimal:"&#128231;",category:"o",emoji_order:"1902"},{name:"incoming_envelope",unicode:"1f4e8",shortname:":incoming_envelope:",code_decimal:"&#128232;",category:"o",emoji_order:"1903"},{name:"envelope_with_arrow",unicode:"1f4e9",shortname:":envelope_with_arrow:",code_decimal:"&#128233;",category:"o",emoji_order:"1904"},{name:"outbox_tray",unicode:"1f4e4",shortname:":outbox_tray:",code_decimal:"&#128228;",category:"o",emoji_order:"1905"},{name:"inbox_tray",unicode:"1f4e5",shortname:":inbox_tray:",code_decimal:"&#128229;",category:"o",emoji_order:"1906"},{name:"package",unicode:"1f4e6",shortname:":package:",code_decimal:"&#128230;",category:"o",emoji_order:"1907"},{name:"mailbox",unicode:"1f4eb",shortname:":mailbox:",code_decimal:"&#128235;",category:"o",emoji_order:"1908"},{name:"mailbox_closed",unicode:"1f4ea",shortname:":mailbox_closed:",code_decimal:"&#128234;",category:"o",emoji_order:"1909"},{name:"mailbox_with_mail",unicode:"1f4ec",shortname:":mailbox_with_mail:",code_decimal:"&#128236;",category:"o",emoji_order:"1910"},{name:"mailbox_with_no_mail",unicode:"1f4ed",shortname:":mailbox_with_no_mail:",code_decimal:"&#128237;",category:"o",emoji_order:"1911"},{name:"postbox",unicode:"1f4ee",shortname:":postbox:",code_decimal:"&#128238;",category:"o",emoji_order:"1912"},{name:"ballot_box_with_ballot",unicode:"1f5f3",shortname:":ballot_box:",code_decimal:"&#128499;",category:"o",emoji_order:"1913"},{name:"pencil2",unicode:"270f",shortname:":pencil2:",code_decimal:"&#9999;",category:"o",emoji_order:"1914"},{name:"black_nib",unicode:"2712",shortname:":black_nib:",code_decimal:"&#10002;",category:"o",emoji_order:"1915"},{name:"lower_left_fountain_pen",unicode:"1f58b",shortname:":pen_fountain:",code_decimal:"&#128395;",category:"o",emoji_order:"1916"},{name:"lower_left_ballpoint_pen",unicode:"1f58a",shortname:":pen_ballpoint:",code_decimal:"&#128394;",category:"o",emoji_order:"1917"},{name:"lower_left_paintbrush",unicode:"1f58c",shortname:":paintbrush:",code_decimal:"&#128396;",category:"o",emoji_order:"1918"},{name:"lower_left_crayon",unicode:"1f58d",shortname:":crayon:",code_decimal:"&#128397;",category:"o",emoji_order:"1919"},{name:"memo",unicode:"1f4dd",shortname:":pencil:",code_decimal:"&#128221;",category:"o",emoji_order:"1920"},{name:"briefcase",unicode:"1f4bc",shortname:":briefcase:",code_decimal:"&#128188;",category:"p",emoji_order:"1921"},{name:"file_folder",unicode:"1f4c1",shortname:":file_folder:",code_decimal:"&#128193;",category:"o",emoji_order:"1922"},{name:"open_file_folder",unicode:"1f4c2",shortname:":open_file_folder:",code_decimal:"&#128194;",category:"o",emoji_order:"1923"},{name:"card_index_dividers",unicode:"1f5c2",shortname:":dividers:",code_decimal:"&#128450;",category:"o",emoji_order:"1924"},{name:"date",unicode:"1f4c5",shortname:":date:",code_decimal:"&#128197;",category:"o",emoji_order:"1925"},{name:"calendar",unicode:"1f4c6",shortname:":calendar:",code_decimal:"&#128198;",category:"o",emoji_order:"1926"},{name:"spiral_note_pad",unicode:"1f5d2",shortname:":notepad_spiral:",code_decimal:"&#128466;",category:"o",emoji_order:"1927"},{name:"spiral_calendar_pad",unicode:"1f5d3",shortname:":calendar_spiral:",code_decimal:"&#128467;",category:"o",emoji_order:"1928"},{name:"card_index",unicode:"1f4c7",shortname:":card_index:",code_decimal:"&#128199;",category:"o",emoji_order:"1929"},{name:"chart_with_upwards_trend",unicode:"1f4c8",shortname:":chart_with_upwards_trend:",code_decimal:"&#128200;",category:"o",emoji_order:"1930"},{name:"chart_with_downwards_trend",unicode:"1f4c9",shortname:":chart_with_downwards_trend:",code_decimal:"&#128201;",category:"o",emoji_order:"1931"},{name:"bar_chart",unicode:"1f4ca",shortname:":bar_chart:",code_decimal:"&#128202;",category:"o",emoji_order:"1932"},{name:"clipboard",unicode:"1f4cb",shortname:":clipboard:",code_decimal:"&#128203;",category:"o",emoji_order:"1933"},{name:"pushpin",unicode:"1f4cc",shortname:":pushpin:",code_decimal:"&#128204;",category:"o",emoji_order:"1934"},{name:"round_pushpin",unicode:"1f4cd",shortname:":round_pushpin:",code_decimal:"&#128205;",category:"o",emoji_order:"1935"},{name:"paperclip",unicode:"1f4ce",shortname:":paperclip:",code_decimal:"&#128206;",category:"o",emoji_order:"1936"},{name:"linked_paperclips",unicode:"1f587",shortname:":paperclips:",code_decimal:"&#128391;",category:"o",emoji_order:"1937"},{name:"straight_ruler",unicode:"1f4cf",shortname:":straight_ruler:",code_decimal:"&#128207;",category:"o",emoji_order:"1938"},{name:"triangular_ruler",unicode:"1f4d0",shortname:":triangular_ruler:",code_decimal:"&#128208;",category:"o",emoji_order:"1939"},{name:"scissors",unicode:"2702",shortname:":scissors:",code_decimal:"&#9986;",category:"o",emoji_order:"1940"},{name:"card_file_box",unicode:"1f5c3",shortname:":card_box:",code_decimal:"&#128451;",category:"o",emoji_order:"1941"},{name:"file_cabinet",unicode:"1f5c4",shortname:":file_cabinet:",code_decimal:"&#128452;",category:"o",emoji_order:"1942"},{name:"wastebasket",unicode:"1f5d1",shortname:":wastebasket:",code_decimal:"&#128465;",category:"o",emoji_order:"1943"},{name:"lock",unicode:"1f512",shortname:":lock:",code_decimal:"&#128274;",category:"o",emoji_order:"1944"},{name:"unlock",unicode:"1f513",shortname:":unlock:",code_decimal:"&#128275;",category:"o",emoji_order:"1945"},{name:"lock_with_ink_pen",unicode:"1f50f",shortname:":lock_with_ink_pen:",code_decimal:"&#128271;",category:"o",emoji_order:"1946"},{name:"closed_lock_with_key",unicode:"1f510",shortname:":closed_lock_with_key:",code_decimal:"&#128272;",category:"o",emoji_order:"1947"},{name:"key",unicode:"1f511",shortname:":key:",code_decimal:"&#128273;",category:"o",emoji_order:"1948"},{name:"old_key",unicode:"1f5dd",shortname:":key2:",code_decimal:"&#128477;",category:"o",emoji_order:"1949"},{name:"hammer",unicode:"1f528",shortname:":hammer:",code_decimal:"&#128296;",category:"o",emoji_order:"1950"},{name:"pick",unicode:"26cf",shortname:":pick:",code_decimal:"&#9935;",category:"o",emoji_order:"1951"},{name:"hammer_and_pick",unicode:"2692",shortname:":hammer_pick:",code_decimal:"&#9874;",category:"o",emoji_order:"1952"},{name:"hammer_and_wrench",unicode:"1f6e0",shortname:":tools:",code_decimal:"&#128736;",category:"o",emoji_order:"1953"},{name:"dagger_knife",unicode:"1f5e1",shortname:":dagger:",code_decimal:"&#128481;",category:"o",emoji_order:"1954"},{name:"crossed_swords",unicode:"2694",shortname:":crossed_swords:",code_decimal:"&#9876;",category:"o",emoji_order:"1955"},{name:"gun",unicode:"1f52b",shortname:":gun:",code_decimal:"&#128299;",category:"o",emoji_order:"1956"},{name:"bow_and_arrow",unicode:"1f3f9",shortname:":bow_and_arrow:",code_decimal:"&#127993;",category:"a",emoji_order:"1957"},{name:"shield",unicode:"1f6e1",shortname:":shield:",code_decimal:"&#128737;",category:"o",emoji_order:"1958"},{name:"wrench",unicode:"1f527",shortname:":wrench:",code_decimal:"&#128295;",category:"o",emoji_order:"1959"},{name:"nut_and_bolt",unicode:"1f529",shortname:":nut_and_bolt:",code_decimal:"&#128297;",category:"o",emoji_order:"1960"},{name:"gear",unicode:"2699",shortname:":gear:",code_decimal:"&#9881;",category:"o",emoji_order:"1961"},{name:"compression",unicode:"1f5dc",shortname:":compression:",code_decimal:"&#128476;",category:"o",emoji_order:"1962"},{name:"alembic",unicode:"2697",shortname:":alembic:",code_decimal:"&#9879;",category:"o",emoji_order:"1963"},{name:"scales",unicode:"2696",shortname:":scales:",code_decimal:"&#9878;",category:"o",emoji_order:"1964"},{name:"link",unicode:"1f517",shortname:":link:",code_decimal:"&#128279;",category:"o",emoji_order:"1965"},{name:"chains",unicode:"26d3",shortname:":chains:",code_decimal:"&#9939;",category:"o",emoji_order:"1966"},{name:"syringe",unicode:"1f489",shortname:":syringe:",code_decimal:"&#128137;",category:"o",emoji_order:"1967"},{name:"pill",unicode:"1f48a",shortname:":pill:",code_decimal:"&#128138;",category:"o",emoji_order:"1968"},{name:"smoking",unicode:"1f6ac",shortname:":smoking:",code_decimal:"&#128684;",category:"o",emoji_order:"1969"},{name:"coffin",unicode:"26b0",shortname:":coffin:",code_decimal:"&#9904;",category:"o",emoji_order:"1970"},{name:"funeral_urn",unicode:"26b1",shortname:":urn:",code_decimal:"&#9905;",category:"o",emoji_order:"1971"},{name:"moyai",unicode:"1f5ff",shortname:":moyai:",code_decimal:"&#128511;",category:"o",emoji_order:"1972"},{name:"oil_drum",unicode:"1f6e2",shortname:":oil:",code_decimal:"&#128738;",category:"o",emoji_order:"1973"},{name:"crystal_ball",unicode:"1f52e",shortname:":crystal_ball:",code_decimal:"&#128302;",category:"o",emoji_order:"1974"},{name:"atm",unicode:"1f3e7",shortname:":atm:",code_decimal:"&#127975;",category:"s",emoji_order:"1976"},{name:"put_litter_in_its_place",unicode:"1f6ae",shortname:":put_litter_in_its_place:",code_decimal:"&#128686;",category:"s",emoji_order:"1977"},{name:"potable_water",unicode:"1f6b0",shortname:":potable_water:",code_decimal:"&#128688;",category:"s",emoji_order:"1978"},{name:"wheelchair",unicode:"267f",shortname:":wheelchair:",code_decimal:"&#9855;",category:"s",emoji_order:"1979"},{name:"mens",unicode:"1f6b9",shortname:":mens:",code_decimal:"&#128697;",category:"s",emoji_order:"1980"},{name:"womens",unicode:"1f6ba",shortname:":womens:",code_decimal:"&#128698;",category:"s",emoji_order:"1981"},{name:"restroom",unicode:"1f6bb",shortname:":restroom:",code_decimal:"&#128699;",category:"s",emoji_order:"1982"},{name:"baby_symbol",unicode:"1f6bc",shortname:":baby_symbol:",code_decimal:"&#128700;",category:"s",emoji_order:"1983"},{name:"wc",unicode:"1f6be",shortname:":wc:",code_decimal:"&#128702;",category:"s",emoji_order:"1984"},{name:"passport_control",unicode:"1f6c2",shortname:":passport_control:",code_decimal:"&#128706;",category:"s",emoji_order:"1985"},{name:"customs",unicode:"1f6c3",shortname:":customs:",code_decimal:"&#128707;",category:"s",emoji_order:"1986"},{name:"baggage_claim",unicode:"1f6c4",shortname:":baggage_claim:",code_decimal:"&#128708;",category:"s",emoji_order:"1987"},{name:"left_luggage",unicode:"1f6c5",shortname:":left_luggage:",code_decimal:"&#128709;",category:"s",emoji_order:"1988"},{name:"warning",unicode:"26a0",shortname:":warning:",code_decimal:"&#9888;",category:"s",emoji_order:"1989"},{name:"children_crossing",unicode:"1f6b8",shortname:":children_crossing:",code_decimal:"&#128696;",category:"s",emoji_order:"1990"},{name:"no_entry",unicode:"26d4",shortname:":no_entry:",code_decimal:"&#9940;",category:"s",emoji_order:"1991"},{name:"no_entry_sign",unicode:"1f6ab",shortname:":no_entry_sign:",code_decimal:"&#128683;",category:"s",emoji_order:"1992"},{name:"no_bicycles",unicode:"1f6b3",shortname:":no_bicycles:",code_decimal:"&#128691;",category:"s",emoji_order:"1993"},{name:"no_smoking",unicode:"1f6ad",shortname:":no_smoking:",code_decimal:"&#128685;",category:"s",emoji_order:"1994"},{name:"do_not_litter",unicode:"1f6af",shortname:":do_not_litter:",code_decimal:"&#128687;",category:"s",emoji_order:"1995"},{name:"non-potable_water",unicode:"1f6b1",shortname:":non-potable_water:",code_decimal:"&#128689;",category:"s",emoji_order:"1996"},{name:"no_pedestrians",unicode:"1f6b7",shortname:":no_pedestrians:",code_decimal:"&#128695;",category:"s",emoji_order:"1997"},{name:"no_mobile_phones",unicode:"1f4f5",shortname:":no_mobile_phones:",code_decimal:"&#128245;",category:"s",emoji_order:"1998"},{name:"underage",unicode:"1f51e",shortname:":underage:",code_decimal:"&#128286;",category:"s",emoji_order:"1999"},{name:"radioactive",unicode:"2622",shortname:":radioactive:",code_decimal:"&#9762;",category:"s",emoji_order:"2000"},{name:"biohazard",unicode:"2623",shortname:":biohazard:",code_decimal:"&#9763;",category:"s",emoji_order:"2001"},{name:"arrow_up",unicode:"2b06",shortname:":arrow_up:",code_decimal:"&#11014;",category:"s",emoji_order:"2002"},{name:"arrow_upper_right",unicode:"2197",shortname:":arrow_upper_right:",code_decimal:"&#8599;",category:"s",emoji_order:"2003"},{name:"arrow_right",unicode:"27a1",shortname:":arrow_right:",code_decimal:"&#10145;",category:"s",emoji_order:"2004"},{name:"arrow_lower_right",unicode:"2198",shortname:":arrow_lower_right:",code_decimal:"&#8600;",category:"s",emoji_order:"2005"},{name:"arrow_down",unicode:"2b07",shortname:":arrow_down:",code_decimal:"&#11015;",category:"s",emoji_order:"2006"},{name:"arrow_lower_left",unicode:"2199",shortname:":arrow_lower_left:",code_decimal:"&#8601;",category:"s",emoji_order:"2007"},{name:"arrow_left",unicode:"2b05",shortname:":arrow_left:",code_decimal:"&#11013;",category:"s",emoji_order:"2008"},{name:"arrow_upper_left",unicode:"2196",shortname:":arrow_upper_left:",code_decimal:"&#8598;",category:"s",emoji_order:"2009"},{name:"arrow_up_down",unicode:"2195",shortname:":arrow_up_down:",code_decimal:"&#8597;",category:"s",emoji_order:"2010"},{name:"left_right_arrow",unicode:"2194",shortname:":left_right_arrow:",code_decimal:"&harr;",category:"s",emoji_order:"2011"},{name:"leftwards_arrow_with_hook",unicode:"21a9",shortname:":leftwards_arrow_with_hook:",code_decimal:"&#8617;",category:"s",emoji_order:"2012"},{name:"arrow_right_hook",unicode:"21aa",shortname:":arrow_right_hook:",code_decimal:"&#8618;",category:"s",emoji_order:"2013"},{name:"arrow_heading_up",unicode:"2934",shortname:":arrow_heading_up:",code_decimal:"&#10548;",category:"s",emoji_order:"2014"},{name:"arrow_heading_down",unicode:"2935",shortname:":arrow_heading_down:",code_decimal:"&#10549;",category:"s",emoji_order:"2015"},{name:"arrows_clockwise",unicode:"1f503",shortname:":arrows_clockwise:",code_decimal:"&#128259;",category:"s",emoji_order:"2016"},{name:"arrows_counterclockwise",unicode:"1f504",shortname:":arrows_counterclockwise:",code_decimal:"&#128260;",category:"s",emoji_order:"2017"},{name:"back",unicode:"1f519",shortname:":back:",code_decimal:"&#128281;",category:"s",emoji_order:"2018"},{name:"end",unicode:"1f51a",shortname:":end:",code_decimal:"&#128282;",category:"s",emoji_order:"2019"},{name:"on",unicode:"1f51b",shortname:":on:",code_decimal:"&#128283;",category:"s",emoji_order:"2020"},{name:"soon",unicode:"1f51c",shortname:":soon:",code_decimal:"&#128284;",category:"s",emoji_order:"2021"},{name:"top",unicode:"1f51d",shortname:":top:",code_decimal:"&#128285;",category:"s",emoji_order:"2022"},{name:"place_of_worship",unicode:"1f6d0",shortname:":place_of_worship:",code_decimal:"&#128720;",category:"s",emoji_order:"2023"},{name:"atom_symbol",unicode:"269b",shortname:":atom:",code_decimal:"&#9883;",category:"s",emoji_order:"2024"},{name:"om_symbol",unicode:"1f549",shortname:":om_symbol:",code_decimal:"&#128329;",category:"s",emoji_order:"2025"},{name:"star_of_david",unicode:"2721",shortname:":star_of_david:",code_decimal:"&#10017;",category:"s",emoji_order:"2026"},{name:"wheel_of_dharma",unicode:"2638",shortname:":wheel_of_dharma:",code_decimal:"&#9784;",category:"s",emoji_order:"2027"},{name:"yin_yang",unicode:"262f",shortname:":yin_yang:",code_decimal:"&#9775;",category:"s",emoji_order:"2028"},{name:"latin_cross",unicode:"271d",shortname:":cross:",code_decimal:"&#10013;",category:"s",emoji_order:"2029"},{name:"orthodox_cross",unicode:"2626",shortname:":orthodox_cross:",code_decimal:"&#9766;",category:"s",emoji_order:"2030"},{name:"star_and_crescent",unicode:"262a",shortname:":star_and_crescent:",code_decimal:"&#9770;",category:"s",emoji_order:"2031"},{name:"peace_symbol",unicode:"262e",shortname:":peace:",code_decimal:"&#9774;",category:"s",emoji_order:"2032"},{name:"menorah_with_nine_branches",unicode:"1f54e",shortname:":menorah:",code_decimal:"&#128334;",category:"s",emoji_order:"2033"},{name:"six_pointed_star",unicode:"1f52f",shortname:":six_pointed_star:",code_decimal:"&#128303;",category:"s",emoji_order:"2034"},{name:"aries",unicode:"2648",shortname:":aries:",code_decimal:"&#9800;",category:"s",emoji_order:"2035"},{name:"taurus",unicode:"2649",shortname:":taurus:",code_decimal:"&#9801;",category:"s",emoji_order:"2036"},{name:"gemini",unicode:"264a",shortname:":gemini:",code_decimal:"&#9802;",category:"s",emoji_order:"2037"},{name:"cancer",unicode:"264b",shortname:":cancer:",code_decimal:"&#9803;",category:"s",emoji_order:"2038"},{name:"leo",unicode:"264c",shortname:":leo:",code_decimal:"&#9804;",category:"s",emoji_order:"2039"},{name:"virgo",unicode:"264d",shortname:":virgo:",code_decimal:"&#9805;",category:"s",emoji_order:"2040"},{name:"libra",unicode:"264e",shortname:":libra:",code_decimal:"&#9806;",category:"s",emoji_order:"2041"},{name:"scorpius",unicode:"264f",shortname:":scorpius:",code_decimal:"&#9807;",category:"s",emoji_order:"2042"},{name:"sagittarius",unicode:"2650",shortname:":sagittarius:",code_decimal:"&#9808;",category:"s",emoji_order:"2043"},{name:"capricorn",unicode:"2651",shortname:":capricorn:",code_decimal:"&#9809;",category:"s",emoji_order:"2044"},{name:"aquarius",unicode:"2652",shortname:":aquarius:",code_decimal:"&#9810;",category:"s",emoji_order:"2045"},{name:"pisces",unicode:"2653",shortname:":pisces:",code_decimal:"&#9811;",category:"s",emoji_order:"2046"},{name:"ophiuchus",unicode:"26ce",shortname:":ophiuchus:",code_decimal:"&#9934;",category:"s",emoji_order:"2047"},{name:"twisted_rightwards_arrows",unicode:"1f500",shortname:":twisted_rightwards_arrows:",code_decimal:"&#128256;",category:"s",emoji_order:"2048"},{name:"repeat",unicode:"1f501",shortname:":repeat:",code_decimal:"&#128257;",category:"s",emoji_order:"2049"},{name:"repeat_one",unicode:"1f502",shortname:":repeat_one:",code_decimal:"&#128258;",category:"s",emoji_order:"2050"},{name:"arrow_forward",unicode:"25b6",shortname:":arrow_forward:",code_decimal:"&#9654;",category:"s",emoji_order:"2051"},{name:"fast_forward",unicode:"23e9",shortname:":fast_forward:",code_decimal:"&#9193;",category:"s",emoji_order:"2052"},{name:"black_right_pointing_double_triangle_with_vertical_bar",unicode:"23ed",shortname:":track_next:",code_decimal:"&#9197;",category:"s",emoji_order:"2053"},{name:"black_right_pointing_triangle_with_double_vertical_bar",unicode:"23ef",shortname:":play_pause:",code_decimal:"&#9199;",category:"s",emoji_order:"2054"},{name:"arrow_backward",unicode:"25c0",shortname:":arrow_backward:",code_decimal:"&#9664;",category:"s",emoji_order:"2055"},{name:"rewind",unicode:"23ea",shortname:":rewind:",code_decimal:"&#9194;",category:"s",emoji_order:"2056"},{name:"black_left_pointing_double_triangle_with_vertical_bar",unicode:"23ee",shortname:":track_previous:",code_decimal:"&#9198;",category:"s",emoji_order:"2057"},{name:"arrow_up_small",unicode:"1f53c",shortname:":arrow_up_small:",code_decimal:"&#128316;",category:"s",emoji_order:"2058"},{name:"arrow_double_up",unicode:"23eb",shortname:":arrow_double_up:",code_decimal:"&#9195;",category:"s",emoji_order:"2059"},{name:"arrow_down_small",unicode:"1f53d",shortname:":arrow_down_small:",code_decimal:"&#128317;",category:"s",emoji_order:"2060"},{name:"arrow_double_down",unicode:"23ec",shortname:":arrow_double_down:",code_decimal:"&#9196;",category:"s",emoji_order:"2061"},{name:"double_vertical_bar",unicode:"23f8",shortname:":pause_button:",code_decimal:"&#9208;",category:"s",emoji_order:"2062"},{name:"black_square_for_stop",unicode:"23f9",shortname:":stop_button:",code_decimal:"&#9209;",category:"s",emoji_order:"2063"},{name:"black_circle_for_record",unicode:"23fa",shortname:":record_button:",code_decimal:"&#9210;",category:"s",emoji_order:"2064"},{name:"cinema",unicode:"1f3a6",shortname:":cinema:",code_decimal:"&#127910;",category:"s",emoji_order:"2066"},{name:"low_brightness",unicode:"1f505",shortname:":low_brightness:",code_decimal:"&#128261;",category:"s",emoji_order:"2067"},{name:"high_brightness",unicode:"1f506",shortname:":high_brightness:",code_decimal:"&#128262;",category:"s",emoji_order:"2068"},{name:"signal_strength",unicode:"1f4f6",shortname:":signal_strength:",code_decimal:"&#128246;",category:"s",emoji_order:"2069"},{name:"vibration_mode",unicode:"1f4f3",shortname:":vibration_mode:",code_decimal:"&#128243;",category:"s",emoji_order:"2070"},{name:"mobile_phone_off",unicode:"1f4f4",shortname:":mobile_phone_off:",code_decimal:"&#128244;",category:"s",emoji_order:"2071"},{name:"recycle",unicode:"267b",shortname:":recycle:",code_decimal:"&#9851;",category:"s",emoji_order:"2072"},{name:"name_badge",unicode:"1f4db",shortname:":name_badge:",code_decimal:"&#128219;",category:"s",emoji_order:"2073"},{name:"fleur_de_lis",unicode:"269c",shortname:":fleur-de-lis:",code_decimal:"&#9884;",category:"s",emoji_order:"2074"},{name:"beginner",unicode:"1f530",shortname:":beginner:",code_decimal:"&#128304;",category:"s",emoji_order:"2075"},{name:"trident",unicode:"1f531",shortname:":trident:",code_decimal:"&#128305;",category:"s",emoji_order:"2076"},{name:"o",unicode:"2b55",shortname:":o:",code_decimal:"&#11093;",category:"s",emoji_order:"2077"},{name:"white_check_mark",unicode:"2705",shortname:":white_check_mark:",code_decimal:"&#9989;",category:"s",emoji_order:"2078"},{name:"ballot_box_with_check",unicode:"2611",shortname:":ballot_box_with_check:",code_decimal:"&#9745;",category:"s",emoji_order:"2079"},{name:"heavy_check_mark",unicode:"2714",shortname:":heavy_check_mark:",code_decimal:"&#10004;",category:"s",emoji_order:"2080"},{name:"heavy_multiplication_x",unicode:"2716",shortname:":heavy_multiplication_x:",code_decimal:"&#10006;",category:"s",emoji_order:"2081"},{name:"x",unicode:"274c",shortname:":x:",code_decimal:"&#10060;",category:"s",emoji_order:"2082"},{name:"negative_squared_cross_mark",unicode:"274e",shortname:":negative_squared_cross_mark:",code_decimal:"&#10062;",category:"s",emoji_order:"2083"},{name:"heavy_plus_sign",unicode:"2795",shortname:":heavy_plus_sign:",code_decimal:"&#10133;",category:"s",emoji_order:"2084"},{name:"heavy_minus_sign",unicode:"2796",shortname:":heavy_minus_sign:",code_decimal:"&#10134;",category:"s",emoji_order:"2088"},{name:"heavy_division_sign",unicode:"2797",shortname:":heavy_division_sign:",code_decimal:"&#10135;",category:"s",emoji_order:"2089"},{name:"curly_loop",unicode:"27b0",shortname:":curly_loop:",code_decimal:"&#10160;",category:"s",emoji_order:"2090"},{name:"loop",unicode:"27bf",shortname:":loop:",code_decimal:"&#10175;",category:"s",emoji_order:"2091"},{name:"part_alternation_mark",unicode:"303d",shortname:":part_alternation_mark:",code_decimal:"&#12349;",category:"s",emoji_order:"2092"},{name:"eight_spoked_asterisk",unicode:"2733",shortname:":eight_spoked_asterisk:",code_decimal:"&#10035;",category:"s",emoji_order:"2093"},{name:"eight_pointed_black_star",unicode:"2734",shortname:":eight_pointed_black_star:",code_decimal:"&#10036;",category:"s",emoji_order:"2094"},{name:"sparkle",unicode:"2747",shortname:":sparkle:",code_decimal:"&#10055;",category:"s",emoji_order:"2095"},{name:"bangbang",unicode:"203c",shortname:":bangbang:",code_decimal:"&#8252;",category:"s",emoji_order:"2096"},{name:"interrobang",unicode:"2049",shortname:":interrobang:",code_decimal:"&#8265;",category:"s",emoji_order:"2097"},{name:"question",unicode:"2753",shortname:":question:",code_decimal:"&#10067;",category:"s",emoji_order:"2098"},{name:"grey_question",unicode:"2754",shortname:":grey_question:",code_decimal:"&#10068;",category:"s",emoji_order:"2099"},{name:"grey_exclamation",unicode:"2755",shortname:":grey_exclamation:",code_decimal:"&#10069;",category:"s",emoji_order:"2100"},{name:"exclamation",unicode:"2757",shortname:":exclamation:",code_decimal:"&#10071;",category:"s",emoji_order:"2101"},{name:"wavy_dash",unicode:"3030",shortname:":wavy_dash:",code_decimal:"&#12336;",category:"s",emoji_order:"2102"},{name:"copyright",unicode:"00a9",shortname:":copyright:",code_decimal:"&copy;",category:"s",emoji_order:"2103"},{name:"registered",unicode:"00ae",shortname:":registered:",code_decimal:"&reg;",category:"s",emoji_order:"2104"},{name:"tm",unicode:"2122",shortname:":tm:",code_decimal:"&trade;",category:"s",emoji_order:"2105"},{name:"hash",unicode:"0023-20e3",shortname:":hash:",code_decimal:"#&#8419;",category:"s",emoji_order:"2106"},{name:"keycap_star",unicode:"002a-20e3",shortname:":asterisk:",code_decimal:"*&#8419;",category:"s",emoji_order:"2107"},{name:"zero",unicode:"0030-20e3",shortname:":zero:",code_decimal:"0&#8419;",category:"s",emoji_order:"2108"},{name:"one",unicode:"0031-20e3",shortname:":one:",code_decimal:"1&#8419;",category:"s",emoji_order:"2109"},{name:"two",unicode:"0032-20e3",shortname:":two:",code_decimal:"2&#8419;",category:"s",emoji_order:"2110"},{name:"three",unicode:"0033-20e3",shortname:":three:",code_decimal:"3&#8419;",category:"s",emoji_order:"2111"},{name:"four",unicode:"0034-20e3",shortname:":four:",code_decimal:"4&#8419;",category:"s",emoji_order:"2112"},{name:"five",unicode:"0035-20e3",shortname:":five:",code_decimal:"5&#8419;",category:"s",emoji_order:"2113"},{name:"six",unicode:"0036-20e3",shortname:":six:",code_decimal:"6&#8419;",category:"s",emoji_order:"2114"},{name:"seven",unicode:"0037-20e3",shortname:":seven:",code_decimal:"7&#8419;",category:"s",emoji_order:"2115"},{name:"eight",unicode:"0038-20e3",shortname:":eight:",code_decimal:"8&#8419;",category:"s",emoji_order:"2116"},{name:"nine",unicode:"0039-20e3",shortname:":nine:",code_decimal:"9&#8419;",category:"s",emoji_order:"2117"},{name:"keycap_ten",unicode:"1f51f",shortname:":keycap_ten:",code_decimal:"&#128287;",category:"s",emoji_order:"2118"},{name:"capital_abcd",unicode:"1f520",shortname:":capital_abcd:",code_decimal:"&#128288;",category:"s",emoji_order:"2120"},{name:"abcd",unicode:"1f521",shortname:":abcd:",code_decimal:"&#128289;",category:"s",emoji_order:"2121"},{name:"s",unicode:"1f523",shortname:":s:",code_decimal:"&#128291;",category:"s",emoji_order:"2123"},{name:"abc",unicode:"1f524",shortname:":abc:",code_decimal:"&#128292;",category:"s",emoji_order:"2124"},{name:"a",unicode:"1f170",shortname:":a:",code_decimal:"&#127344;",category:"s",emoji_order:"2125"},{name:"ab",unicode:"1f18e",shortname:":ab:",code_decimal:"&#127374;",category:"s",emoji_order:"2126"},{name:"b",unicode:"1f171",shortname:":b:",code_decimal:"&#127345;",category:"s",emoji_order:"2127"},{name:"cl",unicode:"1f191",shortname:":cl:",code_decimal:"&#127377;",category:"s",emoji_order:"2128"},{name:"cool",unicode:"1f192",shortname:":cool:",code_decimal:"&#127378;",category:"s",emoji_order:"2129"},{name:"free",unicode:"1f193",shortname:":free:",code_decimal:"&#127379;",category:"s",emoji_order:"2130"},{name:"information_source",unicode:"2139",shortname:":information_source:",code_decimal:"&#8505;",category:"s",emoji_order:"2131"},{name:"id",unicode:"1f194",shortname:":id:",code_decimal:"&#127380;",category:"s",emoji_order:"2132"},{name:"m",unicode:"24c2",shortname:":m:",code_decimal:"&#9410;",category:"s",emoji_order:"2133"},{name:"new",unicode:"1f195",shortname:":new:",code_decimal:"&#127381;",category:"s",emoji_order:"2134"},{name:"ng",unicode:"1f196",shortname:":ng:",code_decimal:"&#127382;",category:"s",emoji_order:"2135"},{name:"o2",unicode:"1f17e",shortname:":o2:",code_decimal:"&#127358;",category:"s",emoji_order:"2136"},{name:"ok",unicode:"1f197",shortname:":ok:",code_decimal:"&#127383;",category:"s",emoji_order:"2137"},{name:"parking",unicode:"1f17f",shortname:":parking:",code_decimal:"&#127359;",category:"s",emoji_order:"2138"},{name:"sos",unicode:"1f198",shortname:":sos:",code_decimal:"&#127384;",category:"s",emoji_order:"2139"},{name:"up",unicode:"1f199",shortname:":up:",code_decimal:"&#127385;",category:"s",emoji_order:"2140"},{name:"vs",unicode:"1f19a",shortname:":vs:",code_decimal:"&#127386;",category:"s",emoji_order:"2141"},{name:"koko",unicode:"1f201",shortname:":koko:",code_decimal:"&#127489;",category:"s",emoji_order:"2142"},{name:"sa",unicode:"1f202",shortname:":sa:",code_decimal:"&#127490;",category:"s",emoji_order:"2143"},{name:"u6708",unicode:"1f237",shortname:":u6708:",code_decimal:"&#127543;",category:"s",emoji_order:"2144"},{name:"u6709",unicode:"1f236",shortname:":u6709:",code_decimal:"&#127542;",category:"s",emoji_order:"2145"},{name:"u6307",unicode:"1f22f",shortname:":u6307:",code_decimal:"&#127535;",category:"s",emoji_order:"2146"},{name:"ideograph_advantage",unicode:"1f250",shortname:":ideograph_advantage:",code_decimal:"&#127568;",category:"s",emoji_order:"2147"},{name:"u5272",unicode:"1f239",shortname:":u5272:",code_decimal:"&#127545;",category:"s",emoji_order:"2148"},{name:"u7121",unicode:"1f21a",shortname:":u7121:",code_decimal:"&#127514;",category:"s",emoji_order:"2149"},{name:"u7981",unicode:"1f232",shortname:":u7981:",code_decimal:"&#127538;",category:"s",emoji_order:"2150"},{name:"accept",unicode:"1f251",shortname:":accept:",code_decimal:"&#127569;",category:"s",emoji_order:"2151"},{name:"u7533",unicode:"1f238",shortname:":u7533:",code_decimal:"&#127544;",category:"s",emoji_order:"2152"},{name:"u5408",unicode:"1f234",shortname:":u5408:",code_decimal:"&#127540;",category:"s",emoji_order:"2153"},{name:"u7a7a",unicode:"1f233",shortname:":u7a7a:",code_decimal:"&#127539;",category:"s",emoji_order:"2154"},{name:"congratulations",unicode:"3297",shortname:":congratulations:",code_decimal:"&#12951;",category:"s",emoji_order:"2155"},{name:"secret",unicode:"3299",shortname:":secret:",code_decimal:"&#12953;",category:"s",emoji_order:"2156"},{name:"u55b6",unicode:"1f23a",shortname:":u55b6:",code_decimal:"&#127546;",category:"s",emoji_order:"2157"},{name:"u6e80",unicode:"1f235",shortname:":u6e80:",code_decimal:"&#127541;",category:"s",emoji_order:"2158"},{name:"black_small_square",unicode:"25aa",shortname:":black_small_square:",code_decimal:"&#9642;",category:"s",emoji_order:"2159"},{name:"white_small_square",unicode:"25ab",shortname:":white_small_square:",code_decimal:"&#9643;",category:"s",emoji_order:"2160"},{name:"white_medium_square",unicode:"25fb",shortname:":white_medium_square:",code_decimal:"&#9723;",category:"s",emoji_order:"2161"},{name:"black_medium_square",unicode:"25fc",shortname:":black_medium_square:",code_decimal:"&#9724;",category:"s",emoji_order:"2162"},{name:"white_medium_small_square",unicode:"25fd",shortname:":white_medium_small_square:",code_decimal:"&#9725;",category:"s",emoji_order:"2163"},{name:"black_medium_small_square",unicode:"25fe",shortname:":black_medium_small_square:",code_decimal:"&#9726;",category:"s",emoji_order:"2164"},{name:"black_large_square",unicode:"2b1b",shortname:":black_large_square:",code_decimal:"&#11035;",category:"s",emoji_order:"2165"},{name:"white_large_square",unicode:"2b1c",shortname:":white_large_square:",code_decimal:"&#11036;",category:"s",emoji_order:"2166"},{name:"large_orange_diamond",unicode:"1f536",shortname:":large_orange_diamond:",code_decimal:"&#128310;",category:"s",emoji_order:"2167"},{name:"large_blue_diamond",unicode:"1f537",shortname:":large_blue_diamond:",code_decimal:"&#128311;",category:"s",emoji_order:"2168"},{name:"small_orange_diamond",unicode:"1f538",shortname:":small_orange_diamond:",code_decimal:"&#128312;",category:"s",emoji_order:"2169"},{name:"small_blue_diamond",unicode:"1f539",shortname:":small_blue_diamond:",code_decimal:"&#128313;",category:"s",emoji_order:"2170"},{name:"small_red_triangle",unicode:"1f53a",shortname:":small_red_triangle:",code_decimal:"&#128314;",category:"s",emoji_order:"2171"},{name:"small_red_triangle_down",unicode:"1f53b",shortname:":small_red_triangle_down:",code_decimal:"&#128315;",category:"s",emoji_order:"2172"},{name:"diamond_shape_with_a_dot_inside",unicode:"1f4a0",shortname:":diamond_shape_with_a_dot_inside:",code_decimal:"&#128160;",category:"s",emoji_order:"2173"},{name:"radio_button",unicode:"1f518",shortname:":radio_button:",code_decimal:"&#128280;",category:"s",emoji_order:"2174"},{name:"black_square_button",unicode:"1f532",shortname:":black_square_button:",code_decimal:"&#128306;",category:"s",emoji_order:"2175"},{name:"white_square_button",unicode:"1f533",shortname:":white_square_button:",code_decimal:"&#128307;",category:"s",emoji_order:"2176"},{name:"white_circle",unicode:"26aa",shortname:":white_circle:",code_decimal:"&#9898;",category:"s",emoji_order:"2177"},{name:"black_circle",unicode:"26ab",shortname:":black_circle:",code_decimal:"&#9899;",category:"s",emoji_order:"2178"},{name:"red_circle",unicode:"1f534",shortname:":red_circle:",code_decimal:"&#128308;",category:"s",emoji_order:"2179"},{name:"large_blue_circle",unicode:"1f535",shortname:":blue_circle:",code_decimal:"&#128309;",category:"s",emoji_order:"2180"},{name:"checkered_flag",unicode:"1f3c1",shortname:":checkered_flag:",code_decimal:"&#127937;",category:"t",emoji_order:"2181"},{name:"triangular_flag_on_post",unicode:"1f6a9",shortname:":triangular_flag_on_post:",code_decimal:"&#128681;",category:"o",emoji_order:"2182"},{name:"crossed_flags",unicode:"1f38c",shortname:":crossed_flags:",code_decimal:"&#127884;",category:"o",emoji_order:"2183"},{name:"waving_black_flag",unicode:"1f3f4",shortname:":flag_black:",code_decimal:"&#127988;",category:"o",emoji_order:"2184"},{name:"waving_white_flag",unicode:"1f3f3",shortname:":flag_white:",code_decimal:"&#127987;",category:"o",emoji_order:"2185"},{name:"flag-ac",unicode:"1f1e6-1f1e8",shortname:":flag_ac:",code_decimal:"&#127462;&#127464;",category:"f",emoji_order:"2187"},{name:"flag-ad",unicode:"1f1e6-1f1e9",shortname:":flag_ad:",code_decimal:"&#127462;&#127465;",category:"f",emoji_order:"2188"},{name:"flag-ae",unicode:"1f1e6-1f1ea",shortname:":flag_ae:",code_decimal:"&#127462;&#127466;",category:"f",emoji_order:"2189"},{name:"flag-af",unicode:"1f1e6-1f1eb",shortname:":flag_af:",code_decimal:"&#127462;&#127467;",category:"f",emoji_order:"2190"},{name:"flag-ag",unicode:"1f1e6-1f1ec",shortname:":flag_ag:",code_decimal:"&#127462;&#127468;",category:"f",emoji_order:"2191"},{name:"flag-ai",unicode:"1f1e6-1f1ee",shortname:":flag_ai:",code_decimal:"&#127462;&#127470;",category:"f",emoji_order:"2192"},{name:"flag-al",unicode:"1f1e6-1f1f1",shortname:":flag_al:",code_decimal:"&#127462;&#127473;",category:"f",emoji_order:"2193"},{name:"flag-am",unicode:"1f1e6-1f1f2",shortname:":flag_am:",code_decimal:"&#127462;&#127474;",category:"f",emoji_order:"2194"},{name:"flag-ao",unicode:"1f1e6-1f1f4",shortname:":flag-ao:",code_decimal:"&#127462;&#127476;",category:"f",emoji_order:"2195"},{name:"flag-aq",unicode:"1f1e6-1f1f6",shortname:":flag-aq:",code_decimal:"&#127462;&#127478;",category:"f",emoji_order:"2196"},{name:"flag-ar",unicode:"1f1e6-1f1f7",shortname:":flag-ar:",code_decimal:"&#127462;&#127479;",category:"f",emoji_order:"2197"},{name:"flag-as",unicode:"1f1e6-1f1f8",shortname:":flag-as:",code_decimal:"&#127462;&#127480;",category:"f",emoji_order:"2198"},{name:"flag-at",unicode:"1f1e6-1f1f9",shortname:":flag-at:",code_decimal:"&#127462;&#127481;",category:"f",emoji_order:"2199"},{name:"flag-au",unicode:"1f1e6-1f1fa",shortname:":flag-au:",code_decimal:"&#127462;&#127482;",category:"f",emoji_order:"2200"},{name:"flag-aw",unicode:"1f1e6-1f1fc",shortname:":flag-aw:",code_decimal:"&#127462;&#127484;",category:"f",emoji_order:"2201"},{name:"flag-ax",unicode:"1f1e6-1f1fd",shortname:":flag-ax:",code_decimal:"&#127462;&#127485;",category:"f",emoji_order:"2202"},{name:"flag-az",unicode:"1f1e6-1f1ff",shortname:":flag-az:",code_decimal:"&#127462;&#127487;",category:"f",emoji_order:"2203"},{name:"flag-ba",unicode:"1f1e7-1f1e6",shortname:":flag-ba:",code_decimal:"&#127463;&#127462;",category:"f",emoji_order:"2204"},{name:"flag-bb",unicode:"1f1e7-1f1e7",shortname:":flag-bb:",code_decimal:"&#127463;&#127463;",category:"f",emoji_order:"2205"},{name:"flag-bd",unicode:"1f1e7-1f1e9",shortname:":flag-bd:",code_decimal:"&#127463;&#127465;",category:"f",emoji_order:"2206"},{name:"flag-be",unicode:"1f1e7-1f1ea",shortname:":flag-be:",code_decimal:"&#127463;&#127466;",category:"f",emoji_order:"2207"},{name:"flag-bf",unicode:"1f1e7-1f1eb",shortname:":flag-bf:",code_decimal:"&#127463;&#127467;",category:"f",emoji_order:"2208"},{name:"flag-bg",unicode:"1f1e7-1f1ec",shortname:":flag-bg:",code_decimal:"&#127463;&#127468;",category:"f",emoji_order:"2209"},{name:"flag-bh",unicode:"1f1e7-1f1ed",shortname:":flag-bh:",code_decimal:"&#127463;&#127469;",category:"f",emoji_order:"2210"},{name:"flag-bi",unicode:"1f1e7-1f1ee",shortname:":flag-bi:",code_decimal:"&#127463;&#127470;",category:"f",emoji_order:"2211"},{name:"flag-bj",unicode:"1f1e7-1f1ef",shortname:":flag-bj:",code_decimal:"&#127463;&#127471;",category:"f",emoji_order:"2212"},{name:"flag-bl",unicode:"1f1e7-1f1f1",shortname:":flag-bl:",code_decimal:"&#127463;&#127473;",category:"f",emoji_order:"2213"},{name:"flag-bm",unicode:"1f1e7-1f1f2",shortname:":flag-bm:",code_decimal:"&#127463;&#127474;",category:"f",emoji_order:"2214"},{name:"flag-bn",unicode:"1f1e7-1f1f3",shortname:":flag-bn:",code_decimal:"&#127463;&#127475;",category:"f",emoji_order:"2215"},{name:"flag-bo",unicode:"1f1e7-1f1f4",shortname:":flag-bo:",code_decimal:"&#127463;&#127476;",category:"f",emoji_order:"2216"},{name:"flag-bq",unicode:"1f1e7-1f1f6",shortname:":flag-bq:",code_decimal:"&#127463;&#127478;",category:"f",emoji_order:"2217"},{name:"flag-br",unicode:"1f1e7-1f1f7",shortname:":flag-br:",code_decimal:"&#127463;&#127479;",category:"f",emoji_order:"2218"},{name:"flag-bs",unicode:"1f1e7-1f1f8",shortname:":flag-bs:",code_decimal:"&#127463;&#127480;",category:"f",emoji_order:"2219"},{name:"flag-bt",unicode:"1f1e7-1f1f9",shortname:":flag-bt:",code_decimal:"&#127463;&#127481;",category:"f",emoji_order:"2220"},{name:"flag-bv",unicode:"1f1e7-1f1fb",shortname:":flag-bv:",code_decimal:"&#127463;&#127483;",category:"f",emoji_order:"2221"},{name:"flag-bw",unicode:"1f1e7-1f1fc",shortname:":flag-bw:",code_decimal:"&#127463;&#127484;",category:"f",emoji_order:"2222"},{name:"flag-by",unicode:"1f1e7-1f1fe",shortname:":flag-by:",code_decimal:"&#127463;&#127486;",category:"f",emoji_order:"2223"},{name:"flag-bz",unicode:"1f1e7-1f1ff",shortname:":flag-bz:",code_decimal:"&#127463;&#127487;",category:"f",emoji_order:"2224"},{name:"flag-ca",unicode:"1f1e8-1f1e6",shortname:":flag-ca:",code_decimal:"&#127464;&#127462;",category:"f",emoji_order:"2225"},{name:"flag-cc",unicode:"1f1e8-1f1e8",shortname:":flag-cc:",code_decimal:"&#127464;&#127464;",category:"f",emoji_order:"2226"},{name:"flag-cd",unicode:"1f1e8-1f1e9",shortname:":flag-cd:",code_decimal:"&#127464;&#127465;",category:"f",emoji_order:"2227"},{name:"flag-cf",unicode:"1f1e8-1f1eb",shortname:":flag-cf:",code_decimal:"&#127464;&#127467;",category:"f",emoji_order:"2228"},{name:"flag-cg",unicode:"1f1e8-1f1ec",shortname:":flag-cg:",code_decimal:"&#127464;&#127468;",category:"f",emoji_order:"2229"},{name:"flag-ch",unicode:"1f1e8-1f1ed",shortname:":flag-ch:",code_decimal:"&#127464;&#127469;",category:"f",emoji_order:"2230"},{name:"flag-ci",unicode:"1f1e8-1f1ee",shortname:":flag-ci:",code_decimal:"&#127464;&#127470;",category:"f",emoji_order:"2231"},{name:"flag-ck",unicode:"1f1e8-1f1f0",shortname:":flag-ck:",code_decimal:"&#127464;&#127472;",category:"f",emoji_order:"2232"},{name:"flag-cl",unicode:"1f1e8-1f1f1",shortname:":flag-cl:",code_decimal:"&#127464;&#127473;",category:"f",emoji_order:"2233"},{name:"flag-cm",unicode:"1f1e8-1f1f2",shortname:":flag-cm:",code_decimal:"&#127464;&#127474;",category:"f",emoji_order:"2234"},{name:"flag-cn",unicode:"1f1e8-1f1f3",shortname:":flag-cn:",code_decimal:"&#127464;&#127475;",category:"f",emoji_order:"2235"},{name:"flag-co",unicode:"1f1e8-1f1f4",shortname:":flag-co:",code_decimal:"&#127464;&#127476;",category:"f",emoji_order:"2236"},{name:"flag-cp",unicode:"1f1e8-1f1f5",shortname:":flag-cp:",code_decimal:"&#127464;&#127477;",category:"f",emoji_order:"2237"},{name:"flag-cr",unicode:"1f1e8-1f1f7",shortname:":flag-cr:",code_decimal:"&#127464;&#127479;",category:"f",emoji_order:"2238"},{name:"flag-cu",unicode:"1f1e8-1f1fa",shortname:":flag-cu:",code_decimal:"&#127464;&#127482;",category:"f",emoji_order:"2239"},{name:"flag-cv",unicode:"1f1e8-1f1fb",shortname:":flag-cv:",code_decimal:"&#127464;&#127483;",category:"f",emoji_order:"2240"},{name:"flag-cw",unicode:"1f1e8-1f1fc",shortname:":flag-cw:",code_decimal:"&#127464;&#127484;",category:"f",emoji_order:"2241"},{name:"flag-cx",unicode:"1f1e8-1f1fd",shortname:":flag-cx:",code_decimal:"&#127464;&#127485;",category:"f",emoji_order:"2242"},{name:"flag-cy",unicode:"1f1e8-1f1fe",shortname:":flag-cy:",code_decimal:"&#127464;&#127486;",category:"f",emoji_order:"2243"},{name:"flag-cz",unicode:"1f1e8-1f1ff",shortname:":flag-cz:",code_decimal:"&#127464;&#127487;",category:"f",emoji_order:"2244"},{name:"flag-de",unicode:"1f1e9-1f1ea",shortname:":flag-de:",code_decimal:"&#127465;&#127466;",category:"f",emoji_order:"2245"},{name:"flag-dg",unicode:"1f1e9-1f1ec",shortname:":flag-dg:",code_decimal:"&#127465;&#127468;",category:"f",emoji_order:"2246"},{name:"flag-dj",unicode:"1f1e9-1f1ef",shortname:":flag-dj:",code_decimal:"&#127465;&#127471;",category:"f",emoji_order:"2247"},{name:"flag-dk",unicode:"1f1e9-1f1f0",shortname:":flag-dk:",code_decimal:"&#127465;&#127472;",category:"f",emoji_order:"2248"},{name:"flag-dm",unicode:"1f1e9-1f1f2",shortname:":flag-dm:",code_decimal:"&#127465;&#127474;",category:"f",emoji_order:"2249"},{name:"flag-do",unicode:"1f1e9-1f1f4",shortname:":flag-do:",code_decimal:"&#127465;&#127476;",category:"f",emoji_order:"2250"},{name:"flag-dz",unicode:"1f1e9-1f1ff",shortname:":flag-dz:",code_decimal:"&#127465;&#127487;",category:"f",emoji_order:"2251"},{name:"flag-ea",unicode:"1f1ea-1f1e6",shortname:":flag-ea:",code_decimal:"&#127466;&#127462;",category:"f",emoji_order:"2252"},{name:"flag-ec",unicode:"1f1ea-1f1e8",shortname:":flag-ec:",code_decimal:"&#127466;&#127464;",category:"f",emoji_order:"2253"},{name:"flag-ee",unicode:"1f1ea-1f1ea",shortname:":flag-ee:",code_decimal:"&#127466;&#127466;",category:"f",emoji_order:"2254"},{name:"flag-eg",unicode:"1f1ea-1f1ec",shortname:":flag-eg:",code_decimal:"&#127466;&#127468;",category:"f",emoji_order:"2255"},{name:"flag-eh",unicode:"1f1ea-1f1ed",shortname:":flag-eh:",code_decimal:"&#127466;&#127469;",category:"f",emoji_order:"2256"},{name:"flag-er",unicode:"1f1ea-1f1f7",shortname:":flag-er:",code_decimal:"&#127466;&#127479;",category:"f",emoji_order:"2257"},{name:"flag-es",unicode:"1f1ea-1f1f8",shortname:":flag-es:",code_decimal:"&#127466;&#127480;",category:"f",emoji_order:"2258"},{name:"flag-et",unicode:"1f1ea-1f1f9",shortname:":flag-et:",code_decimal:"&#127466;&#127481;",category:"f",emoji_order:"2259"},{name:"flag-eu",unicode:"1f1ea-1f1fa",shortname:":flag-eu:",code_decimal:"&#127466;&#127482;",category:"f",emoji_order:"2260"},{name:"flag-fi",unicode:"1f1eb-1f1ee",shortname:":flag-fi:",code_decimal:"&#127467;&#127470;",category:"f",emoji_order:"2261"},{name:"flag-fj",unicode:"1f1eb-1f1ef",shortname:":flag-fj:",code_decimal:"&#127467;&#127471;",category:"f",emoji_order:"2262"},{name:"flag-fk",unicode:"1f1eb-1f1f0",shortname:":flag-fk:",code_decimal:"&#127467;&#127472;",category:"f",emoji_order:"2263"},{name:"flag-fm",unicode:"1f1eb-1f1f2",shortname:":flag-fm:",code_decimal:"&#127467;&#127474;",category:"f",emoji_order:"2264"},{name:"flag-fo",unicode:"1f1eb-1f1f4",shortname:":flag-fo:",code_decimal:"&#127467;&#127476;",category:"f",emoji_order:"2265"},{name:"flag-fr",unicode:"1f1eb-1f1f7",shortname:":flag-fr:",code_decimal:"&#127467;&#127479;",category:"f",emoji_order:"2266"},{name:"flag-ga",unicode:"1f1ec-1f1e6",shortname:":flag-ga:",code_decimal:"&#127468;&#127462;",category:"f",emoji_order:"2267"},{name:"flag-gb",unicode:"1f1ec-1f1e7",shortname:":flag-gb:",code_decimal:"&#127468;&#127463;",category:"f",emoji_order:"2268"},{name:"flag-gd",unicode:"1f1ec-1f1e9",shortname:":flag-gd:",code_decimal:"&#127468;&#127465;",category:"f",emoji_order:"2269"},{name:"flag-ge",unicode:"1f1ec-1f1ea",shortname:":flag-ge:",code_decimal:"&#127468;&#127466;",category:"f",emoji_order:"2270"},{name:"flag-gf",unicode:"1f1ec-1f1eb",shortname:":flag-gf:",code_decimal:"&#127468;&#127467;",category:"f",emoji_order:"2271"},{name:"flag-gg",unicode:"1f1ec-1f1ec",shortname:":flag-gg:",code_decimal:"&#127468;&#127468;",category:"f",emoji_order:"2272"},{name:"flag-gh",unicode:"1f1ec-1f1ed",shortname:":flag-gh:",code_decimal:"&#127468;&#127469;",category:"f",emoji_order:"2273"},{name:"flag-gi",unicode:"1f1ec-1f1ee",shortname:":flag-gi:",code_decimal:"&#127468;&#127470;",category:"f",emoji_order:"2274"},{name:"flag-gl",unicode:"1f1ec-1f1f1",shortname:":flag-gl:",code_decimal:"&#127468;&#127473;",category:"f",emoji_order:"2275"},{name:"flag-gm",unicode:"1f1ec-1f1f2",shortname:":flag-gm:",code_decimal:"&#127468;&#127474;",category:"f",emoji_order:"2276"},{name:"flag-gn",unicode:"1f1ec-1f1f3",shortname:":flag-gn:",code_decimal:"&#127468;&#127475;",category:"f",emoji_order:"2277"},{name:"flag-gp",unicode:"1f1ec-1f1f5",shortname:":flag-gp:",code_decimal:"&#127468;&#127477;",category:"f",emoji_order:"2278"},{name:"flag-gq",unicode:"1f1ec-1f1f6",shortname:":flag-gq:",code_decimal:"&#127468;&#127478;",category:"f",emoji_order:"2279"},{name:"flag-gr",unicode:"1f1ec-1f1f7",shortname:":flag-gr:",code_decimal:"&#127468;&#127479;",category:"f",emoji_order:"2280"},{name:"flag-gs",unicode:"1f1ec-1f1f8",shortname:":flag-gs:",code_decimal:"&#127468;&#127480;",category:"f",emoji_order:"2281"},{name:"flag-gt",unicode:"1f1ec-1f1f9",shortname:":flag-gt:",code_decimal:"&#127468;&#127481;",category:"f",emoji_order:"2282"},{name:"flag-gu",unicode:"1f1ec-1f1fa",shortname:":flag-gu:",code_decimal:"&#127468;&#127482;",category:"f",emoji_order:"2283"},{name:"flag-gw",unicode:"1f1ec-1f1fc",shortname:":flag-gw:",code_decimal:"&#127468;&#127484;",category:"f",emoji_order:"2284"},{name:"flag-gy",unicode:"1f1ec-1f1fe",shortname:":flag-gy:",code_decimal:"&#127468;&#127486;",category:"f",emoji_order:"2285"},{name:"flag-hk",unicode:"1f1ed-1f1f0",shortname:":flag-hk:",code_decimal:"&#127469;&#127472;",category:"f",emoji_order:"2286"},{name:"flag-hm",unicode:"1f1ed-1f1f2",shortname:":flag-hm:",code_decimal:"&#127469;&#127474;",category:"f",emoji_order:"2287"},{name:"flag-hn",unicode:"1f1ed-1f1f3",shortname:":flag-hn:",code_decimal:"&#127469;&#127475;",category:"f",emoji_order:"2288"},{name:"flag-hr",unicode:"1f1ed-1f1f7",shortname:":flag-hr:",code_decimal:"&#127469;&#127479;",category:"f",emoji_order:"2289"},{name:"flag-ht",unicode:"1f1ed-1f1f9",shortname:":flag-ht:",code_decimal:"&#127469;&#127481;",category:"f",emoji_order:"2290"},{name:"flag-hu",unicode:"1f1ed-1f1fa",shortname:":flag-hu:",code_decimal:"&#127469;&#127482;",category:"f",emoji_order:"2291"},{name:"flag-ic",unicode:"1f1ee-1f1e8",shortname:":flag-ic:",code_decimal:"&#127470;&#127464;",category:"f",emoji_order:"2292"},{name:"flag-id",unicode:"1f1ee-1f1e9",shortname:":flag-id:",code_decimal:"&#127470;&#127465;",category:"f",emoji_order:"2293"},{name:"flag-ie",unicode:"1f1ee-1f1ea",shortname:":flag-ie:",code_decimal:"&#127470;&#127466;",category:"f",emoji_order:"2294"},{name:"flag-il",unicode:"1f1ee-1f1f1",shortname:":flag-il:",code_decimal:"&#127470;&#127473;",category:"f",emoji_order:"2295"},{name:"flag-im",unicode:"1f1ee-1f1f2",shortname:":flag-im:",code_decimal:"&#127470;&#127474;",category:"f",emoji_order:"2296"},{name:"flag-in",unicode:"1f1ee-1f1f3",shortname:":flag-in:",code_decimal:"&#127470;&#127475;",category:"f",emoji_order:"2297"},{name:"flag-io",unicode:"1f1ee-1f1f4",shortname:":flag-io:",code_decimal:"&#127470;&#127476;",category:"f",emoji_order:"2298"},{name:"flag-iq",unicode:"1f1ee-1f1f6",shortname:":flag-iq:",code_decimal:"&#127470;&#127478;",category:"f",emoji_order:"2299"},{name:"flag-ir",unicode:"1f1ee-1f1f7",shortname:":flag-ir:",code_decimal:"&#127470;&#127479;",category:"f",emoji_order:"2300"},{name:"flag-is",unicode:"1f1ee-1f1f8",shortname:":flag-is:",code_decimal:"&#127470;&#127480;",category:"f",emoji_order:"2301"},{name:"flag-it",unicode:"1f1ee-1f1f9",shortname:":flag-it:",code_decimal:"&#127470;&#127481;",category:"f",emoji_order:"2302"},{name:"flag-je",unicode:"1f1ef-1f1ea",shortname:":flag-je:",code_decimal:"&#127471;&#127466;",category:"f",emoji_order:"2303"},{name:"flag-jm",unicode:"1f1ef-1f1f2",shortname:":flag-jm:",code_decimal:"&#127471;&#127474;",category:"f",emoji_order:"2304"},{name:"flag-jo",unicode:"1f1ef-1f1f4",shortname:":flag-jo:",code_decimal:"&#127471;&#127476;",category:"f",emoji_order:"2305"},{name:"flag-jp",unicode:"1f1ef-1f1f5",shortname:":flag-jp:",code_decimal:"&#127471;&#127477;",category:"f",emoji_order:"2306"},{name:"flag-ke",unicode:"1f1f0-1f1ea",shortname:":flag-ke:",code_decimal:"&#127472;&#127466;",category:"f",emoji_order:"2307"},{name:"flag-kg",unicode:"1f1f0-1f1ec",shortname:":flag-kg:",code_decimal:"&#127472;&#127468;",category:"f",emoji_order:"2308"},{name:"flag-kh",unicode:"1f1f0-1f1ed",shortname:":flag-kh:",code_decimal:"&#127472;&#127469;",category:"f",emoji_order:"2309"},{name:"flag-ki",unicode:"1f1f0-1f1ee",shortname:":flag-ki:",code_decimal:"&#127472;&#127470;",category:"f",emoji_order:"2310"},{name:"flag-km",unicode:"1f1f0-1f1f2",shortname:":flag-km:",code_decimal:"&#127472;&#127474;",category:"f",emoji_order:"2311"},{name:"flag-kn",unicode:"1f1f0-1f1f3",shortname:":flag-kn:",code_decimal:"&#127472;&#127475;",category:"f",emoji_order:"2312"},{name:"flag-kp",unicode:"1f1f0-1f1f5",shortname:":flag-kp:",code_decimal:"&#127472;&#127477;",category:"f",emoji_order:"2313"},{name:"flag-kr",unicode:"1f1f0-1f1f7",shortname:":flag-kr:",code_decimal:"&#127472;&#127479;",category:"f",emoji_order:"2314"},{name:"flag-kw",unicode:"1f1f0-1f1fc",shortname:":flag-kw:",code_decimal:"&#127472;&#127484;",category:"f",emoji_order:"2315"},{name:"flag-ky",unicode:"1f1f0-1f1fe",shortname:":flag-ky:",code_decimal:"&#127472;&#127486;",category:"f",emoji_order:"2316"},{name:"flag-kz",unicode:"1f1f0-1f1ff",shortname:":flag-kz:",code_decimal:"&#127472;&#127487;",category:"f",emoji_order:"2317"},{name:"flag-la",unicode:"1f1f1-1f1e6",shortname:":flag-la:",code_decimal:"&#127473;&#127462;",category:"f",emoji_order:"2318"},{name:"flag-lb",unicode:"1f1f1-1f1e7",shortname:":flag-lb:",code_decimal:"&#127473;&#127463;",category:"f",emoji_order:"2319"},{name:"flag-lc",unicode:"1f1f1-1f1e8",shortname:":flag-lc:",code_decimal:"&#127473;&#127464;",category:"f",emoji_order:"2320"},{name:"flag-li",unicode:"1f1f1-1f1ee",shortname:":flag-li:",code_decimal:"&#127473;&#127470;",category:"f",emoji_order:"2321"},{name:"flag-lk",unicode:"1f1f1-1f1f0",shortname:":flag-lk:",code_decimal:"&#127473;&#127472;",category:"f",emoji_order:"2322"},{name:"flag-lr",unicode:"1f1f1-1f1f7",shortname:":flag-lr:",code_decimal:"&#127473;&#127479;",category:"f",emoji_order:"2323"},{name:"flag-ls",unicode:"1f1f1-1f1f8",shortname:":flag-ls:",code_decimal:"&#127473;&#127480;",category:"f",emoji_order:"2324"},{name:"flag-lt",unicode:"1f1f1-1f1f9",shortname:":flag-lt:",code_decimal:"&#127473;&#127481;",category:"f",emoji_order:"2325"},{name:"flag-lu",unicode:"1f1f1-1f1fa",shortname:":flag-lu:",code_decimal:"&#127473;&#127482;",category:"f",emoji_order:"2326"},{name:"flag-lv",unicode:"1f1f1-1f1fb",shortname:":flag-lv:",code_decimal:"&#127473;&#127483;",category:"f",emoji_order:"2327"},{name:"flag-ly",unicode:"1f1f1-1f1fe",shortname:":flag-ly:",code_decimal:"&#127473;&#127486;",category:"f",emoji_order:"2328"},{name:"flag-ma",unicode:"1f1f2-1f1e6",shortname:":flag-ma:",code_decimal:"&#127474;&#127462;",category:"f",emoji_order:"2329"},{name:"flag-mc",unicode:"1f1f2-1f1e8",shortname:":flag-mc:",code_decimal:"&#127474;&#127464;",category:"f",emoji_order:"2330"},{name:"flag-md",unicode:"1f1f2-1f1e9",shortname:":flag-md:",code_decimal:"&#127474;&#127465;",category:"f",emoji_order:"2331"},{name:"flag-me",unicode:"1f1f2-1f1ea",shortname:":flag-me:",code_decimal:"&#127474;&#127466;",category:"f",emoji_order:"2332"},{name:"flag-mf",unicode:"1f1f2-1f1eb",shortname:":flag-mf:",code_decimal:"&#127474;&#127467;",category:"f",emoji_order:"2333"},{name:"flag-mg",unicode:"1f1f2-1f1ec",shortname:":flag-mg:",code_decimal:"&#127474;&#127468;",category:"f",emoji_order:"2334"},{name:"flag-mh",unicode:"1f1f2-1f1ed",shortname:":flag-mh:",code_decimal:"&#127474;&#127469;",category:"f",emoji_order:"2335"},{name:"flag-mk",unicode:"1f1f2-1f1f0",shortname:":flag-mk:",code_decimal:"&#127474;&#127472;",category:"f",emoji_order:"2336"},{name:"flag-ml",unicode:"1f1f2-1f1f1",shortname:":flag-ml:",code_decimal:"&#127474;&#127473;",category:"f",emoji_order:"2337"},{name:"flag-mm",unicode:"1f1f2-1f1f2",shortname:":flag-mm:",code_decimal:"&#127474;&#127474;",category:"f",emoji_order:"2338"},{name:"flag-mn",unicode:"1f1f2-1f1f3",shortname:":flag-mn:",code_decimal:"&#127474;&#127475;",category:"f",emoji_order:"2339"},{name:"flag-mo",unicode:"1f1f2-1f1f4",shortname:":flag-mo:",code_decimal:"&#127474;&#127476;",category:"f",emoji_order:"2340"},{name:"flag-mp",unicode:"1f1f2-1f1f5",shortname:":flag-mp:",code_decimal:"&#127474;&#127477;",category:"f",emoji_order:"2341"},{name:"flag-mq",unicode:"1f1f2-1f1f6",shortname:":flag-mq:",code_decimal:"&#127474;&#127478;",category:"f",emoji_order:"2342"},{name:"flag-mr",unicode:"1f1f2-1f1f7",shortname:":flag-mr:",code_decimal:"&#127474;&#127479;",category:"f",emoji_order:"2343"},{name:"flag-ms",unicode:"1f1f2-1f1f8",shortname:":flag-ms:",code_decimal:"&#127474;&#127480;",category:"f",emoji_order:"2344"},{name:"flag-mt",unicode:"1f1f2-1f1f9",shortname:":flag-mt:",code_decimal:"&#127474;&#127481;",category:"f",emoji_order:"2345"},{name:"flag-mu",unicode:"1f1f2-1f1fa",shortname:":flag-mu:",code_decimal:"&#127474;&#127482;",category:"f",emoji_order:"2346"},{name:"flag-mv",unicode:"1f1f2-1f1fb",shortname:":flag-mv:",code_decimal:"&#127474;&#127483;",category:"f",emoji_order:"2347"},{name:"flag-mw",unicode:"1f1f2-1f1fc",shortname:":flag-mw:",code_decimal:"&#127474;&#127484;",category:"f",emoji_order:"2348"},{name:"flag-mx",unicode:"1f1f2-1f1fd",shortname:":flag-mx:",code_decimal:"&#127474;&#127485;",category:"f",emoji_order:"2349"},{name:"flag-my",unicode:"1f1f2-1f1fe",shortname:":flag-my:",code_decimal:"&#127474;&#127486;",category:"f",emoji_order:"2350"},{name:"flag-mz",unicode:"1f1f2-1f1ff",shortname:":flag-mz:",code_decimal:"&#127474;&#127487;",category:"f",emoji_order:"2351"},{name:"flag-na",unicode:"1f1f3-1f1e6",shortname:":flag-na:",code_decimal:"&#127475;&#127462;",category:"f",emoji_order:"2352"},{name:"flag-nc",unicode:"1f1f3-1f1e8",shortname:":flag-nc:",code_decimal:"&#127475;&#127464;",category:"f",emoji_order:"2353"},{name:"flag-ne",unicode:"1f1f3-1f1ea",shortname:":flag-ne:",code_decimal:"&#127475;&#127466;",category:"f",emoji_order:"2354"},{name:"flag-nf",unicode:"1f1f3-1f1eb",shortname:":flag-nf:",code_decimal:"&#127475;&#127467;",category:"f",emoji_order:"2355"},{name:"flag-ng",unicode:"1f1f3-1f1ec",shortname:":flag-ng:",code_decimal:"&#127475;&#127468;",category:"f",emoji_order:"2356"},{name:"flag-ni",unicode:"1f1f3-1f1ee",shortname:":flag-ni:",code_decimal:"&#127475;&#127470;",category:"f",emoji_order:"2357"},{name:"flag-nl",unicode:"1f1f3-1f1f1",shortname:":flag-nl:",code_decimal:"&#127475;&#127473;",category:"f",emoji_order:"2358"},{name:"flag-no",unicode:"1f1f3-1f1f4",shortname:":flag-no:",code_decimal:"&#127475;&#127476;",category:"f",emoji_order:"2359"},{name:"flag-np",unicode:"1f1f3-1f1f5",shortname:":flag-np:",code_decimal:"&#127475;&#127477;",category:"f",emoji_order:"2360"},{name:"flag-nr",unicode:"1f1f3-1f1f7",shortname:":flag-nr:",code_decimal:"&#127475;&#127479;",category:"f",emoji_order:"2361"},{name:"flag-nu",unicode:"1f1f3-1f1fa",shortname:":flag-nu:",code_decimal:"&#127475;&#127482;",category:"f",emoji_order:"2362"},{name:"flag-nz",unicode:"1f1f3-1f1ff",shortname:":flag-nz:",code_decimal:"&#127475;&#127487;",category:"f",emoji_order:"2363"},{name:"flag-om",unicode:"1f1f4-1f1f2",shortname:":flag-om:",code_decimal:"&#127476;&#127474;",category:"f",emoji_order:"2364"},{name:"flag-pa",unicode:"1f1f5-1f1e6",shortname:":flag-pa:",code_decimal:"&#127477;&#127462;",category:"f",emoji_order:"2365"},{name:"flag-pe",unicode:"1f1f5-1f1ea",shortname:":flag-pe:",code_decimal:"&#127477;&#127466;",category:"f",emoji_order:"2366"},{name:"flag-pf",unicode:"1f1f5-1f1eb",shortname:":flag-pf:",code_decimal:"&#127477;&#127467;",category:"f",emoji_order:"2367"},{name:"flag-pg",unicode:"1f1f5-1f1ec",shortname:":flag-pg:",code_decimal:"&#127477;&#127468;",category:"f",emoji_order:"2368"},{name:"flag-ph",unicode:"1f1f5-1f1ed",shortname:":flag-ph:",code_decimal:"&#127477;&#127469;",category:"f",emoji_order:"2369"},{name:"flag-pk",unicode:"1f1f5-1f1f0",shortname:":flag-pk:",code_decimal:"&#127477;&#127472;",category:"f",emoji_order:"2370"},{name:"flag-pl",unicode:"1f1f5-1f1f1",shortname:":flag-pl:",code_decimal:"&#127477;&#127473;",category:"f",emoji_order:"2371"},{name:"flag-pm",unicode:"1f1f5-1f1f2",shortname:":flag-pm:",code_decimal:"&#127477;&#127474;",category:"f",emoji_order:"2372"},{name:"flag-pn",unicode:"1f1f5-1f1f3",shortname:":flag-pn:",code_decimal:"&#127477;&#127475;",category:"f",emoji_order:"2373"},{name:"flag-pr",unicode:"1f1f5-1f1f7",shortname:":flag-pr:",code_decimal:"&#127477;&#127479;",category:"f",emoji_order:"2374"},{name:"flag-ps",unicode:"1f1f5-1f1f8",shortname:":flag-ps:",code_decimal:"&#127477;&#127480;",category:"f",emoji_order:"2375"},{name:"flag-pt",unicode:"1f1f5-1f1f9",shortname:":flag-pt:",code_decimal:"&#127477;&#127481;",category:"f",emoji_order:"2376"},{name:"flag-pw",unicode:"1f1f5-1f1fc",shortname:":flag-pw:",code_decimal:"&#127477;&#127484;",category:"f",emoji_order:"2377"},{name:"flag-py",unicode:"1f1f5-1f1fe",shortname:":flag-py:",code_decimal:"&#127477;&#127486;",category:"f",emoji_order:"2378"},{name:"flag-qa",unicode:"1f1f6-1f1e6",shortname:":flag-qa:",code_decimal:"&#127478;&#127462;",category:"f",emoji_order:"2379"},{name:"flag-re",unicode:"1f1f7-1f1ea",shortname:":flag-re:",code_decimal:"&#127479;&#127466;",category:"f",emoji_order:"2380"},{name:"flag-ro",unicode:"1f1f7-1f1f4",shortname:":flag-ro:",code_decimal:"&#127479;&#127476;",category:"f",emoji_order:"2381"},{name:"flag-rs",unicode:"1f1f7-1f1f8",shortname:":flag-rs:",code_decimal:"&#127479;&#127480;",category:"f",emoji_order:"2382"},{name:"flag-ru",unicode:"1f1f7-1f1fa",shortname:":flag-ru:",code_decimal:"&#127479;&#127482;",category:"f",emoji_order:"2383"},{name:"flag-rw",unicode:"1f1f7-1f1fc",shortname:":flag-rw:",code_decimal:"&#127479;&#127484;",category:"f",emoji_order:"2384"},{name:"flag-sa",unicode:"1f1f8-1f1e6",shortname:":flag-sa:",code_decimal:"&#127480;&#127462;",category:"f",emoji_order:"2385"},{name:"flag-sb",unicode:"1f1f8-1f1e7",shortname:":flag-sb:",code_decimal:"&#127480;&#127463;",category:"f",emoji_order:"2386"},{name:"flag-sc",unicode:"1f1f8-1f1e8",shortname:":flag-sc:",code_decimal:"&#127480;&#127464;",category:"f",emoji_order:"2387"},{name:"flag-sd",unicode:"1f1f8-1f1e9",shortname:":flag-sd:",code_decimal:"&#127480;&#127465;",category:"f",emoji_order:"2388"},{name:"flag-se",unicode:"1f1f8-1f1ea",shortname:":flag-se:",code_decimal:"&#127480;&#127466;",category:"f",emoji_order:"2389"},{name:"flag-sg",unicode:"1f1f8-1f1ec",shortname:":flag-sg:",code_decimal:"&#127480;&#127468;",category:"f",emoji_order:"2390"},{name:"flag-sh",unicode:"1f1f8-1f1ed",shortname:":flag-sh:",code_decimal:"&#127480;&#127469;",category:"f",emoji_order:"2391"},{name:"flag-si",unicode:"1f1f8-1f1ee",shortname:":flag-si:",code_decimal:"&#127480;&#127470;",category:"f",emoji_order:"2392"},{name:"flag-sj",unicode:"1f1f8-1f1ef",shortname:":flag-sj:",code_decimal:"&#127480;&#127471;",category:"f",emoji_order:"2393"},{name:"flag-sk",unicode:"1f1f8-1f1f0",shortname:":flag-sk:",code_decimal:"&#127480;&#127472;",category:"f",emoji_order:"2394"},{name:"flag-sl",unicode:"1f1f8-1f1f1",shortname:":flag-sl:",code_decimal:"&#127480;&#127473;",category:"f",emoji_order:"2395"},{name:"flag-sm",unicode:"1f1f8-1f1f2",shortname:":flag-sm:",code_decimal:"&#127480;&#127474;",category:"f",emoji_order:"2396"},{name:"flag-sn",unicode:"1f1f8-1f1f3",shortname:":flag-sn:",code_decimal:"&#127480;&#127475;",category:"f",emoji_order:"2397"},{name:"flag-so",unicode:"1f1f8-1f1f4",shortname:":flag-so:",code_decimal:"&#127480;&#127476;",category:"f",emoji_order:"2398"},{name:"flag-sr",unicode:"1f1f8-1f1f7",shortname:":flag-sr:",code_decimal:"&#127480;&#127479;",category:"f",emoji_order:"2399"},{name:"flag-ss",unicode:"1f1f8-1f1f8",shortname:":flag-ss:",code_decimal:"&#127480;&#127480;",category:"f",emoji_order:"2400"},{name:"flag-st",unicode:"1f1f8-1f1f9",shortname:":flag-st:",code_decimal:"&#127480;&#127481;",category:"f",emoji_order:"2401"},{name:"flag-sv",unicode:"1f1f8-1f1fb",shortname:":flag-sv:",code_decimal:"&#127480;&#127483;",category:"f",emoji_order:"2402"},{name:"flag-sx",unicode:"1f1f8-1f1fd",shortname:":flag-sx:",code_decimal:"&#127480;&#127485;",category:"f",emoji_order:"2403"},{name:"flag-sy",unicode:"1f1f8-1f1fe",shortname:":flag-sy:",code_decimal:"&#127480;&#127486;",category:"f",emoji_order:"2404"},{name:"flag-sz",unicode:"1f1f8-1f1ff",shortname:":flag-sz:",code_decimal:"&#127480;&#127487;",category:"f",emoji_order:"2405"},{name:"flag-ta",unicode:"1f1f9-1f1e6",shortname:":flag-ta:",code_decimal:"&#127481;&#127462;",category:"f",emoji_order:"2406"},{name:"flag-tc",unicode:"1f1f9-1f1e8",shortname:":flag-tc:",code_decimal:"&#127481;&#127464;",category:"f",emoji_order:"2407"},{name:"flag-td",unicode:"1f1f9-1f1e9",shortname:":flag-td:",code_decimal:"&#127481;&#127465;",category:"f",emoji_order:"2408"},{name:"flag-tf",unicode:"1f1f9-1f1eb",shortname:":flag-tf:",code_decimal:"&#127481;&#127467;",category:"f",emoji_order:"2409"},{name:"flag-tg",unicode:"1f1f9-1f1ec",shortname:":flag-tg:",code_decimal:"&#127481;&#127468;",category:"f",emoji_order:"2410"},{name:"flag-th",unicode:"1f1f9-1f1ed",shortname:":flag-th:",code_decimal:"&#127481;&#127469;",category:"f",emoji_order:"2411"},{name:"flag-tj",unicode:"1f1f9-1f1ef",shortname:":flag-tj:",code_decimal:"&#127481;&#127471;",category:"f",emoji_order:"2412"},{name:"flag-tk",unicode:"1f1f9-1f1f0",shortname:":flag-tk:",code_decimal:"&#127481;&#127472;",category:"f",emoji_order:"2413"},{name:"flag-tl",unicode:"1f1f9-1f1f1",shortname:":flag-tl:",code_decimal:"&#127481;&#127473;",category:"f",emoji_order:"2414"},{name:"flag-tm",unicode:"1f1f9-1f1f2",shortname:":flag-tm:",code_decimal:"&#127481;&#127474;",category:"f",emoji_order:"2415"},{name:"flag-tn",unicode:"1f1f9-1f1f3",shortname:":flag-tn:",code_decimal:"&#127481;&#127475;",category:"f",emoji_order:"2416"},{name:"flag-to",unicode:"1f1f9-1f1f4",shortname:":flag-to:",code_decimal:"&#127481;&#127476;",category:"f",emoji_order:"2417"},{name:"flag-tr",unicode:"1f1f9-1f1f7",shortname:":flag-tr:",code_decimal:"&#127481;&#127479;",category:"f",emoji_order:"2418"},{name:"flag-tt",unicode:"1f1f9-1f1f9",shortname:":flag-tt:",code_decimal:"&#127481;&#127481;",category:"f",emoji_order:"2419"},{name:"flag-tv",unicode:"1f1f9-1f1fb",shortname:":flag-tv:",code_decimal:"&#127481;&#127483;",category:"f",emoji_order:"2420"},{name:"flag-tw",unicode:"1f1f9-1f1fc",shortname:":flag-tw:",code_decimal:"&#127481;&#127484;",category:"f",emoji_order:"2421"},{name:"flag-tz",unicode:"1f1f9-1f1ff",shortname:":flag-tz:",code_decimal:"&#127481;&#127487;",category:"f",emoji_order:"2422"},{name:"flag-ua",unicode:"1f1fa-1f1e6",shortname:":flag-ua:",code_decimal:"&#127482;&#127462;",category:"f",emoji_order:"2423"},{name:"flag-ug",unicode:"1f1fa-1f1ec",shortname:":flag-ug:",code_decimal:"&#127482;&#127468;",category:"f",emoji_order:"2424"},{name:"flag-um",unicode:"1f1fa-1f1f2",shortname:":flag-um:",code_decimal:"&#127482;&#127474;",category:"f",emoji_order:"2425"},{name:"flag-us",unicode:"1f1fa-1f1f8",shortname:":flag-us:",code_decimal:"&#127482;&#127480;",category:"f",emoji_order:"2427"},{name:"flag-uy",unicode:"1f1fa-1f1fe",shortname:":flag-uy:",code_decimal:"&#127482;&#127486;",category:"f",emoji_order:"2428"},{name:"flag-uz",unicode:"1f1fa-1f1ff",shortname:":flag-uz:",code_decimal:"&#127482;&#127487;",category:"f",emoji_order:"2429"},{name:"flag-va",unicode:"1f1fb-1f1e6",shortname:":flag-va:",code_decimal:"&#127483;&#127462;",category:"f",emoji_order:"2430"},{name:"flag-vc",unicode:"1f1fb-1f1e8",shortname:":flag-vc:",code_decimal:"&#127483;&#127464;",category:"f",emoji_order:"2431"},{name:"flag-ve",unicode:"1f1fb-1f1ea",shortname:":flag-ve:",code_decimal:"&#127483;&#127466;",category:"f",emoji_order:"2432"},{name:"flag-vg",unicode:"1f1fb-1f1ec",shortname:":flag-vg:",code_decimal:"&#127483;&#127468;",category:"f",emoji_order:"2433"},{name:"flag-vi",unicode:"1f1fb-1f1ee",shortname:":flag-vi:",code_decimal:"&#127483;&#127470;",category:"f",emoji_order:"2434"},{name:"flag-vn",unicode:"1f1fb-1f1f3",shortname:":flag-vn:",code_decimal:"&#127483;&#127475;",category:"f",emoji_order:"2435"},{name:"flag-vu",unicode:"1f1fb-1f1fa",shortname:":flag_vu:",code_decimal:"&#127483;&#127482;",category:"f",emoji_order:"2436"},{name:"flag-wf",unicode:"1f1fc-1f1eb",shortname:":flag_wf:",code_decimal:"&#127484;&#127467;",category:"f",emoji_order:"2437"},{name:"flag-ws",unicode:"1f1fc-1f1f8",shortname:":flag_ws:",code_decimal:"&#127484;&#127480;",category:"f",emoji_order:"2438"},{name:"flag-xk",unicode:"1f1fd-1f1f0",shortname:":flag_xk:",code_decimal:"&#127485;&#127472;",category:"f",emoji_order:"2439"},{name:"flag-ye",unicode:"1f1fe-1f1ea",shortname:":flag_ye:",code_decimal:"&#127486;&#127466;",category:"f",emoji_order:"2440"},{name:"flag-yt",unicode:"1f1fe-1f1f9",shortname:":flag_yt:",code_decimal:"&#127486;&#127481;",category:"f",emoji_order:"2441"},{name:"flag-za",unicode:"1f1ff-1f1e6",shortname:":flag_za:",code_decimal:"&#127487;&#127462;",category:"f",emoji_order:"2442"},{name:"flag-zm",unicode:"1f1ff-1f1f2",shortname:":flag_zm:",code_decimal:"&#127487;&#127474;",category:"f",emoji_order:"2443"},{name:"flag-zw",unicode:"1f1ff-1f1fc",shortname:":flag_zw:",code_decimal:"&#127487;&#127484;",category:"f",emoji_order:"2444"},{name:"speech",unicode:"1f600",shortname:":speech:",code_decimal:"&#128172;",category:"p",emoji_order:"1"}],n={};c.forEach(function(e){n[e.name]=e});var d=n;function i(e){return function(e){if(Array.isArray(e)){for(var o=0,a=new Array(e.length);o<e.length;o++)a[o]=e[o];return a}}(e)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance")}()}function t(e){return(t="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function _(e,o){for(var a=0;a<o.length;a++){var r=o[a];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function l(e,o){return!o||"object"!==t(o)&&"function"!=typeof o?function(e){if(void 0!==e)return e;throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}(e):o}function s(e,o,a){return(s="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,o,a){var r=function(e,o){for(;!Object.prototype.hasOwnProperty.call(e,o)&&null!==(e=f(e)););return e}(e,o);if(r){var c=Object.getOwnPropertyDescriptor(r,o);return c.get?c.get.call(a):c.value}})(e,o,a||e)}function f(e){return(f=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function g(e,o){return(g=Object.setPrototypeOf||function(e,o){return e.__proto__=o,e})(e,o)}var u=m.a.import("blots/embed"),h=function(e){function r(){return function(e,o){if(!(e instanceof o))throw new TypeError("Cannot call a class as a function")}(this,r),l(this,f(r).apply(this,arguments))}var o,a,c;return function(e,o){if("function"!=typeof o&&null!==o)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(o&&o.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),o&&g(e,o)}(r,u),o=r,c=[{key:"create",value:function(e){var o=s(f(r),"create",this).call(this);if("object"===t(e))r.buildSpan(e,o);else if("string"==typeof e){var a=d[e];a&&r.buildSpan(a,o)}return o}},{key:"value",value:function(e){return e.dataset.name}},{key:"buildSpan",value:function(e,o){o.setAttribute("data-name",e.name);var a=document.createElement("span");a.classList.add(this.emojiClass),a.classList.add(this.emojiPrefix+e.name),a.innerText=String.fromCodePoint.apply(String,i(r.parseUnicode(e.unicode))),o.appendChild(a)}},{key:"parseUnicode",value:function(e){return e.split("-").map(function(e){return parseInt(e,16)})}}],(a=null)&&_(o.prototype,a),c&&_(o,c),r}();h.blotName="emoji",h.className="ql-emojiblot",h.tagName="span",h.emojiClass="ap",h.emojiPrefix="ap-";var y=h,j=a(1),p=a.n(j);function b(e){return(b="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function v(e,o){for(var a=0;a<o.length;a++){var r=o[a];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function k(e){return(k=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function w(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function x(e,o){return(x=Object.setPrototypeOf||function(e,o){return e.__proto__=o,e})(e,o)}var S=m.a.import("core/module"),q=function(e){function n(e,o){var a,r,c;return function(e,o){if(!(e instanceof o))throw new TypeError("Cannot call a class as a function")}(this,n),r=this,(a=!(c=k(n).call(this,e,o))||"object"!==b(c)&&"function"!=typeof c?w(r):c).emojiList=o.emojiList,a.fuse=new p.a(o.emojiList,o.fuse),a.quill=e,a.onClose=o.onClose,a.onOpen=o.onOpen,a.container=document.createElement("ul"),a.container.classList.add("emoji_completions"),a.quill.container.appendChild(a.container),a.container.style.position="absolute",a.container.style.display="none",a.onSelectionChange=a.maybeUnfocus.bind(w(a)),a.onTextChange=a.update.bind(w(a)),a.open=!1,a.atIndex=null,a.focusedButton=null,a.isWhiteSpace=function(e){var o=!1;return/\s/.test(e)&&(o=!0),o},e.keyboard.addBinding({key:186,shiftKey:!0},a.triggerPicker.bind(w(a))),e.keyboard.addBinding({key:59,shiftKey:!0},a.triggerPicker.bind(w(a))),e.keyboard.addBinding({key:39,collapsed:!0},a.handleArrow.bind(w(a))),e.keyboard.addBinding({key:40,collapsed:!0},a.handleArrow.bind(w(a))),a}var o,a,r;return function(e,o){if("function"!=typeof o&&null!==o)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(o&&o.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),o&&x(e,o)}(n,S),o=n,(a=[{key:"triggerPicker",value:function(e,o){if(this.open)return!0;0<e.length&&this.quill.deleteText(e.index,e.length,m.a.sources.USER),this.quill.insertText(e.index,":","emoji-shortname",m.a.sources.USER);var a=this.quill.getBounds(e.index);this.quill.setSelection(e.index+1,m.a.sources.SILENT),this.atIndex=e.index,a.left+250>this.quill.container.offsetWidth?this.container.style.left=a.left-250+"px":this.container.style.left=a.left+"px",this.container.style.top=a.top+a.height+"px",this.open=!0,this.quill.on("text-change",this.onTextChange),this.quill.once("selection-change",this.onSelectionChange),this.onOpen&&this.onOpen()}},{key:"handleArrow",value:function(){if(!this.open)return!0;this.buttons[0].classList.remove("emoji-active"),this.buttons[0].focus(),1<this.buttons.length&&this.buttons[1].focus()}},{key:"update",value:function(){var e=this.quill.getSelection().index;if(this.atIndex>=e)return this.close(null);this.query=this.quill.getText(this.atIndex+1,e-this.atIndex-1);try{if(event&&this.isWhiteSpace(this.query))return void this.close(null)}catch(e){console.warn(e)}this.query=this.query.trim();var o=this.fuse.search(this.query);o.sort(function(e,o){return e.emoji_order-o.emoji_order}),this.query.length<this.options.fuse.minMatchCharLength||0===o.length?this.container.style.display="none":(15<o.length&&(o=o.slice(0,15)),this.renderCompletions(o))}},{key:"maybeUnfocus",value:function(){this.container.querySelector("*:focus")||this.close(null)}},{key:"renderCompletions",value:function(e){var n=this;try{if(event){if("Enter"===event.key||13===event.keyCode)return this.close(e[0],1),void(this.container.style.display="none");if("Tab"===event.key||9===event.keyCode)return this.quill.disable(),this.buttons[0].classList.remove("emoji-active"),void this.buttons[1].focus()}}catch(e){console.warn(e)}for(;this.container.firstChild;)this.container.removeChild(this.container.firstChild);var d=Array(e.length);this.buttons=d;if(e.forEach(function(e,o){var a,r,c=E("li",{},E("button",{type:"button"},E("span",{className:"button-emoji ap ap-"+e.name,innerHTML:e.code_decimal}),E("span",{className:"unmatched"},e.shortname)));n.container.appendChild(c),d[o]=c.firstChild,d[o].addEventListener("keydown",(a=o,r=e,function(e){if("ArrowRight"===e.key||39===e.keyCode)e.preventDefault(),d[Math.min(d.length-1,a+1)].focus();else if("Tab"===e.key||9===e.keyCode){if(e.preventDefault(),a+1===d.length)return void d[0].focus();d[Math.min(d.length-1,a+1)].focus()}else"ArrowLeft"===e.key||37===e.keyCode?(e.preventDefault(),d[Math.max(0,a-1)].focus()):"ArrowDown"===e.key||40===e.keyCode?(e.preventDefault(),d[Math.min(d.length-1,a+1)].focus()):"ArrowUp"===e.key||38===e.keyCode?(e.preventDefault(),d[Math.max(0,a-1)].focus()):"Enter"!==e.key&&13!==e.keyCode&&" "!==e.key&&32!==e.keyCode&&"Tab"!==e.key&&9!==e.keyCode||(e.preventDefault(),n.quill.enable(),n.close(r))})),d[o].addEventListener("mousedown",function(){return n.close(e)}),d[o].addEventListener("focus",function(){return n.focusedButton=o}),d[o].addEventListener("unfocus",function(){return n.focusedButton=null})}),this.container.style.display="block",this.quill.container.classList.contains("top-emoji")){var o,a=this.container.querySelectorAll("li");for(o=0;o<a.length;o++)a[o].style.display="block";window.innerHeight/2<this.quill.container.getBoundingClientRect().top&&0<this.container.offsetHeight&&(this.container.style.top="-"+this.container.offsetHeight+"px")}d[0].classList.add("emoji-active")}},{key:"close",value:function(e){var o=this,a=1<arguments.length&&void 0!==arguments[1]?arguments[1]:0;for(this.quill.enable(),this.container.style.display="none";this.container.firstChild;)this.container.removeChild(this.container.firstChild);this.quill.off("selection-change",this.onSelectionChange),this.quill.off("text-change",this.onTextChange),e&&(this.quill.deleteText(this.atIndex,this.query.length+1+a,m.a.sources.USER),this.quill.insertEmbed(this.atIndex,"emoji",e,m.a.sources.USER),setTimeout(function(){return o.quill.setSelection(o.atIndex+1)},0)),this.quill.focus(),this.open=!1,this.onClose&&this.onClose(e)}}])&&v(o.prototype,a),r&&v(o,r),n}();function E(e,o){var a=document.createElement(e);Object.keys(o).forEach(function(e){return a[e]=o[e]});for(var r=arguments.length,c=new Array(2<r?r-2:0),n=2;n<r;n++)c[n-2]=arguments[n];return c.forEach(function(e){"string"==typeof e&&(e=document.createTextNode(e)),a.appendChild(e)}),a}q.DEFAULTS={emojiList:c,fuse:{shouldSort:!0,threshold:.1,location:0,distance:100,maxPatternLength:32,minMatchCharLength:1,keys:["shortname"]}};var C=q;function L(e){return(L="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function O(e,o){for(var a=0;a<o.length;a++){var r=o[a];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function M(e,o){return!o||"object"!==L(o)&&"function"!=typeof o?function(e){if(void 0!==e)return e;throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}(e):o}function z(e){return(z=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function T(e,o){return(T=Object.setPrototypeOf||function(e,o){return e.__proto__=o,e})(e,o)}m.a.import("delta");var P=m.a.import("core/module"),A=function(e){function c(e,o){var a;!function(e,o){if(!(e instanceof o))throw new TypeError("Cannot call a class as a function")}(this,c),(a=M(this,z(c).call(this,e,o))).quill=e,a.toolbar=e.getModule("toolbar"),void 0!==a.toolbar&&a.toolbar.addHandler("emoji",a.checkPalatteExist);var r=document.getElementsByClassName("ql-emoji");return r&&[].slice.call(r).forEach(function(e){e.innerHTML=o.buttonIcon}),a}var o,a,r;return function(e,o){if("function"!=typeof o&&null!==o)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(o&&o.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),o&&T(e,o)}(c,P),o=c,(a=[{key:"checkPalatteExist",value:function(){var e,o,r=this.quill;e=r,(o=document.getElementById("emoji-palette"))?o.remove():function(c){var e=document.createElement("div"),o=(document.querySelector(".ql-toolbar"),c.getSelection()),a=c.getBounds(o.index);c.container.appendChild(e);var r=c.container.offsetWidth/2,n=c.container.offsetHeight/2,d=(a.left+a.right)/2,i=(a.top+a.bottom)/2;a.left,e.id="emoji-palette",e.style.top=10+a.top+a.height+"px",e.style.left=d<r?d+"px":d-250+"px",e.style.top=i<n?i+"px":i-250+"px";var m=document.createElement("div");m.id="tab-toolbar",e.appendChild(m);var t=document.createElement("div");t.id="tab-panel",e.appendChild(t);var _=document.createElement("ul");if(m.appendChild(_),null===document.getElementById("emoji-close-div")){var l=document.createElement("div");l.id="emoji-close-div",l.addEventListener("click",I,!1),document.getElementsByTagName("body")[0].appendChild(l)}else document.getElementById("emoji-close-div").style.display="block";[{type:"p",name:"people",content:'<div class="i-people"></div>'},{type:"n",name:"nature",content:'<div class="i-nature"></div>'},{type:"d",name:"food",content:'<div class="i-food"></div>'},{type:"s",name:"symbols",content:'<div class="i-symbols"></div>'},{type:"a",name:"activity",content:'<div class="i-activity"></div>'},{type:"t",name:"travel",content:'<div class="i-travel"></div>'},{type:"o",name:"objects",content:'<div class="i-objects"></div>'},{type:"f",name:"flags",content:'<div class="i-flags"></div>'}].map(function(e){var o=document.createElement("li");o.classList.add("emoji-tab"),o.classList.add("filter-"+e.name);var a=e.content;o.innerHTML=a,o.dataset.filter=e.type,_.appendChild(o);var r=document.querySelector(".filter-"+e.name);r.addEventListener("click",function(){var e=document.querySelector(".active");e&&e.classList.remove("active"),r.classList.toggle("active"),function(e,o,a){for(;o.firstChild;)o.removeChild(o.firstChild);H(e.dataset.filter,o,a)}(r,t,c)})}),H("p",t,c),document.querySelector(".filter-people").classList.add("active")}(e),this.quill.on("text-change",function(e,o,a){"user"===a&&(I(),B(r))})}}])&&O(o.prototype,a),r&&O(o,r),c}();function I(){var e=document.getElementById("emoji-palette");document.getElementById("emoji-close-div").style.display="none",e&&e.remove()}function B(e){return e.getSelection()}function H(e,n,d){var o=new p.a(c,{shouldSort:!0,matchAllTokens:!0,threshold:.3,location:0,distance:100,maxPatternLength:32,minMatchCharLength:3,keys:["category"]}).search(e);o.sort(function(e,o){return e.emoji_order-o.emoji_order}),d.focus();var i=B(d);o.map(function(e){var o=document.createElement("span"),a=document.createTextNode(e.shortname);o.appendChild(a),o.classList.add("bem"),o.classList.add("bem-"+e.name),o.classList.add("ap"),o.classList.add("ap-"+e.name);var r=""+e.code_decimal;o.innerHTML=r+" ",n.appendChild(o);var c=document.querySelector(".bem-"+e.name);c&&c.addEventListener("click",function(){(function(e,o){var a=document.createElement(e);Object.keys(o).forEach(function(e){return a[e]=o[e]});for(var r=arguments.length,c=new Array(2<r?r-2:0),n=2;n<r;n++)c[n-2]=arguments[n];return c.forEach(function(e){"string"==typeof e&&(e=document.createTextNode(e)),a.appendChild(e)}),a})("span",{className:"ico",innerHTML:e.code_decimal+" "}).innerHTML;d.insertEmbed(i.index,"emoji",e,m.a.sources.USER),setTimeout(function(){return d.setSelection(i.index+1)},0),I()})})}A.DEFAULTS={buttonIcon:'<svg viewbox="0 0 18 18"><circle class="ql-fill" cx="7" cy="7" r="1"></circle><circle class="ql-fill" cx="11" cy="7" r="1"></circle><path class="ql-stroke" d="M7,10a2,2,0,0,0,4,0H7Z"></path><circle class="ql-stroke" cx="9" cy="9" r="6"></circle></svg>'};var R=A;function N(e){return(N="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function U(e,o){for(var a=0;a<o.length;a++){var r=o[a];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function D(e){return(D=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function F(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function K(e,o){return(K=Object.setPrototypeOf||function(e,o){return e.__proto__=o,e})(e,o)}m.a.import("delta");var W=m.a.import("core/module"),Q=function(e){function n(e,o){var a,r,c;return function(e,o){if(!(e instanceof o))throw new TypeError("Cannot call a class as a function")}(this,n),r=this,(a=!(c=D(n).call(this,e,o))||"object"!==N(c)&&"function"!=typeof c?F(r):c).quill=e,a.container=document.createElement("div"),a.container.classList.add("textarea-emoji-control"),a.container.style.position="absolute",a.container.innerHTML=o.buttonIcon,a.quill.container.appendChild(a.container),a.container.addEventListener("click",a.checkEmojiBoxExist.bind(F(a)),!1),a}var o,a,r;return function(e,o){if("function"!=typeof o&&null!==o)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(o&&o.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),o&&K(e,o)}(n,W),o=n,(a=[{key:"checkEmojiBoxExist",value:function(){var e,o,a=document.getElementById("textarea-emoji");if(a)a.remove();else{var r=document.createElement("div");r.id="textarea-emoji",this.quill.container.appendChild(r);var c=document.createElement("div");c.id="tab-toolbar",r.appendChild(c);var n=document.createElement("ul");if(c.appendChild(n),null===document.getElementById("emoji-close-div")){var d=document.createElement("div");d.id="emoji-close-div",d.addEventListener("click",Z,!1),document.getElementsByTagName("body")[0].appendChild(d)}else document.getElementById("emoji-close-div").style.display="block";var i=document.createElement("div");i.id="tab-panel",r.appendChild(i);var m=this.quill;[{type:"p",name:"people",content:'<div class="i-people"></div>'},{type:"n",name:"nature",content:'<div class="i-nature"></div>'},{type:"d",name:"food",content:'<div class="i-food"></div>'},{type:"s",name:"symbols",content:'<div class="i-symbols"></div>'},{type:"a",name:"activity",content:'<div class="i-activity"></div>'},{type:"t",name:"travel",content:'<div class="i-travel"></div>'},{type:"o",name:"objects",content:'<div class="i-objects"></div>'},{type:"f",name:"flags",content:'<div class="i-flags"></div>'}].map(function(e){var o=document.createElement("li");o.classList.add("emoji-tab"),o.classList.add("filter-"+e.name);var a=e.content;o.innerHTML=a,o.dataset.filter=e.type,n.appendChild(o);var r=document.querySelector(".filter-"+e.name);r.addEventListener("click",function(){var e=document.getElementById("textarea-emoji"),o=e&&e.querySelector(".active");for(o&&o.classList.remove("active"),r.classList.toggle("active");i.firstChild;)i.removeChild(i.firstChild);$(r.dataset.filter,i,m)})}),window.innerHeight/2<this.quill.container.getBoundingClientRect().top&&(r.style.top="-250px"),e=i,o=this.quill,$("p",e,o),document.querySelector(".filter-people").classList.add("active")}}}])&&U(o.prototype,a),r&&U(o,r),n}();function Z(){var e=document.getElementById("textarea-emoji");document.getElementById("emoji-close-div").style.display="none",e&&e.remove()}function $(e,n,d){var o=new p.a(c,{shouldSort:!0,matchAllTokens:!0,threshold:.3,location:0,distance:100,maxPatternLength:32,minMatchCharLength:3,keys:["category"]}).search(e);o.sort(function(e,o){return e.emoji_order-o.emoji_order}),d.focus();var i=d.getSelection();o.map(function(e){var o=document.createElement("span"),a=document.createTextNode(e.shortname);o.appendChild(a),o.classList.add("bem"),o.classList.add("bem-"+e.name),o.classList.add("ap"),o.classList.add("ap-"+e.name);var r=""+e.code_decimal;o.innerHTML=r+" ",n.appendChild(o);var c=document.querySelector(".bem-"+e.name);c&&c.addEventListener("click",function(){d.insertEmbed(i.index,"emoji",e,m.a.sources.USER),setTimeout(function(){return d.setSelection(i.index+1)},0),Z()})})}Q.DEFAULTS={buttonIcon:'<svg viewbox="0 0 18 18"><circle class="ql-fill" cx="7" cy="7" r="1"></circle><circle class="ql-fill" cx="11" cy="7" r="1"></circle><path class="ql-stroke" d="M7,10a2,2,0,0,0,4,0H7Z"></path><circle class="ql-stroke" cx="9" cy="9" r="6"></circle></svg>'};var J=Q;a(2);m.a.register({"formats/emoji":y,"modules/emoji-shortname":C,"modules/emoji-toolbar":R,"modules/emoji-textarea":J},!0);o.default={EmojiBlot:y,ShortNameEmoji:C,ToolbarEmoji:R,TextAreaEmoji:J}}])});'''

QuillJS = r'''
/*!
 * Quill Editor v1.3.6
 * https://quilljs.com/
 * Copyright (c) 2014, Jason Chen
 * Copyright (c) 2013, salesforce.com
 */
(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define([], factory);
	else if(typeof exports === 'object')
		exports["Quill"] = factory();
	else
		root["Quill"] = factory();
})(typeof self !== 'undefined' ? self : this, function() {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 109);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var container_1 = __webpack_require__(17);
var format_1 = __webpack_require__(18);
var leaf_1 = __webpack_require__(19);
var scroll_1 = __webpack_require__(45);
var inline_1 = __webpack_require__(46);
var block_1 = __webpack_require__(47);
var embed_1 = __webpack_require__(48);
var text_1 = __webpack_require__(49);
var attributor_1 = __webpack_require__(12);
var class_1 = __webpack_require__(32);
var style_1 = __webpack_require__(33);
var store_1 = __webpack_require__(31);
var Registry = __webpack_require__(1);
var Parchment = {
    Scope: Registry.Scope,
    create: Registry.create,
    find: Registry.find,
    query: Registry.query,
    register: Registry.register,
    Container: container_1.default,
    Format: format_1.default,
    Leaf: leaf_1.default,
    Embed: embed_1.default,
    Scroll: scroll_1.default,
    Block: block_1.default,
    Inline: inline_1.default,
    Text: text_1.default,
    Attributor: {
        Attribute: attributor_1.default,
        Class: class_1.default,
        Style: style_1.default,
        Store: store_1.default,
    },
};
exports.default = Parchment;


/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var ParchmentError = /** @class */ (function (_super) {
    __extends(ParchmentError, _super);
    function ParchmentError(message) {
        var _this = this;
        message = '[Parchment] ' + message;
        _this = _super.call(this, message) || this;
        _this.message = message;
        _this.name = _this.constructor.name;
        return _this;
    }
    return ParchmentError;
}(Error));
exports.ParchmentError = ParchmentError;
var attributes = {};
var classes = {};
var tags = {};
var types = {};
exports.DATA_KEY = '__blot';
var Scope;
(function (Scope) {
    Scope[Scope["TYPE"] = 3] = "TYPE";
    Scope[Scope["LEVEL"] = 12] = "LEVEL";
    Scope[Scope["ATTRIBUTE"] = 13] = "ATTRIBUTE";
    Scope[Scope["BLOT"] = 14] = "BLOT";
    Scope[Scope["INLINE"] = 7] = "INLINE";
    Scope[Scope["BLOCK"] = 11] = "BLOCK";
    Scope[Scope["BLOCK_BLOT"] = 10] = "BLOCK_BLOT";
    Scope[Scope["INLINE_BLOT"] = 6] = "INLINE_BLOT";
    Scope[Scope["BLOCK_ATTRIBUTE"] = 9] = "BLOCK_ATTRIBUTE";
    Scope[Scope["INLINE_ATTRIBUTE"] = 5] = "INLINE_ATTRIBUTE";
    Scope[Scope["ANY"] = 15] = "ANY";
})(Scope = exports.Scope || (exports.Scope = {}));
function create(input, value) {
    var match = query(input);
    if (match == null) {
        throw new ParchmentError("Unable to create " + input + " blot");
    }
    var BlotClass = match;
    var node = 
    // @ts-ignore
    input instanceof Node || input['nodeType'] === Node.TEXT_NODE ? input : BlotClass.create(value);
    return new BlotClass(node, value);
}
exports.create = create;
function find(node, bubble) {
    if (bubble === void 0) { bubble = false; }
    if (node == null)
        return null;
    // @ts-ignore
    if (node[exports.DATA_KEY] != null)
        return node[exports.DATA_KEY].blot;
    if (bubble)
        return find(node.parentNode, bubble);
    return null;
}
exports.find = find;
function query(query, scope) {
    if (scope === void 0) { scope = Scope.ANY; }
    var match;
    if (typeof query === 'string') {
        match = types[query] || attributes[query];
        // @ts-ignore
    }
    else if (query instanceof Text || query['nodeType'] === Node.TEXT_NODE) {
        match = types['text'];
    }
    else if (typeof query === 'number') {
        if (query & Scope.LEVEL & Scope.BLOCK) {
            match = types['block'];
        }
        else if (query & Scope.LEVEL & Scope.INLINE) {
            match = types['inline'];
        }
    }
    else if (query instanceof HTMLElement) {
        var names = (query.getAttribute('class') || '').split(/\s+/);
        for (var i in names) {
            match = classes[names[i]];
            if (match)
                break;
        }
        match = match || tags[query.tagName];
    }
    if (match == null)
        return null;
    // @ts-ignore
    if (scope & Scope.LEVEL & match.scope && scope & Scope.TYPE & match.scope)
        return match;
    return null;
}
exports.query = query;
function register() {
    var Definitions = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        Definitions[_i] = arguments[_i];
    }
    if (Definitions.length > 1) {
        return Definitions.map(function (d) {
            return register(d);
        });
    }
    var Definition = Definitions[0];
    if (typeof Definition.blotName !== 'string' && typeof Definition.attrName !== 'string') {
        throw new ParchmentError('Invalid definition');
    }
    else if (Definition.blotName === 'abstract') {
        throw new ParchmentError('Cannot register abstract class');
    }
    types[Definition.blotName || Definition.attrName] = Definition;
    if (typeof Definition.keyName === 'string') {
        attributes[Definition.keyName] = Definition;
    }
    else {
        if (Definition.className != null) {
            classes[Definition.className] = Definition;
        }
        if (Definition.tagName != null) {
            if (Array.isArray(Definition.tagName)) {
                Definition.tagName = Definition.tagName.map(function (tagName) {
                    return tagName.toUpperCase();
                });
            }
            else {
                Definition.tagName = Definition.tagName.toUpperCase();
            }
            var tagNames = Array.isArray(Definition.tagName) ? Definition.tagName : [Definition.tagName];
            tagNames.forEach(function (tag) {
                if (tags[tag] == null || Definition.className == null) {
                    tags[tag] = Definition;
                }
            });
        }
    }
    return Definition;
}
exports.register = register;


/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

var diff = __webpack_require__(51);
var equal = __webpack_require__(11);
var extend = __webpack_require__(3);
var op = __webpack_require__(20);


var NULL_CHARACTER = String.fromCharCode(0);  // Placeholder char for embed in diff()


var Delta = function (ops) {
  // Assume we are given a well formed ops
  if (Array.isArray(ops)) {
    this.ops = ops;
  } else if (ops != null && Array.isArray(ops.ops)) {
    this.ops = ops.ops;
  } else {
    this.ops = [];
  }
};


Delta.prototype.insert = function (text, attributes) {
  var newOp = {};
  if (text.length === 0) return this;
  newOp.insert = text;
  if (attributes != null && typeof attributes === 'object' && Object.keys(attributes).length > 0) {
    newOp.attributes = attributes;
  }
  return this.push(newOp);
};

Delta.prototype['delete'] = function (length) {
  if (length <= 0) return this;
  return this.push({ 'delete': length });
};

Delta.prototype.retain = function (length, attributes) {
  if (length <= 0) return this;
  var newOp = { retain: length };
  if (attributes != null && typeof attributes === 'object' && Object.keys(attributes).length > 0) {
    newOp.attributes = attributes;
  }
  return this.push(newOp);
};

Delta.prototype.push = function (newOp) {
  var index = this.ops.length;
  var lastOp = this.ops[index - 1];
  newOp = extend(true, {}, newOp);
  if (typeof lastOp === 'object') {
    if (typeof newOp['delete'] === 'number' && typeof lastOp['delete'] === 'number') {
      this.ops[index - 1] = { 'delete': lastOp['delete'] + newOp['delete'] };
      return this;
    }
    // Since it does not matter if we insert before or after deleting at the same index,
    // always prefer to insert first
    if (typeof lastOp['delete'] === 'number' && newOp.insert != null) {
      index -= 1;
      lastOp = this.ops[index - 1];
      if (typeof lastOp !== 'object') {
        this.ops.unshift(newOp);
        return this;
      }
    }
    if (equal(newOp.attributes, lastOp.attributes)) {
      if (typeof newOp.insert === 'string' && typeof lastOp.insert === 'string') {
        this.ops[index - 1] = { insert: lastOp.insert + newOp.insert };
        if (typeof newOp.attributes === 'object') this.ops[index - 1].attributes = newOp.attributes
        return this;
      } else if (typeof newOp.retain === 'number' && typeof lastOp.retain === 'number') {
        this.ops[index - 1] = { retain: lastOp.retain + newOp.retain };
        if (typeof newOp.attributes === 'object') this.ops[index - 1].attributes = newOp.attributes
        return this;
      }
    }
  }
  if (index === this.ops.length) {
    this.ops.push(newOp);
  } else {
    this.ops.splice(index, 0, newOp);
  }
  return this;
};

Delta.prototype.chop = function () {
  var lastOp = this.ops[this.ops.length - 1];
  if (lastOp && lastOp.retain && !lastOp.attributes) {
    this.ops.pop();
  }
  return this;
};

Delta.prototype.filter = function (predicate) {
  return this.ops.filter(predicate);
};

Delta.prototype.forEach = function (predicate) {
  this.ops.forEach(predicate);
};

Delta.prototype.map = function (predicate) {
  return this.ops.map(predicate);
};

Delta.prototype.partition = function (predicate) {
  var passed = [], failed = [];
  this.forEach(function(op) {
    var target = predicate(op) ? passed : failed;
    target.push(op);
  });
  return [passed, failed];
};

Delta.prototype.reduce = function (predicate, initial) {
  return this.ops.reduce(predicate, initial);
};

Delta.prototype.changeLength = function () {
  return this.reduce(function (length, elem) {
    if (elem.insert) {
      return length + op.length(elem);
    } else if (elem.delete) {
      return length - elem.delete;
    }
    return length;
  }, 0);
};

Delta.prototype.length = function () {
  return this.reduce(function (length, elem) {
    return length + op.length(elem);
  }, 0);
};

Delta.prototype.slice = function (start, end) {
  start = start || 0;
  if (typeof end !== 'number') end = Infinity;
  var ops = [];
  var iter = op.iterator(this.ops);
  var index = 0;
  while (index < end && iter.hasNext()) {
    var nextOp;
    if (index < start) {
      nextOp = iter.next(start - index);
    } else {
      nextOp = iter.next(end - index);
      ops.push(nextOp);
    }
    index += op.length(nextOp);
  }
  return new Delta(ops);
};


Delta.prototype.compose = function (other) {
  var thisIter = op.iterator(this.ops);
  var otherIter = op.iterator(other.ops);
  var delta = new Delta();
  while (thisIter.hasNext() || otherIter.hasNext()) {
    if (otherIter.peekType() === 'insert') {
      delta.push(otherIter.next());
    } else if (thisIter.peekType() === 'delete') {
      delta.push(thisIter.next());
    } else {
      var length = Math.min(thisIter.peekLength(), otherIter.peekLength());
      var thisOp = thisIter.next(length);
      var otherOp = otherIter.next(length);
      if (typeof otherOp.retain === 'number') {
        var newOp = {};
        if (typeof thisOp.retain === 'number') {
          newOp.retain = length;
        } else {
          newOp.insert = thisOp.insert;
        }
        // Preserve null when composing with a retain, otherwise remove it for inserts
        var attributes = op.attributes.compose(thisOp.attributes, otherOp.attributes, typeof thisOp.retain === 'number');
        if (attributes) newOp.attributes = attributes;
        delta.push(newOp);
      // Other op should be delete, we could be an insert or retain
      // Insert + delete cancels out
      } else if (typeof otherOp['delete'] === 'number' && typeof thisOp.retain === 'number') {
        delta.push(otherOp);
      }
    }
  }
  return delta.chop();
};

Delta.prototype.concat = function (other) {
  var delta = new Delta(this.ops.slice());
  if (other.ops.length > 0) {
    delta.push(other.ops[0]);
    delta.ops = delta.ops.concat(other.ops.slice(1));
  }
  return delta;
};

Delta.prototype.diff = function (other, index) {
  if (this.ops === other.ops) {
    return new Delta();
  }
  var strings = [this, other].map(function (delta) {
    return delta.map(function (op) {
      if (op.insert != null) {
        return typeof op.insert === 'string' ? op.insert : NULL_CHARACTER;
      }
      var prep = (delta === other) ? 'on' : 'with';
      throw new Error('diff() called ' + prep + ' non-document');
    }).join('');
  });
  var delta = new Delta();
  var diffResult = diff(strings[0], strings[1], index);
  var thisIter = op.iterator(this.ops);
  var otherIter = op.iterator(other.ops);
  diffResult.forEach(function (component) {
    var length = component[1].length;
    while (length > 0) {
      var opLength = 0;
      switch (component[0]) {
        case diff.INSERT:
          opLength = Math.min(otherIter.peekLength(), length);
          delta.push(otherIter.next(opLength));
          break;
        case diff.DELETE:
          opLength = Math.min(length, thisIter.peekLength());
          thisIter.next(opLength);
          delta['delete'](opLength);
          break;
        case diff.EQUAL:
          opLength = Math.min(thisIter.peekLength(), otherIter.peekLength(), length);
          var thisOp = thisIter.next(opLength);
          var otherOp = otherIter.next(opLength);
          if (equal(thisOp.insert, otherOp.insert)) {
            delta.retain(opLength, op.attributes.diff(thisOp.attributes, otherOp.attributes));
          } else {
            delta.push(otherOp)['delete'](opLength);
          }
          break;
      }
      length -= opLength;
    }
  });
  return delta.chop();
};

Delta.prototype.eachLine = function (predicate, newline) {
  newline = newline || '\n';
  var iter = op.iterator(this.ops);
  var line = new Delta();
  var i = 0;
  while (iter.hasNext()) {
    if (iter.peekType() !== 'insert') return;
    var thisOp = iter.peek();
    var start = op.length(thisOp) - iter.peekLength();
    var index = typeof thisOp.insert === 'string' ?
      thisOp.insert.indexOf(newline, start) - start : -1;
    if (index < 0) {
      line.push(iter.next());
    } else if (index > 0) {
      line.push(iter.next(index));
    } else {
      if (predicate(line, iter.next(1).attributes || {}, i) === false) {
        return;
      }
      i += 1;
      line = new Delta();
    }
  }
  if (line.length() > 0) {
    predicate(line, {}, i);
  }
};

Delta.prototype.transform = function (other, priority) {
  priority = !!priority;
  if (typeof other === 'number') {
    return this.transformPosition(other, priority);
  }
  var thisIter = op.iterator(this.ops);
  var otherIter = op.iterator(other.ops);
  var delta = new Delta();
  while (thisIter.hasNext() || otherIter.hasNext()) {
    if (thisIter.peekType() === 'insert' && (priority || otherIter.peekType() !== 'insert')) {
      delta.retain(op.length(thisIter.next()));
    } else if (otherIter.peekType() === 'insert') {
      delta.push(otherIter.next());
    } else {
      var length = Math.min(thisIter.peekLength(), otherIter.peekLength());
      var thisOp = thisIter.next(length);
      var otherOp = otherIter.next(length);
      if (thisOp['delete']) {
        // Our delete either makes their delete redundant or removes their retain
        continue;
      } else if (otherOp['delete']) {
        delta.push(otherOp);
      } else {
        // We retain either their retain or insert
        delta.retain(length, op.attributes.transform(thisOp.attributes, otherOp.attributes, priority));
      }
    }
  }
  return delta.chop();
};

Delta.prototype.transformPosition = function (index, priority) {
  priority = !!priority;
  var thisIter = op.iterator(this.ops);
  var offset = 0;
  while (thisIter.hasNext() && offset <= index) {
    var length = thisIter.peekLength();
    var nextType = thisIter.peekType();
    thisIter.next();
    if (nextType === 'delete') {
      index -= Math.min(length, index - offset);
      continue;
    } else if (nextType === 'insert' && (offset < index || !priority)) {
      index += length;
    }
    offset += length;
  }
  return index;
};


module.exports = Delta;


/***/ }),
/* 3 */
/***/ (function(module, exports) {

'use strict';

var hasOwn = Object.prototype.hasOwnProperty;
var toStr = Object.prototype.toString;

var isArray = function isArray(arr) {
	if (typeof Array.isArray === 'function') {
		return Array.isArray(arr);
	}

	return toStr.call(arr) === '[object Array]';
};

var isPlainObject = function isPlainObject(obj) {
	if (!obj || toStr.call(obj) !== '[object Object]') {
		return false;
	}

	var hasOwnConstructor = hasOwn.call(obj, 'constructor');
	var hasIsPrototypeOf = obj.constructor && obj.constructor.prototype && hasOwn.call(obj.constructor.prototype, 'isPrototypeOf');
	// Not own constructor property must be Object
	if (obj.constructor && !hasOwnConstructor && !hasIsPrototypeOf) {
		return false;
	}

	// Own properties are enumerated firstly, so to speed up,
	// if last one is own, then all properties are own.
	var key;
	for (key in obj) { /**/ }

	return typeof key === 'undefined' || hasOwn.call(obj, key);
};

module.exports = function extend() {
	var options, name, src, copy, copyIsArray, clone;
	var target = arguments[0];
	var i = 1;
	var length = arguments.length;
	var deep = false;

	// Handle a deep copy situation
	if (typeof target === 'boolean') {
		deep = target;
		target = arguments[1] || {};
		// skip the boolean and the target
		i = 2;
	}
	if (target == null || (typeof target !== 'object' && typeof target !== 'function')) {
		target = {};
	}

	for (; i < length; ++i) {
		options = arguments[i];
		// Only deal with non-null/undefined values
		if (options != null) {
			// Extend the base object
			for (name in options) {
				src = target[name];
				copy = options[name];

				// Prevent never-ending loop
				if (target !== copy) {
					// Recurse if we're merging plain objects or arrays
					if (deep && copy && (isPlainObject(copy) || (copyIsArray = isArray(copy)))) {
						if (copyIsArray) {
							copyIsArray = false;
							clone = src && isArray(src) ? src : [];
						} else {
							clone = src && isPlainObject(src) ? src : {};
						}

						// Never move original objects, clone them
						target[name] = extend(deep, clone, copy);

					// Don't bring in undefined values
					} else if (typeof copy !== 'undefined') {
						target[name] = copy;
					}
				}
			}
		}
	}

	// Return the modified object
	return target;
};


/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = exports.BlockEmbed = exports.bubbleFormats = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _extend = __webpack_require__(3);

var _extend2 = _interopRequireDefault(_extend);

var _quillDelta = __webpack_require__(2);

var _quillDelta2 = _interopRequireDefault(_quillDelta);

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _break = __webpack_require__(16);

var _break2 = _interopRequireDefault(_break);

var _inline = __webpack_require__(6);

var _inline2 = _interopRequireDefault(_inline);

var _text = __webpack_require__(7);

var _text2 = _interopRequireDefault(_text);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var NEWLINE_LENGTH = 1;

var BlockEmbed = function (_Parchment$Embed) {
  _inherits(BlockEmbed, _Parchment$Embed);

  function BlockEmbed() {
    _classCallCheck(this, BlockEmbed);

    return _possibleConstructorReturn(this, (BlockEmbed.__proto__ || Object.getPrototypeOf(BlockEmbed)).apply(this, arguments));
  }

  _createClass(BlockEmbed, [{
    key: 'attach',
    value: function attach() {
      _get(BlockEmbed.prototype.__proto__ || Object.getPrototypeOf(BlockEmbed.prototype), 'attach', this).call(this);
      this.attributes = new _parchment2.default.Attributor.Store(this.domNode);
    }
  }, {
    key: 'delta',
    value: function delta() {
      return new _quillDelta2.default().insert(this.value(), (0, _extend2.default)(this.formats(), this.attributes.values()));
    }
  }, {
    key: 'format',
    value: function format(name, value) {
      var attribute = _parchment2.default.query(name, _parchment2.default.Scope.BLOCK_ATTRIBUTE);
      if (attribute != null) {
        this.attributes.attribute(attribute, value);
      }
    }
  }, {
    key: 'formatAt',
    value: function formatAt(index, length, name, value) {
      this.format(name, value);
    }
  }, {
    key: 'insertAt',
    value: function insertAt(index, value, def) {
      if (typeof value === 'string' && value.endsWith('\n')) {
        var block = _parchment2.default.create(Block.blotName);
        this.parent.insertBefore(block, index === 0 ? this : this.next);
        block.insertAt(0, value.slice(0, -1));
      } else {
        _get(BlockEmbed.prototype.__proto__ || Object.getPrototypeOf(BlockEmbed.prototype), 'insertAt', this).call(this, index, value, def);
      }
    }
  }]);

  return BlockEmbed;
}(_parchment2.default.Embed);

BlockEmbed.scope = _parchment2.default.Scope.BLOCK_BLOT;
// It is important for cursor behavior BlockEmbeds use tags that are block level elements


var Block = function (_Parchment$Block) {
  _inherits(Block, _Parchment$Block);

  function Block(domNode) {
    _classCallCheck(this, Block);

    var _this2 = _possibleConstructorReturn(this, (Block.__proto__ || Object.getPrototypeOf(Block)).call(this, domNode));

    _this2.cache = {};
    return _this2;
  }

  _createClass(Block, [{
    key: 'delta',
    value: function delta() {
      if (this.cache.delta == null) {
        this.cache.delta = this.descendants(_parchment2.default.Leaf).reduce(function (delta, leaf) {
          if (leaf.length() === 0) {
            return delta;
          } else {
            return delta.insert(leaf.value(), bubbleFormats(leaf));
          }
        }, new _quillDelta2.default()).insert('\n', bubbleFormats(this));
      }
      return this.cache.delta;
    }
  }, {
    key: 'deleteAt',
    value: function deleteAt(index, length) {
      _get(Block.prototype.__proto__ || Object.getPrototypeOf(Block.prototype), 'deleteAt', this).call(this, index, length);
      this.cache = {};
    }
  }, {
    key: 'formatAt',
    value: function formatAt(index, length, name, value) {
      if (length <= 0) return;
      if (_parchment2.default.query(name, _parchment2.default.Scope.BLOCK)) {
        if (index + length === this.length()) {
          this.format(name, value);
        }
      } else {
        _get(Block.prototype.__proto__ || Object.getPrototypeOf(Block.prototype), 'formatAt', this).call(this, index, Math.min(length, this.length() - index - 1), name, value);
      }
      this.cache = {};
    }
  }, {
    key: 'insertAt',
    value: function insertAt(index, value, def) {
      if (def != null) return _get(Block.prototype.__proto__ || Object.getPrototypeOf(Block.prototype), 'insertAt', this).call(this, index, value, def);
      if (value.length === 0) return;
      var lines = value.split('\n');
      var text = lines.shift();
      if (text.length > 0) {
        if (index < this.length() - 1 || this.children.tail == null) {
          _get(Block.prototype.__proto__ || Object.getPrototypeOf(Block.prototype), 'insertAt', this).call(this, Math.min(index, this.length() - 1), text);
        } else {
          this.children.tail.insertAt(this.children.tail.length(), text);
        }
        this.cache = {};
      }
      var block = this;
      lines.reduce(function (index, line) {
        block = block.split(index, true);
        block.insertAt(0, line);
        return line.length;
      }, index + text.length);
    }
  }, {
    key: 'insertBefore',
    value: function insertBefore(blot, ref) {
      var head = this.children.head;
      _get(Block.prototype.__proto__ || Object.getPrototypeOf(Block.prototype), 'insertBefore', this).call(this, blot, ref);
      if (head instanceof _break2.default) {
        head.remove();
      }
      this.cache = {};
    }
  }, {
    key: 'length',
    value: function length() {
      if (this.cache.length == null) {
        this.cache.length = _get(Block.prototype.__proto__ || Object.getPrototypeOf(Block.prototype), 'length', this).call(this) + NEWLINE_LENGTH;
      }
      return this.cache.length;
    }
  }, {
    key: 'moveChildren',
    value: function moveChildren(target, ref) {
      _get(Block.prototype.__proto__ || Object.getPrototypeOf(Block.prototype), 'moveChildren', this).call(this, target, ref);
      this.cache = {};
    }
  }, {
    key: 'optimize',
    value: function optimize(context) {
      _get(Block.prototype.__proto__ || Object.getPrototypeOf(Block.prototype), 'optimize', this).call(this, context);
      this.cache = {};
    }
  }, {
    key: 'path',
    value: function path(index) {
      return _get(Block.prototype.__proto__ || Object.getPrototypeOf(Block.prototype), 'path', this).call(this, index, true);
    }
  }, {
    key: 'removeChild',
    value: function removeChild(child) {
      _get(Block.prototype.__proto__ || Object.getPrototypeOf(Block.prototype), 'removeChild', this).call(this, child);
      this.cache = {};
    }
  }, {
    key: 'split',
    value: function split(index) {
      var force = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;

      if (force && (index === 0 || index >= this.length() - NEWLINE_LENGTH)) {
        var clone = this.clone();
        if (index === 0) {
          this.parent.insertBefore(clone, this);
          return this;
        } else {
          this.parent.insertBefore(clone, this.next);
          return clone;
        }
      } else {
        var next = _get(Block.prototype.__proto__ || Object.getPrototypeOf(Block.prototype), 'split', this).call(this, index, force);
        this.cache = {};
        return next;
      }
    }
  }]);

  return Block;
}(_parchment2.default.Block);

Block.blotName = 'block';
Block.tagName = 'P';
Block.defaultChild = 'break';
Block.allowedChildren = [_inline2.default, _parchment2.default.Embed, _text2.default];

function bubbleFormats(blot) {
  var formats = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

  if (blot == null) return formats;
  if (typeof blot.formats === 'function') {
    formats = (0, _extend2.default)(formats, blot.formats());
  }
  if (blot.parent == null || blot.parent.blotName == 'scroll' || blot.parent.statics.scope !== blot.statics.scope) {
    return formats;
  }
  return bubbleFormats(blot.parent, formats);
}

exports.bubbleFormats = bubbleFormats;
exports.BlockEmbed = BlockEmbed;
exports.default = Block;

/***/ }),
/* 5 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = exports.overload = exports.expandConfig = undefined;

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

__webpack_require__(50);

var _quillDelta = __webpack_require__(2);

var _quillDelta2 = _interopRequireDefault(_quillDelta);

var _editor = __webpack_require__(14);

var _editor2 = _interopRequireDefault(_editor);

var _emitter3 = __webpack_require__(8);

var _emitter4 = _interopRequireDefault(_emitter3);

var _module = __webpack_require__(9);

var _module2 = _interopRequireDefault(_module);

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _selection = __webpack_require__(15);

var _selection2 = _interopRequireDefault(_selection);

var _extend = __webpack_require__(3);

var _extend2 = _interopRequireDefault(_extend);

var _logger = __webpack_require__(10);

var _logger2 = _interopRequireDefault(_logger);

var _theme = __webpack_require__(34);

var _theme2 = _interopRequireDefault(_theme);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var debug = (0, _logger2.default)('quill');

var Quill = function () {
  _createClass(Quill, null, [{
    key: 'debug',
    value: function debug(limit) {
      if (limit === true) {
        limit = 'log';
      }
      _logger2.default.level(limit);
    }
  }, {
    key: 'find',
    value: function find(node) {
      return node.__quill || _parchment2.default.find(node);
    }
  }, {
    key: 'import',
    value: function _import(name) {
      if (this.imports[name] == null) {
        debug.error('Cannot import ' + name + '. Are you sure it was registered?');
      }
      return this.imports[name];
    }
  }, {
    key: 'register',
    value: function register(path, target) {
      var _this = this;

      var overwrite = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;

      if (typeof path !== 'string') {
        var name = path.attrName || path.blotName;
        if (typeof name === 'string') {
          // register(Blot | Attributor, overwrite)
          this.register('formats/' + name, path, target);
        } else {
          Object.keys(path).forEach(function (key) {
            _this.register(key, path[key], target);
          });
        }
      } else {
        if (this.imports[path] != null && !overwrite) {
          debug.warn('Overwriting ' + path + ' with', target);
        }
        this.imports[path] = target;
        if ((path.startsWith('blots/') || path.startsWith('formats/')) && target.blotName !== 'abstract') {
          _parchment2.default.register(target);
        } else if (path.startsWith('modules') && typeof target.register === 'function') {
          target.register();
        }
      }
    }
  }]);

  function Quill(container) {
    var _this2 = this;

    var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

    _classCallCheck(this, Quill);

    this.options = expandConfig(container, options);
    this.container = this.options.container;
    if (this.container == null) {
      return debug.error('Invalid Quill container', container);
    }
    if (this.options.debug) {
      Quill.debug(this.options.debug);
    }
    var html = this.container.innerHTML.trim();
    this.container.classList.add('ql-container');
    this.container.innerHTML = '';
    this.container.__quill = this;
    this.root = this.addContainer('ql-editor');
    this.root.classList.add('ql-blank');
    this.root.setAttribute('data-gramm', false);
    this.scrollingContainer = this.options.scrollingContainer || this.root;
    this.emitter = new _emitter4.default();
    this.scroll = _parchment2.default.create(this.root, {
      emitter: this.emitter,
      whitelist: this.options.formats
    });
    this.editor = new _editor2.default(this.scroll);
    this.selection = new _selection2.default(this.scroll, this.emitter);
    this.theme = new this.options.theme(this, this.options);
    this.keyboard = this.theme.addModule('keyboard');
    this.clipboard = this.theme.addModule('clipboard');
    this.history = this.theme.addModule('history');
    this.theme.init();
    this.emitter.on(_emitter4.default.events.EDITOR_CHANGE, function (type) {
      if (type === _emitter4.default.events.TEXT_CHANGE) {
        _this2.root.classList.toggle('ql-blank', _this2.editor.isBlank());
      }
    });
    this.emitter.on(_emitter4.default.events.SCROLL_UPDATE, function (source, mutations) {
      var range = _this2.selection.lastRange;
      var index = range && range.length === 0 ? range.index : undefined;
      modify.call(_this2, function () {
        return _this2.editor.update(null, mutations, index);
      }, source);
    });
    var contents = this.clipboard.convert('<div class=\'ql-editor\' style="white-space: normal;">' + html + '<p><br></p></div>');
    this.setContents(contents);
    this.history.clear();
    if (this.options.placeholder) {
      this.root.setAttribute('data-placeholder', this.options.placeholder);
    }
    if (this.options.readOnly) {
      this.disable();
    }
  }

  _createClass(Quill, [{
    key: 'addContainer',
    value: function addContainer(container) {
      var refNode = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;

      if (typeof container === 'string') {
        var className = container;
        container = document.createElement('div');
        container.classList.add(className);
      }
      this.container.insertBefore(container, refNode);
      return container;
    }
  }, {
    key: 'blur',
    value: function blur() {
      this.selection.setRange(null);
    }
  }, {
    key: 'deleteText',
    value: function deleteText(index, length, source) {
      var _this3 = this;

      var _overload = overload(index, length, source);

      var _overload2 = _slicedToArray(_overload, 4);

      index = _overload2[0];
      length = _overload2[1];
      source = _overload2[3];

      return modify.call(this, function () {
        return _this3.editor.deleteText(index, length);
      }, source, index, -1 * length);
    }
  }, {
    key: 'disable',
    value: function disable() {
      this.enable(false);
    }
  }, {
    key: 'enable',
    value: function enable() {
      var enabled = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : true;

      this.scroll.enable(enabled);
      this.container.classList.toggle('ql-disabled', !enabled);
    }
  }, {
    key: 'focus',
    value: function focus() {
      var scrollTop = this.scrollingContainer.scrollTop;
      this.selection.focus();
      this.scrollingContainer.scrollTop = scrollTop;
      this.scrollIntoView();
    }
  }, {
    key: 'format',
    value: function format(name, value) {
      var _this4 = this;

      var source = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : _emitter4.default.sources.API;

      return modify.call(this, function () {
        var range = _this4.getSelection(true);
        var change = new _quillDelta2.default();
        if (range == null) {
          return change;
        } else if (_parchment2.default.query(name, _parchment2.default.Scope.BLOCK)) {
          change = _this4.editor.formatLine(range.index, range.length, _defineProperty({}, name, value));
        } else if (range.length === 0) {
          _this4.selection.format(name, value);
          return change;
        } else {
          change = _this4.editor.formatText(range.index, range.length, _defineProperty({}, name, value));
        }
        _this4.setSelection(range, _emitter4.default.sources.SILENT);
        return change;
      }, source);
    }
  }, {
    key: 'formatLine',
    value: function formatLine(index, length, name, value, source) {
      var _this5 = this;

      var formats = void 0;

      var _overload3 = overload(index, length, name, value, source);

      var _overload4 = _slicedToArray(_overload3, 4);

      index = _overload4[0];
      length = _overload4[1];
      formats = _overload4[2];
      source = _overload4[3];

      return modify.call(this, function () {
        return _this5.editor.formatLine(index, length, formats);
      }, source, index, 0);
    }
  }, {
    key: 'formatText',
    value: function formatText(index, length, name, value, source) {
      var _this6 = this;

      var formats = void 0;

      var _overload5 = overload(index, length, name, value, source);

      var _overload6 = _slicedToArray(_overload5, 4);

      index = _overload6[0];
      length = _overload6[1];
      formats = _overload6[2];
      source = _overload6[3];

      return modify.call(this, function () {
        return _this6.editor.formatText(index, length, formats);
      }, source, index, 0);
    }
  }, {
    key: 'getBounds',
    value: function getBounds(index) {
      var length = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0;

      var bounds = void 0;
      if (typeof index === 'number') {
        bounds = this.selection.getBounds(index, length);
      } else {
        bounds = this.selection.getBounds(index.index, index.length);
      }
      var containerBounds = this.container.getBoundingClientRect();
      return {
        bottom: bounds.bottom - containerBounds.top,
        height: bounds.height,
        left: bounds.left - containerBounds.left,
        right: bounds.right - containerBounds.left,
        top: bounds.top - containerBounds.top,
        width: bounds.width
      };
    }
  }, {
    key: 'getContents',
    value: function getContents() {
      var index = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;
      var length = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : this.getLength() - index;

      var _overload7 = overload(index, length);

      var _overload8 = _slicedToArray(_overload7, 2);

      index = _overload8[0];
      length = _overload8[1];

      return this.editor.getContents(index, length);
    }
  }, {
    key: 'getFormat',
    value: function getFormat() {
      var index = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : this.getSelection(true);
      var length = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0;

      if (typeof index === 'number') {
        return this.editor.getFormat(index, length);
      } else {
        return this.editor.getFormat(index.index, index.length);
      }
    }
  }, {
    key: 'getIndex',
    value: function getIndex(blot) {
      return blot.offset(this.scroll);
    }
  }, {
    key: 'getLength',
    value: function getLength() {
      return this.scroll.length();
    }
  }, {
    key: 'getLeaf',
    value: function getLeaf(index) {
      return this.scroll.leaf(index);
    }
  }, {
    key: 'getLine',
    value: function getLine(index) {
      return this.scroll.line(index);
    }
  }, {
    key: 'getLines',
    value: function getLines() {
      var index = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;
      var length = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : Number.MAX_VALUE;

      if (typeof index !== 'number') {
        return this.scroll.lines(index.index, index.length);
      } else {
        return this.scroll.lines(index, length);
      }
    }
  }, {
    key: 'getModule',
    value: function getModule(name) {
      return this.theme.modules[name];
    }
  }, {
    key: 'getSelection',
    value: function getSelection() {
      var focus = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : false;

      if (focus) this.focus();
      this.update(); // Make sure we access getRange with editor in consistent state
      return this.selection.getRange()[0];
    }
  }, {
    key: 'getText',
    value: function getText() {
      var index = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;
      var length = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : this.getLength() - index;

      var _overload9 = overload(index, length);

      var _overload10 = _slicedToArray(_overload9, 2);

      index = _overload10[0];
      length = _overload10[1];

      return this.editor.getText(index, length);
    }
  }, {
    key: 'hasFocus',
    value: function hasFocus() {
      return this.selection.hasFocus();
    }
  }, {
    key: 'insertEmbed',
    value: function insertEmbed(index, embed, value) {
      var _this7 = this;

      var source = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : Quill.sources.API;

      return modify.call(this, function () {
        return _this7.editor.insertEmbed(index, embed, value);
      }, source, index);
    }
  }, {
    key: 'insertText',
    value: function insertText(index, text, name, value, source) {
      var _this8 = this;

      var formats = void 0;

      var _overload11 = overload(index, 0, name, value, source);

      var _overload12 = _slicedToArray(_overload11, 4);

      index = _overload12[0];
      formats = _overload12[2];
      source = _overload12[3];

      return modify.call(this, function () {
        return _this8.editor.insertText(index, text, formats);
      }, source, index, text.length);
    }
  }, {
    key: 'isEnabled',
    value: function isEnabled() {
      return !this.container.classList.contains('ql-disabled');
    }
  }, {
    key: 'off',
    value: function off() {
      return this.emitter.off.apply(this.emitter, arguments);
    }
  }, {
    key: 'on',
    value: function on() {
      return this.emitter.on.apply(this.emitter, arguments);
    }
  }, {
    key: 'once',
    value: function once() {
      return this.emitter.once.apply(this.emitter, arguments);
    }
  }, {
    key: 'pasteHTML',
    value: function pasteHTML(index, html, source) {
      this.clipboard.dangerouslyPasteHTML(index, html, source);
    }
  }, {
    key: 'removeFormat',
    value: function removeFormat(index, length, source) {
      var _this9 = this;

      var _overload13 = overload(index, length, source);

      var _overload14 = _slicedToArray(_overload13, 4);

      index = _overload14[0];
      length = _overload14[1];
      source = _overload14[3];

      return modify.call(this, function () {
        return _this9.editor.removeFormat(index, length);
      }, source, index);
    }
  }, {
    key: 'scrollIntoView',
    value: function scrollIntoView() {
      this.selection.scrollIntoView(this.scrollingContainer);
    }
  }, {
    key: 'setContents',
    value: function setContents(delta) {
      var _this10 = this;

      var source = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : _emitter4.default.sources.API;

      return modify.call(this, function () {
        delta = new _quillDelta2.default(delta);
        var length = _this10.getLength();
        var deleted = _this10.editor.deleteText(0, length);
        var applied = _this10.editor.applyDelta(delta);
        var lastOp = applied.ops[applied.ops.length - 1];
        if (lastOp != null && typeof lastOp.insert === 'string' && lastOp.insert[lastOp.insert.length - 1] === '\n') {
          _this10.editor.deleteText(_this10.getLength() - 1, 1);
          applied.delete(1);
        }
        var ret = deleted.compose(applied);
        return ret;
      }, source);
    }
  }, {
    key: 'setSelection',
    value: function setSelection(index, length, source) {
      if (index == null) {
        this.selection.setRange(null, length || Quill.sources.API);
      } else {
        var _overload15 = overload(index, length, source);

        var _overload16 = _slicedToArray(_overload15, 4);

        index = _overload16[0];
        length = _overload16[1];
        source = _overload16[3];

        this.selection.setRange(new _selection.Range(index, length), source);
        if (source !== _emitter4.default.sources.SILENT) {
          this.selection.scrollIntoView(this.scrollingContainer);
        }
      }
    }
  }, {
    key: 'setText',
    value: function setText(text) {
      var source = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : _emitter4.default.sources.API;

      var delta = new _quillDelta2.default().insert(text);
      return this.setContents(delta, source);
    }
  }, {
    key: 'update',
    value: function update() {
      var source = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : _emitter4.default.sources.USER;

      var change = this.scroll.update(source); // Will update selection before selection.update() does if text changes
      this.selection.update(source);
      return change;
    }
  }, {
    key: 'updateContents',
    value: function updateContents(delta) {
      var _this11 = this;

      var source = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : _emitter4.default.sources.API;

      return modify.call(this, function () {
        delta = new _quillDelta2.default(delta);
        return _this11.editor.applyDelta(delta, source);
      }, source, true);
    }
  }]);

  return Quill;
}();

Quill.DEFAULTS = {
  bounds: null,
  formats: null,
  modules: {},
  placeholder: '',
  readOnly: false,
  scrollingContainer: null,
  strict: true,
  theme: 'default'
};
Quill.events = _emitter4.default.events;
Quill.sources = _emitter4.default.sources;
// eslint-disable-next-line no-undef
Quill.version =  false ? 'dev' : "1.3.6";

Quill.imports = {
  'delta': _quillDelta2.default,
  'parchment': _parchment2.default,
  'core/module': _module2.default,
  'core/theme': _theme2.default
};

function expandConfig(container, userConfig) {
  userConfig = (0, _extend2.default)(true, {
    container: container,
    modules: {
      clipboard: true,
      keyboard: true,
      history: true
    }
  }, userConfig);
  if (!userConfig.theme || userConfig.theme === Quill.DEFAULTS.theme) {
    userConfig.theme = _theme2.default;
  } else {
    userConfig.theme = Quill.import('themes/' + userConfig.theme);
    if (userConfig.theme == null) {
      throw new Error('Invalid theme ' + userConfig.theme + '. Did you register it?');
    }
  }
  var themeConfig = (0, _extend2.default)(true, {}, userConfig.theme.DEFAULTS);
  [themeConfig, userConfig].forEach(function (config) {
    config.modules = config.modules || {};
    Object.keys(config.modules).forEach(function (module) {
      if (config.modules[module] === true) {
        config.modules[module] = {};
      }
    });
  });
  var moduleNames = Object.keys(themeConfig.modules).concat(Object.keys(userConfig.modules));
  var moduleConfig = moduleNames.reduce(function (config, name) {
    var moduleClass = Quill.import('modules/' + name);
    if (moduleClass == null) {
      debug.error('Cannot load ' + name + ' module. Are you sure you registered it?');
    } else {
      config[name] = moduleClass.DEFAULTS || {};
    }
    return config;
  }, {});
  // Special case toolbar shorthand
  if (userConfig.modules != null && userConfig.modules.toolbar && userConfig.modules.toolbar.constructor !== Object) {
    userConfig.modules.toolbar = {
      container: userConfig.modules.toolbar
    };
  }
  userConfig = (0, _extend2.default)(true, {}, Quill.DEFAULTS, { modules: moduleConfig }, themeConfig, userConfig);
  ['bounds', 'container', 'scrollingContainer'].forEach(function (key) {
    if (typeof userConfig[key] === 'string') {
      userConfig[key] = document.querySelector(userConfig[key]);
    }
  });
  userConfig.modules = Object.keys(userConfig.modules).reduce(function (config, name) {
    if (userConfig.modules[name]) {
      config[name] = userConfig.modules[name];
    }
    return config;
  }, {});
  return userConfig;
}

// Handle selection preservation and TEXT_CHANGE emission
// common to modification APIs
function modify(modifier, source, index, shift) {
  if (this.options.strict && !this.isEnabled() && source === _emitter4.default.sources.USER) {
    return new _quillDelta2.default();
  }
  var range = index == null ? null : this.getSelection();
  var oldDelta = this.editor.delta;
  var change = modifier();
  if (range != null) {
    if (index === true) index = range.index;
    if (shift == null) {
      range = shiftRange(range, change, source);
    } else if (shift !== 0) {
      range = shiftRange(range, index, shift, source);
    }
    this.setSelection(range, _emitter4.default.sources.SILENT);
  }
  if (change.length() > 0) {
    var _emitter;

    var args = [_emitter4.default.events.TEXT_CHANGE, change, oldDelta, source];
    (_emitter = this.emitter).emit.apply(_emitter, [_emitter4.default.events.EDITOR_CHANGE].concat(args));
    if (source !== _emitter4.default.sources.SILENT) {
      var _emitter2;

      (_emitter2 = this.emitter).emit.apply(_emitter2, args);
    }
  }
  return change;
}

function overload(index, length, name, value, source) {
  var formats = {};
  if (typeof index.index === 'number' && typeof index.length === 'number') {
    // Allow for throwaway end (used by insertText/insertEmbed)
    if (typeof length !== 'number') {
      source = value, value = name, name = length, length = index.length, index = index.index;
    } else {
      length = index.length, index = index.index;
    }
  } else if (typeof length !== 'number') {
    source = value, value = name, name = length, length = 0;
  }
  // Handle format being object, two format name/value strings or excluded
  if ((typeof name === 'undefined' ? 'undefined' : _typeof(name)) === 'object') {
    formats = name;
    source = value;
  } else if (typeof name === 'string') {
    if (value != null) {
      formats[name] = value;
    } else {
      source = name;
    }
  }
  // Handle optional source
  source = source || _emitter4.default.sources.API;
  return [index, length, formats, source];
}

function shiftRange(range, index, length, source) {
  if (range == null) return null;
  var start = void 0,
      end = void 0;
  if (index instanceof _quillDelta2.default) {
    var _map = [range.index, range.index + range.length].map(function (pos) {
      return index.transformPosition(pos, source !== _emitter4.default.sources.USER);
    });

    var _map2 = _slicedToArray(_map, 2);

    start = _map2[0];
    end = _map2[1];
  } else {
    var _map3 = [range.index, range.index + range.length].map(function (pos) {
      if (pos < index || pos === index && source === _emitter4.default.sources.USER) return pos;
      if (length >= 0) {
        return pos + length;
      } else {
        return Math.max(index, pos + length);
      }
    });

    var _map4 = _slicedToArray(_map3, 2);

    start = _map4[0];
    end = _map4[1];
  }
  return new _selection.Range(start, end - start);
}

exports.expandConfig = expandConfig;
exports.overload = overload;
exports.default = Quill;

/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _text = __webpack_require__(7);

var _text2 = _interopRequireDefault(_text);

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Inline = function (_Parchment$Inline) {
  _inherits(Inline, _Parchment$Inline);

  function Inline() {
    _classCallCheck(this, Inline);

    return _possibleConstructorReturn(this, (Inline.__proto__ || Object.getPrototypeOf(Inline)).apply(this, arguments));
  }

  _createClass(Inline, [{
    key: 'formatAt',
    value: function formatAt(index, length, name, value) {
      if (Inline.compare(this.statics.blotName, name) < 0 && _parchment2.default.query(name, _parchment2.default.Scope.BLOT)) {
        var blot = this.isolate(index, length);
        if (value) {
          blot.wrap(name, value);
        }
      } else {
        _get(Inline.prototype.__proto__ || Object.getPrototypeOf(Inline.prototype), 'formatAt', this).call(this, index, length, name, value);
      }
    }
  }, {
    key: 'optimize',
    value: function optimize(context) {
      _get(Inline.prototype.__proto__ || Object.getPrototypeOf(Inline.prototype), 'optimize', this).call(this, context);
      if (this.parent instanceof Inline && Inline.compare(this.statics.blotName, this.parent.statics.blotName) > 0) {
        var parent = this.parent.isolate(this.offset(), this.length());
        this.moveChildren(parent);
        parent.wrap(this);
      }
    }
  }], [{
    key: 'compare',
    value: function compare(self, other) {
      var selfIndex = Inline.order.indexOf(self);
      var otherIndex = Inline.order.indexOf(other);
      if (selfIndex >= 0 || otherIndex >= 0) {
        return selfIndex - otherIndex;
      } else if (self === other) {
        return 0;
      } else if (self < other) {
        return -1;
      } else {
        return 1;
      }
    }
  }]);

  return Inline;
}(_parchment2.default.Inline);

Inline.allowedChildren = [Inline, _parchment2.default.Embed, _text2.default];
// Lower index means deeper in the DOM tree, since not found (-1) is for embeds
Inline.order = ['cursor', 'inline', // Must be lower
'underline', 'strike', 'italic', 'bold', 'script', 'link', 'code' // Must be higher
];

exports.default = Inline;

/***/ }),
/* 7 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var TextBlot = function (_Parchment$Text) {
  _inherits(TextBlot, _Parchment$Text);

  function TextBlot() {
    _classCallCheck(this, TextBlot);

    return _possibleConstructorReturn(this, (TextBlot.__proto__ || Object.getPrototypeOf(TextBlot)).apply(this, arguments));
  }

  return TextBlot;
}(_parchment2.default.Text);

exports.default = TextBlot;

/***/ }),
/* 8 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _eventemitter = __webpack_require__(54);

var _eventemitter2 = _interopRequireDefault(_eventemitter);

var _logger = __webpack_require__(10);

var _logger2 = _interopRequireDefault(_logger);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var debug = (0, _logger2.default)('quill:events');

var EVENTS = ['selectionchange', 'mousedown', 'mouseup', 'click'];

EVENTS.forEach(function (eventName) {
  document.addEventListener(eventName, function () {
    for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    [].slice.call(document.querySelectorAll('.ql-container')).forEach(function (node) {
      // TODO use WeakMap
      if (node.__quill && node.__quill.emitter) {
        var _node$__quill$emitter;

        (_node$__quill$emitter = node.__quill.emitter).handleDOM.apply(_node$__quill$emitter, args);
      }
    });
  });
});

var Emitter = function (_EventEmitter) {
  _inherits(Emitter, _EventEmitter);

  function Emitter() {
    _classCallCheck(this, Emitter);

    var _this = _possibleConstructorReturn(this, (Emitter.__proto__ || Object.getPrototypeOf(Emitter)).call(this));

    _this.listeners = {};
    _this.on('error', debug.error);
    return _this;
  }

  _createClass(Emitter, [{
    key: 'emit',
    value: function emit() {
      debug.log.apply(debug, arguments);
      _get(Emitter.prototype.__proto__ || Object.getPrototypeOf(Emitter.prototype), 'emit', this).apply(this, arguments);
    }
  }, {
    key: 'handleDOM',
    value: function handleDOM(event) {
      for (var _len2 = arguments.length, args = Array(_len2 > 1 ? _len2 - 1 : 0), _key2 = 1; _key2 < _len2; _key2++) {
        args[_key2 - 1] = arguments[_key2];
      }

      (this.listeners[event.type] || []).forEach(function (_ref) {
        var node = _ref.node,
            handler = _ref.handler;

        if (event.target === node || node.contains(event.target)) {
          handler.apply(undefined, [event].concat(args));
        }
      });
    }
  }, {
    key: 'listenDOM',
    value: function listenDOM(eventName, node, handler) {
      if (!this.listeners[eventName]) {
        this.listeners[eventName] = [];
      }
      this.listeners[eventName].push({ node: node, handler: handler });
    }
  }]);

  return Emitter;
}(_eventemitter2.default);

Emitter.events = {
  EDITOR_CHANGE: 'editor-change',
  SCROLL_BEFORE_UPDATE: 'scroll-before-update',
  SCROLL_OPTIMIZE: 'scroll-optimize',
  SCROLL_UPDATE: 'scroll-update',
  SELECTION_CHANGE: 'selection-change',
  TEXT_CHANGE: 'text-change'
};
Emitter.sources = {
  API: 'api',
  SILENT: 'silent',
  USER: 'user'
};

exports.default = Emitter;

/***/ }),
/* 9 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Module = function Module(quill) {
  var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

  _classCallCheck(this, Module);

  this.quill = quill;
  this.options = options;
};

Module.DEFAULTS = {};

exports.default = Module;

/***/ }),
/* 10 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
var levels = ['error', 'warn', 'log', 'info'];
var level = 'warn';

function debug(method) {
  if (levels.indexOf(method) <= levels.indexOf(level)) {
    var _console;

    for (var _len = arguments.length, args = Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
      args[_key - 1] = arguments[_key];
    }

    (_console = console)[method].apply(_console, args); // eslint-disable-line no-console
  }
}

function namespace(ns) {
  return levels.reduce(function (logger, method) {
    logger[method] = debug.bind(console, method, ns);
    return logger;
  }, {});
}

debug.level = namespace.level = function (newLevel) {
  level = newLevel;
};

exports.default = namespace;

/***/ }),
/* 11 */
/***/ (function(module, exports, __webpack_require__) {

var pSlice = Array.prototype.slice;
var objectKeys = __webpack_require__(52);
var isArguments = __webpack_require__(53);

var deepEqual = module.exports = function (actual, expected, opts) {
  if (!opts) opts = {};
  // 7.1. All identical values are equivalent, as determined by ===.
  if (actual === expected) {
    return true;

  } else if (actual instanceof Date && expected instanceof Date) {
    return actual.getTime() === expected.getTime();

  // 7.3. Other pairs that do not both pass typeof value == 'object',
  // equivalence is determined by ==.
  } else if (!actual || !expected || typeof actual != 'object' && typeof expected != 'object') {
    return opts.strict ? actual === expected : actual == expected;

  // 7.4. For all other Object pairs, including Array objects, equivalence is
  // determined by having the same number of owned properties (as verified
  // with Object.prototype.hasOwnProperty.call), the same set of keys
  // (although not necessarily the same order), equivalent values for every
  // corresponding key, and an identical 'prototype' property. Note: this
  // accounts for both named and indexed properties on Arrays.
  } else {
    return objEquiv(actual, expected, opts);
  }
}

function isUndefinedOrNull(value) {
  return value === null || value === undefined;
}

function isBuffer (x) {
  if (!x || typeof x !== 'object' || typeof x.length !== 'number') return false;
  if (typeof x.copy !== 'function' || typeof x.slice !== 'function') {
    return false;
  }
  if (x.length > 0 && typeof x[0] !== 'number') return false;
  return true;
}

function objEquiv(a, b, opts) {
  var i, key;
  if (isUndefinedOrNull(a) || isUndefinedOrNull(b))
    return false;
  // an identical 'prototype' property.
  if (a.prototype !== b.prototype) return false;
  //~~~I've managed to break Object.keys through screwy arguments passing.
  //   Converting to array solves the problem.
  if (isArguments(a)) {
    if (!isArguments(b)) {
      return false;
    }
    a = pSlice.call(a);
    b = pSlice.call(b);
    return deepEqual(a, b, opts);
  }
  if (isBuffer(a)) {
    if (!isBuffer(b)) {
      return false;
    }
    if (a.length !== b.length) return false;
    for (i = 0; i < a.length; i++) {
      if (a[i] !== b[i]) return false;
    }
    return true;
  }
  try {
    var ka = objectKeys(a),
        kb = objectKeys(b);
  } catch (e) {//happens when one is a string literal and the other isn't
    return false;
  }
  // having the same number of owned properties (keys incorporates
  // hasOwnProperty)
  if (ka.length != kb.length)
    return false;
  //the same set of keys (although not necessarily the same order),
  ka.sort();
  kb.sort();
  //~~~cheap key test
  for (i = ka.length - 1; i >= 0; i--) {
    if (ka[i] != kb[i])
      return false;
  }
  //equivalent values for every corresponding key, and
  //~~~possibly expensive deep test
  for (i = ka.length - 1; i >= 0; i--) {
    key = ka[i];
    if (!deepEqual(a[key], b[key], opts)) return false;
  }
  return typeof a === typeof b;
}


/***/ }),
/* 12 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var Registry = __webpack_require__(1);
var Attributor = /** @class */ (function () {
    function Attributor(attrName, keyName, options) {
        if (options === void 0) { options = {}; }
        this.attrName = attrName;
        this.keyName = keyName;
        var attributeBit = Registry.Scope.TYPE & Registry.Scope.ATTRIBUTE;
        if (options.scope != null) {
            // Ignore type bits, force attribute bit
            this.scope = (options.scope & Registry.Scope.LEVEL) | attributeBit;
        }
        else {
            this.scope = Registry.Scope.ATTRIBUTE;
        }
        if (options.whitelist != null)
            this.whitelist = options.whitelist;
    }
    Attributor.keys = function (node) {
        return [].map.call(node.attributes, function (item) {
            return item.name;
        });
    };
    Attributor.prototype.add = function (node, value) {
        if (!this.canAdd(node, value))
            return false;
        node.setAttribute(this.keyName, value);
        return true;
    };
    Attributor.prototype.canAdd = function (node, value) {
        var match = Registry.query(node, Registry.Scope.BLOT & (this.scope | Registry.Scope.TYPE));
        if (match == null)
            return false;
        if (this.whitelist == null)
            return true;
        if (typeof value === 'string') {
            return this.whitelist.indexOf(value.replace(/["']/g, '')) > -1;
        }
        else {
            return this.whitelist.indexOf(value) > -1;
        }
    };
    Attributor.prototype.remove = function (node) {
        node.removeAttribute(this.keyName);
    };
    Attributor.prototype.value = function (node) {
        var value = node.getAttribute(this.keyName);
        if (this.canAdd(node, value) && value) {
            return value;
        }
        return '';
    };
    return Attributor;
}());
exports.default = Attributor;


/***/ }),
/* 13 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = exports.Code = undefined;

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _quillDelta = __webpack_require__(2);

var _quillDelta2 = _interopRequireDefault(_quillDelta);

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _block = __webpack_require__(4);

var _block2 = _interopRequireDefault(_block);

var _inline = __webpack_require__(6);

var _inline2 = _interopRequireDefault(_inline);

var _text = __webpack_require__(7);

var _text2 = _interopRequireDefault(_text);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Code = function (_Inline) {
  _inherits(Code, _Inline);

  function Code() {
    _classCallCheck(this, Code);

    return _possibleConstructorReturn(this, (Code.__proto__ || Object.getPrototypeOf(Code)).apply(this, arguments));
  }

  return Code;
}(_inline2.default);

Code.blotName = 'code';
Code.tagName = 'CODE';

var CodeBlock = function (_Block) {
  _inherits(CodeBlock, _Block);

  function CodeBlock() {
    _classCallCheck(this, CodeBlock);

    return _possibleConstructorReturn(this, (CodeBlock.__proto__ || Object.getPrototypeOf(CodeBlock)).apply(this, arguments));
  }

  _createClass(CodeBlock, [{
    key: 'delta',
    value: function delta() {
      var _this3 = this;

      var text = this.domNode.textContent;
      if (text.endsWith('\n')) {
        // Should always be true
        text = text.slice(0, -1);
      }
      return text.split('\n').reduce(function (delta, frag) {
        return delta.insert(frag).insert('\n', _this3.formats());
      }, new _quillDelta2.default());
    }
  }, {
    key: 'format',
    value: function format(name, value) {
      if (name === this.statics.blotName && value) return;

      var _descendant = this.descendant(_text2.default, this.length() - 1),
          _descendant2 = _slicedToArray(_descendant, 1),
          text = _descendant2[0];

      if (text != null) {
        text.deleteAt(text.length() - 1, 1);
      }
      _get(CodeBlock.prototype.__proto__ || Object.getPrototypeOf(CodeBlock.prototype), 'format', this).call(this, name, value);
    }
  }, {
    key: 'formatAt',
    value: function formatAt(index, length, name, value) {
      if (length === 0) return;
      if (_parchment2.default.query(name, _parchment2.default.Scope.BLOCK) == null || name === this.statics.blotName && value === this.statics.formats(this.domNode)) {
        return;
      }
      var nextNewline = this.newlineIndex(index);
      if (nextNewline < 0 || nextNewline >= index + length) return;
      var prevNewline = this.newlineIndex(index, true) + 1;
      var isolateLength = nextNewline - prevNewline + 1;
      var blot = this.isolate(prevNewline, isolateLength);
      var next = blot.next;
      blot.format(name, value);
      if (next instanceof CodeBlock) {
        next.formatAt(0, index - prevNewline + length - isolateLength, name, value);
      }
    }
  }, {
    key: 'insertAt',
    value: function insertAt(index, value, def) {
      if (def != null) return;

      var _descendant3 = this.descendant(_text2.default, index),
          _descendant4 = _slicedToArray(_descendant3, 2),
          text = _descendant4[0],
          offset = _descendant4[1];

      text.insertAt(offset, value);
    }
  }, {
    key: 'length',
    value: function length() {
      var length = this.domNode.textContent.length;
      if (!this.domNode.textContent.endsWith('\n')) {
        return length + 1;
      }
      return length;
    }
  }, {
    key: 'newlineIndex',
    value: function newlineIndex(searchIndex) {
      var reverse = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;

      if (!reverse) {
        var offset = this.domNode.textContent.slice(searchIndex).indexOf('\n');
        return offset > -1 ? searchIndex + offset : -1;
      } else {
        return this.domNode.textContent.slice(0, searchIndex).lastIndexOf('\n');
      }
    }
  }, {
    key: 'optimize',
    value: function optimize(context) {
      if (!this.domNode.textContent.endsWith('\n')) {
        this.appendChild(_parchment2.default.create('text', '\n'));
      }
      _get(CodeBlock.prototype.__proto__ || Object.getPrototypeOf(CodeBlock.prototype), 'optimize', this).call(this, context);
      var next = this.next;
      if (next != null && next.prev === this && next.statics.blotName === this.statics.blotName && this.statics.formats(this.domNode) === next.statics.formats(next.domNode)) {
        next.optimize(context);
        next.moveChildren(this);
        next.remove();
      }
    }
  }, {
    key: 'replace',
    value: function replace(target) {
      _get(CodeBlock.prototype.__proto__ || Object.getPrototypeOf(CodeBlock.prototype), 'replace', this).call(this, target);
      [].slice.call(this.domNode.querySelectorAll('*')).forEach(function (node) {
        var blot = _parchment2.default.find(node);
        if (blot == null) {
          node.parentNode.removeChild(node);
        } else if (blot instanceof _parchment2.default.Embed) {
          blot.remove();
        } else {
          blot.unwrap();
        }
      });
    }
  }], [{
    key: 'create',
    value: function create(value) {
      var domNode = _get(CodeBlock.__proto__ || Object.getPrototypeOf(CodeBlock), 'create', this).call(this, value);
      domNode.setAttribute('spellcheck', false);
      return domNode;
    }
  }, {
    key: 'formats',
    value: function formats() {
      return true;
    }
  }]);

  return CodeBlock;
}(_block2.default);

CodeBlock.blotName = 'code-block';
CodeBlock.tagName = 'PRE';
CodeBlock.TAB = '  ';

exports.Code = Code;
exports.default = CodeBlock;

/***/ }),
/* 14 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _quillDelta = __webpack_require__(2);

var _quillDelta2 = _interopRequireDefault(_quillDelta);

var _op = __webpack_require__(20);

var _op2 = _interopRequireDefault(_op);

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _code = __webpack_require__(13);

var _code2 = _interopRequireDefault(_code);

var _cursor = __webpack_require__(24);

var _cursor2 = _interopRequireDefault(_cursor);

var _block = __webpack_require__(4);

var _block2 = _interopRequireDefault(_block);

var _break = __webpack_require__(16);

var _break2 = _interopRequireDefault(_break);

var _clone = __webpack_require__(21);

var _clone2 = _interopRequireDefault(_clone);

var _deepEqual = __webpack_require__(11);

var _deepEqual2 = _interopRequireDefault(_deepEqual);

var _extend = __webpack_require__(3);

var _extend2 = _interopRequireDefault(_extend);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var ASCII = /^[ -~]*$/;

var Editor = function () {
  function Editor(scroll) {
    _classCallCheck(this, Editor);

    this.scroll = scroll;
    this.delta = this.getDelta();
  }

  _createClass(Editor, [{
    key: 'applyDelta',
    value: function applyDelta(delta) {
      var _this = this;

      var consumeNextNewline = false;
      this.scroll.update();
      var scrollLength = this.scroll.length();
      this.scroll.batchStart();
      delta = normalizeDelta(delta);
      delta.reduce(function (index, op) {
        var length = op.retain || op.delete || op.insert.length || 1;
        var attributes = op.attributes || {};
        if (op.insert != null) {
          if (typeof op.insert === 'string') {
            var text = op.insert;
            if (text.endsWith('\n') && consumeNextNewline) {
              consumeNextNewline = false;
              text = text.slice(0, -1);
            }
            if (index >= scrollLength && !text.endsWith('\n')) {
              consumeNextNewline = true;
            }
            _this.scroll.insertAt(index, text);

            var _scroll$line = _this.scroll.line(index),
                _scroll$line2 = _slicedToArray(_scroll$line, 2),
                line = _scroll$line2[0],
                offset = _scroll$line2[1];

            var formats = (0, _extend2.default)({}, (0, _block.bubbleFormats)(line));
            if (line instanceof _block2.default) {
              var _line$descendant = line.descendant(_parchment2.default.Leaf, offset),
                  _line$descendant2 = _slicedToArray(_line$descendant, 1),
                  leaf = _line$descendant2[0];

              formats = (0, _extend2.default)(formats, (0, _block.bubbleFormats)(leaf));
            }
            attributes = _op2.default.attributes.diff(formats, attributes) || {};
          } else if (_typeof(op.insert) === 'object') {
            var key = Object.keys(op.insert)[0]; // There should only be one key
            if (key == null) return index;
            _this.scroll.insertAt(index, key, op.insert[key]);
          }
          scrollLength += length;
        }
        Object.keys(attributes).forEach(function (name) {
          _this.scroll.formatAt(index, length, name, attributes[name]);
        });
        return index + length;
      }, 0);
      delta.reduce(function (index, op) {
        if (typeof op.delete === 'number') {
          _this.scroll.deleteAt(index, op.delete);
          return index;
        }
        return index + (op.retain || op.insert.length || 1);
      }, 0);
      this.scroll.batchEnd();
      return this.update(delta);
    }
  }, {
    key: 'deleteText',
    value: function deleteText(index, length) {
      this.scroll.deleteAt(index, length);
      return this.update(new _quillDelta2.default().retain(index).delete(length));
    }
  }, {
    key: 'formatLine',
    value: function formatLine(index, length) {
      var _this2 = this;

      var formats = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};

      this.scroll.update();
      Object.keys(formats).forEach(function (format) {
        if (_this2.scroll.whitelist != null && !_this2.scroll.whitelist[format]) return;
        var lines = _this2.scroll.lines(index, Math.max(length, 1));
        var lengthRemaining = length;
        lines.forEach(function (line) {
          var lineLength = line.length();
          if (!(line instanceof _code2.default)) {
            line.format(format, formats[format]);
          } else {
            var codeIndex = index - line.offset(_this2.scroll);
            var codeLength = line.newlineIndex(codeIndex + lengthRemaining) - codeIndex + 1;
            line.formatAt(codeIndex, codeLength, format, formats[format]);
          }
          lengthRemaining -= lineLength;
        });
      });
      this.scroll.optimize();
      return this.update(new _quillDelta2.default().retain(index).retain(length, (0, _clone2.default)(formats)));
    }
  }, {
    key: 'formatText',
    value: function formatText(index, length) {
      var _this3 = this;

      var formats = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};

      Object.keys(formats).forEach(function (format) {
        _this3.scroll.formatAt(index, length, format, formats[format]);
      });
      return this.update(new _quillDelta2.default().retain(index).retain(length, (0, _clone2.default)(formats)));
    }
  }, {
    key: 'getContents',
    value: function getContents(index, length) {
      return this.delta.slice(index, index + length);
    }
  }, {
    key: 'getDelta',
    value: function getDelta() {
      return this.scroll.lines().reduce(function (delta, line) {
        return delta.concat(line.delta());
      }, new _quillDelta2.default());
    }
  }, {
    key: 'getFormat',
    value: function getFormat(index) {
      var length = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0;

      var lines = [],
          leaves = [];
      if (length === 0) {
        this.scroll.path(index).forEach(function (path) {
          var _path = _slicedToArray(path, 1),
              blot = _path[0];

          if (blot instanceof _block2.default) {
            lines.push(blot);
          } else if (blot instanceof _parchment2.default.Leaf) {
            leaves.push(blot);
          }
        });
      } else {
        lines = this.scroll.lines(index, length);
        leaves = this.scroll.descendants(_parchment2.default.Leaf, index, length);
      }
      var formatsArr = [lines, leaves].map(function (blots) {
        if (blots.length === 0) return {};
        var formats = (0, _block.bubbleFormats)(blots.shift());
        while (Object.keys(formats).length > 0) {
          var blot = blots.shift();
          if (blot == null) return formats;
          formats = combineFormats((0, _block.bubbleFormats)(blot), formats);
        }
        return formats;
      });
      return _extend2.default.apply(_extend2.default, formatsArr);
    }
  }, {
    key: 'getText',
    value: function getText(index, length) {
      return this.getContents(index, length).filter(function (op) {
        return typeof op.insert === 'string';
      }).map(function (op) {
        return op.insert;
      }).join('');
    }
  }, {
    key: 'insertEmbed',
    value: function insertEmbed(index, embed, value) {
      this.scroll.insertAt(index, embed, value);
      return this.update(new _quillDelta2.default().retain(index).insert(_defineProperty({}, embed, value)));
    }
  }, {
    key: 'insertText',
    value: function insertText(index, text) {
      var _this4 = this;

      var formats = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};

      text = text.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      this.scroll.insertAt(index, text);
      Object.keys(formats).forEach(function (format) {
        _this4.scroll.formatAt(index, text.length, format, formats[format]);
      });
      return this.update(new _quillDelta2.default().retain(index).insert(text, (0, _clone2.default)(formats)));
    }
  }, {
    key: 'isBlank',
    value: function isBlank() {
      if (this.scroll.children.length == 0) return true;
      if (this.scroll.children.length > 1) return false;
      var block = this.scroll.children.head;
      if (block.statics.blotName !== _block2.default.blotName) return false;
      if (block.children.length > 1) return false;
      return block.children.head instanceof _break2.default;
    }
  }, {
    key: 'removeFormat',
    value: function removeFormat(index, length) {
      var text = this.getText(index, length);

      var _scroll$line3 = this.scroll.line(index + length),
          _scroll$line4 = _slicedToArray(_scroll$line3, 2),
          line = _scroll$line4[0],
          offset = _scroll$line4[1];

      var suffixLength = 0,
          suffix = new _quillDelta2.default();
      if (line != null) {
        if (!(line instanceof _code2.default)) {
          suffixLength = line.length() - offset;
        } else {
          suffixLength = line.newlineIndex(offset) - offset + 1;
        }
        suffix = line.delta().slice(offset, offset + suffixLength - 1).insert('\n');
      }
      var contents = this.getContents(index, length + suffixLength);
      var diff = contents.diff(new _quillDelta2.default().insert(text).concat(suffix));
      var delta = new _quillDelta2.default().retain(index).concat(diff);
      return this.applyDelta(delta);
    }
  }, {
    key: 'update',
    value: function update(change) {
      var mutations = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : [];
      var cursorIndex = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : undefined;

      var oldDelta = this.delta;
      if (mutations.length === 1 && mutations[0].type === 'characterData' && mutations[0].target.data.match(ASCII) && _parchment2.default.find(mutations[0].target)) {
        // Optimization for character changes
        var textBlot = _parchment2.default.find(mutations[0].target);
        var formats = (0, _block.bubbleFormats)(textBlot);
        var index = textBlot.offset(this.scroll);
        var oldValue = mutations[0].oldValue.replace(_cursor2.default.CONTENTS, '');
        var oldText = new _quillDelta2.default().insert(oldValue);
        var newText = new _quillDelta2.default().insert(textBlot.value());
        var diffDelta = new _quillDelta2.default().retain(index).concat(oldText.diff(newText, cursorIndex));
        change = diffDelta.reduce(function (delta, op) {
          if (op.insert) {
            return delta.insert(op.insert, formats);
          } else {
            return delta.push(op);
          }
        }, new _quillDelta2.default());
        this.delta = oldDelta.compose(change);
      } else {
        this.delta = this.getDelta();
        if (!change || !(0, _deepEqual2.default)(oldDelta.compose(change), this.delta)) {
          change = oldDelta.diff(this.delta, cursorIndex);
        }
      }
      return change;
    }
  }]);

  return Editor;
}();

function combineFormats(formats, combined) {
  return Object.keys(combined).reduce(function (merged, name) {
    if (formats[name] == null) return merged;
    if (combined[name] === formats[name]) {
      merged[name] = combined[name];
    } else if (Array.isArray(combined[name])) {
      if (combined[name].indexOf(formats[name]) < 0) {
        merged[name] = combined[name].concat([formats[name]]);
      }
    } else {
      merged[name] = [combined[name], formats[name]];
    }
    return merged;
  }, {});
}

function normalizeDelta(delta) {
  return delta.reduce(function (delta, op) {
    if (op.insert === 1) {
      var attributes = (0, _clone2.default)(op.attributes);
      delete attributes['image'];
      return delta.insert({ image: op.attributes.image }, attributes);
    }
    if (op.attributes != null && (op.attributes.list === true || op.attributes.bullet === true)) {
      op = (0, _clone2.default)(op);
      if (op.attributes.list) {
        op.attributes.list = 'ordered';
      } else {
        op.attributes.list = 'bullet';
        delete op.attributes.bullet;
      }
    }
    if (typeof op.insert === 'string') {
      var text = op.insert.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      return delta.insert(text, op.attributes);
    }
    return delta.push(op);
  }, new _quillDelta2.default());
}

exports.default = Editor;

/***/ }),
/* 15 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = exports.Range = undefined;

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _clone = __webpack_require__(21);

var _clone2 = _interopRequireDefault(_clone);

var _deepEqual = __webpack_require__(11);

var _deepEqual2 = _interopRequireDefault(_deepEqual);

var _emitter3 = __webpack_require__(8);

var _emitter4 = _interopRequireDefault(_emitter3);

var _logger = __webpack_require__(10);

var _logger2 = _interopRequireDefault(_logger);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var debug = (0, _logger2.default)('quill:selection');

var Range = function Range(index) {
  var length = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0;

  _classCallCheck(this, Range);

  this.index = index;
  this.length = length;
};

var Selection = function () {
  function Selection(scroll, emitter) {
    var _this = this;

    _classCallCheck(this, Selection);

    this.emitter = emitter;
    this.scroll = scroll;
    this.composing = false;
    this.mouseDown = false;
    this.root = this.scroll.domNode;
    this.cursor = _parchment2.default.create('cursor', this);
    // savedRange is last non-null range
    this.lastRange = this.savedRange = new Range(0, 0);
    this.handleComposition();
    this.handleDragging();
    this.emitter.listenDOM('selectionchange', document, function () {
      if (!_this.mouseDown) {
        setTimeout(_this.update.bind(_this, _emitter4.default.sources.USER), 1);
      }
    });
    this.emitter.on(_emitter4.default.events.EDITOR_CHANGE, function (type, delta) {
      if (type === _emitter4.default.events.TEXT_CHANGE && delta.length() > 0) {
        _this.update(_emitter4.default.sources.SILENT);
      }
    });
    this.emitter.on(_emitter4.default.events.SCROLL_BEFORE_UPDATE, function () {
      if (!_this.hasFocus()) return;
      var native = _this.getNativeRange();
      if (native == null) return;
      if (native.start.node === _this.cursor.textNode) return; // cursor.restore() will handle
      // TODO unclear if this has negative side effects
      _this.emitter.once(_emitter4.default.events.SCROLL_UPDATE, function () {
        try {
          _this.setNativeRange(native.start.node, native.start.offset, native.end.node, native.end.offset);
        } catch (ignored) {}
      });
    });
    this.emitter.on(_emitter4.default.events.SCROLL_OPTIMIZE, function (mutations, context) {
      if (context.range) {
        var _context$range = context.range,
            startNode = _context$range.startNode,
            startOffset = _context$range.startOffset,
            endNode = _context$range.endNode,
            endOffset = _context$range.endOffset;

        _this.setNativeRange(startNode, startOffset, endNode, endOffset);
      }
    });
    this.update(_emitter4.default.sources.SILENT);
  }

  _createClass(Selection, [{
    key: 'handleComposition',
    value: function handleComposition() {
      var _this2 = this;

      this.root.addEventListener('compositionstart', function () {
        _this2.composing = true;
      });
      this.root.addEventListener('compositionend', function () {
        _this2.composing = false;
        if (_this2.cursor.parent) {
          var range = _this2.cursor.restore();
          if (!range) return;
          setTimeout(function () {
            _this2.setNativeRange(range.startNode, range.startOffset, range.endNode, range.endOffset);
          }, 1);
        }
      });
    }
  }, {
    key: 'handleDragging',
    value: function handleDragging() {
      var _this3 = this;

      this.emitter.listenDOM('mousedown', document.body, function () {
        _this3.mouseDown = true;
      });
      this.emitter.listenDOM('mouseup', document.body, function () {
        _this3.mouseDown = false;
        _this3.update(_emitter4.default.sources.USER);
      });
    }
  }, {
    key: 'focus',
    value: function focus() {
      if (this.hasFocus()) return;
      this.root.focus();
      this.setRange(this.savedRange);
    }
  }, {
    key: 'format',
    value: function format(_format, value) {
      if (this.scroll.whitelist != null && !this.scroll.whitelist[_format]) return;
      this.scroll.update();
      var nativeRange = this.getNativeRange();
      if (nativeRange == null || !nativeRange.native.collapsed || _parchment2.default.query(_format, _parchment2.default.Scope.BLOCK)) return;
      if (nativeRange.start.node !== this.cursor.textNode) {
        var blot = _parchment2.default.find(nativeRange.start.node, false);
        if (blot == null) return;
        // TODO Give blot ability to not split
        if (blot instanceof _parchment2.default.Leaf) {
          var after = blot.split(nativeRange.start.offset);
          blot.parent.insertBefore(this.cursor, after);
        } else {
          blot.insertBefore(this.cursor, nativeRange.start.node); // Should never happen
        }
        this.cursor.attach();
      }
      this.cursor.format(_format, value);
      this.scroll.optimize();
      this.setNativeRange(this.cursor.textNode, this.cursor.textNode.data.length);
      this.update();
    }
  }, {
    key: 'getBounds',
    value: function getBounds(index) {
      var length = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0;

      var scrollLength = this.scroll.length();
      index = Math.min(index, scrollLength - 1);
      length = Math.min(index + length, scrollLength - 1) - index;
      var node = void 0,
          _scroll$leaf = this.scroll.leaf(index),
          _scroll$leaf2 = _slicedToArray(_scroll$leaf, 2),
          leaf = _scroll$leaf2[0],
          offset = _scroll$leaf2[1];
      if (leaf == null) return null;

      var _leaf$position = leaf.position(offset, true);

      var _leaf$position2 = _slicedToArray(_leaf$position, 2);

      node = _leaf$position2[0];
      offset = _leaf$position2[1];

      var range = document.createRange();
      if (length > 0) {
        range.setStart(node, offset);

        var _scroll$leaf3 = this.scroll.leaf(index + length);

        var _scroll$leaf4 = _slicedToArray(_scroll$leaf3, 2);

        leaf = _scroll$leaf4[0];
        offset = _scroll$leaf4[1];

        if (leaf == null) return null;

        var _leaf$position3 = leaf.position(offset, true);

        var _leaf$position4 = _slicedToArray(_leaf$position3, 2);

        node = _leaf$position4[0];
        offset = _leaf$position4[1];

        range.setEnd(node, offset);
        return range.getBoundingClientRect();
      } else {
        var side = 'left';
        var rect = void 0;
        if (node instanceof Text) {
          if (offset < node.data.length) {
            range.setStart(node, offset);
            range.setEnd(node, offset + 1);
          } else {
            range.setStart(node, offset - 1);
            range.setEnd(node, offset);
            side = 'right';
          }
          rect = range.getBoundingClientRect();
        } else {
          rect = leaf.domNode.getBoundingClientRect();
          if (offset > 0) side = 'right';
        }
        return {
          bottom: rect.top + rect.height,
          height: rect.height,
          left: rect[side],
          right: rect[side],
          top: rect.top,
          width: 0
        };
      }
    }
  }, {
    key: 'getNativeRange',
    value: function getNativeRange() {
      var selection = document.getSelection();
      if (selection == null || selection.rangeCount <= 0) return null;
      var nativeRange = selection.getRangeAt(0);
      if (nativeRange == null) return null;
      var range = this.normalizeNative(nativeRange);
      debug.info('getNativeRange', range);
      return range;
    }
  }, {
    key: 'getRange',
    value: function getRange() {
      var normalized = this.getNativeRange();
      if (normalized == null) return [null, null];
      var range = this.normalizedToRange(normalized);
      return [range, normalized];
    }
  }, {
    key: 'hasFocus',
    value: function hasFocus() {
      return document.activeElement === this.root;
    }
  }, {
    key: 'normalizedToRange',
    value: function normalizedToRange(range) {
      var _this4 = this;

      var positions = [[range.start.node, range.start.offset]];
      if (!range.native.collapsed) {
        positions.push([range.end.node, range.end.offset]);
      }
      var indexes = positions.map(function (position) {
        var _position = _slicedToArray(position, 2),
            node = _position[0],
            offset = _position[1];

        var blot = _parchment2.default.find(node, true);
        var index = blot.offset(_this4.scroll);
        if (offset === 0) {
          return index;
        } else if (blot instanceof _parchment2.default.Container) {
          return index + blot.length();
        } else {
          return index + blot.index(node, offset);
        }
      });
      var end = Math.min(Math.max.apply(Math, _toConsumableArray(indexes)), this.scroll.length() - 1);
      var start = Math.min.apply(Math, [end].concat(_toConsumableArray(indexes)));
      return new Range(start, end - start);
    }
  }, {
    key: 'normalizeNative',
    value: function normalizeNative(nativeRange) {
      if (!contains(this.root, nativeRange.startContainer) || !nativeRange.collapsed && !contains(this.root, nativeRange.endContainer)) {
        return null;
      }
      var range = {
        start: { node: nativeRange.startContainer, offset: nativeRange.startOffset },
        end: { node: nativeRange.endContainer, offset: nativeRange.endOffset },
        native: nativeRange
      };
      [range.start, range.end].forEach(function (position) {
        var node = position.node,
            offset = position.offset;
        while (!(node instanceof Text) && node.childNodes.length > 0) {
          if (node.childNodes.length > offset) {
            node = node.childNodes[offset];
            offset = 0;
          } else if (node.childNodes.length === offset) {
            node = node.lastChild;
            offset = node instanceof Text ? node.data.length : node.childNodes.length + 1;
          } else {
            break;
          }
        }
        position.node = node, position.offset = offset;
      });
      return range;
    }
  }, {
    key: 'rangeToNative',
    value: function rangeToNative(range) {
      var _this5 = this;

      var indexes = range.collapsed ? [range.index] : [range.index, range.index + range.length];
      var args = [];
      var scrollLength = this.scroll.length();
      indexes.forEach(function (index, i) {
        index = Math.min(scrollLength - 1, index);
        var node = void 0,
            _scroll$leaf5 = _this5.scroll.leaf(index),
            _scroll$leaf6 = _slicedToArray(_scroll$leaf5, 2),
            leaf = _scroll$leaf6[0],
            offset = _scroll$leaf6[1];
        var _leaf$position5 = leaf.position(offset, i !== 0);

        var _leaf$position6 = _slicedToArray(_leaf$position5, 2);

        node = _leaf$position6[0];
        offset = _leaf$position6[1];

        args.push(node, offset);
      });
      if (args.length < 2) {
        args = args.concat(args);
      }
      return args;
    }
  }, {
    key: 'scrollIntoView',
    value: function scrollIntoView(scrollingContainer) {
      var range = this.lastRange;
      if (range == null) return;
      var bounds = this.getBounds(range.index, range.length);
      if (bounds == null) return;
      var limit = this.scroll.length() - 1;

      var _scroll$line = this.scroll.line(Math.min(range.index, limit)),
          _scroll$line2 = _slicedToArray(_scroll$line, 1),
          first = _scroll$line2[0];

      var last = first;
      if (range.length > 0) {
        var _scroll$line3 = this.scroll.line(Math.min(range.index + range.length, limit));

        var _scroll$line4 = _slicedToArray(_scroll$line3, 1);

        last = _scroll$line4[0];
      }
      if (first == null || last == null) return;
      var scrollBounds = scrollingContainer.getBoundingClientRect();
      if (bounds.top < scrollBounds.top) {
        scrollingContainer.scrollTop -= scrollBounds.top - bounds.top;
      } else if (bounds.bottom > scrollBounds.bottom) {
        scrollingContainer.scrollTop += bounds.bottom - scrollBounds.bottom;
      }
    }
  }, {
    key: 'setNativeRange',
    value: function setNativeRange(startNode, startOffset) {
      var endNode = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : startNode;
      var endOffset = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : startOffset;
      var force = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : false;

      debug.info('setNativeRange', startNode, startOffset, endNode, endOffset);
      if (startNode != null && (this.root.parentNode == null || startNode.parentNode == null || endNode.parentNode == null)) {
        return;
      }
      var selection = document.getSelection();
      if (selection == null) return;
      if (startNode != null) {
        if (!this.hasFocus()) this.root.focus();
        var native = (this.getNativeRange() || {}).native;
        if (native == null || force || startNode !== native.startContainer || startOffset !== native.startOffset || endNode !== native.endContainer || endOffset !== native.endOffset) {

          if (startNode.tagName == "BR") {
            startOffset = [].indexOf.call(startNode.parentNode.childNodes, startNode);
            startNode = startNode.parentNode;
          }
          if (endNode.tagName == "BR") {
            endOffset = [].indexOf.call(endNode.parentNode.childNodes, endNode);
            endNode = endNode.parentNode;
          }
          var range = document.createRange();
          range.setStart(startNode, startOffset);
          range.setEnd(endNode, endOffset);
          selection.removeAllRanges();
          selection.addRange(range);
        }
      } else {
        selection.removeAllRanges();
        this.root.blur();
        document.body.focus(); // root.blur() not enough on IE11+Travis+SauceLabs (but not local VMs)
      }
    }
  }, {
    key: 'setRange',
    value: function setRange(range) {
      var force = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;
      var source = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : _emitter4.default.sources.API;

      if (typeof force === 'string') {
        source = force;
        force = false;
      }
      debug.info('setRange', range);
      if (range != null) {
        var args = this.rangeToNative(range);
        this.setNativeRange.apply(this, _toConsumableArray(args).concat([force]));
      } else {
        this.setNativeRange(null);
      }
      this.update(source);
    }
  }, {
    key: 'update',
    value: function update() {
      var source = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : _emitter4.default.sources.USER;

      var oldRange = this.lastRange;

      var _getRange = this.getRange(),
          _getRange2 = _slicedToArray(_getRange, 2),
          lastRange = _getRange2[0],
          nativeRange = _getRange2[1];

      this.lastRange = lastRange;
      if (this.lastRange != null) {
        this.savedRange = this.lastRange;
      }
      if (!(0, _deepEqual2.default)(oldRange, this.lastRange)) {
        var _emitter;

        if (!this.composing && nativeRange != null && nativeRange.native.collapsed && nativeRange.start.node !== this.cursor.textNode) {
          this.cursor.restore();
        }
        var args = [_emitter4.default.events.SELECTION_CHANGE, (0, _clone2.default)(this.lastRange), (0, _clone2.default)(oldRange), source];
        (_emitter = this.emitter).emit.apply(_emitter, [_emitter4.default.events.EDITOR_CHANGE].concat(args));
        if (source !== _emitter4.default.sources.SILENT) {
          var _emitter2;

          (_emitter2 = this.emitter).emit.apply(_emitter2, args);
        }
      }
    }
  }]);

  return Selection;
}();

function contains(parent, descendant) {
  try {
    // Firefox inserts inaccessible nodes around video elements
    descendant.parentNode;
  } catch (e) {
    return false;
  }
  // IE11 has bug with Text nodes
  // https://connect.microsoft.com/IE/feedback/details/780874/node-contains-is-incorrect
  if (descendant instanceof Text) {
    descendant = descendant.parentNode;
  }
  return parent.contains(descendant);
}

exports.Range = Range;
exports.default = Selection;

/***/ }),
/* 16 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Break = function (_Parchment$Embed) {
  _inherits(Break, _Parchment$Embed);

  function Break() {
    _classCallCheck(this, Break);

    return _possibleConstructorReturn(this, (Break.__proto__ || Object.getPrototypeOf(Break)).apply(this, arguments));
  }

  _createClass(Break, [{
    key: 'insertInto',
    value: function insertInto(parent, ref) {
      if (parent.children.length === 0) {
        _get(Break.prototype.__proto__ || Object.getPrototypeOf(Break.prototype), 'insertInto', this).call(this, parent, ref);
      } else {
        this.remove();
      }
    }
  }, {
    key: 'length',
    value: function length() {
      return 0;
    }
  }, {
    key: 'value',
    value: function value() {
      return '';
    }
  }], [{
    key: 'value',
    value: function value() {
      return undefined;
    }
  }]);

  return Break;
}(_parchment2.default.Embed);

Break.blotName = 'break';
Break.tagName = 'BR';

exports.default = Break;

/***/ }),
/* 17 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var linked_list_1 = __webpack_require__(44);
var shadow_1 = __webpack_require__(30);
var Registry = __webpack_require__(1);
var ContainerBlot = /** @class */ (function (_super) {
    __extends(ContainerBlot, _super);
    function ContainerBlot(domNode) {
        var _this = _super.call(this, domNode) || this;
        _this.build();
        return _this;
    }
    ContainerBlot.prototype.appendChild = function (other) {
        this.insertBefore(other);
    };
    ContainerBlot.prototype.attach = function () {
        _super.prototype.attach.call(this);
        this.children.forEach(function (child) {
            child.attach();
        });
    };
    ContainerBlot.prototype.build = function () {
        var _this = this;
        this.children = new linked_list_1.default();
        // Need to be reversed for if DOM nodes already in order
        [].slice
            .call(this.domNode.childNodes)
            .reverse()
            .forEach(function (node) {
            try {
                var child = makeBlot(node);
                _this.insertBefore(child, _this.children.head || undefined);
            }
            catch (err) {
                if (err instanceof Registry.ParchmentError)
                    return;
                else
                    throw err;
            }
        });
    };
    ContainerBlot.prototype.deleteAt = function (index, length) {
        if (index === 0 && length === this.length()) {
            return this.remove();
        }
        this.children.forEachAt(index, length, function (child, offset, length) {
            child.deleteAt(offset, length);
        });
    };
    ContainerBlot.prototype.descendant = function (criteria, index) {
        var _a = this.children.find(index), child = _a[0], offset = _a[1];
        if ((criteria.blotName == null && criteria(child)) ||
            (criteria.blotName != null && child instanceof criteria)) {
            return [child, offset];
        }
        else if (child instanceof ContainerBlot) {
            return child.descendant(criteria, offset);
        }
        else {
            return [null, -1];
        }
    };
    ContainerBlot.prototype.descendants = function (criteria, index, length) {
        if (index === void 0) { index = 0; }
        if (length === void 0) { length = Number.MAX_VALUE; }
        var descendants = [];
        var lengthLeft = length;
        this.children.forEachAt(index, length, function (child, index, length) {
            if ((criteria.blotName == null && criteria(child)) ||
                (criteria.blotName != null && child instanceof criteria)) {
                descendants.push(child);
            }
            if (child instanceof ContainerBlot) {
                descendants = descendants.concat(child.descendants(criteria, index, lengthLeft));
            }
            lengthLeft -= length;
        });
        return descendants;
    };
    ContainerBlot.prototype.detach = function () {
        this.children.forEach(function (child) {
            child.detach();
        });
        _super.prototype.detach.call(this);
    };
    ContainerBlot.prototype.formatAt = function (index, length, name, value) {
        this.children.forEachAt(index, length, function (child, offset, length) {
            child.formatAt(offset, length, name, value);
        });
    };
    ContainerBlot.prototype.insertAt = function (index, value, def) {
        var _a = this.children.find(index), child = _a[0], offset = _a[1];
        if (child) {
            child.insertAt(offset, value, def);
        }
        else {
            var blot = def == null ? Registry.create('text', value) : Registry.create(value, def);
            this.appendChild(blot);
        }
    };
    ContainerBlot.prototype.insertBefore = function (childBlot, refBlot) {
        if (this.statics.allowedChildren != null &&
            !this.statics.allowedChildren.some(function (child) {
                return childBlot instanceof child;
            })) {
            throw new Registry.ParchmentError("Cannot insert " + childBlot.statics.blotName + " into " + this.statics.blotName);
        }
        childBlot.insertInto(this, refBlot);
    };
    ContainerBlot.prototype.length = function () {
        return this.children.reduce(function (memo, child) {
            return memo + child.length();
        }, 0);
    };
    ContainerBlot.prototype.moveChildren = function (targetParent, refNode) {
        this.children.forEach(function (child) {
            targetParent.insertBefore(child, refNode);
        });
    };
    ContainerBlot.prototype.optimize = function (context) {
        _super.prototype.optimize.call(this, context);
        if (this.children.length === 0) {
            if (this.statics.defaultChild != null) {
                var child = Registry.create(this.statics.defaultChild);
                this.appendChild(child);
                child.optimize(context);
            }
            else {
                this.remove();
            }
        }
    };
    ContainerBlot.prototype.path = function (index, inclusive) {
        if (inclusive === void 0) { inclusive = false; }
        var _a = this.children.find(index, inclusive), child = _a[0], offset = _a[1];
        var position = [[this, index]];
        if (child instanceof ContainerBlot) {
            return position.concat(child.path(offset, inclusive));
        }
        else if (child != null) {
            position.push([child, offset]);
        }
        return position;
    };
    ContainerBlot.prototype.removeChild = function (child) {
        this.children.remove(child);
    };
    ContainerBlot.prototype.replace = function (target) {
        if (target instanceof ContainerBlot) {
            target.moveChildren(this);
        }
        _super.prototype.replace.call(this, target);
    };
    ContainerBlot.prototype.split = function (index, force) {
        if (force === void 0) { force = false; }
        if (!force) {
            if (index === 0)
                return this;
            if (index === this.length())
                return this.next;
        }
        var after = this.clone();
        this.parent.insertBefore(after, this.next);
        this.children.forEachAt(index, this.length(), function (child, offset, length) {
            child = child.split(offset, force);
            after.appendChild(child);
        });
        return after;
    };
    ContainerBlot.prototype.unwrap = function () {
        this.moveChildren(this.parent, this.next);
        this.remove();
    };
    ContainerBlot.prototype.update = function (mutations, context) {
        var _this = this;
        var addedNodes = [];
        var removedNodes = [];
        mutations.forEach(function (mutation) {
            if (mutation.target === _this.domNode && mutation.type === 'childList') {
                addedNodes.push.apply(addedNodes, mutation.addedNodes);
                removedNodes.push.apply(removedNodes, mutation.removedNodes);
            }
        });
        removedNodes.forEach(function (node) {
            // Check node has actually been removed
            // One exception is Chrome does not immediately remove IFRAMEs
            // from DOM but MutationRecord is correct in its reported removal
            if (node.parentNode != null &&
                // @ts-ignore
                node.tagName !== 'IFRAME' &&
                document.body.compareDocumentPosition(node) & Node.DOCUMENT_POSITION_CONTAINED_BY) {
                return;
            }
            var blot = Registry.find(node);
            if (blot == null)
                return;
            if (blot.domNode.parentNode == null || blot.domNode.parentNode === _this.domNode) {
                blot.detach();
            }
        });
        addedNodes
            .filter(function (node) {
            return node.parentNode == _this.domNode;
        })
            .sort(function (a, b) {
            if (a === b)
                return 0;
            if (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING) {
                return 1;
            }
            return -1;
        })
            .forEach(function (node) {
            var refBlot = null;
            if (node.nextSibling != null) {
                refBlot = Registry.find(node.nextSibling);
            }
            var blot = makeBlot(node);
            if (blot.next != refBlot || blot.next == null) {
                if (blot.parent != null) {
                    blot.parent.removeChild(_this);
                }
                _this.insertBefore(blot, refBlot || undefined);
            }
        });
    };
    return ContainerBlot;
}(shadow_1.default));
function makeBlot(node) {
    var blot = Registry.find(node);
    if (blot == null) {
        try {
            blot = Registry.create(node);
        }
        catch (e) {
            blot = Registry.create(Registry.Scope.INLINE);
            [].slice.call(node.childNodes).forEach(function (child) {
                // @ts-ignore
                blot.domNode.appendChild(child);
            });
            if (node.parentNode) {
                node.parentNode.replaceChild(blot.domNode, node);
            }
            blot.attach();
        }
    }
    return blot;
}
exports.default = ContainerBlot;


/***/ }),
/* 18 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var attributor_1 = __webpack_require__(12);
var store_1 = __webpack_require__(31);
var container_1 = __webpack_require__(17);
var Registry = __webpack_require__(1);
var FormatBlot = /** @class */ (function (_super) {
    __extends(FormatBlot, _super);
    function FormatBlot(domNode) {
        var _this = _super.call(this, domNode) || this;
        _this.attributes = new store_1.default(_this.domNode);
        return _this;
    }
    FormatBlot.formats = function (domNode) {
        if (typeof this.tagName === 'string') {
            return true;
        }
        else if (Array.isArray(this.tagName)) {
            return domNode.tagName.toLowerCase();
        }
        return undefined;
    };
    FormatBlot.prototype.format = function (name, value) {
        var format = Registry.query(name);
        if (format instanceof attributor_1.default) {
            this.attributes.attribute(format, value);
        }
        else if (value) {
            if (format != null && (name !== this.statics.blotName || this.formats()[name] !== value)) {
                this.replaceWith(name, value);
            }
        }
    };
    FormatBlot.prototype.formats = function () {
        var formats = this.attributes.values();
        var format = this.statics.formats(this.domNode);
        if (format != null) {
            formats[this.statics.blotName] = format;
        }
        return formats;
    };
    FormatBlot.prototype.replaceWith = function (name, value) {
        var replacement = _super.prototype.replaceWith.call(this, name, value);
        this.attributes.copy(replacement);
        return replacement;
    };
    FormatBlot.prototype.update = function (mutations, context) {
        var _this = this;
        _super.prototype.update.call(this, mutations, context);
        if (mutations.some(function (mutation) {
            return mutation.target === _this.domNode && mutation.type === 'attributes';
        })) {
            this.attributes.build();
        }
    };
    FormatBlot.prototype.wrap = function (name, value) {
        var wrapper = _super.prototype.wrap.call(this, name, value);
        if (wrapper instanceof FormatBlot && wrapper.statics.scope === this.statics.scope) {
            this.attributes.move(wrapper);
        }
        return wrapper;
    };
    return FormatBlot;
}(container_1.default));
exports.default = FormatBlot;


/***/ }),
/* 19 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var shadow_1 = __webpack_require__(30);
var Registry = __webpack_require__(1);
var LeafBlot = /** @class */ (function (_super) {
    __extends(LeafBlot, _super);
    function LeafBlot() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LeafBlot.value = function (domNode) {
        return true;
    };
    LeafBlot.prototype.index = function (node, offset) {
        if (this.domNode === node ||
            this.domNode.compareDocumentPosition(node) & Node.DOCUMENT_POSITION_CONTAINED_BY) {
            return Math.min(offset, 1);
        }
        return -1;
    };
    LeafBlot.prototype.position = function (index, inclusive) {
        var offset = [].indexOf.call(this.parent.domNode.childNodes, this.domNode);
        if (index > 0)
            offset += 1;
        return [this.parent.domNode, offset];
    };
    LeafBlot.prototype.value = function () {
        return _a = {}, _a[this.statics.blotName] = this.statics.value(this.domNode) || true, _a;
        var _a;
    };
    LeafBlot.scope = Registry.Scope.INLINE_BLOT;
    return LeafBlot;
}(shadow_1.default));
exports.default = LeafBlot;


/***/ }),
/* 20 */
/***/ (function(module, exports, __webpack_require__) {

var equal = __webpack_require__(11);
var extend = __webpack_require__(3);


var lib = {
  attributes: {
    compose: function (a, b, keepNull) {
      if (typeof a !== 'object') a = {};
      if (typeof b !== 'object') b = {};
      var attributes = extend(true, {}, b);
      if (!keepNull) {
        attributes = Object.keys(attributes).reduce(function (copy, key) {
          if (attributes[key] != null) {
            copy[key] = attributes[key];
          }
          return copy;
        }, {});
      }
      for (var key in a) {
        if (a[key] !== undefined && b[key] === undefined) {
          attributes[key] = a[key];
        }
      }
      return Object.keys(attributes).length > 0 ? attributes : undefined;
    },

    diff: function(a, b) {
      if (typeof a !== 'object') a = {};
      if (typeof b !== 'object') b = {};
      var attributes = Object.keys(a).concat(Object.keys(b)).reduce(function (attributes, key) {
        if (!equal(a[key], b[key])) {
          attributes[key] = b[key] === undefined ? null : b[key];
        }
        return attributes;
      }, {});
      return Object.keys(attributes).length > 0 ? attributes : undefined;
    },

    transform: function (a, b, priority) {
      if (typeof a !== 'object') return b;
      if (typeof b !== 'object') return undefined;
      if (!priority) return b;  // b simply overwrites us without priority
      var attributes = Object.keys(b).reduce(function (attributes, key) {
        if (a[key] === undefined) attributes[key] = b[key];  // null is a valid value
        return attributes;
      }, {});
      return Object.keys(attributes).length > 0 ? attributes : undefined;
    }
  },

  iterator: function (ops) {
    return new Iterator(ops);
  },

  length: function (op) {
    if (typeof op['delete'] === 'number') {
      return op['delete'];
    } else if (typeof op.retain === 'number') {
      return op.retain;
    } else {
      return typeof op.insert === 'string' ? op.insert.length : 1;
    }
  }
};


function Iterator(ops) {
  this.ops = ops;
  this.index = 0;
  this.offset = 0;
};

Iterator.prototype.hasNext = function () {
  return this.peekLength() < Infinity;
};

Iterator.prototype.next = function (length) {
  if (!length) length = Infinity;
  var nextOp = this.ops[this.index];
  if (nextOp) {
    var offset = this.offset;
    var opLength = lib.length(nextOp)
    if (length >= opLength - offset) {
      length = opLength - offset;
      this.index += 1;
      this.offset = 0;
    } else {
      this.offset += length;
    }
    if (typeof nextOp['delete'] === 'number') {
      return { 'delete': length };
    } else {
      var retOp = {};
      if (nextOp.attributes) {
        retOp.attributes = nextOp.attributes;
      }
      if (typeof nextOp.retain === 'number') {
        retOp.retain = length;
      } else if (typeof nextOp.insert === 'string') {
        retOp.insert = nextOp.insert.substr(offset, length);
      } else {
        // offset should === 0, length should === 1
        retOp.insert = nextOp.insert;
      }
      return retOp;
    }
  } else {
    return { retain: Infinity };
  }
};

Iterator.prototype.peek = function () {
  return this.ops[this.index];
};

Iterator.prototype.peekLength = function () {
  if (this.ops[this.index]) {
    // Should never return 0 if our index is being managed correctly
    return lib.length(this.ops[this.index]) - this.offset;
  } else {
    return Infinity;
  }
};

Iterator.prototype.peekType = function () {
  if (this.ops[this.index]) {
    if (typeof this.ops[this.index]['delete'] === 'number') {
      return 'delete';
    } else if (typeof this.ops[this.index].retain === 'number') {
      return 'retain';
    } else {
      return 'insert';
    }
  }
  return 'retain';
};


module.exports = lib;


/***/ }),
/* 21 */
/***/ (function(module, exports) {

var clone = (function() {
'use strict';

function _instanceof(obj, type) {
  return type != null && obj instanceof type;
}

var nativeMap;
try {
  nativeMap = Map;
} catch(_) {
  // maybe a reference error because no `Map`. Give it a dummy value that no
  // value will ever be an instanceof.
  nativeMap = function() {};
}

var nativeSet;
try {
  nativeSet = Set;
} catch(_) {
  nativeSet = function() {};
}

var nativePromise;
try {
  nativePromise = Promise;
} catch(_) {
  nativePromise = function() {};
}

/**
 * Clones (copies) an Object using deep copying.
 *
 * This function supports circular references by default, but if you are certain
 * there are no circular references in your object, you can save some CPU time
 * by calling clone(obj, false).
 *
 * Caution: if `circular` is false and `parent` contains circular references,
 * your program may enter an infinite loop and crash.
 *
 * @param `parent` - the object to be cloned
 * @param `circular` - set to true if the object to be cloned may contain
 *    circular references. (optional - true by default)
 * @param `depth` - set to a number if the object is only to be cloned to
 *    a particular depth. (optional - defaults to Infinity)
 * @param `prototype` - sets the prototype to be used when cloning an object.
 *    (optional - defaults to parent prototype).
 * @param `includeNonEnumerable` - set to true if the non-enumerable properties
 *    should be cloned as well. Non-enumerable properties on the prototype
 *    chain will be ignored. (optional - false by default)
*/
function clone(parent, circular, depth, prototype, includeNonEnumerable) {
  if (typeof circular === 'object') {
    depth = circular.depth;
    prototype = circular.prototype;
    includeNonEnumerable = circular.includeNonEnumerable;
    circular = circular.circular;
  }
  // maintain two arrays for circular references, where corresponding parents
  // and children have the same index
  var allParents = [];
  var allChildren = [];

  var useBuffer = typeof Buffer != 'undefined';

  if (typeof circular == 'undefined')
    circular = true;

  if (typeof depth == 'undefined')
    depth = Infinity;

  // recurse this function so we don't reset allParents and allChildren
  function _clone(parent, depth) {
    // cloning null always returns null
    if (parent === null)
      return null;

    if (depth === 0)
      return parent;

    var child;
    var proto;
    if (typeof parent != 'object') {
      return parent;
    }

    if (_instanceof(parent, nativeMap)) {
      child = new nativeMap();
    } else if (_instanceof(parent, nativeSet)) {
      child = new nativeSet();
    } else if (_instanceof(parent, nativePromise)) {
      child = new nativePromise(function (resolve, reject) {
        parent.then(function(value) {
          resolve(_clone(value, depth - 1));
        }, function(err) {
          reject(_clone(err, depth - 1));
        });
      });
    } else if (clone.__isArray(parent)) {
      child = [];
    } else if (clone.__isRegExp(parent)) {
      child = new RegExp(parent.source, __getRegExpFlags(parent));
      if (parent.lastIndex) child.lastIndex = parent.lastIndex;
    } else if (clone.__isDate(parent)) {
      child = new Date(parent.getTime());
    } else if (useBuffer && Buffer.isBuffer(parent)) {
      child = new Buffer(parent.length);
      parent.copy(child);
      return child;
    } else if (_instanceof(parent, Error)) {
      child = Object.create(parent);
    } else {
      if (typeof prototype == 'undefined') {
        proto = Object.getPrototypeOf(parent);
        child = Object.create(proto);
      }
      else {
        child = Object.create(prototype);
        proto = prototype;
      }
    }

    if (circular) {
      var index = allParents.indexOf(parent);

      if (index != -1) {
        return allChildren[index];
      }
      allParents.push(parent);
      allChildren.push(child);
    }

    if (_instanceof(parent, nativeMap)) {
      parent.forEach(function(value, key) {
        var keyChild = _clone(key, depth - 1);
        var valueChild = _clone(value, depth - 1);
        child.set(keyChild, valueChild);
      });
    }
    if (_instanceof(parent, nativeSet)) {
      parent.forEach(function(value) {
        var entryChild = _clone(value, depth - 1);
        child.add(entryChild);
      });
    }

    for (var i in parent) {
      var attrs;
      if (proto) {
        attrs = Object.getOwnPropertyDescriptor(proto, i);
      }

      if (attrs && attrs.set == null) {
        continue;
      }
      child[i] = _clone(parent[i], depth - 1);
    }

    if (Object.getOwnPropertySymbols) {
      var symbols = Object.getOwnPropertySymbols(parent);
      for (var i = 0; i < symbols.length; i++) {
        // Don't need to worry about cloning a symbol because it is a primitive,
        // like a number or string.
        var symbol = symbols[i];
        var descriptor = Object.getOwnPropertyDescriptor(parent, symbol);
        if (descriptor && !descriptor.enumerable && !includeNonEnumerable) {
          continue;
        }
        child[symbol] = _clone(parent[symbol], depth - 1);
        if (!descriptor.enumerable) {
          Object.defineProperty(child, symbol, {
            enumerable: false
          });
        }
      }
    }

    if (includeNonEnumerable) {
      var allPropertyNames = Object.getOwnPropertyNames(parent);
      for (var i = 0; i < allPropertyNames.length; i++) {
        var propertyName = allPropertyNames[i];
        var descriptor = Object.getOwnPropertyDescriptor(parent, propertyName);
        if (descriptor && descriptor.enumerable) {
          continue;
        }
        child[propertyName] = _clone(parent[propertyName], depth - 1);
        Object.defineProperty(child, propertyName, {
          enumerable: false
        });
      }
    }

    return child;
  }

  return _clone(parent, depth);
}

/**
 * Simple flat clone using prototype, accepts only objects, usefull for property
 * override on FLAT configuration object (no nested props).
 *
 * USE WITH CAUTION! This may not behave as you wish if you do not know how this
 * works.
 */
clone.clonePrototype = function clonePrototype(parent) {
  if (parent === null)
    return null;

  var c = function () {};
  c.prototype = parent;
  return new c();
};

// private utility functions

function __objToStr(o) {
  return Object.prototype.toString.call(o);
}
clone.__objToStr = __objToStr;

function __isDate(o) {
  return typeof o === 'object' && __objToStr(o) === '[object Date]';
}
clone.__isDate = __isDate;

function __isArray(o) {
  return typeof o === 'object' && __objToStr(o) === '[object Array]';
}
clone.__isArray = __isArray;

function __isRegExp(o) {
  return typeof o === 'object' && __objToStr(o) === '[object RegExp]';
}
clone.__isRegExp = __isRegExp;

function __getRegExpFlags(re) {
  var flags = '';
  if (re.global) flags += 'g';
  if (re.ignoreCase) flags += 'i';
  if (re.multiline) flags += 'm';
  return flags;
}
clone.__getRegExpFlags = __getRegExpFlags;

return clone;
})();

if (typeof module === 'object' && module.exports) {
  module.exports = clone;
}


/***/ }),
/* 22 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _emitter = __webpack_require__(8);

var _emitter2 = _interopRequireDefault(_emitter);

var _block = __webpack_require__(4);

var _block2 = _interopRequireDefault(_block);

var _break = __webpack_require__(16);

var _break2 = _interopRequireDefault(_break);

var _code = __webpack_require__(13);

var _code2 = _interopRequireDefault(_code);

var _container = __webpack_require__(25);

var _container2 = _interopRequireDefault(_container);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function isLine(blot) {
  return blot instanceof _block2.default || blot instanceof _block.BlockEmbed;
}

var Scroll = function (_Parchment$Scroll) {
  _inherits(Scroll, _Parchment$Scroll);

  function Scroll(domNode, config) {
    _classCallCheck(this, Scroll);

    var _this = _possibleConstructorReturn(this, (Scroll.__proto__ || Object.getPrototypeOf(Scroll)).call(this, domNode));

    _this.emitter = config.emitter;
    if (Array.isArray(config.whitelist)) {
      _this.whitelist = config.whitelist.reduce(function (whitelist, format) {
        whitelist[format] = true;
        return whitelist;
      }, {});
    }
    // Some reason fixes composition issues with character languages in Windows/Chrome, Safari
    _this.domNode.addEventListener('DOMNodeInserted', function () {});
    _this.optimize();
    _this.enable();
    return _this;
  }

  _createClass(Scroll, [{
    key: 'batchStart',
    value: function batchStart() {
      this.batch = true;
    }
  }, {
    key: 'batchEnd',
    value: function batchEnd() {
      this.batch = false;
      this.optimize();
    }
  }, {
    key: 'deleteAt',
    value: function deleteAt(index, length) {
      var _line = this.line(index),
          _line2 = _slicedToArray(_line, 2),
          first = _line2[0],
          offset = _line2[1];

      var _line3 = this.line(index + length),
          _line4 = _slicedToArray(_line3, 1),
          last = _line4[0];

      _get(Scroll.prototype.__proto__ || Object.getPrototypeOf(Scroll.prototype), 'deleteAt', this).call(this, index, length);
      if (last != null && first !== last && offset > 0) {
        if (first instanceof _block.BlockEmbed || last instanceof _block.BlockEmbed) {
          this.optimize();
          return;
        }
        if (first instanceof _code2.default) {
          var newlineIndex = first.newlineIndex(first.length(), true);
          if (newlineIndex > -1) {
            first = first.split(newlineIndex + 1);
            if (first === last) {
              this.optimize();
              return;
            }
          }
        } else if (last instanceof _code2.default) {
          var _newlineIndex = last.newlineIndex(0);
          if (_newlineIndex > -1) {
            last.split(_newlineIndex + 1);
          }
        }
        var ref = last.children.head instanceof _break2.default ? null : last.children.head;
        first.moveChildren(last, ref);
        first.remove();
      }
      this.optimize();
    }
  }, {
    key: 'enable',
    value: function enable() {
      var enabled = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : true;

      this.domNode.setAttribute('contenteditable', enabled);
    }
  }, {
    key: 'formatAt',
    value: function formatAt(index, length, format, value) {
      if (this.whitelist != null && !this.whitelist[format]) return;
      _get(Scroll.prototype.__proto__ || Object.getPrototypeOf(Scroll.prototype), 'formatAt', this).call(this, index, length, format, value);
      this.optimize();
    }
  }, {
    key: 'insertAt',
    value: function insertAt(index, value, def) {
      if (def != null && this.whitelist != null && !this.whitelist[value]) return;
      if (index >= this.length()) {
        if (def == null || _parchment2.default.query(value, _parchment2.default.Scope.BLOCK) == null) {
          var blot = _parchment2.default.create(this.statics.defaultChild);
          this.appendChild(blot);
          if (def == null && value.endsWith('\n')) {
            value = value.slice(0, -1);
          }
          blot.insertAt(0, value, def);
        } else {
          var embed = _parchment2.default.create(value, def);
          this.appendChild(embed);
        }
      } else {
        _get(Scroll.prototype.__proto__ || Object.getPrototypeOf(Scroll.prototype), 'insertAt', this).call(this, index, value, def);
      }
      this.optimize();
    }
  }, {
    key: 'insertBefore',
    value: function insertBefore(blot, ref) {
      if (blot.statics.scope === _parchment2.default.Scope.INLINE_BLOT) {
        var wrapper = _parchment2.default.create(this.statics.defaultChild);
        wrapper.appendChild(blot);
        blot = wrapper;
      }
      _get(Scroll.prototype.__proto__ || Object.getPrototypeOf(Scroll.prototype), 'insertBefore', this).call(this, blot, ref);
    }
  }, {
    key: 'leaf',
    value: function leaf(index) {
      return this.path(index).pop() || [null, -1];
    }
  }, {
    key: 'line',
    value: function line(index) {
      if (index === this.length()) {
        return this.line(index - 1);
      }
      return this.descendant(isLine, index);
    }
  }, {
    key: 'lines',
    value: function lines() {
      var index = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;
      var length = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : Number.MAX_VALUE;

      var getLines = function getLines(blot, index, length) {
        var lines = [],
            lengthLeft = length;
        blot.children.forEachAt(index, length, function (child, index, length) {
          if (isLine(child)) {
            lines.push(child);
          } else if (child instanceof _parchment2.default.Container) {
            lines = lines.concat(getLines(child, index, lengthLeft));
          }
          lengthLeft -= length;
        });
        return lines;
      };
      return getLines(this, index, length);
    }
  }, {
    key: 'optimize',
    value: function optimize() {
      var mutations = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];
      var context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

      if (this.batch === true) return;
      _get(Scroll.prototype.__proto__ || Object.getPrototypeOf(Scroll.prototype), 'optimize', this).call(this, mutations, context);
      if (mutations.length > 0) {
        this.emitter.emit(_emitter2.default.events.SCROLL_OPTIMIZE, mutations, context);
      }
    }
  }, {
    key: 'path',
    value: function path(index) {
      return _get(Scroll.prototype.__proto__ || Object.getPrototypeOf(Scroll.prototype), 'path', this).call(this, index).slice(1); // Exclude self
    }
  }, {
    key: 'update',
    value: function update(mutations) {
      if (this.batch === true) return;
      var source = _emitter2.default.sources.USER;
      if (typeof mutations === 'string') {
        source = mutations;
      }
      if (!Array.isArray(mutations)) {
        mutations = this.observer.takeRecords();
      }
      if (mutations.length > 0) {
        this.emitter.emit(_emitter2.default.events.SCROLL_BEFORE_UPDATE, source, mutations);
      }
      _get(Scroll.prototype.__proto__ || Object.getPrototypeOf(Scroll.prototype), 'update', this).call(this, mutations.concat([])); // pass copy
      if (mutations.length > 0) {
        this.emitter.emit(_emitter2.default.events.SCROLL_UPDATE, source, mutations);
      }
    }
  }]);

  return Scroll;
}(_parchment2.default.Scroll);

Scroll.blotName = 'scroll';
Scroll.className = 'ql-editor';
Scroll.tagName = 'DIV';
Scroll.defaultChild = 'block';
Scroll.allowedChildren = [_block2.default, _block.BlockEmbed, _container2.default];

exports.default = Scroll;

/***/ }),
/* 23 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.SHORTKEY = exports.default = undefined;

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _clone = __webpack_require__(21);

var _clone2 = _interopRequireDefault(_clone);

var _deepEqual = __webpack_require__(11);

var _deepEqual2 = _interopRequireDefault(_deepEqual);

var _extend = __webpack_require__(3);

var _extend2 = _interopRequireDefault(_extend);

var _quillDelta = __webpack_require__(2);

var _quillDelta2 = _interopRequireDefault(_quillDelta);

var _op = __webpack_require__(20);

var _op2 = _interopRequireDefault(_op);

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _quill = __webpack_require__(5);

var _quill2 = _interopRequireDefault(_quill);

var _logger = __webpack_require__(10);

var _logger2 = _interopRequireDefault(_logger);

var _module = __webpack_require__(9);

var _module2 = _interopRequireDefault(_module);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var debug = (0, _logger2.default)('quill:keyboard');

var SHORTKEY = /Mac/i.test(navigator.platform) ? 'metaKey' : 'ctrlKey';

var Keyboard = function (_Module) {
  _inherits(Keyboard, _Module);

  _createClass(Keyboard, null, [{
    key: 'match',
    value: function match(evt, binding) {
      binding = normalize(binding);
      if (['altKey', 'ctrlKey', 'metaKey', 'shiftKey'].some(function (key) {
        return !!binding[key] !== evt[key] && binding[key] !== null;
      })) {
        return false;
      }
      return binding.key === (evt.which || evt.keyCode);
    }
  }]);

  function Keyboard(quill, options) {
    _classCallCheck(this, Keyboard);

    var _this = _possibleConstructorReturn(this, (Keyboard.__proto__ || Object.getPrototypeOf(Keyboard)).call(this, quill, options));

    _this.bindings = {};
    Object.keys(_this.options.bindings).forEach(function (name) {
      if (name === 'list autofill' && quill.scroll.whitelist != null && !quill.scroll.whitelist['list']) {
        return;
      }
      if (_this.options.bindings[name]) {
        _this.addBinding(_this.options.bindings[name]);
      }
    });
    _this.addBinding({ key: Keyboard.keys.ENTER, shiftKey: null }, handleEnter);
    _this.addBinding({ key: Keyboard.keys.ENTER, metaKey: null, ctrlKey: null, altKey: null }, function () {});
    if (/Firefox/i.test(navigator.userAgent)) {
      // Need to handle delete and backspace for Firefox in the general case #1171
      _this.addBinding({ key: Keyboard.keys.BACKSPACE }, { collapsed: true }, handleBackspace);
      _this.addBinding({ key: Keyboard.keys.DELETE }, { collapsed: true }, handleDelete);
    } else {
      _this.addBinding({ key: Keyboard.keys.BACKSPACE }, { collapsed: true, prefix: /^.?$/ }, handleBackspace);
      _this.addBinding({ key: Keyboard.keys.DELETE }, { collapsed: true, suffix: /^.?$/ }, handleDelete);
    }
    _this.addBinding({ key: Keyboard.keys.BACKSPACE }, { collapsed: false }, handleDeleteRange);
    _this.addBinding({ key: Keyboard.keys.DELETE }, { collapsed: false }, handleDeleteRange);
    _this.addBinding({ key: Keyboard.keys.BACKSPACE, altKey: null, ctrlKey: null, metaKey: null, shiftKey: null }, { collapsed: true, offset: 0 }, handleBackspace);
    _this.listen();
    return _this;
  }

  _createClass(Keyboard, [{
    key: 'addBinding',
    value: function addBinding(key) {
      var context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
      var handler = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};

      var binding = normalize(key);
      if (binding == null || binding.key == null) {
        return debug.warn('Attempted to add invalid keyboard binding', binding);
      }
      if (typeof context === 'function') {
        context = { handler: context };
      }
      if (typeof handler === 'function') {
        handler = { handler: handler };
      }
      binding = (0, _extend2.default)(binding, context, handler);
      this.bindings[binding.key] = this.bindings[binding.key] || [];
      this.bindings[binding.key].push(binding);
    }
  }, {
    key: 'listen',
    value: function listen() {
      var _this2 = this;

      this.quill.root.addEventListener('keydown', function (evt) {
        if (evt.defaultPrevented) return;
        var which = evt.which || evt.keyCode;
        var bindings = (_this2.bindings[which] || []).filter(function (binding) {
          return Keyboard.match(evt, binding);
        });
        if (bindings.length === 0) return;
        var range = _this2.quill.getSelection();
        if (range == null || !_this2.quill.hasFocus()) return;

        var _quill$getLine = _this2.quill.getLine(range.index),
            _quill$getLine2 = _slicedToArray(_quill$getLine, 2),
            line = _quill$getLine2[0],
            offset = _quill$getLine2[1];

        var _quill$getLeaf = _this2.quill.getLeaf(range.index),
            _quill$getLeaf2 = _slicedToArray(_quill$getLeaf, 2),
            leafStart = _quill$getLeaf2[0],
            offsetStart = _quill$getLeaf2[1];

        var _ref = range.length === 0 ? [leafStart, offsetStart] : _this2.quill.getLeaf(range.index + range.length),
            _ref2 = _slicedToArray(_ref, 2),
            leafEnd = _ref2[0],
            offsetEnd = _ref2[1];

        var prefixText = leafStart instanceof _parchment2.default.Text ? leafStart.value().slice(0, offsetStart) : '';
        var suffixText = leafEnd instanceof _parchment2.default.Text ? leafEnd.value().slice(offsetEnd) : '';
        var curContext = {
          collapsed: range.length === 0,
          empty: range.length === 0 && line.length() <= 1,
          format: _this2.quill.getFormat(range),
          offset: offset,
          prefix: prefixText,
          suffix: suffixText
        };
        var prevented = bindings.some(function (binding) {
          if (binding.collapsed != null && binding.collapsed !== curContext.collapsed) return false;
          if (binding.empty != null && binding.empty !== curContext.empty) return false;
          if (binding.offset != null && binding.offset !== curContext.offset) return false;
          if (Array.isArray(binding.format)) {
            // any format is present
            if (binding.format.every(function (name) {
              return curContext.format[name] == null;
            })) {
              return false;
            }
          } else if (_typeof(binding.format) === 'object') {
            // all formats must match
            if (!Object.keys(binding.format).every(function (name) {
              if (binding.format[name] === true) return curContext.format[name] != null;
              if (binding.format[name] === false) return curContext.format[name] == null;
              return (0, _deepEqual2.default)(binding.format[name], curContext.format[name]);
            })) {
              return false;
            }
          }
          if (binding.prefix != null && !binding.prefix.test(curContext.prefix)) return false;
          if (binding.suffix != null && !binding.suffix.test(curContext.suffix)) return false;
          return binding.handler.call(_this2, range, curContext) !== true;
        });
        if (prevented) {
          evt.preventDefault();
        }
      });
    }
  }]);

  return Keyboard;
}(_module2.default);

Keyboard.keys = {
  BACKSPACE: 8,
  TAB: 9,
  ENTER: 13,
  ESCAPE: 27,
  LEFT: 37,
  UP: 38,
  RIGHT: 39,
  DOWN: 40,
  DELETE: 46
};

Keyboard.DEFAULTS = {
  bindings: {
    'bold': makeFormatHandler('bold'),
    'italic': makeFormatHandler('italic'),
    'underline': makeFormatHandler('underline'),
    'indent': {
      // highlight tab or tab at beginning of list, indent or blockquote
      key: Keyboard.keys.TAB,
      format: ['blockquote', 'indent', 'list'],
      handler: function handler(range, context) {
        if (context.collapsed && context.offset !== 0) return true;
        this.quill.format('indent', '+1', _quill2.default.sources.USER);
      }
    },
    'outdent': {
      key: Keyboard.keys.TAB,
      shiftKey: true,
      format: ['blockquote', 'indent', 'list'],
      // highlight tab or tab at beginning of list, indent or blockquote
      handler: function handler(range, context) {
        if (context.collapsed && context.offset !== 0) return true;
        this.quill.format('indent', '-1', _quill2.default.sources.USER);
      }
    },
    'outdent backspace': {
      key: Keyboard.keys.BACKSPACE,
      collapsed: true,
      shiftKey: null,
      metaKey: null,
      ctrlKey: null,
      altKey: null,
      format: ['indent', 'list'],
      offset: 0,
      handler: function handler(range, context) {
        if (context.format.indent != null) {
          this.quill.format('indent', '-1', _quill2.default.sources.USER);
        } else if (context.format.list != null) {
          this.quill.format('list', false, _quill2.default.sources.USER);
        }
      }
    },
    'indent code-block': makeCodeBlockHandler(true),
    'outdent code-block': makeCodeBlockHandler(false),
    'remove tab': {
      key: Keyboard.keys.TAB,
      shiftKey: true,
      collapsed: true,
      prefix: /\t$/,
      handler: function handler(range) {
        this.quill.deleteText(range.index - 1, 1, _quill2.default.sources.USER);
      }
    },
    'tab': {
      key: Keyboard.keys.TAB,
      handler: function handler(range) {
        this.quill.history.cutoff();
        var delta = new _quillDelta2.default().retain(range.index).delete(range.length).insert('\t');
        this.quill.updateContents(delta, _quill2.default.sources.USER);
        this.quill.history.cutoff();
        this.quill.setSelection(range.index + 1, _quill2.default.sources.SILENT);
      }
    },
    'list empty enter': {
      key: Keyboard.keys.ENTER,
      collapsed: true,
      format: ['list'],
      empty: true,
      handler: function handler(range, context) {
        this.quill.format('list', false, _quill2.default.sources.USER);
        if (context.format.indent) {
          this.quill.format('indent', false, _quill2.default.sources.USER);
        }
      }
    },
    'checklist enter': {
      key: Keyboard.keys.ENTER,
      collapsed: true,
      format: { list: 'checked' },
      handler: function handler(range) {
        var _quill$getLine3 = this.quill.getLine(range.index),
            _quill$getLine4 = _slicedToArray(_quill$getLine3, 2),
            line = _quill$getLine4[0],
            offset = _quill$getLine4[1];

        var formats = (0, _extend2.default)({}, line.formats(), { list: 'checked' });
        var delta = new _quillDelta2.default().retain(range.index).insert('\n', formats).retain(line.length() - offset - 1).retain(1, { list: 'unchecked' });
        this.quill.updateContents(delta, _quill2.default.sources.USER);
        this.quill.setSelection(range.index + 1, _quill2.default.sources.SILENT);
        this.quill.scrollIntoView();
      }
    },
    'header enter': {
      key: Keyboard.keys.ENTER,
      collapsed: true,
      format: ['header'],
      suffix: /^$/,
      handler: function handler(range, context) {
        var _quill$getLine5 = this.quill.getLine(range.index),
            _quill$getLine6 = _slicedToArray(_quill$getLine5, 2),
            line = _quill$getLine6[0],
            offset = _quill$getLine6[1];

        var delta = new _quillDelta2.default().retain(range.index).insert('\n', context.format).retain(line.length() - offset - 1).retain(1, { header: null });
        this.quill.updateContents(delta, _quill2.default.sources.USER);
        this.quill.setSelection(range.index + 1, _quill2.default.sources.SILENT);
        this.quill.scrollIntoView();
      }
    },
    'list autofill': {
      key: ' ',
      collapsed: true,
      format: { list: false },
      prefix: /^\s*?(\d+\.|-|\*|\[ ?\]|\[x\])$/,
      handler: function handler(range, context) {
        var length = context.prefix.length;

        var _quill$getLine7 = this.quill.getLine(range.index),
            _quill$getLine8 = _slicedToArray(_quill$getLine7, 2),
            line = _quill$getLine8[0],
            offset = _quill$getLine8[1];

        if (offset > length) return true;
        var value = void 0;
        switch (context.prefix.trim()) {
          case '[]':case '[ ]':
            value = 'unchecked';
            break;
          case '[x]':
            value = 'checked';
            break;
          case '-':case '*':
            value = 'bullet';
            break;
          default:
            value = 'ordered';
        }
        this.quill.insertText(range.index, ' ', _quill2.default.sources.USER);
        this.quill.history.cutoff();
        var delta = new _quillDelta2.default().retain(range.index - offset).delete(length + 1).retain(line.length() - 2 - offset).retain(1, { list: value });
        this.quill.updateContents(delta, _quill2.default.sources.USER);
        this.quill.history.cutoff();
        this.quill.setSelection(range.index - length, _quill2.default.sources.SILENT);
      }
    },
    'code exit': {
      key: Keyboard.keys.ENTER,
      collapsed: true,
      format: ['code-block'],
      prefix: /\n\n$/,
      suffix: /^\s+$/,
      handler: function handler(range) {
        var _quill$getLine9 = this.quill.getLine(range.index),
            _quill$getLine10 = _slicedToArray(_quill$getLine9, 2),
            line = _quill$getLine10[0],
            offset = _quill$getLine10[1];

        var delta = new _quillDelta2.default().retain(range.index + line.length() - offset - 2).retain(1, { 'code-block': null }).delete(1);
        this.quill.updateContents(delta, _quill2.default.sources.USER);
      }
    },
    'embed left': makeEmbedArrowHandler(Keyboard.keys.LEFT, false),
    'embed left shift': makeEmbedArrowHandler(Keyboard.keys.LEFT, true),
    'embed right': makeEmbedArrowHandler(Keyboard.keys.RIGHT, false),
    'embed right shift': makeEmbedArrowHandler(Keyboard.keys.RIGHT, true)
  }
};

function makeEmbedArrowHandler(key, shiftKey) {
  var _ref3;

  var where = key === Keyboard.keys.LEFT ? 'prefix' : 'suffix';
  return _ref3 = {
    key: key,
    shiftKey: shiftKey,
    altKey: null
  }, _defineProperty(_ref3, where, /^$/), _defineProperty(_ref3, 'handler', function handler(range) {
    var index = range.index;
    if (key === Keyboard.keys.RIGHT) {
      index += range.length + 1;
    }

    var _quill$getLeaf3 = this.quill.getLeaf(index),
        _quill$getLeaf4 = _slicedToArray(_quill$getLeaf3, 1),
        leaf = _quill$getLeaf4[0];

    if (!(leaf instanceof _parchment2.default.Embed)) return true;
    if (key === Keyboard.keys.LEFT) {
      if (shiftKey) {
        this.quill.setSelection(range.index - 1, range.length + 1, _quill2.default.sources.USER);
      } else {
        this.quill.setSelection(range.index - 1, _quill2.default.sources.USER);
      }
    } else {
      if (shiftKey) {
        this.quill.setSelection(range.index, range.length + 1, _quill2.default.sources.USER);
      } else {
        this.quill.setSelection(range.index + range.length + 1, _quill2.default.sources.USER);
      }
    }
    return false;
  }), _ref3;
}

function handleBackspace(range, context) {
  if (range.index === 0 || this.quill.getLength() <= 1) return;

  var _quill$getLine11 = this.quill.getLine(range.index),
      _quill$getLine12 = _slicedToArray(_quill$getLine11, 1),
      line = _quill$getLine12[0];

  var formats = {};
  if (context.offset === 0) {
    var _quill$getLine13 = this.quill.getLine(range.index - 1),
        _quill$getLine14 = _slicedToArray(_quill$getLine13, 1),
        prev = _quill$getLine14[0];

    if (prev != null && prev.length() > 1) {
      var curFormats = line.formats();
      var prevFormats = this.quill.getFormat(range.index - 1, 1);
      formats = _op2.default.attributes.diff(curFormats, prevFormats) || {};
    }
  }
  // Check for astral symbols
  var length = /[\uD800-\uDBFF][\uDC00-\uDFFF]$/.test(context.prefix) ? 2 : 1;
  this.quill.deleteText(range.index - length, length, _quill2.default.sources.USER);
  if (Object.keys(formats).length > 0) {
    this.quill.formatLine(range.index - length, length, formats, _quill2.default.sources.USER);
  }
  this.quill.focus();
}

function handleDelete(range, context) {
  // Check for astral symbols
  var length = /^[\uD800-\uDBFF][\uDC00-\uDFFF]/.test(context.suffix) ? 2 : 1;
  if (range.index >= this.quill.getLength() - length) return;
  var formats = {},
      nextLength = 0;

  var _quill$getLine15 = this.quill.getLine(range.index),
      _quill$getLine16 = _slicedToArray(_quill$getLine15, 1),
      line = _quill$getLine16[0];

  if (context.offset >= line.length() - 1) {
    var _quill$getLine17 = this.quill.getLine(range.index + 1),
        _quill$getLine18 = _slicedToArray(_quill$getLine17, 1),
        next = _quill$getLine18[0];

    if (next) {
      var curFormats = line.formats();
      var nextFormats = this.quill.getFormat(range.index, 1);
      formats = _op2.default.attributes.diff(curFormats, nextFormats) || {};
      nextLength = next.length();
    }
  }
  this.quill.deleteText(range.index, length, _quill2.default.sources.USER);
  if (Object.keys(formats).length > 0) {
    this.quill.formatLine(range.index + nextLength - 1, length, formats, _quill2.default.sources.USER);
  }
}

function handleDeleteRange(range) {
  var lines = this.quill.getLines(range);
  var formats = {};
  if (lines.length > 1) {
    var firstFormats = lines[0].formats();
    var lastFormats = lines[lines.length - 1].formats();
    formats = _op2.default.attributes.diff(lastFormats, firstFormats) || {};
  }
  this.quill.deleteText(range, _quill2.default.sources.USER);
  if (Object.keys(formats).length > 0) {
    this.quill.formatLine(range.index, 1, formats, _quill2.default.sources.USER);
  }
  this.quill.setSelection(range.index, _quill2.default.sources.SILENT);
  this.quill.focus();
}

function handleEnter(range, context) {
  var _this3 = this;

  if (range.length > 0) {
    this.quill.scroll.deleteAt(range.index, range.length); // So we do not trigger text-change
  }
  var lineFormats = Object.keys(context.format).reduce(function (lineFormats, format) {
    if (_parchment2.default.query(format, _parchment2.default.Scope.BLOCK) && !Array.isArray(context.format[format])) {
      lineFormats[format] = context.format[format];
    }
    return lineFormats;
  }, {});
  this.quill.insertText(range.index, '\n', lineFormats, _quill2.default.sources.USER);
  // Earlier scroll.deleteAt might have messed up our selection,
  // so insertText's built in selection preservation is not reliable
  this.quill.setSelection(range.index + 1, _quill2.default.sources.SILENT);
  this.quill.focus();
  Object.keys(context.format).forEach(function (name) {
    if (lineFormats[name] != null) return;
    if (Array.isArray(context.format[name])) return;
    if (name === 'link') return;
    _this3.quill.format(name, context.format[name], _quill2.default.sources.USER);
  });
}

function makeCodeBlockHandler(indent) {
  return {
    key: Keyboard.keys.TAB,
    shiftKey: !indent,
    format: { 'code-block': true },
    handler: function handler(range) {
      var CodeBlock = _parchment2.default.query('code-block');
      var index = range.index,
          length = range.length;

      var _quill$scroll$descend = this.quill.scroll.descendant(CodeBlock, index),
          _quill$scroll$descend2 = _slicedToArray(_quill$scroll$descend, 2),
          block = _quill$scroll$descend2[0],
          offset = _quill$scroll$descend2[1];

      if (block == null) return;
      var scrollIndex = this.quill.getIndex(block);
      var start = block.newlineIndex(offset, true) + 1;
      var end = block.newlineIndex(scrollIndex + offset + length);
      var lines = block.domNode.textContent.slice(start, end).split('\n');
      offset = 0;
      lines.forEach(function (line, i) {
        if (indent) {
          block.insertAt(start + offset, CodeBlock.TAB);
          offset += CodeBlock.TAB.length;
          if (i === 0) {
            index += CodeBlock.TAB.length;
          } else {
            length += CodeBlock.TAB.length;
          }
        } else if (line.startsWith(CodeBlock.TAB)) {
          block.deleteAt(start + offset, CodeBlock.TAB.length);
          offset -= CodeBlock.TAB.length;
          if (i === 0) {
            index -= CodeBlock.TAB.length;
          } else {
            length -= CodeBlock.TAB.length;
          }
        }
        offset += line.length + 1;
      });
      this.quill.update(_quill2.default.sources.USER);
      this.quill.setSelection(index, length, _quill2.default.sources.SILENT);
    }
  };
}

function makeFormatHandler(format) {
  return {
    key: format[0].toUpperCase(),
    shortKey: true,
    handler: function handler(range, context) {
      this.quill.format(format, !context.format[format], _quill2.default.sources.USER);
    }
  };
}

function normalize(binding) {
  if (typeof binding === 'string' || typeof binding === 'number') {
    return normalize({ key: binding });
  }
  if ((typeof binding === 'undefined' ? 'undefined' : _typeof(binding)) === 'object') {
    binding = (0, _clone2.default)(binding, false);
  }
  if (typeof binding.key === 'string') {
    if (Keyboard.keys[binding.key.toUpperCase()] != null) {
      binding.key = Keyboard.keys[binding.key.toUpperCase()];
    } else if (binding.key.length === 1) {
      binding.key = binding.key.toUpperCase().charCodeAt(0);
    } else {
      return null;
    }
  }
  if (binding.shortKey) {
    binding[SHORTKEY] = binding.shortKey;
    delete binding.shortKey;
  }
  return binding;
}

exports.default = Keyboard;
exports.SHORTKEY = SHORTKEY;

/***/ }),
/* 24 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _text = __webpack_require__(7);

var _text2 = _interopRequireDefault(_text);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Cursor = function (_Parchment$Embed) {
  _inherits(Cursor, _Parchment$Embed);

  _createClass(Cursor, null, [{
    key: 'value',
    value: function value() {
      return undefined;
    }
  }]);

  function Cursor(domNode, selection) {
    _classCallCheck(this, Cursor);

    var _this = _possibleConstructorReturn(this, (Cursor.__proto__ || Object.getPrototypeOf(Cursor)).call(this, domNode));

    _this.selection = selection;
    _this.textNode = document.createTextNode(Cursor.CONTENTS);
    _this.domNode.appendChild(_this.textNode);
    _this._length = 0;
    return _this;
  }

  _createClass(Cursor, [{
    key: 'detach',
    value: function detach() {
      // super.detach() will also clear domNode.__blot
      if (this.parent != null) this.parent.removeChild(this);
    }
  }, {
    key: 'format',
    value: function format(name, value) {
      if (this._length !== 0) {
        return _get(Cursor.prototype.__proto__ || Object.getPrototypeOf(Cursor.prototype), 'format', this).call(this, name, value);
      }
      var target = this,
          index = 0;
      while (target != null && target.statics.scope !== _parchment2.default.Scope.BLOCK_BLOT) {
        index += target.offset(target.parent);
        target = target.parent;
      }
      if (target != null) {
        this._length = Cursor.CONTENTS.length;
        target.optimize();
        target.formatAt(index, Cursor.CONTENTS.length, name, value);
        this._length = 0;
      }
    }
  }, {
    key: 'index',
    value: function index(node, offset) {
      if (node === this.textNode) return 0;
      return _get(Cursor.prototype.__proto__ || Object.getPrototypeOf(Cursor.prototype), 'index', this).call(this, node, offset);
    }
  }, {
    key: 'length',
    value: function length() {
      return this._length;
    }
  }, {
    key: 'position',
    value: function position() {
      return [this.textNode, this.textNode.data.length];
    }
  }, {
    key: 'remove',
    value: function remove() {
      _get(Cursor.prototype.__proto__ || Object.getPrototypeOf(Cursor.prototype), 'remove', this).call(this);
      this.parent = null;
    }
  }, {
    key: 'restore',
    value: function restore() {
      if (this.selection.composing || this.parent == null) return;
      var textNode = this.textNode;
      var range = this.selection.getNativeRange();
      var restoreText = void 0,
          start = void 0,
          end = void 0;
      if (range != null && range.start.node === textNode && range.end.node === textNode) {
        var _ref = [textNode, range.start.offset, range.end.offset];
        restoreText = _ref[0];
        start = _ref[1];
        end = _ref[2];
      }
      // Link format will insert text outside of anchor tag
      while (this.domNode.lastChild != null && this.domNode.lastChild !== this.textNode) {
        this.domNode.parentNode.insertBefore(this.domNode.lastChild, this.domNode);
      }
      if (this.textNode.data !== Cursor.CONTENTS) {
        var text = this.textNode.data.split(Cursor.CONTENTS).join('');
        if (this.next instanceof _text2.default) {
          restoreText = this.next.domNode;
          this.next.insertAt(0, text);
          this.textNode.data = Cursor.CONTENTS;
        } else {
          this.textNode.data = text;
          this.parent.insertBefore(_parchment2.default.create(this.textNode), this);
          this.textNode = document.createTextNode(Cursor.CONTENTS);
          this.domNode.appendChild(this.textNode);
        }
      }
      this.remove();
      if (start != null) {
        var _map = [start, end].map(function (offset) {
          return Math.max(0, Math.min(restoreText.data.length, offset - 1));
        });

        var _map2 = _slicedToArray(_map, 2);

        start = _map2[0];
        end = _map2[1];

        return {
          startNode: restoreText,
          startOffset: start,
          endNode: restoreText,
          endOffset: end
        };
      }
    }
  }, {
    key: 'update',
    value: function update(mutations, context) {
      var _this2 = this;

      if (mutations.some(function (mutation) {
        return mutation.type === 'characterData' && mutation.target === _this2.textNode;
      })) {
        var range = this.restore();
        if (range) context.range = range;
      }
    }
  }, {
    key: 'value',
    value: function value() {
      return '';
    }
  }]);

  return Cursor;
}(_parchment2.default.Embed);

Cursor.blotName = 'cursor';
Cursor.className = 'ql-cursor';
Cursor.tagName = 'span';
Cursor.CONTENTS = '\uFEFF'; // Zero width no break space


exports.default = Cursor;

/***/ }),
/* 25 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _block = __webpack_require__(4);

var _block2 = _interopRequireDefault(_block);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Container = function (_Parchment$Container) {
  _inherits(Container, _Parchment$Container);

  function Container() {
    _classCallCheck(this, Container);

    return _possibleConstructorReturn(this, (Container.__proto__ || Object.getPrototypeOf(Container)).apply(this, arguments));
  }

  return Container;
}(_parchment2.default.Container);

Container.allowedChildren = [_block2.default, _block.BlockEmbed, Container];

exports.default = Container;

/***/ }),
/* 26 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.ColorStyle = exports.ColorClass = exports.ColorAttributor = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var ColorAttributor = function (_Parchment$Attributor) {
  _inherits(ColorAttributor, _Parchment$Attributor);

  function ColorAttributor() {
    _classCallCheck(this, ColorAttributor);

    return _possibleConstructorReturn(this, (ColorAttributor.__proto__ || Object.getPrototypeOf(ColorAttributor)).apply(this, arguments));
  }

  _createClass(ColorAttributor, [{
    key: 'value',
    value: function value(domNode) {
      var value = _get(ColorAttributor.prototype.__proto__ || Object.getPrototypeOf(ColorAttributor.prototype), 'value', this).call(this, domNode);
      if (!value.startsWith('rgb(')) return value;
      value = value.replace(/^[^\d]+/, '').replace(/[^\d]+$/, '');
      return '#' + value.split(',').map(function (component) {
        return ('00' + parseInt(component).toString(16)).slice(-2);
      }).join('');
    }
  }]);

  return ColorAttributor;
}(_parchment2.default.Attributor.Style);

var ColorClass = new _parchment2.default.Attributor.Class('color', 'ql-color', {
  scope: _parchment2.default.Scope.INLINE
});
var ColorStyle = new ColorAttributor('color', 'color', {
  scope: _parchment2.default.Scope.INLINE
});

exports.ColorAttributor = ColorAttributor;
exports.ColorClass = ColorClass;
exports.ColorStyle = ColorStyle;

/***/ }),
/* 27 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.sanitize = exports.default = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _inline = __webpack_require__(6);

var _inline2 = _interopRequireDefault(_inline);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Link = function (_Inline) {
  _inherits(Link, _Inline);

  function Link() {
    _classCallCheck(this, Link);

    return _possibleConstructorReturn(this, (Link.__proto__ || Object.getPrototypeOf(Link)).apply(this, arguments));
  }

  _createClass(Link, [{
    key: 'format',
    value: function format(name, value) {
      if (name !== this.statics.blotName || !value) return _get(Link.prototype.__proto__ || Object.getPrototypeOf(Link.prototype), 'format', this).call(this, name, value);
      value = this.constructor.sanitize(value);
      this.domNode.setAttribute('href', value);
    }
  }], [{
    key: 'create',
    value: function create(value) {
      var node = _get(Link.__proto__ || Object.getPrototypeOf(Link), 'create', this).call(this, value);
      value = this.sanitize(value);
      node.setAttribute('href', value);
      node.setAttribute('target', '_blank');
      return node;
    }
  }, {
    key: 'formats',
    value: function formats(domNode) {
      return domNode.getAttribute('href');
    }
  }, {
    key: 'sanitize',
    value: function sanitize(url) {
      return _sanitize(url, this.PROTOCOL_WHITELIST) ? url : this.SANITIZED_URL;
    }
  }]);

  return Link;
}(_inline2.default);

Link.blotName = 'link';
Link.tagName = 'A';
Link.SANITIZED_URL = 'about:blank';
Link.PROTOCOL_WHITELIST = ['http', 'https', 'mailto', 'tel'];

function _sanitize(url, protocols) {
  var anchor = document.createElement('a');
  anchor.href = url;
  var protocol = anchor.href.slice(0, anchor.href.indexOf(':'));
  return protocols.indexOf(protocol) > -1;
}

exports.default = Link;
exports.sanitize = _sanitize;

/***/ }),
/* 28 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _keyboard = __webpack_require__(23);

var _keyboard2 = _interopRequireDefault(_keyboard);

var _dropdown = __webpack_require__(107);

var _dropdown2 = _interopRequireDefault(_dropdown);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var optionsCounter = 0;

function toggleAriaAttribute(element, attribute) {
  element.setAttribute(attribute, !(element.getAttribute(attribute) === 'true'));
}

var Picker = function () {
  function Picker(select) {
    var _this = this;

    _classCallCheck(this, Picker);

    this.select = select;
    this.container = document.createElement('span');
    this.buildPicker();
    this.select.style.display = 'none';
    this.select.parentNode.insertBefore(this.container, this.select);

    this.label.addEventListener('mousedown', function () {
      _this.togglePicker();
    });
    this.label.addEventListener('keydown', function (event) {
      switch (event.keyCode) {
        // Allows the "Enter" key to open the picker
        case _keyboard2.default.keys.ENTER:
          _this.togglePicker();
          break;

        // Allows the "Escape" key to close the picker
        case _keyboard2.default.keys.ESCAPE:
          _this.escape();
          event.preventDefault();
          break;
        default:
      }
    });
    this.select.addEventListener('change', this.update.bind(this));
  }

  _createClass(Picker, [{
    key: 'togglePicker',
    value: function togglePicker() {
      this.container.classList.toggle('ql-expanded');
      // Toggle aria-expanded and aria-hidden to make the picker accessible
      toggleAriaAttribute(this.label, 'aria-expanded');
      toggleAriaAttribute(this.options, 'aria-hidden');
    }
  }, {
    key: 'buildItem',
    value: function buildItem(option) {
      var _this2 = this;

      var item = document.createElement('span');
      item.tabIndex = '0';
      item.setAttribute('role', 'button');

      item.classList.add('ql-picker-item');
      if (option.hasAttribute('value')) {
        item.setAttribute('data-value', option.getAttribute('value'));
      }
      if (option.textContent) {
        item.setAttribute('data-label', option.textContent);
      }
      item.addEventListener('click', function () {
        _this2.selectItem(item, true);
      });
      item.addEventListener('keydown', function (event) {
        switch (event.keyCode) {
          // Allows the "Enter" key to select an item
          case _keyboard2.default.keys.ENTER:
            _this2.selectItem(item, true);
            event.preventDefault();
            break;

          // Allows the "Escape" key to close the picker
          case _keyboard2.default.keys.ESCAPE:
            _this2.escape();
            event.preventDefault();
            break;
          default:
        }
      });

      return item;
    }
  }, {
    key: 'buildLabel',
    value: function buildLabel() {
      var label = document.createElement('span');
      label.classList.add('ql-picker-label');
      label.innerHTML = _dropdown2.default;
      label.tabIndex = '0';
      label.setAttribute('role', 'button');
      label.setAttribute('aria-expanded', 'false');
      this.container.appendChild(label);
      return label;
    }
  }, {
    key: 'buildOptions',
    value: function buildOptions() {
      var _this3 = this;

      var options = document.createElement('span');
      options.classList.add('ql-picker-options');

      // Don't want screen readers to read this until options are visible
      options.setAttribute('aria-hidden', 'true');
      options.tabIndex = '-1';

      // Need a unique id for aria-controls
      options.id = 'ql-picker-options-' + optionsCounter;
      optionsCounter += 1;
      this.label.setAttribute('aria-controls', options.id);

      this.options = options;

      [].slice.call(this.select.options).forEach(function (option) {
        var item = _this3.buildItem(option);
        options.appendChild(item);
        if (option.selected === true) {
          _this3.selectItem(item);
        }
      });
      this.container.appendChild(options);
    }
  }, {
    key: 'buildPicker',
    value: function buildPicker() {
      var _this4 = this;

      [].slice.call(this.select.attributes).forEach(function (item) {
        _this4.container.setAttribute(item.name, item.value);
      });
      this.container.classList.add('ql-picker');
      this.label = this.buildLabel();
      this.buildOptions();
    }
  }, {
    key: 'escape',
    value: function escape() {
      var _this5 = this;

      // Close menu and return focus to trigger label
      this.close();
      // Need setTimeout for accessibility to ensure that the browser executes
      // focus on the next process thread and after any DOM content changes
      setTimeout(function () {
        return _this5.label.focus();
      }, 1);
    }
  }, {
    key: 'close',
    value: function close() {
      this.container.classList.remove('ql-expanded');
      this.label.setAttribute('aria-expanded', 'false');
      this.options.setAttribute('aria-hidden', 'true');
    }
  }, {
    key: 'selectItem',
    value: function selectItem(item) {
      var trigger = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;

      var selected = this.container.querySelector('.ql-selected');
      if (item === selected) return;
      if (selected != null) {
        selected.classList.remove('ql-selected');
      }
      if (item == null) return;
      item.classList.add('ql-selected');
      this.select.selectedIndex = [].indexOf.call(item.parentNode.children, item);
      if (item.hasAttribute('data-value')) {
        this.label.setAttribute('data-value', item.getAttribute('data-value'));
      } else {
        this.label.removeAttribute('data-value');
      }
      if (item.hasAttribute('data-label')) {
        this.label.setAttribute('data-label', item.getAttribute('data-label'));
      } else {
        this.label.removeAttribute('data-label');
      }
      if (trigger) {
        if (typeof Event === 'function') {
          this.select.dispatchEvent(new Event('change'));
        } else if ((typeof Event === 'undefined' ? 'undefined' : _typeof(Event)) === 'object') {
          // IE11
          var event = document.createEvent('Event');
          event.initEvent('change', true, true);
          this.select.dispatchEvent(event);
        }
        this.close();
      }
    }
  }, {
    key: 'update',
    value: function update() {
      var option = void 0;
      if (this.select.selectedIndex > -1) {
        var item = this.container.querySelector('.ql-picker-options').children[this.select.selectedIndex];
        option = this.select.options[this.select.selectedIndex];
        this.selectItem(item);
      } else {
        this.selectItem(null);
      }
      var isActive = option != null && option !== this.select.querySelector('option[selected]');
      this.label.classList.toggle('ql-active', isActive);
    }
  }]);

  return Picker;
}();

exports.default = Picker;

/***/ }),
/* 29 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _quill = __webpack_require__(5);

var _quill2 = _interopRequireDefault(_quill);

var _block = __webpack_require__(4);

var _block2 = _interopRequireDefault(_block);

var _break = __webpack_require__(16);

var _break2 = _interopRequireDefault(_break);

var _container = __webpack_require__(25);

var _container2 = _interopRequireDefault(_container);

var _cursor = __webpack_require__(24);

var _cursor2 = _interopRequireDefault(_cursor);

var _embed = __webpack_require__(35);

var _embed2 = _interopRequireDefault(_embed);

var _inline = __webpack_require__(6);

var _inline2 = _interopRequireDefault(_inline);

var _scroll = __webpack_require__(22);

var _scroll2 = _interopRequireDefault(_scroll);

var _text = __webpack_require__(7);

var _text2 = _interopRequireDefault(_text);

var _clipboard = __webpack_require__(55);

var _clipboard2 = _interopRequireDefault(_clipboard);

var _history = __webpack_require__(42);

var _history2 = _interopRequireDefault(_history);

var _keyboard = __webpack_require__(23);

var _keyboard2 = _interopRequireDefault(_keyboard);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

_quill2.default.register({
  'blots/block': _block2.default,
  'blots/block/embed': _block.BlockEmbed,
  'blots/break': _break2.default,
  'blots/container': _container2.default,
  'blots/cursor': _cursor2.default,
  'blots/embed': _embed2.default,
  'blots/inline': _inline2.default,
  'blots/scroll': _scroll2.default,
  'blots/text': _text2.default,

  'modules/clipboard': _clipboard2.default,
  'modules/history': _history2.default,
  'modules/keyboard': _keyboard2.default
});

_parchment2.default.register(_block2.default, _break2.default, _cursor2.default, _inline2.default, _scroll2.default, _text2.default);

exports.default = _quill2.default;

/***/ }),
/* 30 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var Registry = __webpack_require__(1);
var ShadowBlot = /** @class */ (function () {
    function ShadowBlot(domNode) {
        this.domNode = domNode;
        // @ts-ignore
        this.domNode[Registry.DATA_KEY] = { blot: this };
    }
    Object.defineProperty(ShadowBlot.prototype, "statics", {
        // Hack for accessing inherited static methods
        get: function () {
            return this.constructor;
        },
        enumerable: true,
        configurable: true
    });
    ShadowBlot.create = function (value) {
        if (this.tagName == null) {
            throw new Registry.ParchmentError('Blot definition missing tagName');
        }
        var node;
        if (Array.isArray(this.tagName)) {
            if (typeof value === 'string') {
                value = value.toUpperCase();
                if (parseInt(value).toString() === value) {
                    value = parseInt(value);
                }
            }
            if (typeof value === 'number') {
                node = document.createElement(this.tagName[value - 1]);
            }
            else if (this.tagName.indexOf(value) > -1) {
                node = document.createElement(value);
            }
            else {
                node = document.createElement(this.tagName[0]);
            }
        }
        else {
            node = document.createElement(this.tagName);
        }
        if (this.className) {
            node.classList.add(this.className);
        }
        return node;
    };
    ShadowBlot.prototype.attach = function () {
        if (this.parent != null) {
            this.scroll = this.parent.scroll;
        }
    };
    ShadowBlot.prototype.clone = function () {
        var domNode = this.domNode.cloneNode(false);
        return Registry.create(domNode);
    };
    ShadowBlot.prototype.detach = function () {
        if (this.parent != null)
            this.parent.removeChild(this);
        // @ts-ignore
        delete this.domNode[Registry.DATA_KEY];
    };
    ShadowBlot.prototype.deleteAt = function (index, length) {
        var blot = this.isolate(index, length);
        blot.remove();
    };
    ShadowBlot.prototype.formatAt = function (index, length, name, value) {
        var blot = this.isolate(index, length);
        if (Registry.query(name, Registry.Scope.BLOT) != null && value) {
            blot.wrap(name, value);
        }
        else if (Registry.query(name, Registry.Scope.ATTRIBUTE) != null) {
            var parent = Registry.create(this.statics.scope);
            blot.wrap(parent);
            parent.format(name, value);
        }
    };
    ShadowBlot.prototype.insertAt = function (index, value, def) {
        var blot = def == null ? Registry.create('text', value) : Registry.create(value, def);
        var ref = this.split(index);
        this.parent.insertBefore(blot, ref);
    };
    ShadowBlot.prototype.insertInto = function (parentBlot, refBlot) {
        if (refBlot === void 0) { refBlot = null; }
        if (this.parent != null) {
            this.parent.children.remove(this);
        }
        var refDomNode = null;
        parentBlot.children.insertBefore(this, refBlot);
        if (refBlot != null) {
            refDomNode = refBlot.domNode;
        }
        if (this.domNode.parentNode != parentBlot.domNode ||
            this.domNode.nextSibling != refDomNode) {
            parentBlot.domNode.insertBefore(this.domNode, refDomNode);
        }
        this.parent = parentBlot;
        this.attach();
    };
    ShadowBlot.prototype.isolate = function (index, length) {
        var target = this.split(index);
        target.split(length);
        return target;
    };
    ShadowBlot.prototype.length = function () {
        return 1;
    };
    ShadowBlot.prototype.offset = function (root) {
        if (root === void 0) { root = this.parent; }
        if (this.parent == null || this == root)
            return 0;
        return this.parent.children.offset(this) + this.parent.offset(root);
    };
    ShadowBlot.prototype.optimize = function (context) {
        // TODO clean up once we use WeakMap
        // @ts-ignore
        if (this.domNode[Registry.DATA_KEY] != null) {
            // @ts-ignore
            delete this.domNode[Registry.DATA_KEY].mutations;
        }
    };
    ShadowBlot.prototype.remove = function () {
        if (this.domNode.parentNode != null) {
            this.domNode.parentNode.removeChild(this.domNode);
        }
        this.detach();
    };
    ShadowBlot.prototype.replace = function (target) {
        if (target.parent == null)
            return;
        target.parent.insertBefore(this, target.next);
        target.remove();
    };
    ShadowBlot.prototype.replaceWith = function (name, value) {
        var replacement = typeof name === 'string' ? Registry.create(name, value) : name;
        replacement.replace(this);
        return replacement;
    };
    ShadowBlot.prototype.split = function (index, force) {
        return index === 0 ? this : this.next;
    };
    ShadowBlot.prototype.update = function (mutations, context) {
        // Nothing to do by default
    };
    ShadowBlot.prototype.wrap = function (name, value) {
        var wrapper = typeof name === 'string' ? Registry.create(name, value) : name;
        if (this.parent != null) {
            this.parent.insertBefore(wrapper, this.next);
        }
        wrapper.appendChild(this);
        return wrapper;
    };
    ShadowBlot.blotName = 'abstract';
    return ShadowBlot;
}());
exports.default = ShadowBlot;


/***/ }),
/* 31 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var attributor_1 = __webpack_require__(12);
var class_1 = __webpack_require__(32);
var style_1 = __webpack_require__(33);
var Registry = __webpack_require__(1);
var AttributorStore = /** @class */ (function () {
    function AttributorStore(domNode) {
        this.attributes = {};
        this.domNode = domNode;
        this.build();
    }
    AttributorStore.prototype.attribute = function (attribute, value) {
        // verb
        if (value) {
            if (attribute.add(this.domNode, value)) {
                if (attribute.value(this.domNode) != null) {
                    this.attributes[attribute.attrName] = attribute;
                }
                else {
                    delete this.attributes[attribute.attrName];
                }
            }
        }
        else {
            attribute.remove(this.domNode);
            delete this.attributes[attribute.attrName];
        }
    };
    AttributorStore.prototype.build = function () {
        var _this = this;
        this.attributes = {};
        var attributes = attributor_1.default.keys(this.domNode);
        var classes = class_1.default.keys(this.domNode);
        var styles = style_1.default.keys(this.domNode);
        attributes
            .concat(classes)
            .concat(styles)
            .forEach(function (name) {
            var attr = Registry.query(name, Registry.Scope.ATTRIBUTE);
            if (attr instanceof attributor_1.default) {
                _this.attributes[attr.attrName] = attr;
            }
        });
    };
    AttributorStore.prototype.copy = function (target) {
        var _this = this;
        Object.keys(this.attributes).forEach(function (key) {
            var value = _this.attributes[key].value(_this.domNode);
            target.format(key, value);
        });
    };
    AttributorStore.prototype.move = function (target) {
        var _this = this;
        this.copy(target);
        Object.keys(this.attributes).forEach(function (key) {
            _this.attributes[key].remove(_this.domNode);
        });
        this.attributes = {};
    };
    AttributorStore.prototype.values = function () {
        var _this = this;
        return Object.keys(this.attributes).reduce(function (attributes, name) {
            attributes[name] = _this.attributes[name].value(_this.domNode);
            return attributes;
        }, {});
    };
    return AttributorStore;
}());
exports.default = AttributorStore;


/***/ }),
/* 32 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var attributor_1 = __webpack_require__(12);
function match(node, prefix) {
    var className = node.getAttribute('class') || '';
    return className.split(/\s+/).filter(function (name) {
        return name.indexOf(prefix + "-") === 0;
    });
}
var ClassAttributor = /** @class */ (function (_super) {
    __extends(ClassAttributor, _super);
    function ClassAttributor() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ClassAttributor.keys = function (node) {
        return (node.getAttribute('class') || '').split(/\s+/).map(function (name) {
            return name
                .split('-')
                .slice(0, -1)
                .join('-');
        });
    };
    ClassAttributor.prototype.add = function (node, value) {
        if (!this.canAdd(node, value))
            return false;
        this.remove(node);
        node.classList.add(this.keyName + "-" + value);
        return true;
    };
    ClassAttributor.prototype.remove = function (node) {
        var matches = match(node, this.keyName);
        matches.forEach(function (name) {
            node.classList.remove(name);
        });
        if (node.classList.length === 0) {
            node.removeAttribute('class');
        }
    };
    ClassAttributor.prototype.value = function (node) {
        var result = match(node, this.keyName)[0] || '';
        var value = result.slice(this.keyName.length + 1); // +1 for hyphen
        return this.canAdd(node, value) ? value : '';
    };
    return ClassAttributor;
}(attributor_1.default));
exports.default = ClassAttributor;


/***/ }),
/* 33 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var attributor_1 = __webpack_require__(12);
function camelize(name) {
    var parts = name.split('-');
    var rest = parts
        .slice(1)
        .map(function (part) {
        return part[0].toUpperCase() + part.slice(1);
    })
        .join('');
    return parts[0] + rest;
}
var StyleAttributor = /** @class */ (function (_super) {
    __extends(StyleAttributor, _super);
    function StyleAttributor() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    StyleAttributor.keys = function (node) {
        return (node.getAttribute('style') || '').split(';').map(function (value) {
            var arr = value.split(':');
            return arr[0].trim();
        });
    };
    StyleAttributor.prototype.add = function (node, value) {
        if (!this.canAdd(node, value))
            return false;
        // @ts-ignore
        node.style[camelize(this.keyName)] = value;
        return true;
    };
    StyleAttributor.prototype.remove = function (node) {
        // @ts-ignore
        node.style[camelize(this.keyName)] = '';
        if (!node.getAttribute('style')) {
            node.removeAttribute('style');
        }
    };
    StyleAttributor.prototype.value = function (node) {
        // @ts-ignore
        var value = node.style[camelize(this.keyName)];
        return this.canAdd(node, value) ? value : '';
    };
    return StyleAttributor;
}(attributor_1.default));
exports.default = StyleAttributor;


/***/ }),
/* 34 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Theme = function () {
  function Theme(quill, options) {
    _classCallCheck(this, Theme);

    this.quill = quill;
    this.options = options;
    this.modules = {};
  }

  _createClass(Theme, [{
    key: 'init',
    value: function init() {
      var _this = this;

      Object.keys(this.options.modules).forEach(function (name) {
        if (_this.modules[name] == null) {
          _this.addModule(name);
        }
      });
    }
  }, {
    key: 'addModule',
    value: function addModule(name) {
      var moduleClass = this.quill.constructor.import('modules/' + name);
      this.modules[name] = new moduleClass(this.quill, this.options.modules[name] || {});
      return this.modules[name];
    }
  }]);

  return Theme;
}();

Theme.DEFAULTS = {
  modules: {}
};
Theme.themes = {
  'default': Theme
};

exports.default = Theme;

/***/ }),
/* 35 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _text = __webpack_require__(7);

var _text2 = _interopRequireDefault(_text);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var GUARD_TEXT = '\uFEFF';

var Embed = function (_Parchment$Embed) {
  _inherits(Embed, _Parchment$Embed);

  function Embed(node) {
    _classCallCheck(this, Embed);

    var _this = _possibleConstructorReturn(this, (Embed.__proto__ || Object.getPrototypeOf(Embed)).call(this, node));

    _this.contentNode = document.createElement('span');
    _this.contentNode.setAttribute('contenteditable', false);
    [].slice.call(_this.domNode.childNodes).forEach(function (childNode) {
      _this.contentNode.appendChild(childNode);
    });
    _this.leftGuard = document.createTextNode(GUARD_TEXT);
    _this.rightGuard = document.createTextNode(GUARD_TEXT);
    _this.domNode.appendChild(_this.leftGuard);
    _this.domNode.appendChild(_this.contentNode);
    _this.domNode.appendChild(_this.rightGuard);
    return _this;
  }

  _createClass(Embed, [{
    key: 'index',
    value: function index(node, offset) {
      if (node === this.leftGuard) return 0;
      if (node === this.rightGuard) return 1;
      return _get(Embed.prototype.__proto__ || Object.getPrototypeOf(Embed.prototype), 'index', this).call(this, node, offset);
    }
  }, {
    key: 'restore',
    value: function restore(node) {
      var range = void 0,
          textNode = void 0;
      var text = node.data.split(GUARD_TEXT).join('');
      if (node === this.leftGuard) {
        if (this.prev instanceof _text2.default) {
          var prevLength = this.prev.length();
          this.prev.insertAt(prevLength, text);
          range = {
            startNode: this.prev.domNode,
            startOffset: prevLength + text.length
          };
        } else {
          textNode = document.createTextNode(text);
          this.parent.insertBefore(_parchment2.default.create(textNode), this);
          range = {
            startNode: textNode,
            startOffset: text.length
          };
        }
      } else if (node === this.rightGuard) {
        if (this.next instanceof _text2.default) {
          this.next.insertAt(0, text);
          range = {
            startNode: this.next.domNode,
            startOffset: text.length
          };
        } else {
          textNode = document.createTextNode(text);
          this.parent.insertBefore(_parchment2.default.create(textNode), this.next);
          range = {
            startNode: textNode,
            startOffset: text.length
          };
        }
      }
      node.data = GUARD_TEXT;
      return range;
    }
  }, {
    key: 'update',
    value: function update(mutations, context) {
      var _this2 = this;

      mutations.forEach(function (mutation) {
        if (mutation.type === 'characterData' && (mutation.target === _this2.leftGuard || mutation.target === _this2.rightGuard)) {
          var range = _this2.restore(mutation.target);
          if (range) context.range = range;
        }
      });
    }
  }]);

  return Embed;
}(_parchment2.default.Embed);

exports.default = Embed;

/***/ }),
/* 36 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.AlignStyle = exports.AlignClass = exports.AlignAttribute = undefined;

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var config = {
  scope: _parchment2.default.Scope.BLOCK,
  whitelist: ['right', 'center', 'justify']
};

var AlignAttribute = new _parchment2.default.Attributor.Attribute('align', 'align', config);
var AlignClass = new _parchment2.default.Attributor.Class('align', 'ql-align', config);
var AlignStyle = new _parchment2.default.Attributor.Style('align', 'text-align', config);

exports.AlignAttribute = AlignAttribute;
exports.AlignClass = AlignClass;
exports.AlignStyle = AlignStyle;

/***/ }),
/* 37 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.BackgroundStyle = exports.BackgroundClass = undefined;

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _color = __webpack_require__(26);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var BackgroundClass = new _parchment2.default.Attributor.Class('background', 'ql-bg', {
  scope: _parchment2.default.Scope.INLINE
});
var BackgroundStyle = new _color.ColorAttributor('background', 'background-color', {
  scope: _parchment2.default.Scope.INLINE
});

exports.BackgroundClass = BackgroundClass;
exports.BackgroundStyle = BackgroundStyle;

/***/ }),
/* 38 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.DirectionStyle = exports.DirectionClass = exports.DirectionAttribute = undefined;

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var config = {
  scope: _parchment2.default.Scope.BLOCK,
  whitelist: ['rtl']
};

var DirectionAttribute = new _parchment2.default.Attributor.Attribute('direction', 'dir', config);
var DirectionClass = new _parchment2.default.Attributor.Class('direction', 'ql-direction', config);
var DirectionStyle = new _parchment2.default.Attributor.Style('direction', 'direction', config);

exports.DirectionAttribute = DirectionAttribute;
exports.DirectionClass = DirectionClass;
exports.DirectionStyle = DirectionStyle;

/***/ }),
/* 39 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.FontClass = exports.FontStyle = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var config = {
  scope: _parchment2.default.Scope.INLINE,
  whitelist: ['serif', 'monospace']
};

var FontClass = new _parchment2.default.Attributor.Class('font', 'ql-font', config);

var FontStyleAttributor = function (_Parchment$Attributor) {
  _inherits(FontStyleAttributor, _Parchment$Attributor);

  function FontStyleAttributor() {
    _classCallCheck(this, FontStyleAttributor);

    return _possibleConstructorReturn(this, (FontStyleAttributor.__proto__ || Object.getPrototypeOf(FontStyleAttributor)).apply(this, arguments));
  }

  _createClass(FontStyleAttributor, [{
    key: 'value',
    value: function value(node) {
      return _get(FontStyleAttributor.prototype.__proto__ || Object.getPrototypeOf(FontStyleAttributor.prototype), 'value', this).call(this, node).replace(/["']/g, '');
    }
  }]);

  return FontStyleAttributor;
}(_parchment2.default.Attributor.Style);

var FontStyle = new FontStyleAttributor('font', 'font-family', config);

exports.FontStyle = FontStyle;
exports.FontClass = FontClass;

/***/ }),
/* 40 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.SizeStyle = exports.SizeClass = undefined;

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var SizeClass = new _parchment2.default.Attributor.Class('size', 'ql-size', {
  scope: _parchment2.default.Scope.INLINE,
  whitelist: ['small', 'large', 'huge']
});
var SizeStyle = new _parchment2.default.Attributor.Style('size', 'font-size', {
  scope: _parchment2.default.Scope.INLINE,
  whitelist: ['10px', '18px', '32px']
});

exports.SizeClass = SizeClass;
exports.SizeStyle = SizeStyle;

/***/ }),
/* 41 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = {
  'align': {
    '': __webpack_require__(76),
    'center': __webpack_require__(77),
    'right': __webpack_require__(78),
    'justify': __webpack_require__(79)
  },
  'background': __webpack_require__(80),
  'blockquote': __webpack_require__(81),
  'bold': __webpack_require__(82),
  'clean': __webpack_require__(83),
  'code': __webpack_require__(58),
  'code-block': __webpack_require__(58),
  'color': __webpack_require__(84),
  'direction': {
    '': __webpack_require__(85),
    'rtl': __webpack_require__(86)
  },
  'float': {
    'center': __webpack_require__(87),
    'full': __webpack_require__(88),
    'left': __webpack_require__(89),
    'right': __webpack_require__(90)
  },
  'formula': __webpack_require__(91),
  'header': {
    '1': __webpack_require__(92),
    '2': __webpack_require__(93)
  },
  'italic': __webpack_require__(94),
  'image': __webpack_require__(95),
  'indent': {
    '+1': __webpack_require__(96),
    '-1': __webpack_require__(97)
  },
  'link': __webpack_require__(98),
  'list': {
    'ordered': __webpack_require__(99),
    'bullet': __webpack_require__(100),
    'check': __webpack_require__(101)
  },
  'script': {
    'sub': __webpack_require__(102),
    'super': __webpack_require__(103)
  },
  'strike': __webpack_require__(104),
  'underline': __webpack_require__(105),
  'video': __webpack_require__(106)
};

/***/ }),
/* 42 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.getLastChangeIndex = exports.default = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _quill = __webpack_require__(5);

var _quill2 = _interopRequireDefault(_quill);

var _module = __webpack_require__(9);

var _module2 = _interopRequireDefault(_module);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var History = function (_Module) {
  _inherits(History, _Module);

  function History(quill, options) {
    _classCallCheck(this, History);

    var _this = _possibleConstructorReturn(this, (History.__proto__ || Object.getPrototypeOf(History)).call(this, quill, options));

    _this.lastRecorded = 0;
    _this.ignoreChange = false;
    _this.clear();
    _this.quill.on(_quill2.default.events.EDITOR_CHANGE, function (eventName, delta, oldDelta, source) {
      if (eventName !== _quill2.default.events.TEXT_CHANGE || _this.ignoreChange) return;
      if (!_this.options.userOnly || source === _quill2.default.sources.USER) {
        _this.record(delta, oldDelta);
      } else {
        _this.transform(delta);
      }
    });
    _this.quill.keyboard.addBinding({ key: 'Z', shortKey: true }, _this.undo.bind(_this));
    _this.quill.keyboard.addBinding({ key: 'Z', shortKey: true, shiftKey: true }, _this.redo.bind(_this));
    if (/Win/i.test(navigator.platform)) {
      _this.quill.keyboard.addBinding({ key: 'Y', shortKey: true }, _this.redo.bind(_this));
    }
    return _this;
  }

  _createClass(History, [{
    key: 'change',
    value: function change(source, dest) {
      if (this.stack[source].length === 0) return;
      var delta = this.stack[source].pop();
      this.stack[dest].push(delta);
      this.lastRecorded = 0;
      this.ignoreChange = true;
      this.quill.updateContents(delta[source], _quill2.default.sources.USER);
      this.ignoreChange = false;
      var index = getLastChangeIndex(delta[source]);
      this.quill.setSelection(index);
    }
  }, {
    key: 'clear',
    value: function clear() {
      this.stack = { undo: [], redo: [] };
    }
  }, {
    key: 'cutoff',
    value: function cutoff() {
      this.lastRecorded = 0;
    }
  }, {
    key: 'record',
    value: function record(changeDelta, oldDelta) {
      if (changeDelta.ops.length === 0) return;
      this.stack.redo = [];
      var undoDelta = this.quill.getContents().diff(oldDelta);
      var timestamp = Date.now();
      if (this.lastRecorded + this.options.delay > timestamp && this.stack.undo.length > 0) {
        var delta = this.stack.undo.pop();
        undoDelta = undoDelta.compose(delta.undo);
        changeDelta = delta.redo.compose(changeDelta);
      } else {
        this.lastRecorded = timestamp;
      }
      this.stack.undo.push({
        redo: changeDelta,
        undo: undoDelta
      });
      if (this.stack.undo.length > this.options.maxStack) {
        this.stack.undo.shift();
      }
    }
  }, {
    key: 'redo',
    value: function redo() {
      this.change('redo', 'undo');
    }
  }, {
    key: 'transform',
    value: function transform(delta) {
      this.stack.undo.forEach(function (change) {
        change.undo = delta.transform(change.undo, true);
        change.redo = delta.transform(change.redo, true);
      });
      this.stack.redo.forEach(function (change) {
        change.undo = delta.transform(change.undo, true);
        change.redo = delta.transform(change.redo, true);
      });
    }
  }, {
    key: 'undo',
    value: function undo() {
      this.change('undo', 'redo');
    }
  }]);

  return History;
}(_module2.default);

History.DEFAULTS = {
  delay: 1000,
  maxStack: 100,
  userOnly: false
};

function endsWithNewlineChange(delta) {
  var lastOp = delta.ops[delta.ops.length - 1];
  if (lastOp == null) return false;
  if (lastOp.insert != null) {
    return typeof lastOp.insert === 'string' && lastOp.insert.endsWith('\n');
  }
  if (lastOp.attributes != null) {
    return Object.keys(lastOp.attributes).some(function (attr) {
      return _parchment2.default.query(attr, _parchment2.default.Scope.BLOCK) != null;
    });
  }
  return false;
}

function getLastChangeIndex(delta) {
  var deleteLength = delta.reduce(function (length, op) {
    length += op.delete || 0;
    return length;
  }, 0);
  var changeIndex = delta.length() - deleteLength;
  if (endsWithNewlineChange(delta)) {
    changeIndex -= 1;
  }
  return changeIndex;
}

exports.default = History;
exports.getLastChangeIndex = getLastChangeIndex;

/***/ }),
/* 43 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = exports.BaseTooltip = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _extend = __webpack_require__(3);

var _extend2 = _interopRequireDefault(_extend);

var _quillDelta = __webpack_require__(2);

var _quillDelta2 = _interopRequireDefault(_quillDelta);

var _emitter = __webpack_require__(8);

var _emitter2 = _interopRequireDefault(_emitter);

var _keyboard = __webpack_require__(23);

var _keyboard2 = _interopRequireDefault(_keyboard);

var _theme = __webpack_require__(34);

var _theme2 = _interopRequireDefault(_theme);

var _colorPicker = __webpack_require__(59);

var _colorPicker2 = _interopRequireDefault(_colorPicker);

var _iconPicker = __webpack_require__(60);

var _iconPicker2 = _interopRequireDefault(_iconPicker);

var _picker = __webpack_require__(28);

var _picker2 = _interopRequireDefault(_picker);

var _tooltip = __webpack_require__(61);

var _tooltip2 = _interopRequireDefault(_tooltip);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var ALIGNS = [false, 'center', 'right', 'justify'];

var COLORS = ["#000000", "#e60000", "#ff9900", "#ffff00", "#008a00", "#0066cc", "#9933ff", "#ffffff", "#facccc", "#ffebcc", "#ffffcc", "#cce8cc", "#cce0f5", "#ebd6ff", "#bbbbbb", "#f06666", "#ffc266", "#ffff66", "#66b966", "#66a3e0", "#c285ff", "#888888", "#a10000", "#b26b00", "#b2b200", "#006100", "#0047b2", "#6b24b2", "#444444", "#5c0000", "#663d00", "#666600", "#003700", "#002966", "#3d1466"];

var FONTS = [false, 'serif', 'monospace'];

var HEADERS = ['1', '2', '3', false];

var SIZES = ['small', false, 'large', 'huge'];

var BaseTheme = function (_Theme) {
  _inherits(BaseTheme, _Theme);

  function BaseTheme(quill, options) {
    _classCallCheck(this, BaseTheme);

    var _this = _possibleConstructorReturn(this, (BaseTheme.__proto__ || Object.getPrototypeOf(BaseTheme)).call(this, quill, options));

    var listener = function listener(e) {
      if (!document.body.contains(quill.root)) {
        return document.body.removeEventListener('click', listener);
      }
      if (_this.tooltip != null && !_this.tooltip.root.contains(e.target) && document.activeElement !== _this.tooltip.textbox && !_this.quill.hasFocus()) {
        _this.tooltip.hide();
      }
      if (_this.pickers != null) {
        _this.pickers.forEach(function (picker) {
          if (!picker.container.contains(e.target)) {
            picker.close();
          }
        });
      }
    };
    quill.emitter.listenDOM('click', document.body, listener);
    return _this;
  }

  _createClass(BaseTheme, [{
    key: 'addModule',
    value: function addModule(name) {
      var module = _get(BaseTheme.prototype.__proto__ || Object.getPrototypeOf(BaseTheme.prototype), 'addModule', this).call(this, name);
      if (name === 'toolbar') {
        this.extendToolbar(module);
      }
      return module;
    }
  }, {
    key: 'buildButtons',
    value: function buildButtons(buttons, icons) {
      buttons.forEach(function (button) {
        var className = button.getAttribute('class') || '';
        className.split(/\s+/).forEach(function (name) {
          if (!name.startsWith('ql-')) return;
          name = name.slice('ql-'.length);
          if (icons[name] == null) return;
          if (name === 'direction') {
            button.innerHTML = icons[name][''] + icons[name]['rtl'];
          } else if (typeof icons[name] === 'string') {
            button.innerHTML = icons[name];
          } else {
            var value = button.value || '';
            if (value != null && icons[name][value]) {
              button.innerHTML = icons[name][value];
            }
          }
        });
      });
    }
  }, {
    key: 'buildPickers',
    value: function buildPickers(selects, icons) {
      var _this2 = this;

      this.pickers = selects.map(function (select) {
        if (select.classList.contains('ql-align')) {
          if (select.querySelector('option') == null) {
            fillSelect(select, ALIGNS);
          }
          return new _iconPicker2.default(select, icons.align);
        } else if (select.classList.contains('ql-background') || select.classList.contains('ql-color')) {
          var format = select.classList.contains('ql-background') ? 'background' : 'color';
          if (select.querySelector('option') == null) {
            fillSelect(select, COLORS, format === 'background' ? '#ffffff' : '#000000');
          }
          return new _colorPicker2.default(select, icons[format]);
        } else {
          if (select.querySelector('option') == null) {
            if (select.classList.contains('ql-font')) {
              fillSelect(select, FONTS);
            } else if (select.classList.contains('ql-header')) {
              fillSelect(select, HEADERS);
            } else if (select.classList.contains('ql-size')) {
              fillSelect(select, SIZES);
            }
          }
          return new _picker2.default(select);
        }
      });
      var update = function update() {
        _this2.pickers.forEach(function (picker) {
          picker.update();
        });
      };
      this.quill.on(_emitter2.default.events.EDITOR_CHANGE, update);
    }
  }]);

  return BaseTheme;
}(_theme2.default);

BaseTheme.DEFAULTS = (0, _extend2.default)(true, {}, _theme2.default.DEFAULTS, {
  modules: {
    toolbar: {
      handlers: {
        formula: function formula() {
          this.quill.theme.tooltip.edit('formula');
        },
        image: function image() {
          var _this3 = this;

          var fileInput = this.container.querySelector('input.ql-image[type=file]');
          if (fileInput == null) {
            fileInput = document.createElement('input');
            fileInput.setAttribute('type', 'file');
            fileInput.setAttribute('accept', 'image/png, image/gif, image/jpeg, image/bmp, image/x-icon');
            fileInput.classList.add('ql-image');
            fileInput.addEventListener('change', function () {
              if (fileInput.files != null && fileInput.files[0] != null) {
                var reader = new FileReader();
                reader.onload = function (e) {
                  var range = _this3.quill.getSelection(true);
                  _this3.quill.updateContents(new _quillDelta2.default().retain(range.index).delete(range.length).insert({ image: e.target.result }), _emitter2.default.sources.USER);
                  _this3.quill.setSelection(range.index + 1, _emitter2.default.sources.SILENT);
                  fileInput.value = "";
                };
                reader.readAsDataURL(fileInput.files[0]);
              }
            });
            this.container.appendChild(fileInput);
          }
          fileInput.click();
        },
        video: function video() {
          this.quill.theme.tooltip.edit('video');
        }
      }
    }
  }
});

var BaseTooltip = function (_Tooltip) {
  _inherits(BaseTooltip, _Tooltip);

  function BaseTooltip(quill, boundsContainer) {
    _classCallCheck(this, BaseTooltip);

    var _this4 = _possibleConstructorReturn(this, (BaseTooltip.__proto__ || Object.getPrototypeOf(BaseTooltip)).call(this, quill, boundsContainer));

    _this4.textbox = _this4.root.querySelector('input[type="text"]');
    _this4.listen();
    return _this4;
  }

  _createClass(BaseTooltip, [{
    key: 'listen',
    value: function listen() {
      var _this5 = this;

      this.textbox.addEventListener('keydown', function (event) {
        if (_keyboard2.default.match(event, 'enter')) {
          _this5.save();
          event.preventDefault();
        } else if (_keyboard2.default.match(event, 'escape')) {
          _this5.cancel();
          event.preventDefault();
        }
      });
    }
  }, {
    key: 'cancel',
    value: function cancel() {
      this.hide();
    }
  }, {
    key: 'edit',
    value: function edit() {
      var mode = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'link';
      var preview = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;

      this.root.classList.remove('ql-hidden');
      this.root.classList.add('ql-editing');
      if (preview != null) {
        this.textbox.value = preview;
      } else if (mode !== this.root.getAttribute('data-mode')) {
        this.textbox.value = '';
      }
      this.position(this.quill.getBounds(this.quill.selection.savedRange));
      this.textbox.select();
      this.textbox.setAttribute('placeholder', this.textbox.getAttribute('data-' + mode) || '');
      this.root.setAttribute('data-mode', mode);
    }
  }, {
    key: 'restoreFocus',
    value: function restoreFocus() {
      var scrollTop = this.quill.scrollingContainer.scrollTop;
      this.quill.focus();
      this.quill.scrollingContainer.scrollTop = scrollTop;
    }
  }, {
    key: 'save',
    value: function save() {
      var value = this.textbox.value;
      switch (this.root.getAttribute('data-mode')) {
        case 'link':
          {
            var scrollTop = this.quill.root.scrollTop;
            if (this.linkRange) {
              this.quill.formatText(this.linkRange, 'link', value, _emitter2.default.sources.USER);
              delete this.linkRange;
            } else {
              this.restoreFocus();
              this.quill.format('link', value, _emitter2.default.sources.USER);
            }
            this.quill.root.scrollTop = scrollTop;
            break;
          }
        case 'video':
          {
            value = extractVideoUrl(value);
          } // eslint-disable-next-line no-fallthrough
        case 'formula':
          {
            if (!value) break;
            var range = this.quill.getSelection(true);
            if (range != null) {
              var index = range.index + range.length;
              this.quill.insertEmbed(index, this.root.getAttribute('data-mode'), value, _emitter2.default.sources.USER);
              if (this.root.getAttribute('data-mode') === 'formula') {
                this.quill.insertText(index + 1, ' ', _emitter2.default.sources.USER);
              }
              this.quill.setSelection(index + 2, _emitter2.default.sources.USER);
            }
            break;
          }
        default:
      }
      this.textbox.value = '';
      this.hide();
    }
  }]);

  return BaseTooltip;
}(_tooltip2.default);

function extractVideoUrl(url) {
  var match = url.match(/^(?:(https?):\/\/)?(?:(?:www|m)\.)?youtube\.com\/watch.*v=([a-zA-Z0-9_-]+)/) || url.match(/^(?:(https?):\/\/)?(?:(?:www|m)\.)?youtu\.be\/([a-zA-Z0-9_-]+)/);
  if (match) {
    return (match[1] || 'https') + '://www.youtube.com/embed/' + match[2] + '?showinfo=0';
  }
  if (match = url.match(/^(?:(https?):\/\/)?(?:www\.)?vimeo\.com\/(\d+)/)) {
    // eslint-disable-line no-cond-assign
    return (match[1] || 'https') + '://player.vimeo.com/video/' + match[2] + '/';
  }
  return url;
}

function fillSelect(select, values) {
  var defaultValue = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;

  values.forEach(function (value) {
    var option = document.createElement('option');
    if (value === defaultValue) {
      option.setAttribute('selected', 'selected');
    } else {
      option.setAttribute('value', value);
    }
    select.appendChild(option);
  });
}

exports.BaseTooltip = BaseTooltip;
exports.default = BaseTheme;

/***/ }),
/* 44 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var LinkedList = /** @class */ (function () {
    function LinkedList() {
        this.head = this.tail = null;
        this.length = 0;
    }
    LinkedList.prototype.append = function () {
        var nodes = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            nodes[_i] = arguments[_i];
        }
        this.insertBefore(nodes[0], null);
        if (nodes.length > 1) {
            this.append.apply(this, nodes.slice(1));
        }
    };
    LinkedList.prototype.contains = function (node) {
        var cur, next = this.iterator();
        while ((cur = next())) {
            if (cur === node)
                return true;
        }
        return false;
    };
    LinkedList.prototype.insertBefore = function (node, refNode) {
        if (!node)
            return;
        node.next = refNode;
        if (refNode != null) {
            node.prev = refNode.prev;
            if (refNode.prev != null) {
                refNode.prev.next = node;
            }
            refNode.prev = node;
            if (refNode === this.head) {
                this.head = node;
            }
        }
        else if (this.tail != null) {
            this.tail.next = node;
            node.prev = this.tail;
            this.tail = node;
        }
        else {
            node.prev = null;
            this.head = this.tail = node;
        }
        this.length += 1;
    };
    LinkedList.prototype.offset = function (target) {
        var index = 0, cur = this.head;
        while (cur != null) {
            if (cur === target)
                return index;
            index += cur.length();
            cur = cur.next;
        }
        return -1;
    };
    LinkedList.prototype.remove = function (node) {
        if (!this.contains(node))
            return;
        if (node.prev != null)
            node.prev.next = node.next;
        if (node.next != null)
            node.next.prev = node.prev;
        if (node === this.head)
            this.head = node.next;
        if (node === this.tail)
            this.tail = node.prev;
        this.length -= 1;
    };
    LinkedList.prototype.iterator = function (curNode) {
        if (curNode === void 0) { curNode = this.head; }
        // TODO use yield when we can
        return function () {
            var ret = curNode;
            if (curNode != null)
                curNode = curNode.next;
            return ret;
        };
    };
    LinkedList.prototype.find = function (index, inclusive) {
        if (inclusive === void 0) { inclusive = false; }
        var cur, next = this.iterator();
        while ((cur = next())) {
            var length = cur.length();
            if (index < length ||
                (inclusive && index === length && (cur.next == null || cur.next.length() !== 0))) {
                return [cur, index];
            }
            index -= length;
        }
        return [null, 0];
    };
    LinkedList.prototype.forEach = function (callback) {
        var cur, next = this.iterator();
        while ((cur = next())) {
            callback(cur);
        }
    };
    LinkedList.prototype.forEachAt = function (index, length, callback) {
        if (length <= 0)
            return;
        var _a = this.find(index), startNode = _a[0], offset = _a[1];
        var cur, curIndex = index - offset, next = this.iterator(startNode);
        while ((cur = next()) && curIndex < index + length) {
            var curLength = cur.length();
            if (index > curIndex) {
                callback(cur, index - curIndex, Math.min(length, curIndex + curLength - index));
            }
            else {
                callback(cur, 0, Math.min(curLength, index + length - curIndex));
            }
            curIndex += curLength;
        }
    };
    LinkedList.prototype.map = function (callback) {
        return this.reduce(function (memo, cur) {
            memo.push(callback(cur));
            return memo;
        }, []);
    };
    LinkedList.prototype.reduce = function (callback, memo) {
        var cur, next = this.iterator();
        while ((cur = next())) {
            memo = callback(memo, cur);
        }
        return memo;
    };
    return LinkedList;
}());
exports.default = LinkedList;


/***/ }),
/* 45 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var container_1 = __webpack_require__(17);
var Registry = __webpack_require__(1);
var OBSERVER_CONFIG = {
    attributes: true,
    characterData: true,
    characterDataOldValue: true,
    childList: true,
    subtree: true,
};
var MAX_OPTIMIZE_ITERATIONS = 100;
var ScrollBlot = /** @class */ (function (_super) {
    __extends(ScrollBlot, _super);
    function ScrollBlot(node) {
        var _this = _super.call(this, node) || this;
        _this.scroll = _this;
        _this.observer = new MutationObserver(function (mutations) {
            _this.update(mutations);
        });
        _this.observer.observe(_this.domNode, OBSERVER_CONFIG);
        _this.attach();
        return _this;
    }
    ScrollBlot.prototype.detach = function () {
        _super.prototype.detach.call(this);
        this.observer.disconnect();
    };
    ScrollBlot.prototype.deleteAt = function (index, length) {
        this.update();
        if (index === 0 && length === this.length()) {
            this.children.forEach(function (child) {
                child.remove();
            });
        }
        else {
            _super.prototype.deleteAt.call(this, index, length);
        }
    };
    ScrollBlot.prototype.formatAt = function (index, length, name, value) {
        this.update();
        _super.prototype.formatAt.call(this, index, length, name, value);
    };
    ScrollBlot.prototype.insertAt = function (index, value, def) {
        this.update();
        _super.prototype.insertAt.call(this, index, value, def);
    };
    ScrollBlot.prototype.optimize = function (mutations, context) {
        var _this = this;
        if (mutations === void 0) { mutations = []; }
        if (context === void 0) { context = {}; }
        _super.prototype.optimize.call(this, context);
        // We must modify mutations directly, cannot make copy and then modify
        var records = [].slice.call(this.observer.takeRecords());
        // Array.push currently seems to be implemented by a non-tail recursive function
        // so we cannot just mutations.push.apply(mutations, this.observer.takeRecords());
        while (records.length > 0)
            mutations.push(records.pop());
        // TODO use WeakMap
        var mark = function (blot, markParent) {
            if (markParent === void 0) { markParent = true; }
            if (blot == null || blot === _this)
                return;
            if (blot.domNode.parentNode == null)
                return;
            // @ts-ignore
            if (blot.domNode[Registry.DATA_KEY].mutations == null) {
                // @ts-ignore
                blot.domNode[Registry.DATA_KEY].mutations = [];
            }
            if (markParent)
                mark(blot.parent);
        };
        var optimize = function (blot) {
            // Post-order traversal
            if (
            // @ts-ignore
            blot.domNode[Registry.DATA_KEY] == null ||
                // @ts-ignore
                blot.domNode[Registry.DATA_KEY].mutations == null) {
                return;
            }
            if (blot instanceof container_1.default) {
                blot.children.forEach(optimize);
            }
            blot.optimize(context);
        };
        var remaining = mutations;
        for (var i = 0; remaining.length > 0; i += 1) {
            if (i >= MAX_OPTIMIZE_ITERATIONS) {
                throw new Error('[Parchment] Maximum optimize iterations reached');
            }
            remaining.forEach(function (mutation) {
                var blot = Registry.find(mutation.target, true);
                if (blot == null)
                    return;
                if (blot.domNode === mutation.target) {
                    if (mutation.type === 'childList') {
                        mark(Registry.find(mutation.previousSibling, false));
                        [].forEach.call(mutation.addedNodes, function (node) {
                            var child = Registry.find(node, false);
                            mark(child, false);
                            if (child instanceof container_1.default) {
                                child.children.forEach(function (grandChild) {
                                    mark(grandChild, false);
                                });
                            }
                        });
                    }
                    else if (mutation.type === 'attributes') {
                        mark(blot.prev);
                    }
                }
                mark(blot);
            });
            this.children.forEach(optimize);
            remaining = [].slice.call(this.observer.takeRecords());
            records = remaining.slice();
            while (records.length > 0)
                mutations.push(records.pop());
        }
    };
    ScrollBlot.prototype.update = function (mutations, context) {
        var _this = this;
        if (context === void 0) { context = {}; }
        mutations = mutations || this.observer.takeRecords();
        // TODO use WeakMap
        mutations
            .map(function (mutation) {
            var blot = Registry.find(mutation.target, true);
            if (blot == null)
                return null;
            // @ts-ignore
            if (blot.domNode[Registry.DATA_KEY].mutations == null) {
                // @ts-ignore
                blot.domNode[Registry.DATA_KEY].mutations = [mutation];
                return blot;
            }
            else {
                // @ts-ignore
                blot.domNode[Registry.DATA_KEY].mutations.push(mutation);
                return null;
            }
        })
            .forEach(function (blot) {
            if (blot == null ||
                blot === _this ||
                //@ts-ignore
                blot.domNode[Registry.DATA_KEY] == null)
                return;
            // @ts-ignore
            blot.update(blot.domNode[Registry.DATA_KEY].mutations || [], context);
        });
        // @ts-ignore
        if (this.domNode[Registry.DATA_KEY].mutations != null) {
            // @ts-ignore
            _super.prototype.update.call(this, this.domNode[Registry.DATA_KEY].mutations, context);
        }
        this.optimize(mutations, context);
    };
    ScrollBlot.blotName = 'scroll';
    ScrollBlot.defaultChild = 'block';
    ScrollBlot.scope = Registry.Scope.BLOCK_BLOT;
    ScrollBlot.tagName = 'DIV';
    return ScrollBlot;
}(container_1.default));
exports.default = ScrollBlot;


/***/ }),
/* 46 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var format_1 = __webpack_require__(18);
var Registry = __webpack_require__(1);
// Shallow object comparison
function isEqual(obj1, obj2) {
    if (Object.keys(obj1).length !== Object.keys(obj2).length)
        return false;
    // @ts-ignore
    for (var prop in obj1) {
        // @ts-ignore
        if (obj1[prop] !== obj2[prop])
            return false;
    }
    return true;
}
var InlineBlot = /** @class */ (function (_super) {
    __extends(InlineBlot, _super);
    function InlineBlot() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    InlineBlot.formats = function (domNode) {
        if (domNode.tagName === InlineBlot.tagName)
            return undefined;
        return _super.formats.call(this, domNode);
    };
    InlineBlot.prototype.format = function (name, value) {
        var _this = this;
        if (name === this.statics.blotName && !value) {
            this.children.forEach(function (child) {
                if (!(child instanceof format_1.default)) {
                    child = child.wrap(InlineBlot.blotName, true);
                }
                _this.attributes.copy(child);
            });
            this.unwrap();
        }
        else {
            _super.prototype.format.call(this, name, value);
        }
    };
    InlineBlot.prototype.formatAt = function (index, length, name, value) {
        if (this.formats()[name] != null || Registry.query(name, Registry.Scope.ATTRIBUTE)) {
            var blot = this.isolate(index, length);
            blot.format(name, value);
        }
        else {
            _super.prototype.formatAt.call(this, index, length, name, value);
        }
    };
    InlineBlot.prototype.optimize = function (context) {
        _super.prototype.optimize.call(this, context);
        var formats = this.formats();
        if (Object.keys(formats).length === 0) {
            return this.unwrap(); // unformatted span
        }
        var next = this.next;
        if (next instanceof InlineBlot && next.prev === this && isEqual(formats, next.formats())) {
            next.moveChildren(this);
            next.remove();
        }
    };
    InlineBlot.blotName = 'inline';
    InlineBlot.scope = Registry.Scope.INLINE_BLOT;
    InlineBlot.tagName = 'SPAN';
    return InlineBlot;
}(format_1.default));
exports.default = InlineBlot;


/***/ }),
/* 47 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var format_1 = __webpack_require__(18);
var Registry = __webpack_require__(1);
var BlockBlot = /** @class */ (function (_super) {
    __extends(BlockBlot, _super);
    function BlockBlot() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    BlockBlot.formats = function (domNode) {
        var tagName = Registry.query(BlockBlot.blotName).tagName;
        if (domNode.tagName === tagName)
            return undefined;
        return _super.formats.call(this, domNode);
    };
    BlockBlot.prototype.format = function (name, value) {
        if (Registry.query(name, Registry.Scope.BLOCK) == null) {
            return;
        }
        else if (name === this.statics.blotName && !value) {
            this.replaceWith(BlockBlot.blotName);
        }
        else {
            _super.prototype.format.call(this, name, value);
        }
    };
    BlockBlot.prototype.formatAt = function (index, length, name, value) {
        if (Registry.query(name, Registry.Scope.BLOCK) != null) {
            this.format(name, value);
        }
        else {
            _super.prototype.formatAt.call(this, index, length, name, value);
        }
    };
    BlockBlot.prototype.insertAt = function (index, value, def) {
        if (def == null || Registry.query(value, Registry.Scope.INLINE) != null) {
            // Insert text or inline
            _super.prototype.insertAt.call(this, index, value, def);
        }
        else {
            var after = this.split(index);
            var blot = Registry.create(value, def);
            after.parent.insertBefore(blot, after);
        }
    };
    BlockBlot.prototype.update = function (mutations, context) {
        if (navigator.userAgent.match(/Trident/)) {
            this.build();
        }
        else {
            _super.prototype.update.call(this, mutations, context);
        }
    };
    BlockBlot.blotName = 'block';
    BlockBlot.scope = Registry.Scope.BLOCK_BLOT;
    BlockBlot.tagName = 'P';
    return BlockBlot;
}(format_1.default));
exports.default = BlockBlot;


/***/ }),
/* 48 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var leaf_1 = __webpack_require__(19);
var EmbedBlot = /** @class */ (function (_super) {
    __extends(EmbedBlot, _super);
    function EmbedBlot() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EmbedBlot.formats = function (domNode) {
        return undefined;
    };
    EmbedBlot.prototype.format = function (name, value) {
        // super.formatAt wraps, which is what we want in general,
        // but this allows subclasses to overwrite for formats
        // that just apply to particular embeds
        _super.prototype.formatAt.call(this, 0, this.length(), name, value);
    };
    EmbedBlot.prototype.formatAt = function (index, length, name, value) {
        if (index === 0 && length === this.length()) {
            this.format(name, value);
        }
        else {
            _super.prototype.formatAt.call(this, index, length, name, value);
        }
    };
    EmbedBlot.prototype.formats = function () {
        return this.statics.formats(this.domNode);
    };
    return EmbedBlot;
}(leaf_1.default));
exports.default = EmbedBlot;


/***/ }),
/* 49 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var leaf_1 = __webpack_require__(19);
var Registry = __webpack_require__(1);
var TextBlot = /** @class */ (function (_super) {
    __extends(TextBlot, _super);
    function TextBlot(node) {
        var _this = _super.call(this, node) || this;
        _this.text = _this.statics.value(_this.domNode);
        return _this;
    }
    TextBlot.create = function (value) {
        return document.createTextNode(value);
    };
    TextBlot.value = function (domNode) {
        var text = domNode.data;
        // @ts-ignore
        if (text['normalize'])
            text = text['normalize']();
        return text;
    };
    TextBlot.prototype.deleteAt = function (index, length) {
        this.domNode.data = this.text = this.text.slice(0, index) + this.text.slice(index + length);
    };
    TextBlot.prototype.index = function (node, offset) {
        if (this.domNode === node) {
            return offset;
        }
        return -1;
    };
    TextBlot.prototype.insertAt = function (index, value, def) {
        if (def == null) {
            this.text = this.text.slice(0, index) + value + this.text.slice(index);
            this.domNode.data = this.text;
        }
        else {
            _super.prototype.insertAt.call(this, index, value, def);
        }
    };
    TextBlot.prototype.length = function () {
        return this.text.length;
    };
    TextBlot.prototype.optimize = function (context) {
        _super.prototype.optimize.call(this, context);
        this.text = this.statics.value(this.domNode);
        if (this.text.length === 0) {
            this.remove();
        }
        else if (this.next instanceof TextBlot && this.next.prev === this) {
            this.insertAt(this.length(), this.next.value());
            this.next.remove();
        }
    };
    TextBlot.prototype.position = function (index, inclusive) {
        if (inclusive === void 0) { inclusive = false; }
        return [this.domNode, index];
    };
    TextBlot.prototype.split = function (index, force) {
        if (force === void 0) { force = false; }
        if (!force) {
            if (index === 0)
                return this;
            if (index === this.length())
                return this.next;
        }
        var after = Registry.create(this.domNode.splitText(index));
        this.parent.insertBefore(after, this.next);
        this.text = this.statics.value(this.domNode);
        return after;
    };
    TextBlot.prototype.update = function (mutations, context) {
        var _this = this;
        if (mutations.some(function (mutation) {
            return mutation.type === 'characterData' && mutation.target === _this.domNode;
        })) {
            this.text = this.statics.value(this.domNode);
        }
    };
    TextBlot.prototype.value = function () {
        return this.text;
    };
    TextBlot.blotName = 'text';
    TextBlot.scope = Registry.Scope.INLINE_BLOT;
    return TextBlot;
}(leaf_1.default));
exports.default = TextBlot;


/***/ }),
/* 50 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var elem = document.createElement('div');
elem.classList.toggle('test-class', false);
if (elem.classList.contains('test-class')) {
  var _toggle = DOMTokenList.prototype.toggle;
  DOMTokenList.prototype.toggle = function (token, force) {
    if (arguments.length > 1 && !this.contains(token) === !force) {
      return force;
    } else {
      return _toggle.call(this, token);
    }
  };
}

if (!String.prototype.startsWith) {
  String.prototype.startsWith = function (searchString, position) {
    position = position || 0;
    return this.substr(position, searchString.length) === searchString;
  };
}

if (!String.prototype.endsWith) {
  String.prototype.endsWith = function (searchString, position) {
    var subjectString = this.toString();
    if (typeof position !== 'number' || !isFinite(position) || Math.floor(position) !== position || position > subjectString.length) {
      position = subjectString.length;
    }
    position -= searchString.length;
    var lastIndex = subjectString.indexOf(searchString, position);
    return lastIndex !== -1 && lastIndex === position;
  };
}

if (!Array.prototype.find) {
  Object.defineProperty(Array.prototype, "find", {
    value: function value(predicate) {
      if (this === null) {
        throw new TypeError('Array.prototype.find called on null or undefined');
      }
      if (typeof predicate !== 'function') {
        throw new TypeError('predicate must be a function');
      }
      var list = Object(this);
      var length = list.length >>> 0;
      var thisArg = arguments[1];
      var value;

      for (var i = 0; i < length; i++) {
        value = list[i];
        if (predicate.call(thisArg, value, i, list)) {
          return value;
        }
      }
      return undefined;
    }
  });
}

document.addEventListener("DOMContentLoaded", function () {
  // Disable resizing in Firefox
  document.execCommand("enableObjectResizing", false, false);
  // Disable automatic linkifying in IE11
  document.execCommand("autoUrlDetect", false, false);
});

/***/ }),
/* 51 */
/***/ (function(module, exports) {

/**
 * This library modifies the diff-patch-match library by Neil Fraser
 * by removing the patch and match functionality and certain advanced
 * options in the diff function. The original license is as follows:
 *
 * ===
 *
 * Diff Match and Patch
 *
 * Copyright 2006 Google Inc.
 * http://code.google.com/p/google-diff-match-patch/
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


/**
 * The data structure representing a diff is an array of tuples:
 * [[DIFF_DELETE, 'Hello'], [DIFF_INSERT, 'Goodbye'], [DIFF_EQUAL, ' world.']]
 * which means: delete 'Hello', add 'Goodbye' and keep ' world.'
 */
var DIFF_DELETE = -1;
var DIFF_INSERT = 1;
var DIFF_EQUAL = 0;


/**
 * Find the differences between two texts.  Simplifies the problem by stripping
 * any common prefix or suffix off the texts before diffing.
 * @param {string} text1 Old string to be diffed.
 * @param {string} text2 New string to be diffed.
 * @param {Int} cursor_pos Expected edit position in text1 (optional)
 * @return {Array} Array of diff tuples.
 */
function diff_main(text1, text2, cursor_pos) {
  // Check for equality (speedup).
  if (text1 == text2) {
    if (text1) {
      return [[DIFF_EQUAL, text1]];
    }
    return [];
  }

  // Check cursor_pos within bounds
  if (cursor_pos < 0 || text1.length < cursor_pos) {
    cursor_pos = null;
  }

  // Trim off common prefix (speedup).
  var commonlength = diff_commonPrefix(text1, text2);
  var commonprefix = text1.substring(0, commonlength);
  text1 = text1.substring(commonlength);
  text2 = text2.substring(commonlength);

  // Trim off common suffix (speedup).
  commonlength = diff_commonSuffix(text1, text2);
  var commonsuffix = text1.substring(text1.length - commonlength);
  text1 = text1.substring(0, text1.length - commonlength);
  text2 = text2.substring(0, text2.length - commonlength);

  // Compute the diff on the middle block.
  var diffs = diff_compute_(text1, text2);

  // Restore the prefix and suffix.
  if (commonprefix) {
    diffs.unshift([DIFF_EQUAL, commonprefix]);
  }
  if (commonsuffix) {
    diffs.push([DIFF_EQUAL, commonsuffix]);
  }
  diff_cleanupMerge(diffs);
  if (cursor_pos != null) {
    diffs = fix_cursor(diffs, cursor_pos);
  }
  diffs = fix_emoji(diffs);
  return diffs;
};


/**
 * Find the differences between two texts.  Assumes that the texts do not
 * have any common prefix or suffix.
 * @param {string} text1 Old string to be diffed.
 * @param {string} text2 New string to be diffed.
 * @return {Array} Array of diff tuples.
 */
function diff_compute_(text1, text2) {
  var diffs;

  if (!text1) {
    // Just add some text (speedup).
    return [[DIFF_INSERT, text2]];
  }

  if (!text2) {
    // Just delete some text (speedup).
    return [[DIFF_DELETE, text1]];
  }

  var longtext = text1.length > text2.length ? text1 : text2;
  var shorttext = text1.length > text2.length ? text2 : text1;
  var i = longtext.indexOf(shorttext);
  if (i != -1) {
    // Shorter text is inside the longer text (speedup).
    diffs = [[DIFF_INSERT, longtext.substring(0, i)],
             [DIFF_EQUAL, shorttext],
             [DIFF_INSERT, longtext.substring(i + shorttext.length)]];
    // Swap insertions for deletions if diff is reversed.
    if (text1.length > text2.length) {
      diffs[0][0] = diffs[2][0] = DIFF_DELETE;
    }
    return diffs;
  }

  if (shorttext.length == 1) {
    // Single character string.
    // After the previous speedup, the character can't be an equality.
    return [[DIFF_DELETE, text1], [DIFF_INSERT, text2]];
  }

  // Check to see if the problem can be split in two.
  var hm = diff_halfMatch_(text1, text2);
  if (hm) {
    // A half-match was found, sort out the return data.
    var text1_a = hm[0];
    var text1_b = hm[1];
    var text2_a = hm[2];
    var text2_b = hm[3];
    var mid_common = hm[4];
    // Send both pairs off for separate processing.
    var diffs_a = diff_main(text1_a, text2_a);
    var diffs_b = diff_main(text1_b, text2_b);
    // Merge the results.
    return diffs_a.concat([[DIFF_EQUAL, mid_common]], diffs_b);
  }

  return diff_bisect_(text1, text2);
};


/**
 * Find the 'middle snake' of a diff, split the problem in two
 * and return the recursively constructed diff.
 * See Myers 1986 paper: An O(ND) Difference Algorithm and Its Variations.
 * @param {string} text1 Old string to be diffed.
 * @param {string} text2 New string to be diffed.
 * @return {Array} Array of diff tuples.
 * @private
 */
function diff_bisect_(text1, text2) {
  // Cache the text lengths to prevent multiple calls.
  var text1_length = text1.length;
  var text2_length = text2.length;
  var max_d = Math.ceil((text1_length + text2_length) / 2);
  var v_offset = max_d;
  var v_length = 2 * max_d;
  var v1 = new Array(v_length);
  var v2 = new Array(v_length);
  // Setting all elements to -1 is faster in Chrome & Firefox than mixing
  // integers and undefined.
  for (var x = 0; x < v_length; x++) {
    v1[x] = -1;
    v2[x] = -1;
  }
  v1[v_offset + 1] = 0;
  v2[v_offset + 1] = 0;
  var delta = text1_length - text2_length;
  // If the total number of characters is odd, then the front path will collide
  // with the reverse path.
  var front = (delta % 2 != 0);
  // Offsets for start and end of k loop.
  // Prevents mapping of space beyond the grid.
  var k1start = 0;
  var k1end = 0;
  var k2start = 0;
  var k2end = 0;
  for (var d = 0; d < max_d; d++) {
    // Walk the front path one step.
    for (var k1 = -d + k1start; k1 <= d - k1end; k1 += 2) {
      var k1_offset = v_offset + k1;
      var x1;
      if (k1 == -d || (k1 != d && v1[k1_offset - 1] < v1[k1_offset + 1])) {
        x1 = v1[k1_offset + 1];
      } else {
        x1 = v1[k1_offset - 1] + 1;
      }
      var y1 = x1 - k1;
      while (x1 < text1_length && y1 < text2_length &&
             text1.charAt(x1) == text2.charAt(y1)) {
        x1++;
        y1++;
      }
      v1[k1_offset] = x1;
      if (x1 > text1_length) {
        // Ran off the right of the graph.
        k1end += 2;
      } else if (y1 > text2_length) {
        // Ran off the bottom of the graph.
        k1start += 2;
      } else if (front) {
        var k2_offset = v_offset + delta - k1;
        if (k2_offset >= 0 && k2_offset < v_length && v2[k2_offset] != -1) {
          // Mirror x2 onto top-left coordinate system.
          var x2 = text1_length - v2[k2_offset];
          if (x1 >= x2) {
            // Overlap detected.
            return diff_bisectSplit_(text1, text2, x1, y1);
          }
        }
      }
    }

    // Walk the reverse path one step.
    for (var k2 = -d + k2start; k2 <= d - k2end; k2 += 2) {
      var k2_offset = v_offset + k2;
      var x2;
      if (k2 == -d || (k2 != d && v2[k2_offset - 1] < v2[k2_offset + 1])) {
        x2 = v2[k2_offset + 1];
      } else {
        x2 = v2[k2_offset - 1] + 1;
      }
      var y2 = x2 - k2;
      while (x2 < text1_length && y2 < text2_length &&
             text1.charAt(text1_length - x2 - 1) ==
             text2.charAt(text2_length - y2 - 1)) {
        x2++;
        y2++;
      }
      v2[k2_offset] = x2;
      if (x2 > text1_length) {
        // Ran off the left of the graph.
        k2end += 2;
      } else if (y2 > text2_length) {
        // Ran off the top of the graph.
        k2start += 2;
      } else if (!front) {
        var k1_offset = v_offset + delta - k2;
        if (k1_offset >= 0 && k1_offset < v_length && v1[k1_offset] != -1) {
          var x1 = v1[k1_offset];
          var y1 = v_offset + x1 - k1_offset;
          // Mirror x2 onto top-left coordinate system.
          x2 = text1_length - x2;
          if (x1 >= x2) {
            // Overlap detected.
            return diff_bisectSplit_(text1, text2, x1, y1);
          }
        }
      }
    }
  }
  // Diff took too long and hit the deadline or
  // number of diffs equals number of characters, no commonality at all.
  return [[DIFF_DELETE, text1], [DIFF_INSERT, text2]];
};


/**
 * Given the location of the 'middle snake', split the diff in two parts
 * and recurse.
 * @param {string} text1 Old string to be diffed.
 * @param {string} text2 New string to be diffed.
 * @param {number} x Index of split point in text1.
 * @param {number} y Index of split point in text2.
 * @return {Array} Array of diff tuples.
 */
function diff_bisectSplit_(text1, text2, x, y) {
  var text1a = text1.substring(0, x);
  var text2a = text2.substring(0, y);
  var text1b = text1.substring(x);
  var text2b = text2.substring(y);

  // Compute both diffs serially.
  var diffs = diff_main(text1a, text2a);
  var diffsb = diff_main(text1b, text2b);

  return diffs.concat(diffsb);
};


/**
 * Determine the common prefix of two strings.
 * @param {string} text1 First string.
 * @param {string} text2 Second string.
 * @return {number} The number of characters common to the start of each
 *     string.
 */
function diff_commonPrefix(text1, text2) {
  // Quick check for common null cases.
  if (!text1 || !text2 || text1.charAt(0) != text2.charAt(0)) {
    return 0;
  }
  // Binary search.
  // Performance analysis: http://neil.fraser.name/news/2007/10/09/
  var pointermin = 0;
  var pointermax = Math.min(text1.length, text2.length);
  var pointermid = pointermax;
  var pointerstart = 0;
  while (pointermin < pointermid) {
    if (text1.substring(pointerstart, pointermid) ==
        text2.substring(pointerstart, pointermid)) {
      pointermin = pointermid;
      pointerstart = pointermin;
    } else {
      pointermax = pointermid;
    }
    pointermid = Math.floor((pointermax - pointermin) / 2 + pointermin);
  }
  return pointermid;
};


/**
 * Determine the common suffix of two strings.
 * @param {string} text1 First string.
 * @param {string} text2 Second string.
 * @return {number} The number of characters common to the end of each string.
 */
function diff_commonSuffix(text1, text2) {
  // Quick check for common null cases.
  if (!text1 || !text2 ||
      text1.charAt(text1.length - 1) != text2.charAt(text2.length - 1)) {
    return 0;
  }
  // Binary search.
  // Performance analysis: http://neil.fraser.name/news/2007/10/09/
  var pointermin = 0;
  var pointermax = Math.min(text1.length, text2.length);
  var pointermid = pointermax;
  var pointerend = 0;
  while (pointermin < pointermid) {
    if (text1.substring(text1.length - pointermid, text1.length - pointerend) ==
        text2.substring(text2.length - pointermid, text2.length - pointerend)) {
      pointermin = pointermid;
      pointerend = pointermin;
    } else {
      pointermax = pointermid;
    }
    pointermid = Math.floor((pointermax - pointermin) / 2 + pointermin);
  }
  return pointermid;
};


/**
 * Do the two texts share a substring which is at least half the length of the
 * longer text?
 * This speedup can produce non-minimal diffs.
 * @param {string} text1 First string.
 * @param {string} text2 Second string.
 * @return {Array.<string>} Five element Array, containing the prefix of
 *     text1, the suffix of text1, the prefix of text2, the suffix of
 *     text2 and the common middle.  Or null if there was no match.
 */
function diff_halfMatch_(text1, text2) {
  var longtext = text1.length > text2.length ? text1 : text2;
  var shorttext = text1.length > text2.length ? text2 : text1;
  if (longtext.length < 4 || shorttext.length * 2 < longtext.length) {
    return null;  // Pointless.
  }

  /**
   * Does a substring of shorttext exist within longtext such that the substring
   * is at least half the length of longtext?
   * Closure, but does not reference any external variables.
   * @param {string} longtext Longer string.
   * @param {string} shorttext Shorter string.
   * @param {number} i Start index of quarter length substring within longtext.
   * @return {Array.<string>} Five element Array, containing the prefix of
   *     longtext, the suffix of longtext, the prefix of shorttext, the suffix
   *     of shorttext and the common middle.  Or null if there was no match.
   * @private
   */
  function diff_halfMatchI_(longtext, shorttext, i) {
    // Start with a 1/4 length substring at position i as a seed.
    var seed = longtext.substring(i, i + Math.floor(longtext.length / 4));
    var j = -1;
    var best_common = '';
    var best_longtext_a, best_longtext_b, best_shorttext_a, best_shorttext_b;
    while ((j = shorttext.indexOf(seed, j + 1)) != -1) {
      var prefixLength = diff_commonPrefix(longtext.substring(i),
                                           shorttext.substring(j));
      var suffixLength = diff_commonSuffix(longtext.substring(0, i),
                                           shorttext.substring(0, j));
      if (best_common.length < suffixLength + prefixLength) {
        best_common = shorttext.substring(j - suffixLength, j) +
            shorttext.substring(j, j + prefixLength);
        best_longtext_a = longtext.substring(0, i - suffixLength);
        best_longtext_b = longtext.substring(i + prefixLength);
        best_shorttext_a = shorttext.substring(0, j - suffixLength);
        best_shorttext_b = shorttext.substring(j + prefixLength);
      }
    }
    if (best_common.length * 2 >= longtext.length) {
      return [best_longtext_a, best_longtext_b,
              best_shorttext_a, best_shorttext_b, best_common];
    } else {
      return null;
    }
  }

  // First check if the second quarter is the seed for a half-match.
  var hm1 = diff_halfMatchI_(longtext, shorttext,
                             Math.ceil(longtext.length / 4));
  // Check again based on the third quarter.
  var hm2 = diff_halfMatchI_(longtext, shorttext,
                             Math.ceil(longtext.length / 2));
  var hm;
  if (!hm1 && !hm2) {
    return null;
  } else if (!hm2) {
    hm = hm1;
  } else if (!hm1) {
    hm = hm2;
  } else {
    // Both matched.  Select the longest.
    hm = hm1[4].length > hm2[4].length ? hm1 : hm2;
  }

  // A half-match was found, sort out the return data.
  var text1_a, text1_b, text2_a, text2_b;
  if (text1.length > text2.length) {
    text1_a = hm[0];
    text1_b = hm[1];
    text2_a = hm[2];
    text2_b = hm[3];
  } else {
    text2_a = hm[0];
    text2_b = hm[1];
    text1_a = hm[2];
    text1_b = hm[3];
  }
  var mid_common = hm[4];
  return [text1_a, text1_b, text2_a, text2_b, mid_common];
};


/**
 * Reorder and merge like edit sections.  Merge equalities.
 * Any edit section can move as long as it doesn't cross an equality.
 * @param {Array} diffs Array of diff tuples.
 */
function diff_cleanupMerge(diffs) {
  diffs.push([DIFF_EQUAL, '']);  // Add a dummy entry at the end.
  var pointer = 0;
  var count_delete = 0;
  var count_insert = 0;
  var text_delete = '';
  var text_insert = '';
  var commonlength;
  while (pointer < diffs.length) {
    switch (diffs[pointer][0]) {
      case DIFF_INSERT:
        count_insert++;
        text_insert += diffs[pointer][1];
        pointer++;
        break;
      case DIFF_DELETE:
        count_delete++;
        text_delete += diffs[pointer][1];
        pointer++;
        break;
      case DIFF_EQUAL:
        // Upon reaching an equality, check for prior redundancies.
        if (count_delete + count_insert > 1) {
          if (count_delete !== 0 && count_insert !== 0) {
            // Factor out any common prefixies.
            commonlength = diff_commonPrefix(text_insert, text_delete);
            if (commonlength !== 0) {
              if ((pointer - count_delete - count_insert) > 0 &&
                  diffs[pointer - count_delete - count_insert - 1][0] ==
                  DIFF_EQUAL) {
                diffs[pointer - count_delete - count_insert - 1][1] +=
                    text_insert.substring(0, commonlength);
              } else {
                diffs.splice(0, 0, [DIFF_EQUAL,
                                    text_insert.substring(0, commonlength)]);
                pointer++;
              }
              text_insert = text_insert.substring(commonlength);
              text_delete = text_delete.substring(commonlength);
            }
            // Factor out any common suffixies.
            commonlength = diff_commonSuffix(text_insert, text_delete);
            if (commonlength !== 0) {
              diffs[pointer][1] = text_insert.substring(text_insert.length -
                  commonlength) + diffs[pointer][1];
              text_insert = text_insert.substring(0, text_insert.length -
                  commonlength);
              text_delete = text_delete.substring(0, text_delete.length -
                  commonlength);
            }
          }
          // Delete the offending records and add the merged ones.
          if (count_delete === 0) {
            diffs.splice(pointer - count_insert,
                count_delete + count_insert, [DIFF_INSERT, text_insert]);
          } else if (count_insert === 0) {
            diffs.splice(pointer - count_delete,
                count_delete + count_insert, [DIFF_DELETE, text_delete]);
          } else {
            diffs.splice(pointer - count_delete - count_insert,
                count_delete + count_insert, [DIFF_DELETE, text_delete],
                [DIFF_INSERT, text_insert]);
          }
          pointer = pointer - count_delete - count_insert +
                    (count_delete ? 1 : 0) + (count_insert ? 1 : 0) + 1;
        } else if (pointer !== 0 && diffs[pointer - 1][0] == DIFF_EQUAL) {
          // Merge this equality with the previous one.
          diffs[pointer - 1][1] += diffs[pointer][1];
          diffs.splice(pointer, 1);
        } else {
          pointer++;
        }
        count_insert = 0;
        count_delete = 0;
        text_delete = '';
        text_insert = '';
        break;
    }
  }
  if (diffs[diffs.length - 1][1] === '') {
    diffs.pop();  // Remove the dummy entry at the end.
  }

  // Second pass: look for single edits surrounded on both sides by equalities
  // which can be shifted sideways to eliminate an equality.
  // e.g: A<ins>BA</ins>C -> <ins>AB</ins>AC
  var changes = false;
  pointer = 1;
  // Intentionally ignore the first and last element (don't need checking).
  while (pointer < diffs.length - 1) {
    if (diffs[pointer - 1][0] == DIFF_EQUAL &&
        diffs[pointer + 1][0] == DIFF_EQUAL) {
      // This is a single edit surrounded by equalities.
      if (diffs[pointer][1].substring(diffs[pointer][1].length -
          diffs[pointer - 1][1].length) == diffs[pointer - 1][1]) {
        // Shift the edit over the previous equality.
        diffs[pointer][1] = diffs[pointer - 1][1] +
            diffs[pointer][1].substring(0, diffs[pointer][1].length -
                                        diffs[pointer - 1][1].length);
        diffs[pointer + 1][1] = diffs[pointer - 1][1] + diffs[pointer + 1][1];
        diffs.splice(pointer - 1, 1);
        changes = true;
      } else if (diffs[pointer][1].substring(0, diffs[pointer + 1][1].length) ==
          diffs[pointer + 1][1]) {
        // Shift the edit over the next equality.
        diffs[pointer - 1][1] += diffs[pointer + 1][1];
        diffs[pointer][1] =
            diffs[pointer][1].substring(diffs[pointer + 1][1].length) +
            diffs[pointer + 1][1];
        diffs.splice(pointer + 1, 1);
        changes = true;
      }
    }
    pointer++;
  }
  // If shifts were made, the diff needs reordering and another shift sweep.
  if (changes) {
    diff_cleanupMerge(diffs);
  }
};


var diff = diff_main;
diff.INSERT = DIFF_INSERT;
diff.DELETE = DIFF_DELETE;
diff.EQUAL = DIFF_EQUAL;

module.exports = diff;

/*
 * Modify a diff such that the cursor position points to the start of a change:
 * E.g.
 *   cursor_normalize_diff([[DIFF_EQUAL, 'abc']], 1)
 *     => [1, [[DIFF_EQUAL, 'a'], [DIFF_EQUAL, 'bc']]]
 *   cursor_normalize_diff([[DIFF_INSERT, 'new'], [DIFF_DELETE, 'xyz']], 2)
 *     => [2, [[DIFF_INSERT, 'new'], [DIFF_DELETE, 'xy'], [DIFF_DELETE, 'z']]]
 *
 * @param {Array} diffs Array of diff tuples
 * @param {Int} cursor_pos Suggested edit position. Must not be out of bounds!
 * @return {Array} A tuple [cursor location in the modified diff, modified diff]
 */
function cursor_normalize_diff (diffs, cursor_pos) {
  if (cursor_pos === 0) {
    return [DIFF_EQUAL, diffs];
  }
  for (var current_pos = 0, i = 0; i < diffs.length; i++) {
    var d = diffs[i];
    if (d[0] === DIFF_DELETE || d[0] === DIFF_EQUAL) {
      var next_pos = current_pos + d[1].length;
      if (cursor_pos === next_pos) {
        return [i + 1, diffs];
      } else if (cursor_pos < next_pos) {
        // copy to prevent side effects
        diffs = diffs.slice();
        // split d into two diff changes
        var split_pos = cursor_pos - current_pos;
        var d_left = [d[0], d[1].slice(0, split_pos)];
        var d_right = [d[0], d[1].slice(split_pos)];
        diffs.splice(i, 1, d_left, d_right);
        return [i + 1, diffs];
      } else {
        current_pos = next_pos;
      }
    }
  }
  throw new Error('cursor_pos is out of bounds!')
}

/*
 * Modify a diff such that the edit position is "shifted" to the proposed edit location (cursor_position).
 *
 * Case 1)
 *   Check if a naive shift is possible:
 *     [0, X], [ 1, Y] -> [ 1, Y], [0, X]    (if X + Y === Y + X)
 *     [0, X], [-1, Y] -> [-1, Y], [0, X]    (if X + Y === Y + X) - holds same result
 * Case 2)
 *   Check if the following shifts are possible:
 *     [0, 'pre'], [ 1, 'prefix'] -> [ 1, 'pre'], [0, 'pre'], [ 1, 'fix']
 *     [0, 'pre'], [-1, 'prefix'] -> [-1, 'pre'], [0, 'pre'], [-1, 'fix']
 *         ^            ^
 *         d          d_next
 *
 * @param {Array} diffs Array of diff tuples
 * @param {Int} cursor_pos Suggested edit position. Must not be out of bounds!
 * @return {Array} Array of diff tuples
 */
function fix_cursor (diffs, cursor_pos) {
  var norm = cursor_normalize_diff(diffs, cursor_pos);
  var ndiffs = norm[1];
  var cursor_pointer = norm[0];
  var d = ndiffs[cursor_pointer];
  var d_next = ndiffs[cursor_pointer + 1];

  if (d == null) {
    // Text was deleted from end of original string,
    // cursor is now out of bounds in new string
    return diffs;
  } else if (d[0] !== DIFF_EQUAL) {
    // A modification happened at the cursor location.
    // This is the expected outcome, so we can return the original diff.
    return diffs;
  } else {
    if (d_next != null && d[1] + d_next[1] === d_next[1] + d[1]) {
      // Case 1)
      // It is possible to perform a naive shift
      ndiffs.splice(cursor_pointer, 2, d_next, d)
      return merge_tuples(ndiffs, cursor_pointer, 2)
    } else if (d_next != null && d_next[1].indexOf(d[1]) === 0) {
      // Case 2)
      // d[1] is a prefix of d_next[1]
      // We can assume that d_next[0] !== 0, since d[0] === 0
      // Shift edit locations..
      ndiffs.splice(cursor_pointer, 2, [d_next[0], d[1]], [0, d[1]]);
      var suffix = d_next[1].slice(d[1].length);
      if (suffix.length > 0) {
        ndiffs.splice(cursor_pointer + 2, 0, [d_next[0], suffix]);
      }
      return merge_tuples(ndiffs, cursor_pointer, 3)
    } else {
      // Not possible to perform any modification
      return diffs;
    }
  }
}

/*
 * Check diff did not split surrogate pairs.
 * Ex. [0, '\uD83D'], [-1, '\uDC36'], [1, '\uDC2F'] -> [-1, '\uD83D\uDC36'], [1, '\uD83D\uDC2F']
 *     '\uD83D\uDC36' === '🐶', '\uD83D\uDC2F' === '🐯'
 *
 * @param {Array} diffs Array of diff tuples
 * @return {Array} Array of diff tuples
 */
function fix_emoji (diffs) {
  var compact = false;
  var starts_with_pair_end = function(str) {
    return str.charCodeAt(0) >= 0xDC00 && str.charCodeAt(0) <= 0xDFFF;
  }
  var ends_with_pair_start = function(str) {
    return str.charCodeAt(str.length-1) >= 0xD800 && str.charCodeAt(str.length-1) <= 0xDBFF;
  }
  for (var i = 2; i < diffs.length; i += 1) {
    if (diffs[i-2][0] === DIFF_EQUAL && ends_with_pair_start(diffs[i-2][1]) &&
        diffs[i-1][0] === DIFF_DELETE && starts_with_pair_end(diffs[i-1][1]) &&
        diffs[i][0] === DIFF_INSERT && starts_with_pair_end(diffs[i][1])) {
      compact = true;

      diffs[i-1][1] = diffs[i-2][1].slice(-1) + diffs[i-1][1];
      diffs[i][1] = diffs[i-2][1].slice(-1) + diffs[i][1];

      diffs[i-2][1] = diffs[i-2][1].slice(0, -1);
    }
  }
  if (!compact) {
    return diffs;
  }
  var fixed_diffs = [];
  for (var i = 0; i < diffs.length; i += 1) {
    if (diffs[i][1].length > 0) {
      fixed_diffs.push(diffs[i]);
    }
  }
  return fixed_diffs;
}

/*
 * Try to merge tuples with their neigbors in a given range.
 * E.g. [0, 'a'], [0, 'b'] -> [0, 'ab']
 *
 * @param {Array} diffs Array of diff tuples.
 * @param {Int} start Position of the first element to merge (diffs[start] is also merged with diffs[start - 1]).
 * @param {Int} length Number of consecutive elements to check.
 * @return {Array} Array of merged diff tuples.
 */
function merge_tuples (diffs, start, length) {
  // Check from (start-1) to (start+length).
  for (var i = start + length - 1; i >= 0 && i >= start - 1; i--) {
    if (i + 1 < diffs.length) {
      var left_d = diffs[i];
      var right_d = diffs[i+1];
      if (left_d[0] === right_d[1]) {
        diffs.splice(i, 2, [left_d[0], left_d[1] + right_d[1]]);
      }
    }
  }
  return diffs;
}


/***/ }),
/* 52 */
/***/ (function(module, exports) {

exports = module.exports = typeof Object.keys === 'function'
  ? Object.keys : shim;

exports.shim = shim;
function shim (obj) {
  var keys = [];
  for (var key in obj) keys.push(key);
  return keys;
}


/***/ }),
/* 53 */
/***/ (function(module, exports) {

var supportsArgumentsClass = (function(){
  return Object.prototype.toString.call(arguments)
})() == '[object Arguments]';

exports = module.exports = supportsArgumentsClass ? supported : unsupported;

exports.supported = supported;
function supported(object) {
  return Object.prototype.toString.call(object) == '[object Arguments]';
};

exports.unsupported = unsupported;
function unsupported(object){
  return object &&
    typeof object == 'object' &&
    typeof object.length == 'number' &&
    Object.prototype.hasOwnProperty.call(object, 'callee') &&
    !Object.prototype.propertyIsEnumerable.call(object, 'callee') ||
    false;
};


/***/ }),
/* 54 */
/***/ (function(module, exports) {

'use strict';

var has = Object.prototype.hasOwnProperty
  , prefix = '~';

/**
 * Constructor to create a storage for our `EE` objects.
 * An `Events` instance is a plain object whose properties are event names.
 *
 * @constructor
 * @api private
 */
function Events() {}

//
// We try to not inherit from `Object.prototype`. In some engines creating an
// instance in this way is faster than calling `Object.create(null)` directly.
// If `Object.create(null)` is not supported we prefix the event names with a
// character to make sure that the built-in object properties are not
// overridden or used as an attack vector.
//
if (Object.create) {
  Events.prototype = Object.create(null);

  //
  // This hack is needed because the `__proto__` property is still inherited in
  // some old browsers like Android 4, iPhone 5.1, Opera 11 and Safari 5.
  //
  if (!new Events().__proto__) prefix = false;
}

/**
 * Representation of a single event listener.
 *
 * @param {Function} fn The listener function.
 * @param {Mixed} context The context to invoke the listener with.
 * @param {Boolean} [once=false] Specify if the listener is a one-time listener.
 * @constructor
 * @api private
 */
function EE(fn, context, once) {
  this.fn = fn;
  this.context = context;
  this.once = once || false;
}

/**
 * Minimal `EventEmitter` interface that is molded against the Node.js
 * `EventEmitter` interface.
 *
 * @constructor
 * @api public
 */
function EventEmitter() {
  this._events = new Events();
  this._eventsCount = 0;
}

/**
 * Return an array listing the events for which the emitter has registered
 * listeners.
 *
 * @returns {Array}
 * @api public
 */
EventEmitter.prototype.eventNames = function eventNames() {
  var names = []
    , events
    , name;

  if (this._eventsCount === 0) return names;

  for (name in (events = this._events)) {
    if (has.call(events, name)) names.push(prefix ? name.slice(1) : name);
  }

  if (Object.getOwnPropertySymbols) {
    return names.concat(Object.getOwnPropertySymbols(events));
  }

  return names;
};

/**
 * Return the listeners registered for a given event.
 *
 * @param {String|Symbol} event The event name.
 * @param {Boolean} exists Only check if there are listeners.
 * @returns {Array|Boolean}
 * @api public
 */
EventEmitter.prototype.listeners = function listeners(event, exists) {
  var evt = prefix ? prefix + event : event
    , available = this._events[evt];

  if (exists) return !!available;
  if (!available) return [];
  if (available.fn) return [available.fn];

  for (var i = 0, l = available.length, ee = new Array(l); i < l; i++) {
    ee[i] = available[i].fn;
  }

  return ee;
};

/**
 * Calls each of the listeners registered for a given event.
 *
 * @param {String|Symbol} event The event name.
 * @returns {Boolean} `true` if the event had listeners, else `false`.
 * @api public
 */
EventEmitter.prototype.emit = function emit(event, a1, a2, a3, a4, a5) {
  var evt = prefix ? prefix + event : event;

  if (!this._events[evt]) return false;

  var listeners = this._events[evt]
    , len = arguments.length
    , args
    , i;

  if (listeners.fn) {
    if (listeners.once) this.removeListener(event, listeners.fn, undefined, true);

    switch (len) {
      case 1: return listeners.fn.call(listeners.context), true;
      case 2: return listeners.fn.call(listeners.context, a1), true;
      case 3: return listeners.fn.call(listeners.context, a1, a2), true;
      case 4: return listeners.fn.call(listeners.context, a1, a2, a3), true;
      case 5: return listeners.fn.call(listeners.context, a1, a2, a3, a4), true;
      case 6: return listeners.fn.call(listeners.context, a1, a2, a3, a4, a5), true;
    }

    for (i = 1, args = new Array(len -1); i < len; i++) {
      args[i - 1] = arguments[i];
    }

    listeners.fn.apply(listeners.context, args);
  } else {
    var length = listeners.length
      , j;

    for (i = 0; i < length; i++) {
      if (listeners[i].once) this.removeListener(event, listeners[i].fn, undefined, true);

      switch (len) {
        case 1: listeners[i].fn.call(listeners[i].context); break;
        case 2: listeners[i].fn.call(listeners[i].context, a1); break;
        case 3: listeners[i].fn.call(listeners[i].context, a1, a2); break;
        case 4: listeners[i].fn.call(listeners[i].context, a1, a2, a3); break;
        default:
          if (!args) for (j = 1, args = new Array(len -1); j < len; j++) {
            args[j - 1] = arguments[j];
          }

          listeners[i].fn.apply(listeners[i].context, args);
      }
    }
  }

  return true;
};

/**
 * Add a listener for a given event.
 *
 * @param {String|Symbol} event The event name.
 * @param {Function} fn The listener function.
 * @param {Mixed} [context=this] The context to invoke the listener with.
 * @returns {EventEmitter} `this`.
 * @api public
 */
EventEmitter.prototype.on = function on(event, fn, context) {
  var listener = new EE(fn, context || this)
    , evt = prefix ? prefix + event : event;

  if (!this._events[evt]) this._events[evt] = listener, this._eventsCount++;
  else if (!this._events[evt].fn) this._events[evt].push(listener);
  else this._events[evt] = [this._events[evt], listener];

  return this;
};

/**
 * Add a one-time listener for a given event.
 *
 * @param {String|Symbol} event The event name.
 * @param {Function} fn The listener function.
 * @param {Mixed} [context=this] The context to invoke the listener with.
 * @returns {EventEmitter} `this`.
 * @api public
 */
EventEmitter.prototype.once = function once(event, fn, context) {
  var listener = new EE(fn, context || this, true)
    , evt = prefix ? prefix + event : event;

  if (!this._events[evt]) this._events[evt] = listener, this._eventsCount++;
  else if (!this._events[evt].fn) this._events[evt].push(listener);
  else this._events[evt] = [this._events[evt], listener];

  return this;
};

/**
 * Remove the listeners of a given event.
 *
 * @param {String|Symbol} event The event name.
 * @param {Function} fn Only remove the listeners that match this function.
 * @param {Mixed} context Only remove the listeners that have this context.
 * @param {Boolean} once Only remove one-time listeners.
 * @returns {EventEmitter} `this`.
 * @api public
 */
EventEmitter.prototype.removeListener = function removeListener(event, fn, context, once) {
  var evt = prefix ? prefix + event : event;

  if (!this._events[evt]) return this;
  if (!fn) {
    if (--this._eventsCount === 0) this._events = new Events();
    else delete this._events[evt];
    return this;
  }

  var listeners = this._events[evt];

  if (listeners.fn) {
    if (
         listeners.fn === fn
      && (!once || listeners.once)
      && (!context || listeners.context === context)
    ) {
      if (--this._eventsCount === 0) this._events = new Events();
      else delete this._events[evt];
    }
  } else {
    for (var i = 0, events = [], length = listeners.length; i < length; i++) {
      if (
           listeners[i].fn !== fn
        || (once && !listeners[i].once)
        || (context && listeners[i].context !== context)
      ) {
        events.push(listeners[i]);
      }
    }

    //
    // Reset the array, or remove it completely if we have no more listeners.
    //
    if (events.length) this._events[evt] = events.length === 1 ? events[0] : events;
    else if (--this._eventsCount === 0) this._events = new Events();
    else delete this._events[evt];
  }

  return this;
};

/**
 * Remove all listeners, or those of the specified event.
 *
 * @param {String|Symbol} [event] The event name.
 * @returns {EventEmitter} `this`.
 * @api public
 */
EventEmitter.prototype.removeAllListeners = function removeAllListeners(event) {
  var evt;

  if (event) {
    evt = prefix ? prefix + event : event;
    if (this._events[evt]) {
      if (--this._eventsCount === 0) this._events = new Events();
      else delete this._events[evt];
    }
  } else {
    this._events = new Events();
    this._eventsCount = 0;
  }

  return this;
};

//
// Alias methods names because people roll like that.
//
EventEmitter.prototype.off = EventEmitter.prototype.removeListener;
EventEmitter.prototype.addListener = EventEmitter.prototype.on;

//
// This function doesn't apply anymore.
//
EventEmitter.prototype.setMaxListeners = function setMaxListeners() {
  return this;
};

//
// Expose the prefix.
//
EventEmitter.prefixed = prefix;

//
// Allow `EventEmitter` to be imported as module namespace.
//
EventEmitter.EventEmitter = EventEmitter;

//
// Expose the module.
//
if ('undefined' !== typeof module) {
  module.exports = EventEmitter;
}


/***/ }),
/* 55 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.matchText = exports.matchSpacing = exports.matchNewline = exports.matchBlot = exports.matchAttributor = exports.default = undefined;

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _extend2 = __webpack_require__(3);

var _extend3 = _interopRequireDefault(_extend2);

var _quillDelta = __webpack_require__(2);

var _quillDelta2 = _interopRequireDefault(_quillDelta);

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _quill = __webpack_require__(5);

var _quill2 = _interopRequireDefault(_quill);

var _logger = __webpack_require__(10);

var _logger2 = _interopRequireDefault(_logger);

var _module = __webpack_require__(9);

var _module2 = _interopRequireDefault(_module);

var _align = __webpack_require__(36);

var _background = __webpack_require__(37);

var _code = __webpack_require__(13);

var _code2 = _interopRequireDefault(_code);

var _color = __webpack_require__(26);

var _direction = __webpack_require__(38);

var _font = __webpack_require__(39);

var _size = __webpack_require__(40);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var debug = (0, _logger2.default)('quill:clipboard');

var DOM_KEY = '__ql-matcher';

var CLIPBOARD_CONFIG = [[Node.TEXT_NODE, matchText], [Node.TEXT_NODE, matchNewline], ['br', matchBreak], [Node.ELEMENT_NODE, matchNewline], [Node.ELEMENT_NODE, matchBlot], [Node.ELEMENT_NODE, matchSpacing], [Node.ELEMENT_NODE, matchAttributor], [Node.ELEMENT_NODE, matchStyles], ['li', matchIndent], ['b', matchAlias.bind(matchAlias, 'bold')], ['i', matchAlias.bind(matchAlias, 'italic')], ['style', matchIgnore]];

var ATTRIBUTE_ATTRIBUTORS = [_align.AlignAttribute, _direction.DirectionAttribute].reduce(function (memo, attr) {
  memo[attr.keyName] = attr;
  return memo;
}, {});

var STYLE_ATTRIBUTORS = [_align.AlignStyle, _background.BackgroundStyle, _color.ColorStyle, _direction.DirectionStyle, _font.FontStyle, _size.SizeStyle].reduce(function (memo, attr) {
  memo[attr.keyName] = attr;
  return memo;
}, {});

var Clipboard = function (_Module) {
  _inherits(Clipboard, _Module);

  function Clipboard(quill, options) {
    _classCallCheck(this, Clipboard);

    var _this = _possibleConstructorReturn(this, (Clipboard.__proto__ || Object.getPrototypeOf(Clipboard)).call(this, quill, options));

    _this.quill.root.addEventListener('paste', _this.onPaste.bind(_this));
    _this.container = _this.quill.addContainer('ql-clipboard');
    _this.container.setAttribute('contenteditable', true);
    _this.container.setAttribute('tabindex', -1);
    _this.matchers = [];
    CLIPBOARD_CONFIG.concat(_this.options.matchers).forEach(function (_ref) {
      var _ref2 = _slicedToArray(_ref, 2),
          selector = _ref2[0],
          matcher = _ref2[1];

      if (!options.matchVisual && matcher === matchSpacing) return;
      _this.addMatcher(selector, matcher);
    });
    return _this;
  }

  _createClass(Clipboard, [{
    key: 'addMatcher',
    value: function addMatcher(selector, matcher) {
      this.matchers.push([selector, matcher]);
    }
  }, {
    key: 'convert',
    value: function convert(html) {
      if (typeof html === 'string') {
        this.container.innerHTML = html.replace(/\>\r?\n +\</g, '><'); // Remove spaces between tags
        return this.convert();
      }
      var formats = this.quill.getFormat(this.quill.selection.savedRange.index);
      if (formats[_code2.default.blotName]) {
        var text = this.container.innerText;
        this.container.innerHTML = '';
        return new _quillDelta2.default().insert(text, _defineProperty({}, _code2.default.blotName, formats[_code2.default.blotName]));
      }

      var _prepareMatching = this.prepareMatching(),
          _prepareMatching2 = _slicedToArray(_prepareMatching, 2),
          elementMatchers = _prepareMatching2[0],
          textMatchers = _prepareMatching2[1];

      var delta = traverse(this.container, elementMatchers, textMatchers);
      // Remove trailing newline
      if (deltaEndsWith(delta, '\n') && delta.ops[delta.ops.length - 1].attributes == null) {
        delta = delta.compose(new _quillDelta2.default().retain(delta.length() - 1).delete(1));
      }
      debug.log('convert', this.container.innerHTML, delta);
      this.container.innerHTML = '';
      return delta;
    }
  }, {
    key: 'dangerouslyPasteHTML',
    value: function dangerouslyPasteHTML(index, html) {
      var source = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : _quill2.default.sources.API;

      if (typeof index === 'string') {
        this.quill.setContents(this.convert(index), html);
        this.quill.setSelection(0, _quill2.default.sources.SILENT);
      } else {
        var paste = this.convert(html);
        this.quill.updateContents(new _quillDelta2.default().retain(index).concat(paste), source);
        this.quill.setSelection(index + paste.length(), _quill2.default.sources.SILENT);
      }
    }
  }, {
    key: 'onPaste',
    value: function onPaste(e) {
      var _this2 = this;

      if (e.defaultPrevented || !this.quill.isEnabled()) return;
      var range = this.quill.getSelection();
      var delta = new _quillDelta2.default().retain(range.index);
      var scrollTop = this.quill.scrollingContainer.scrollTop;
      this.container.focus();
      this.quill.selection.update(_quill2.default.sources.SILENT);
      setTimeout(function () {
        delta = delta.concat(_this2.convert()).delete(range.length);
        _this2.quill.updateContents(delta, _quill2.default.sources.USER);
        // range.length contributes to delta.length()
        _this2.quill.setSelection(delta.length() - range.length, _quill2.default.sources.SILENT);
        _this2.quill.scrollingContainer.scrollTop = scrollTop;
        _this2.quill.focus();
      }, 1);
    }
  }, {
    key: 'prepareMatching',
    value: function prepareMatching() {
      var _this3 = this;

      var elementMatchers = [],
          textMatchers = [];
      this.matchers.forEach(function (pair) {
        var _pair = _slicedToArray(pair, 2),
            selector = _pair[0],
            matcher = _pair[1];

        switch (selector) {
          case Node.TEXT_NODE:
            textMatchers.push(matcher);
            break;
          case Node.ELEMENT_NODE:
            elementMatchers.push(matcher);
            break;
          default:
            [].forEach.call(_this3.container.querySelectorAll(selector), function (node) {
              // TODO use weakmap
              node[DOM_KEY] = node[DOM_KEY] || [];
              node[DOM_KEY].push(matcher);
            });
            break;
        }
      });
      return [elementMatchers, textMatchers];
    }
  }]);

  return Clipboard;
}(_module2.default);

Clipboard.DEFAULTS = {
  matchers: [],
  matchVisual: true
};

function applyFormat(delta, format, value) {
  if ((typeof format === 'undefined' ? 'undefined' : _typeof(format)) === 'object') {
    return Object.keys(format).reduce(function (delta, key) {
      return applyFormat(delta, key, format[key]);
    }, delta);
  } else {
    return delta.reduce(function (delta, op) {
      if (op.attributes && op.attributes[format]) {
        return delta.push(op);
      } else {
        return delta.insert(op.insert, (0, _extend3.default)({}, _defineProperty({}, format, value), op.attributes));
      }
    }, new _quillDelta2.default());
  }
}

function computeStyle(node) {
  if (node.nodeType !== Node.ELEMENT_NODE) return {};
  var DOM_KEY = '__ql-computed-style';
  return node[DOM_KEY] || (node[DOM_KEY] = window.getComputedStyle(node));
}

function deltaEndsWith(delta, text) {
  var endText = "";
  for (var i = delta.ops.length - 1; i >= 0 && endText.length < text.length; --i) {
    var op = delta.ops[i];
    if (typeof op.insert !== 'string') break;
    endText = op.insert + endText;
  }
  return endText.slice(-1 * text.length) === text;
}

function isLine(node) {
  if (node.childNodes.length === 0) return false; // Exclude embed blocks
  var style = computeStyle(node);
  return ['block', 'list-item'].indexOf(style.display) > -1;
}

function traverse(node, elementMatchers, textMatchers) {
  // Post-order
  if (node.nodeType === node.TEXT_NODE) {
    return textMatchers.reduce(function (delta, matcher) {
      return matcher(node, delta);
    }, new _quillDelta2.default());
  } else if (node.nodeType === node.ELEMENT_NODE) {
    return [].reduce.call(node.childNodes || [], function (delta, childNode) {
      var childrenDelta = traverse(childNode, elementMatchers, textMatchers);
      if (childNode.nodeType === node.ELEMENT_NODE) {
        childrenDelta = elementMatchers.reduce(function (childrenDelta, matcher) {
          return matcher(childNode, childrenDelta);
        }, childrenDelta);
        childrenDelta = (childNode[DOM_KEY] || []).reduce(function (childrenDelta, matcher) {
          return matcher(childNode, childrenDelta);
        }, childrenDelta);
      }
      return delta.concat(childrenDelta);
    }, new _quillDelta2.default());
  } else {
    return new _quillDelta2.default();
  }
}

function matchAlias(format, node, delta) {
  return applyFormat(delta, format, true);
}

function matchAttributor(node, delta) {
  var attributes = _parchment2.default.Attributor.Attribute.keys(node);
  var classes = _parchment2.default.Attributor.Class.keys(node);
  var styles = _parchment2.default.Attributor.Style.keys(node);
  var formats = {};
  attributes.concat(classes).concat(styles).forEach(function (name) {
    var attr = _parchment2.default.query(name, _parchment2.default.Scope.ATTRIBUTE);
    if (attr != null) {
      formats[attr.attrName] = attr.value(node);
      if (formats[attr.attrName]) return;
    }
    attr = ATTRIBUTE_ATTRIBUTORS[name];
    if (attr != null && (attr.attrName === name || attr.keyName === name)) {
      formats[attr.attrName] = attr.value(node) || undefined;
    }
    attr = STYLE_ATTRIBUTORS[name];
    if (attr != null && (attr.attrName === name || attr.keyName === name)) {
      attr = STYLE_ATTRIBUTORS[name];
      formats[attr.attrName] = attr.value(node) || undefined;
    }
  });
  if (Object.keys(formats).length > 0) {
    delta = applyFormat(delta, formats);
  }
  return delta;
}

function matchBlot(node, delta) {
  var match = _parchment2.default.query(node);
  if (match == null) return delta;
  if (match.prototype instanceof _parchment2.default.Embed) {
    var embed = {};
    var value = match.value(node);
    if (value != null) {
      embed[match.blotName] = value;
      delta = new _quillDelta2.default().insert(embed, match.formats(node));
    }
  } else if (typeof match.formats === 'function') {
    delta = applyFormat(delta, match.blotName, match.formats(node));
  }
  return delta;
}

function matchBreak(node, delta) {
  if (!deltaEndsWith(delta, '\n')) {
    delta.insert('\n');
  }
  return delta;
}

function matchIgnore() {
  return new _quillDelta2.default();
}

function matchIndent(node, delta) {
  var match = _parchment2.default.query(node);
  if (match == null || match.blotName !== 'list-item' || !deltaEndsWith(delta, '\n')) {
    return delta;
  }
  var indent = -1,
      parent = node.parentNode;
  while (!parent.classList.contains('ql-clipboard')) {
    if ((_parchment2.default.query(parent) || {}).blotName === 'list') {
      indent += 1;
    }
    parent = parent.parentNode;
  }
  if (indent <= 0) return delta;
  return delta.compose(new _quillDelta2.default().retain(delta.length() - 1).retain(1, { indent: indent }));
}

function matchNewline(node, delta) {
  if (!deltaEndsWith(delta, '\n')) {
    if (isLine(node) || delta.length() > 0 && node.nextSibling && isLine(node.nextSibling)) {
      delta.insert('\n');
    }
  }
  return delta;
}

function matchSpacing(node, delta) {
  if (isLine(node) && node.nextElementSibling != null && !deltaEndsWith(delta, '\n\n')) {
    var nodeHeight = node.offsetHeight + parseFloat(computeStyle(node).marginTop) + parseFloat(computeStyle(node).marginBottom);
    if (node.nextElementSibling.offsetTop > node.offsetTop + nodeHeight * 1.5) {
      delta.insert('\n');
    }
  }
  return delta;
}

function matchStyles(node, delta) {
  var formats = {};
  var style = node.style || {};
  if (style.fontStyle && computeStyle(node).fontStyle === 'italic') {
    formats.italic = true;
  }
  if (style.fontWeight && (computeStyle(node).fontWeight.startsWith('bold') || parseInt(computeStyle(node).fontWeight) >= 700)) {
    formats.bold = true;
  }
  if (Object.keys(formats).length > 0) {
    delta = applyFormat(delta, formats);
  }
  if (parseFloat(style.textIndent || 0) > 0) {
    // Could be 0.5in
    delta = new _quillDelta2.default().insert('\t').concat(delta);
  }
  return delta;
}

function matchText(node, delta) {
  var text = node.data;
  // Word represents empty line with <o:p>&nbsp;</o:p>
  if (node.parentNode.tagName === 'O:P') {
    return delta.insert(text.trim());
  }
  if (text.trim().length === 0 && node.parentNode.classList.contains('ql-clipboard')) {
    return delta;
  }
  if (!computeStyle(node.parentNode).whiteSpace.startsWith('pre')) {
    // eslint-disable-next-line func-style
    var replacer = function replacer(collapse, match) {
      match = match.replace(/[^\u00a0]/g, ''); // \u00a0 is nbsp;
      return match.length < 1 && collapse ? ' ' : match;
    };
    text = text.replace(/\r\n/g, ' ').replace(/\n/g, ' ');
    text = text.replace(/\s\s+/g, replacer.bind(replacer, true)); // collapse whitespace
    if (node.previousSibling == null && isLine(node.parentNode) || node.previousSibling != null && isLine(node.previousSibling)) {
      text = text.replace(/^\s+/, replacer.bind(replacer, false));
    }
    if (node.nextSibling == null && isLine(node.parentNode) || node.nextSibling != null && isLine(node.nextSibling)) {
      text = text.replace(/\s+$/, replacer.bind(replacer, false));
    }
  }
  return delta.insert(text);
}

exports.default = Clipboard;
exports.matchAttributor = matchAttributor;
exports.matchBlot = matchBlot;
exports.matchNewline = matchNewline;
exports.matchSpacing = matchSpacing;
exports.matchText = matchText;

/***/ }),
/* 56 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _inline = __webpack_require__(6);

var _inline2 = _interopRequireDefault(_inline);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Bold = function (_Inline) {
  _inherits(Bold, _Inline);

  function Bold() {
    _classCallCheck(this, Bold);

    return _possibleConstructorReturn(this, (Bold.__proto__ || Object.getPrototypeOf(Bold)).apply(this, arguments));
  }

  _createClass(Bold, [{
    key: 'optimize',
    value: function optimize(context) {
      _get(Bold.prototype.__proto__ || Object.getPrototypeOf(Bold.prototype), 'optimize', this).call(this, context);
      if (this.domNode.tagName !== this.statics.tagName[0]) {
        this.replaceWith(this.statics.blotName);
      }
    }
  }], [{
    key: 'create',
    value: function create() {
      return _get(Bold.__proto__ || Object.getPrototypeOf(Bold), 'create', this).call(this);
    }
  }, {
    key: 'formats',
    value: function formats() {
      return true;
    }
  }]);

  return Bold;
}(_inline2.default);

Bold.blotName = 'bold';
Bold.tagName = ['STRONG', 'B'];

exports.default = Bold;

/***/ }),
/* 57 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.addControls = exports.default = undefined;

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _quillDelta = __webpack_require__(2);

var _quillDelta2 = _interopRequireDefault(_quillDelta);

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _quill = __webpack_require__(5);

var _quill2 = _interopRequireDefault(_quill);

var _logger = __webpack_require__(10);

var _logger2 = _interopRequireDefault(_logger);

var _module = __webpack_require__(9);

var _module2 = _interopRequireDefault(_module);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var debug = (0, _logger2.default)('quill:toolbar');

var Toolbar = function (_Module) {
  _inherits(Toolbar, _Module);

  function Toolbar(quill, options) {
    _classCallCheck(this, Toolbar);

    var _this = _possibleConstructorReturn(this, (Toolbar.__proto__ || Object.getPrototypeOf(Toolbar)).call(this, quill, options));

    if (Array.isArray(_this.options.container)) {
      var container = document.createElement('div');
      addControls(container, _this.options.container);
      quill.container.parentNode.insertBefore(container, quill.container);
      _this.container = container;
    } else if (typeof _this.options.container === 'string') {
      _this.container = document.querySelector(_this.options.container);
    } else {
      _this.container = _this.options.container;
    }
    if (!(_this.container instanceof HTMLElement)) {
      var _ret;

      return _ret = debug.error('Container required for toolbar', _this.options), _possibleConstructorReturn(_this, _ret);
    }
    _this.container.classList.add('ql-toolbar');
    _this.controls = [];
    _this.handlers = {};
    Object.keys(_this.options.handlers).forEach(function (format) {
      _this.addHandler(format, _this.options.handlers[format]);
    });
    [].forEach.call(_this.container.querySelectorAll('button, select'), function (input) {
      _this.attach(input);
    });
    _this.quill.on(_quill2.default.events.EDITOR_CHANGE, function (type, range) {
      if (type === _quill2.default.events.SELECTION_CHANGE) {
        _this.update(range);
      }
    });
    _this.quill.on(_quill2.default.events.SCROLL_OPTIMIZE, function () {
      var _this$quill$selection = _this.quill.selection.getRange(),
          _this$quill$selection2 = _slicedToArray(_this$quill$selection, 1),
          range = _this$quill$selection2[0]; // quill.getSelection triggers update


      _this.update(range);
    });
    return _this;
  }

  _createClass(Toolbar, [{
    key: 'addHandler',
    value: function addHandler(format, handler) {
      this.handlers[format] = handler;
    }
  }, {
    key: 'attach',
    value: function attach(input) {
      var _this2 = this;

      var format = [].find.call(input.classList, function (className) {
        return className.indexOf('ql-') === 0;
      });
      if (!format) return;
      format = format.slice('ql-'.length);
      if (input.tagName === 'BUTTON') {
        input.setAttribute('type', 'button');
      }
      if (this.handlers[format] == null) {
        if (this.quill.scroll.whitelist != null && this.quill.scroll.whitelist[format] == null) {
          debug.warn('ignoring attaching to disabled format', format, input);
          return;
        }
        if (_parchment2.default.query(format) == null) {
          debug.warn('ignoring attaching to nonexistent format', format, input);
          return;
        }
      }
      var eventName = input.tagName === 'SELECT' ? 'change' : 'click';
      input.addEventListener(eventName, function (e) {
        var value = void 0;
        if (input.tagName === 'SELECT') {
          if (input.selectedIndex < 0) return;
          var selected = input.options[input.selectedIndex];
          if (selected.hasAttribute('selected')) {
            value = false;
          } else {
            value = selected.value || false;
          }
        } else {
          if (input.classList.contains('ql-active')) {
            value = false;
          } else {
            value = input.value || !input.hasAttribute('value');
          }
          e.preventDefault();
        }
        _this2.quill.focus();

        var _quill$selection$getR = _this2.quill.selection.getRange(),
            _quill$selection$getR2 = _slicedToArray(_quill$selection$getR, 1),
            range = _quill$selection$getR2[0];

        if (_this2.handlers[format] != null) {
          _this2.handlers[format].call(_this2, value);
        } else if (_parchment2.default.query(format).prototype instanceof _parchment2.default.Embed) {
          value = prompt('Enter ' + format);
          if (!value) return;
          _this2.quill.updateContents(new _quillDelta2.default().retain(range.index).delete(range.length).insert(_defineProperty({}, format, value)), _quill2.default.sources.USER);
        } else {
          _this2.quill.format(format, value, _quill2.default.sources.USER);
        }
        _this2.update(range);
      });
      // TODO use weakmap
      this.controls.push([format, input]);
    }
  }, {
    key: 'update',
    value: function update(range) {
      var formats = range == null ? {} : this.quill.getFormat(range);
      this.controls.forEach(function (pair) {
        var _pair = _slicedToArray(pair, 2),
            format = _pair[0],
            input = _pair[1];

        if (input.tagName === 'SELECT') {
          var option = void 0;
          if (range == null) {
            option = null;
          } else if (formats[format] == null) {
            option = input.querySelector('option[selected]');
          } else if (!Array.isArray(formats[format])) {
            var value = formats[format];
            if (typeof value === 'string') {
              value = value.replace(/\"/g, '\\"');
            }
            option = input.querySelector('option[value="' + value + '"]');
          }
          if (option == null) {
            input.value = ''; // TODO make configurable?
            input.selectedIndex = -1;
          } else {
            option.selected = true;
          }
        } else {
          if (range == null) {
            input.classList.remove('ql-active');
          } else if (input.hasAttribute('value')) {
            // both being null should match (default values)
            // '1' should match with 1 (headers)
            var isActive = formats[format] === input.getAttribute('value') || formats[format] != null && formats[format].toString() === input.getAttribute('value') || formats[format] == null && !input.getAttribute('value');
            input.classList.toggle('ql-active', isActive);
          } else {
            input.classList.toggle('ql-active', formats[format] != null);
          }
        }
      });
    }
  }]);

  return Toolbar;
}(_module2.default);

Toolbar.DEFAULTS = {};

function addButton(container, format, value) {
  var input = document.createElement('button');
  input.setAttribute('type', 'button');
  input.classList.add('ql-' + format);
  if (value != null) {
    input.value = value;
  }
  container.appendChild(input);
}

function addControls(container, groups) {
  if (!Array.isArray(groups[0])) {
    groups = [groups];
  }
  groups.forEach(function (controls) {
    var group = document.createElement('span');
    group.classList.add('ql-formats');
    controls.forEach(function (control) {
      if (typeof control === 'string') {
        addButton(group, control);
      } else {
        var format = Object.keys(control)[0];
        var value = control[format];
        if (Array.isArray(value)) {
          addSelect(group, format, value);
        } else {
          addButton(group, format, value);
        }
      }
    });
    container.appendChild(group);
  });
}

function addSelect(container, format, values) {
  var input = document.createElement('select');
  input.classList.add('ql-' + format);
  values.forEach(function (value) {
    var option = document.createElement('option');
    if (value !== false) {
      option.setAttribute('value', value);
    } else {
      option.setAttribute('selected', 'selected');
    }
    input.appendChild(option);
  });
  container.appendChild(input);
}

Toolbar.DEFAULTS = {
  container: null,
  handlers: {
    clean: function clean() {
      var _this3 = this;

      var range = this.quill.getSelection();
      if (range == null) return;
      if (range.length == 0) {
        var formats = this.quill.getFormat();
        Object.keys(formats).forEach(function (name) {
          // Clean functionality in existing apps only clean inline formats
          if (_parchment2.default.query(name, _parchment2.default.Scope.INLINE) != null) {
            _this3.quill.format(name, false);
          }
        });
      } else {
        this.quill.removeFormat(range, _quill2.default.sources.USER);
      }
    },
    direction: function direction(value) {
      var align = this.quill.getFormat()['align'];
      if (value === 'rtl' && align == null) {
        this.quill.format('align', 'right', _quill2.default.sources.USER);
      } else if (!value && align === 'right') {
        this.quill.format('align', false, _quill2.default.sources.USER);
      }
      this.quill.format('direction', value, _quill2.default.sources.USER);
    },
    indent: function indent(value) {
      var range = this.quill.getSelection();
      var formats = this.quill.getFormat(range);
      var indent = parseInt(formats.indent || 0);
      if (value === '+1' || value === '-1') {
        var modifier = value === '+1' ? 1 : -1;
        if (formats.direction === 'rtl') modifier *= -1;
        this.quill.format('indent', indent + modifier, _quill2.default.sources.USER);
      }
    },
    link: function link(value) {
      if (value === true) {
        value = prompt('Enter link URL:');
      }
      this.quill.format('link', value, _quill2.default.sources.USER);
    },
    list: function list(value) {
      var range = this.quill.getSelection();
      var formats = this.quill.getFormat(range);
      if (value === 'check') {
        if (formats['list'] === 'checked' || formats['list'] === 'unchecked') {
          this.quill.format('list', false, _quill2.default.sources.USER);
        } else {
          this.quill.format('list', 'unchecked', _quill2.default.sources.USER);
        }
      } else {
        this.quill.format('list', value, _quill2.default.sources.USER);
      }
    }
  }
};

exports.default = Toolbar;
exports.addControls = addControls;

/***/ }),
/* 58 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <polyline class=\"ql-even ql-stroke\" points=\"5 7 3 9 5 11\"></polyline> <polyline class=\"ql-even ql-stroke\" points=\"13 7 15 9 13 11\"></polyline> <line class=ql-stroke x1=10 x2=8 y1=5 y2=13></line> </svg>";

/***/ }),
/* 59 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _picker = __webpack_require__(28);

var _picker2 = _interopRequireDefault(_picker);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var ColorPicker = function (_Picker) {
  _inherits(ColorPicker, _Picker);

  function ColorPicker(select, label) {
    _classCallCheck(this, ColorPicker);

    var _this = _possibleConstructorReturn(this, (ColorPicker.__proto__ || Object.getPrototypeOf(ColorPicker)).call(this, select));

    _this.label.innerHTML = label;
    _this.container.classList.add('ql-color-picker');
    [].slice.call(_this.container.querySelectorAll('.ql-picker-item'), 0, 7).forEach(function (item) {
      item.classList.add('ql-primary');
    });
    return _this;
  }

  _createClass(ColorPicker, [{
    key: 'buildItem',
    value: function buildItem(option) {
      var item = _get(ColorPicker.prototype.__proto__ || Object.getPrototypeOf(ColorPicker.prototype), 'buildItem', this).call(this, option);
      item.style.backgroundColor = option.getAttribute('value') || '';
      return item;
    }
  }, {
    key: 'selectItem',
    value: function selectItem(item, trigger) {
      _get(ColorPicker.prototype.__proto__ || Object.getPrototypeOf(ColorPicker.prototype), 'selectItem', this).call(this, item, trigger);
      var colorLabel = this.label.querySelector('.ql-color-label');
      var value = item ? item.getAttribute('data-value') || '' : '';
      if (colorLabel) {
        if (colorLabel.tagName === 'line') {
          colorLabel.style.stroke = value;
        } else {
          colorLabel.style.fill = value;
        }
      }
    }
  }]);

  return ColorPicker;
}(_picker2.default);

exports.default = ColorPicker;

/***/ }),
/* 60 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _picker = __webpack_require__(28);

var _picker2 = _interopRequireDefault(_picker);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var IconPicker = function (_Picker) {
  _inherits(IconPicker, _Picker);

  function IconPicker(select, icons) {
    _classCallCheck(this, IconPicker);

    var _this = _possibleConstructorReturn(this, (IconPicker.__proto__ || Object.getPrototypeOf(IconPicker)).call(this, select));

    _this.container.classList.add('ql-icon-picker');
    [].forEach.call(_this.container.querySelectorAll('.ql-picker-item'), function (item) {
      item.innerHTML = icons[item.getAttribute('data-value') || ''];
    });
    _this.defaultItem = _this.container.querySelector('.ql-selected');
    _this.selectItem(_this.defaultItem);
    return _this;
  }

  _createClass(IconPicker, [{
    key: 'selectItem',
    value: function selectItem(item, trigger) {
      _get(IconPicker.prototype.__proto__ || Object.getPrototypeOf(IconPicker.prototype), 'selectItem', this).call(this, item, trigger);
      item = item || this.defaultItem;
      this.label.innerHTML = item.innerHTML;
    }
  }]);

  return IconPicker;
}(_picker2.default);

exports.default = IconPicker;

/***/ }),
/* 61 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Tooltip = function () {
  function Tooltip(quill, boundsContainer) {
    var _this = this;

    _classCallCheck(this, Tooltip);

    this.quill = quill;
    this.boundsContainer = boundsContainer || document.body;
    this.root = quill.addContainer('ql-tooltip');
    this.root.innerHTML = this.constructor.TEMPLATE;
    if (this.quill.root === this.quill.scrollingContainer) {
      this.quill.root.addEventListener('scroll', function () {
        _this.root.style.marginTop = -1 * _this.quill.root.scrollTop + 'px';
      });
    }
    this.hide();
  }

  _createClass(Tooltip, [{
    key: 'hide',
    value: function hide() {
      this.root.classList.add('ql-hidden');
    }
  }, {
    key: 'position',
    value: function position(reference) {
      var left = reference.left + reference.width / 2 - this.root.offsetWidth / 2;
      // root.scrollTop should be 0 if scrollContainer !== root
      var top = reference.bottom + this.quill.root.scrollTop;
      this.root.style.left = left + 'px';
      this.root.style.top = top + 'px';
      this.root.classList.remove('ql-flip');
      var containerBounds = this.boundsContainer.getBoundingClientRect();
      var rootBounds = this.root.getBoundingClientRect();
      var shift = 0;
      if (rootBounds.right > containerBounds.right) {
        shift = containerBounds.right - rootBounds.right;
        this.root.style.left = left + shift + 'px';
      }
      if (rootBounds.left < containerBounds.left) {
        shift = containerBounds.left - rootBounds.left;
        this.root.style.left = left + shift + 'px';
      }
      if (rootBounds.bottom > containerBounds.bottom) {
        var height = rootBounds.bottom - rootBounds.top;
        var verticalShift = reference.bottom - reference.top + height;
        this.root.style.top = top - verticalShift + 'px';
        this.root.classList.add('ql-flip');
      }
      return shift;
    }
  }, {
    key: 'show',
    value: function show() {
      this.root.classList.remove('ql-editing');
      this.root.classList.remove('ql-hidden');
    }
  }]);

  return Tooltip;
}();

exports.default = Tooltip;

/***/ }),
/* 62 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _extend = __webpack_require__(3);

var _extend2 = _interopRequireDefault(_extend);

var _emitter = __webpack_require__(8);

var _emitter2 = _interopRequireDefault(_emitter);

var _base = __webpack_require__(43);

var _base2 = _interopRequireDefault(_base);

var _link = __webpack_require__(27);

var _link2 = _interopRequireDefault(_link);

var _selection = __webpack_require__(15);

var _icons = __webpack_require__(41);

var _icons2 = _interopRequireDefault(_icons);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var TOOLBAR_CONFIG = [[{ header: ['1', '2', '3', false] }], ['bold', 'italic', 'underline', 'link'], [{ list: 'ordered' }, { list: 'bullet' }], ['clean']];

var SnowTheme = function (_BaseTheme) {
  _inherits(SnowTheme, _BaseTheme);

  function SnowTheme(quill, options) {
    _classCallCheck(this, SnowTheme);

    if (options.modules.toolbar != null && options.modules.toolbar.container == null) {
      options.modules.toolbar.container = TOOLBAR_CONFIG;
    }

    var _this = _possibleConstructorReturn(this, (SnowTheme.__proto__ || Object.getPrototypeOf(SnowTheme)).call(this, quill, options));

    _this.quill.container.classList.add('ql-snow');
    return _this;
  }

  _createClass(SnowTheme, [{
    key: 'extendToolbar',
    value: function extendToolbar(toolbar) {
      toolbar.container.classList.add('ql-snow');
      this.buildButtons([].slice.call(toolbar.container.querySelectorAll('button')), _icons2.default);
      this.buildPickers([].slice.call(toolbar.container.querySelectorAll('select')), _icons2.default);
      this.tooltip = new SnowTooltip(this.quill, this.options.bounds);
      if (toolbar.container.querySelector('.ql-link')) {
        this.quill.keyboard.addBinding({ key: 'K', shortKey: true }, function (range, context) {
          toolbar.handlers['link'].call(toolbar, !context.format.link);
        });
      }
    }
  }]);

  return SnowTheme;
}(_base2.default);

SnowTheme.DEFAULTS = (0, _extend2.default)(true, {}, _base2.default.DEFAULTS, {
  modules: {
    toolbar: {
      handlers: {
        link: function link(value) {
          if (value) {
            var range = this.quill.getSelection();
            if (range == null || range.length == 0) return;
            var preview = this.quill.getText(range);
            if (/^\S+@\S+\.\S+$/.test(preview) && preview.indexOf('mailto:') !== 0) {
              preview = 'mailto:' + preview;
            }
            var tooltip = this.quill.theme.tooltip;
            tooltip.edit('link', preview);
          } else {
            this.quill.format('link', false);
          }
        }
      }
    }
  }
});

var SnowTooltip = function (_BaseTooltip) {
  _inherits(SnowTooltip, _BaseTooltip);

  function SnowTooltip(quill, bounds) {
    _classCallCheck(this, SnowTooltip);

    var _this2 = _possibleConstructorReturn(this, (SnowTooltip.__proto__ || Object.getPrototypeOf(SnowTooltip)).call(this, quill, bounds));

    _this2.preview = _this2.root.querySelector('a.ql-preview');
    return _this2;
  }

  _createClass(SnowTooltip, [{
    key: 'listen',
    value: function listen() {
      var _this3 = this;

      _get(SnowTooltip.prototype.__proto__ || Object.getPrototypeOf(SnowTooltip.prototype), 'listen', this).call(this);
      this.root.querySelector('a.ql-action').addEventListener('click', function (event) {
        if (_this3.root.classList.contains('ql-editing')) {
          _this3.save();
        } else {
          _this3.edit('link', _this3.preview.textContent);
        }
        event.preventDefault();
      });
      this.root.querySelector('a.ql-remove').addEventListener('click', function (event) {
        if (_this3.linkRange != null) {
          var range = _this3.linkRange;
          _this3.restoreFocus();
          _this3.quill.formatText(range, 'link', false, _emitter2.default.sources.USER);
          delete _this3.linkRange;
        }
        event.preventDefault();
        _this3.hide();
      });
      this.quill.on(_emitter2.default.events.SELECTION_CHANGE, function (range, oldRange, source) {
        if (range == null) return;
        if (range.length === 0 && source === _emitter2.default.sources.USER) {
          var _quill$scroll$descend = _this3.quill.scroll.descendant(_link2.default, range.index),
              _quill$scroll$descend2 = _slicedToArray(_quill$scroll$descend, 2),
              link = _quill$scroll$descend2[0],
              offset = _quill$scroll$descend2[1];

          if (link != null) {
            _this3.linkRange = new _selection.Range(range.index - offset, link.length());
            var preview = _link2.default.formats(link.domNode);
            _this3.preview.textContent = preview;
            _this3.preview.setAttribute('href', preview);
            _this3.show();
            _this3.position(_this3.quill.getBounds(_this3.linkRange));
            return;
          }
        } else {
          delete _this3.linkRange;
        }
        _this3.hide();
      });
    }
  }, {
    key: 'show',
    value: function show() {
      _get(SnowTooltip.prototype.__proto__ || Object.getPrototypeOf(SnowTooltip.prototype), 'show', this).call(this);
      this.root.removeAttribute('data-mode');
    }
  }]);

  return SnowTooltip;
}(_base.BaseTooltip);

SnowTooltip.TEMPLATE = ['<a class="ql-preview" target="_blank" href="about:blank"></a>', '<input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL">', '<a class="ql-action"></a>', '<a class="ql-remove"></a>'].join('');

exports.default = SnowTheme;

/***/ }),
/* 63 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _core = __webpack_require__(29);

var _core2 = _interopRequireDefault(_core);

var _align = __webpack_require__(36);

var _direction = __webpack_require__(38);

var _indent = __webpack_require__(64);

var _blockquote = __webpack_require__(65);

var _blockquote2 = _interopRequireDefault(_blockquote);

var _header = __webpack_require__(66);

var _header2 = _interopRequireDefault(_header);

var _list = __webpack_require__(67);

var _list2 = _interopRequireDefault(_list);

var _background = __webpack_require__(37);

var _color = __webpack_require__(26);

var _font = __webpack_require__(39);

var _size = __webpack_require__(40);

var _bold = __webpack_require__(56);

var _bold2 = _interopRequireDefault(_bold);

var _italic = __webpack_require__(68);

var _italic2 = _interopRequireDefault(_italic);

var _link = __webpack_require__(27);

var _link2 = _interopRequireDefault(_link);

var _script = __webpack_require__(69);

var _script2 = _interopRequireDefault(_script);

var _strike = __webpack_require__(70);

var _strike2 = _interopRequireDefault(_strike);

var _underline = __webpack_require__(71);

var _underline2 = _interopRequireDefault(_underline);

var _image = __webpack_require__(72);

var _image2 = _interopRequireDefault(_image);

var _video = __webpack_require__(73);

var _video2 = _interopRequireDefault(_video);

var _code = __webpack_require__(13);

var _code2 = _interopRequireDefault(_code);

var _formula = __webpack_require__(74);

var _formula2 = _interopRequireDefault(_formula);

var _syntax = __webpack_require__(75);

var _syntax2 = _interopRequireDefault(_syntax);

var _toolbar = __webpack_require__(57);

var _toolbar2 = _interopRequireDefault(_toolbar);

var _icons = __webpack_require__(41);

var _icons2 = _interopRequireDefault(_icons);

var _picker = __webpack_require__(28);

var _picker2 = _interopRequireDefault(_picker);

var _colorPicker = __webpack_require__(59);

var _colorPicker2 = _interopRequireDefault(_colorPicker);

var _iconPicker = __webpack_require__(60);

var _iconPicker2 = _interopRequireDefault(_iconPicker);

var _tooltip = __webpack_require__(61);

var _tooltip2 = _interopRequireDefault(_tooltip);

var _bubble = __webpack_require__(108);

var _bubble2 = _interopRequireDefault(_bubble);

var _snow = __webpack_require__(62);

var _snow2 = _interopRequireDefault(_snow);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

_core2.default.register({
  'attributors/attribute/direction': _direction.DirectionAttribute,

  'attributors/class/align': _align.AlignClass,
  'attributors/class/background': _background.BackgroundClass,
  'attributors/class/color': _color.ColorClass,
  'attributors/class/direction': _direction.DirectionClass,
  'attributors/class/font': _font.FontClass,
  'attributors/class/size': _size.SizeClass,

  'attributors/style/align': _align.AlignStyle,
  'attributors/style/background': _background.BackgroundStyle,
  'attributors/style/color': _color.ColorStyle,
  'attributors/style/direction': _direction.DirectionStyle,
  'attributors/style/font': _font.FontStyle,
  'attributors/style/size': _size.SizeStyle
}, true);

_core2.default.register({
  'formats/align': _align.AlignClass,
  'formats/direction': _direction.DirectionClass,
  'formats/indent': _indent.IndentClass,

  'formats/background': _background.BackgroundStyle,
  'formats/color': _color.ColorStyle,
  'formats/font': _font.FontClass,
  'formats/size': _size.SizeClass,

  'formats/blockquote': _blockquote2.default,
  'formats/code-block': _code2.default,
  'formats/header': _header2.default,
  'formats/list': _list2.default,

  'formats/bold': _bold2.default,
  'formats/code': _code.Code,
  'formats/italic': _italic2.default,
  'formats/link': _link2.default,
  'formats/script': _script2.default,
  'formats/strike': _strike2.default,
  'formats/underline': _underline2.default,

  'formats/image': _image2.default,
  'formats/video': _video2.default,

  'formats/list/item': _list.ListItem,

  'modules/formula': _formula2.default,
  'modules/syntax': _syntax2.default,
  'modules/toolbar': _toolbar2.default,

  'themes/bubble': _bubble2.default,
  'themes/snow': _snow2.default,

  'ui/icons': _icons2.default,
  'ui/picker': _picker2.default,
  'ui/icon-picker': _iconPicker2.default,
  'ui/color-picker': _colorPicker2.default,
  'ui/tooltip': _tooltip2.default
}, true);

exports.default = _core2.default;

/***/ }),
/* 64 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.IndentClass = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var IdentAttributor = function (_Parchment$Attributor) {
  _inherits(IdentAttributor, _Parchment$Attributor);

  function IdentAttributor() {
    _classCallCheck(this, IdentAttributor);

    return _possibleConstructorReturn(this, (IdentAttributor.__proto__ || Object.getPrototypeOf(IdentAttributor)).apply(this, arguments));
  }

  _createClass(IdentAttributor, [{
    key: 'add',
    value: function add(node, value) {
      if (value === '+1' || value === '-1') {
        var indent = this.value(node) || 0;
        value = value === '+1' ? indent + 1 : indent - 1;
      }
      if (value === 0) {
        this.remove(node);
        return true;
      } else {
        return _get(IdentAttributor.prototype.__proto__ || Object.getPrototypeOf(IdentAttributor.prototype), 'add', this).call(this, node, value);
      }
    }
  }, {
    key: 'canAdd',
    value: function canAdd(node, value) {
      return _get(IdentAttributor.prototype.__proto__ || Object.getPrototypeOf(IdentAttributor.prototype), 'canAdd', this).call(this, node, value) || _get(IdentAttributor.prototype.__proto__ || Object.getPrototypeOf(IdentAttributor.prototype), 'canAdd', this).call(this, node, parseInt(value));
    }
  }, {
    key: 'value',
    value: function value(node) {
      return parseInt(_get(IdentAttributor.prototype.__proto__ || Object.getPrototypeOf(IdentAttributor.prototype), 'value', this).call(this, node)) || undefined; // Don't return NaN
    }
  }]);

  return IdentAttributor;
}(_parchment2.default.Attributor.Class);

var IndentClass = new IdentAttributor('indent', 'ql-indent', {
  scope: _parchment2.default.Scope.BLOCK,
  whitelist: [1, 2, 3, 4, 5, 6, 7, 8]
});

exports.IndentClass = IndentClass;

/***/ }),
/* 65 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _block = __webpack_require__(4);

var _block2 = _interopRequireDefault(_block);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Blockquote = function (_Block) {
  _inherits(Blockquote, _Block);

  function Blockquote() {
    _classCallCheck(this, Blockquote);

    return _possibleConstructorReturn(this, (Blockquote.__proto__ || Object.getPrototypeOf(Blockquote)).apply(this, arguments));
  }

  return Blockquote;
}(_block2.default);

Blockquote.blotName = 'blockquote';
Blockquote.tagName = 'blockquote';

exports.default = Blockquote;

/***/ }),
/* 66 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _block = __webpack_require__(4);

var _block2 = _interopRequireDefault(_block);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Header = function (_Block) {
  _inherits(Header, _Block);

  function Header() {
    _classCallCheck(this, Header);

    return _possibleConstructorReturn(this, (Header.__proto__ || Object.getPrototypeOf(Header)).apply(this, arguments));
  }

  _createClass(Header, null, [{
    key: 'formats',
    value: function formats(domNode) {
      return this.tagName.indexOf(domNode.tagName) + 1;
    }
  }]);

  return Header;
}(_block2.default);

Header.blotName = 'header';
Header.tagName = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6'];

exports.default = Header;

/***/ }),
/* 67 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = exports.ListItem = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _block = __webpack_require__(4);

var _block2 = _interopRequireDefault(_block);

var _container = __webpack_require__(25);

var _container2 = _interopRequireDefault(_container);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var ListItem = function (_Block) {
  _inherits(ListItem, _Block);

  function ListItem() {
    _classCallCheck(this, ListItem);

    return _possibleConstructorReturn(this, (ListItem.__proto__ || Object.getPrototypeOf(ListItem)).apply(this, arguments));
  }

  _createClass(ListItem, [{
    key: 'format',
    value: function format(name, value) {
      if (name === List.blotName && !value) {
        this.replaceWith(_parchment2.default.create(this.statics.scope));
      } else {
        _get(ListItem.prototype.__proto__ || Object.getPrototypeOf(ListItem.prototype), 'format', this).call(this, name, value);
      }
    }
  }, {
    key: 'remove',
    value: function remove() {
      if (this.prev == null && this.next == null) {
        this.parent.remove();
      } else {
        _get(ListItem.prototype.__proto__ || Object.getPrototypeOf(ListItem.prototype), 'remove', this).call(this);
      }
    }
  }, {
    key: 'replaceWith',
    value: function replaceWith(name, value) {
      this.parent.isolate(this.offset(this.parent), this.length());
      if (name === this.parent.statics.blotName) {
        this.parent.replaceWith(name, value);
        return this;
      } else {
        this.parent.unwrap();
        return _get(ListItem.prototype.__proto__ || Object.getPrototypeOf(ListItem.prototype), 'replaceWith', this).call(this, name, value);
      }
    }
  }], [{
    key: 'formats',
    value: function formats(domNode) {
      return domNode.tagName === this.tagName ? undefined : _get(ListItem.__proto__ || Object.getPrototypeOf(ListItem), 'formats', this).call(this, domNode);
    }
  }]);

  return ListItem;
}(_block2.default);

ListItem.blotName = 'list-item';
ListItem.tagName = 'LI';

var List = function (_Container) {
  _inherits(List, _Container);

  _createClass(List, null, [{
    key: 'create',
    value: function create(value) {
      var tagName = value === 'ordered' ? 'OL' : 'UL';
      var node = _get(List.__proto__ || Object.getPrototypeOf(List), 'create', this).call(this, tagName);
      if (value === 'checked' || value === 'unchecked') {
        node.setAttribute('data-checked', value === 'checked');
      }
      return node;
    }
  }, {
    key: 'formats',
    value: function formats(domNode) {
      if (domNode.tagName === 'OL') return 'ordered';
      if (domNode.tagName === 'UL') {
        if (domNode.hasAttribute('data-checked')) {
          return domNode.getAttribute('data-checked') === 'true' ? 'checked' : 'unchecked';
        } else {
          return 'bullet';
        }
      }
      return undefined;
    }
  }]);

  function List(domNode) {
    _classCallCheck(this, List);

    var _this2 = _possibleConstructorReturn(this, (List.__proto__ || Object.getPrototypeOf(List)).call(this, domNode));

    var listEventHandler = function listEventHandler(e) {
      if (e.target.parentNode !== domNode) return;
      var format = _this2.statics.formats(domNode);
      var blot = _parchment2.default.find(e.target);
      if (format === 'checked') {
        blot.format('list', 'unchecked');
      } else if (format === 'unchecked') {
        blot.format('list', 'checked');
      }
    };

    domNode.addEventListener('touchstart', listEventHandler);
    domNode.addEventListener('mousedown', listEventHandler);
    return _this2;
  }

  _createClass(List, [{
    key: 'format',
    value: function format(name, value) {
      if (this.children.length > 0) {
        this.children.tail.format(name, value);
      }
    }
  }, {
    key: 'formats',
    value: function formats() {
      // We don't inherit from FormatBlot
      return _defineProperty({}, this.statics.blotName, this.statics.formats(this.domNode));
    }
  }, {
    key: 'insertBefore',
    value: function insertBefore(blot, ref) {
      if (blot instanceof ListItem) {
        _get(List.prototype.__proto__ || Object.getPrototypeOf(List.prototype), 'insertBefore', this).call(this, blot, ref);
      } else {
        var index = ref == null ? this.length() : ref.offset(this);
        var after = this.split(index);
        after.parent.insertBefore(blot, after);
      }
    }
  }, {
    key: 'optimize',
    value: function optimize(context) {
      _get(List.prototype.__proto__ || Object.getPrototypeOf(List.prototype), 'optimize', this).call(this, context);
      var next = this.next;
      if (next != null && next.prev === this && next.statics.blotName === this.statics.blotName && next.domNode.tagName === this.domNode.tagName && next.domNode.getAttribute('data-checked') === this.domNode.getAttribute('data-checked')) {
        next.moveChildren(this);
        next.remove();
      }
    }
  }, {
    key: 'replace',
    value: function replace(target) {
      if (target.statics.blotName !== this.statics.blotName) {
        var item = _parchment2.default.create(this.statics.defaultChild);
        target.moveChildren(item);
        this.appendChild(item);
      }
      _get(List.prototype.__proto__ || Object.getPrototypeOf(List.prototype), 'replace', this).call(this, target);
    }
  }]);

  return List;
}(_container2.default);

List.blotName = 'list';
List.scope = _parchment2.default.Scope.BLOCK_BLOT;
List.tagName = ['OL', 'UL'];
List.defaultChild = 'list-item';
List.allowedChildren = [ListItem];

exports.ListItem = ListItem;
exports.default = List;

/***/ }),
/* 68 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _bold = __webpack_require__(56);

var _bold2 = _interopRequireDefault(_bold);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Italic = function (_Bold) {
  _inherits(Italic, _Bold);

  function Italic() {
    _classCallCheck(this, Italic);

    return _possibleConstructorReturn(this, (Italic.__proto__ || Object.getPrototypeOf(Italic)).apply(this, arguments));
  }

  return Italic;
}(_bold2.default);

Italic.blotName = 'italic';
Italic.tagName = ['EM', 'I'];

exports.default = Italic;

/***/ }),
/* 69 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _inline = __webpack_require__(6);

var _inline2 = _interopRequireDefault(_inline);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Script = function (_Inline) {
  _inherits(Script, _Inline);

  function Script() {
    _classCallCheck(this, Script);

    return _possibleConstructorReturn(this, (Script.__proto__ || Object.getPrototypeOf(Script)).apply(this, arguments));
  }

  _createClass(Script, null, [{
    key: 'create',
    value: function create(value) {
      if (value === 'super') {
        return document.createElement('sup');
      } else if (value === 'sub') {
        return document.createElement('sub');
      } else {
        return _get(Script.__proto__ || Object.getPrototypeOf(Script), 'create', this).call(this, value);
      }
    }
  }, {
    key: 'formats',
    value: function formats(domNode) {
      if (domNode.tagName === 'SUB') return 'sub';
      if (domNode.tagName === 'SUP') return 'super';
      return undefined;
    }
  }]);

  return Script;
}(_inline2.default);

Script.blotName = 'script';
Script.tagName = ['SUB', 'SUP'];

exports.default = Script;

/***/ }),
/* 70 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _inline = __webpack_require__(6);

var _inline2 = _interopRequireDefault(_inline);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Strike = function (_Inline) {
  _inherits(Strike, _Inline);

  function Strike() {
    _classCallCheck(this, Strike);

    return _possibleConstructorReturn(this, (Strike.__proto__ || Object.getPrototypeOf(Strike)).apply(this, arguments));
  }

  return Strike;
}(_inline2.default);

Strike.blotName = 'strike';
Strike.tagName = 'S';

exports.default = Strike;

/***/ }),
/* 71 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _inline = __webpack_require__(6);

var _inline2 = _interopRequireDefault(_inline);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Underline = function (_Inline) {
  _inherits(Underline, _Inline);

  function Underline() {
    _classCallCheck(this, Underline);

    return _possibleConstructorReturn(this, (Underline.__proto__ || Object.getPrototypeOf(Underline)).apply(this, arguments));
  }

  return Underline;
}(_inline2.default);

Underline.blotName = 'underline';
Underline.tagName = 'U';

exports.default = Underline;

/***/ }),
/* 72 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _link = __webpack_require__(27);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var ATTRIBUTES = ['alt', 'height', 'width'];

var Image = function (_Parchment$Embed) {
  _inherits(Image, _Parchment$Embed);

  function Image() {
    _classCallCheck(this, Image);

    return _possibleConstructorReturn(this, (Image.__proto__ || Object.getPrototypeOf(Image)).apply(this, arguments));
  }

  _createClass(Image, [{
    key: 'format',
    value: function format(name, value) {
      if (ATTRIBUTES.indexOf(name) > -1) {
        if (value) {
          this.domNode.setAttribute(name, value);
        } else {
          this.domNode.removeAttribute(name);
        }
      } else {
        _get(Image.prototype.__proto__ || Object.getPrototypeOf(Image.prototype), 'format', this).call(this, name, value);
      }
    }
  }], [{
    key: 'create',
    value: function create(value) {
      var node = _get(Image.__proto__ || Object.getPrototypeOf(Image), 'create', this).call(this, value);
      if (typeof value === 'string') {
        node.setAttribute('src', this.sanitize(value));
      }
      return node;
    }
  }, {
    key: 'formats',
    value: function formats(domNode) {
      return ATTRIBUTES.reduce(function (formats, attribute) {
        if (domNode.hasAttribute(attribute)) {
          formats[attribute] = domNode.getAttribute(attribute);
        }
        return formats;
      }, {});
    }
  }, {
    key: 'match',
    value: function match(url) {
      return (/\.(jpe?g|gif|png)$/.test(url) || /^data:image\/.+;base64/.test(url)
      );
    }
  }, {
    key: 'sanitize',
    value: function sanitize(url) {
      return (0, _link.sanitize)(url, ['http', 'https', 'data']) ? url : '//:0';
    }
  }, {
    key: 'value',
    value: function value(domNode) {
      return domNode.getAttribute('src');
    }
  }]);

  return Image;
}(_parchment2.default.Embed);

Image.blotName = 'image';
Image.tagName = 'IMG';

exports.default = Image;

/***/ }),
/* 73 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _block = __webpack_require__(4);

var _link = __webpack_require__(27);

var _link2 = _interopRequireDefault(_link);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var ATTRIBUTES = ['height', 'width'];

var Video = function (_BlockEmbed) {
  _inherits(Video, _BlockEmbed);

  function Video() {
    _classCallCheck(this, Video);

    return _possibleConstructorReturn(this, (Video.__proto__ || Object.getPrototypeOf(Video)).apply(this, arguments));
  }

  _createClass(Video, [{
    key: 'format',
    value: function format(name, value) {
      if (ATTRIBUTES.indexOf(name) > -1) {
        if (value) {
          this.domNode.setAttribute(name, value);
        } else {
          this.domNode.removeAttribute(name);
        }
      } else {
        _get(Video.prototype.__proto__ || Object.getPrototypeOf(Video.prototype), 'format', this).call(this, name, value);
      }
    }
  }], [{
    key: 'create',
    value: function create(value) {
      var node = _get(Video.__proto__ || Object.getPrototypeOf(Video), 'create', this).call(this, value);
      node.setAttribute('frameborder', '0');
      node.setAttribute('allowfullscreen', true);
      node.setAttribute('src', this.sanitize(value));
      return node;
    }
  }, {
    key: 'formats',
    value: function formats(domNode) {
      return ATTRIBUTES.reduce(function (formats, attribute) {
        if (domNode.hasAttribute(attribute)) {
          formats[attribute] = domNode.getAttribute(attribute);
        }
        return formats;
      }, {});
    }
  }, {
    key: 'sanitize',
    value: function sanitize(url) {
      return _link2.default.sanitize(url);
    }
  }, {
    key: 'value',
    value: function value(domNode) {
      return domNode.getAttribute('src');
    }
  }]);

  return Video;
}(_block.BlockEmbed);

Video.blotName = 'video';
Video.className = 'ql-video';
Video.tagName = 'IFRAME';

exports.default = Video;

/***/ }),
/* 74 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = exports.FormulaBlot = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _embed = __webpack_require__(35);

var _embed2 = _interopRequireDefault(_embed);

var _quill = __webpack_require__(5);

var _quill2 = _interopRequireDefault(_quill);

var _module = __webpack_require__(9);

var _module2 = _interopRequireDefault(_module);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var FormulaBlot = function (_Embed) {
  _inherits(FormulaBlot, _Embed);

  function FormulaBlot() {
    _classCallCheck(this, FormulaBlot);

    return _possibleConstructorReturn(this, (FormulaBlot.__proto__ || Object.getPrototypeOf(FormulaBlot)).apply(this, arguments));
  }

  _createClass(FormulaBlot, null, [{
    key: 'create',
    value: function create(value) {
      var node = _get(FormulaBlot.__proto__ || Object.getPrototypeOf(FormulaBlot), 'create', this).call(this, value);
      if (typeof value === 'string') {
        window.katex.render(value, node, {
          throwOnError: false,
          errorColor: '#f00'
        });
        node.setAttribute('data-value', value);
      }
      return node;
    }
  }, {
    key: 'value',
    value: function value(domNode) {
      return domNode.getAttribute('data-value');
    }
  }]);

  return FormulaBlot;
}(_embed2.default);

FormulaBlot.blotName = 'formula';
FormulaBlot.className = 'ql-formula';
FormulaBlot.tagName = 'SPAN';

var Formula = function (_Module) {
  _inherits(Formula, _Module);

  _createClass(Formula, null, [{
    key: 'register',
    value: function register() {
      _quill2.default.register(FormulaBlot, true);
    }
  }]);

  function Formula() {
    _classCallCheck(this, Formula);

    var _this2 = _possibleConstructorReturn(this, (Formula.__proto__ || Object.getPrototypeOf(Formula)).call(this));

    if (window.katex == null) {
      throw new Error('Formula module requires KaTeX.');
    }
    return _this2;
  }

  return Formula;
}(_module2.default);

exports.FormulaBlot = FormulaBlot;
exports.default = Formula;

/***/ }),
/* 75 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = exports.CodeToken = exports.CodeBlock = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _parchment = __webpack_require__(0);

var _parchment2 = _interopRequireDefault(_parchment);

var _quill = __webpack_require__(5);

var _quill2 = _interopRequireDefault(_quill);

var _module = __webpack_require__(9);

var _module2 = _interopRequireDefault(_module);

var _code = __webpack_require__(13);

var _code2 = _interopRequireDefault(_code);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var SyntaxCodeBlock = function (_CodeBlock) {
  _inherits(SyntaxCodeBlock, _CodeBlock);

  function SyntaxCodeBlock() {
    _classCallCheck(this, SyntaxCodeBlock);

    return _possibleConstructorReturn(this, (SyntaxCodeBlock.__proto__ || Object.getPrototypeOf(SyntaxCodeBlock)).apply(this, arguments));
  }

  _createClass(SyntaxCodeBlock, [{
    key: 'replaceWith',
    value: function replaceWith(block) {
      this.domNode.textContent = this.domNode.textContent;
      this.attach();
      _get(SyntaxCodeBlock.prototype.__proto__ || Object.getPrototypeOf(SyntaxCodeBlock.prototype), 'replaceWith', this).call(this, block);
    }
  }, {
    key: 'highlight',
    value: function highlight(_highlight) {
      var text = this.domNode.textContent;
      if (this.cachedText !== text) {
        if (text.trim().length > 0 || this.cachedText == null) {
          this.domNode.innerHTML = _highlight(text);
          this.domNode.normalize();
          this.attach();
        }
        this.cachedText = text;
      }
    }
  }]);

  return SyntaxCodeBlock;
}(_code2.default);

SyntaxCodeBlock.className = 'ql-syntax';

var CodeToken = new _parchment2.default.Attributor.Class('token', 'hljs', {
  scope: _parchment2.default.Scope.INLINE
});

var Syntax = function (_Module) {
  _inherits(Syntax, _Module);

  _createClass(Syntax, null, [{
    key: 'register',
    value: function register() {
      _quill2.default.register(CodeToken, true);
      _quill2.default.register(SyntaxCodeBlock, true);
    }
  }]);

  function Syntax(quill, options) {
    _classCallCheck(this, Syntax);

    var _this2 = _possibleConstructorReturn(this, (Syntax.__proto__ || Object.getPrototypeOf(Syntax)).call(this, quill, options));

    if (typeof _this2.options.highlight !== 'function') {
      throw new Error('Syntax module requires highlight.js. Please include the library on the page before Quill.');
    }
    var timer = null;
    _this2.quill.on(_quill2.default.events.SCROLL_OPTIMIZE, function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        _this2.highlight();
        timer = null;
      }, _this2.options.interval);
    });
    _this2.highlight();
    return _this2;
  }

  _createClass(Syntax, [{
    key: 'highlight',
    value: function highlight() {
      var _this3 = this;

      if (this.quill.selection.composing) return;
      this.quill.update(_quill2.default.sources.USER);
      var range = this.quill.getSelection();
      this.quill.scroll.descendants(SyntaxCodeBlock).forEach(function (code) {
        code.highlight(_this3.options.highlight);
      });
      this.quill.update(_quill2.default.sources.SILENT);
      if (range != null) {
        this.quill.setSelection(range, _quill2.default.sources.SILENT);
      }
    }
  }]);

  return Syntax;
}(_module2.default);

Syntax.DEFAULTS = {
  highlight: function () {
    if (window.hljs == null) return null;
    return function (text) {
      var result = window.hljs.highlightAuto(text);
      return result.value;
    };
  }(),
  interval: 1000
};

exports.CodeBlock = SyntaxCodeBlock;
exports.CodeToken = CodeToken;
exports.default = Syntax;

/***/ }),
/* 76 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <line class=ql-stroke x1=3 x2=15 y1=9 y2=9></line> <line class=ql-stroke x1=3 x2=13 y1=14 y2=14></line> <line class=ql-stroke x1=3 x2=9 y1=4 y2=4></line> </svg>";

/***/ }),
/* 77 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <line class=ql-stroke x1=15 x2=3 y1=9 y2=9></line> <line class=ql-stroke x1=14 x2=4 y1=14 y2=14></line> <line class=ql-stroke x1=12 x2=6 y1=4 y2=4></line> </svg>";

/***/ }),
/* 78 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <line class=ql-stroke x1=15 x2=3 y1=9 y2=9></line> <line class=ql-stroke x1=15 x2=5 y1=14 y2=14></line> <line class=ql-stroke x1=15 x2=9 y1=4 y2=4></line> </svg>";

/***/ }),
/* 79 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <line class=ql-stroke x1=15 x2=3 y1=9 y2=9></line> <line class=ql-stroke x1=15 x2=3 y1=14 y2=14></line> <line class=ql-stroke x1=15 x2=3 y1=4 y2=4></line> </svg>";

/***/ }),
/* 80 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <g class=\"ql-fill ql-color-label\"> <polygon points=\"6 6.868 6 6 5 6 5 7 5.942 7 6 6.868\"></polygon> <rect height=1 width=1 x=4 y=4></rect> <polygon points=\"6.817 5 6 5 6 6 6.38 6 6.817 5\"></polygon> <rect height=1 width=1 x=2 y=6></rect> <rect height=1 width=1 x=3 y=5></rect> <rect height=1 width=1 x=4 y=7></rect> <polygon points=\"4 11.439 4 11 3 11 3 12 3.755 12 4 11.439\"></polygon> <rect height=1 width=1 x=2 y=12></rect> <rect height=1 width=1 x=2 y=9></rect> <rect height=1 width=1 x=2 y=15></rect> <polygon points=\"4.63 10 4 10 4 11 4.192 11 4.63 10\"></polygon> <rect height=1 width=1 x=3 y=8></rect> <path d=M10.832,4.2L11,4.582V4H10.708A1.948,1.948,0,0,1,10.832,4.2Z></path> <path d=M7,4.582L7.168,4.2A1.929,1.929,0,0,1,7.292,4H7V4.582Z></path> <path d=M8,13H7.683l-0.351.8a1.933,1.933,0,0,1-.124.2H8V13Z></path> <rect height=1 width=1 x=12 y=2></rect> <rect height=1 width=1 x=11 y=3></rect> <path d=M9,3H8V3.282A1.985,1.985,0,0,1,9,3Z></path> <rect height=1 width=1 x=2 y=3></rect> <rect height=1 width=1 x=6 y=2></rect> <rect height=1 width=1 x=3 y=2></rect> <rect height=1 width=1 x=5 y=3></rect> <rect height=1 width=1 x=9 y=2></rect> <rect height=1 width=1 x=15 y=14></rect> <polygon points=\"13.447 10.174 13.469 10.225 13.472 10.232 13.808 11 14 11 14 10 13.37 10 13.447 10.174\"></polygon> <rect height=1 width=1 x=13 y=7></rect> <rect height=1 width=1 x=15 y=5></rect> <rect height=1 width=1 x=14 y=6></rect> <rect height=1 width=1 x=15 y=8></rect> <rect height=1 width=1 x=14 y=9></rect> <path d=M3.775,14H3v1H4V14.314A1.97,1.97,0,0,1,3.775,14Z></path> <rect height=1 width=1 x=14 y=3></rect> <polygon points=\"12 6.868 12 6 11.62 6 12 6.868\"></polygon> <rect height=1 width=1 x=15 y=2></rect> <rect height=1 width=1 x=12 y=5></rect> <rect height=1 width=1 x=13 y=4></rect> <polygon points=\"12.933 9 13 9 13 8 12.495 8 12.933 9\"></polygon> <rect height=1 width=1 x=9 y=14></rect> <rect height=1 width=1 x=8 y=15></rect> <path d=M6,14.926V15H7V14.316A1.993,1.993,0,0,1,6,14.926Z></path> <rect height=1 width=1 x=5 y=15></rect> <path d=M10.668,13.8L10.317,13H10v1h0.792A1.947,1.947,0,0,1,10.668,13.8Z></path> <rect height=1 width=1 x=11 y=15></rect> <path d=M14.332,12.2a1.99,1.99,0,0,1,.166.8H15V12H14.245Z></path> <rect height=1 width=1 x=14 y=15></rect> <rect height=1 width=1 x=15 y=11></rect> </g> <polyline class=ql-stroke points=\"5.5 13 9 5 12.5 13\"></polyline> <line class=ql-stroke x1=11.63 x2=6.38 y1=11 y2=11></line> </svg>";

/***/ }),
/* 81 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <rect class=\"ql-fill ql-stroke\" height=3 width=3 x=4 y=5></rect> <rect class=\"ql-fill ql-stroke\" height=3 width=3 x=11 y=5></rect> <path class=\"ql-even ql-fill ql-stroke\" d=M7,8c0,4.031-3,5-3,5></path> <path class=\"ql-even ql-fill ql-stroke\" d=M14,8c0,4.031-3,5-3,5></path> </svg>";

/***/ }),
/* 82 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <path class=ql-stroke d=M5,4H9.5A2.5,2.5,0,0,1,12,6.5v0A2.5,2.5,0,0,1,9.5,9H5A0,0,0,0,1,5,9V4A0,0,0,0,1,5,4Z></path> <path class=ql-stroke d=M5,9h5.5A2.5,2.5,0,0,1,13,11.5v0A2.5,2.5,0,0,1,10.5,14H5a0,0,0,0,1,0,0V9A0,0,0,0,1,5,9Z></path> </svg>";

/***/ }),
/* 83 */
/***/ (function(module, exports) {

module.exports = "<svg class=\"\" viewbox=\"0 0 18 18\"> <line class=ql-stroke x1=5 x2=13 y1=3 y2=3></line> <line class=ql-stroke x1=6 x2=9.35 y1=12 y2=3></line> <line class=ql-stroke x1=11 x2=15 y1=11 y2=15></line> <line class=ql-stroke x1=15 x2=11 y1=11 y2=15></line> <rect class=ql-fill height=1 rx=0.5 ry=0.5 width=7 x=2 y=14></rect> </svg>";

/***/ }),
/* 84 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <line class=\"ql-color-label ql-stroke ql-transparent\" x1=3 x2=15 y1=15 y2=15></line> <polyline class=ql-stroke points=\"5.5 11 9 3 12.5 11\"></polyline> <line class=ql-stroke x1=11.63 x2=6.38 y1=9 y2=9></line> </svg>";

/***/ }),
/* 85 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <polygon class=\"ql-stroke ql-fill\" points=\"3 11 5 9 3 7 3 11\"></polygon> <line class=\"ql-stroke ql-fill\" x1=15 x2=11 y1=4 y2=4></line> <path class=ql-fill d=M11,3a3,3,0,0,0,0,6h1V3H11Z></path> <rect class=ql-fill height=11 width=1 x=11 y=4></rect> <rect class=ql-fill height=11 width=1 x=13 y=4></rect> </svg>";

/***/ }),
/* 86 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <polygon class=\"ql-stroke ql-fill\" points=\"15 12 13 10 15 8 15 12\"></polygon> <line class=\"ql-stroke ql-fill\" x1=9 x2=5 y1=4 y2=4></line> <path class=ql-fill d=M5,3A3,3,0,0,0,5,9H6V3H5Z></path> <rect class=ql-fill height=11 width=1 x=5 y=4></rect> <rect class=ql-fill height=11 width=1 x=7 y=4></rect> </svg>";

/***/ }),
/* 87 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <path class=ql-fill d=M14,16H4a1,1,0,0,1,0-2H14A1,1,0,0,1,14,16Z /> <path class=ql-fill d=M14,4H4A1,1,0,0,1,4,2H14A1,1,0,0,1,14,4Z /> <rect class=ql-fill x=3 y=6 width=12 height=6 rx=1 ry=1 /> </svg>";

/***/ }),
/* 88 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <path class=ql-fill d=M13,16H5a1,1,0,0,1,0-2h8A1,1,0,0,1,13,16Z /> <path class=ql-fill d=M13,4H5A1,1,0,0,1,5,2h8A1,1,0,0,1,13,4Z /> <rect class=ql-fill x=2 y=6 width=14 height=6 rx=1 ry=1 /> </svg>";

/***/ }),
/* 89 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <path class=ql-fill d=M15,8H13a1,1,0,0,1,0-2h2A1,1,0,0,1,15,8Z /> <path class=ql-fill d=M15,12H13a1,1,0,0,1,0-2h2A1,1,0,0,1,15,12Z /> <path class=ql-fill d=M15,16H5a1,1,0,0,1,0-2H15A1,1,0,0,1,15,16Z /> <path class=ql-fill d=M15,4H5A1,1,0,0,1,5,2H15A1,1,0,0,1,15,4Z /> <rect class=ql-fill x=2 y=6 width=8 height=6 rx=1 ry=1 /> </svg>";

/***/ }),
/* 90 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <path class=ql-fill d=M5,8H3A1,1,0,0,1,3,6H5A1,1,0,0,1,5,8Z /> <path class=ql-fill d=M5,12H3a1,1,0,0,1,0-2H5A1,1,0,0,1,5,12Z /> <path class=ql-fill d=M13,16H3a1,1,0,0,1,0-2H13A1,1,0,0,1,13,16Z /> <path class=ql-fill d=M13,4H3A1,1,0,0,1,3,2H13A1,1,0,0,1,13,4Z /> <rect class=ql-fill x=8 y=6 width=8 height=6 rx=1 ry=1 transform=\"translate(24 18) rotate(-180)\"/> </svg>";

/***/ }),
/* 91 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <path class=ql-fill d=M11.759,2.482a2.561,2.561,0,0,0-3.53.607A7.656,7.656,0,0,0,6.8,6.2C6.109,9.188,5.275,14.677,4.15,14.927a1.545,1.545,0,0,0-1.3-.933A0.922,0.922,0,0,0,2,15.036S1.954,16,4.119,16s3.091-2.691,3.7-5.553c0.177-.826.36-1.726,0.554-2.6L8.775,6.2c0.381-1.421.807-2.521,1.306-2.676a1.014,1.014,0,0,0,1.02.56A0.966,0.966,0,0,0,11.759,2.482Z></path> <rect class=ql-fill height=1.6 rx=0.8 ry=0.8 width=5 x=5.15 y=6.2></rect> <path class=ql-fill d=M13.663,12.027a1.662,1.662,0,0,1,.266-0.276q0.193,0.069.456,0.138a2.1,2.1,0,0,0,.535.069,1.075,1.075,0,0,0,.767-0.3,1.044,1.044,0,0,0,.314-0.8,0.84,0.84,0,0,0-.238-0.619,0.8,0.8,0,0,0-.594-0.239,1.154,1.154,0,0,0-.781.3,4.607,4.607,0,0,0-.781,1q-0.091.15-.218,0.346l-0.246.38c-0.068-.288-0.137-0.582-0.212-0.885-0.459-1.847-2.494-.984-2.941-0.8-0.482.2-.353,0.647-0.094,0.529a0.869,0.869,0,0,1,1.281.585c0.217,0.751.377,1.436,0.527,2.038a5.688,5.688,0,0,1-.362.467,2.69,2.69,0,0,1-.264.271q-0.221-.08-0.471-0.147a2.029,2.029,0,0,0-.522-0.066,1.079,1.079,0,0,0-.768.3A1.058,1.058,0,0,0,9,15.131a0.82,0.82,0,0,0,.832.852,1.134,1.134,0,0,0,.787-0.3,5.11,5.11,0,0,0,.776-0.993q0.141-.219.215-0.34c0.046-.076.122-0.194,0.223-0.346a2.786,2.786,0,0,0,.918,1.726,2.582,2.582,0,0,0,2.376-.185c0.317-.181.212-0.565,0-0.494A0.807,0.807,0,0,1,14.176,15a5.159,5.159,0,0,1-.913-2.446l0,0Q13.487,12.24,13.663,12.027Z></path> </svg>";

/***/ }),
/* 92 */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 18 18\"> <path class=ql-fill d=M10,4V14a1,1,0,0,1-2,0V10H3v4a1,1,0,0,1-2,0V4A1,1,0,0,1,3,4V8H8V4a1,1,0,0,1,2,0Zm6.06787,9.209H14.98975V7.59863a.54085.54085,0,0,0-.605-.60547h-.62744a1.01119,1.01119,0,0,0-.748.29688L11.645,8.56641a.5435.5435,0,0,0-.022.8584l.28613.30762a.53861.53861,0,0,0,.84717.0332l.09912-.08789a1.2137,1.2137,0,0,0,.2417-.35254h.02246s-.01123.30859-.01123.60547V13.209H12.041a.54085.54085,0,0,0-.605.60547v.43945a.54085.54085,0,0,0,.605.60547h4.02686a.54085.54085,0,0,0,.605-.60547v-.43945A.54085.54085,0,0,0,16.06787,13.209Z /> </svg>";

/***/ }),
/* 93 */
/***/ (function(module, exports) {

module.exports = "<svg viewBox=\"0 0 18 18\"> <path class=ql-fill d=M16.73975,13.81445v.43945a.54085.54085,0,0,1-.605.60547H11.855a.58392.58392,0,0,1-.64893-.60547V14.0127c0-2.90527,3.39941-3.42187,3.39941-4.55469a.77675.77675,0,0,0-.84717-.78125,1.17684,1.17684,0,0,0-.83594.38477c-.2749.26367-.561.374-.85791.13184l-.4292-.34082c-.30811-.24219-.38525-.51758-.1543-.81445a2.97155,2.97155,0,0,1,2.45361-1.17676,2.45393,2.45393,0,0,1,2.68408,2.40918c0,2.45312-3.1792,2.92676-3.27832,3.93848h2.79443A.54085.54085,0,0,1,16.73975,13.81445ZM9,3A.99974.99974,0,0,0,8,4V8H3V4A1,1,0,0,0,1,4V14a1,1,0,0,0,2,0V10H8v4a1,1,0,0,0,2,0V4A.99974.99974,0,0,0,9,3Z /> </svg>";

/***/ }),
/* 94 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <line class=ql-stroke x1=7 x2=13 y1=4 y2=4></line> <line class=ql-stroke x1=5 x2=11 y1=14 y2=14></line> <line class=ql-stroke x1=8 x2=10 y1=14 y2=4></line> </svg>";

/***/ }),
/* 95 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <rect class=ql-stroke height=10 width=12 x=3 y=4></rect> <circle class=ql-fill cx=6 cy=7 r=1></circle> <polyline class=\"ql-even ql-fill\" points=\"5 12 5 11 7 9 8 10 11 7 13 9 13 12 5 12\"></polyline> </svg>";

/***/ }),
/* 96 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <line class=ql-stroke x1=3 x2=15 y1=14 y2=14></line> <line class=ql-stroke x1=3 x2=15 y1=4 y2=4></line> <line class=ql-stroke x1=9 x2=15 y1=9 y2=9></line> <polyline class=\"ql-fill ql-stroke\" points=\"3 7 3 11 5 9 3 7\"></polyline> </svg>";

/***/ }),
/* 97 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <line class=ql-stroke x1=3 x2=15 y1=14 y2=14></line> <line class=ql-stroke x1=3 x2=15 y1=4 y2=4></line> <line class=ql-stroke x1=9 x2=15 y1=9 y2=9></line> <polyline class=ql-stroke points=\"5 7 5 11 3 9 5 7\"></polyline> </svg>";

/***/ }),
/* 98 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <line class=ql-stroke x1=7 x2=11 y1=7 y2=11></line> <path class=\"ql-even ql-stroke\" d=M8.9,4.577a3.476,3.476,0,0,1,.36,4.679A3.476,3.476,0,0,1,4.577,8.9C3.185,7.5,2.035,6.4,4.217,4.217S7.5,3.185,8.9,4.577Z></path> <path class=\"ql-even ql-stroke\" d=M13.423,9.1a3.476,3.476,0,0,0-4.679-.36,3.476,3.476,0,0,0,.36,4.679c1.392,1.392,2.5,2.542,4.679.36S14.815,10.5,13.423,9.1Z></path> </svg>";

/***/ }),
/* 99 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <line class=ql-stroke x1=7 x2=15 y1=4 y2=4></line> <line class=ql-stroke x1=7 x2=15 y1=9 y2=9></line> <line class=ql-stroke x1=7 x2=15 y1=14 y2=14></line> <line class=\"ql-stroke ql-thin\" x1=2.5 x2=4.5 y1=5.5 y2=5.5></line> <path class=ql-fill d=M3.5,6A0.5,0.5,0,0,1,3,5.5V3.085l-0.276.138A0.5,0.5,0,0,1,2.053,3c-0.124-.247-0.023-0.324.224-0.447l1-.5A0.5,0.5,0,0,1,4,2.5v3A0.5,0.5,0,0,1,3.5,6Z></path> <path class=\"ql-stroke ql-thin\" d=M4.5,10.5h-2c0-.234,1.85-1.076,1.85-2.234A0.959,0.959,0,0,0,2.5,8.156></path> <path class=\"ql-stroke ql-thin\" d=M2.5,14.846a0.959,0.959,0,0,0,1.85-.109A0.7,0.7,0,0,0,3.75,14a0.688,0.688,0,0,0,.6-0.736,0.959,0.959,0,0,0-1.85-.109></path> </svg>";

/***/ }),
/* 100 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <line class=ql-stroke x1=6 x2=15 y1=4 y2=4></line> <line class=ql-stroke x1=6 x2=15 y1=9 y2=9></line> <line class=ql-stroke x1=6 x2=15 y1=14 y2=14></line> <line class=ql-stroke x1=3 x2=3 y1=4 y2=4></line> <line class=ql-stroke x1=3 x2=3 y1=9 y2=9></line> <line class=ql-stroke x1=3 x2=3 y1=14 y2=14></line> </svg>";

/***/ }),
/* 101 */
/***/ (function(module, exports) {

module.exports = "<svg class=\"\" viewbox=\"0 0 18 18\"> <line class=ql-stroke x1=9 x2=15 y1=4 y2=4></line> <polyline class=ql-stroke points=\"3 4 4 5 6 3\"></polyline> <line class=ql-stroke x1=9 x2=15 y1=14 y2=14></line> <polyline class=ql-stroke points=\"3 14 4 15 6 13\"></polyline> <line class=ql-stroke x1=9 x2=15 y1=9 y2=9></line> <polyline class=ql-stroke points=\"3 9 4 10 6 8\"></polyline> </svg>";

/***/ }),
/* 102 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <path class=ql-fill d=M15.5,15H13.861a3.858,3.858,0,0,0,1.914-2.975,1.8,1.8,0,0,0-1.6-1.751A1.921,1.921,0,0,0,12.021,11.7a0.50013,0.50013,0,1,0,.957.291h0a0.914,0.914,0,0,1,1.053-.725,0.81,0.81,0,0,1,.744.762c0,1.076-1.16971,1.86982-1.93971,2.43082A1.45639,1.45639,0,0,0,12,15.5a0.5,0.5,0,0,0,.5.5h3A0.5,0.5,0,0,0,15.5,15Z /> <path class=ql-fill d=M9.65,5.241a1,1,0,0,0-1.409.108L6,7.964,3.759,5.349A1,1,0,0,0,2.192,6.59178Q2.21541,6.6213,2.241,6.649L4.684,9.5,2.241,12.35A1,1,0,0,0,3.71,13.70722q0.02557-.02768.049-0.05722L6,11.036,8.241,13.65a1,1,0,1,0,1.567-1.24277Q9.78459,12.3777,9.759,12.35L7.316,9.5,9.759,6.651A1,1,0,0,0,9.65,5.241Z /> </svg>";

/***/ }),
/* 103 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <path class=ql-fill d=M15.5,7H13.861a4.015,4.015,0,0,0,1.914-2.975,1.8,1.8,0,0,0-1.6-1.751A1.922,1.922,0,0,0,12.021,3.7a0.5,0.5,0,1,0,.957.291,0.917,0.917,0,0,1,1.053-.725,0.81,0.81,0,0,1,.744.762c0,1.077-1.164,1.925-1.934,2.486A1.423,1.423,0,0,0,12,7.5a0.5,0.5,0,0,0,.5.5h3A0.5,0.5,0,0,0,15.5,7Z /> <path class=ql-fill d=M9.651,5.241a1,1,0,0,0-1.41.108L6,7.964,3.759,5.349a1,1,0,1,0-1.519,1.3L4.683,9.5,2.241,12.35a1,1,0,1,0,1.519,1.3L6,11.036,8.241,13.65a1,1,0,0,0,1.519-1.3L7.317,9.5,9.759,6.651A1,1,0,0,0,9.651,5.241Z /> </svg>";

/***/ }),
/* 104 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <line class=\"ql-stroke ql-thin\" x1=15.5 x2=2.5 y1=8.5 y2=9.5></line> <path class=ql-fill d=M9.007,8C6.542,7.791,6,7.519,6,6.5,6,5.792,7.283,5,9,5c1.571,0,2.765.679,2.969,1.309a1,1,0,0,0,1.9-.617C13.356,4.106,11.354,3,9,3,6.2,3,4,4.538,4,6.5a3.2,3.2,0,0,0,.5,1.843Z></path> <path class=ql-fill d=M8.984,10C11.457,10.208,12,10.479,12,11.5c0,0.708-1.283,1.5-3,1.5-1.571,0-2.765-.679-2.969-1.309a1,1,0,1,0-1.9.617C4.644,13.894,6.646,15,9,15c2.8,0,5-1.538,5-3.5a3.2,3.2,0,0,0-.5-1.843Z></path> </svg>";

/***/ }),
/* 105 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <path class=ql-stroke d=M5,3V9a4.012,4.012,0,0,0,4,4H9a4.012,4.012,0,0,0,4-4V3></path> <rect class=ql-fill height=1 rx=0.5 ry=0.5 width=12 x=3 y=15></rect> </svg>";

/***/ }),
/* 106 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <rect class=ql-stroke height=12 width=12 x=3 y=3></rect> <rect class=ql-fill height=12 width=1 x=5 y=3></rect> <rect class=ql-fill height=12 width=1 x=12 y=3></rect> <rect class=ql-fill height=2 width=8 x=5 y=8></rect> <rect class=ql-fill height=1 width=3 x=3 y=5></rect> <rect class=ql-fill height=1 width=3 x=3 y=7></rect> <rect class=ql-fill height=1 width=3 x=3 y=10></rect> <rect class=ql-fill height=1 width=3 x=3 y=12></rect> <rect class=ql-fill height=1 width=3 x=12 y=5></rect> <rect class=ql-fill height=1 width=3 x=12 y=7></rect> <rect class=ql-fill height=1 width=3 x=12 y=10></rect> <rect class=ql-fill height=1 width=3 x=12 y=12></rect> </svg>";

/***/ }),
/* 107 */
/***/ (function(module, exports) {

module.exports = "<svg viewbox=\"0 0 18 18\"> <polygon class=ql-stroke points=\"7 11 9 13 11 11 7 11\"></polygon> <polygon class=ql-stroke points=\"7 7 9 5 11 7 7 7\"></polygon> </svg>";

/***/ }),
/* 108 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = exports.BubbleTooltip = undefined;

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _extend = __webpack_require__(3);

var _extend2 = _interopRequireDefault(_extend);

var _emitter = __webpack_require__(8);

var _emitter2 = _interopRequireDefault(_emitter);

var _base = __webpack_require__(43);

var _base2 = _interopRequireDefault(_base);

var _selection = __webpack_require__(15);

var _icons = __webpack_require__(41);

var _icons2 = _interopRequireDefault(_icons);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var TOOLBAR_CONFIG = [['bold', 'italic', 'link'], [{ header: 1 }, { header: 2 }, 'blockquote']];

var BubbleTheme = function (_BaseTheme) {
  _inherits(BubbleTheme, _BaseTheme);

  function BubbleTheme(quill, options) {
    _classCallCheck(this, BubbleTheme);

    if (options.modules.toolbar != null && options.modules.toolbar.container == null) {
      options.modules.toolbar.container = TOOLBAR_CONFIG;
    }

    var _this = _possibleConstructorReturn(this, (BubbleTheme.__proto__ || Object.getPrototypeOf(BubbleTheme)).call(this, quill, options));

    _this.quill.container.classList.add('ql-bubble');
    return _this;
  }

  _createClass(BubbleTheme, [{
    key: 'extendToolbar',
    value: function extendToolbar(toolbar) {
      this.tooltip = new BubbleTooltip(this.quill, this.options.bounds);
      this.tooltip.root.appendChild(toolbar.container);
      this.buildButtons([].slice.call(toolbar.container.querySelectorAll('button')), _icons2.default);
      this.buildPickers([].slice.call(toolbar.container.querySelectorAll('select')), _icons2.default);
    }
  }]);

  return BubbleTheme;
}(_base2.default);

BubbleTheme.DEFAULTS = (0, _extend2.default)(true, {}, _base2.default.DEFAULTS, {
  modules: {
    toolbar: {
      handlers: {
        link: function link(value) {
          if (!value) {
            this.quill.format('link', false);
          } else {
            this.quill.theme.tooltip.edit();
          }
        }
      }
    }
  }
});

var BubbleTooltip = function (_BaseTooltip) {
  _inherits(BubbleTooltip, _BaseTooltip);

  function BubbleTooltip(quill, bounds) {
    _classCallCheck(this, BubbleTooltip);

    var _this2 = _possibleConstructorReturn(this, (BubbleTooltip.__proto__ || Object.getPrototypeOf(BubbleTooltip)).call(this, quill, bounds));

    _this2.quill.on(_emitter2.default.events.EDITOR_CHANGE, function (type, range, oldRange, source) {
      if (type !== _emitter2.default.events.SELECTION_CHANGE) return;
      if (range != null && range.length > 0 && source === _emitter2.default.sources.USER) {
        _this2.show();
        // Lock our width so we will expand beyond our offsetParent boundaries
        _this2.root.style.left = '0px';
        _this2.root.style.width = '';
        _this2.root.style.width = _this2.root.offsetWidth + 'px';
        var lines = _this2.quill.getLines(range.index, range.length);
        if (lines.length === 1) {
          _this2.position(_this2.quill.getBounds(range));
        } else {
          var lastLine = lines[lines.length - 1];
          var index = _this2.quill.getIndex(lastLine);
          var length = Math.min(lastLine.length() - 1, range.index + range.length - index);
          var _bounds = _this2.quill.getBounds(new _selection.Range(index, length));
          _this2.position(_bounds);
        }
      } else if (document.activeElement !== _this2.textbox && _this2.quill.hasFocus()) {
        _this2.hide();
      }
    });
    return _this2;
  }

  _createClass(BubbleTooltip, [{
    key: 'listen',
    value: function listen() {
      var _this3 = this;

      _get(BubbleTooltip.prototype.__proto__ || Object.getPrototypeOf(BubbleTooltip.prototype), 'listen', this).call(this);
      this.root.querySelector('.ql-close').addEventListener('click', function () {
        _this3.root.classList.remove('ql-editing');
      });
      this.quill.on(_emitter2.default.events.SCROLL_OPTIMIZE, function () {
        // Let selection be restored by toolbar handlers before repositioning
        setTimeout(function () {
          if (_this3.root.classList.contains('ql-hidden')) return;
          var range = _this3.quill.getSelection();
          if (range != null) {
            _this3.position(_this3.quill.getBounds(range));
          }
        }, 1);
      });
    }
  }, {
    key: 'cancel',
    value: function cancel() {
      this.show();
    }
  }, {
    key: 'position',
    value: function position(reference) {
      var shift = _get(BubbleTooltip.prototype.__proto__ || Object.getPrototypeOf(BubbleTooltip.prototype), 'position', this).call(this, reference);
      var arrow = this.root.querySelector('.ql-tooltip-arrow');
      arrow.style.marginLeft = '';
      if (shift === 0) return shift;
      arrow.style.marginLeft = -1 * shift - arrow.offsetWidth / 2 + 'px';
    }
  }]);

  return BubbleTooltip;
}(_base.BaseTooltip);

BubbleTooltip.TEMPLATE = ['<span class="ql-tooltip-arrow"></span>', '<div class="ql-tooltip-editor">', '<input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL">', '<a class="ql-close"></a>', '</div>'].join('');

exports.BubbleTooltip = BubbleTooltip;
exports.default = BubbleTheme;

/***/ }),
/* 109 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(63);


/***/ })
/******/ ])["default"];
});'''