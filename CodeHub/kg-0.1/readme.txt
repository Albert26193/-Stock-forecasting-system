version 1.0
实现了先前仓库的部分功能，功能十分简陋

1
-------------------------------------------------------------------------------------
GetData.py 	从tushare库中获取信息
import_neo4j_csv.py	生产能用于neo4j构建的csv文件
--------------------------------------------------------------------------------------
生成的文件：
实体文件Person.csv		标签类型：Person 描述人	标签属性：id（md5加密生成的唯一识别序列）；name（这里加入年龄性别还需要一些额外的操作，暂时没加）
实体文件Stock.csv		标签类型：Stock	描述股票/公司	标签属性：id；代码；名称；行业；市场板块
关系文件Person_Stock.csv 	标签类型：employ_of 	标签属性（关系种类）：chairman_of；manager_of；secretary_of

--------------------------------------------------------------------------------------------


2
----------------------------------------------------------------------------------------------
利用这些文件导入neo4j图数据库

开启neo4j服务
在cmd窗口输入：
neo4j_home$ bin/neo4j-admin import --nodes Person.csv --nodes Stock.csv -- relationships Person_Stock.csv   (neo4j的批量导入功能)
打开console浏览器服务器可以查看图形

以上是我估计的步骤，我自己neo4j安装出了些问题，大家可以试一试数据是否可以。数据形式和这个命令我都是根据参考的仓库来的，没有查看官方文档。
(参考仓库link : https://github.com/lemonhu/stock-knowledge-graph)

------------------------------------------------------------------------------------------------------------------


3
-------------------------------------------------------------------------------------------------------
这个版本实现了仓库的大致功能，但是都是得由python获取生产csv再拿来构建，且无法体现股票交易数据
后续的想法：
1.不清楚股票的实时数据怎么体现在neo4j中，至少历史行情数据觉得无法体现在图数据库中，毕竟量太多需要的键值对太多。或者是 {历史行情：一个历史行情的csv文件}，不清楚图数据库是否能以一个数据文件作为值。
2.动态部分：
	2.1 把上述这个过程不需要手动实现，由程序自动完成导入工作
	2.2 加入一些动态监控的部分，比如公司的法人发生变化了，就实时对neo4j单个实体进行修改（整个重新构建肯定浪费）
	2.3 动态监控的部分，可能需要将数据库和程序部署在服务器上连轴跑，服务器的操作后续还需要学习
----------------------------------------------------------------------------------------------------------------


4
------------------------------------------------------------------------------------------------------
程序里部分我写了注释，有空的同学可以稍微了解一下这个过程，十分易懂。大家多多交流 :)

