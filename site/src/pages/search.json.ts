/**
 * Exposes the search index as a JSON endpoint at /search.json
 * so the client-side search can fetch it on demand.
 */
import type { APIRoute } from 'astro';
import { getSearchIndex } from '../lib/data';

export const GET: APIRoute = () => {
  const index = getSearchIndex();
  return new Response(JSON.stringify(index), {
    headers: { 'Content-Type': 'application/json' },
  });
};
