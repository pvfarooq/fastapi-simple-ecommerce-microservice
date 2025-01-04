const mongoose = require('mongoose');


const connectToMongoDB = async () => {
    try {
        const MONGODB_URI = process.env.MONGODB_URI;
        await mongoose.connect(MONGODB_URI);
        console.log('Connected to products database ✅');
    } catch (error) {
        console.log('Failed to connect to DB ❌');
    }
}

module.exports = {connectToMongoDB};