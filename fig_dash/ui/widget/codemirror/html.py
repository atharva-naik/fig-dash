import jinja2

CMHtml = jinja2.Template(r'''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <style>
            /* scroll bar style: Chrome, safari */
            *::-webkit-scrollbar {
                width: 7px;
                height: 7px;
            }    
            *::-webkit-scrollbar-track {
                background-color: rgba(235, 235, 235, 0.1);
            }
    
            *::-webkit-scrollbar-thumb {
                background-color: gray;
            }
            *::-webkit-scrollbar-thumb:hover {
                background-color: orange;
            }
            *::-webkit-scrollbar-corner {
                background-color: transparent;
                /* background: rgba(235, 235, 235, 0.1); */
            }
            /* Firefox */
            /* .selector {
                scrollbar-width: none;
            } */
        </style>
        <style> {{ CODEMIRROR_CSS }} </style>
        <!-- editor themes -->
        <style> {{ THEMES_CSS }} </style>
        <!-- addon styling -->
        <style> {{ DIALOG_CSS }} </style>
        <style> {{ FULLSCREEN_CSS }} </style>
        <style> {{ FOLDGUTTER_CSS }} </style>
        <style> {{ SHOW_HINT_CSS }} </style>
        <style> {{ LINT_CSS }} </style>
        <style> {{ MERGE_CSS }} </style>
        <!-- 
        <style> {{ FULLSCREEN_CSS }} </style>
        <style> {{ FOLDGUTTER_CSS }} </style>
        <style> {{ MATCHES_ON_SCROLLBARS_CSS }} </style>
        <style> {{ SIMPLE_SCROLLBARS_CSS }} </style>
        <style> {{ LINT_CSS }} </style>
        <style> {{ TERN_CSS }} </style> -->
        
        <title> {{ TITLE }} </title>
    </head>
    <body style="background-color: {{ EDITOR_BACKGROUND_COLOR }}; margin: 0px;">
        <div style="margin-left: auto; margin-right: auto;">
            <p style="display: none;"><span style="color: white; font-size: 13px">Select a theme </span>
                <select style="text-align: center; background-color: #292929; color: #32a852; font-family: Monospace; border: 0px; outline: none;" onchange="selectTheme()" id="select" style="display: none;">
                <option>default</option>
                <option>3024-day</option>
                <option>3024-night</option>
                <option>abbott</option>
                <option>abcdef</option>
                <option>ambiance</option>
                <option>ayu-dark</option>
                <option>ayu-mirage</option>
                <option>base16-dark</option>
                <option>base16-light</option>
                <option>bespin</option>
                <option>blackboard</option>
                <option>cobalt</option>
                <option>colorforth</option>
                <option>darcula</option>
                <option>dracula</option>
                <option>duotone-dark</option>
                <option>duotone-light</option>
                <option>eclipse</option>
                <option>elegant</option>
                <option>erlang-dark</option>
                <option selected>gruvbox-dark</option>
                <option>hopscotch</option>
                <option>icecoder</option>
                <option>idea</option>
                <option>isotope</option>
                <option>juejin</option>
                <option>lesser-dark</option>
                <option>liquibyte</option>
                <option>lucario</option>
                <option>material</option>
                <option>material-darker</option>
                <option>material-palenight</option>
                <option>material-ocean</option>
                <option>mbo</option>
                <option>mdn-like</option>
                <option>midnight</option>
                <option>monokai</option>
                <option>moxer</option>
                <option>neat</option>
                <option>neo</option>
                <option>night</option>
                <option>nord</option>
                <option>oceanic-next</option>
                <option>panda-syntax</option>
                <option>paraiso-dark</option>
                <option>paraiso-light</option>
                <option>pastel-on-dark</option>
                <option>railscasts</option>
                <option>rubyblue</option>
                <option>seti</option>
                <option>shadowfox</option>
                <option>solarized dark</option>
                <option>solarized light</option>
                <option>the-matrix</option>
                <option>tomorrow-night-bright</option>
                <option>tomorrow-night-eighties</option>
                <option>ttcn</option>
                <option>twilight</option>
                <option>vibrant-ink</option>
                <option>xq-dark</option>
                <option>xq-light</option>
                <option>yeti</option>
                <option>yonce</option>
                <option>zenburn</option>
            </select>
            </p>
        </div>
<textarea id="codemirror">
{{ CODE_FILE_CONTENT }}
</textarea>
            <section data-parallax="scroll" height="100px">       
                <canvas id="c" height="50px"></canvas>
              <script>
                var ctr = 0;
                var color = '#'+Math.floor(Math.random()*16777215).toString(16);
                function draw(){
                    if (ctr % 100 == 0) {
                        color = '#'+Math.floor(Math.random()*16777215).toString(16);
                    }
                    // console.log(ctr);
                    ctx.fillStyle="rgba(0, 0,0,0.05)",
                    ctx.fillRect(0,0,c.width,c.height),
                    // ctx.fillStyle="#F0F",
                    ctx.fillStyle=color,
                    ctr += 1;
                    ctx.font=font_size+"px arial";
                        for (var a=0;a<drops.length;a++) {
                            var b=j[Math.floor(Math.random()*j.length)];
                            ctx.fillText(b, a*font_size, drops[a]*font_size), 
                            drops[a]*font_size > c.height && Math.random() > 0.975 && (drops[a]=0), 
                            drops[a]++
                        }
                    }
                    var c=document.getElementById("c"),
                    ctx=c.getContext("2d");
                    c.height=120, 
                    c.width=1340;
                    var j= "abcdefghijklmnopqrstuvwxyz1!2@3#4$5%6^7&8*9(0)";
                    j = j.split("");
                    for (var font_size=15, columns=c.width/font_size, drops=[], x=0; x<columns; x++)
                        drops[x]=1;
                        setInterval(draw, 33);
              </script>
            </section>
        <!-- core javascript source -->
        <script> {{ CODEMIRROR_JS }} </script>
        <!-- addon JS sources -->
        <!-- comment addon -->
        <script> {{ COMMENT_JS }} </script>
        <script> {{ CONTINUECOMMENT_JS }} </script>
        <!-- dialog addon -->
        <script> {{ DIALOG_JS }} </script>
        <!-- display addon -->
        <script> {{ AUTOREFRESH_JS }} </script>
        <script> {{ FULLSCREEN_JS }} </script>
        <script> {{ PANEL_JS }} </script>
        <script> {{ PLACEHOLDER_JS }} </script>
        <script> {{ RULER_JS }} </script>
        <!-- edit addon -->
        <script> {{ CLOSEBRACKETS_JS }} </script>
        <script> {{ CLOSETAG_JS }} </script>
        <script> {{ CONTINUELIST_JS }} </script>
        <script> {{ MATCHBRACKETS_JS }} </script>
        <script> {{ MATCHTAGS_JS }} </script>
        <script> {{ TRAILINGSPACE_JS }} </script>
        <!-- fold addon -->
        <script> {{ FOLDCODE_JS }} </script>
        <script> {{ FOLDGUTTER_JS }} </script>
        <script> {{ INDENT_FOLD_JS }} </script>
        <script> {{ BRACE_FOLD_JS }} </script>
        <script> {{ COMMENT_FOLD_JS }} </script>
        <script> {{ MARKDOWN_FOLD_JS }} </script>
        <script> {{ XML_FOLD_JS }} </script>
        <!-- hint addon -->
        <script> {{ ANYWORD_HINT_JS }} </script>
        <script> {{ CSS_HINT_JS }} </script>
        <script> {{ HTML_HINT_JS }} </script>
        <script> {{ JAVASCRIPT_HINT_JS }} </script>
        <script> {{ SHOW_HINT_JS }} </script>
        <script> {{ SQL_HINT_JS }} </script>
        <script> {{ XML_HINT_JS }} </script>
        <!-- lint addon -->
        <script> {{ LINT_JS }} </script>
        <script> {{ CSS_LINT_JS }} </script>
        <script> {{ HTML_LINT_JS }} </script>
        <script> {{ JAVASCRIPT_LINT_JS }} </script>
        <script> {{ JSON_LINT_JS }} </script>
        <script> {{ YAML_LINT_JS }} </script>
        <script> {{ COFFEESCRIPT_LINT_JS }} </script>
        <!-- merge addon -->
        <script> {{ MATCH_PATCH_JS }} </script>
        <script> {{ MERGE_JS }} </script>
        <!-- wrap addon -->
        <script> {{ HARDWRAP_JS }} </script>
        <!-- default lang mode js -->
        <script> {{ DEFAULT_MODE_JS }} </script>
        <!-- keymap -->
        <script> {{ KEYMAP_JS }}</script>
        <!-- qwebchannel js -->
        <script> {{ QWEBCHANNEL_JS }} </script>
        <style>
            .CodeMirror-gutter-wrapper {
                width: 80px;
            }
            .CodeMirror-linenumber {
                /* padding: 1px 8px 0 5px; */
                padding-left: 25px;
                /* color: #c8d2d7; */
                /* font-size: 10px; */
            }
            .CodeMirror {border: 1px solid black;}
            .CodeMirror-activeline-gutter {background-image: url({{ HINT_IMAGE }}); background-color: purple}
            .lint-error {font-family: arial; font-size: 70%; background: #ffa; color: #a00; padding: 2px 5px 3px; }
            .lint-error-icon {color: white; background-color: red; font-weight: bold; border-radius: 50%; padding: 0 3px; margin-right: 7px;}
       </style>
        <script>
            function getRulerHTML(num_rulers) {
                var spaceAmt = 35.2818;
                var rulers = ''
                for (var i = 0; i < num_rulers; i++) {
                    rulers += `<div class="CodeMirror-ruler" style="border-color: rgb(78, 78, 78); border-left-style: solid; left: ${spaceAmt}px;"></div>`
                    spaceAmt += 66.5636-35.2818;
                }

                return rulers
            }
            function getRulers(num_rulers) {
                rulers = []
                for (var i = 0; i < num_rulers; i++) {
                    rulers.push({color: '#4e4e4e', column: 4*(i+1), lineStyle: "solid"});
                }

                return rulers;
            }
            function numLeadingTabs(text) {
                var count = 0;
                var index = 0;
                var space_count = 0;
                while (text.charAt(index) === "\t" || text.charAt(index) === ' ') {
                    if (text.charAt(index) == "\t") {
                        count++;
                    }
                    else {
                        space_count++;
                    }
                    index++;
                }
                return count+Math.floor(space_count/4);
            }
            var editor = CodeMirror.fromTextArea(document.getElementById("codemirror"), {
                value: "write your code here",
                rulers: getRulers(1),
                lineNumbers: true,
                electricChars: true,
                lineSeparator: null,
                indentUnit: 4,
                keyMap: "sublime",
                autoCloseBrackets: true,
                matchBrackets: true,
                styleActiveLine: true,
                xml: true,
                fencedCodeBlockHighlighting: true,
                foldGutter: true,
                highlightFormatting: true,
                highlightNonStandardPropertyKeywords: true, 
                gutters: ["breakpoints", "CodeMirror-linenumbers", "CodeMirror-foldgutter"],
                mode: "{{ LANG_MODE }}",
                smartIndent: true,
                theme: "{{ THEME }}",
            });
            editor.on("gutterClick", function(cm, n) {
                var info = cm.lineInfo(n);
                cm.setGutterMarker(n, "breakpoints", info.gutterMarkers ? null : makeMarker());
            });
            function makeMarker() {
                var marker = document.createElement("div");
                marker.style.color = "#ff4d00";
                marker.style.whiteSpace = "nowrap";
                marker.innerHTML = " ●" // `●<img width='14px' src='{{ HINT_IMAGE }}' title="hints">`;
                return marker;
            }
            editor.setSize("100%", 600);
            editor.setOption('viewportMargin', Infinity);
            var input = document.getElementById("select");
            function selectTheme() {
                var theme = input.options[input.selectedIndex].textContent;
                // alert(theme)
                editor.setOption("theme", theme);
                location.hash = "#" + theme;
            }
            function selectThemeByIndex(selectedIndex) {
                var theme = input.options[selectedIndex].textContent;
                // alert(theme)
                editor.setOption("theme", theme);
                location.hash = "#" + theme;
            }
            var choice = (location.hash && location.hash.slice(1)) ||
                        (document.location.search &&
                            decodeURIComponent(document.location.search.slice(1)));
            if (choice) {
                console.error(choice);
                input.value = choice;
                editor.setOption("theme", choice);
            }
            CodeMirror.on(window, "hashchange", function() {
                var theme = location.hash.slice(1);
                if (theme) { input.value = theme; selectTheme(); }
            });
            CodeMirror.on(editor, "cursorActivity", (instance, obj) => {
                lines = instance.getValue().split('\n');
                max_leading_tabs = 0
                for (var i = 0; i < lines.length; i++) {
                    max_leading_tabs = Math.max(
                        max_leading_tabs, 
                        numLeadingTabs(lines[i])
                    );
                }
                var num_rulers = Math.max(max_leading_tabs-1, 0);
                var rulerDiv = document.getElementsByClassName("CodeMirror-rulers")[0];
                rulerDiv.innerHTML = getRulerHTML(num_rulers);
                /* console.log(getRulerHTML(num_rulers)); */
            })
            /* CodeMirror.on(editor, "cursorActivity", (instance, obj) => {
                cursor = instance.doc.getCursor()
                col = cursor.ch
                line = cursor.line
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    backend = channel.objects.backend;
                    // backend.getRef(x, function(pyval) {
                    //     backend.printRef(pyval);
                    // });
                    backend.sendCursorPos(line, col)
                });
            }) */
            selectThemeByIndex(21);
        </script>
    </body>
</html>''')

