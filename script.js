// Contract configuration
const contractAddress = "0xdC0Fb4B0fe1b236BcC3B3e92593A0Cc8c9f30587";  // Replace with your deployed contract address
const contractABI = [

	{
		"inputs": [
			{
				"internalType": "string",
				"name": "productId",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "manufacturer",
				"type": "string"
			}
		],
		"name": "addProduct",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "productId",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "manufacturer",
				"type": "string"
			}
		],
		"name": "ProductAdded",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "productId",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "bool",
				"name": "isAuthentic",
				"type": "bool"
			}
		],
		"name": "ProductVerified",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "admin",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "getProductByIndex",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getProductCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "productIds",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "products",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "manufacturer",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "isAuthentic",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "productId",
				"type": "string"
			}
		],
		"name": "verifyProduct",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
];  // Replace with your contract ABI

let web3;
let contract;
let adminAddress;
let currentAccount;

// Initialize the application
window.addEventListener("load", async () => {
    if (window.ethereum) {
        web3 = new Web3(window.ethereum);
        try {
            await ethereum.request({ method: "eth_requestAccounts" });
            contract = new web3.eth.Contract(contractABI, contractAddress);
            
            // Get the admin address from the contract
            adminAddress = await contract.methods.admin().call();
            
            // Log contract info for debugging
            logContractInfo();

            // Connect wallet and update UI
            await connectWallet();
            
            // Test contract connection
            await testContractConnection();
        } catch (error) {
            console.error("Error initializing:", error);
            // alert("Error initializing the application. Please check the console for details.");
        }
    } else {
        alert("MetaMask is not installed. Please install MetaMask to use this application.");
    }
});

// Wallet connection function
async function connectWallet() {
    try {
        const accounts = await web3.eth.getAccounts();
        currentAccount = accounts[0];

        if (currentAccount) {
            // Enable account selection
            const accountSelect = document.getElementById("accountSelect");
            accountSelect.innerHTML = "<option value=''>--Select Account--</option>";
            accounts.forEach((account) => {
                const option = document.createElement("option");
                option.value = account;
                option.innerText = `${account.substring(0, 6)}...${account.substring(38)}`;
                accountSelect.appendChild(option);
            });
            accountSelect.value = currentAccount;
            accountSelect.disabled = false;
            
            // Update user role display
            const userRole = document.getElementById("userRole");
            const isAdmin = currentAccount.toLowerCase() === adminAddress.toLowerCase();
            userRole.textContent = isAdmin ? "Role: Admin" : "Role: User";
            userRole.style.color = isAdmin ? "#4CAF50" : "#2196F3";

            // Show/hide appropriate sections
            document.getElementById("adminSection").style.display = isAdmin ? "block" : "none";
            document.getElementById("userSection").style.display = "block";

            // Load the products list
            await loadProducts();
        }
    } catch (error) {
        console.error("Error connecting wallet:", error);
        alert("Error connecting wallet. Please check the console for details.");
    }
}

// Account switching function
async function switchAccount() {
    const selectedAccount = document.getElementById("accountSelect").value;
    if (selectedAccount) {
        currentAccount = selectedAccount;
        const isAdmin = currentAccount.toLowerCase() === adminAddress.toLowerCase();
        
        // Update UI based on new account
        document.getElementById("adminSection").style.display = isAdmin ? "block" : "none";
        document.getElementById("userRole").textContent = isAdmin ? "Role: Admin" : "Role: User";
        
        await loadProducts();
    }
}

// Product addition function
async function addProduct() {
    const productId = document.getElementById("productId").value.trim();
    const name = document.getElementById("productName").value.trim();
    const manufacturer = document.getElementById("manufacturer").value.trim();
    const addProductError = document.getElementById("addProductError");
    const addButton = document.querySelector('#adminSection button');

    try {
        // Validate inputs
        if (!productId || !name || !manufacturer) {
            addProductError.textContent = "All fields are required.";
            return;
        }

        // Show loading state
        addButton.disabled = true;
        addButton.textContent = 'Adding Product...';

        // Send transaction
        const transaction = await contract.methods.addProduct(productId, name, manufacturer)
            .send({ 
                from: currentAccount,
                gas: 200000 
            });

        console.log("Transaction successful:", transaction);
        
        // Clear input fields
        document.getElementById("productId").value = '';
        document.getElementById("productName").value = '';
        document.getElementById("manufacturer").value = '';
        addProductError.textContent = '';
        
        // Refresh product list
        await loadProducts();
        
        alert("Product added successfully!");
    } catch (error) {
        console.error("Error in addProduct:", error);
        addProductError.textContent = `Error: ${error.message}`;
    } finally {
        // Reset button state
        addButton.disabled = false;
        addButton.textContent = 'Add Product';
    }
}

// Product loading function
async function loadProducts() {
    const tableBody = document.getElementById("productTableBody");
    tableBody.innerHTML = '';

    try {
        const productCount = parseInt(await contract.methods.getProductCount().call());
        console.log("Product Count:", productCount);

        if (productCount === 0) {
            tableBody.innerHTML = '<tr><td colspan="3" class="text-center">No products found</td></tr>';
            return;
        }

        for (let i = 0; i < productCount; i++) {
            try {
                const productData = await contract.methods.getProductByIndex(i).call();
                console.log("Product Data for index", i, ":", productData);

                const row = tableBody.insertRow();
                row.insertCell(0).textContent = productData[0] || 'N/A'; // Product ID
                row.insertCell(1).textContent = productData[1] || 'N/A'; // Name
                row.insertCell(2).textContent = productData[2] || 'N/A'; // Manufacturer
            } catch (productError) {
                console.error(`Error loading product at index ${i}:`, productError);
            }
        }
    } catch (error) {
        console.error("Error in loadProducts:", error);
        tableBody.innerHTML = `
            <tr>
                <td colspan="3" class="text-center text-red-500">
                    Error loading products: ${error.message}
                </td>
            </tr>`;
    }
}

// Product verification function
// Product verification function
async function verifyProduct() {
    const productId = document.getElementById("verifyProductId").value.trim();
    const verifyResult = document.getElementById("verifyResult");

    try {
        if (!productId) {
            verifyResult.textContent = "Please enter a Product ID";
            verifyResult.style.color = "red";
            return;
        }

        const isAuthentic = await contract.methods.verifyProduct(productId).call();
        
        if (isAuthentic) {
            // Get product details
            const productCount = await contract.methods.getProductCount().call();
            let productDetails = null;
            
            for (let i = 0; i < productCount; i++) {
                const productData = await contract.methods.getProductByIndex(i).call();
                // Check if the returned productData contains the matching productId
                if (productData && productData[0] === productId) {
                    productDetails = {
                        name: productData[1],
                        manufacturer: productData[2]
                    };
                    break;
                }
            }

            if (productDetails) {
                verifyResult.innerHTML = `
                    <span style="color: #4CAF50">✅ Product is authentic!</span><br>
                    <strong>Name:</strong> ${productDetails.name}<br>
                    <strong>Manufacturer:</strong> ${productDetails.manufacturer}
                `;
                verifyResult.style.color = "black";
            } else {
                verifyResult.textContent = "✅ Product is authentic (details unavailable)";
                verifyResult.style.color = "#4CAF50";
            }
        } else {
            verifyResult.textContent = "❌ Product is not authentic or does not exist";
            verifyResult.style.color = "red";
        }
    } catch (error) {
        console.error("Error in verifyProduct:", error);
        verifyResult.textContent = "Error: Could not verify product. Please try again.";
        verifyResult.style.color = "red";
    }
}