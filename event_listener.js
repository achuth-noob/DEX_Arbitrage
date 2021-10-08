const cpr = require('child_process');
const Web3 = require('web3');
const web3 = new Web3('wss://mainnet.infura.io/ws/v3/b217b1509fa24c9e8bfcb9d8bdabfa41');
const topics_list = [
'0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1'
];
const redis = require('redis');
const client = redis.createClient({
    host: 'localhost',
    port: 6379,
    db:1
});

client.on('connect', function() {
    console.log('Connected to Redis.......');
});

var entries = 0;
web3.eth.subscribe('logs', {
    'topics': topics_list
}, 
    (err,events) => {
        if(err){
            console.log(err)
        }
        if(events.removed===false){
            console.log(Date.now(),events.blockNumber)
            entries=client.get('Cachedentries')+1;
            client.rpush(['id', entries], function(err, reply) {

            });
            client.set(['Cachedentries', entries], function(err, reply){

            });
            client.rpush(['timestamp', Date.now()], function(err, reply) {

            });
            client.set(['lastupdate', Date.now()], function(err, reply) {
                // Emit event in case of less duration 
                // between blocks to cancel the response.
            });
            client.rpush(['data',events.data], function(err, reply){
                // console.log(decode_data(events.data));
            });
            client.rpush(['blocknumber', events.blockNumber], function(err, reply){

            });
            client.set(['latestblock', events.blockNumber], function(err, reply){

            });
            client.rpush(['address', events.address], function(err, reply){

            });
            // client.rpush(['topics', events.topics[0]], function(err, reply){

            // });
        }
    }
);