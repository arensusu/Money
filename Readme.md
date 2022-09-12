# 記帳小幫手 - 馬尼

本專案使用 AWS Lambda 及 DynamoDB 部署 Line Bot 機器人，提供簡易的記帳功能。

# 指令

## 紀錄支出

功能：將支出記錄在帳本之中。

使用者 項目 價格

ex: 阿任 珍珠奶茶 50

馬尼回覆 "已存入" 代表此筆支出成功紀錄。

## 支出結算

功能：查閱週期內的總支出及各項目的支出金額。

使用者 週期[ 週結算 | 月結算 | 年結算 ] 數值

週結算：訊息當月份指定週數的結算

    第一週：每月 1 號到 7 號
    第二週：每月 8 號到 14 號
    第三週：每月 15 號到 21 號
    第四週：每月 22 號到 31 號

月結算：訊息當年度指定月份的結算

年結算：指定年度的結算

ex: 阿任 月結算 9

馬尼回覆當年度 9 月的支出結算