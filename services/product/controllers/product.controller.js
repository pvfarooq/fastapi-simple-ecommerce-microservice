const Product = require('../models/product.model.js');

const getProducts = async (req, res) => {
    try{
        const products = await Product.find();
        res.status(200).json({products});
    }catch(error){
        res.status(400).json({error});
    }
};

const getProductById = async (req, res) => {
    try{
        const {id} = req.params;
        const product = await Product.findById(id);
        res.status(200).json({product});
    }catch(error){
        res.status(400).json({error});
    }
}

const createProduct = async (req, res) => {
    try{
        const product = await Product.create(req.body);
        res.status(201).json({product});
    }
    catch(error){
        res.status(400).json({error});
    }
}

module.exports = {
    getProducts,
    getProductById,
    createProduct
};
