from custom_practice.runner import Case


CUSTOMERS = (
    "id,name,order",
    "c1,Ada,10",
    "c2,Linus,2",
    "c3,Grace,7",
)

PROCESSORS = (
    "id,status,order",
    "c1,paid,20",
    "c2,failed,5",
)


TEST_CASES = [
    Case(
        name="left join keeps unmatched customer and sorts numerically",
        args=("id", CUSTOMERS, PROCESSORS, False),
        expected=[
            "id,name,order,id,status,order",
            "c2,Linus,2,c2,failed,5",
            "c3,Grace,7,,,",
            "c1,Ada,10,c1,paid,20",
        ],
    ),
    Case(
        name="skip unmatched gives inner join",
        args=("id", CUSTOMERS, PROCESSORS, True),
        expected=[
            "id,name,order,id,status,order",
            "c2,Linus,2,c2,failed,5",
            "c1,Ada,10,c1,paid,20",
        ],
    ),
    Case(
        name="one-to-many processor matches use processor numeric order",
        args=(
            "id",
            ("id,name,order", "x,A,1"),
            (
                "id,status,order",
                "x,last,100",
                "x,first,3",
                "x,middle,20",
            ),
            False,
        ),
        expected=[
            "id,name,order,id,status,order",
            "x,A,1,x,first,3",
            "x,A,1,x,middle,20",
            "x,A,1,x,last,100",
        ],
    ),
    Case(
        name="duplicate customer keys expand independently",
        args=(
            "id",
            ("id,name,order", "x,B,2", "x,A,1"),
            ("id,status,order", "x,ok,9"),
            False,
        ),
        expected=[
            "id,name,order,id,status,order",
            "x,A,1,x,ok,9",
            "x,B,2,x,ok,9",
        ],
    ),
    Case(
        name="ties preserve customer then processor source order",
        args=(
            "key",
            ("key,value,order", "x,first,1", "x,second,1"),
            ("key,result,order", "x,p1,4", "x,p2,4"),
            False,
        ),
        expected=[
            "key,value,order,key,result,order",
            "x,first,1,x,p1,4",
            "x,first,1,x,p2,4",
            "x,second,1,x,p1,4",
            "x,second,1,x,p2,4",
        ],
    ),
    Case(
        name="empty processor data keeps header and left rows",
        args=(
            "id",
            ("id,name,order", "a,A,1"),
            ("id,status,order",),
            False,
        ),
        expected=[
            "id,name,order,id,status,order",
            "a,A,1,,,",
        ],
    ),
    Case(
        name="empty processor data with skip returns header only",
        args=(
            "id",
            ("id,name,order", "a,A,1"),
            ("id,status,order",),
            True,
        ),
        expected=["id,name,order,id,status,order"],
    ),
]
