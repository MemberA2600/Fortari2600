
pacal = """do=[for perform],[common],command,end,None,[],None,None,None
do-while=[for-while perform-while],[common],command,end,brackets,[],[statement],read,None
do-until=[for-until perform-until],[common],command,end,brackets,[],[statement],read,None
do-times=[for-until perform-until],[common],command,end,brackets,[],[number|stringConst variable],write,None
do-items=[for-items perform-items foreach],[common],command,end,brackets,[],[array],item,None
cycle=[continue next],[common],command,None,None,[],None,None,None
exit=[break next-sentence],[common],command,None,None,[],None,None,None
subroutine=[procedure subr proc],[common],command,end,brackets,[subroutines],[string],None,0
return=[],[common],command,None,brackets,[subroutines],[number|variable|stringConst],read,None
call=[exec execute],[common],command,None,brackets,[],[subroutine {variable}],write,None
set=[],[common],command,None,brackets,[],[variable number|variable|stringConst],write,None
const=[constant],[common],command,None,brackets,[enter],[string number],None,None
select=[switch evaluate],[common],command,end,brackets,[],[variable|stringConst|number],read,None
case=[when],[common],command,None,brackets,[],[variable|number|statement|stringConst],read,None
default=[other else],[common],command,None,brackets,[],[variable|number|statement|stringConst],read,None
asm=[assembly],[common],command,None,brackets,[],[string {string}],None,None
calc=[calculate compute comp],[common],command,None,brackets,[],[variable statement],write,None
incr=[increment ++],[common],command,None,brackets,[],[variable],write,None
decr=[decrement --],[common],command,None,brackets,[],[variable],write,None
leave=[],[common],command,None,None,[overscan],None,None,None
goto=[],[common],command,None,None,[leave],[number|stringConst|variable],None,None
screen=[],[common],command,end,brackets,[screenroutines],[string],None,0
add=[addition +],[common],command,None,brackets,[],[variable number|variable|stringConst],None,None,None
sub=[subtract -],[common],command,None,brackets,[],[variable number|variable|stringConst],None,None,None
multi=[multiply *],[common],command,None,brackets,[],[variable number|variable|stringConst],None,None,None
div=[divide /],[common],command,None,brackets,[],[variable number|variable|stringConst {variable}],None,None,None
pow=[power **],[common],command,None,brackets,[],[variable number|variable|stringConst],None,None,None
sqrt=[],[common],command,None,brackets,[],[variable number|variable|stringConst],None,None,None
swap=[],[common],command,None,brackets,[],[variable variable],None,None,None
rand=[random],[common],command,None,brackets,[],[variable number|variable|stringConst number|variable|stringConst],None,None,None
and=[& &&],[common],command,None,brackets,[],[variable number|variable|stringConst],None,None,None
or=[| ||],[common],command,None,brackets,[],[variable number|variable|stringConst],None,None,None
not=[! / ~],[common],command,None,brackets,[],[variable],None,None,None
xor=[eor],[common],command,None,brackets,[],[variable number|variable|stringConst],None,None,None
shiftL=[asl],[common],command,None,brackets,[],[variable],None,None,None
shiftR=[lsr],[common],command,None,brackets,[],[variable],None,None,None
rollL=[rol],[common],command,None,brackets,[],[variable],None,None,None
rollR=[ror],[common],command,None,brackets,[],[variable],None,None,None"""

pacal = pacal.split("\n")
pacal.sort()

pacal = "\n".join(pacal)

print(pacal)