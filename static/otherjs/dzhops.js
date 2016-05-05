/**
 * Created by Guibin on 2016/3/19.
 */

//实现复选框全选与反选；
function checkAll(chkall) {
    if(chkall.checked){
        $("input[name='minion_id']").each(function(){this.checked=true;});
    }else{
        $("input[name='minion_id']").each(function(){this.checked=false;});
    }
}

//获取复选框的值
function getCheckValue(action) {
    var minion_id = "";
    $('input[name="minion_id"]:checked').each(function(){
        minion_id += $(this).val() + ',';
    });
    if (minion_id === "") {
        alert("您尚未选择任何选项，请重新选择后提交！");
        return false;
    } else {
        var url = '/keys/' + action + '/'
        $.getJSON(url, {"minion_id": minion_id, "action": action}, function(result) {
            if (result === true) {
                var ret = deleteTbodyTr(minion_id);
                if (ret === true) {
                    alert('操作成功！')
                } else {
                    alert('错误1：操作失败！')
                }

            } else {
                alert('错误2：操作失败！')
            }
        });
    }
}

//将'aaa,bbb,ccc,'转换为数组，并以此删除以此为id的元素；
function deleteTbodyTr(minion_id) {
    var minion_id_str = minion_id.slice(0,-1);
    var minion_id_array = minion_id_str.split(',');
    $.each(minion_id_array, function(index,value) {
        var tbody_tr_id = '#' + value;
        $(tbody_tr_id).remove();
    });
    return true;
}

function saltExecute() {
// $.ajaxSettings.async = false;
    $(document).ready(function(){
        $('#result').html("");
        $('#info').html("")
        var tgt = $("input[name='tgt']").val();
        var arg = $("input[name='arg']").val();
        var datacenter = "";
        $('input[name="datacenter"]:checked').each(function(){
            datacenter += $(this).val() + ',';
        });
        if ((tgt === '' || tgt === null) && (datacenter === '' || datacenter === null)) {
            alert('请输入服务器IP或选择对应机房！');
            return false;
        }
        if (arg === '' || arg === null) {
            alert('请输入将要执行的命令！');
            return false;
        }
        $("#execapi").attr("disabled","disabled");
        $("#execapi").html('<img src="/static/img/button.gif" style="width:28px;height:16px;"/>');
        $.getJSON("/salt/api/execute/",{'tgt':tgt,'datacenter':datacenter, 'arg': arg}, function(ret){
            if (ret.hasOwnProperty('errors')) {
                alert(ret.errors);
                $("#execapi").removeAttr("disabled");
                $("#execapi").html("提交");
                return false;
            } else {
                if (ret.info.unrecv_count===0) {
                    $('#info').html("本次执行对象共"+ret.info.send_count+"台，其中"+ret.info.recv_count+"台返回结果;"
                      );
                } else {
                    $('#info').html("本次执行对象共" + ret.info.send_count + "台，其中" + ret.info.recv_count + "台返回结果；未返回结果的有以下" + ret.info.unrecv_count + "台：<br/>" + ret.info.unrecv_strings
                      );
                }
                    var sortArray = [];
                $.each(ret.result, function(key, val) { sortArray[sortArray.length] = key;});
                sortArray.sort();
                $.each(sortArray, function(i, key) {
                    $("#result").append(
                            "<hr/><p class='bg-info'><b>" + key + "</b></p><pre>"+ret['result'][key]['cont']+"</pre>"
                    );
                });
            };
            $("#execapi").removeAttr("disabled");
            $("#execapi").html("提交");
        });
    });
    // $.ajaxSettings.async = true;
}

