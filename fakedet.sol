// SPDX-License-Identifier: MIT
pragma solidity ^0.8.14;

contract FakeProductIdentification {

    address public admin;

    struct Product {
        string name;
        string manufacturer;
        bool isAuthentic;
    }

    // Mapping productId to Product struct
    mapping(string => Product) public products;
    string[] public productIds;

    event ProductAdded(string productId, string name, string manufacturer);
    event ProductVerified(string productId, bool isAuthentic);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    // Add a product
    function addProduct(
        string memory productId,
        string memory name,
        string memory manufacturer
    ) public onlyAdmin {
        require(bytes(products[productId].name).length == 0, "Product already exists");
        products[productId] = Product(name, manufacturer, true);
        productIds.push(productId);  // Store product ID in the array
        emit ProductAdded(productId, name, manufacturer);
    }

    // Get product count
    function getProductCount() public view returns (uint) {
        return productIds.length;
    }

    // Get product by index
    function getProductByIndex(uint index) public view returns (string memory, string memory, string memory) {
        require(index < productIds.length, "Product index out of bounds");
        string memory productId = productIds[index];
        Product memory product = products[productId];
        return (productId, product.name, product.manufacturer);
    }

    // Verify product authenticity
    function verifyProduct(string memory productId) public view returns (bool) {
        return products[productId].isAuthentic;
    }
}
