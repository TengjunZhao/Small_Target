
<
t
e
m
p
l
a
t
e
>


 
 
<
d
i
v
 
c
l
a
s
s
=
"
p
r
o
j
e
c
t
-
m
a
n
a
g
e
m
e
n
t
-
c
o
n
t
a
i
n
e
r
"
>


 
 
 
 
<
!
-
-
 
头
部
导
航
 
-
-
>


 
 
 
 
<
e
l
-
p
a
g
e
-
h
e
a
d
e
r
 
@
b
a
c
k
=
"
g
o
B
a
c
k
"
 
t
i
t
l
e
=
"
返
回
主
页
"
>


 
 
 
 
 
 
<
t
e
m
p
l
a
t
e
 
#
c
o
n
t
e
n
t
>


 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
t
e
x
t
-
l
a
r
g
e
 
f
o
n
t
-
6
0
0
 
m
r
-
3
"
>
 
项
目
管
理
系
统
 
<
/
s
p
a
n
>


 
 
 
 
 
 
<
/
t
e
m
p
l
a
t
e
>


 
 
 
 
<
/
e
l
-
p
a
g
e
-
h
e
a
d
e
r
>




 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
m
a
i
n
-
c
o
n
t
e
n
t
"
>


 
 
 
 
 
 
<
!
-
-
 
项
目
列
表
区
域
 
-
-
>


 
 
 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
p
r
o
j
e
c
t
-
l
i
s
t
-
s
e
c
t
i
o
n
"
>


 
 
 
 
 
 
 
 
<
e
l
-
c
a
r
d
 
c
l
a
s
s
=
"
b
o
x
-
c
a
r
d
"
>


 
 
 
 
 
 
 
 
 
 
<
t
e
m
p
l
a
t
e
 
#
h
e
a
d
e
r
>


 
 
 
 
 
 
 
 
 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
c
a
r
d
-
h
e
a
d
e
r
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
>
项
目
列
表
<
/
s
p
a
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
t
y
p
e
=
"
p
r
i
m
a
r
y
"
 
@
c
l
i
c
k
=
"
s
h
o
w
C
r
e
a
t
e
D
i
a
l
o
g
 
=
 
t
r
u
e
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
c
o
n
>
<
P
l
u
s
 
/
>
<
/
e
l
-
i
c
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
b
t
n
-
t
e
x
t
"
>
新
建
项
目
<
/
s
p
a
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
<
/
d
i
v
>


 
 
 
 
 
 
 
 
 
 
<
/
t
e
m
p
l
a
t
e
>




 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
a
b
l
e


 
 
 
 
 
 
 
 
 
 
 
 
:
d
a
t
a
=
"
p
r
o
j
e
c
t
s
"


 
 
 
 
 
 
 
 
 
 
 
 
s
t
y
l
e
=
"
w
i
d
t
h
:
 
1
0
0
%
"


 
 
 
 
 
 
 
 
 
 
 
 
@
r
o
w
-
c
l
i
c
k
=
"
s
e
l
e
c
t
P
r
o
j
e
c
t
"


 
 
 
 
 
 
 
 
 
 
 
 
:
r
o
w
-
c
l
a
s
s
-
n
a
m
e
=
"
t
a
b
l
e
R
o
w
C
l
a
s
s
N
a
m
e
"


 
 
 
 
 
 
 
 
 
 
 
 
h
i
g
h
l
i
g
h
t
-
c
u
r
r
e
n
t
-
r
o
w


 
 
 
 
 
 
 
 
 
 
 
 
:
f
i
t
=
"
t
r
u
e
"


 
 
 
 
 
 
 
 
 
 
 
 
s
i
z
e
=
"
s
m
a
l
l
"


 
 
 
 
 
 
 
 
 
 
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
a
b
l
e
-
c
o
l
u
m
n
 
p
r
o
p
=
"
n
a
m
e
"
 
l
a
b
e
l
=
"
项
目
名
称
"
 
m
i
n
-
w
i
d
t
h
=
"
1
2
0
"
 
/
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
a
b
l
e
-
c
o
l
u
m
n
 
p
r
o
p
=
"
d
e
s
c
r
i
p
t
i
o
n
"
 
l
a
b
e
l
=
"
描
述
"
 
m
i
n
-
w
i
d
t
h
=
"
1
5
0
"
 
s
h
o
w
-
o
v
e
r
f
l
o
w
-
t
o
o
l
t
i
p
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
t
e
m
p
l
a
t
e
 
#
d
e
f
a
u
l
t
=
"
s
c
o
p
e
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
t
r
u
n
c
a
t
e
-
t
e
x
t
"
>
{
{
 
s
c
o
p
e
.
r
o
w
.
d
e
s
c
r
i
p
t
i
o
n
 
}
}
<
/
s
p
a
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
t
e
m
p
l
a
t
e
>


 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
t
a
b
l
e
-
c
o
l
u
m
n
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
a
b
l
e
-
c
o
l
u
m
n
 
p
r
o
p
=
"
s
t
a
r
t
_
d
a
t
e
"
 
l
a
b
e
l
=
"
开
始
日
期
"
 
w
i
d
t
h
=
"
1
0
0
"
 
/
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
a
b
l
e
-
c
o
l
u
m
n
 
p
r
o
p
=
"
e
n
d
_
d
a
t
e
"
 
l
a
b
e
l
=
"
结
束
日
期
"
 
w
i
d
t
h
=
"
1
0
0
"
 
/
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
a
b
l
e
-
c
o
l
u
m
n
 
l
a
b
e
l
=
"
状
态
"
 
w
i
d
t
h
=
"
8
0
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
t
e
m
p
l
a
t
e
 
#
d
e
f
a
u
l
t
=
"
s
c
o
p
e
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
a
g
 
:
t
y
p
e
=
"
s
c
o
p
e
.
r
o
w
.
i
s
_
a
c
t
i
v
e
 
?
 
'
s
u
c
c
e
s
s
'
 
:
 
'
i
n
f
o
'
"
 
s
i
z
e
=
"
s
m
a
l
l
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
{
{
 
s
c
o
p
e
.
r
o
w
.
i
s
_
a
c
t
i
v
e
 
?
 
'
进
行
中
'
 
:
 
'
已
结
束
'
 
}
}


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
t
a
g
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
t
e
m
p
l
a
t
e
>


 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
t
a
b
l
e
-
c
o
l
u
m
n
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
a
b
l
e
-
c
o
l
u
m
n
 
l
a
b
e
l
=
"
操
作
"
 
w
i
d
t
h
=
"
2
0
0
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
t
e
m
p
l
a
t
e
 
#
d
e
f
a
u
l
t
=
"
s
c
o
p
e
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
用
 
f
l
e
x
 
容
器
包
裹
两
个
按
钮
，
确
保
水
平
排
列
 
-
-
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
t
a
b
l
e
-
o
p
e
r
a
t
i
o
n
-
b
u
t
t
o
n
s
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
s
i
z
e
=
"
m
i
n
i
"
 
@
c
l
i
c
k
.
s
t
o
p
=
"
e
d
i
t
P
r
o
j
e
c
t
(
s
c
o
p
e
.
r
o
w
)
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
c
o
n
>
<
E
d
i
t
 
/
>
<
/
e
l
-
i
c
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
b
t
n
-
t
e
x
t
"
>
编
辑
<
/
s
p
a
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
s
i
z
e
=
"
m
i
n
i
"
 
t
y
p
e
=
"
d
a
n
g
e
r
"
 
@
c
l
i
c
k
.
s
t
o
p
=
"
d
e
l
e
t
e
P
r
o
j
e
c
t
(
s
c
o
p
e
.
r
o
w
)
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
c
o
n
>
<
D
e
l
e
t
e
 
/
>
<
/
e
l
-
i
c
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
b
t
n
-
t
e
x
t
"
>
删
除
<
/
s
p
a
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
d
i
v
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
t
e
m
p
l
a
t
e
>


 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
t
a
b
l
e
-
c
o
l
u
m
n
>


 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
t
a
b
l
e
>


 
 
 
 
 
 
 
 
<
/
e
l
-
c
a
r
d
>


 
 
 
 
 
 
<
/
d
i
v
>




 
 
 
 
 
 
<
!
-
-
 
项
目
详
情
区
域
 
-
 
新
增
选
项
卡
切
换
 
-
-
>


 
 
 
 
 
 
<
d
i
v
 
v
-
i
f
=
"
s
e
l
e
c
t
e
d
P
r
o
j
e
c
t
"
 
c
l
a
s
s
=
"
p
r
o
j
e
c
t
-
d
e
t
a
i
l
-
s
e
c
t
i
o
n
"
>


 
 
 
 
 
 
 
 
<
e
l
-
c
a
r
d
 
c
l
a
s
s
=
"
b
o
x
-
c
a
r
d
"
>


 
 
 
 
 
 
 
 
 
 
<
t
e
m
p
l
a
t
e
 
#
h
e
a
d
e
r
>


 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
>
项
目
详
情
：
{
{
 
s
e
l
e
c
t
e
d
P
r
o
j
e
c
t
.
n
a
m
e
 
}
}
<
/
s
p
a
n
>


 
 
 
 
 
 
 
 
 
 
<
/
t
e
m
p
l
a
t
e
>




 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
核
心
：
选
项
卡
组
件
 
-
-
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
a
b
s
 
v
-
m
o
d
e
l
=
"
a
c
t
i
v
e
T
a
b
"
 
c
l
a
s
s
=
"
w
-
f
u
l
l
"
 
t
y
p
e
=
"
c
a
r
d
"
>


 
 
 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
甘
特
图
选
项
卡
 
-
-
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
a
b
-
p
a
n
e
 
l
a
b
e
l
=
"
甘
特
图
"
 
n
a
m
e
=
"
g
a
n
t
t
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
g
a
n
t
t
-
c
o
n
t
a
i
n
e
r
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
d
i
v
 
r
e
f
=
"
g
a
n
t
t
R
e
f
"
 
c
l
a
s
s
=
"
g
a
n
t
t
-
c
o
n
t
e
n
t
"
>
<
/
d
i
v
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
m
t
-
4
 
f
l
e
x
 
g
a
p
-
2
 
f
l
e
x
-
w
r
a
p
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
@
c
l
i
c
k
=
"
c
h
a
n
g
e
V
i
e
w
(
'
D
a
y
'
)
"
 
s
i
z
e
=
"
s
m
a
l
l
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
c
o
n
>
<
C
a
l
e
n
d
a
r
 
/
>
<
/
e
l
-
i
c
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
b
t
n
-
t
e
x
t
"
>
日
视
图
<
/
s
p
a
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
@
c
l
i
c
k
=
"
c
h
a
n
g
e
V
i
e
w
(
'
M
o
n
t
h
'
)
"
 
s
i
z
e
=
"
s
m
a
l
l
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
c
o
n
>
<
C
a
l
e
n
d
a
r
 
/
>
<
/
e
l
-
i
c
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
b
t
n
-
t
e
x
t
"
>
月
视
图
<
/
s
p
a
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
d
i
v
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
d
i
v
>


 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
t
a
b
-
p
a
n
e
>




 
 
 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
任
务
分
解
树
选
项
卡
 
-
-
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
a
b
-
p
a
n
e
 
l
a
b
e
l
=
"
任
务
分
解
树
"
 
n
a
m
e
=
"
t
a
s
k
T
r
e
e
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
t
a
s
k
-
t
r
e
e
-
c
o
n
t
a
i
n
e
r
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
t
y
p
e
=
"
p
r
i
m
a
r
y
"
 
s
i
z
e
=
"
s
m
a
l
l
"
 
@
c
l
i
c
k
=
"
s
h
o
w
T
a
s
k
D
i
a
l
o
g
 
=
 
t
r
u
e
;
 
e
d
i
t
i
n
g
T
a
s
k
 
=
 
n
u
l
l
;
 
c
u
r
r
e
n
t
P
a
r
e
n
t
T
a
s
k
 
=
 
n
u
l
l
;
 
r
e
s
e
t
T
a
s
k
F
o
r
m
(
)
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
c
o
n
>
<
P
l
u
s
 
/
>
<
/
e
l
-
i
c
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
b
t
n
-
t
e
x
t
"
>
新
增
任
务
<
/
s
p
a
n
>




 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
任
务
操
作
按
钮
 
-
-
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
m
b
-
4
 
f
l
e
x
 
g
a
p
-
2
 
f
l
e
x
-
w
r
a
p
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
t
y
p
e
=
"
p
r
i
m
a
r
y
"
 
s
i
z
e
=
"
s
m
a
l
l
"
 
@
c
l
i
c
k
=
"
s
h
o
w
T
a
s
k
D
i
a
l
o
g
 
=
 
t
r
u
e
;
 
e
d
i
t
i
n
g
T
a
s
k
 
=
 
n
u
l
l
;
 
c
u
r
r
e
n
t
P
a
r
e
n
t
T
a
s
k
 
=
 
n
u
l
l
;
 
r
e
s
e
t
T
a
s
k
F
o
r
m
(
)
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
c
o
n
>
<
P
l
u
s
 
/
>
<
/
e
l
-
i
c
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
b
t
n
-
t
e
x
t
"
>
新
增
任
务
<
/
s
p
a
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
b
u
t
t
o
n
>


=
=
=
=
=
=
=


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
t
y
p
e
=
"
p
r
i
m
a
r
y
"
 
s
i
z
e
=
"
s
m
a
l
l
"
 
@
c
l
i
c
k
=
"
s
h
o
w
T
a
s
k
D
i
a
l
o
g
 
=
 
t
r
u
e
;
 
e
d
i
t
i
n
g
T
a
s
k
 
=
 
n
u
l
l
;
 
c
u
r
r
e
n
t
P
a
r
e
n
t
T
a
s
k
 
=
 
n
u
l
l
;
 
r
e
s
e
t
T
a
s
k
F
o
r
m
(
)
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
c
o
n
>
<
P
l
u
s
 
/
>
<
/
e
l
-
i
c
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
b
t
n
-
t
e
x
t
"
>
新
增
任
务
<
/
s
p
a
n
>




 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
s
i
z
e
=
"
s
m
a
l
l
"
 
@
c
l
i
c
k
=
"
r
e
f
r
e
s
h
T
a
s
k
T
r
e
e
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
c
o
n
>
<
R
e
f
r
e
s
h
 
/
>
<
/
e
l
-
i
c
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
b
t
n
-
t
e
x
t
"
>
刷
新
<
/
s
p
a
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
@
c
l
i
c
k
=
"
e
x
p
a
n
d
A
l
l
N
o
d
e
s
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
展
开
全
部


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
@
c
l
i
c
k
=
"
c
o
l
l
a
p
s
e
A
l
l
N
o
d
e
s
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
折
叠
全
部


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
@
c
l
i
c
k
=
"
c
o
n
s
o
l
e
.
l
o
g
(
'
当
前
展
开
的
节
点
:
'
,
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
)
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
查
看
展
开
状
态


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
d
i
v
>




 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
任
务
树
形
组
件
 
-
-
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
d
e
f
a
u
l
t
-
e
x
p
a
n
d
-
a
l
l


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
c
l
a
s
s
=
"
t
a
s
k
-
t
r
e
e
-
c
o
n
t
e
n
t
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
:
e
x
p
a
n
d
-
o
n
-
c
l
i
c
k
-
n
o
d
e
=
"
f
a
l
s
e
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
s
i
z
e
=
"
s
m
a
l
l
"




 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
r
e
e


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
:
d
a
t
a
=
"
t
a
s
k
T
r
e
e
D
a
t
a
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
:
p
r
o
p
s
=
"
t
r
e
e
P
r
o
p
s
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
n
o
d
e
-
k
e
y
=
"
i
d
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
:
d
e
f
a
u
l
t
-
e
x
p
a
n
d
e
d
-
k
e
y
s
=
"
e
x
p
a
n
d
e
d
K
e
y
s
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
c
l
a
s
s
=
"
w
-
f
u
l
l
 
h
-
f
u
l
l
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
:
e
x
p
a
n
d
-
o
n
-
c
l
i
c
k
-
n
o
d
e
=
"
f
a
l
s
e
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
@
n
o
d
e
-
e
x
p
a
n
d
=
"
h
a
n
d
l
e
N
o
d
e
E
x
p
a
n
d
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
@
n
o
d
e
-
c
o
l
l
a
p
s
e
=
"
h
a
n
d
l
e
N
o
d
e
C
o
l
l
a
p
s
e
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
>


=
=
=
=
=
=
=


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
d
e
f
a
u
l
t
-
e
x
p
a
n
d
-
a
l
l


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
c
l
a
s
s
=
"
t
a
s
k
-
t
r
e
e
-
c
o
n
t
e
n
t
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
:
e
x
p
a
n
d
-
o
n
-
c
l
i
c
k
-
n
o
d
e
=
"
f
a
l
s
e
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
s
i
z
e
=
"
s
m
a
l
l
"




 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
