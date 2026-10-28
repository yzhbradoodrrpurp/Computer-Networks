if(ipc.network().getDeviceCount()!==0)throw new Error("Use a new blank project.");
var ws=ipc.appWindow().getActiveWorkspace().getLogicalWorkspace();
var pn=ws.addDevice(8,"PC-PT",300,250);var pc=ipc.network().getDevice(pn);pc.setName("PC-2023141220023");
var dn=ws.addDevice(9,"Server-PT",750,150);var dns=ipc.network().getDevice(dn);dns.setName("DNS-2023141220023");
var hn=ws.addDevice(9,"Server-PT",750,400);var host=ipc.network().getDevice(hn);host.setName("HOST-2023141220023");
var sn=ws.addDevice(1,"Switch-PT",500,250);var sw=ipc.network().getDevice(sn);sw.setName("SW-2023141220023");
dprint("PC="+pc.getPorts());dprint("DNS="+dns.getPorts());dprint("SW="+sw.getPorts());
