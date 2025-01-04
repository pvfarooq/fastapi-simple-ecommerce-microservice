const rabbit = require('amqplib');

const {deductProductStock} = require('../consumers/productStockHandler.js');

const ROUTING_KEY = 'product_queue';


const createRabbitMQConnection = async () => {
    try{
        const rabbitmqConnection = rabbit.connect('amqp://product_service:guest@rabbitmq:5672');
        rabbitmqConnection.then(async (conn)=>{
            const channel = await conn.createChannel();
            await channel.assertQueue(ROUTING_KEY, {durable: false});
            console.log('RabbitMQ connection established 🐰');

            channel.consume(ROUTING_KEY, (msg) => {
                const message = JSON.parse(msg.content.toString());
                const event = message.event;

                switch(event){
                    case 'product_stock_reduction':
                        deductProductStock(message.product_id, message.quantity);
                        break;
                    default:
                        console.log('Unknown event');
                }

            }, {noAck: true});

            console.log("Consumer is waiting for messages in the queue...");
        });
        return rabbitmqConnection;
    }catch(e){
        console.log('Error connecting to RabbitMQ', e);
    }
}


module.exports = createRabbitMQConnection;