自
定
义
树
形
节
点
内
容
 
-
-
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
t
e
m
p
l
a
t
e
 
#
d
e
f
a
u
l
t
=
"
{
 
n
o
d
e
,
 
d
a
t
a
 
}
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
t
r
e
e
-
n
o
d
e
-
c
o
n
t
e
n
t
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
n
o
d
e
-
l
e
f
t
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
状
态
标
签
 
-
-
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
a
g


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
:
t
y
p
e
=
"
d
a
t
a
.
s
t
a
t
u
s
 
=
=
=
 
'
已
完
成
'
 
?
 
'
s
u
c
c
e
s
s
'
 
:


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
d
a
t
a
.
s
t
a
t
u
s
 
=
=
=
 
'
进
行
中
'
 
?
 
'
w
a
r
n
i
n
g
'
 
:
 
'
i
n
f
o
'
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
s
i
z
e
=
"
m
i
n
i
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
c
l
a
s
s
=
"
m
r
-
2
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
{
{
 
d
a
t
a
.
s
t
a
t
u
s
 
}
}


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
t
a
g
>




 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
任
务
名
称
 
-
-
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
f
o
n
t
-
m
e
d
i
u
m
 
t
r
u
n
c
a
t
e
"
 
:
t
i
t
l
e
=
"
n
o
d
e
.
l
a
b
e
l
 
+
 
(
d
a
t
a
.
d
e
s
c
r
i
p
t
i
o
n
 
?
 
'
 
-
 
'
 
+
 
d
a
t
a
.
d
e
s
c
r
i
p
t
i
o
n
 
:
 
'
'
)
"
>
{
{
 
n
o
d
e
.
l
a
b
e
l
 
}
}
<
/
s
p
a
n
>




 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
优
先
级
标
签
（
移
动
端
隐
藏
）
 
-
-
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
t
a
g


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
v
-
i
f
=
"
d
a
t
a
.
p
r
i
o
r
i
t
y
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
:
t
y
p
e
=
"
d
a
t
a
.
p
r
i
o
r
i
t
y
 
=
=
=
 
3
 
?
 
'
d
a
n
g
e
r
'
 
:


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
d
a
t
a
.
p
r
i
o
r
i
t
y
 
=
=
=
 
2
 
?
 
'
w
a
r
n
i
n
g
'
 
:
 
'
i
n
f
o
'
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
s
i
z
e
=
"
m
i
n
i
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
e
f
f
e
c
t
=
"
p
l
a
i
n
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
c
l
a
s
s
=
"
m
l
-
2
 
p
r
i
o
r
i
t
y
-
t
a
g
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
{
{
 
d
a
t
a
.
p
r
i
o
r
i
t
y
 
=
=
=
 
3
 
?
 
'
高
'
 
:
 
d
a
t
a
.
p
r
i
o
r
i
t
y
 
=
=
=
 
2
 
?
 
'
中
'
 
:
 
'
低
'
 
}
}


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
t
a
g
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
d
i
v
>




 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
右
侧
信
息
 
-
-
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
n
o
d
e
-
r
i
g
h
t
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
进
度
（
简
化
显
示
）
 
-
-
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
t
e
x
t
-
x
s
 
p
r
o
g
r
e
s
s
-
t
e
x
t
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
{
{
 
d
a
t
a
.
p
r
o
g
r
e
s
s
 
}
}
%


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
s
p
a
n
>




 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
操
作
按
钮
 
-
-
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
n
o
d
e
-
a
c
t
i
o
n
s
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
t
y
p
e
=
"
p
r
i
m
a
r
y
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
s
i
z
e
=
"
m
i
n
i
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
@
c
l
i
c
k
.
s
t
o
p
=
"
e
d
i
t
T
a
s
k
(
d
a
t
a
)
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
i
c
o
n
=
"
E
d
i
t
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
c
i
r
c
l
e


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
t
i
t
l
e
=
"
编
辑
任
务
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
/
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
t
y
p
e
=
"
s
u
c
c
e
s
s
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
s
i
z
e
=
"
m
i
n
i
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
@
c
l
i
c
k
.
s
t
o
p
=
"
a
d
d
C
h
i
l
d
T
a
s
k
(
d
a
t
a
)
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
i
c
o
n
=
"
P
l
u
s
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
c
i
r
c
l
e


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
t
i
t
l
e
=
"
添
加
子
任
务
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
/
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
t
y
p
e
=
"
d
a
n
g
e
r
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
s
i
z
e
=
"
m
i
n
i
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
@
c
l
i
c
k
.
s
t
o
p
=
"
d
e
l
e
t
e
T
a
s
k
(
d
a
t
a
)
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
i
c
o
n
=
"
D
e
l
e
t
e
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
c
i
r
c
l
e


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
t
i
t
l
e
=
"
删
除
任
务
"


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
/
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
d
i
v
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
d
i
v
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
d
i
v
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
t
e
m
p
l
a
t
e
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
t
r
e
e
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
/
d
i
v
>


 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
t
a
b
-
p
a
n
e
>


 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
t
a
b
s
>




 
 
 
 
 
 
 
 
 
 
<
!
-
-
 
返
回
按
钮
 
-
-
>


 
 
 
 
 
 
 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
m
t
-
4
 
f
l
e
x
 
j
u
s
t
i
f
y
-
e
n
d
"
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
t
y
p
e
=
"
p
r
i
m
a
r
y
"
 
s
i
z
e
=
"
s
m
a
l
l
"
 
@
c
l
i
c
k
=
"
h
a
n
d
l
e
B
a
c
k
"
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
c
o
n
>
<
A
r
r
o
w
L
e
f
t
 
/
>
<
/
e
l
-
i
c
o
n
>


 
 
 
 
 
 
 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
b
t
n
-
t
e
x
t
"
>
返
回
列
表
<
/
s
p
a
n
>


 
 
 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
<
/
d
i
v
>


 
 
 
 
 
 
 
 
<
/
e
l
-
c
a
r
d
>


 
 
 
 
 
 
<
/
d
i
v
>


 
 
 
 
<
/
d
i
v
>




 
 
 
 
<
!
-
-
 
创
建
/
编
辑
项
目
对
话
框
 
-
-
>


 
 
 
 
<
e
l
-
d
i
a
l
o
g
 
v
-
m
o
d
e
l
=
"
s
h
o
w
C
r
e
a
t
e
D
i
a
l
o
g
"
 
:
t
i
t
l
e
=
"
e
d
i
t
i
n
g
P
r
o
j
e
c
t
 
?
 
'
编
辑
项
目
'
 
:
 
'
新
建
项
目
'
"
 
w
i
d
t
h
=
"
9
0
%
"
 
m
a
x
-
w
i
d
t
h
=
"
5
0
0
p
x
"
>


 
 
 
 
 
 
<
e
l
-
f
o
r
m
 
:
m
o
d
e
l
=
"
p
r
o
j
e
c
t
F
o
r
m
"
 
:
r
u
l
e
s
=
"
p
r
o
j
e
c
t
R
u
l
e
s
"
 
r
e
f
=
"
p
r
o
j
e
c
t
F
o
r
m
R
e
f
"
 
l
a
b
e
l
-
w
i
d
t
h
=
"
8
0
p
x
"
 
s
i
z
e
=
"
s
m
a
l
l
"
>


 
 
 
 
 
 
 
 
<
e
l
-
f
o
r
m
-
i
t
e
m
 
l
a
b
e
l
=
"
项
目
名
称
"
 
p
r
o
p
=
"
n
a
m
e
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
n
p
u
t
 
v
-
m
o
d
e
l
=
"
p
r
o
j
e
c
t
F
o
r
m
.
n
a
m
e
"
 
/
>


 
 
 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
-
i
t
e
m
>


 
 
 
 
 
 
 
 
<
e
l
-
f
o
r
m
-
i
t
e
m
 
l
a
b
e
l
=
"
描
述
"
 
p
r
o
p
=
"
d
e
s
c
r
i
p
t
i
o
n
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
n
p
u
t
 
v
-
m
o
d
e
l
=
"
p
r
o
j
e
c
t
F
o
r
m
.
d
e
s
c
r
i
p
t
i
o
n
"
 
t
y
p
e
=
"
t
e
x
t
a
r
e
a
"
 
:
r
o
w
s
=
"
2
"
 
/
>


 
 
 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
-
i
t
e
m
>


 
 
 
 
 
 
 
 
<
e
l
-
f
o
r
m
-
i
t
e
m
 
l
a
b
e
l
=
"
开
始
日
期
"
 
p
r
o
p
=
"
s
t
a
r
t
_
d
a
t
e
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
d
a
t
e
-
p
i
c
k
e
r
 
v
-
m
o
d
e
l
=
"
p
r
o
j
e
c
t
F
o
r
m
.
s
t
a
r
t
_
d
a
t
e
"
 
t
y
p
e
=
"
d
a
t
e
"
 
p
l
a
c
e
h
o
l
d
e
r
=
"
选
择
开
始
日
期
"
 
/
>


 
 
 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
-
i
t
e
m
>


 
 
 
 
 
 
 
 
<
e
l
-
f
o
r
m
-
i
t
e
m
 
l
a
b
e
l
=
"
结
束
日
期
"
 
p
r
o
p
=
"
e
n
d
_
d
a
t
e
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
d
a
t
e
-
p
i
c
k
e
r
 
v
-
m
o
d
e
l
=
"
p
r
o
j
e
c
t
F
o
r
m
.
e
n
d
_
d
a
t
e
"
 
t
y
p
e
=
"
d
a
t
e
"
 
p
l
a
c
e
h
o
l
d
e
r
=
"
选
择
结
束
日
期
"
 
/
>


 
 
 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
-
i
t
e
m
>


 
 
 
 
 
 
 
 
<
e
l
-
f
o
r
m
-
i
t
e
m
 
l
a
b
e
l
=
"
负
责
人
"
 
p
r
o
p
=
"
o
w
n
e
r
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
s
e
l
e
c
t
 
v
-
m
o
d
e
l
=
"
p
r
o
j
e
c
t
F
o
r
m
.
o
w
n
e
r
"
 
p
l
a
c
e
h
o
l
d
e
r
=
"
选
择
负
责
人
"
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
o
p
t
i
o
n
 
l
a
b
e
l
=
"
管
理
员
"
 
:
v
a
l
u
e
=
"
1
"
 
/
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
o
p
t
i
o
n
 
l
a
b
e
l
=
"
用
户
1
"
 
:
v
a
l
u
e
=
"
2
"
 
/
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
o
p
t
i
o
n
 
l
a
b
e
l
=
"
用
户
2
"
 
:
v
a
l
u
e
=
"
3
"
 
/
>


 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
s
e
l
e
c
t
>


 
 
 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
-
i
t
e
m
>


 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
>


 
 
 
 
 
 
<
t
e
m
p
l
a
t
e
 
#
f
o
o
t
e
r
>


 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
d
i
a
l
o
g
-
f
o
o
t
e
r
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
s
i
z
e
=
"
s
m
a
l
l
"
 
@
c
l
i
c
k
=
"
s
h
o
w
C
r
e
a
t
e
D
i
a
l
o
g
 
=
 
f
a
l
s
e
"
>
取
消
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
t
y
p
e
=
"
p
r
i
m
a
r
y
"
 
s
i
z
e
=
"
s
m
a
l
l
"
 
@
c
l
i
c
k
=
"
s
a
v
e
P
r
o
j
e
c
t
"
>
保
存
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
<
/
s
p
a
n
>


 
 
 
 
 
 
<
/
t
e
m
p
l
a
t
e
>


 
 
 
 
<
/
e
l
-
d
i
a
l
o
g
>




 
 
 
 
<
!
-
-
 
任
务
对
话
框
 
-
-
>


 
 
 
 
<
e
l
-
d
i
a
l
o
g


 
 
 
 
 
 
v
-
m
o
d
e
l
=
"
s
h
o
w
T
a
s
k
D
i
a
l
o
g
"


 
 
 
 
 
 
:
t
i
t
l
e
=
"
e
d
i
t
i
n
g
T
a
s
k
 
?
 
'
编
辑
任
务
'
 
:
 
(
c
u
r
r
e
n
t
P
a
r
e
n
t
T
a
s
k
 
?
 
'
添
加
子
任
务
'
 
:
 
'
新
增
任
务
'
)
"


 
 
 
 
 
 
w
i
d
t
h
=
"
9
0
%
"


 
 
 
 
 
 
m
a
x
-
w
i
d
t
h
=
"
5
0
0
p
x
"


 
 
 
 
>


 
 
 
 
 
 
<
e
l
-
f
o
r
m
 
:
m
o
d
e
l
=
"
t
a
s
k
F
o
r
m
"
 
:
r
u
l
e
s
=
"
t
a
s
k
R
u
l
e
s
"
 
r
e
f
=
"
t
a
s
k
F
o
r
m
R
e
f
"
 
l
a
b
e
l
-
w
i
d
t
h
=
"
8
0
p
x
"
 
s
i
z
e
=
"
s
m
a
l
l
"
>


 
 
 
 
 
 
 
 
<
e
l
-
f
o
r
m
-
i
t
e
m
 
l
a
b
e
l
=
"
任
务
名
称
"
 
p
r
o
p
=
"
n
a
m
e
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
n
p
u
t
 
v
-
m
o
d
e
l
=
"
t
a
s
k
F
o
r
m
.
n
a
m
e
"
 
/
>


 
 
 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
-
i
t
e
m
>


 
 
 
 
 
 
 
 
<
e
l
-
f
o
r
m
-
i
t
e
m
 
l
a
b
e
l
=
"
描
述
"
 
p
r
o
p
=
"
d
e
s
c
r
i
p
t
i
o
n
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
n
p
u
t
 
v
-
m
o
d
e
l
=
"
t
a
s
k
F
o
r
m
.
d
e
s
c
r
i
p
t
i
o
n
"
 
t
y
p
e
=
"
t
e
x
t
a
r
e
a
"
 
:
r
o
w
s
=
"
2
"
 
/
>


 
 
 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
-
i
t
e
m
>


 
 
 
 
 
 
 
 
<
e
l
-
f
o
r
m
-
i
t
e
m
 
l
a
b
e
l
=
"
开
始
日
期
"
 
p
r
o
p
=
"
s
t
a
r
t
_
d
a
t
e
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
d
a
t
e
-
p
i
c
k
e
r
 
v
-
m
o
d
e
l
=
"
t
a
s
k
F
o
r
m
.
s
t
a
r
t
_
d
a
t
e
"
 
t
y
p
e
=
"
d
a
t
e
"
 
p
l
a
c
e
h
o
l
d
e
r
=
"
选
择
开
始
日
期
"
 
/
>


 
 
 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
-
i
t
e
m
>


 
 
 
 
 
 
 
 
<
e
l
-
f
o
r
m
-
i
t
e
m
 
l
a
b
e
l
=
"
结
束
日
期
"
 
p
r
o
p
=
"
e
n
d
_
d
a
t
e
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
d
a
t
e
-
p
i
c
k
e
r
 
v
-
m
o
d
e
l
=
"
t
a
s
k
F
o
r
m
.
e
n
d
_
d
a
t
e
"
 
t
y
p
e
=
"
d
a
t
e
"
 
p
l
a
c
e
h
o
l
d
e
r
=
"
选
择
结
束
日
期
"
 
/
>


 
 
 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
-
i
t
e
m
>


 
 
 
 
 
 
 
 
<
e
l
-
f
o
r
m
-
i
t
e
m
 
l
a
b
e
l
=
"
持
续
天
数
"
 
p
r
o
p
=
"
d
u
r
a
t
i
o
n
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
i
n
p
u
t
-
n
u
m
b
e
r
 
v
-
m
o
d
e
l
=
"
t
a
s
k
F
o
r
m
.
d
u
r
a
t
i
o
n
"
 
:
m
i
n
=
"
1
"
 
s
i
z
e
=
"
s
m
a
l
l
"
 
/
>


 
 
 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
-
i
t
e
m
>


 
 
 
 
 
 
 
 
<
e
l
-
f
o
r
m
-
i
t
e
m
 
l
a
b
e
l
=
"
进
度
"
 
p
r
o
p
=
"
p
r
o
g
r
e
s
s
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
s
l
i
d
e
r
 
v
-
m
o
d
e
l
=
"
t
a
s
k
F
o
r
m
.
p
r
o
g
r
e
s
s
"
 
:
m
a
x
=
"
1
0
0
"
 
s
h
o
w
-
i
n
p
u
t
 
s
i
z
e
=
"
s
m
a
l
l
"
 
/
>


 
 
 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
-
i
t
e
m
>


 
 
 
 
 
 
 
 
<
e
l
-
f
o
r
m
-
i
t
e
m
 
l
a
b
e
l
=
"
优
先
级
"
 
p
r
o
p
=
"
p
r
i
o
r
i
t
y
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
s
e
l
e
c
t
 
