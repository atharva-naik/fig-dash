import jinja2

XSpreadsheetHtml = jinja2.Template(r'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>{{ TITLE }}</title>
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
    <style> {{ XSPREADSHEET_CSS }} </style>
</head>
<body onload="load()">
  <div id="spreadsheet-editor"></div>
  <script>
    function load(){
      const rows10 = { len: 1000 };
      for (let i = 0; i < 1000; i += 1) {
        rows10[i] = {
          cells: {
            0: { text: 'A-' + i },
            1: { text: 'B-' + i },
            2: { text: 'C-' + i },
            3: { text: 'D-' + i },
            4: { text: 'E-' + i },
            5: { text: 'F-' + i },
          }
        };
      }
      const rows = {
        len: 80,
        1: {
          cells: {
            0: { text: 'testingtesttestetst' },
            2: { text: 'testing' },
          },
        },
        2: {
          cells: {
            0: { text: 'render', style: 0 },
            1: { text: 'Hello' },
            2: { text: 'haha', merge: [1, 1] },
          }
        },
        8: {
          cells: {
            8: { text: 'border test', style: 0 },
          }
        }
      };
      // x_spreadsheet.locale('zh-cn');
      var xs = x_spreadsheet('#spreadsheet-editor', 
        {
            showToolbar: true, 
            showGrid: true
        })
        .loadData([{
            // freeze: 'B3',
            styles: [
                {
                    bgcolor: '#f4f5f8',
                    textwrap: true,
                    color: '#900b09',
                    border: {
                        top: ['thin', '#0366d6'],
                        bottom: ['thin', '#0366d6'],
                        right: ['thin', '#0366d6'],
                        left: ['thin', '#0366d6'],
                    },
                },
            ],
            merges: [
                'C3:D4',
            ],
            cols: {
                len: 10,
                2: { width: 200 },
            },
            rows,
        }, { name: 'sheet-test', rows: rows10 }]).change((cdata) => {
          // console.log(cdata);
          console.log('>>>', xs.getData());
        });

        xs.on('cell-selected', (cell, ri, ci) => {
            console.log('cell:', cell, ', ri:', ri, ', ci:', ci);
        }).on('cell-edited', (text, ri, ci) => {
            console.log('text:', text, ', ri: ', ri, ', ci:', ci);
        });

        setTimeout(() => {
            // xs.loadData([{ rows }]);
            xs.cellText(14, 3, 'cell-text').reRender();
            console.log('cell(8, 8):', xs.cell(8, 8));
            console.log('cellStyle(8, 8):', xs.cellStyle(8, 8));
        }, 5000);
    }
    </script>
    <script> {{ XSPREADSHEET_JS }}}</script>
</body>
</html>''')