function saltFunc() {
    //$.ajaxSettings.async = false;
    $(document).ready(function(){
        $("#info").html("");
        $("#result").html("");
        var tgt = $("input[name='tgt']").val();
        var datacenter = "";
        var arg = "";
        $("input[name='datacenter']:checked").each(function(){
            datacenter += $(this).val() + ',';
        });
        $("input[name='sls']:checked").each(function(){
            arg = $(this).val();
        });
        if ((tgt === '' || tgt === null) && (datacenter === '' || datacenter === null)) {
            alert('请输入服务器IP或选择对应机房！');
            return false;
        };
        if (arg === '' || arg === null) {
            alert('请选择将要进行的操作！');
            return false;
        };
        $("#salt_submit").attr("disabled","disabled");
        $("#salt_submit").html('<img src="/static/img/button.gif" style="width:28px;height:16px;"/>');
        $.getJSON("/salt/api/deploy/", {"tgt":tgt, "datacenter":datacenter, "sls":arg}, function(ret){
            if (ret.hasOwnProperty("errors")) {
                alert(ret.errors);
                $("#salt_submit").removeAttr("disabled");
                $("#salt_submit").html("提交");
                return false;
            } else {
                if (ret.info.unrecv_count === 0) {
                    $("#info").html('\
                        <hr/>本次执行对象'+ret.info.send_count+'台，\
                        共'+ret.info.recv_count+'台返回结果，\
                        其中成功'+ret.info.succeed+'台，\
                        失败'+ret.info.failed+'台；<hr/>'
                    );
                } else {
                    $("#info").html('\
                        <hr/>本次执行对象'+ret.info.send_count+'台，\
                        共'+ret.info.recv_count+'台返回结果，\
                        其中成功'+ret.info.succeed+'台，\
                        失败'+ret.info.failed+'台；\
                        未返回结果的有以下'+ret.info.unrecv_count+'台:\
                        <br/>'+ ret.info.unrecv_strings+';<hr/>'
                    );
                }
            }
            var sortArray = [];
            $.each(ret.result, function(key, value) {
                sortArray[sortArray.length] = key;
            });
            sortArray.sort();
            $.each(sortArray, function(i, key) {
                var ip_nodot = key.replace(/\./g,'');
                if (ret['result'][key]['status'] === 'True') {
                    $("#result").append('\
                        <div class="col-md-3" style="margin-bottom:5px">\
                            <button type="button" class="btn btn-info btn-block" data-toggle="modal" data-target="#'+ip_nodot+'">'+key+'</button>\
                        </div>\
                        <div class="modal fade bs-example-modal-lg" id="'+ip_nodot+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\
                          <div class="modal-dialog modal-lg">\
                            <div class="modal-content">\
                              <div class="modal-header">\
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
                                <h4 class="modal-title" id="myModalLabel">'+key+'</h4>\
                              </div>\
                              <div class="modal-body">\
                                <pre>'+ret['result'][key]['cont']+'</pre>\
                              </div>\
                              <div class="modal-footer">\
                                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>\
                              </div>\
                            </div>\
                          </div>\
                        </div>'
                    );
                } else {
                    $("#result").append('\
                        <div class="col-md-3" style="margin-bottom:5px">\
                            <button type="button" class="btn btn-danger btn-block" data-toggle="modal" data-target="#'+ip_nodot+'">'+key+'</button>\
                        </div>\
                        <div class="modal fade bs-example-modal-lg" id="'+ip_nodot+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\
                          <div class="modal-dialog modal-lg">\
                            <div class="modal-content">\
                              <div class="modal-header">\
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
                                <h4 class="modal-title" id="myModalLabel">'+key+'</h4>\
                              </div>\
                              <div class="modal-body">\
                                <pre>'+ret['result'][key]['cont']+'</pre>\
                              </div>\
                              <div class="modal-footer">\
                                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>\
                              </div>\
                            </div>\
                          </div>\
                        </div>');
                };
            });
            $("#salt_submit").removeAttr("disabled");
            $("#salt_submit").html("提交");
        });
    });
    //$.ajaxSettings.async = true;
}

//修复历史数据
function repairHistoryData() {
    $("#info").html("");
    $("#result").html("");
    var datacenter = "";
    var stockexchange = "";
    var sls = "";
    $("input[name='datacenter']:checked").each(function(){
        datacenter += $(this).val() + ',';
    });
    $("input[name='stockexchange']:checked").each(function(){
        stockexchange += $(this).val() + ',';
    });
    $("input[name='sls']:checked").each(function(){
        sls = $(this).val();
    });
    if (datacenter === '' || datacenter === null) {
        alert('请选择将要操作的机房！');
        return false;
    }
    if (stockexchange === '' || stockexchange === null) {
        alert('请选择将要补数据的市场！');
        return false;
    }
    if (sls === '' || sls === null) {
        alert('请选择补过数据以后是否需要重启行情程序！');
        return false;
    }
    $("#submit_history").attr("disabled","disabled");
    $("#submit_history").html('<img src="/static/img/button.gif" style="width:28px;height:16px;"/>');
    $.getJSON("/data/api/history/", {"datacenter":datacenter, "stockexchange":stockexchange, "sls": sls}, function(ret){
        if (ret.hasOwnProperty("errors")) {
            alert(ret.errors);
            $("#submit_history").removeAttr("disabled");
            $("#submit_history").html("提交");
            return false;
        } else {
            if (ret.info.unrecv_count === 0) {
                $("#info").html('\
                    <hr/>本次执行对象'+ret.info.send_count+'台，\
                    共'+ret.info.recv_count+'台返回结果，\
                    其中成功'+ret.info.succeed+'台，\
                    失败'+ret.info.failed+'台；<hr/>'
                );
            } else {
                $("#info").html('\
                    <hr/>本次执行对象'+ret.info.send_count+'台，\
                    共'+ret.info.recv_count+'台返回结果，\
                    其中成功'+ret.info.succeed+'台，\
                    失败'+ret.info.failed+'台；\
                    未返回结果的有以下'+ret.info.unrecv_count+'台:\
                    <br/>'+ ret.info.unrecv_strings+'<hr/>'
                );
            }
        }
        var sortArray = [];
        $.each(ret.result, function(key, value) {
            sortArray[sortArray.length] = key;
        });
        sortArray.sort();
        $.each(sortArray, function(i, key) {
            var ip_nodot = key.replace(/\./g,'');
            if (ret['result'][key]['status'] === 'True') {
                $("#result").append('\
                    <div class="col-md-3" style="margin-bottom:5px">\
                        <button type="button" class="btn btn-info btn-block" data-toggle="modal" data-target="#'+ip_nodot+'">'+key+'</button>\
                    </div>\
                    <div class="modal fade bs-example-modal-lg" id="'+ip_nodot+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\
                      <div class="modal-dialog modal-lg">\
                        <div class="modal-content">\
                          <div class="modal-header">\
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
                            <h4 class="modal-title" id="myModalLabel">'+key+'</h4>\
                          </div>\
                          <div class="modal-body">\
                            <pre>'+ret['result'][key]['cont']+'</pre>\
                          </div>\
                          <div class="modal-footer">\
                            <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>\
                          </div>\
                        </div>\
                      </div>\
                    </div>'
                );
            } else {
                $("#result").append('\
                    <div class="col-md-3" style="margin-bottom:5px">\
                        <button type="button" class="btn btn-danger btn-block" data-toggle="modal" data-target="#'+ip_nodot+'">'+key+'</button>\
                    </div>\
                    <div class="modal fade bs-example-modal-lg" id="'+ip_nodot+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\
                      <div class="modal-dialog modal-lg">\
                        <div class="modal-content">\
                          <div class="modal-header">\
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
                            <h4 class="modal-title" id="myModalLabel">'+key+'</h4>\
                          </div>\
                          <div class="modal-body">\
                            <pre>'+ret['result'][key]['cont']+'</pre>\
                          </div>\
                          <div class="modal-footer">\
                            <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>\
                          </div>\
                        </div>\
                      </div>\
                    </div>');
            };
        });
        $("#submit_history").removeAttr("disabled");
        $("#submit_history").html("提交");
    });
}