v
-
m
o
d
e
l
=
"
t
a
s
k
F
o
r
m
.
p
r
i
o
r
i
t
y
"
 
s
i
z
e
=
"
s
m
a
l
l
"
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
o
p
t
i
o
n
 
l
a
b
e
l
=
"
低
"
 
:
v
a
l
u
e
=
"
1
"
 
/
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
o
p
t
i
o
n
 
l
a
b
e
l
=
"
中
"
 
:
v
a
l
u
e
=
"
2
"
 
/
>


 
 
 
 
 
 
 
 
 
 
 
 
<
e
l
-
o
p
t
i
o
n
 
l
a
b
e
l
=
"
高
"
 
:
v
a
l
u
e
=
"
3
"
 
/
>


 
 
 
 
 
 
 
 
 
 
<
/
e
l
-
s
e
l
e
c
t
>


 
 
 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
-
i
t
e
m
>


 
 
 
 
 
 
<
/
e
l
-
f
o
r
m
>


 
 
 
 
 
 
<
t
e
m
p
l
a
t
e
 
#
f
o
o
t
e
r
>


 
 
 
 
 
 
 
 
<
s
p
a
n
 
c
l
a
s
s
=
"
d
i
a
l
o
g
-
f
o
o
t
e
r
"
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
s
i
z
e
=
"
s
m
a
l
l
"
 
@
c
l
i
c
k
=
"
s
h
o
w
T
a
s
k
D
i
a
l
o
g
 
=
 
f
a
l
s
e
"
>
取
消
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
 
 
<
e
l
-
b
u
t
t
o
n
 
t
y
p
e
=
"
p
r
i
m
a
r
y
"
 
s
i
z
e
=
"
s
m
a
l
l
"
 
@
c
l
i
c
k
=
"
s
a
v
e
T
a
s
k
"
>
保
存
<
/
e
l
-
b
u
t
t
o
n
>


 
 
 
 
 
 
 
 
<
/
s
p
a
n
>


 
 
 
 
 
 
<
/
t
e
m
p
l
a
t
e
>


 
 
 
 
<
/
e
l
-
d
i
a
l
o
g
>


 
 
<
/
d
i
v
>


<
/
t
e
m
p
l
a
t
e
>




<
s
c
r
i
p
t
 
s
e
t
u
p
>


i
m
p
o
r
t
 
{
 
r
e
f
,
 
r
e
a
c
t
i
v
e
,
 
o
n
M
o
u
n
t
e
d
,
 
n
e
x
t
T
i
c
k
 
}
 
f
r
o
m
 
'
v
u
e
'


i
m
p
o
r
t
 
{
 
E
l
M
e
s
s
a
g
e
,
 
E
l
M
e
s
s
a
g
e
B
o
x
 
}
 
f
r
o
m
 
'
e
l
e
m
e
n
t
-
p
l
u
s
'


i
m
p
o
r
t
 
{
 
P
l
u
s
,
 
E
d
i
t
,
 
D
e
l
e
t
e
,
 
R
e
f
r
e
s
h
,
 
C
a
l
e
n
d
a
r
,
 
A
r
r
o
w
L
e
f
t
 
}
 
f
r
o
m
 
'
@
e
l
e
m
e
n
t
-
p
l
u
s
/
i
c
o
n
s
-
v
u
e
'


i
m
p
o
r
t
 
a
x
i
o
s
 
f
r
o
m
 
'
a
x
i
o
s
'


i
m
p
o
r
t
 
G
a
n
t
t
 
f
r
o
m
 
'
f
r
a
p
p
e
-
g
a
n
t
t
'


i
m
p
o
r
t
 
'
.
.
/
a
s
s
e
t
s
/
f
r
a
p
p
e
-
g
a
n
t
t
.
c
s
s
'




/
/
 
状
态
管
理


c
o
n
s
t
 
p
r
o
j
e
c
t
s
 
=
 
r
e
f
(
[
]
)


c
o
n
s
t
 
s
e
l
e
c
t
e
d
P
r
o
j
e
c
t
 
=
 
r
e
f
(
n
u
l
l
)


c
o
n
s
t
 
s
h
o
w
C
r
e
a
t
e
D
i
a
l
o
g
 
=
 
r
e
f
(
f
a
l
s
e
)


c
o
n
s
t
 
e
d
i
t
i
n
g
P
r
o
j
e
c
t
 
=
 
r
e
f
(
n
u
l
l
)


c
o
n
s
t
 
a
c
t
i
v
e
T
a
b
 
=
 
r
e
f
(
'
g
a
n
t
t
'
)




/
/
 
任
务
管
理
状
态


c
o
n
s
t
 
s
h
o
w
T
a
s
k
D
i
a
l
o
g
 
=
 
r
e
f
(
f
a
l
s
e
)


c
o
n
s
t
 
e
d
i
t
i
n
g
T
a
s
k
 
=
 
r
e
f
(
n
u
l
l
)


c
o
n
s
t
 
c
u
r
r
e
n
t
P
a
r
e
n
t
T
a
s
k
 
=
 
r
e
f
(
n
u
l
l
)


c
o
n
s
t
 
t
a
s
k
F
o
r
m
R
e
f
 
=
 
r
e
f
(
n
u
l
l
)




/
/
 
表
单
相
关


c
o
n
s
t
 
p
r
o
j
e
c
t
F
o
r
m
 
=
 
r
e
a
c
t
i
v
e
(
{


 
 
n
a
m
e
:
 
'
'
,


 
 
d
e
s
c
r
i
p
t
i
o
n
:
 
'
'
,


 
 
s
t
a
r
t
_
d
a
t
e
:
 
'
'
,


 
 
e
n
d
_
d
a
t
e
:
 
'
'
,


 
 
o
w
n
e
r
:
 
1


}
)




c
o
n
s
t
 
p
r
o
j
e
c
t
R
u
l
e
s
 
=
 
{


 
 
n
a
m
e
:
 
[
{
 
r
e
q
u
i
r
e
d
:
 
t
r
u
e
,
 
m
e
s
s
a
g
e
:
 
'
请
输
入
项
目
名
称
'
,
 
t
r
i
g
g
e
r
:
 
'
b
l
u
r
'
 
}
]
,


 
 
s
t
a
r
t
_
d
a
t
e
:
 
[
{
 
r
e
q
u
i
r
e
d
:
 
t
r
u
e
,
 
m
e
s
s
a
g
e
:
 
'
请
选
择
开
始
日
期
'
,
 
t
r
i
g
g
e
r
:
 
'
c
h
a
n
g
e
'
 
}
]
,


 
 
e
n
d
_
d
a
t
e
:
 
[
{
 
r
e
q
u
i
r
e
d
:
 
t
r
u
e
,
 
m
e
s
s
a
g
e
:
 
'
请
选
择
结
束
日
期
'
,
 
t
r
i
g
g
e
r
:
 
'
c
h
a
n
g
e
'
 
}
]
,


 
 
o
w
n
e
r
:
 
[
{
 
r
e
q
u
i
r
e
d
:
 
t
r
u
e
,
 
m
e
s
s
a
g
e
:
 
'
请
选
择
项
目
负
责
人
'
,
 
t
r
i
g
g
e
r
:
 
'
c
h
a
n
g
e
'
 
}
]


}




/
/
 
任
务
表
单


c
o
n
s
t
 
t
a
s
k
F
o
r
m
 
=
 
r
e
a
c
t
i
v
e
(
{


 
 
i
d
:
 
n
u
l
l
,


 
 
n
a
m
e
:
 
'
'
,


 
 
d
e
s
c
r
i
p
t
i
o
n
:
 
'
'
,


 
 
s
t
a
r
t
_
d
a
t
e
:
 
'
'
,


 
 
e
n
d
_
d
a
t
e
:
 
'
'
,


 
 
d
u
r
a
t
i
o
n
:
 
1
,


 
 
p
r
o
g
r
e
s
s
:
 
0
,


 
 
p
r
i
o
r
i
t
y
:
 
2
,


 
 
p
a
r
e
n
t
:
 
n
u
l
l


}
)




/
/
 
任
务
表
单
验
证
规
则


c
o
n
s
t
 
t
a
s
k
R
u
l
e
s
 
=
 
{


 
 
n
a
m
e
:
 
[


 
 
 
 
{
 
r
e
q
u
i
r
e
d
:
 
t
r
u
e
,
 
m
e
s
s
a
g
e
:
 
'
请
输
入
任
务
名
称
'
,
 
t
r
i
g
g
e
r
:
 
'
b
l
u
r
'
 
}


 
 
]
,


 
 
s
t
a
r
t
_
d
a
t
e
:
 
[


 
 
 
 
{
 
r
e
q
u
i
r
e
d
:
 
t
r
u
e
,
 
m
e
s
s
a
g
e
:
 
'
请
选
择
开
始
日
期
'
,
 
t
r
i
g
g
e
r
:
 
'
c
h
a
n
g
e
'
 
}


 
 
]
,


 
 
e
n
d
_
d
a
t
e
:
 
[


 
 
 
 
{
 
r
e
q
u
i
r
e
d
:
 
t
r
u
e
,
 
m
e
s
s
a
g
e
:
 
'
请
选
择
结
束
日
期
'
,
 
t
r
i
g
g
e
r
:
 
'
c
h
a
n
g
e
'
 
}


 
 
]


}




/
/
 
甘
特
图
核
心
配
置


c
o
n
s
t
 
g
a
n
t
t
R
e
f
 
=
 
r
e
f
(
n
u
l
l
)


l
e
t
 
g
a
n
t
t
I
n
s
t
a
n
c
e
 
=
 
n
u
l
l


c
o
n
s
t
 
g
a
n
t
t
D
a
t
a
 
=
 
r
e
f
(
[
]
)


c
o
n
s
t
 
t
a
s
k
T
r
e
e
D
a
t
a
 
=
 
r
e
f
(
[
]
)


c
o
n
s
t
 
t
r
e
e
P
r
o
p
s
 
=
 
r
e
f
(
{


 
 
l
a
b
e
l
:
 
'
n
a
m
e
'
,


 
 
c
h
i
l
d
r
e
n
:
 
'
c
h
i
l
d
r
e
n
'
,


 
 
i
s
L
e
a
f
:
 
(
d
a
t
a
)
 
=
>
 
!
d
a
t
a
.
c
h
i
l
d
r
e
n
 
|
|
 
d
a
t
a
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
=
=
=
 
0


}
)




/
/
 
新
增
：
树
形
组
件
展
开
状
态
管
理
（
遵
循
内
存
中
的
最
佳
实
践
）


c
o
n
s
t
 
e
x
p
a
n
d
e
d
K
e
y
s
 
=
 
r
e
f
(
[
]
)




/
/
 
A
P
I
基
础
U
R
L


c
o
n
s
t
 
A
P
I
_
B
A
S
E
 
=
 
'
/
a
p
i
'




/
/
 
生
命
周
期
钩
子


o
n
M
o
u
n
t
e
d
(
(
)
 
=
>
 
{


 
 
l
o
a
d
P
r
o
j
e
c
t
s
(
)


}
)




/
/
 
方
法
定
义


c
o
n
s
t
 
g
o
B
a
c
k
 
=
 
(
)
 
=
>
 
{


 
 
w
i
n
d
o
w
.
h
i
s
t
o
r
y
.
b
a
c
k
(
)


}




c
o
n
s
t
 
h
a
n
d
l
e
B
a
c
k
 
=
 
(
)
 
=
>
 
{


 
 
s
e
l
e
c
t
e
d
P
r
o
j
e
c
t
.
v
a
l
u
e
 
=
 
n
u
l
l


 
 
a
c
t
i
v
e
T
a
b
.
v
a
l
u
e
 
=
 
'
g
a
n
t
t
'


 
 
i
f
 
(
g
a
n
t
t
I
n
s
t
a
n
c
e
)
 
{


 
 
 
 
t
r
y
 
{


 
 
 
 
 
 
g
a
n
t
t
I
n
s
t
a
n
c
e
.
d
e
s
t
r
o
y
(
)


 
 
 
 
}
 
c
a
t
c
h
 
(
e
)
 
{


 
 
 
 
 
 
i
f
 
(
g
a
n
t
t
R
e
f
.
v
a
l
u
e
)
 
g
a
n
t
t
R
e
f
.
v
a
l
u
e
.
i
n
n
e
r
H
T
M
L
 
=
 
'
'


 
 
 
 
}


 
 
 
 
g
a
n
t
t
I
n
s
t
a
n
c
e
 
=
 
n
u
l
l


 
 
}


}




c
o
n
s
t
 
l
o
a
d
P
r
o
j
e
c
t
s
 
=
 
a
s
y
n
c
 
(
)
 
=
>
 
{


 
 
t
r
y
 
{


 
 
 
 
c
o
n
s
t
 
r
e
s
p
o
n
s
e
 
=
 
a
w
a
i
t
 
a
x
i
o
s
.
g
e
t
(
`
$
{
A
P
I
_
B
A
S
E
}
/
p
r
o
j
e
c
t
s
/
p
r
o
j
e
c
t
s
/
`
)


 
 
 
 
p
r
o
j
e
c
t
s
.
v
a
l
u
e
 
=
 
A
r
r
a
y
.
i
s
A
r
r
a
y
(
r
e
s
p
o
n
s
e
.
d
a
t
a
)
 
?
 
r
e
s
p
o
n
s
e
.
d
a
t
a
 
:
 
[
]


 
 
}
 
c
a
t
c
h
 
(
e
r
r
o
r
)
 
{


 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
'
加
载
项
目
列
表
失
败
'
)


 
 
 
 
c
o
n
s
o
l
e
.
e
r
r
o
r
(
e
r
r
o
r
)


 
 
 
 
p
r
o
j
e
c
t
s
.
v
a
l
u
e
 
=
 
[
]


 
 
}


}




c
o
n
s
t
 
s
e
l
e
c
t
P
r
o
j
e
c
t
 
=
 
a
s
y
n
c
 
(
p
r
o
j
e
c
t
)
 
=
>
 
{


 
 
i
f
 
(
s
e
l
e
c
t
e
d
P
r
o
j
e
c
t
.
v
a
l
u
e
?
.
i
d
 
=
=
=
 
p
r
o
j
e
c
t
.
i
d
)
 
r
e
t
u
r
n




 
 
s
e
l
e
c
t
e
d
P
r
o
j
e
c
t
.
v
a
l
u
e
 
=
 
p
r
o
j
e
c
t


 
 
a
c
t
i
v
e
T
a
b
.
v
a
l
u
e
 
=
 
'
g
a
n
t
t
'


 
 
a
w
a
i
t
 
n
e
x
t
T
i
c
k
(
)




 
 
i
f
 
(
g
a
n
t
t
I
n
s
t
a
n
c
e
)
 
{


 
 
 
 
t
r
y
 
{


 
 
 
 
 
 
g
a
n
t
t
I
n
s
t
a
n
c
e
.
d
e
s
t
r
o
y
(
)


 
 
 
 
}
 
c
a
t
c
h
 
(
e
)
 
{


 
 
 
 
 
 
i
f
 
(
g
a
n
t
t
R
e
f
.
v
a
l
u
e
)
 
g
a
n
t
t
R
e
f
.
v
a
l
u
e
.
i
n
n
e
r
H
T
M
L
 
=
 
'
'


 
 
 
 
}


 
 
}




 
 
i
f
 
(
!
g
a
n
t
t
R
e
f
.
v
a
l
u
e
)
 
{


 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
'
甘
特
图
容
器
未
找
到
'
)


 
 
 
 
r
e
t
u
r
n


 
 
}




 
 
t
r
y
 
