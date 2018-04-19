<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
<title>汇总统计</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=2.0, user-scalable=yes" />

<style type="text/css">

  html, body, div, span, object, iframe,
  h1, h2, h3, h4, h5, h6, p, blockquote, pre,
  abbr, address, cite, code,
  del, dfn, em, img, ins, kbd, q, samp,
  small, strong, sub, sup, var,
  b, i,
  dl, dt, dd, ol, ul, li,
  fieldset, form, label, legend,
  table, caption, tbody, tfoot, thead, tr, th, td {
    margin:0;
    padding:0;
    border:0;
    outline:0;
    font-size:100%;
    vertical-align:baseline;
    background:transparent;
  }

  body {
    margin:0;
    padding:0;
    font:12px/15px "Helvetica Neue",Arial, Helvetica, sans-serif;
    color: #555;
    background:#f5f5f5;
  }

  a {color:#666;}

  #content {width:100%; max-width:690px; margin:6% auto 0;}

  #btncontent {
    margin:10px;
    display:flex;
    justify-content:center;}

  table {
    overflow:hidden;
    border:1px solid #d3d3d3;
    background:#fefefe;
    width:70%;
    margin:5% auto 0;
    -moz-border-radius:5px; /* FF1+ */
    -webkit-border-radius:5px; /* Saf3-4 */
    border-radius:5px;
    -moz-box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
    -webkit-box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
  }

  th, td {padding:18px 28px 18px; text-align:center; }

  th {padding-top:22px; text-shadow: 1px 1px 1px #fff; background:#e8eaeb;}

  td {border-top:1px solid #e0e0e0; border-right:1px solid #e0e0e0;}

  tr.odd-row td {background:#f6f6f6;}

  td.first, th.first {text-align:left}

  td.last {border-right:none;}

  td {
    background: -moz-linear-gradient(100% 25% 90deg, #fefefe, #f9f9f9);
    background: -webkit-gradient(linear, 0% 0%, 0% 25%, from(#f9f9f9), to(#fefefe));
  }

  tr.odd-row td {
    background: -moz-linear-gradient(100% 25% 90deg, #f6f6f6, #f1f1f1);
    background: -webkit-gradient(linear, 0% 0%, 0% 25%, from(#f1f1f1), to(#f6f6f6));
  }

  th {
    background: -moz-linear-gradient(100% 20% 90deg, #e8eaeb, #ededed);
    background: -webkit-gradient(linear, 0% 0%, 0% 20%, from(#ededed), to(#e8eaeb));
  }

  tr:first-child th.first {
    -moz-border-radius-topleft:5px;
    -webkit-border-top-left-radius:5px; /* Saf3-4 */
  }

  tr:first-child th.last {
    -moz-border-radius-topright:5px;
    -webkit-border-top-right-radius:5px; /* Saf3-4 */
  }

  tr:last-child td.first {
    -moz-border-radius-bottomleft:5px;
    -webkit-border-bottom-left-radius:5px; /* Saf3-4 */
  }

  tr:last-child td.last {
    -moz-border-radius-bottomright:5px;
    -webkit-border-bottom-right-radius:5px; /* Saf3-4 */
  }

.button {
  display: inline-block;
  outline: none;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  font: 14px/100% Arial, Helvetica, sans-serif;
  padding: .5em 2em .55em;
  text-shadow: 0 1px 1px rgba(0,0,0,.3);
  -webkit-border-radius: .5em;
  -moz-border-radius: .5em;
  border-radius: .5em;
  -webkit-box-shadow: 0 1px 2px rgba(0,0,0,.2);
  -moz-box-shadow: 0 1px 2px rgba(0,0,0,.2);
  box-shadow: 0 1px 2px rgba(0,0,0,.2);
}
.button:hover {
  text-decoration: none;
}
.button:active {
  position: relative;
  top: 1px;
}

.orange {
  color: #fef4e9;
  border: solid 1px #da7c0c;
  background: #f78d1d;
  background: -webkit-gradient(linear, left top, left bottom, from(#faa51a), to(#f47a20));
  background: -moz-linear-gradient(top,  #faa51a,  #f47a20);
  filter:  progid:DXImageTransform.Microsoft.gradient(startColorstr='#faa51a', endColorstr='#f47a20');
}
.orange:hover {
  background: #f47c20;
  background: -webkit-gradient(linear, left top, left bottom, from(#f88e11), to(#f06015));
  background: -moz-linear-gradient(top,  #f88e11,  #f06015);
  filter:  progid:DXImageTransform.Microsoft.gradient(startColorstr='#f88e11', endColorstr='#f06015');
}
.orange:active {
  color: #fcd3a5;
  background: -webkit-gradient(linear, left top, left bottom, from(#f47a20), to(#faa51a));
  background: -moz-linear-gradient(top,  #f47a20,  #faa51a);
  filter:  progid:DXImageTransform.Microsoft.gradient(startColorstr='#f47a20', endColorstr='#faa51a');
}

</style>

</head>
<body>

<div id="content">

    <table cellspacing="0">
    <tr>
      <th nowrap>日期</th>
      <th nowrap>汇总表</th>
      <th nowrap>详情表</th>
      <th nowrap>空字段</th>
    </tr>

    <?php
    $con = mysql_connect("localhost:8889","stock","this is not mima");
    mysql_select_db("stockdb", $con);
    $sql="SELECT * FROM dailyCheck ORDER BY Fddate DESC LIMIT 8";
    $result = mysql_query($sql);
    while($row = mysql_fetch_array($result, MYSQL_ASSOC)){
    ?>
    <tr>
        <td nowrap><?php echo $row['Fddate']; ?></td>
        <td nowrap>
        <?php
        if ($row['Fdsumcount'] == 0){
          echo '<p style="color:red">';
        }
        echo $row['Fdsumcount'];
        ?>
        </td>
                <td nowrap>
        <?php
        if (($row['Fddetailcount'] == 0)||($row['Fddetailcount'] <> $row['Fdsumcount'])){
          echo '<p style="color:red">';
        }
        echo $row['Fddetailcount'];
        ?>
        </td>
        <td nowrap>
        <?php
        if ($row['Fdemptycount'] <> 0){
          echo '<p style="color:red">';
        }
        echo $row['Fdemptycount'];
        ?>
        </td>
    </tr>

    <?php
    }
    ?>
    </table>
</div>

<div id="btncontent">

<?php
    if(!empty($_POST['chaxun']))
    {//点击“同步数据”按钮后才执行
      $sql = "call stockdb.proc_stock();";
      mysql_query($sql);

      $emptyCount = 0;
      $tempDate = '2018-01-18';
      $sql="SELECT * FROM stockdb.auditionList ORDER BY Fadate";

      $result = mysql_query($sql);

      while($row = mysql_fetch_array($result, MYSQL_ASSOC))
      {
          if ($row['Fadate'] <> $tempDate){
              $sql = "UPDATE dailyCheck SET Fdemptycount = ".$emptyCount." WHERE Fddate ='".$tempDate."'";
              mysql_query($sql);
              $tempDate = $row['Fadate'];
              $emptyCount = 0;
          }
          if ($row['Fastockno']=='') {$emptyCount = $emptyCount + 1;}
          if ($row['Fastockname']=='') {$emptyCount = $emptyCount + 1;}
          if ($row['Facloseprice'] == 0) {$emptyCount = $emptyCount + 1;}
          if ($row['Faequity'] == 0) {$emptyCount = $emptyCount + 1;}
          if ($row['Fasection']=='') {$emptyCount = $emptyCount + 1;}
          if ($row['Falagmoney']=='') {$emptyCount = $emptyCount + 1;}
          if ($row['Famidmoney']=='') {$emptyCount = $emptyCount + 1;}
          if ($row['Fasmlmoney']=='') {$emptyCount = $emptyCount + 1;}
          if ($row['Facostdesc']=='') {$emptyCount = $emptyCount + 1;}
          if ($row['Factrldesc']=='') {$emptyCount = $emptyCount + 1;}
      }
      if ($row['Fadate'] <> $tempDate){
          $sql = "UPDATE dailyCheck SET Fdemptycount = ".$emptyCount." WHERE Fddate ='".$tempDate."'";
          mysql_query($sql);
      }

      echo "<script>location.href='admin.php'</script>";
    }
?>

  <form action="" method="post">
    <input class="button orange" type="hidden" name="chaxun" value="查询数据隐藏域" />
    <input class="button orange" type="submit" name="button" value="同步数据" />
  </form>

</div>

</body>
</html>