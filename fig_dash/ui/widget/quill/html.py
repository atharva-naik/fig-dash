import jinja2

QuillParams = {
    "LANG": "en",
    "THEME": "snow",
    "TITLE": "Quill Editor",
    "SNOW_CSS": "",
    "EMOJI_CSS": "",
    "JS": "",
    "EMOJI_JS": "",
    "EMOJI_IMAGE": "",
}
QuillHTML = jinja2.Template('''<!DOCTYPE html>
<html lang="{{ LANG }}">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <style> 
            {{ SNOW_CSS }}
            {{ EMOJI_CSS }}
        </style>
        <title>{{ TITLE }}</title>
    </head>
    <body>
        <div name="wrapper" style="height: 100%; flex: 1">
            <div id="quill-editor" style="height: 100%; flex: 1"></div>
        </div>
        </div>
        <script>{{ JS }}</script>
        <script>{{ EMOJI_JS }}</script>
        <script>
            const toolbarOptions = {
                container: [
                    [{ 'header': [1, 2, 3, 4, 5, 6, false] }, 'bold', 'italic', 'underline', 'strike',{ 'script': 'sub'}, { 'script': 'super' }],
                    ['blockquote', 'code-block', { 'indent': '-1'}, { 'indent': '+1' }],
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    ['image', 'link'],
                    // [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
                    [{ 'color': [] }, { 'background': [] }, { 'font': [] }, { 'align': [] }],          // dropdown with defaults from theme
                    ['emoji'],
                ],
                handlers: {'emoji': function() {}}
            }

            var quill = new Quill('#quill-editor', {
                modules: {
                    // syntax: true,
                    // table: true,
                    toolbar: toolbarOptions,
                    "emoji-toolbar" : true,
                    "emoji-textarea": true,
                    "emoji-shortname": true,
                },
                theme: '{{ THEME }}',
                placeholder: 'Jot down your ideas here!'
            });
        </script>
    </body>
</html>''')