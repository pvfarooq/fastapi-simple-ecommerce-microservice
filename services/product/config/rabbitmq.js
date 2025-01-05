const rabbit = require('amqplib');
const {deductProductStock} = require('../consumers/productStockHandler.js');


const ROUTING_KEY = 'product_queue';

const createRabbitMQConnection = async () => {
    try {
        const conn = await rabbit.connect('amqp://product_service:guest@rabbitmq:5672');
        console.log('RabbitMQ connection established 🐰');

        const channel = await conn.createChannel();
        await channel.assertQueue(ROUTING_KEY, { durable: false });

        channel.consume(
            ROUTING_KEY,
            (msg) => {
                try {
                    if (!msg) {
                        console.error('Received empty message');
                        return;
                    }

                    const message = JSON.parse(msg.content.toString());
                    const event = message.event;

                    switch (event) {
                        case 'product_stock_reduction':
                            deductProductStock(message.product_id, message.quantity);
                            break;
                        default:
                            console.warn('Unknown event:', event);
                    }
                } catch (consumeErr) {
                    console.error('Error processing message:', consumeErr);
                }
            },
            { noAck: true }
        );

        console.log("Consumer is waiting for messages in the queue...");
        return conn;
    } catch (err) {
        console.error('Error connecting to RabbitMQ:');
        // err -> (log me)
        // throw err; 
    }
};

module.exports = createRabbitMQConnection;