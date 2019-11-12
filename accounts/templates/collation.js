/********************************
 * csv読み込み
 **********************************/
var table = document.getElementById('table1');  //表のオブジェクトを取得
var form = document.getElementById("csvget");
form.addEventListener('change',function(evt){
    var file = evt.target.files[0];
    //FileReaderのインスタンスを作成する
    var reader = new FileReader();
    // ファイル読み取りに失敗したとき
    reader.onerror = function() {
        alert('ファイル読み取りに失敗しました');
    }
    //テキスト形式で読み込む
    reader.readAsText(file);

    var data = new Array();
    var rows =[];
    //読込終了後の処理
    reader.addEventListener( 'load', function(){
        // 行単位で配列にする
        var itemArr = reader.result.split(',');
        for(var i = 0; i < itemArr.length; i++){
            data =  reader.result.split(',');
        }
        for(var j = 0; j < itemArr.length; j++){
            rows.push(table.insertRow(-1));
            //列は初期で設定している見出しの数（<!-- 見出し -->）のとこ※今回は3つなのでk<3
            for(var k = 0; k < 3; k ++){
                cell = rows[j].insertCell(-1);
                if(k ==　0){
                    cell.innerHTML = j+1;
                }
                else if(k == 1){
                    cell.innerHTML = data[j];                  //出荷実績
                }
                // else if(k == 2){
                //     // cell.innerHTML = '<input class="inpval" type="text"   id="txt' + j + '" name="txt' + j + '" value="" size="20" >';         //テキストボックスの作成：通し番号
                //     cell.innerHTML = "";
                // }
                else{
                    // cell.innerHTML = '<input class="inpval" type="text"   id="Colresult' + i + '" name="Colresult' + i + '" value="否" size="10" >';     //テキストボックスの作成：照合結果
                    cell.innerHTML ="";
                }
            }
        }
    })
},false);

/********************************
 * csvファイルの取得
**********************************/
// function GetList(){
    
// }


/********************************
 * テキスト値取得，貼付け
 **********************************/
function GetValue(){
    var pailnum = document.getElementById('text').value;
//  document.getElementById("textout").value = pailnum;
    var table = document.getElementById('table1');  //表のオブジェクトを取得
    var cells = new Array();
    // td内のtrをループ。rowsコレクションで,行位置取得。
    for(var i = 1,rowlen = table.rows.length; i < rowlen; i++){
    //i行目の1列目のセルの値を取得(出荷実績)
    cells.push(table.rows[i].cells[1].innerHTML);
    }
    var pailnum_position = cells.indexOf(pailnum); //配列の中のpailnumの数値がある配列位置を取得
    //杭番号があれば
    if(pailnum_position > -1){
        //初めての読取りの場合
        if(!(table.rows[pailnum_position + 1].cells[2].innerHTML)){
        //  table.rows[pailnum_position + 1].cells[2].innerHTML = pailnum; //「通し番号」に杭番号出力
        var pailnum_save = pailnum;//「注番」保存
        }
        //二度目の読取りの場合
        else{
            alert('既に読み込まれています');
            document.getElementById('text').value = "";
            document.getElementById('text').focus();
        }
    }
    else{
        alert('受入れた杭番号は出荷実績に含まれていません');
        document.getElementById('text').value = "";
        document.getElementById('text').focus();
    }
    //照合結果出力
    //出荷実績と通し番号が同じならば照合完了と出力
    //  if(table.rows[pailnum_position + 1].cells[1].innerHTML == table.rows[pailnum_position + 1].cells[2].innerHTML){
    //     table.rows[pailnum_position + 1].cells[3].innerHTML = "照合完了"
    //     document.getElementById('text').value = "";
    //     document.getElementById('text').focus();
    //  }        
    if(table.rows[pailnum_position + 1].cells[1].innerHTML == pailnum_save){
        var now = new Date();
        var Year = now.getFullYear();
        var Month = now.getMonth()+1;
        var date = now.getDate();
        var Hour = now.getHours();
        var Min = now.getMinutes();
        var Sec = now.getSeconds();
        table.rows[pailnum_position + 1].cells[2].innerHTML = Year + "/" + Month + "/" + date + "/" + Hour + ":" + Min + ":" + Sec;
        document.getElementById('text').value = "";
        document.getElementById('text').focus();
        }              
}
/********************************
 * csvダウンロード
 **********************************/
function handleDownload() {
    var bom = new Uint8Array([0xEF, 0xBB, 0xBF]);//文字コードをBOM付きUTF-8に指定
    var table = document.getElementById('table1');//id=table1という要素を取得
    var data_csv="";//ここに文字データとして値を格納していく
    /********************************
    一番上に見出しを付けて次に値の出力
    ********************************/
    // for(var i = 0;  i < 1; i++){
    //     for(var j = 0; j < table.rows[i].cells.length; j++){
    //         data_csv += table.rows[i].cells[j].innerHTML;//HTML中の表のセル値をdata_csvに格納
    //         if(j == table.rows[i].cells.length-1) data_csv += "\n";//行終わりに改行コードを追加
    //         else data_csv += ",";//セル値の区切り文字として,を追加
    //     }
    // }
    for(var i = 0;  i < 1; i++){
        for(var j = 0; j < 11; j++){ //列の固定（建材に確認※1028現在の想定では10個）
            if(j == 0){data_csv += "No"}
            else if (j == 1){data_csv += "出荷実績"}
            else if (j == 2){data_csv += "受入実績"}
            else if (j == 3){data_csv += "受入者"}
            else if (j == 4){data_csv += "受入検査"}
            else if (j == 5){data_csv += "検査者"}
            else if (j == 6){data_csv += "打設位置"}
            else if (j == 7){data_csv += "断面"}
            else if (j == 8){data_csv += "打設完了"}
            else if (j == 9){data_csv += "打設完了時間"}
            else {data_csv += "打設者"}
            if(j == 10) data_csv += "\n";//行終わりに改行コードを追加
            else data_csv += ",";//セル値の区切り文字として,を追加
        }
    }
    for(var i=1; i < table.rows.length; i++){
        data_csv += i;
        data_csv += ",";//セル値の区切り文字として,を追加
        data_csv += table.rows[i].cells[1].innerHTML; //出荷実績
        data_csv += ",";//セル値の区切り文字として,を追加
        // data_csv += table.rows[i].cells[2].innerHTML; //通し番号
        // data_csv += ",";//セル値の区切り文字として,を追加
        data_csv += table.rows[i].cells[2].innerHTML; //照合結果
        data_csv += "\n";//行終わりに改行コードを追加
    }
    //*******************************
    var blob = new Blob([ bom, data_csv], { "type" : "text/csv" });//data_csvのデータをcsvとしてダウンロードする関数
    if (window.navigator.msSaveBlob) { //IEの場合の処理
        window.navigator.msSaveBlob(blob, "杭照合結果.csv"); 
        //window.navigator.msSaveOrOpenBlob(blob, "test.csv");// msSaveOrOpenBlobの場合はファイルを保存せずに開ける
    } 
    else {
        document.getElementById("download").href = window.URL.createObjectURL(blob);
    }
    delete data_csv;//data_csvオブジェクトはもういらないので消去してメモリを開放
}