CMMergeHtml = jinja2.Template(r'''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <style>
            /* scroll bar style: Chrome, safari */
            *::-webkit-scrollbar {
                width: 7px;
                height: 7px;
            }    
            *::-webkit-scrollbar-track {
                background-color: rgba(235, 235, 235, 0.1);
            }
    
            *::-webkit-scrollbar-thumb {
                background-color: gray;
            }
            *::-webkit-scrollbar-thumb:hover {
                background-color: orange;
            }
            *::-webkit-scrollbar-corner {
                background-color: transparent;
                /* background: rgba(235, 235, 235, 0.1); */
            }
            /* Firefox */
            /* .selector {
                scrollbar-width: none;
            } */
        </style>
        <style> {{ CODEMIRROR_CSS }} </style>
        <!-- editor themes -->
        <style> {{ THEMES_CSS }} </style>
        <!-- addon styling -->
        <style> {{ DIALOG_CSS }} </style>
        <style> {{ FULLSCREEN_CSS }} </style>
        <style> {{ FOLDGUTTER_CSS }} </style>
        <style> {{ SHOW_HINT_CSS }} </style>
        <style> {{ LINT_CSS }} </style>
        <style> {{ MERGE_CSS }} </style>
        <!-- core javascript -->
        <script> {{ CODEMIRROR_JS }} </script>
        <!-- merge addon -->
        <script> {{ MATCH_PATCH_JS }} </script>
        <script> {{ MERGE_JS }} </script>

        <title> {{ TITLE }} </title>
    </head>
    <body style="background-color: {{ EDITOR_BACKGROUND_COLOR }}; margin: 0px;">
<div id="view">
{{ CODE_FILE_CONTENT }}
</div>
        <!-- default lang mode js -->
        <script> {{ DEFAULT_MODE_JS }} </script>
        <script>
            function getRulerHTML(num_rulers) {
                var spaceAmt = 35.2818;
                var rulers = ''
                for (var i = 0; i < num_rulers; i++) {
                    rulers += `<div class="CodeMirror-ruler" style="border-color: rgb(78, 78, 78); border-left-style: solid; left: ${spaceAmt}px;"></div>`
                    spaceAmt += 66.5636-35.2818;
                }

                return rulers
            }
            function getRulers(num_rulers) {
                rulers = []
                for (var i = 0; i < num_rulers; i++) {
                    rulers.push({color: '#4e4e4e', column: 4*(i+1), lineStyle: "solid"});
                }

                return rulers;
            }
            function numLeadingTabs(text) {
                var count = 0;
                var index = 0;
                var space_count = 0;
                while (text.charAt(index) === "\t" || text.charAt(index) === ' ') {
                    if (text.charAt(index) == "\t") {
                        count++;
                    }
                    else {
                        space_count++;
                    }
                    index++;
                }
                return count+Math.floor(space_count/4);
            }
            var value, orig1, orig2, dv, panes = 2, highlight = true, connect = "align", collapse = false;
            function initUI() {
                if (value == null) return;
                var target = document.getElementById("view");
                target.innerHTML = "";
                dv = CodeMirror.MergeView(target, {
                    value: value,
                    origLeft: panes == 3 ? orig1 : null,
                    orig: orig2,
                    lineNumbers: true,
                    mode: "{{ LANG_MODE }}",
                    smartIndent: true,
                    theme: "{{ THEME }}",
                    highlightDifferences: highlight,
                    connect: connect,
                    collapseIdentical: collapse
                });
                dv.editor().setSize("100%", "600");
            }
            function toggleDifferences() {
                dv.setShowDifferences(highlight = !highlight);
            }
            window.onload = function() {
                value = document.documentElement.innerHTML;
                orig1 = "<!doctype html>\n\n" + value.replace(/\.\.\//g, "codemirror/").replace("yellow", "orange");
                orig2 = value.replace(/\u003cscript/g, "\u003cscript type=text/javascript ")
                .replace("white", "purple;\n      font: comic sans;\n      text-decoration: underline;\n      height: 15em");
                initUI();
                let d = document.createElement("div"); d.style.cssText = "width: 50px; margin: 7px; height: 14px"; dv.editor().addLineWidget(57, d)
            };
            function mergeViewHeight(mergeView) {
                function editorHeight(editor) {
                    if (!editor) return 0;
                    return editor.getScrollInfo().height;
                }
                return Math.max(editorHeight(mergeView.leftOriginal()),
                                editorHeight(mergeView.editor()),
                                editorHeight(mergeView.rightOriginal()));
            }
            function resize(mergeView) {
                var height = mergeViewHeight(mergeView);
                for(;;) {
                    if (mergeView.leftOriginal())
                        mergeView.leftOriginal().setSize(null, height);
                    mergeView.editor().setSize(null, height);
                    if (mergeView.rightOriginal())
                        mergeView.rightOriginal().setSize(null, height);

                    var newHeight = mergeViewHeight(mergeView);
                    if (newHeight >= height) break;
                    else height = newHeight;
                }
                mergeView.wrap.style.height = height + "px";
            }
            /* window.addEventListener('resize', function(event) {
                console.error(event.width, event.height);
            }); */
        /* document.getElementById("select").style.display = "none"; */
        select.
        </script>
    <!-- SUB TEMP_JS_SOURCES HERE -->
    </body>
</html>''')

