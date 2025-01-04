const express = require('express');
const productRoutes = require('./routes/product.route.js');
const dotenv = require('dotenv').config()
const {connectToMongoDB} = require('./database/init.js')


const app = express();

// Middleware
app.use(express.json());

// Routes
app.use("/api/products", productRoutes);

// Connect to MongoDB
connectToMongoDB();


app.listen(3000, () => {
    console.log('Server is running on port 3000.');
});

app.get('/health', (req, res) => {
    res.status(200).json();
});