{


 
 
 
 
c
o
n
s
t
 
r
e
s
p
o
n
s
e
 
=
 
a
w
a
i
t
 
a
x
i
o
s
.
g
e
t
(
`
$
{
A
P
I
_
B
A
S
E
}
/
p
r
o
j
e
c
t
s
/
p
r
o
j
e
c
t
s
/
$
{
p
r
o
j
e
c
t
.
i
d
}
/
g
a
n
t
t
_
d
a
t
a
/
`
)


 
 
 
 
c
o
n
s
t
 
b
a
c
k
e
n
d
G
a
n
t
t
D
a
t
a
 
=
 
r
e
s
p
o
n
s
e
.
d
a
t
a


 
 
 
 
c
o
n
s
t
 
f
o
r
m
a
t
t
e
d
G
a
n
t
t
D
a
t
a
 
=
 
b
a
c
k
e
n
d
G
a
n
t
t
D
a
t
a
.
m
a
p
(
t
a
s
k
 
=
>
 
(
{


 
 
 
 
 
 
i
d
:
 
t
a
s
k
.
i
d
.
t
o
S
t
r
i
n
g
(
)
,


 
 
 
 
 
 
n
a
m
e
:
 
t
a
s
k
.
n
a
m
e
,


 
 
 
 
 
 
s
t
a
r
t
:
 
t
a
s
k
.
s
t
a
r
t
_
d
a
t
e
,


 
 
 
 
 
 
e
n
d
:
 
t
a
s
k
.
e
n
d
_
d
a
t
e
,


 
 
 
 
 
 
p
r
o
g
r
e
s
s
:
 
t
a
s
k
.
p
r
o
g
r
e
s
s
 
|
|
 
0
,


 
 
 
 
 
 
c
u
s
t
o
m
_
c
l
a
s
s
:
 
t
a
s
k
.
s
t
a
t
u
s
 
=
=
=
 
'
c
o
m
p
l
e
t
e
d
'
 
?
 
'
b
g
-
g
r
e
e
n
-
5
0
0
'
 
:


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
t
a
s
k
.
p
r
o
g
r
e
s
s
 
>
 
0
 
?
 
'
b
g
-
y
e
l
l
o
w
-
5
0
0
'
 
:
 
'
b
g
-
b
l
u
e
-
5
0
0
'


 
 
 
 
}
)
)




 
 
 
 
g
a
n
t
t
D
a
t
a
.
v
a
l
u
e
 
=
 
f
o
r
m
a
t
t
e
d
G
a
n
t
t
D
a
t
a


 
 
 
 
g
a
n
t
t
I
n
s
t
a
n
c
e
 
=
 
n
e
w
 
G
a
n
t
t
(
g
a
n
t
t
R
e
f
.
v
a
l
u
e
,
 
g
a
n
t
t
D
a
t
a
.
v
a
l
u
e
,
 
{


 
 
 
 
 
 
h
e
a
d
e
r
_
h
e
i
g
h
t
:
 
4
0
,
 
/
/
 
移
动
端
缩
小
头
部
高
度


 
 
 
 
 
 
c
o
l
u
m
n
_
w
i
d
t
h
:
 
5
0
,


 
 
 
 
 
 
s
t
e
p
:
 
2
4
,


 
 
 
 
 
 
v
i
e
w
_
m
o
d
e
s
:
 
[
'
D
a
y
'
,
 
'
W
e
e
k
'
,
 
'
M
o
n
t
h
'
]
,


 
 
 
 
 
 
b
a
r
_
h
e
i
g
h
t
:
 
1
8
,


 
 
 
 
 
 
b
a
r
_
c
o
r
n
e
r
_
r
a
d
i
u
s
:
 
4
,


 
 
 
 
 
 
a
r
r
o
w
_
c
u
r
v
e
:
 
5
,


 
 
 
 
 
 
p
a
d
d
i
n
g
:
 
1
0
,


 
 
 
 
 
 
d
a
t
e
_
f
o
r
m
a
t
:
 
'
Y
Y
Y
Y
-
M
M
-
D
D
'
,


 
 
 
 
 
 
p
o
p
u
p
_
t
r
i
g
g
e
r
:
 
'
c
l
i
c
k
'
,


 
 
 
 
 
 
c
u
s
t
o
m
_
p
o
p
u
p
_
h
t
m
l
:
 
(
t
a
s
k
)
 
=
>
 
{


 
 
 
 
 
 
 
 
r
e
t
u
r
n
 
`


 
 
 
 
 
 
 
 
 
 
<
d
i
v
 
c
l
a
s
s
=
"
p
-
2
 
b
g
-
w
h
i
t
e
 
r
o
u
n
d
e
d
-
l
g
 
s
h
a
d
o
w
-
l
g
 
b
o
r
d
e
r
 
b
o
r
d
e
r
-
g
r
a
y
-
2
0
0
 
t
e
x
t
-
s
m
"
>


 
 
 
 
 
 
 
 
 
 
 
 
<
h
5
 
c
l
a
s
s
=
"
f
o
n
t
-
b
o
l
d
 
t
e
x
t
-
g
r
a
y
-
8
0
0
"
>
$
{
t
a
s
k
.
n
a
m
e
}
<
/
h
5
>


 
 
 
 
 
 
 
 
 
 
 
 
<
p
 
c
l
a
s
s
=
"
t
e
x
t
-
x
s
 
t
e
x
t
-
g
r
a
y
-
6
0
0
"
>
进
度
：
$
{
t
a
s
k
.
p
r
o
g
r
e
s
s
}
%
<
/
p
>


 
 
 
 
 
 
 
 
 
 
 
 
<
p
 
c
l
a
s
s
=
"
t
e
x
t
-
x
s
 
t
e
x
t
-
g
r
a
y
-
6
0
0
"
>
时
间
：
$
{
t
a
s
k
.
s
t
a
r
t
}
 
-
 
$
{
t
a
s
k
.
e
n
d
}
<
/
p
>


 
 
 
 
 
 
 
 
 
 
<
/
d
i
v
>


 
 
 
 
 
 
 
 
`


 
 
 
 
 
 
}


 
 
 
 
}
)


 
 
 
 
E
l
M
e
s
s
a
g
e
.
s
u
c
c
e
s
s
(
`
已
加
载
$
{
p
r
o
j
e
c
t
.
n
a
m
e
}
的
甘
特
图
`
)


 
 
 
 
a
w
a
i
t
 
l
o
a
d
T
a
s
k
T
r
e
e
D
a
t
a
(
p
r
o
j
e
c
t
.
i
d
)


 
 
}
 
c
a
t
c
h
 
(
e
r
r
)
 
{


 
 
 
 
c
o
n
s
o
l
e
.
e
r
r
o
r
(
'
甘
特
图
初
始
化
失
败
：
'
,
 
e
r
r
)


 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
'
甘
特
图
初
始
化
失
败
'
)


 
 
 
 
g
a
n
t
t
D
a
t
a
.
v
a
l
u
e
 
=
 
[
]


 
 
 
 
t
r
y
 
{


 
 
 
 
 
 
g
a
n
t
t
I
n
s
t
a
n
c
e
 
=
 
n
e
w
 
G
a
n
t
t
(
g
a
n
t
t
R
e
f
.
v
a
l
u
e
,
 
[
]
,
 
{
}
)


 
 
 
 
}
 
c
a
t
c
h
 
(
e
)
 
{
}


 
 
}


}




c
o
n
s
t
 
l
o
a
d
T
a
s
k
T
r
e
e
D
a
t
a
 
=
 
a
s
y
n
c
 
(
p
r
o
j
e
c
t
I
d
)
 
=
>
 
{


 
 
t
r
y
 
{


 
 
 
 
c
o
n
s
t
 
t
r
e
e
D
a
t
a
 
=
 
r
e
s
p
o
n
s
e
.
d
a
t
a
.
t
a
s
k
s
 
|
|
 
[
]




 
 
 
 
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
 
=
 
t
r
e
e
D
a
t
a


 
 
 
 
a
w
a
i
t
 
n
e
x
t
T
i
c
k
(
)


 
 
 
 
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
 
=
 
[
.
.
.
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
]




 
 
 
 


 
 
 
 
/
/
 
调
试
信
息


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
从
后
端
获
取
的
任
务
树
数
据
:
'
,
 
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
)


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
根
节
点
数
量
:
'
,
 
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
.
l
e
n
g
t
h
)


 
 
 
 


 
 
 
 
/
/
 
计
算
并
显
示
树
的
深
度


 
 
 
 
c
o
n
s
t
 
t
r
e
e
D
e
p
t
h
 
=
 
c
a
l
c
u
l
a
t
e
T
r
e
e
D
e
p
t
h
(
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
)


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
任
务
树
最
大
深
度
:
'
,
 
t
r
e
e
D
e
p
t
h
)


 
 
 
 


 
 
 
 
/
/
 
初
始
化
展
开
状
态
 
-
 
展
开
前
两
层
节
点


 
 
 
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
 
=
 
[
]


 
 
 
 
c
o
n
s
t
 
c
o
l
l
e
c
t
E
x
p
a
n
d
e
d
K
e
y
s
 
=
 
(
n
o
d
e
s
,
 
m
a
x
D
e
p
t
h
 
=
 
2
,
 
c
u
r
r
e
n
t
D
e
p
t
h
 
=
 
0
)
 
=
>
 
{


 
 
 
 
 
 
i
f
 
(
!
n
o
d
e
s
 
|
|
 
c
u
r
r
e
n
t
D
e
p
t
h
 
>
=
 
m
a
x
D
e
p
t
h
)
 
r
e
t
u
r
n


 
 
 
 
 
 


 
 
 
 
 
 
f
o
r
 
(
c
o
n
s
t
 
n
o
d
e
 
o
f
 
n
o
d
e
s
)
 
{


 
 
 
 
 
 
 
 
i
f
 
(
c
u
r
r
e
n
t
D
e
p
t
h
 
<
 
m
a
x
D
e
p
t
h
 
-
 
1
)
 
{


 
 
 
 
 
 
 
 
 
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
.
p
u
s
h
(
n
o
d
e
.
i
d
)


 
 
 
 
 
 
 
 
}


 
 
 
 
 
 
 
 
i
f
 
(
n
o
d
e
.
c
h
i
l
d
r
e
n
 
&
&
 
n
o
d
e
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
>
 
0
)
 
{


 
 
 
 
 
 
 
 
 
 
c
o
l
l
e
c
t
E
x
p
a
n
d
e
d
K
e
y
s
(
n
o
d
e
.
c
h
i
l
d
r
e
n
,
 
m
a
x
D
e
p
t
h
,
 
c
u
r
r
e
n
t
D
e
p
t
h
 
+
 
1
)


 
 
 
 
 
 
 
 
}


 
 
 
 
 
 
}


 
 
 
 
}


 
 
 
 


 
 
 
 
c
o
l
l
e
c
t
E
x
p
a
n
d
e
d
K
e
y
s
(
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
)


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
初
始
展
开
的
节
点
k
e
y
s
:
'
,
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
)


 
 
 
 


 
 
 
 
/
/
 
验
证
数
据
结
构


 
 
 
 
c
o
n
s
t
 
v
a
l
i
d
a
t
e
T
r
e
e
S
t
r
u
c
t
u
r
e
 
=
 
(
n
o
d
e
s
,
 
l
e
v
e
l
 
=
 
0
,
 
p
a
r
e
n
t
I
d
 
=
 
n
u
l
l
)
 
=
>
 
{


 
 
 
 
 
 
i
f
 
(
!
n
o
d
e
s
)
 
r
e
t
u
r
n


 
 
 
 
 
 


 
 
 
 
 
 
n
o
d
e
s
.
f
o
r
E
a
c
h
(
(
n
o
d
e
,
 
i
n
d
e
x
)
 
=
>
 
{


 
 
 
 
 
 
 
 
c
o
n
s
t
 
i
n
d
e
n
t
 
=
 
'
 
 
'
.
r
e
p
e
a
t
(
l
e
v
e
l
)


 
 
 
 
 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
`
$
{
i
n
d
e
n
t
}
节
点
 
[
$
{
l
e
v
e
l
}
]
 
$
{
i
n
d
e
x
}
:
`
,
 
{


 
 
 
 
 
 
 
 
 
 
i
d
:
 
n
o
d
e
.
i
d
,


 
 
 
 
 
 
 
 
 
 
l
a
b
e
l
:
 
n
o
d
e
.
l
a
b
e
l
,


 
 
 
 
 
 
 
 
 
 
n
a
m
e
:
 
n
o
d
e
.
n
a
m
e
,


 
 
 
 
 
 
 
 
 
 
p
a
r
e
n
t
_
i
d
:
 
n
o
d
e
.
p
a
r
e
n
t
_
i
d
,


 
 
 
 
 
 
 
 
 
 
p
a
r
e
n
t
I
d
C
h
e
c
k
:
 
n
o
d
e
.
p
a
r
e
n
t
_
i
d
 
=
=
=
 
p
a
r
e
n
t
I
d
,


 
 
 
 
 
 
 
 
 
 
c
h
i
l
d
r
e
n
C
o
u
n
t
:
 
n
o
d
e
.
c
h
i
l
d
r
e
n
 
?
 
n
o
d
e
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
:
 
0
,


 
 
 
 
 
 
 
 
 
 
h
a
s
C
h
i
l
d
r
e
n
:
 
!
!
(
n
o
d
e
.
c
h
i
l
d
r
e
n
 
&
&
 
n
o
d
e
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
>
 
0
)


 
 
 
 
 
 
 
 
}
)


 
 
 
 
 
 
 
 


 
 
 
 
 
 
 
 
/
/
 
递
归
验
证
子
节
点


 
 
 
 
 
 
 
 
i
f
 
(
n
o
d
e
.
c
h
i
l
d
r
e
n
 
&
&
 
n
o
d
e
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
>
 
0
)
 
{


 
 
 
 
 
 
 
 
 
 
v
a
l
i
d
a
t
e
T
r
e
e
S
t
r
u
c
t
u
r
e
(
n
o
d
e
.
c
h
i
l
d
r
e
n
,
 
l
e
v
e
l
 
+
 
1
,
 
n
o
d
e
.
i
d
)


 
 
 
 
 
 
 
 
}


 
 
 
 
 
 
}
)


 
 
 
 
}


 
 
 
 


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
=
=
=
 
任
务
树
结
构
验
证
 
=
=
=
'
)


 
 
 
 
v
a
l
i
d
a
t
e
T
r
e
e
S
t
r
u
c
t
u
r
e
(
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
)


 
 
 
 




 
 
 
 
c
o
n
s
t
 
r
e
s
p
o
n
s
e
 
=
 
a
w
a
i
t
 
a
x
i
o
s
.
g
e
t
(
`
$
{
A
P
I
_
B
A
S
E
}
/
p
r
o
j
e
c
t
s
/
p
r
o
j
e
c
t
s
/
$
{
p
r
o
j
e
c
t
I
d
}
/
`
)


 
 
 
 
/
/
 
后
端
已
经
返
回
了
完
整
的
树
形
结
构
，
直
接
使
用


 
 
 
 
l
e
t
 
t
r
e
e
D
a
t
a
 
=
 
r
e
s
p
o
n
s
e
.
d
a
t
a
.
t
a
s
k
s
 
|
|
 
[
]


 
 
 
 


 
 
 
 
/
/
 
数
据
转
换
：
将
后
端
的
 
n
a
m
e
 
字
段
转
换
为
前
端
需
要
的
 
l
a
b
e
l
 
字
段


 
 
 
 
c
o
n
s
t
 
c
o
n
v
e
r
t
T
a
s
k
D
a
t
a
 
=
 
(
t
a
s
k
s
)
 
=
>
 
{


 
 
 
 
 
 
r
e
t
u
r
n
 
t
a
s
k
s
.
m
a
p
(
t
a
s
k
 
=
>
 
{


 
 
 
 
 
 
 
 
/
/
 
创
建
新
对
象
，
保
留
原
有
属
性


 
 
 
 
 
 
 
 
c
o
n
s
t
 
c
o
n
v
e
r
t
e
d
T
a
s
k
 
=
 
{


 
 
 
 
 
 
 
 
 
 
.
.
.
t
a
s
k
,


 
 
 
 
 
 
 
 
 
 
l
a
b
e
l
:
 
t
a
s
k
.
n
a
m
e
 
|
|
 
t
a
s
k
.
l
a
b
e
l
 
|
|
 
'
未
命
名
任
务
'
,
 
/
/
 
使
用
n
a
m
e
作
为
l
a
b
e
l


 
 
 
 
 
 
 
 
 
 
c
h
i
l
d
r
e
n
:
 
t
a
s
k
.
c
h
i
l
d
r
e
n
 
?
 
c
o
n
v
e
r
t
T
a
s
k
D
a
t
a
(
t
a
s
k
.
c
h
i
l
d
r
e
n
)
 
:
 
[
]


 
 
 
 
 
 
 
 
}


 
 
 
 
 
 
 
 
r
e
t
u
r
n
 
c
o
n
v
e
r
t
e
d
T
a
s
k


 
 
 
 
 
 
}
)


 
 
 
 
}


 
 
 
 


 
 
 
 
t
r
e
e
D
a
t
a
 
=
 
c
o
n
v
e
r
t
T
a
s
k
D
a
t
a
(
t
r
e
e
D
a
t
a
)


 
 
 
 


 
 
 
 
/
/
 
直
接
赋
值
，
因
为
后
端
已
经
构
建
好
了
树
形
结
构


 
 
 
 
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
 
=
 
t
r
e
e
D
a
t
a


 
 
 
 
a
w
a
i
t
 
n
e
x
t
T
i
c
k
(
)


 
 
 
 
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
 
=
 
[
.
.
.
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
]


 
 
 
 


 
 
 
 
/
/
 
调
试
信
息


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
从
后
端
获
取
的
任
务
树
数
据
:
'
,
 
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
)


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
根
节
点
数
量
:
'
,
 
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
.
l
e
n
g
t
h
)


 
 
 
 


 
 
 
 
/
/
 
计
算
并
显
示
树
的
深
度


 
 
 
 
c
o
n
s
t
 
t
r
e
e
D
e
p
t
h
 
=
 
