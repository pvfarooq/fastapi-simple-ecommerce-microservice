const Product = require("../models/product.model.js");

const deductProductStock = async (productId, quantity) => {
    console.log(`Deducting stock for product ${productId} by ${quantity}`);

    try{
        const product = await Product.findById(productId);
        
        if(!product){
            throw new Error('Product not found');
        }

        if(product.stock < quantity){
            throw new Error('Insufficient stock');
        }

        product.stock -= quantity;
        await product.save();
        return product;
    }
    catch(e){
        throw e;
    }
}

module.exports = {deductProductStock};