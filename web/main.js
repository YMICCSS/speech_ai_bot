function btn_click() {
    //呼叫的方式，就是加上eel.加上剛剛被expose PY function的名稱然後多加()輸入參數，最後加()取值
    // 下面這行，目前正在程式更新，所以先註解
    // lession = eel.get_lession()()
    result = eel.main()()

}

//將函數曝露給python使用
eel.expose(print_lession)
function print_lession(lessions,length) {
    //呼叫的方式，就是加上eel.加上剛剛被expose PY function的名稱然後多加()輸入參數，最後加()取值
    document.querySelector('#content-1-content').innerHTML = "本月課程如下，請點擊該課程名稱開啟簽到表"
    if (document.querySelector('.btn')){
        return " huttons are in this Screen "
    } else {
        for (step = 0; step < length; step++) {
            str = document.createElement('button');
            // 用 createElement 增加一個 DOM 節點
            // 先用 JS 寫好要增加的內容
            str.textContent = lessions[step][0]+"\n"+lessions[step][1];
            // 新增各式屬性
            str.setAttribute('type', "button");
            str.setAttribute('class', "btn btn-primary btn-sm m-2");
            // 將這個按鍵本身的物件傳遞給js做處理
            str.setAttribute('onclick', "open_sign_in_form(this)");
            str.setAttribute('id', lessions[step][1] + "-" + lessions[step][0]);
            // 用 appendChild() 把上面寫好的子節點掛在既有的 #content-1 下面，新增的內容會依序排列在後面，不會被洗掉
            document.querySelector('#content-1').appendChild(str);
        }
    }
}

function open_sign_in_form(this_item) {
    console.log(this_item.id) ;
    file_name = this_item.id ;
    //呼叫的方式，就是加上eel.加上剛剛被expose PY function的名稱然後多加()輸入參數，最後加()取值
    lession = eel.open_sign_in_form(file_name)();

}

// 刪除按鈕後上回應
eel.expose(update_display)
function update_display(display_content) {
    var btn_child_list = document.querySelectorAll('.btn')
    console.log(document.querySelectorAll('.btn'))
    for (item=0;item<btn_child_list.length;item++){
        document.querySelector('#content-1').removeChild(btn_child_list[item]);
    }
    // 插入預測的文字
    document.querySelector('#content-1-content').innerHTML = display_content;

}