c
a
l
c
u
l
a
t
e
T
r
e
e
D
e
p
t
h
(
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
)


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
任
务
树
最
大
深
度
:
'
,
 
t
r
e
e
D
e
p
t
h
)


 
 
 
 


 
 
 
 
/
/
 
初
始
化
展
开
状
态
 
-
 
展
开
前
两
层
节
点


 
 
 
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
 
=
 
[
]


 
 
 
 
c
o
n
s
t
 
c
o
l
l
e
c
t
E
x
p
a
n
d
e
d
K
e
y
s
 
=
 
(
n
o
d
e
s
,
 
m
a
x
D
e
p
t
h
 
=
 
2
,
 
c
u
r
r
e
n
t
D
e
p
t
h
 
=
 
0
)
 
=
>
 
{


 
 
 
 
 
 
i
f
 
(
!
n
o
d
e
s
 
|
|
 
c
u
r
r
e
n
t
D
e
p
t
h
 
>
=
 
m
a
x
D
e
p
t
h
)
 
r
e
t
u
r
n


 
 
 
 
 
 


 
 
 
 
 
 
f
o
r
 
(
c
o
n
s
t
 
n
o
d
e
 
o
f
 
n
o
d
e
s
)
 
{


 
 
 
 
 
 
 
 
i
f
 
(
c
u
r
r
e
n
t
D
e
p
t
h
 
<
 
m
a
x
D
e
p
t
h
 
-
 
1
)
 
{


 
 
 
 
 
 
 
 
 
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
.
p
u
s
h
(
n
o
d
e
.
i
d
)


 
 
 
 
 
 
 
 
}


 
 
 
 
 
 
 
 
i
f
 
(
n
o
d
e
.
c
h
i
l
d
r
e
n
 
&
&
 
n
o
d
e
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
>
 
0
)
 
{


 
 
 
 
 
 
 
 
 
 
c
o
l
l
e
c
t
E
x
p
a
n
d
e
d
K
e
y
s
(
n
o
d
e
.
c
h
i
l
d
r
e
n
,
 
m
a
x
D
e
p
t
h
,
 
c
u
r
r
e
n
t
D
e
p
t
h
 
+
 
1
)


 
 
 
 
 
 
 
 
}


 
 
 
 
 
 
}


 
 
 
 
}


 
 
 
 


 
 
 
 
c
o
l
l
e
c
t
E
x
p
a
n
d
e
d
K
e
y
s
(
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
)


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
初
始
展
开
的
节
点
k
e
y
s
:
'
,
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
)


 
 
 
 


 
 
 
 
/
/
 
验
证
数
据
结
构


 
 
 
 
c
o
n
s
t
 
v
a
l
i
d
a
t
e
T
r
e
e
S
t
r
u
c
t
u
r
e
 
=
 
(
n
o
d
e
s
,
 
l
e
v
e
l
 
=
 
0
,
 
p
a
r
e
n
t
I
d
 
=
 
n
u
l
l
)
 
=
>
 
{


 
 
 
 
 
 
i
f
 
(
!
n
o
d
e
s
)
 
r
e
t
u
r
n


 
 
 
 
 
 


 
 
 
 
 
 
n
o
d
e
s
.
f
o
r
E
a
c
h
(
(
n
o
d
e
,
 
i
n
d
e
x
)
 
=
>
 
{


 
 
 
 
 
 
 
 
c
o
n
s
t
 
i
n
d
e
n
t
 
=
 
'
 
 
'
.
r
e
p
e
a
t
(
l
e
v
e
l
)


 
 
 
 
 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
`
$
{
i
n
d
e
n
t
}
节
点
 
[
$
{
l
e
v
e
l
}
]
 
$
{
i
n
d
e
x
}
:
`
,
 
{


 
 
 
 
 
 
 
 
 
 
i
d
:
 
n
o
d
e
.
i
d
,


 
 
 
 
 
 
 
 
 
 
l
a
b
e
l
:
 
n
o
d
e
.
l
a
b
e
l
,


 
 
 
 
 
 
 
 
 
 
n
a
m
e
:
 
n
o
d
e
.
n
a
m
e
,


 
 
 
 
 
 
 
 
 
 
p
a
r
e
n
t
_
i
d
:
 
n
o
d
e
.
p
a
r
e
n
t
_
i
d
,


 
 
 
 
 
 
 
 
 
 
p
a
r
e
n
t
I
d
C
h
e
c
k
:
 
n
o
d
e
.
p
a
r
e
n
t
_
i
d
 
=
=
=
 
p
a
r
e
n
t
I
d
,


 
 
 
 
 
 
 
 
 
 
c
h
i
l
d
r
e
n
C
o
u
n
t
:
 
n
o
d
e
.
c
h
i
l
d
r
e
n
 
?
 
n
o
d
e
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
:
 
0
,


 
 
 
 
 
 
 
 
 
 
h
a
s
C
h
i
l
d
r
e
n
:
 
!
!
(
n
o
d
e
.
c
h
i
l
d
r
e
n
 
&
&
 
n
o
d
e
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
>
 
0
)


 
 
 
 
 
 
 
 
}
)


 
 
 
 
 
 
 
 


 
 
 
 
 
 
 
 
/
/
 
递
归
验
证
子
节
点


 
 
 
 
 
 
 
 
i
f
 
(
n
o
d
e
.
c
h
i
l
d
r
e
n
 
&
&
 
n
o
d
e
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
>
 
0
)
 
{


 
 
 
 
 
 
 
 
 
 
v
a
l
i
d
a
t
e
T
r
e
e
S
t
r
u
c
t
u
r
e
(
n
o
d
e
.
c
h
i
l
d
r
e
n
,
 
l
e
v
e
l
 
+
 
1
,
 
n
o
d
e
.
i
d
)


 
 
 
 
 
 
 
 
}


 
 
 
 
 
 
}
)


 
 
 
 
}


 
 
 
 


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
=
=
=
 
任
务
树
结
构
验
证
 
=
=
=
'
)


 
 
 
 
v
a
l
i
d
a
t
e
T
r
e
e
S
t
r
u
c
t
u
r
e
(
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
)


=
=
=
=
=
=
=


 
 
 
 
c
o
n
s
t
 
t
r
e
e
D
a
t
a
 
=
 
r
e
s
p
o
n
s
e
.
d
a
t
a
.
t
a
s
k
s
 
|
|
 
[
]




 
 
 
 
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
 
=
 
t
r
e
e
D
a
t
a


 
 
 
 
a
w
a
i
t
 
n
e
x
t
T
i
c
k
(
)


 
 
 
 
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
 
=
 
[
.
.
.
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
]




 
 
 
 


 
 
 
 
/
/
 
调
试
信
息


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
从
后
端
获
取
的
任
务
树
数
据
:
'
,
 
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
)


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
根
节
点
数
量
:
'
,
 
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
.
l
e
n
g
t
h
)


 
 
 
 


 
 
 
 
/
/
 
计
算
并
显
示
树
的
深
度


 
 
 
 
c
o
n
s
t
 
t
r
e
e
D
e
p
t
h
 
=
 
c
a
l
c
u
l
a
t
e
T
r
e
e
D
e
p
t
h
(
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
)


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
任
务
树
最
大
深
度
:
'
,
 
t
r
e
e
D
e
p
t
h
)


 
 
 
 


 
 
 
 
/
/
 
初
始
化
展
开
状
态
 
-
 
展
开
前
两
层
节
点


 
 
 
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
 
=
 
[
]


 
 
 
 
c
o
n
s
t
 
c
o
l
l
e
c
t
E
x
p
a
n
d
e
d
K
e
y
s
 
=
 
(
n
o
d
e
s
,
 
m
a
x
D
e
p
t
h
 
=
 
2
,
 
c
u
r
r
e
n
t
D
e
p
t
h
 
=
 
0
)
 
=
>
 
{


 
 
 
 
 
 
i
f
 
(
!
n
o
d
e
s
 
|
|
 
c
u
r
r
e
n
t
D
e
p
t
h
 
>
=
 
m
a
x
D
e
p
t
h
)
 
r
e
t
u
r
n


 
 
 
 
 
 


 
 
 
 
 
 
f
o
r
 
(
c
o
n
s
t
 
n
o
d
e
 
o
f
 
n
o
d
e
s
)
 
{


 
 
 
 
 
 
 
 
i
f
 
(
c
u
r
r
e
n
t
D
e
p
t
h
 
<
 
m
a
x
D
e
p
t
h
 
-
 
1
)
 
{


 
 
 
 
 
 
 
 
 
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
.
p
u
s
h
(
n
o
d
e
.
i
d
)


 
 
 
 
 
 
 
 
}


 
 
 
 
 
 
 
 
i
f
 
(
n
o
d
e
.
c
h
i
l
d
r
e
n
 
&
&
 
n
o
d
e
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
>
 
0
)
 
{


 
 
 
 
 
 
 
 
 
 
c
o
l
l
e
c
t
E
x
p
a
n
d
e
d
K
e
y
s
(
n
o
d
e
.
c
h
i
l
d
r
e
n
,
 
m
a
x
D
e
p
t
h
,
 
c
u
r
r
e
n
t
D
e
p
t
h
 
+
 
1
)


 
 
 
 
 
 
 
 
}


 
 
 
 
 
 
}


 
 
 
 
}


 
 
 
 


 
 
 
 
c
o
l
l
e
c
t
E
x
p
a
n
d
e
d
K
e
y
s
(
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
)


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
初
始
展
开
的
节
点
k
e
y
s
:
'
,
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
)


 
 
 
 


 
 
 
 
/
/
 
验
证
数
据
结
构


 
 
 
 
c
o
n
s
t
 
v
a
l
i
d
a
t
e
T
r
e
e
S
t
r
u
c
t
u
r
e
 
=
 
(
n
o
d
e
s
,
 
l
e
v
e
l
 
=
 
0
,
 
p
a
r
e
n
t
I
d
 
=
 
n
u
l
l
)
 
=
>
 
{


 
 
 
 
 
 
i
f
 
(
!
n
o
d
e
s
)
 
r
e
t
u
r
n


 
 
 
 
 
 


 
 
 
 
 
 
n
o
d
e
s
.
f
o
r
E
a
c
h
(
(
n
o
d
e
,
 
i
n
d
e
x
)
 
=
>
 
{


 
 
 
 
 
 
 
 
c
o
n
s
t
 
i
n
d
e
n
t
 
=
 
'
 
 
'
.
r
e
p
e
a
t
(
l
e
v
e
l
)


 
 
 
 
 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
`
$
{
i
n
d
e
n
t
}
节
点
 
[
$
{
l
e
v
e
l
}
]
 
$
{
i
n
d
e
x
}
:
`
,
 
{


 
 
 
 
 
 
 
 
 
 
i
d
:
 
n
o
d
e
.
i
d
,


 
 
 
 
 
 
 
 
 
 
l
a
b
e
l
:
 
n
o
d
e
.
l
a
b
e
l
,


 
 
 
 
 
 
 
 
 
 
n
a
m
e
:
 
n
o
d
e
.
n
a
m
e
,


 
 
 
 
 
 
 
 
 
 
p
a
r
e
n
t
_
i
d
:
 
n
o
d
e
.
p
a
r
e
n
t
_
i
d
,


 
 
 
 
 
 
 
 
 
 
p
a
r
e
n
t
I
d
C
h
e
c
k
:
 
n
o
d
e
.
p
a
r
e
n
t
_
i
d
 
=
=
=
 
p
a
r
e
n
t
I
d
,


 
 
 
 
 
 
 
 
 
 
c
h
i
l
d
r
e
n
C
o
u
n
t
:
 
n
o
d
e
.
c
h
i
l
d
r
e
n
 
?
 
n
o
d
e
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
:
 
0
,


 
 
 
 
 
 
 
 
 
 
h
a
s
C
h
i
l
d
r
e
n
:
 
!
!
(
n
o
d
e
.
c
h
i
l
d
r
e
n
 
&
&
 
n
o
d
e
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
>
 
0
)


 
 
 
 
 
 
 
 
}
)


 
 
 
 
 
 
 
 


 
 
 
 
 
 
 
 
/
/
 
递
归
验
证
子
节
点


 
 
 
 
 
 
 
 
i
f
 
(
n
o
d
e
.
c
h
i
l
d
r
e
n
 
&
&
 
n
o
d
e
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
>
 
0
)
 
{


 
 
 
 
 
 
 
 
 
 
v
a
l
i
d
a
t
e
T
r
e
e
S
t
r
u
c
t
u
r
e
(
n
o
d
e
.
c
h
i
l
d
r
e
n
,
 
l
e
v
e
l
 
+
 
1
,
 
n
o
d
e
.
i
d
)


 
 
 
 
 
 
 
 
}


 
 
 
 
 
 
}
)


 
 
 
 
}


 
 
 
 


 
 
 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
=
=
=
 
任
务
树
结
构
验
证
 
=
=
=
'
)


 
 
 
 
v
a
l
i
d
a
t
e
T
r
e
e
S
t
r
u
c
t
u
r
e
(
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
)


 
 
 
 


=
=
=
=
=
=
=




 
 
}
 
c
a
t
c
h
 
(
e
r
r
o
r
)
 
{


 
 
 
 
c
o
n
s
o
l
e
.
e
r
r
o
r
(
'
加
载
任
务
树
数
据
失
败
：
'
,
 
e
r
r
o
r
)


 
 
 
 
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
 
=
 
[
]


 
 
}


}




c
o
n
s
t
 
c
h
a
n
g
e
V
i
e
w
 
=
 
(
m
o
d
e
)
 
=
>
 
{


 
 
i
f
 
(
!
g
a
n
t
t
I
n
s
t
a
n
c
e
)
 
r
e
t
u
r
n


 
 
t
r
y
 
{


 
 
 
 
i
f
 
(
g
a
n
t
t
I
n
s
t
a
n
c
e
.
c
h
a
n
g
e
_
v
i
e
w
_
m
o
d
e
)
 
{


 
 
 
 
 
 
g
a
n
t
t
I
n
s
t
a
n
c
e
.
c
h
a
n
g
e
_
v
i
e
w
_
m
o
d
e
(
m
o
d
e
)


 
 
 
 
}
 
e
l
s
e
 
i
f
 
(
g
a
n
t
t
I
n
s
t
a
n
c
e
.
s
e
t
V
i
e
w
M
o
d
e
)
 
{


 
 
 
 
 
 
g
a
n
t
t
I
n
s
t
a
n
c
e
.
s
e
t
V
i
e
w
M
o
d
e
(
m
o
d
e
)


 
 
 
 
}
 
e
l
s
e
 
{


 
 
 
 
 
 
c
o
n
s
t
 
n
e
w
I
n
s
t
a
n
c
e
 
=
 
n
e
w
 
G
a
n
t
t
(
g
a
n
t
t
R
e
f
.
v
a
l
u
e
,
 
g
a
n
t
t
D
a
t
a
,
 
{


 
 
 
 
 
 
 
 
h
e
a
d
e
r
_
h
e
i
g
h
t
:
 
4
0
,


 
 
 
 
 
 
 
 
c
o
l
u
m
n
_
w
i
d
t
h
:
 
5
0
,


 
 
 
 
 
 
 
 
s
t
e
p
:
 
2
4
,


 
 
 
 
 
 
 
 
v
i
e
w
_
m
o
d
e
s
:
 
[
'
D
a
y
'
,
 
'
W
e
e
k
'
,
 
'
M
o
n
t
h
'
]
,


 
 
 
 
 
 
 
 
v
i
e
w
_
m
o
d
e
:
 
m
o
d
e
,


 
 
 
 
 
 
 
 
b
a
r
_
h
e
i
g
h
t
:
 
1
8
,


 
 
 
 
 
 
 
 
b
a
r
_
c
o
r
n
e
r
_
r
a
d
i
u
s
:
 
4
,


 
 
 
 
 
 
 
 
a
r
r
o
w
_
c
u
r
v
e
:
 
5
,


 
 
 
 
 
 
 
 
p
a
d
d
i
n
g
:
 
1
0
,


 
 
 
 
 
 
 
 
d
a
t
e
_
f
o
r
m
a
t
:
 
'
Y
Y
Y
Y
-
M
M
-
D
D
'


 
 
 
 
 
 
}
)


 
 
 
 
 
 
g
a
n
t
t
I
n
s
t
a
n
c
e
 
=
 
n
e
w
I
n
s
t
a
n
c
e


 
 
 
 
}


 
 
 
 
E
l
M
e
s
s
a
g
e
.
s
u
c
c
e
s
s
(
`
切
换
为
$
{
m
o
d
e
}
视
图
`
)


 
 
}
 
c
a
t
c
h
 
(
e
r
r
)
 
{


 
 
 
 
c
o
n
s
o
l
e
.
e
r
r
o
r
(
'
切
换
视
图
失
败
：
'
,
 
e
r
r
)


 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
`
切
换
$
{
m
o
d
e
}
视
图
失
败
，
请
重
试
`
)


 
 
}


}




