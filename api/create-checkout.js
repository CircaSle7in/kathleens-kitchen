const { SquareClient, SquareEnvironment } = require('square');
const crypto = require('crypto');

// Product catalog with prices in cents
const PRODUCTS = {
  "Grandma's Rolls":           { price: 2200, unit: 'dozen' },
  "Cinnamon Rolls":            { price: 4800, unit: 'dozen' },
  "Crescent Rolls":            { price: 2400, unit: 'dozen' },
  "Cheese Rolls":              { price: 2800, unit: 'dozen' },
  "Dinner Rolls":              { price: 2000, unit: 'dozen' },
  "Cookie Dough Brownies":     { price: 4800, unit: 'dozen' },
  "Peanut Butter Bars":        { price: 4200, unit: 'dozen' },
  "Lemon Bars":                { price: 4200, unit: 'dozen' },
  "Caramel Rice Krispie Treats": { price: 3600, unit: 'dozen' },
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
  const client = new SquareClient({
    token: process.env.SQUARE_ACCESS_TOKEN,
    environment: isSandbox ? SquareEnvironment.Sandbox : SquareEnvironment.Production,
  });

  const baseUrl = process.env.VERCEL_PROJECT_PRODUCTION_URL
    ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`
    : `https://${req.headers.host}`;

  try {
    const response = await client.checkout.createPaymentLink({
      idempotencyKey: crypto.randomUUID(),
      order: {
        locationId: process.env.SQUARE_LOCATION_ID,
        lineItems: lineItems,
        metadata: {
          customer_name: name,
          customer_phone: phone,
          event: event,
          notes: notes || '',
        },
      },
      checkoutOptions: {
        redirectUrl: `${baseUrl}/order-confirmed.html`,
        askForShippingAddress: false,
        merchantSupportEmail: 'kathleens.kitchen.ut@gmail.com',
        allowTipping: true,
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
    console.error('Square Checkout Error:', error);
    return res.status(500).json({
      error: 'Failed to create checkout session',
      details: isSandbox ? error.message : undefined,
    });
  }
};
