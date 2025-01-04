const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const dotenv = require('dotenv').config()

const productRoutes = require('./routes/product.route.js');
const {connectToMongoDB} = require('./database/init.js')

const PORT = process.env.PORT || 8008;

const app = express();

// Middleware
app.use(express.json());
app.use(helmet());
app.use(cors());

// Routes
app.use("/api/products", productRoutes);

// Connect to MongoDB
connectToMongoDB();

app.get('/health', (req, res) => {
    res.status(200).json({
        status: 'UP',
        version: process.env.npm_package_version || '1.0.0'
    });
});


app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

process.on('SIGINT', async () => {
    console.log('Shutting down server...');
    process.exit(0);
});

app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ message: 'Internal Server Error' });
});