c
o
n
s
t
 
s
a
v
e
P
r
o
j
e
c
t
 
=
 
a
s
y
n
c
 
(
)
 
=
>
 
{


 
 
t
r
y
 
{


 
 
 
 
c
o
n
s
t
 
p
r
o
j
e
c
t
D
a
t
a
 
=
 
{


 
 
 
 
 
 
n
a
m
e
:
 
p
r
o
j
e
c
t
F
o
r
m
.
n
a
m
e
.
t
r
i
m
(
)
,


 
 
 
 
 
 
d
e
s
c
r
i
p
t
i
o
n
:
 
p
r
o
j
e
c
t
F
o
r
m
.
d
e
s
c
r
i
p
t
i
o
n
.
t
r
i
m
(
)
 
|
|
 
'
'
,


 
 
 
 
 
 
s
t
a
r
t
_
d
a
t
e
:
 
p
r
o
j
e
c
t
F
o
r
m
.
s
t
a
r
t
_
d
a
t
e
,


 
 
 
 
 
 
e
n
d
_
d
a
t
e
:
 
p
r
o
j
e
c
t
F
o
r
m
.
e
n
d
_
d
a
t
e
,


 
 
 
 
 
 
o
w
n
e
r
:
 
p
r
o
j
e
c
t
F
o
r
m
.
o
w
n
e
r


 
 
 
 
}
;




 
 
 
 
i
f
 
(
!
p
r
o
j
e
c
t
D
a
t
a
.
n
a
m
e
)
 
{


 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
'
项
目
名
称
不
能
为
空
'
)
;


 
 
 
 
 
 
r
e
t
u
r
n
;


 
 
 
 
}


 
 
 
 
i
f
 
(
!
p
r
o
j
e
c
t
D
a
t
a
.
s
t
a
r
t
_
d
a
t
e
 
|
|
 
!
p
r
o
j
e
c
t
D
a
t
a
.
e
n
d
_
d
a
t
e
)
 
{


 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
'
请
填
写
完
整
的
日
期
信
息
'
)
;


 
 
 
 
 
 
r
e
t
u
r
n
;


 
 
 
 
}


 
 
 
 
i
f
 
(
!
p
r
o
j
e
c
t
D
a
t
a
.
o
w
n
e
r
)
 
{


 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
'
请
选
择
项
目
负
责
人
'
)
;


 
 
 
 
 
 
r
e
t
u
r
n
;


 
 
 
 
}




 
 
 
 
i
f
 
(
e
d
i
t
i
n
g
P
r
o
j
e
c
t
.
v
a
l
u
e
)
 
{


 
 
 
 
 
 
a
w
a
i
t
 
a
x
i
o
s
.
p
u
t
(
`
$
{
A
P
I
_
B
A
S
E
}
/
p
r
o
j
e
c
t
s
/
p
r
o
j
e
c
t
s
/
$
{
e
d
i
t
i
n
g
P
r
o
j
e
c
t
.
v
a
l
u
e
.
i
d
}
/
`
,
 
p
r
o
j
e
c
t
D
a
t
a
)
;


 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
s
u
c
c
e
s
s
(
'
项
目
更
新
成
功
'
)
;


 
 
 
 
}
 
e
l
s
e
 
{


 
 
 
 
 
 
a
w
a
i
t
 
a
x
i
o
s
.
p
o
s
t
(
`
$
{
A
P
I
_
B
A
S
E
}
/
p
r
o
j
e
c
t
s
/
p
r
o
j
e
c
t
s
/
`
,
 
p
r
o
j
e
c
t
D
a
t
a
)
;


 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
s
u
c
c
e
s
s
(
'
项
目
创
建
成
功
'
)
;


 
 
 
 
}




 
 
 
 
s
h
o
w
C
r
e
a
t
e
D
i
a
l
o
g
.
v
a
l
u
e
 
=
 
f
a
l
s
e
;


 
 
 
 
a
w
a
i
t
 
l
o
a
d
P
r
o
j
e
c
t
s
(
)
;


 
 
 
 
r
e
s
e
t
P
r
o
j
e
c
t
F
o
r
m
(
)
;


 
 
}
 
c
a
t
c
h
 
(
e
r
r
o
r
)
 
{


 
 
 
 
c
o
n
s
t
 
e
r
r
o
r
M
e
s
s
a
g
e
 
=
 
e
d
i
t
i
n
g
P
r
o
j
e
c
t
.
v
a
l
u
e
 
?
 
'
项
目
更
新
失
败
'
 
:
 
'
项
目
创
建
失
败
'
;


 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
e
r
r
o
r
M
e
s
s
a
g
e
)
;


 
 
 
 
c
o
n
s
o
l
e
.
e
r
r
o
r
(
'
项
目
保
存
错
误
:
'
,
 
e
r
r
o
r
.
r
e
s
p
o
n
s
e
?
.
d
a
t
a
 
|
|
 
e
r
r
o
r
.
m
e
s
s
a
g
e
)
;


 
 
 
 
i
f
 
(
e
r
r
o
r
.
r
e
s
p
o
n
s
e
?
.
d
a
t
a
)
 
{


 
 
 
 
 
 
c
o
n
s
t
 
e
r
r
o
r
D
e
t
a
i
l
s
 
=
 
e
r
r
o
r
.
r
e
s
p
o
n
s
e
.
d
a
t
a
;


 
 
 
 
 
 
i
f
 
(
t
y
p
e
o
f
 
e
r
r
o
r
D
e
t
a
i
l
s
 
=
=
=
 
'
o
b
j
e
c
t
'
)
 
{


 
 
 
 
 
 
 
 
O
b
j
e
c
t
.
k
e
y
s
(
e
r
r
o
r
D
e
t
a
i
l
s
)
.
f
o
r
E
a
c
h
(
k
e
y
 
=
>
 
{


 
 
 
 
 
 
 
 
 
 
c
o
n
s
t
 
f
i
e
l
d
E
r
r
o
r
s
 
=
 
e
r
r
o
r
D
e
t
a
i
l
s
[
k
e
y
]
;


 
 
 
 
 
 
 
 
 
 
i
f
 
(
A
r
r
a
y
.
i
s
A
r
r
a
y
(
f
i
e
l
d
E
r
r
o
r
s
)
)
 
{


 
 
 
 
 
 
 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
`
$
{
k
e
y
}
:
 
$
{
f
i
e
l
d
E
r
r
o
r
s
.
j
o
i
n
(
'
,
 
'
)
}
`
)
;


 
 
 
 
 
 
 
 
 
 
}


 
 
 
 
 
 
 
 
}
)
;


 
 
 
 
 
 
}


 
 
 
 
}


 
 
}


}




c
o
n
s
t
 
e
d
i
t
P
r
o
j
e
c
t
 
=
 
(
p
r
o
j
e
c
t
)
 
=
>
 
{


 
 
e
d
i
t
i
n
g
P
r
o
j
e
c
t
.
v
a
l
u
e
 
=
 
p
r
o
j
e
c
t


 
 
O
b
j
e
c
t
.
a
s
s
i
g
n
(
p
r
o
j
e
c
t
F
o
r
m
,
 
{


 
 
 
 
n
a
m
e
:
 
p
r
o
j
e
c
t
.
n
a
m
e
,


 
 
 
 
d
e
s
c
r
i
p
t
i
o
n
:
 
p
r
o
j
e
c
t
.
d
e
s
c
r
i
p
t
i
o
n
,


 
 
 
 
s
t
a
r
t
_
d
a
t
e
:
 
p
r
o
j
e
c
t
.
s
t
a
r
t
_
d
a
t
e
,


 
 
 
 
e
n
d
_
d
a
t
e
:
 
p
r
o
j
e
c
t
.
e
n
d
_
d
a
t
e


 
 
}
)


 
 
s
h
o
w
C
r
e
a
t
e
D
i
a
l
o
g
.
v
a
l
u
e
 
=
 
t
r
u
e


}




c
o
n
s
t
 
d
e
l
e
t
e
P
r
o
j
e
c
t
 
=
 
a
s
y
n
c
 
(
p
r
o
j
e
c
t
)
 
=
>
 
{


 
 
t
r
y
 
{


 
 
 
 
a
w
a
i
t
 
E
l
M
e
s
s
a
g
e
B
o
x
.
c
o
n
f
i
r
m
(
`
确
定
要
删
除
项
目
 
"
$
{
p
r
o
j
e
c
t
.
n
a
m
e
}
"
 
吗
？
`
,
 
'
确
认
删
除
'
,
 
{


 
 
 
 
 
 
c
o
n
f
i
r
m
B
u
t
t
o
n
T
e
x
t
:
 
'
确
定
'
,


 
 
 
 
 
 
c
a
n
c
e
l
B
u
t
t
o
n
T
e
x
t
:
 
'
取
消
'
,


 
 
 
 
 
 
t
y
p
e
:
 
'
w
a
r
n
i
n
g
'


 
 
 
 
}
)


 
 
 
 
a
w
a
i
t
 
a
x
i
o
s
.
d
e
l
e
t
e
(
`
$
{
A
P
I
_
B
A
S
E
}
/
p
r
o
j
e
c
t
s
/
p
r
o
j
e
c
t
s
/
$
{
p
r
o
j
e
c
t
.
i
d
}
/
`
)


 
 
 
 
E
l
M
e
s
s
a
g
e
.
s
u
c
c
e
s
s
(
'
项
目
删
除
成
功
'
)


 
 
 
 
l
o
a
d
P
r
o
j
e
c
t
s
(
)


 
 
 
 
i
f
 
(
s
e
l
e
c
t
e
d
P
r
o
j
e
c
t
.
v
a
l
u
e
?
.
i
d
 
=
=
=
 
p
r
o
j
e
c
t
.
i
d
)
 
{


 
 
 
 
 
 
h
a
n
d
l
e
B
a
c
k
(
)


 
 
 
 
}


 
 
}
 
c
a
t
c
h
 
(
e
r
r
o
r
)
 
{


 
 
 
 
i
f
 
(
e
r
r
o
r
 
!
=
=
 
'
c
a
n
c
e
l
'
)
 
{


 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
'
项
目
删
除
失
败
'
)


 
 
 
 
 
 
c
o
n
s
o
l
e
.
e
r
r
o
r
(
e
r
r
o
r
)


 
 
 
 
}


 
 
}


}




c
o
n
s
t
 
t
a
b
l
e
R
o
w
C
l
a
s
s
N
a
m
e
 
=
 
(
{
 
r
o
w
 
}
)
 
=
>
 
{


 
 
r
e
t
u
r
n
 
r
o
w
.
i
d
 
=
=
=
 
s
e
l
e
c
t
e
d
P
r
o
j
e
c
t
.
v
a
l
u
e
?
.
i
d
 
?
 
'
s
e
l
e
c
t
e
d
-
r
o
w
'
 
:
 
'
'


}




c
o
n
s
t
 
r
e
s
e
t
P
r
o
j
e
c
t
F
o
r
m
 
=
 
(
)
 
=
>
 
{


 
 
O
b
j
e
c
t
.
a
s
s
i
g
n
(
p
r
o
j
e
c
t
F
o
r
m
,
 
{


 
 
 
 
n
a
m
e
:
 
'
'
,


 
 
 
 
d
e
s
c
r
i
p
t
i
o
n
:
 
'
'
,


 
 
 
 
s
t
a
r
t
_
d
a
t
e
:
 
'
'
,


 
 
 
 
e
n
d
_
d
a
t
e
:
 
'
'
,


 
 
 
 
o
w
n
e
r
:
 
1


 
 
}
)


 
 
e
d
i
t
i
n
g
P
r
o
j
e
c
t
.
v
a
l
u
e
 
=
 
n
u
l
l


}




c
o
n
s
t
 
r
e
s
e
t
T
a
s
k
F
o
r
m
 
=
 
(
)
 
=
>
 
{


 
 
O
b
j
e
c
t
.
a
s
s
i
g
n
(
t
a
s
k
F
o
r
m
,
 
{


 
 
 
 
n
a
m
e
:
 
'
'
,


 
 
 
 
d
e
s
c
r
i
p
t
i
o
n
:
 
'
'
,


 
 
 
 
s
t
a
r
t
_
d
a
t
e
:
 
'
'
,


 
 
 
 
e
n
d
_
d
a
t
e
:
 
'
'
,


 
 
 
 
d
u
r
a
t
i
o
n
:
 
1
,


 
 
 
 
p
r
o
g
r
e
s
s
:
 
0
,


 
 
 
 
p
r
i
o
r
i
t
y
:
 
2
,


 
 
 
 
p
a
r
e
n
t
:
 
c
u
r
r
e
n
t
P
a
r
e
n
t
T
a
s
k
.
v
a
l
u
e
 
?
 
c
u
r
r
e
n
t
P
a
r
e
n
t
T
a
s
k
.
v
a
l
u
e
.
i
d
 
:
 
n
u
l
l


 
 
}
)


 
 
e
d
i
t
i
n
g
T
a
s
k
.
v
a
l
u
e
 
=
 
n
u
l
l


}




c
o
n
s
t
 
r
e
f
r
e
s
h
T
a
s
k
T
r
e
e
 
=
 
a
s
y
n
c
 
(
)
 
=
>
 
{


 
 
i
f
 
(
s
e
l
e
c
t
e
d
P
r
o
j
e
c
t
.
v
a
l
u
e
)
 
{


 
 
 
 
a
w
a
i
t
 
l
o
a
d
T
a
s
k
T
r
e
e
D
a
t
a
(
s
e
l
e
c
t
e
d
P
r
o
j
e
c
t
.
v
a
l
u
e
.
i
d
)


 
 
 
 
E
l
M
e
s
s
a
g
e
.
s
u
c
c
e
s
s
(
'
任
务
树
已
刷
新
'
)


 
 
}


}




/
/
 
新
增
：
树
节
点
展
开
处
理


c
o
n
s
t
 
h
a
n
d
l
e
N
o
d
e
E
x
p
a
n
d
 
=
 
(
d
a
t
a
,
 
n
o
d
e
)
 
=
>
 
{


 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
节
点
展
开
:
'
,
 
d
a
t
a
.
i
d
,
 
d
a
t
a
.
l
a
b
e
l
)


 
 
i
f
 
(
!
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
.
i
n
c
l
u
d
e
s
(
d
a
t
a
.
i
d
)
)
 
{


 
 
 
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
.
p
u
s
h
(
d
a
t
a
.
i
d
)


 
 
}


}




/
/
 
新
增
：
树
节
点
折
叠
处
理


c
o
n
s
t
 
h
a
n
d
l
e
N
o
d
e
C
o
l
l
a
p
s
e
 
=
 
(
d
a
t
a
,
 
n
o
d
e
)
 
=
>
 
{


 
 
c
o
n
s
o
l
e
.
l
o
g
(
'
节
点
折
叠
:
'
,
 
d
a
t
a
.
i
d
,
 
d
a
t
a
.
l
a
b
e
l
)


 
 
c
o
n
s
t
 
i
n
d
e
x
 
=
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
.
i
n
d
e
x
O
f
(
d
a
t
a
.
i
d
)


 
 
i
f
 
(
i
n
d
e
x
 
>
 
-
1
)
 
{


 
 
 
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
.
s
p
l
i
c
e
(
i
n
d
e
x
,
 
1
)


 
 
}


}




/
/
 
新
增
：
计
算
树
的
最
大
深
度
（
用
于
调
试
）


c
o
n
s
t
 
c
a
l
c
u
l
a
t
e
T
r
e
e
D
e
p
t
h
 
=
 
(
n
o
d
e
s
,
 
c
u
r
r
e
n
t
D
e
p
t
h
 
=
 
0
)
 
=
>
 
{


 
 
i
f
 
(
!
n
o
d
e
s
 
|
|
 
n
o
d
e
s
.
l
e
n
g
t
h
 
=
=
=
 
0
)
 
r
e
t
u
r
n
 
c
u
r
r
e
n
t
D
e
p
t
h


 
 


 
 
l
e
t
 
m
a
x
D
e
p
t
h
 
=
 
c
u
r
r
e
n
t
D
e
p
t
h


 
 
f
o
r
 
(
c
o
n
s
t
 
n
o
d
e
 
o
f
 
n
o
d
e
s
)
 
{


 
 
 
 
c
o
n
s
t
 
d
e
p
t
h
 
=
 
c
a
l
c
u
l
a
t
e
T
r
e
e
D
e
p
t
h
(
n
o
d
e
.
c
h
i
l
d
r
e
n
,
 
c
u
r
r
e
n
t
D
e
p
t
h
 
+
 
1
)


 
 
 
 
m
a
x
D
e
p
t
h
 
=
 
M
a
t
h
.
m
a
x
(
m
a
x
D
e
p
t
h
,
 
d
e
p
t
h
)


 
 
}


 
 
r
e
t
u
r
n
 
m
a
x
D
e
p
t
h


}




c
o
n
s
t
 
