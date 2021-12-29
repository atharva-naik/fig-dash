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
        <!-- 
        <style> {{ FULLSCREEN_CSS }} </style>
        <style> {{ FOLDGUTTER_CSS }} </style>
        <style> {{ MATCHES_ON_SCROLLBARS_CSS }} </style>
        <style> {{ SIMPLE_SCROLLBARS_CSS }} </style>
        <style> {{ LINT_CSS }} </style>
        <style> {{ TERN_CSS }} </style> -->
        
        <title> {{ TITLE }} </title>
    </head>
    <body style="background-color: {{ EDITOR_BACKGROUND_COLOR }}">
        <!-- <header class="top" style='background-color: black;'>
            <div class="wrapper">
            </div>
        </header> -->
        <div style="margin-left: auto; margin-right: auto;">
            <p><span style="color: white; font-size: 13px">Select a theme </span>
                <select style="text-align: center; background-color: #292929; color: #32a852; font-family: Monospace; border: 0px; outline: none;" onchange="selectTheme()" id=select>
                <option>default</option>
                <option>3024-day</option>
                <option>3024-night</option>
                <option>abbott</option>
                <option>abcdef</option>
                <option>ambiance</option>
                <option selected>ayu-dark</option>
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
                <option>gruvbox-dark</option>
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
        <script> {{ COMMENT_FOLD_JS }} </script
        <script> {{ MARKDOWN_FOLD_JS }} </script>
        <script> {{ XML_FOLD_JS }} </script>
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
                theme: "ayu-dark",
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
            var choice = (location.hash && location.hash.slice(1)) ||
                        (document.location.search &&
                            decodeURIComponent(document.location.search.slice(1)));
            if (choice) {
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

        </script>
    </body>
</html>''')