JS_SOURCES = r'''
        <!-- addon JS sources -->
        <!-- comment addon -->
        <script> {{ COMMENT_JS }} </script>
        <script> {{ CONTINUECOMMENT_JS }} </script>
        <!-- dialog addon -->
        <script> {{ DIALOG_JS }} </script>
        <!-- display addon -->
        <script> {{ AUTOREFRESH_JS }} </script>
        <script> {{ FULLSCREEN_JS }} </script>
        <script> {{ PANEL_JS }} </script>
        <script> {{ PLACEHOLDER_JS }} </script>
        <script> {{ RULER_JS }} </script>
        <!-- edit addon -->
        <script> {{ CLOSEBRACKETS_JS }} </script>
        <script> {{ CLOSETAG_JS }} </script>
        <script> {{ CONTINUELIST_JS }} </script>
        <script> {{ MATCHBRACKETS_JS }} </script>
        <script> {{ MATCHTAGS_JS }} </script>
        <script> {{ TRAILINGSPACE_JS }} </script>
        <!-- fold addon -->
        <script> {{ FOLDCODE_JS }} </script>
        <script> {{ FOLDGUTTER_JS }} </script>
        <script> {{ INDENT_FOLD_JS }} </script>
        <script> {{ BRACE_FOLD_JS }} </script>
        <script> {{ COMMENT_FOLD_JS }} </script>
        <script> {{ MARKDOWN_FOLD_JS }} </script>
        <script> {{ XML_FOLD_JS }} </script>
        <!-- hint addon -->
        <script> {{ ANYWORD_HINT_JS }} </script>
        <script> {{ CSS_HINT_JS }} </script>
        <script> {{ HTML_HINT_JS }} </script>
        <script> {{ JAVASCRIPT_HINT_JS }} </script>
        <script> {{ SHOW_HINT_JS }} </script>
        <script> {{ SQL_HINT_JS }} </script>
        <script> {{ XML_HINT_JS }} </script>
        <!-- lint addon -->
        <script> {{ LINT_JS }} </script>
        <script> {{ CSS_LINT_JS }} </script>
        <script> {{ HTML_LINT_JS }} </script>
        <script> {{ JAVASCRIPT_LINT_JS }} </script>
        <script> {{ JSON_LINT_JS }} </script>
        <script> {{ YAML_LINT_JS }} </script>
        <script> {{ COFFEESCRIPT_LINT_JS }} </script>
        <!-- merge addon -->
        <script> {{ MATCH_PATCH_JS }} </script>
        <script> {{ MERGE_JS }} </script>
        <!-- wrap addon -->
        <script> {{ HARDWRAP_JS }} </script>
        <!-- keymap -->
        <script> {{ KEYMAP_JS }}</script>
        <!-- qwebchannel js -->
        <script> {{ QWEBCHANNEL_JS }} </script>'''