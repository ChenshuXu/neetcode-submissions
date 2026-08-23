from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="route returns distance and healthy attempt order as capacity fills",
        args=((
            "REGISTER,us-west,38,-122,2",
            "REGISTER,us-east,41,-74,100",
            "ROUTE,38,-122",
            "ROUTE,38,-122",
            "ROUTE,38,-122",
        ),),
        expected=[
            "OK",
            "OK",
            "us-west 0 us-west,us-east",
            "us-west 0 us-west,us-east",
            "us-east 4080 us-west,us-east",
        ],
    ),
    Case(
        name="unhealthy nearest target is skipped",
        args=((
            "REGISTER,a,0,0,2",
            "REGISTER,b,0,1,2",
            "SET_HEALTHY,a,false",
            "ROUTE,0,0",
        ),),
        expected=["OK", "OK", "OK", "b 111 b"],
    ),
    Case(
        name="all unhealthy or full returns none",
        args=((
            "REGISTER,a,0,0,1",
            "ROUTE,0,0",
            "ROUTE,0,0",
            "SET_HEALTHY,a,false",
            "ROUTE,0,0",
        ),),
        expected=["OK", "a 0 a", "NONE a", "OK", "NONE"],
    ),
    Case(
        name="invalid registration is atomic and name remains available",
        args=((
            "REGISTER,bad,91,0,1",
            "REGISTER,bad,0,0,1",
            "REGISTER,bad,1,1,2",
            "REGISTER,zero,0,0,0",
        ),),
        expected=["ERROR", "OK", "ERROR", "ERROR"],
    ),
    Case(
        name="coordinate boundaries are accepted",
        args=((
            "REGISTER,north,90,180,1",
            "REGISTER,south,-90,-180,1",
            "ROUTE,90,180",
        ),),
        expected=["OK", "OK", "north 0 north,south"],
    ),
    Case(
        name="distance command uses rounded haversine kilometers",
        args=((
            "DISTANCE,0,0,0,0",
            "DISTANCE,38,-122,41,-74",
            "DISTANCE,0,0,10,0",
            "DISTANCE,36,140,-33,-71",
        ),),
        expected=["0", "4080", "1112", "17167"],
    ),
    Case(
        name="equal distance tie uses datacenter name",
        args=((
            "REGISTER,b,0,1,1",
            "REGISTER,a,0,-1,1",
            "ROUTE,0,0",
        ),),
        expected=["OK", "OK", "a 111 a,b"],
    ),
    Case(
        name="unknown names invalid booleans and malformed commands error",
        args=((
            "SET_HEALTHY,missing,true",
            "REGISTER,a,0,0,1",
            "SET_HEALTHY,a,yes",
            "DISTANCE,0,0,0",
            "ROUTE,0,181",
        ),),
        expected=["ERROR", "OK", "ERROR", "ERROR", "ERROR"],
    ),
]