e
d
i
t
T
a
s
k
 
=
 
(
t
a
s
k
)
 
=
>
 
{


 
 
e
d
i
t
i
n
g
T
a
s
k
.
v
a
l
u
e
 
=
 
t
a
s
k
;


 
 
c
u
r
r
e
n
t
P
a
r
e
n
t
T
a
s
k
.
v
a
l
u
e
 
=
 
n
u
l
l
;


 
 
O
b
j
e
c
t
.
a
s
s
i
g
n
(
t
a
s
k
F
o
r
m
,
 
{


 
 
 
 
n
a
m
e
:
 
t
a
s
k
.
l
a
b
e
l
 
|
|
 
t
a
s
k
.
n
a
m
e
 
|
|
 
'
'
,


 
 
 
 
d
e
s
c
r
i
p
t
i
o
n
:
 
t
a
s
k
.
d
e
s
c
r
i
p
t
i
o
n
 
|
|
 
'
'
,


 
 
 
 
s
t
a
r
t
_
d
a
t
e
:
 
t
a
s
k
.
s
t
a
r
t
_
d
a
t
e
 
|
|
 
'
'
,


 
 
 
 
e
n
d
_
d
a
t
e
:
 
t
a
s
k
.
e
n
d
_
d
a
t
e
 
|
|
 
'
'
,


 
 
 
 
d
u
r
a
t
i
o
n
:
 
t
a
s
k
.
d
u
r
a
t
i
o
n
 
|
|
 
1
,


 
 
 
 
p
r
o
g
r
e
s
s
:
 
t
a
s
k
.
p
r
o
g
r
e
s
s
 
|
|
 
0
,


 
 
 
 
p
r
i
o
r
i
t
y
:
 
t
a
s
k
.
p
r
i
o
r
i
t
y
 
|
|
 
2
,


 
 
 
 
p
a
r
e
n
t
:
 
t
a
s
k
.
p
a
r
e
n
t
_
i
d
 
|
|
 
n
u
l
l


 
 
}
)
;


 
 
s
h
o
w
T
a
s
k
D
i
a
l
o
g
.
v
a
l
u
e
 
=
 
t
r
u
e
;


 
 
s
e
t
T
i
m
e
o
u
t
(
(
)
 
=
>
 
{


 
 
 
 
c
o
n
s
t
 
n
a
m
e
I
n
p
u
t
 
=
 
d
o
c
u
m
e
n
t
.
q
u
e
r
y
S
e
l
e
c
t
o
r
(
'
.
e
l
-
d
i
a
l
o
g
 
i
n
p
u
t
[
p
l
a
c
e
h
o
l
d
e
r
=
"
任
务
名
称
"
]
'
)
;


 
 
 
 
i
f
 
(
n
a
m
e
I
n
p
u
t
)
 
n
a
m
e
I
n
p
u
t
.
f
o
c
u
s
(
)
;


 
 
}
,
 
1
0
0
)
;


}




c
o
n
s
t
 
a
d
d
C
h
i
l
d
T
a
s
k
 
=
 
(
p
a
r
e
n
t
T
a
s
k
)
 
=
>
 
{


 
 
e
d
i
t
i
n
g
T
a
s
k
.
v
a
l
u
e
 
=
 
n
u
l
l
;


 
 
c
u
r
r
e
n
t
P
a
r
e
n
t
T
a
s
k
.
v
a
l
u
e
 
=
 
p
a
r
e
n
t
T
a
s
k
;


 
 
r
e
s
e
t
T
a
s
k
F
o
r
m
(
)
;


 
 
t
a
s
k
F
o
r
m
.
p
a
r
e
n
t
 
=
 
p
a
r
e
n
t
T
a
s
k
.
i
d
;


 
 
s
h
o
w
T
a
s
k
D
i
a
l
o
g
.
v
a
l
u
e
 
=
 
t
r
u
e
;


 
 
s
e
t
T
i
m
e
o
u
t
(
(
)
 
=
>
 
{


 
 
 
 
c
o
n
s
t
 
n
a
m
e
I
n
p
u
t
 
=
 
d
o
c
u
m
e
n
t
.
q
u
e
r
y
S
e
l
e
c
t
o
r
(
'
.
e
l
-
d
i
a
l
o
g
 
i
n
p
u
t
[
p
l
a
c
e
h
o
l
d
e
r
=
"
任
务
名
称
"
]
'
)
;


 
 
 
 
i
f
 
(
n
a
m
e
I
n
p
u
t
)
 
n
a
m
e
I
n
p
u
t
.
f
o
c
u
s
(
)
;


 
 
}
,
 
1
0
0
)
;


}




/
/
 
新
增
：
手
动
展
开
/
折
叠
所
有
节
点
的
功
能


c
o
n
s
t
 
e
x
p
a
n
d
A
l
l
N
o
d
e
s
 
=
 
(
)
 
=
>
 
{


 
 
c
o
n
s
t
 
c
o
l
l
e
c
t
A
l
l
K
e
y
s
 
=
 
(
n
o
d
e
s
)
 
=
>
 
{


 
 
 
 
c
o
n
s
t
 
k
e
y
s
 
=
 
[
]


 
 
 
 
c
o
n
s
t
 
t
r
a
v
e
r
s
e
 
=
 
(
n
o
d
e
L
i
s
t
)
 
=
>
 
{


 
 
 
 
 
 
i
f
 
(
!
n
o
d
e
L
i
s
t
)
 
r
e
t
u
r
n


 
 
 
 
 
 
n
o
d
e
L
i
s
t
.
f
o
r
E
a
c
h
(
n
o
d
e
 
=
>
 
{


 
 
 
 
 
 
 
 
k
e
y
s
.
p
u
s
h
(
n
o
d
e
.
i
d
)


 
 
 
 
 
 
 
 
i
f
 
(
n
o
d
e
.
c
h
i
l
d
r
e
n
 
&
&
 
n
o
d
e
.
c
h
i
l
d
r
e
n
.
l
e
n
g
t
h
 
>
 
0
)
 
{


 
 
 
 
 
 
 
 
 
 
t
r
a
v
e
r
s
e
(
n
o
d
e
.
c
h
i
l
d
r
e
n
)


 
 
 
 
 
 
 
 
}


 
 
 
 
 
 
}
)


 
 
 
 
}


 
 
 
 
t
r
a
v
e
r
s
e
(
n
o
d
e
s
)


 
 
 
 
r
e
t
u
r
n
 
k
e
y
s


 
 
}


 
 


 
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
 
=
 
c
o
l
l
e
c
t
A
l
l
K
e
y
s
(
t
a
s
k
T
r
e
e
D
a
t
a
.
v
a
l
u
e
)


 
 
E
l
M
e
s
s
a
g
e
.
s
u
c
c
e
s
s
(
'
已
展
开
所
有
节
点
'
)


}




c
o
n
s
t
 
c
o
l
l
a
p
s
e
A
l
l
N
o
d
e
s
 
=
 
(
)
 
=
>
 
{


 
 
e
x
p
a
n
d
e
d
K
e
y
s
.
v
a
l
u
e
 
=
 
[
]


 
 
E
l
M
e
s
s
a
g
e
.
s
u
c
c
e
s
s
(
'
已
折
叠
所
有
节
点
'
)


}




c
o
n
s
t
 
d
e
l
e
t
e
T
a
s
k
 
=
 
a
s
y
n
c
 
(
t
a
s
k
)
 
=
>
 
{


 
 
t
r
y
 
{


 
 
 
 
a
w
a
i
t
 
E
l
M
e
s
s
a
g
e
B
o
x
.
c
o
n
f
i
r
m
(


 
 
 
 
 
 
`
确
定
要
删
除
任
务
 
"
$
{
t
a
s
k
.
l
a
b
e
l
 
|
|
 
t
a
s
k
.
n
a
m
e
}
"
 
吗
？
`
,


 
 
 
 
 
 
'
确
认
删
除
'
,


 
 
 
 
 
 
{
 
t
y
p
e
:
 
'
w
a
r
n
i
n
g
'
 
}


 
 
 
 
)


 
 
 
 
a
w
a
i
t
 
a
x
i
o
s
.
d
e
l
e
t
e
(
`
$
{
A
P
I
_
B
A
S
E
}
/
p
r
o
j
e
c
t
s
/
t
a
s
k
s
/
$
{
t
a
s
k
.
i
d
}
/
`
)


 
 
 
 
E
l
M
e
s
s
a
g
e
.
s
u
c
c
e
s
s
(
'
任
务
删
除
成
功
'
)


 
 
 
 
a
w
a
i
t
 
r
e
f
r
e
s
h
T
a
s
k
T
r
e
e
(
)


 
 
}
 
c
a
t
c
h
 
(
e
r
r
o
r
)
 
{


 
 
 
 
i
f
 
(
e
r
r
o
r
 
!
=
=
 
'
c
a
n
c
e
l
'
)
 
{


 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
'
任
务
删
除
失
败
'
)


 
 
 
 
 
 
c
o
n
s
o
l
e
.
e
r
r
o
r
(
e
r
r
o
r
)


 
 
 
 
}


 
 
}


}




c
o
n
s
t
 
s
a
v
e
T
a
s
k
 
=
 
a
s
y
n
c
 
(
)
 
=
>
 
{


 
 
t
r
y
 
{


 
 
 
 
c
o
n
s
t
 
f
o
r
m
a
t
D
a
t
e
 
=
 
(
d
a
t
e
)
 
=
>
 
{


 
 
 
 
 
 
i
f
 
(
!
d
a
t
e
)
 
r
e
t
u
r
n
 
n
u
l
l
;


 
 
 
 
 
 
c
o
n
s
t
 
d
 
=
 
n
e
w
 
D
a
t
e
(
d
a
t
e
)
;


 
 
 
 
 
 
c
o
n
s
t
 
y
e
a
r
 
=
 
d
.
g
e
t
F
u
l
l
Y
e
a
r
(
)
;


 
 
 
 
 
 
c
o
n
s
t
 
m
o
n
t
h
 
=
 
S
t
r
i
n
g
(
d
.
g
e
t
M
o
n
t
h
(
)
 
+
 
1
)
.
p
a
d
S
t
a
r
t
(
2
,
 
'
0
'
)
;


 
 
 
 
 
 
c
o
n
s
t
 
d
a
y
 
=
 
S
t
r
i
n
g
(
d
.
g
e
t
D
a
t
e
(
)
)
.
p
a
d
S
t
a
r
t
(
2
,
 
'
0
'
)
;


 
 
 
 
 
 
r
e
t
u
r
n
 
`
$
{
y
e
a
r
}
-
$
{
m
o
n
t
h
}
-
$
{
d
a
y
}
`
;


 
 
 
 
}
;




 
 
 
 
c
o
n
s
t
 
t
a
s
k
D
a
t
a
 
=
 
{


 
 
 
 
 
 
n
a
m
e
:
 
t
a
s
k
F
o
r
m
.
n
a
m
e
.
t
r
i
m
(
)
,


 
 
 
 
 
 
d
e
s
c
r
i
p
t
i
o
n
:
 
t
a
s
k
F
o
r
m
.
d
e
s
c
r
i
p
t
i
o
n
.
t
r
i
m
(
)
 
|
|
 
'
'
,


 
 
 
 
 
 
s
t
a
r
t
_
d
a
t
e
:
 
f
o
r
m
a
t
D
a
t
e
(
t
a
s
k
F
o
r
m
.
s
t
a
r
t
_
d
a
t
e
)
,


 
 
 
 
 
 
e
n
d
_
d
a
t
e
:
 
f
o
r
m
a
t
D
a
t
e
(
t
a
s
k
F
o
r
m
.
e
n
d
_
d
a
t
e
)
,


 
 
 
 
 
 
d
u
r
a
t
i
o
n
:
 
t
a
s
k
F
o
r
m
.
d
u
r
a
t
i
o
n
 
|
|
 
1
,


 
 
 
 
 
 
p
r
o
g
r
e
s
s
:
 
t
a
s
k
F
o
r
m
.
p
r
o
g
r
e
s
s
 
|
|
 
0
,


 
 
 
 
 
 
p
r
i
o
r
i
t
y
:
 
t
a
s
k
F
o
r
m
.
p
r
i
o
r
i
t
y
 
|
|
 
2
,


 
 
 
 
 
 
p
r
o
j
e
c
t
:
 
s
e
l
e
c
t
e
d
P
r
o
j
e
c
t
.
v
a
l
u
e
?
.
i
d
,


 
 
 
 
 
 
p
a
r
e
n
t
:
 
t
a
s
k
F
o
r
m
.
p
a
r
e
n
t
 
|
|
 
n
u
l
l


 
 
 
 
}
;




 
 
 
 
i
f
 
(
!
t
a
s
k
D
a
t
a
.
n
a
m
e
)
 
{


 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
'
任
务
名
称
不
能
为
空
'
)
;


 
 
 
 
 
 
r
e
t
u
r
n
;


 
 
 
 
}


 
 
 
 
i
f
 
(
!
t
a
s
k
D
a
t
a
.
s
t
a
r
t
_
d
a
t
e
 
|
|
 
!
t
a
s
k
D
a
t
a
.
e
n
d
_
d
a
t
e
)
 
{


 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
'
请
填
写
完
整
的
日
期
信
息
'
)
;


 
 
 
 
 
 
r
e
t
u
r
n
;


 
 
 
 
}


 
 
 
 
i
f
 
(
!
t
a
s
k
D
a
t
a
.
p
r
o
j
e
c
t
)
 
{


 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
'
未
选
择
项
目
，
请
先
选
择
一
个
项
目
'
)
;


 
 
 
 
 
 
r
e
t
u
r
n
;


 
 
 
 
}


 
 
 
 
i
f
 
(
n
e
w
 
D
a
t
e
(
t
a
s
k
D
a
t
a
.
s
t
a
r
t
_
d
a
t
e
)
 
>
 
n
e
w
 
D
a
t
e
(
t
a
s
k
D
a
t
a
.
e
n
d
_
d
a
t
e
)
)
 
{


 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
'
开
始
日
期
不
能
晚
于
结
束
日
期
'
)
;


 
 
 
 
 
 
r
e
t
u
r
n
;


 
 
 
 
}




 
 
 
 
i
f
 
(
e
d
i
t
i
n
g
T
a
s
k
.
v
a
l
u
e
)
 
{


 
 
 
 
 
 
a
w
a
i
t
 
a
x
i
o
s
.
p
u
t
(
`
$
{
A
P
I
_
B
A
S
E
}
/
p
r
o
j
e
c
t
s
/
t
a
s
k
s
/
$
{
e
d
i
t
i
n
g
T
a
s
k
.
v
a
l
u
e
.
i
d
}
/
`
,
 
t
a
s
k
D
a
t
a
)
;


 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
s
u
c
c
e
s
s
(
'
任
务
更
新
成
功
'
)
;


 
 
 
 
}
 
e
l
s
e
 
{


 
 
 
 
 
 
a
w
a
i
t
 
a
x
i
o
s
.
p
o
s
t
(
`
$
{
A
P
I
_
B
A
S
E
}
/
p
r
o
j
e
c
t
s
/
t
a
s
k
s
/
`
,
 
t
a
s
k
D
a
t
a
)
;


 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
s
u
c
c
e
s
s
(
'
任
务
创
建
成
功
'
)
;


 
 
 
 
}




 
 
 
 
s
h
o
w
T
a
s
k
D
i
a
l
o
g
.
v
a
l
u
e
 
=
 
f
a
l
s
e
;


 
 
 
 
a
w
a
i
t
 
r
e
f
r
e
s
h
T
a
s
k
T
r
e
e
(
)
;


 
 
 
 
r
e
s
e
t
T
a
s
k
F
o
r
m
(
)
;


 
 
}
 
c
a
t
c
h
 
(
e
r
r
o
r
)
 
{


 
 
 
 
c
o
n
s
t
 
e
r
r
o
r
M
e
s
s
a
g
e
 
=
 
e
d
i
t
i
n
g
T
a
s
k
.
v
a
l
u
e
 
?
 
'
任
务
更
新
失
败
'
 
:
 
'
任
务
创
建
失
败
'
;


 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
e
r
r
o
r
M
e
s
s
a
g
e
)
;


 
 
 
 
c
o
n
s
o
l
e
.
e
r
r
o
r
(
'
任
务
保
存
错
误
:
'
,
 
e
r
r
o
r
.
r
e
s
p
o
n
s
e
?
.
d
a
t
a
 
|
|
 
e
r
r
o
r
.
m
e
s
s
a
g
e
)
;


 
 
 
 
i
f
 
(
e
r
r
o
r
.
r
e
s
p
o
n
s
e
?
.
d
a
t
a
)
 
