const express = require('express');
const productController = require('../controllers/product.controller');

const router = express.Router();

router.get('/',productController.getProducts);
router.get('/:id', productController.getProductById);
router.post("/", productController.createProduct);


module.exports = router;