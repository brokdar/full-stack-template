import { HttpResponse, http } from "msw";

const API = "http://localhost:8000/api/v1";

/** Default happy-path handlers. Override per-test with server.use(...). */
export const handlers = [
  http.get(`${API}/items`, () =>
    HttpResponse.json({
      items: [
        {
          id: "0198c5b6-0000-7000-8000-000000000001",
          name: "First item",
          description: "from msw",
          created_at: "2026-01-01T00:00:00Z",
          updated_at: "2026-01-01T00:00:00Z",
        },
      ],
      total: 1,
      offset: 0,
      limit: 50,
    }),
  ),
];