{


 
 
 
 
 
 
c
o
n
s
t
 
e
r
r
o
r
D
e
t
a
i
l
s
 
=
 
e
r
r
o
r
.
r
e
s
p
o
n
s
e
.
d
a
t
a
;


 
 
 
 
 
 
i
f
 
(
t
y
p
e
o
f
 
e
r
r
o
r
D
e
t
a
i
l
s
 
=
=
=
 
'
o
b
j
e
c
t
'
)
 
{


 
 
 
 
 
 
 
 
O
b
j
e
c
t
.
k
e
y
s
(
e
r
r
o
r
D
e
t
a
i
l
s
)
.
f
o
r
E
a
c
h
(
k
e
y
 
=
>
 
{


 
 
 
 
 
 
 
 
 
 
c
o
n
s
t
 
f
i
e
l
d
E
r
r
o
r
s
 
=
 
e
r
r
o
r
D
e
t
a
i
l
s
[
k
e
y
]
;


 
 
 
 
 
 
 
 
 
 
i
f
 
(
A
r
r
a
y
.
i
s
A
r
r
a
y
(
f
i
e
l
d
E
r
r
o
r
s
)
)
 
{


 
 
 
 
 
 
 
 
 
 
 
 
E
l
M
e
s
s
a
g
e
.
e
r
r
o
r
(
`
$
{
k
e
y
}
:
 
$
{
f
i
e
l
d
E
r
r
o
r
s
.
j
o
i
n
(
'
,
 
'
)
}
`
)
;


 
 
 
 
 
 
 
 
 
 
}


 
 
 
 
 
 
 
 
}
)
;


 
 
 
 
 
 
}


 
 
 
 
}


 
 
}


}


<
/
s
c
r
i
p
t
>




<
s
t
y
l
e
 
s
c
o
p
e
d
>


.
p
r
o
j
e
c
t
-
m
a
n
a
g
e
m
e
n
t
-
c
o
n
t
a
i
n
e
r
 
{


 
 
p
a
d
d
i
n
g
:
 
1
0
p
x
;
 
/
*
 
移
动
端
缩
小
内
边
距
 
*
/


 
 
h
e
i
g
h
t
:
 
1
0
0
v
h
;


 
 
d
i
s
p
l
a
y
:
 
f
l
e
x
;


 
 
f
l
e
x
-
d
i
r
e
c
t
i
o
n
:
 
c
o
l
u
m
n
;


 
 
b
o
x
-
s
i
z
i
n
g
:
 
b
o
r
d
e
r
-
b
o
x
;
 
/
*
 
防
止
p
a
d
d
i
n
g
导
致
溢
出
 
*
/


 
 
o
v
e
r
f
l
o
w
:
 
a
u
t
o
;
 
/
*
 
允
许
整
体
滚
动
 
*
/


}




.
m
a
i
n
-
c
o
n
t
e
n
t
 
{


 
 
d
i
s
p
l
a
y
:
 
f
l
e
x
;


 
 
g
a
p
:
 
1
5
p
x
;


 
 
f
l
e
x
:
 
1
;


 
 
m
a
r
g
i
n
-
t
o
p
:
 
1
5
p
x
;


 
 
f
l
e
x
-
w
r
a
p
:
 
w
r
a
p
;
 
/
*
 
允
许
换
行
 
*
/


}




/
*
 
项
目
列
表
区
域
响
应
式
 
*
/


.
p
r
o
j
e
c
t
-
l
i
s
t
-
s
e
c
t
i
o
n
 
{


 
 
f
l
e
x
:
 
1
;


 
 
m
i
n
-
w
i
d
t
h
:
 
2
8
0
p
x
;
 
/
*
 
移
动
端
最
小
宽
度
 
*
/


 
 
m
a
x
-
w
i
d
t
h
:
 
1
0
0
%
;


}




/
*
 
项
目
详
情
区
域
响
应
式
 
*
/


.
p
r
o
j
e
c
t
-
d
e
t
a
i
l
-
s
e
c
t
i
o
n
 
{


 
 
f
l
e
x
:
 
1
;
 
/
*
 
移
动
端
和
列
表
等
分
 
*
/


 
 
m
i
n
-
w
i
d
t
h
:
 
2
8
0
p
x
;


 
 
m
a
x
-
w
i
d
t
h
:
 
1
0
0
%
;


}




.
c
a
r
d
-
h
e
a
d
e
r
 
{


 
 
d
i
s
p
l
a
y
:
 
f
l
e
x
;


 
 
j
u
s
t
i
f
y
-
c
o
n
t
e
n
t
:
 
s
p
a
c
e
-
b
e
t
w
e
e
n
;


 
 
a
l
i
g
n
-
i
t
e
m
s
:
 
c
e
n
t
e
r
;


}




/
*
 
甘
特
图
容
器
响
应
式
 
*
/


.
g
a
n
t
t
-
c
o
n
t
a
i
n
e
r
 
{


 
 
w
i
d
t
h
:
 
1
0
0
%
;


 
 
h
e
i
g
h
t
:
 
4
0
0
p
x
;
 
/
*
 
基
础
高
度
 
*
/


 
 
m
i
n
-
h
e
i
g
h
t
:
 
3
0
0
p
x
;


 
 
m
a
x
-
h
e
i
g
h
t
:
 
6
0
0
p
x
;


 
 
p
a
d
d
i
n
g
:
 
4
p
x
;


 
 
b
a
c
k
g
r
o
u
n
d
-
c
o
l
o
r
:
 
#
f
f
f
;


 
 
b
o
r
d
e
r
-
r
a
d
i
u
s
:
 
8
p
x
;


 
 
b
o
x
-
s
h
a
d
o
w
:
 
0
 
1
p
x
 
2
p
x
 
#
e
e
e
;


}




.
g
a
n
t
t
-
c
o
n
t
e
n
t
 
{


 
 
w
i
d
t
h
:
 
1
0
0
%
;


 
 
h
e
i
g
h
t
:
 
c
a
l
c
(
1
0
0
%
 
-
 
4
0
p
x
)
;
 
/
*
 
预
留
按
钮
空
间
 
*
/


}




/
*
 
任
务
树
容
器
响
应
式
 
*
/


.
t
a
s
k
-
t
r
e
e
-
c
o
n
t
a
i
n
e
r
 
{


 
 
w
i
d
t
h
:
 
1
0
0
%
;


 
 
h
e
i
g
h
t
:
 
4
0
0
p
x
;


 
 
m
i
n
-
h
e
i
g
h
t
:
 
3
0
0
p
x
;


 
 
m
a
x
-
h
e
i
g
h
t
:
 
6
0
0
p
x
;


 
 
p
a
d
d
i
n
g
:
 
4
p
x
;


 
 
b
a
c
k
g
r
o
u
n
d
-
c
o
l
o
r
:
 
#
f
f
f
;


 
 
b
o
r
d
e
r
-
r
a
d
i
u
s
:
 
8
p
x
;


 
 
b
o
x
-
s
h
a
d
o
w
:
 
0
 
1
p
x
 
2
p
x
 
#
e
e
e
;


 
 
o
v
e
r
f
l
o
w
:
 
a
u
t
o
;


}




.
t
a
s
k
-
t
r
e
e
-
c
o
n
t
e
n
t
 
{


 
 
w
i
d
t
h
:
 
1
0
0
%
;


 
 
h
e
i
g
h
t
:
 
c
a
l
c
(
1
0
0
%
 
-
 
4
0
p
x
)
;


}




/
*
 
树
形
节
点
样
式
优
化
 
*
/


.
t
r
e
e
-
n
o
d
e
-
c
o
n
t
e
n
t
 
{


 
 
d
i
s
p
l
a
y
:
 
f
l
e
x
;


 
 
j
u
s
t
i
f
y
-
c
o
n
t
e
n
t
:
 
s
p
a
c
e
-
b
e
t
w
e
e
n
;


 
 
a
l
i
g
n
-
i
t
e
m
s
:
 
c
e
n
t
e
r
;


 
 
w
i
d
t
h
:
 
1
0
0
%
;


 
 
p
a
d
d
i
n
g
:
 
2
p
x
 
0
;


}




.
n
o
d
e
-
l
e
f
t
 
{


 
 
d
i
s
p
l
a
y
:
 
f
l
e
x
;


 
 
a
l
i
g
n
-
i
t
e
m
s
:
 
c
e
n
t
e
r
;


 
 
f
l
e
x
:
 
1
;


 
 
m
i
n
-
w
i
d
t
h
:
 
0
;
 
/
*
 
解
决
文
字
溢
出
 
*
/


 
 
g
a
p
:
 
8
p
x
;


}




.
n
o
d
e
-
r
i
g
h
t
 
{


 
 
d
i
s
p
l
a
y
:
 
f
l
e
x
;


 
 
a
l
i
g
n
-
i
t
e
m
s
:
 
c
e
n
t
e
r
;


 
 
g
a
p
:
 
8
p
x
;


}




.
n
o
d
e
-
a
c
t
i
o
n
s
 
{


 
 
d
i
s
p
l
a
y
:
 
f
l
e
x
;


 
 
g
a
p
:
 
4
p
x
;


}




/
*
 
文
字
截
断
 
*
/


.
t
r
u
n
c
a
t
e
-
t
e
x
t
 
{


 
 
w
h
i
t
e
-
s
p
a
c
e
:
 
n
o
w
r
a
p
;


 
 
o
v
e
r
f
l
o
w
:
 
h
i
d
d
e
n
;


 
 
t
e
x
t
-
o
v
e
r
f
l
o
w
:
 
e
l
l
i
p
s
i
s
;


 
 
m
a
x
-
w
i
d
t
h
:
 
1
0
0
%
;


}




/
*
 
表
格
操
作
按
钮
容
器
 
*
/


.
t
a
b
l
e
-
o
p
e
r
a
t
i
o
n
-
b
u
t
t
o
n
s
 
{


 
 
d
i
s
p
l
a
y
:
 
f
l
e
x
;


 
 
g
a
p
:
 
8
p
x
;


 
 
a
l
i
g
n
-
i
t
e
m
s
:
 
c
e
n
t
e
r
;


}




.
s
e
l
e
c
t
e
d
-
r
o
w
 
{


 
 
b
a
c
k
g
r
o
u
n
d
-
c
o
l
o
r
:
 
#
e
c
f
5
f
f
 
!
i
m
p
o
r
t
a
n
t
;


}




/
*
 
日
期
选
择
器
样
式
修
复
 
*
/


:
d
e
e
p
(
.
e
l
-
d
a
t
e
-
e
d
i
t
o
r
)
 
{


 
 
w
i
d
t
h
:
 
1
0
0
%
;


}




:
d
e
e
p
(
.
e
l
-
d
a
t
e
-
e
d
i
t
o
r
 
.
e
l
-
i
n
p
u
t
_
_
i
n
n
e
r
)
 
{


 
 
w
i
d
t
h
:
 
1
0
0
%
;


}




/
*
 
甘
特
图
样
式
覆
盖
 
*
/


:
d
e
e
p
(
.
g
a
n
t
t
-
t
a
s
k
)
 
{


 
 
b
o
r
d
e
r
-
r
a
d
i
u
s
:
 
4
p
x
;


 
 
t
r
a
n
s
i
t
i
o
n
:
 
a
l
l
 
0
.
2
s
;


}


:
d
e
e
p
(
.
g
a
n
t
t
-
t
a
s
k
:
h
o
v
e
r
)
 
{


 
 
t
r
a
n
s
f
o
r
m
:
 
s
c
a
l
e
(
1
.
0
2
)
;


}


:
d
e
e
p
(
.
g
a
n
t
t
-
h
e
a
d
e
r
)
 
{


 
 
b
a
c
k
g
r
o
u
n
d
-
c
o
l
o
r
:
 
#
f
5
f
5
f
5
;


 
 
b
o
r
d
e
r
-
b
o
t
t
o
m
:
 
1
p
x
 
s
o
l
i
d
 
#
e
e
e
;


}




/
*
 
媒
体
查
询
 
-
 
平
板
 
(
7
6
8
p
x
以
下
)
 
*
/


@
m
e
d
i
a
 
(
m
a
x
-
w
i
d
t
h
:
 
7
6
8
p
x
)
 
{


 
 
.
m
a
i
n
-
c
o
n
t
e
n
t
 
{


 
 
 
 
f
l
e
x
-
d
i
r
e
c
t
i
o
n
:
 
c
o
l
u
m
n
;
 
/
*
 
垂
直
排
列
 
*
/


 
 
 
 
g
a
p
:
 
1
0
p
x
;


 
 
}




 
 
.
g
a
n
t
t
-
c
o
n
t
a
i
n
e
r
,
 
.
t
a
s
k
-
t
r
e
e
-
c
o
n
t
a
i
n
e
r
 
{


 
 
 
 
h
e
i
g
h
t
:
 
3
0
0
p
x
;
 
/
*
 
平
板
缩
小
高
度
 
*
/


 
 
}




 
 
/
*
 
隐
藏
优
先
级
文
字
，
只
留
图
标
 
*
/


 
 
.
p
r
i
o
r
i
t
y
-
t
a
g
 
{


 
 
 
 
d
i
s
p
l
a
y
:
 
n
o
n
e
;


 
 
}




 
 
/
*
 
隐
藏
按
钮
文
字
，
只
留
图
标
 
*
/


 
 
.
b
t
n
-
t
e
x
t
 
{


 
 
 
 
d
i
s
p
l
a
y
:
 
n
o
n
e
;


 
 
}




 
 
/
*
 
进
度
文
字
简
化
 
*
/


 
 
.
p
r
o
g
r
e
s
s
-
t
e
x
t
 
{


 
 
 
 
f
o
n
t
-
s
i
z
e
:
 
1
0
p
x
;


 
 
}


}




/
*
 
媒
体
查
询
 
-
 
手
机
 
(
4
8
0
p
x
以
下
)
 
*
/


@
m
e
d
i
a
 
(
m
a
x
-
w
i
d
t
h
:
 
4
8
0
p
x
)
 
{


 
 
.
p
r
o
j
e
c
t
-
m
a
n
a
g
e
m
e
n
t
-
c
o
n
t
a
i
n
e
r
 
{


 
 
 
 
p
a
d
d
i
n
g
:
 
5
p
x
;


 
 
}




 
 
.
g
a
n
t
t
-
c
o
n
t
a
i
n
e
r
,
 
.
t
a
s
k
-
t
r
e
e
-
c
o
n
t
a
i
n
e
r
 
{


 
 
 
 
h
e
i
g
h
t
:
 
2
5
0
p
x
;
 
/
*
 
手
机
进
一
步
缩
小
高
度
 
*
/


 
 
}




 
 
/
*
 
表
格
列
优
化
 
*
/


 
 
:
d
e
e
p
(
.
e
l
-
t
a
b
l
e
-
c
o
l
u
m
n
-
-
w
i
d
t
h
-
1
0
0
)
 
{


 
 
 
 
w
i
d
t
h
:
 
8
0
p
x
 
!
i
m
p
o
r
t
a
n
t
;


 
 
}




 
 
:
d
e
e
p
(
.
e
l
-
t
a
b
l
e
-
c
o
l
u
m
n
-
-
w
i
d
t
h
-
8
0
)
 
{


 
 
 
 
w
i
d
t
h
:
 
6
0
p
x
 
!
i
m
p
o
r
t
a
n
t
;


 
 
}




 
 
/
*
 
树
形
节
点
进
一
步
简
化
 
*
/


 
 
.
n
o
d
e
-
l
e
f
t
 
{


 
 
 
 
g
a
p
:
 
4
p
x
;


 
 
}




 
 
.
n
o
d
e
-
a
c
t
i
o
n
s
 
{


 
 
 
 
g
a
p
:
 
2
p
x
;


 
 
}


}


.
t
a
b
l
e
-
o
p
e
r
a
t
i
o
n
-
b
u
t
t
o
n
s
 
{


 
 
d
i
s
p
l
a
y
:
 
f
l
e
x
;


 
 
g
a
p
:
 
8
p
x
;
 
/
*
 
按
钮
之
间
的
间
距
 
*
/


 
 
w
h
i
t
e
-
s
p
a
c
e
:
 
n
o
w
r
a
p
;
 
/
*
 
禁
止
按
钮
内
文
字
换
行
 
*
/


 
 
a
l
i
g
n
-
i
t
e
m
s
:
 
c
e
n
t
e
r
;
 
/
*
 
垂
直
居
中
对
齐
 
*
/


}




/
*
 
可
选
：
响
应
式
隐
藏
按
钮
文
字
（
小
屏
幕
只
显
示
图
标
）
 
*
/


@
m
e
d
i
a
 
(
m
a
x
-
w
i
d
t
h
:
 
7
6
8
p
x
)
 
{


 
 
.
b
t
n
-
t
e
x
t
 
{


 
 
 
 
d
i
s
p
l
a
y
:
 
n
o
n
e
;


 
 
}


 
 
.
t
a
b
l
e
-
o
p
e
r
a
t
i
o
n
-
b
u
t
t
o
n
s
 
{


 
 
 
 
g
a
p
:
 
4
p
x
;


 
 
}


}


<
/
s
t
y
l
e
>


