const { SquareClient, SquareEnvironment } = require('square');
const crypto = require('crypto');

// Product catalog with prices in cents
const PRODUCTS = {
  "Grandma's Dinner Rolls":       { price: 2200, unit: 'dozen' },
  "Cinnamon Rolls":                { price: 4800, unit: 'dozen' },
  "Crescent Rolls":                { price: 2200, unit: 'dozen' },
  "Cheese Rolls":                  { price: 2500, unit: 'dozen' },
  "Mom's Wheat Bread":             { price: 1000, unit: 'loaf' },
  "Soft French Bread":             { price: 700, unit: 'loaf' },
  "Cookie Dough Brownies":         { price: 2400, unit: '8x8 pan' },
  "Peanut Butter Bars":            { price: 2000, unit: '8x8 pan' },
  "Lemon Bars":                    { price: 2000, unit: '8x8 pan' },
  "Caramel Rice Krispie Treats":   { price: 2000, unit: '8x8 pan' },
  "Chocolate Dipped Strawberries": { price: 3600, unit: 'dozen' },
  "Chocolate Covered Grapes – Dessert Cup": { price: 600, unit: 'dessert cup (approx. 10 grapes)' },
  "Homemade Oreo Cookies":         { price: 3600, unit: 'dozen' },
};

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { name, phone, event, items, quantities, notes } = req.body;

  if (!name || !phone || !event || !items || !quantities) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  // Build line items from selected products and quantities
  const lineItems = [];
  const itemList = Array.isArray(items) ? items : [items];
  const qtyList = Array.isArray(quantities) ? quantities : [quantities];

  for (let i = 0; i < itemList.length; i++) {
    const product = PRODUCTS[itemList[i]];
    if (!product) continue;

    const qty = parseInt(qtyList[i]) || 1;
    lineItems.push({
      name: itemList[i],
      quantity: String(qty),
      basePriceMoney: {
        amount: BigInt(product.price),
        currency: 'USD',
      },
      note: `${qty} ${product.unit}`,
    });
  }

  if (lineItems.length === 0) {
    return res.status(400).json({ error: 'No valid items selected' });
  }

  // Determine Square environment
  const isSandbox = process.env.SQUARE_ENVIRONMENT !== 'production';
  const token = isSandbox
    ? (process.env.SQUARE_ACCESS_TOKEN_SANDBOX || process.env.SQUARE_ACCESS_TOKEN)
    : (process.env.SQUARE_ACCESS_TOKEN_PROD || process.env.SQUARE_ACCESS_TOKEN);
  const client = new SquareClient({
    token,
    environment: isSandbox ? SquareEnvironment.Sandbox : SquareEnvironment.Production,
  });

  const baseUrl = process.env.VERCEL_PROJECT_PRODUCTION_URL
    ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`
    : `https://${req.headers.host}`;

  try {
    const response = await client.checkout.paymentLinks.create({
      idempotencyKey: crypto.randomUUID(),
      order: {
        locationId: process.env.SQUARE_LOCATION_ID,
        lineItems: lineItems,
        metadata: Object.assign(
          { customer_name: name, customer_phone: phone, event: event },
          notes ? { notes: notes } : {}
        ),
      },
      checkoutOptions: {
        redirectUrl: `${baseUrl}/order-confirmed.html`,
        askForShippingAddress: false,
        merchantSupportEmail: 'kathleens.kitchen.ut@gmail.com',
        allowTipping: false,
      },
      prePopulatedData: {
        buyerPhone: phone,
      },
    });

    return res.status(200).json({
      checkoutUrl: response.paymentLink.url,
      orderId: response.paymentLink.orderId,
    });
  } catch (error) {
    console.error('Square Checkout Error:', JSON.stringify(error, null, 2));
    return res.status(500).json({
      error: 'Failed to create checkout session',
      details: isSandbox ? (error.message || JSON.stringify(error)) : undefined,
    });
  }
};
