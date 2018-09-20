
action=start
app="bsdstreams-origin/live"
stream=268bf
cdn=11255
pubkey=346EA2FF7E289CEDECA23FA4074C79CC
sekretkey=749040ae5b8fb6b8bcc8a83a5dc13f41071bdbac0ad049b13e73f17aba9b3968

url="https://bsdstreams-origin.secdn.net/serecordcontrols?action=$action&app=$app&stream=$stream&secret=$pubkey"


echo $url

curl $url
