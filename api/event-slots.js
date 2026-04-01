const { SquareClient, SquareEnvironment } = require('square');

// Event definitions: slug -> { displayName, total spots }
const EVENTS = {
  'easter-conference-2026': { name: 'Conference Easter Weekend', total: 15 },
  'spring-sweets-2026':     { name: 'Spring Sweets',             total: 15 },
  'mothers-day-2026':       { name: "Mother's Day",              total: 15 },
};

module.exports = async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Cache for 60 seconds to avoid hammering Square API
  res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=120');

  const isSandbox = process.env.SQUARE_ENVIRONMENT !== 'production';
  const token = isSandbox
    ? (process.env.SQUARE_ACCESS_TOKEN_SANDBOX || process.env.SQUARE_ACCESS_TOKEN)
    : (process.env.SQUARE_ACCESS_TOKEN_PROD || process.env.SQUARE_ACCESS_TOKEN);
  const client = new SquareClient({
    token,
    environment: isSandbox ? SquareEnvironment.Sandbox : SquareEnvironment.Production,
  });

  // Build default result with 0 claimed
  const result = {};
  for (const [slug, info] of Object.entries(EVENTS)) {
    result[slug] = { name: info.name, claimed: 0, total: info.total };
  }

  try {
    // Count unique orders per event by searching completed and open orders
    let cursor = null;

    do {
      const searchBody = {
        locationIds: [process.env.SQUARE_LOCATION_ID],
        query: {
          filter: {
            stateFilter: {
              states: ['OPEN', 'COMPLETED'],
            },
          },
          sort: {
            sortField: 'CREATED_AT',
            sortOrder: 'DESC',
          },
        },
        returnEntries: false,
        limit: 100,
      };

      if (cursor) {
        searchBody.cursor = cursor;
      }

      const response = await client.orders.search(searchBody);

      const orders = response.orders || [];
      for (const order of orders) {
        const meta = order.metadata;
        if (!meta || !meta.event) continue;

        const eventSlug = meta.event;
        if (result[eventSlug]) {
          result[eventSlug].claimed += 1;
        }
      }

      cursor = response.cursor || null;
    } while (cursor);

    // Cap claimed at total
    for (const slug of Object.keys(result)) {
      if (result[slug].claimed > result[slug].total) {
        result[slug].claimed = result[slug].total;
      }
    }

    return res.status(200).json(result);
  } catch (error) {
    console.error('Square SearchOrders Error:', JSON.stringify(error, null, 2));
    // Return defaults (0 claimed) on error so frontend still works
    return res.status(200).json(result);
  }
};
