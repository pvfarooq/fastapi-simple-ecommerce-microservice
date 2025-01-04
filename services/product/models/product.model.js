const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, 'Product name is required']
    },
    price: {
        type: Number,
        required: [true, 'Product price is required']
    },
    stock:{
        type: Number,
        default: 0
    },
    description: {
        type: String
    },
    image: {
        type: String
    },
    category: {
        type: String
    },
}, {timestamps: true});

module.exports = mongoose.model('Product', productSchema);